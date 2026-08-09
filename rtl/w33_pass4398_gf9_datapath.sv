// Pass 4398 -- the GF(9) width penalty, measured in cells.
//
// Pass 4389 measured that the Hermitian quadrangle H(3,9) protects its two registers at
// different rates (3.2258% vs 2.7027%), where the symplectic W(3,3) forces them equal.
// Pass 4390 showed the group theory does not obstruct a machine there: four unitary
// transvections generate PSU(4,3).
//
// Neither pass counted anything. The blueprint's four-machine table (103/132/206/240
// cells) was synthesised over GF(3), and a GF(9) datapath is wider. This file is the
// arithmetic core of each, side by side, so yosys can say how much wider.
//
// The comparison being tested, stated before the run so it can fail:
//     if the GF(9) core costs more than ~1.19x the GF(3) core, the asymmetric protection
//     gain (a factor of 1.194 between the two miss rates) is bought at a loss.
//
// Encoding. GF(3) element: 2 bits, values 0,1,2 (3 is illegal and never produced).
// GF(9) = GF(3)[i]/(i^2+1) element: 4 bits, {b,a} for a + b*i, each half a GF(3) element.
// Conjugation is a + b*i -> a - b*i, the Frobenius x -> x^3, which is why the Hermitian
// form costs a negation the symplectic one does not.

