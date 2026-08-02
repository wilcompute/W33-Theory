// Pass 2438 formal -- prove the chirality bifurcation over ALL inputs with SAT,
// rather than inferring it from a constant-folding artefact.
//
// Two assertions, both exhaustive over the 6 fibre elements:
//   1. the C6 antipode NEVER moves the orientation register   (chirality survives)
//   2. the S3 reflection moves it for every p != 0            (chirality destroyed)
`timescale 1ns/1ps
module w33_chirality_formal (
    input wire [1:0] p_in,
    input wire       s_in
);
    wire [1:0] c6p, s3p;
    wire       c6s, s3s;

    w33_c6_fibre u_c6 (.p_in(p_in), .s_in(s_in), .pow(3'd3),
                       .p_out(c6p), .s_out(c6s));
    w33_s3_fibre u_s3 (.p_in(p_in), .s_in(s_in), .a(2'd0), .b(1'b1),
                       .p_out(s3p), .s_out(s3s));

    // p_in ranges over the three antipodal-pair indices only
    always_comb begin
        if (p_in < 2'd3) begin
            // 1. the point-side antipode preserves the orientation register
            assert (c6p == p_in);
            // and it is a genuine involution on the sign
            assert (c6s == ~s_in);

            // 2. the line-side reflection reverses it away from the fixed point
            assert (s3p == ((2'd3 - p_in) % 2'd3));
            if (p_in != 2'd0) assert (s3p != p_in);
            assert (s3s == ~s_in);
        end
    end
endmodule
