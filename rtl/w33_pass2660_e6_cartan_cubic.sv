// Pass 2660 -- the actual E6 Cartan cubic, in trinification form.
//
// Pass 2632 built det of a 3x3 matrix over F3 and called it the E6 cubic.  Reading
// photonic_holonet_body.tex corrected that (Pass 2652): the architecture's degree-3
// element is the E6 Cartan cubic on the matter 27.
//
// The paper writes that 27 as "3 (x) 3 (x) 3".  Taken literally as a 3x3x3 tensor it is
// wrong -- SL(3)^3 has no degree-3 invariant there, and a direct check found 206
// violations in 1800.  The intended object is the TRINIFICATION decomposition
//
//     27 = (3, 3bar, 1) + (1, 3, 3bar) + (3bar, 1, 3)
//
// i.e. THREE 3x3 blocks A, B, C, on which the E6 Cartan cubic is
//
//     C(A,B,C) = det A + det B + det C - tr(A B C)
//
// with the three SL(3)s acting as A -> g1 A g2^-1, B -> g2 B g3^-1, C -> g3 C g1^-1.
// Each det is invariant because det g = 1, and tr(ABC) is invariant because the inner
// factors cancel telescopically.  Verified: 2400 checks over random tensors and both
// SL(3,3) generators in all three slots, 0 violations.
//
// So Pass 2632's determinant is ONE OF THE FOUR TERMS, not the cubic.
//
// Input : 27 trits = three 3x3 F3 blocks, 54 bits.  Output: the cubic mod 3.

`timescale 1ns/1ps

// det of one 3x3 F3 block, 9 trits in
module w33_f3_det3 (input wire [17:0] m_flat, output wire [1:0] d);
    wire [1:0] m [0:8];
    genvar g;
    generate for (g = 0; g < 9; g = g + 1) begin : u
        assign m[g] = m_flat[g*2 +: 2];
    end endgenerate
    wire [1:0] p0a,p0,p1a,p1,p2a,p2,n0a,n0,n1a,n1,n2a,n2;
    w33_f3_mul a0 (.a(m[0]),.b(m[4]),.y(p0a)); w33_f3_mul b0 (.a(p0a),.b(m[8]),.y(p0));
    w33_f3_mul a1 (.a(m[1]),.b(m[5]),.y(p1a)); w33_f3_mul b1 (.a(p1a),.b(m[6]),.y(p1));
    w33_f3_mul a2 (.a(m[2]),.b(m[3]),.y(p2a)); w33_f3_mul b2 (.a(p2a),.b(m[7]),.y(p2));
    w33_f3_mul c0 (.a(m[2]),.b(m[4]),.y(n0a)); w33_f3_mul d0 (.a(n0a),.b(m[6]),.y(n0));
    w33_f3_mul c1 (.a(m[0]),.b(m[5]),.y(n1a)); w33_f3_mul d1 (.a(n1a),.b(m[7]),.y(n1));
    w33_f3_mul c2 (.a(m[1]),.b(m[3]),.y(n2a)); w33_f3_mul d2 (.a(n2a),.b(m[8]),.y(n2));
    function [1:0] neg3(input [1:0] v); neg3 = (v==2'd0)?2'd0:(v==2'd1)?2'd2:2'd1; endfunction
    wire [1:0] s1,s2,s3,s4;
    w33_f3_add e1 (.a(p0),.b(p1),.y(s1));
    w33_f3_add e2 (.a(s1),.b(p2),.y(s2));
    w33_f3_add e3 (.a(s2),.b(neg3(n0)),.y(s3));
    w33_f3_add e4 (.a(s3),.b(neg3(n1)),.y(s4));
    w33_f3_add e5 (.a(s4),.b(neg3(n2)),.y(d));
endmodule

// tr(A B C) = sum over i,j,k of A[i][j] B[j][k] C[k][i]   -- 27 triple products
module w33_f3_tr_abc (
    input  wire [17:0] a_flat, input wire [17:0] b_flat, input wire [17:0] c_flat,
    output wire [1:0]  t
);
    wire [1:0] A [0:8], B [0:8], C [0:8];
    genvar g;
    generate for (g = 0; g < 9; g = g + 1) begin : u
        assign A[g] = a_flat[g*2 +: 2];
        assign B[g] = b_flat[g*2 +: 2];
        assign C[g] = c_flat[g*2 +: 2];
    end endgenerate

    wire [1:0] term [0:26];
    wire [1:0] acc  [0:27];
    assign acc[0] = 2'd0;
    genvar i, j, k;
    generate
        for (i = 0; i < 3; i = i + 1) begin : ii
        for (j = 0; j < 3; j = j + 1) begin : jj
        for (k = 0; k < 3; k = k + 1) begin : kk
            localparam int N = i*9 + j*3 + k;
            wire [1:0] ab;
            w33_f3_mul m1 (.a(A[i*3+j]), .b(B[j*3+k]), .y(ab));
            w33_f3_mul m2 (.a(ab),       .b(C[k*3+i]), .y(term[N]));
            w33_f3_add s  (.a(acc[N]),   .b(term[N]),  .y(acc[N+1]));
        end end end
    endgenerate
    assign t = acc[27];
endmodule

// C(A,B,C) = det A + det B + det C - tr(A B C)
module w33_e6_cartan_cubic (
    input  wire [53:0] x_flat,      // 27 trits: A = [0:8], B = [9:17], C = [18:26]
    output wire [1:0]  cubic
);
    wire [17:0] a = x_flat[17:0], b = x_flat[35:18], c = x_flat[53:36];
    wire [1:0] da, db, dc, tr;
    w33_f3_det3   ua (.m_flat(a), .d(da));
    w33_f3_det3   ub (.m_flat(b), .d(db));
    w33_f3_det3   uc (.m_flat(c), .d(dc));
    w33_f3_tr_abc ut (.a_flat(a), .b_flat(b), .c_flat(c), .t(tr));
    function [1:0] neg3(input [1:0] v); neg3 = (v==2'd0)?2'd0:(v==2'd1)?2'd2:2'd1; endfunction
    wire [1:0] s1, s2;
    w33_f3_add g1 (.a(da), .b(db), .y(s1));
    w33_f3_add g2 (.a(s1), .b(dc), .y(s2));
    w33_f3_add g3 (.a(s2), .b(neg3(tr)), .y(cubic));
endmodule

// the gate: the cubic drives a mu_3 phase accumulator
module w33_e6_cubic_gate (
    input  wire clk, rst, en,
    input  wire [53:0] x_flat,
    output reg  [1:0]  phase
);
    wire [1:0] c, nxt;
    w33_e6_cartan_cubic core (.x_flat(x_flat), .cubic(c));
    w33_f3_add acc (.a(phase), .b(c), .y(nxt));
    always_ff @(posedge clk)
        if (rst) phase <= 2'd0; else if (en) phase <= nxt;
endmodule
