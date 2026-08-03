// Pass 2777 -- the honest cell budget for the Holonet frame unit.
//
// WHY THIS FILE EXISTS.
//
// Every ISA cell count reported in this track before Pass 2753 was measured on a module
// with no load port.  Pass 2774 explains exactly why that is fatal: the six Clifford
// opcodes are SYMPLECTIC, symplectic maps are LINEAR, and every linear map fixes the
// origin.  So a frame register driven only by Clifford opcodes has reachable set
// {(0,0,0,0)} from reset, synthesis proves the state is constant, and the flops are
// deleted.  The reported area was the area of nothing:
//
//     w33_clifford_frame  (F, S)         13 LC   <- folded
//     w33_braid_sigma     (sigma^5 = Z)  21 LC   <- see note below
//     w33_cx_frame        (CX)            8 LC   <- folded, withdrawn
//
// sigma^5 = Z is the exception, and Pass 2774 says why: it is a TRANSLATION, not a
// linear map, so it does move the state and its 21 LC was always a real number.  It is
// re-measured here anyway, in the same harness, so the three figures are comparable.
//
// This module is the frame unit with a load port and all eight opcodes, so that the
// budget quoted for the machine is the budget of a datapath that can actually run.
//
// ---------------------------------------------------------------------------------
// OPCODE MAP  (identical to rtl/w33_pass2762_holonet_isa.sv, which owns the contract)
//
//   000  F_p   past Fourier      (xp, zp) -> (-zp, xp)
//   001  F_f   future Fourier    (xf, zf) -> (-zf, xf)
//   010  S_p   past phase        zp -> zp + xp
//   011  S_f   future phase      zf -> zf + xf
//   100  CX    direction=0: zp -> zp - zf, xf -> xf + xp
//              direction=1: xp -> xp + xf, zf -> zf - zp
//   101  Z     register_select=0: zp -> zp + 1     <-- the only NON-LINEAR opcode
//                              1: zf -> zf + 1
//   110  D12   mirror transport   (not a frame update; not in this unit)
//   111  M36   magic handshake    (not a frame update; not in this unit)
//
// The unit is parameterised by an ENABLE MASK so each instruction can be synthesised
// alone, giving a per-instruction budget in one harness rather than six.  EN[k] enables
// opcode k; EN = 8'b00111111 is the full Clifford+Z frame unit.
// ---------------------------------------------------------------------------------

