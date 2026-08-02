// Pass 2452 -- the R4^2 U6 word as a datapath.
//
// Pass 2439 proved: M = R4^2 U6 has char poly (t+1)(t^2 - t - 1).  It negates the
// A-sector -- the rational line (1,0,0), the V9 inside the 24 -- and induces
// [[0,-1],[-1,1]] on the quotient Z^3/<(1,0,0)>, which has det -1 and trace 1, the
// same as the Fibonacci matrix [[1,1],[1,0]].
//
// So the whole word is a two-register machine:
//     A-register  : one signed value, NEGATED every step        (the 24-sector)
//     BC-register : a pair, advanced by the Fibonacci recursion  (the 90-sector)
//
// This module applies M literally, as integer arithmetic on the 3-vector, and exposes
// the two registers separately so the split is visible in the netlist.

`timescale 1ns/1ps

// One application of M = R4^2 U6 = [[-1,0,0],[0,0,-1],[0,-1,1]].
module w33_m_step #(parameter W = 16) (
    input  wire signed [W-1:0] a_in,   // A-sector   (the invariant rational line)
    input  wire signed [W-1:0] b_in,   // B          } the quotient Z^2, on which M
    input  wire signed [W-1:0] c_in,   // C          } acts by the Fibonacci matrix
    output wire signed [W-1:0] a_out,
    output wire signed [W-1:0] b_out,
    output wire signed [W-1:0] c_out
);
    assign a_out = -a_in;              // eigenvalue -1: the A-sector merely flips sign
    assign b_out = -c_in;              // [[0,-1],
    assign c_out = c_in - b_in;        //  [-1,1]]  acting on (b,c)
endmodule

// n applications, unrolled, so the growth is visible.
module w33_fibonacci_datapath #(parameter W = 16, parameter N = 8) (
    input  wire signed [W-1:0] a0,
    input  wire signed [W-1:0] b0,
    input  wire signed [W-1:0] c0,
    output wire signed [W-1:0] a_n,
    output wire signed [W-1:0] b_n,
    output wire signed [W-1:0] c_n
);
    wire signed [W-1:0] a [0:N];
    wire signed [W-1:0] b [0:N];
    wire signed [W-1:0] c [0:N];
    assign a[0] = a0;
    assign b[0] = b0;
    assign c[0] = c0;
    genvar i;
    generate
        for (i = 0; i < N; i = i + 1) begin : stage
            w33_m_step #(.W(W)) u (
                .a_in(a[i]), .b_in(b[i]), .c_in(c[i]),
                .a_out(a[i+1]), .b_out(b[i+1]), .c_out(c[i+1]));
        end
    endgenerate
    assign a_n = a[N];
    assign b_n = b[N];
    assign c_n = c[N];
endmodule

// The claim, isolated: after two steps the A-sector is restored exactly (since
// (-1)^2 = 1) while the BC-pair has advanced by the SQUARE of the Fibonacci matrix.
// So the A-sector has period 2 and the BC-pair grows without bound: the datapath
// separates a periodic register from a phi-growing one.
module w33_fibonacci_probe #(parameter W = 16) (
    input  wire signed [W-1:0] a0,
    input  wire signed [W-1:0] b0,
    input  wire signed [W-1:0] c0,
    output wire                a_is_periodic_2,
    output wire signed [W-1:0] b2,
    output wire signed [W-1:0] c2
);
    wire signed [W-1:0] a1, b1, c1, a2;
    w33_m_step #(.W(W)) s1 (.a_in(a0), .b_in(b0), .c_in(c0),
                            .a_out(a1), .b_out(b1), .c_out(c1));
    w33_m_step #(.W(W)) s2 (.a_in(a1), .b_in(b1), .c_in(c1),
                            .a_out(a2), .b_out(b2), .c_out(c2));
    assign a_is_periodic_2 = (a2 == a0);
endmodule
