// Pass 2438 -- the chirality bifurcation of Pass 2437, as hardware.
//
// Pass 2437 measured two 6:1 fibrations of the substrate over 40 objects:
//
//   POINT side (240 E8 roots  -> 40 W(3,3) points) : fibre group C6, antipode INSIDE it,
//                                                    quotient action on 3 pairs = C3
//   LINE  side (240 dual cws  -> 40 Q(4,3) points) : fibre group S3, antipode OUTSIDE it,
//                                                    quotient action on 3 pairs = S3
//
// Encode a fibre element as (p, s):  p in {0,1,2} the antipodal-pair index (the
// ORIENTATION register), s in {0,1} the sign.  Then the whole bifurcation is one
// question about the involution:
//
//   C6 involution (the antipode -1) :  (p,s) -> (p,     s^1)   -- p UNTOUCHED
//   S3 involution (a reflection t)  :  (p,s) -> (-p,    s^1)   -- p NEGATED mod 3
//
// The orientation survives on the point side exactly because C6 spends its involution
// on the antipode; on the line side the involution is still free and reverses p.
//
// Both modules are one-hot-free, 3-bit, and combinational, so the synthesised cell
// counts are a fair measure of the difference.

`timescale 1ns/1ps

// ---------------------------------------------------------------------------
// POINT side.  Generator of C6 = (rotate orientation, flip sign).
//   g   : (p,s) -> (p+1 mod 3, s^1)      order 6
//   g^3 : (p,s) -> (p,         s^1)      the antipode -- ORIENTATION PRESERVED
// ---------------------------------------------------------------------------
module w33_c6_fibre (
    input  wire [1:0] p_in,      // orientation register, 0..2
    input  wire       s_in,      // sign
    input  wire [2:0] pow,       // apply g^pow, 0..5
    output wire [1:0] p_out,
    output wire       s_out
);
    // p advances by pow mod 3; s flips with the parity of pow.
    wire [3:0] sum = {2'b0, p_in} + {1'b0, pow};
    wire [3:0] m3  = (sum >= 4'd9) ? (sum - 4'd9)
                   : (sum >= 4'd6) ? (sum - 4'd6)
                   : (sum >= 4'd3) ? (sum - 4'd3)
                   :                  sum;
    assign p_out = m3[1:0];
    assign s_out = s_in ^ pow[0];
endmodule

// ---------------------------------------------------------------------------
// LINE side.  S3 by left multiplication on itself, elements r^p t^s.
//   r : (p,s) -> (p+1 mod 3, s)          rotation, orientation preserved
//   t : (p,s) -> (-p   mod 3, s^1)       reflection, ORIENTATION REVERSED
// Apply r^a then t^b.
// ---------------------------------------------------------------------------
module w33_s3_fibre (
    input  wire [1:0] p_in,
    input  wire       s_in,
    input  wire [1:0] a,         // rotation amount 0..2
    input  wire       b,         // apply a reflection
    output wire [1:0] p_out,
    output wire       s_out
);
    wire [2:0] sum = {1'b0, p_in} + {1'b0, a};
    wire [1:0] rot = (sum >= 3'd3) ? sum[1:0] - 2'd3 : sum[1:0];
    // the reflection: negate the orientation register mod 3 (0->0, 1->2, 2->1)
    wire [1:0] neg = (rot == 2'd0) ? 2'd0 : (rot == 2'd1) ? 2'd2 : 2'd1;
    assign p_out = b ? neg : rot;
    assign s_out = s_in ^ b;
endmodule

// ---------------------------------------------------------------------------
// The control question, isolated: given a fibre element and one involution,
// does the orientation register change?  This is the whole bifurcation.
// ---------------------------------------------------------------------------
module w33_orientation_probe (
    input  wire [1:0] p_in,
    input  wire       s_in,
    output wire       c6_orientation_changed,
    output wire       s3_orientation_changed
);
    wire [1:0] c6p; wire c6s;
    wire [1:0] s3p; wire s3s;
    w33_c6_fibre u_c6 (.p_in(p_in), .s_in(s_in), .pow(3'd3), .p_out(c6p), .s_out(c6s));
    w33_s3_fibre u_s3 (.p_in(p_in), .s_in(s_in), .a(2'd0), .b(1'b1),
                       .p_out(s3p), .s_out(s3s));
    assign c6_orientation_changed = (c6p != p_in);
    assign s3_orientation_changed = (s3p != p_in);
endmodule
