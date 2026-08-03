// Pass 2632 -- the degree-3 gate the universality scaffold is missing.
//
// The corpus records the logical gate set as "degree-2 symplectic + degree-3 E6 cubic
// = Lloyd-Braunstein universal", with Clifford alone in P and Clifford + cubic in BQP.
// Passes 2438-2612 built the degree-2 half (mixer, phase controller, fibre controllers)
// and place-and-routed all of it.  Nothing in this project has ever built the cubic.
//
// Why it cannot be a single-qutrit gate: over F_3, x^3 = x for every x (Fermat), so a
// cubic map on one trit is the IDENTITY.  A nontrivial cubic needs the 27, and
// 27 = 3^3 = the 3x3 matrices over F_3, on which the E6 cubic invariant restricts to the
// DETERMINANT.  That is the object built here.
//
// Encoding: 9 trits, 2 bits each, row-major.  Value 3 is illegal input.
// Output: det(X) mod 3, usable directly as a phase increment on the mu_3 clock.

`timescale 1ns/1ps

// mod-3 helpers.  Inputs are always < 3 by construction of the callers.
module w33_f3_add (input wire [1:0] a, input wire [1:0] b, output wire [1:0] y);
    wire [2:0] s = a + b;
    assign y = (s >= 3) ? s - 3 : s[1:0];
endmodule

module w33_f3_mul (input wire [1:0] a, input wire [1:0] b, output wire [1:0] y);
    // 3x3 table; only a,b in {0,1,2} occur
    assign y = (a == 2'd0 || b == 2'd0) ? 2'd0
             : (a == 2'd1) ? b
             : (b == 2'd1) ? a
             :               2'd1;          // 2*2 = 4 = 1 mod 3
endmodule

// det of a 3x3 matrix over F_3 -- the E6 cubic invariant restricted to the 27.
module w33_e6_cubic (
    input  wire [17:0] x_flat,      // 9 trits, row-major: x[r][c] = x_flat[(3r+c)*2 +: 2]
    output wire [1:0]  det
);
    wire [1:0] m [0:8];
    genvar g;
    generate
        for (g = 0; g < 9; g = g + 1) begin : unpack
            assign m[g] = x_flat[g*2 +: 2];
        end
    endgenerate

    // the six signed products of a 3x3 determinant
    wire [1:0] p0a, p0, p1a, p1, p2a, p2, n0a, n0, n1a, n1, n2a, n2;
    w33_f3_mul u0a (.a(m[0]), .b(m[4]), .y(p0a));  w33_f3_mul u0 (.a(p0a), .b(m[8]), .y(p0));
    w33_f3_mul u1a (.a(m[1]), .b(m[5]), .y(p1a));  w33_f3_mul u1 (.a(p1a), .b(m[6]), .y(p1));
    w33_f3_mul u2a (.a(m[2]), .b(m[3]), .y(p2a));  w33_f3_mul u2 (.a(p2a), .b(m[7]), .y(p2));
    w33_f3_mul v0a (.a(m[2]), .b(m[4]), .y(n0a));  w33_f3_mul v0 (.a(n0a), .b(m[6]), .y(n0));
    w33_f3_mul v1a (.a(m[0]), .b(m[5]), .y(n1a));  w33_f3_mul v1 (.a(n1a), .b(m[7]), .y(n1));
    w33_f3_mul v2a (.a(m[1]), .b(m[3]), .y(n2a));  w33_f3_mul v2 (.a(n2a), .b(m[8]), .y(n2));

    // negation in F_3 is x -> (3 - x) mod 3
    function [1:0] neg3(input [1:0] v); neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1; endfunction

    wire [1:0] s1, s2, s3, s4, s5;
    w33_f3_add a1 (.a(p0),        .b(p1),        .y(s1));
    w33_f3_add a2 (.a(s1),        .b(p2),        .y(s2));
    w33_f3_add a3 (.a(s2),        .b(neg3(n0)),  .y(s3));
    w33_f3_add a4 (.a(s3),        .b(neg3(n1)),  .y(s4));
    w33_f3_add a5 (.a(s4),        .b(neg3(n2)),  .y(s5));
    assign det = s5;
endmodule

// The gate: the cubic drives a mu_3 phase accumulator.  Composing this with the
// degree-2 symplectic interconnect is the Lloyd-Braunstein pair.
module w33_cubic_phase_gate (
    input  wire        clk,
    input  wire        rst,
    input  wire        en,
    input  wire [17:0] x_flat,
    output reg  [1:0]  phase          // accumulated mod 3
);
    wire [1:0] d;
    w33_e6_cubic core (.x_flat(x_flat), .det(d));
    wire [1:0] nxt;
    w33_f3_add acc (.a(phase), .b(d), .y(nxt));
    always_ff @(posedge clk)
        if (rst) phase <= 2'd0;
        else if (en) phase <= nxt;
endmodule
