// Pass 2752 -- a LOADABLE Pauli-frame tracker for the qutrit CX instruction.
//
// PRIOR ART, and this file's reason to exist.
//
// The CX / SUM instruction itself is NOT mine.  `rtl/w33_pass2757_qutrit_cx.sv`
// (parallel track, added 2026-08-03 00:46) owns it: the same Sp(4,3) matrix, the
// same frame map, an exhaustive testbench over all 81^2 pairs, and the W33
// conjugacy certificate (480-class, line profile 1^7 3^11) that identifies it.  I
// derived the same map independently and got the same answer character for
// character -- two independent derivations agreeing is a check, not a discovery,
// and by the repo's ownership rule (earlier file-add wins) the instruction is
// theirs.  My duplicate RTL is withdrawn.
//
// What IS new here is a defect that only synthesis sees.  Their sequential
// wrapper `w33_qutrit_cx_frame` has no load port, so after reset the frame is
// (0,0,0,0) forever:
//
//     xp_out = xp        and     zf_out = zf        (structurally constant)
//     zp_out = zp - zf   = zp    when zf == 0
//     xf_out = xf + xp   = xf    when xp == 0
//
// so the whole state is frozen and the module implements the identity.  Yosys
// proves it -- after `flatten; opt -full` the netlist ends
//
//     assign zf = 2'h0;
//     assign xp = 2'h0;
//
// and 6 of the 8 state flops are deleted.  Their exhaustive testbench does not
// catch this because it drives the COMBINATIONAL modules (`..._frame_map`,
// `..._order3`) directly and never instantiates the sequential wrapper.  The
// combinational map is correct; the tracker built on it cannot be loaded.
//
// My own withdrawn `w33_cx_frame` had exactly the same defect, so the "8 LC,
// 147.08 MHz" figure I measured for it was measuring a folded-away netlist.
// Both numbers were meaningless.  This is a shared blind spot: a frame tracker
// with no load path is measured as free because it is.
//
// This module is the fix -- their exact map, plus the one port that makes it a
// tracker -- so the ISA cell budget has an honest number in it.

`timescale 1ns/1ps

module w33_cx_loadable_frame (
    input  wire       clk,
    input  wire       rst,
    input  wire       load,        // the missing port
    input  wire       apply_cx,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,
    output reg  [1:0] xp, zp, xf, zf
);
    // The map, verbatim from w33_pass2757_qutrit_cx.sv:
    //     (xp, zp, xf, zf) -> (xp, zp - zf, xf + xp, zf)
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] s;
        begin s = a + b; add3 = (s >= 3) ? s - 3 : s[1:0]; end
    endfunction
    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        begin sub3 = add3(a, (b == 2'd0) ? 2'd0 : (b == 2'd1) ? 2'd2 : 2'd1); end
    endfunction

    always_ff @(posedge clk) begin
        if (rst) begin
            xp <= 2'd0; zp <= 2'd0; xf <= 2'd0; zf <= 2'd0;
        end else if (load) begin
            xp <= xp_in; zp <= zp_in; xf <= xf_in; zf <= zf_in;
        end else if (apply_cx) begin
            xp <= xp;
            zp <= sub3(zp, zf);
            xf <= add3(xf, xp);
            zf <= zf;
        end
    end
endmodule

// The property the sequential wrapper must have and the combinational testbench
// cannot check: from ANY loaded frame, three applications restore it.  This is
// the sequential statement of CX^3 = I, which the parallel track proved for the
// map and could not exercise for the tracker.
module w33_cx_loadable_formal (
    input wire        clk,
    input wire [1:0]  xp_in, zp_in, xf_in, zf_in
);
    // Control is COMBINATIONAL in the step counter, so the schedule is exactly
    //     step 0 reset | step 1 load | steps 2,3,4 apply | step 5 check.
    // Registering the control instead costs a cycle and shifts the check one
    // apply too early -- which is how the first version of this proof failed.
    reg [2:0] step = 3'd0;
    wire rst   = (step == 3'd0);
    wire load  = (step == 3'd1);
    wire apply = (step >= 3'd2) && (step <= 3'd4);
    wire [1:0] xp, zp, xf, zf;

    w33_cx_loadable_frame dut (
        .clk(clk), .rst(rst), .load(load), .apply_cx(apply),
        .xp_in(xp_in), .zp_in(zp_in), .xf_in(xf_in), .zf_in(zf_in),
        .xp(xp), .zp(zp), .xf(xf), .zf(zf)
    );

    wire legal = (xp_in < 3) && (zp_in < 3) && (xf_in < 3) && (zf_in < 3);

    // The inputs are free and may change every cycle, so the loaded frame must be
    // SHADOWED at load time; comparing against the live inputs at step 5 compares
    // against a different frame, which is how the second version of this proof
    // failed.  `legal_l` shadows the range constraint with it.
    reg [1:0] sxp, szp, sxf, szf;
    reg       legal_l;

    always_ff @(posedge clk) begin
        step <= (step == 3'd5) ? 3'd5 : step + 3'd1;
        if (load) begin
            sxp <= xp_in; szp <= zp_in; sxf <= xf_in; szf <= zf_in;
            legal_l <= legal;
        end
    end

    // after reset, load, and exactly three applies, the frame is back
    always_comb
        if (legal_l && step == 3'd5)
            assert (xp == sxp && zp == szp && xf == sxf && zf == szf);
endmodule
