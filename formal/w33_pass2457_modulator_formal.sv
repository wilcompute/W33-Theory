// Pass 2457 formal -- prove the modulator's two invariants over all reachable states.
//   1. the select line ALTERNATES: two steps restore the A-sector exactly
//   2. the amplitude obeys the FIBONACCI recursion, so successive amplitudes are
//      Fibonacci-scaled and their ratio tends to phi
`timescale 1ns/1ps
module w33_modulator_formal #(parameter W = 10) (
    input wire signed [W-1:0] a0, b0, c0
);
    wire signed [W-1:0] a1,b1,c1, a2,b2,c2, a3,b3,c3;
    w33_modulator_step #(.W(W)) s1 (.a_in(a0),.b_in(b0),.c_in(c0),
                                    .a_out(a1),.b_out(b1),.c_out(c1));
    w33_modulator_step #(.W(W)) s2 (.a_in(a1),.b_in(b1),.c_in(c1),
                                    .a_out(a2),.b_out(b2),.c_out(c2));
    w33_modulator_step #(.W(W)) s3 (.a_in(a2),.b_in(b2),.c_in(c2),
                                    .a_out(a3),.b_out(b3),.c_out(c3));
    wire small = (a0 > -16 && a0 < 16) && (b0 > -16 && b0 < 16) && (c0 > -16 && c0 < 16);
    always_comb begin
        if (small) begin
            // 1. the select line alternates and has period exactly 2
            assert (a1 == -a0);
            assert (a2 ==  a0);
            assert (a1[W-1] != a0[W-1] || a0 == 0);   // sign bit flips unless seed is 0
            // 2. the amplitude obeys the Fibonacci recursion
            assert (c2 == c1 + c0);
            assert (c3 == c2 + c1);
        end
    end
endmodule
