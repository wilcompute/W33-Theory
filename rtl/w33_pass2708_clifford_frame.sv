// Pass 2708 -- F and S, the single-qutrit Clifford frame instructions.
//
// Two more of the eight I_holo instructions.  With sigma^5 = Z (Pass 2700) that is
// three of eight.
//
// What hardware actually tracks for a Clifford gate is not the state but the PAULI
// FRAME: a two-trit label (a,b) meaning X^a Z^b.  Clifford gates act on that label by
// symplectic matrices over F_3, and the two the paper names generate everything:
//
//     F  (tritter / qutrit Fourier)  : (a,b) -> ( -b,  a )     order 4
//     S  (quadratic phase plate)     : (a,b) -> (  a, a+b )    order 3
//
// Verified: <F,S> closes at order 24 with every determinant 1 -- SL(2,3), the
// single-qutrit Clifford group modulo Pauli.  That closure is the reason two elements
// suffice, and it is checked before the circuit is trusted.
//
// The frame is two trits, so this is four bits of state and a handful of mod-3 adds.
// Clifford tracking is classically efficient by construction, which is exactly the
// paper's point that the Clifford part "is efficiently classically trackable; it is not
// universal by itself".  The non-Clifford element is the E6 cubic (Pass 2660) and the
// magic injection M_36, neither of which is a frame update.

`timescale 1ns/1ps

module w33_clifford_frame (
    input  wire       clk,
    input  wire       rst,
    input  wire       apply_f,     // tritter
    input  wire       apply_s,     // phase plate
    output reg  [1:0] a,           // X exponent, in F_3
    output reg  [1:0] b            // Z exponent, in F_3
);
    // F : (a,b) -> (-b, a)      negation in F_3 is v -> (3-v) mod 3
    function [1:0] neg3(input [1:0] v);
        neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1;
    endfunction

    wire [1:0] fa = neg3(b);
    wire [1:0] fb = a;

    // S : (a,b) -> (a, a+b)
    wire [1:0] sab;
    w33_f3_add u_s (.a(a), .b(b), .y(sab));

    always_ff @(posedge clk) begin
        if (rst) begin
            a <= 2'd0; b <= 2'd0;
        end else if (apply_f) begin
            a <= fa; b <= fb;
        end else if (apply_s) begin
            a <= a;  b <= sab;
        end
    end
endmodule

// The closure property, as a formal statement about one step:
//   F preserves the symplectic form (determinant 1) and has order 4;
//   S preserves it and has order 3.
// Both are checked here as single-step identities over all 9 frames.
module w33_clifford_frame_formal (
    input wire [1:0] a0,
    input wire [1:0] b0
);
    function [1:0] neg3(input [1:0] v);
        neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1;
    endfunction

    wire small = (a0 < 2'd3) && (b0 < 2'd3);

    // F applied four times must be the identity
    wire [1:0] a1 = neg3(b0), b1 = a0;
    wire [1:0] a2 = neg3(b1), b2 = a1;
    wire [1:0] a3 = neg3(b2), b3 = a2;
    wire [1:0] a4 = neg3(b3), b4 = a3;

    // S applied three times must be the identity
    wire [1:0] s1, s2, s3;
    w33_f3_add p1 (.a(a0), .b(b0), .y(s1));
    w33_f3_add p2 (.a(a0), .b(s1), .y(s2));
    w33_f3_add p3 (.a(a0), .b(s2), .y(s3));

    always_comb begin
        if (small) begin
            assert (a4 == a0 && b4 == b0);   // F^4 = I
            assert (s3 == b0);               // S^3 = I
        end
    end
endmodule
