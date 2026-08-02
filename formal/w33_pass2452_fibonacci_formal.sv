// Pass 2452 formal -- SAT-prove the two halves of the R4^2 U6 splitting.
//
//   1. the A-sector has period exactly 2 under M   (eigenvalue -1)
//   2. the BC-pair obeys the FIBONACCI recursion: writing (b,c) -> (b',c'),
//      the c-component satisfies c'' = c' + c, i.e. a(n) = a(n-1) + a(n-2)
//
// (2) is the real content: it is the char poly t^2 - t - 1 read off the datapath.
`timescale 1ns/1ps
module w33_fibonacci_formal #(parameter W = 8) (
    input wire signed [W-1:0] a0,
    input wire signed [W-1:0] b0,
    input wire signed [W-1:0] c0
);
    wire signed [W-1:0] a1, b1, c1, a2, b2, c2, a3, b3, c3;
    w33_m_step #(.W(W)) s1 (.a_in(a0), .b_in(b0), .c_in(c0),
                            .a_out(a1), .b_out(b1), .c_out(c1));
    w33_m_step #(.W(W)) s2 (.a_in(a1), .b_in(b1), .c_in(c1),
                            .a_out(a2), .b_out(b2), .c_out(c2));
    w33_m_step #(.W(W)) s3 (.a_in(a2), .b_in(b2), .c_in(c2),
                            .a_out(a3), .b_out(b3), .c_out(c3));

    // keep every intermediate inside the word so no assertion is about wrapped
    // arithmetic; the range is generous enough to leave the claims non-vacuous
    wire small =
        (a0 > -8 && a0 < 8) && (b0 > -8 && b0 < 8) && (c0 > -8 && c0 < 8);

    always_comb begin
        if (small) begin
            // 1. the A-sector: eigenvalue -1, period exactly 2
            assert (a1 == -a0);
            assert (a2 ==  a0);

            // 2. the BC-pair: b is a delayed, negated c
            assert (b1 == -c0);
            // and the c-component satisfies the FIBONACCI recursion c3 = c2 + c1
            assert (c3 == c2 + c1);

            // the same recursion one step earlier, so it is not an artefact of the end
            assert (c2 == c1 + c0);
        end
    end
endmodule
