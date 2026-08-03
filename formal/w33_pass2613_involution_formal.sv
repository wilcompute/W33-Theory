// Pass 2613 -- prove A^2 = 9I + 6J in the netlist, and hence that the mixer is its
// own inverse on mean-zero signals.
//
// The parallel track states A^2 = 9I + 6J as an algebraic property of the
// SRG(36,15,6,6) adjacency and notes that on mean-zero signals Jx = 0, so R = A/3
// satisfies R^2 x = x -- the same interconnect encodes and decodes.  Their Yosys SAT
// check covers the mask identity; this asserts the SQUARE, which is the statement the
// encoder/decoder claim actually rests on.
//
// Written with generate + concurrent assertions rather than procedural loops: a
// module-scope or conditionally-assigned loop variable makes Yosys infer a latch
// inside always_comb, which it rejects before any solving happens.

`timescale 1ns/1ps
module w33_mixer_involution_formal #(parameter W = 4, parameter M = 12, parameter O = 20) (
    input wire signed [36*W-1:0] x_flat
);
    wire signed [36*M-1:0] y1;
    wire signed [36*O-1:0] y2;

    w33_mix_core #(.W(W), .OW(M)) a1 (.x_flat(x_flat), .y_flat(y1));   // x   -> A x
    w33_mix_core #(.W(M), .OW(O)) a2 (.x_flat(y1),     .y_flat(y2));   // A x -> A(A x)

    // sum of inputs, and a range guard so nothing is asserted about wrapped arithmetic
    wire signed [O-1:0] term  [0:36];
    wire                inrng [0:36];
    assign term[0]  = {O{1'b0}};
    assign inrng[0] = 1'b1;
    genvar t;
    generate
        for (t = 0; t < 36; t = t + 1) begin : sum
            assign term[t+1]  = term[t] + $signed(x_flat[t*W +: W]);
            assign inrng[t+1] = inrng[t]
                              && ($signed(x_flat[t*W +: W]) <=  3)
                              && ($signed(x_flat[t*W +: W]) >= -3);
        end
    endgenerate
    wire signed [O-1:0] xsum  = term[36];
    wire                small = inrng[36];

    genvar k;
    generate
        for (k = 0; k < 36; k = k + 1) begin : chk
            // A^2 = 9I + 6J, entrywise
            always_comb if (small)
                assert ($signed(y2[k*O +: O]) ==
                        9 * $signed(x_flat[k*W +: W]) + 6 * xsum);
            // the consequence: on MEAN-ZERO input A^2 x = 9x, so A/3 is an
            // involution and one interconnect both encodes and decodes
            always_comb if (small && xsum == 0)
                assert ($signed(y2[k*O +: O]) == 9 * $signed(x_flat[k*W +: W]));
        end
    endgenerate
endmodule
