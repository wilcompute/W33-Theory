// Pass 2457 -- the periodic/growing split as a modulator architecture.
//
// Pass 2439/2452: M = R4^2 U6 splits the phase carrier into
//    A-sector (the V9 in the 24)  eigenvalue -1     PERIOD EXACTLY 2
//    BC-pair  (the two V9s in 90) Fibonacci matrix  GROWS LIKE phi^n
//
// Read as hardware that is a modulator: the period-2 register is a chirality
// SELECT line -- it alternates every cycle and nothing else -- while the BC pair
// is an AMPLITUDE accumulator whose successive values are Fibonacci-scaled.
//
// Pass 2449 makes the reading concrete: the outer involution exchanges the two
// chiralities of the E8 carrier, so a one-bit alternating select is exactly the
// right control for a two-path chirality switch.  This module is that control
// path, not an optical model: it emits a select bit and an amplitude word.

`timescale 1ns/1ps

module w33_chirality_modulator #(parameter W = 20) (
    input  wire                clk,
    input  wire                rst,
    output wire                path_select,   // which chirality the light takes
    output wire signed [W-1:0] amplitude,     // Fibonacci-scaled drive level
    output wire signed [W-1:0] amplitude_prev
);
    // A-sector: one signed value negated every cycle.  Its SIGN is the select line.
    reg signed [W-1:0] a;
    // BC-pair: (b,c) -> (-c, c-b), the Fibonacci action on the quotient.
    reg signed [W-1:0] b, c;

    always_ff @(posedge clk) begin
        if (rst) begin
            a <= 1;      // any nonzero seed; the A-sector only ever flips sign
            b <= 0;
            c <= 1;      // Fibonacci seed
        end else begin
            a <= -a;
            b <= -c;
            c <=  c - b;
        end
    end

    assign path_select    = a[W-1];   // sign bit: alternates with period 2
    assign amplitude      = c;
    assign amplitude_prev = b;
endmodule

// The two claims, isolated for formal proof, combinationally.
module w33_modulator_step #(parameter W = 20) (
    input  wire signed [W-1:0] a_in, b_in, c_in,
    output wire signed [W-1:0] a_out, b_out, c_out
);
    assign a_out = -a_in;
    assign b_out = -c_in;
    assign c_out =  c_in - b_in;
endmodule