`default_nettype none

// ---------------------------------------------------------------------------
// GF(3) primitives -- the baseline the blueprint machines are built from.
// ---------------------------------------------------------------------------
module gf3_add (input wire [1:0] a, input wire [1:0] b, output wire [1:0] y);
  wire [2:0] s = a + b;
  assign y = (s >= 3) ? s - 3 : s[1:0];
endmodule

module gf3_neg (input wire [1:0] a, output wire [1:0] y);
  assign y = (a == 2'd0) ? 2'd0 : (a == 2'd1 ? 2'd2 : 2'd1);
endmodule

module gf3_mul (input wire [1:0] a, input wire [1:0] b, output wire [1:0] y);
  // 3x3 table; both operands are known 0..2
  assign y = (a == 2'd0 || b == 2'd0) ? 2'd0
           : (a == 2'd1) ? b
           : (b == 2'd1) ? a
           : 2'd1;                       // 2*2 = 4 = 1 mod 3
endmodule

// ---------------------------------------------------------------------------
// GF(9) primitives.
// ---------------------------------------------------------------------------
module gf9_add (input wire [3:0] a, input wire [3:0] b, output wire [3:0] y);
  gf3_add lo (.a(a[1:0]), .b(b[1:0]), .y(y[1:0]));
  gf3_add hi (.a(a[3:2]), .b(b[3:2]), .y(y[3:2]));
endmodule

// x -> x^3, the involutory automorphism of GF(9) over GF(3): a + b*i -> a - b*i.
module gf9_conj (input wire [3:0] a, output wire [3:0] y);
  assign y[1:0] = a[1:0];
  gf3_neg n (.a(a[3:2]), .y(y[3:2]));
endmodule

// (a + b i)(c + d i) = (ac - bd) + (ad + bc) i
module gf9_mul (input wire [3:0] x, input wire [3:0] z, output wire [3:0] y);
  wire [1:0] a = x[1:0], b = x[3:2], c = z[1:0], d = z[3:2];
  wire [1:0] ac, bd, ad, bc, nbd;
  gf3_mul m0 (.a(a), .b(c), .y(ac));
  gf3_mul m1 (.a(b), .b(d), .y(bd));
  gf3_mul m2 (.a(a), .b(d), .y(ad));
  gf3_mul m3 (.a(b), .b(c), .y(bc));
  gf3_neg g0 (.a(bd), .y(nbd));
  gf3_add s0 (.a(ac),  .b(nbd), .y(y[1:0]));
  gf3_add s1 (.a(ad),  .b(bc),  .y(y[3:2]));
endmodule

// ---------------------------------------------------------------------------
// The two forms, each as one combinational block on a 4-component vector.
// ---------------------------------------------------------------------------

// Symplectic form over GF(3): B(x,y) = x0*y1 - x1*y0 + x2*y3 - x3*y2.
module symplectic_form_gf3 (input wire [7:0] x, input wire [7:0] y,
                            output wire [1:0] f);
  wire [1:0] t0, t1, t2, t3, n1, n3, s0, s1;
  gf3_mul p0 (.a(x[1:0]), .b(y[3:2]), .y(t0));
  gf3_mul p1 (.a(x[3:2]), .b(y[1:0]), .y(t1));
  gf3_mul p2 (.a(x[5:4]), .b(y[7:6]), .y(t2));
  gf3_mul p3 (.a(x[7:6]), .b(y[5:4]), .y(t3));
  gf3_neg g1 (.a(t1), .y(n1));
  gf3_neg g3 (.a(t3), .y(n3));
  gf3_add a0 (.a(t0), .b(n1), .y(s0));
  gf3_add a1 (.a(t2), .b(n3), .y(s1));
  gf3_add a2 (.a(s0), .b(s1), .y(f));
endmodule

// Hermitian form over GF(9): B(x,y) = sum_i x_i * conj(y_i).
module hermitian_form_gf9 (input wire [15:0] x, input wire [15:0] y,
                           output wire [3:0] f);
  wire [3:0] c0, c1, c2, c3, p0, p1, p2, p3, s0, s1;
  gf9_conj k0 (.a(y[3:0]),   .y(c0));
  gf9_conj k1 (.a(y[7:4]),   .y(c1));
  gf9_conj k2 (.a(y[11:8]),  .y(c2));
  gf9_conj k3 (.a(y[15:12]), .y(c3));
  gf9_mul  m0 (.x(x[3:0]),   .z(c0), .y(p0));
  gf9_mul  m1 (.x(x[7:4]),   .z(c1), .y(p1));
  gf9_mul  m2 (.x(x[11:8]),  .z(c2), .y(p2));
  gf9_mul  m3 (.x(x[15:12]), .z(c3), .y(p3));
  gf9_add  a0 (.a(p0), .b(p1), .y(s0));
  gf9_add  a1 (.a(p2), .b(p3), .y(s1));
  gf9_add  a2 (.a(s0), .b(s1), .y(f));
endmodule

// ---------------------------------------------------------------------------
// One transvection step in each geometry -- the actual opcode datapath.
//   symplectic:  x -> x + a * B(x,v) * v      (a in GF(3))
//   unitary:     x -> x + a * B(x,v) * v      (a trace-zero in GF(9), B Hermitian)
// The shape is identical; only the field and the form differ, which is exactly the
// comparison this file exists to price.
// ---------------------------------------------------------------------------
module transvection_gf3 (input wire [7:0] x, input wire [7:0] v, input wire [1:0] a,
                         output wire [7:0] y);
  wire [1:0] f, c;
  symplectic_form_gf3 form (.x(x), .y(v), .f(f));
  gf3_mul scale (.a(a), .b(f), .y(c));
  genvar i;
  generate for (i = 0; i < 4; i = i + 1) begin : lanes
    wire [1:0] cv;
    gf3_mul mv (.a(c), .b(v[2*i+1:2*i]), .y(cv));
    gf3_add av (.a(x[2*i+1:2*i]), .b(cv), .y(y[2*i+1:2*i]));
  end endgenerate
endmodule

module transvection_gf9 (input wire [15:0] x, input wire [15:0] v, input wire [3:0] a,
                         output wire [15:0] y);
  wire [3:0] f, c;
  hermitian_form_gf9 form (.x(x), .y(v), .f(f));
  gf9_mul scale (.x(a), .z(f), .y(c));
  genvar i;
  generate for (i = 0; i < 4; i = i + 1) begin : lanes
    wire [3:0] cv;
    gf9_mul mv (.x(c), .z(v[4*i+3:4*i]), .y(cv));
    gf9_add av (.a(x[4*i+3:4*i]), .b(cv), .y(y[4*i+3:4*i]));
  end endgenerate
endmodule

`default_nettype wire
