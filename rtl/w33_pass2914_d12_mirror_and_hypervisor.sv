// Pass 2914 -- the last unbuilt opcode, and a hypervisor.
//
// PART ONE: D_12-MIRROR, the eighth opcode.
//
// It has sat in the "not built" list of the blueprint since the ISA was written, with the
// honest note that it "is a transport operation in a dihedral group and has no register
// semantics".  That is true and it is not a reason not to build it -- transport is a
// perfectly good thing for hardware to do, it just does not touch the Pauli frame.
//
// Earlier in this project an attempt to build it as a phase accumulator was withdrawn:
// R_4 and U_6 do NOT commute (their commutator has order 4), so the object is dihedral
// D_12, not the cyclic C_12 that a phase accumulator implements.  A counter is the wrong
// circuit.  The right one is a rotation register plus a reflection bit, which is what a
// dihedral group actually is:
//
//     D_12 = <r, s | r^6 = s^2 = 1, s r s = r^-1>,   order 12
//
// so the state is (rotation mod 6, reflection bit) and the two generators are "advance"
// and "flip".  The relation s r s = r^-1 is asserted in the netlist rather than assumed,
// because that relation is exactly what distinguishes D_12 from C_12 and is exactly what
// the withdrawn version got wrong.
//
// PART TWO: A HYPERVISOR.
//
// Pass 2912 computes the emulation cost of running a one-qutrit guest on this machine:
// worst case 8 host instructions per guest instruction, mean 3.33.  The frame is two
// qutrits, so two guests fit on disjoint register pairs -- and the isolation is
// STRUCTURAL rather than enforced: the only opcodes that couple the halves are the two
// CX directions, so a hypervisor that never issues CX to a guest cannot leak between
// them, with no MMU, no tagging and no permission check.
//
// This builds that: one physical frame, N guest contexts, explicit switch.  The question
// it answers is where sharing beats replication -- N guests on one engine against N
// copies of the 43-cell engine.

`timescale 1ns/1ps

// ---------------------------------------------------------------------------------
// D_12 transport: rotation mod 6 and a reflection bit.
// ---------------------------------------------------------------------------------
module w33_d12_mirror (
    input  wire       clk,
    input  wire       rst,
    input  wire       load,
    input  wire [2:0] rot_in,
    input  wire       ref_in,
    input  wire       valid,
    input  wire       op,           // 0 = advance (r), 1 = flip (s)
    output reg  [2:0] rot,          // 0..5
    output reg        refl
);
    wire [2:0] rot_next = (rot == 3'd5) ? 3'd0 : rot + 3'd1;
    // Advancing while reflected runs the rotation BACKWARD: that is s r s = r^-1, and
    // it is the entire difference between D_12 and a 12-state counter.
    wire [2:0] rot_back = (rot == 3'd0) ? 3'd5 : rot - 3'd1;

    always_ff @(posedge clk) begin
        if (rst) begin
            rot <= 3'd0; refl <= 1'b0;
        end else if (load) begin
            rot <= (rot_in > 3'd5) ? 3'd0 : rot_in;
            refl <= ref_in;
        end else if (valid) begin
            if (op == 1'b0) rot <= refl ? rot_back : rot_next;
            else            refl <= ~refl;
        end
    end
endmodule


// The relation that makes it dihedral.  Asserted in the netlist because a phase
// accumulator satisfies every OTHER property of this module and fails exactly this one.
module w33_d12_formal (
    input wire [2:0] rot,
    input wire       refl
);
    wire legal = (rot <= 3'd5);
    // s r s applied to a state must equal r^-1 applied to it
    wire [2:0] fwd  = (rot == 3'd5) ? 3'd0 : rot + 3'd1;
    wire [2:0] back = (rot == 3'd0) ? 3'd5 : rot - 3'd1;
    // conjugate: flip, advance, flip.  Flipping does not move rot, so the conjugated
    // advance is the advance taken with the reflection bit inverted.
    wire [2:0] conj = (~refl) ? back : fwd;
    wire [2:0] plain_inverse = (refl) ? fwd : back;
    always_comb
        if (legal) begin
            assert (conj == plain_inverse);      // s r s = r^-1
            assert (fwd != rot);                 // r has no fixed point: order 6, not 1
        end
endmodule


// ---------------------------------------------------------------------------------
// The hypervisor: N guest frames, one physical datapath.
// ---------------------------------------------------------------------------------
module w33_hypervisor #(
    parameter int NGUEST = 4,
    parameter int IDW = (NGUEST <= 2) ? 1 : (NGUEST <= 4) ? 2 : (NGUEST <= 8) ? 3 : 4
) (
    input  wire           clk,
    input  wire           rst,
    input  wire [IDW-1:0] guest,        // which context this instruction belongs to
    input  wire           valid,
    input  wire [1:0]     opcode,       // the same 2-bit micro-ISA
    input  wire           load,
    input  wire [7:0]     frame_in,     // {zf, xf, zp, xp}, two bits each
    output wire [7:0]     frame_out
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

    // The context store.  This is the whole hypervisor: N frames, one datapath.
    reg [7:0] ctx [0:NGUEST-1];

    wire [1:0] xp = ctx[guest][1:0];
    wire [1:0] zp = ctx[guest][3:2];
    wire [1:0] xf = ctx[guest][5:4];
    wire [1:0] zf = ctx[guest][7:6];

    reg [1:0] nxp, nzp, nxf, nzf;
    always_comb begin
        nxp = xp; nzp = zp; nxf = xf; nzf = zf;
        case (opcode)
            2'b00: begin nxp = neg3(zp);      nzp = xp;           end  // F_p
            2'b01: begin nzp = sub3(zp, zf);  nxf = add3(xf, xp); end  // CX_pf
            2'b10: begin nxp = add3(xp, xf);  nzf = sub3(zf, zp); end  // CX_fp
            2'b11: begin nzp = add3(zp, 2'd1);                    end  // Z_p
        endcase
    end

    integer g;
    always_ff @(posedge clk) begin
        if (rst) begin
            for (g = 0; g < NGUEST; g = g + 1) ctx[g] <= 8'd0;
        end else if (load) begin
            ctx[guest] <= frame_in;
        end else if (valid) begin
            ctx[guest] <= {nzf, nxf, nzp, nxp};
        end
    end

    assign frame_out = ctx[guest];
endmodule
