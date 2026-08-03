// Pass 2773 -- the spread mixer, in a form a toolchain will actually accept.
//
// `rtl/w33_spread_mixer36.sv` (Pass 2206, added 2026-08-02) is headed "synthesizable
// reference datapaths for the exact W(3,3) spread mixer".  It is accepted by NEITHER
// toolchain in this repo:
//
//     yosys    rtl/w33_spread_mixer36.sv:7:  syntax error, unexpected '['
//                                            (unpacked array PORTS: `x [0:35]`)
//     iverilog rtl/w33_spread_mixer36.sv:10: sorry: unpacked array parameters are
//                                            not supported yet   (the MASK table)
//
// Two different frontends, two different unsupported constructs, one file that has
// therefore never been simulated or synthesized since it was committed.  Found by
// `scripts/check_rtl_folds.py` on its first repo-wide sweep, which is the same sweep
// that found the Pass 2753 frame-tracker fold -- both defects are invisible to review
// and to simulation, and visible immediately to a frontend.
//
// The arithmetic below is unchanged: y[i] = sum over j with MASK[i][j] of
// sign-extended x[j].  Only the two rejected constructs are replaced --
//
//     unpacked ports      ->  one packed bus, sliced
//     unpacked localparam ->  one packed 1296-bit constant, indexed i*36 + j
//
// -- so this is a port of the reference, not a new datapath.  Its purpose is to put a
// real number where "synthesizable" was asserted.

`timescale 1ns/1ps

// The datapath and its proof must read the SAME mask constant, and the three obvious
// ways to share it are each rejected by one of the two frontends in this repo:
//
//     `dut.MASK_FLAT`                iverilog: hierarchical reference is not a constant
//                                    yosys:    parameter does not evaluate to a constant
//     `package` + ANSI import        yosys:    syntax error, unexpected TOK_IMPORT
//     `package` + body import        yosys:    syntax error, unexpected TOK_IMPORT
//
// A text macro is the one mechanism both accept, because it is expanded before either
// frontend sees it.  Not elegant; portable, which matters more here.
`define W33_SPREAD36_MASK {                                          \
        36'h615d23330, 36'ha16ac54a8, 36'hc1361e858, 36'h0e6ac2b50,  \
        36'h165d24cc8, 36'h1a36197a0, 36'h1c01ff038, 36'he001f8fc0,  \
        36'h007ff8007, 36'hd8b986184, 36'h74d24b0c1, 36'hace435142,  \
        36'hd8c66061c, 36'hac9b08a2a, 36'h74ac90c31, 36'h8bc4aa8a1,  \
        36'h53c354922, 36'h53a8a924a, 36'h8b9951451, 36'h2792ac514,  \
        36'h27a55228c, 36'h6a5093c0e, 36'hb2610da15, 36'hc63066623,  \
        36'h390786643, 36'h4d0a35a85, 36'h950c4bd06, 36'h9550902f6,  \
        36'h4d610856d, 36'h39306099b, 36'hc6078119b, 36'hb20a3216d,  \
        36'h6a0c4c0f6, 36'h00c81e79b, 36'h0094c5b6d, 36'h00a323cf6   \
    }

module w33_spread_mixer36_synth #(
    parameter int W  = 16,
    parameter int OW = W + 4
) (
    input  wire [36*W  - 1:0] x_flat,     // 36 signed W-bit lanes, lane j at [j*W +: W]
    output reg  [36*OW - 1:0] y_flat      // 36 signed OW-bit lanes
);
    // The 36 x 36 incidence mask, one 36-bit row per output lane, packed row-major.
    // Row i occupies MASK_FLAT[i*36 +: 36]; bit j of that row is MASK_FLAT[i*36 + j].
    // Rows are listed low-index-first, so the concatenation is written in reverse.
    localparam logic [36*36-1:0] MASK_FLAT = `W33_SPREAD36_MASK;

    integer i, j;
    reg signed [OW-1:0] acc;
    reg signed [W-1:0]  lane;

    always_comb begin
        y_flat = '0;
        for (i = 0; i < 36; i = i + 1) begin
            acc = '0;
            for (j = 0; j < 36; j = j + 1) begin
                lane = x_flat[j*W +: W];
                // Explicit sign extension.  A ternary with one unsigned operand is
                // unsigned throughout in Verilog -- the trap that corrupted 91% of the
                // signed lane checks earlier in this track.  Written as an if, with the
                // extension spelled out, there is nothing for the rule to apply to.
                if (MASK_FLAT[i*36 + j])
                    acc = acc + {{(OW-W){lane[W-1]}}, lane};
            end
            y_flat[i*OW +: OW] = acc;
        end
    end
endmodule

// Equivalence to the reference arithmetic, checked exhaustively on the one input class
// that separates a correct signed mixer from the unsigned trap: single-lane impulses at
// the most negative value.  If sign extension is dropped anywhere, y is wrong here and
// nowhere else on small inputs -- which is why a two-column simulation with non-negative
// columns passed the broken version earlier in this track.
module w33_spread_mixer36_formal #(
    parameter int W  = 8,
    parameter int OW = W + 4
) (
    input wire [5:0] lane_sel                   // which lane carries the impulse
);
    reg  [36*W-1:0] x_flat;
    wire [36*OW-1:0] y_flat;

    w33_spread_mixer36_synth #(.W(W), .OW(OW)) dut (.x_flat(x_flat), .y_flat(y_flat));

    localparam logic [36*36-1:0] M = `W33_SPREAD36_MASK;

    // The impulse.  Written with a loop that assigns on EVERY path -- guarding the
    // assignment with `if (lane_sel < 36)` and looping only inside the guard makes the
    // loop variable unassigned on the else path, and yosys infers a latch on it.
    integer k;
    always_comb begin
        x_flat = '0;
        for (k = 0; k < 36; k = k + 1)
            if (k == lane_sel)
                x_flat[k*W +: W] = {1'b1, {(W-1){1'b0}}};       // most negative value
    end

    // Row k picks up the impulse exactly when the mask bit is set.  When lane_sel >= 36
    // there is no impulse and every row must read zero, which the same expression gives
    // because M[k*36 + lane_sel] is then out of the row and reads 0.
    integer r;
    always_comb
        for (r = 0; r < 36; r = r + 1)
            assert (y_flat[r*OW +: OW] ==
                    ((lane_sel < 36 && M[r*36 + lane_sel])
                     ? {{(OW-W){1'b1}}, 1'b1, {(W-1){1'b0}}}
                     : {OW{1'b0}}));
endmodule