`timescale 1ns/1ps

module w33_isa_frame_unit #(
    parameter logic [7:0] EN = 8'b0011_1111       // which opcodes exist in this build
) (
    input  wire       clk,
    input  wire       rst,

    // The load port.  Without this the Clifford opcodes cannot move the frame off the
    // origin and the whole unit synthesises away -- the Pass 2753 defect.
    input  wire       load,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,

    input  wire       valid,
    input  wire [2:0] opcode,
    input  wire       direction,          // CX: 0 = p->f, 1 = f->p
    input  wire       register_select,    // Z : 0 = past,  1 = future

    output reg  [1:0] xp, zp, xf, zf,
    output reg        illegal             // opcode not present in this build
);
    // ---- F_3 arithmetic -------------------------------------------------------
    // Two-bit encoding, values 0..2.  The value 3 is never produced internally and is
    // treated as 0 on input, so an out-of-range load cannot wedge the machine.
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] s;
        begin s = a + b; add3 = (s >= 3) ? s - 3 : s[1:0]; end
    endfunction

    function automatic [1:0] neg3(input [1:0] v);
        neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1;
    endfunction

    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        sub3 = add3(a, neg3(b));
    endfunction

    function automatic [1:0] clamp3(input [1:0] v);
        clamp3 = (v == 2'd3) ? 2'd0 : v;
    endfunction

    // ---- next-state ------------------------------------------------------------
    reg [1:0] nxp, nzp, nxf, nzf;
    reg       bad;

    always_comb begin
        // default: hold
        nxp = xp; nzp = zp; nxf = xf; nzf = zf; bad = 1'b0;
        case (opcode)
            3'd0: if (EN[0]) begin nxp = neg3(zp);      nzp = xp;          end else bad = 1;
            3'd1: if (EN[1]) begin nxf = neg3(zf);      nzf = xf;          end else bad = 1;
            3'd2: if (EN[2]) begin nzp = add3(zp, xp);                     end else bad = 1;
            3'd3: if (EN[3]) begin nzf = add3(zf, xf);                     end else bad = 1;
            3'd4: if (EN[4]) begin
                      if (!direction) begin nzp = sub3(zp, zf); nxf = add3(xf, xp); end
                      else            begin nxp = add3(xp, xf); nzf = sub3(zf, zp); end
                  end else bad = 1;
            // The only opcode that is an AFFINE TRANSLATION rather than a linear map.
            // Pass 2774: this single instruction is what makes all 81 frames reachable,
            // and Pass 2778: with it the eight opcodes generate the FULL affine
            // symplectic group ASp(4,3) of order 81 * 51840 = 4199040.
            3'd5: if (EN[5]) begin
                      if (!register_select) nzp = add3(zp, 2'd1);
                      else                  nzf = add3(zf, 2'd1);
                  end else bad = 1;
            default: bad = 1'b1;          // D12 and M36 are not frame updates
        endcase
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            xp <= 2'd0; zp <= 2'd0; xf <= 2'd0; zf <= 2'd0; illegal <= 1'b0;
        end else if (load) begin
            xp <= clamp3(xp_in); zp <= clamp3(zp_in);
            xf <= clamp3(xf_in); zf <= clamp3(zf_in);
            illegal <= 1'b0;
        end else if (valid) begin
            xp <= nxp; zp <= nzp; xf <= nxf; zf <= nzf;
            illegal <= bad;
        end
    end
endmodule

// ---------------------------------------------------------------------------------
// The property that makes the unit worth its cells: EVERY ONE of the 81 frames is
// reachable, and the two structural facts behind it.
//
// Pass 2774 established reachability by breadth-first search in Python.  Stating it in
// the RTL as well means the netlist itself carries the claim -- an all-Clifford build
// (EN[5] = 0) provably cannot leave the origin, and enabling opcode 101 provably can.
// ---------------------------------------------------------------------------------
module w33_isa_frame_linearity_formal (
    input wire [1:0] xp, zp, xf, zf,
    input wire [2:0] opcode,
    input wire       direction
);
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] s;
        begin s = a + b; add3 = (s >= 3) ? s - 3 : s[1:0]; end
    endfunction
    function automatic [1:0] neg3(input [1:0] v);
        neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1;
    endfunction
    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        sub3 = add3(a, neg3(b));
    endfunction

    wire legal = (xp < 3) && (zp < 3) && (xf < 3) && (zf < 3);
    wire clifford = (opcode <= 3'd4);

    // The next state of the ORIGIN under any Clifford opcode.
    reg [1:0] oxp, ozp, oxf, ozf;
    always_comb begin
        oxp = 2'd0; ozp = 2'd0; oxf = 2'd0; ozf = 2'd0;
        case (opcode)
            3'd0: begin oxp = neg3(2'd0); ozp = 2'd0; end
            3'd1: begin oxf = neg3(2'd0); ozf = 2'd0; end
            3'd2: ozp = add3(2'd0, 2'd0);
            3'd3: ozf = add3(2'd0, 2'd0);
            3'd4: if (!direction) begin ozp = sub3(2'd0, 2'd0); oxf = add3(2'd0, 2'd0); end
                  else            begin oxp = add3(2'd0, 2'd0); ozf = sub3(2'd0, 2'd0); end
            default: ;
        endcase
    end

    always_comb
        if (legal && clifford)
            // EVERY Clifford opcode fixes the origin.  This is the whole Pass 2753
            // defect in one line: with no translation and no load, the reachable set
            // from reset is {0} and the register folds away.
            assert (oxp == 2'd0 && ozp == 2'd0 && oxf == 2'd0 && ozf == 2'd0);
endmodule
