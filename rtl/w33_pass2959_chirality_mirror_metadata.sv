// Pass 2959 -- reversible C3 phase-label reflection controlled by the D12 mirror bit.
// Keeping mirror_o makes (phase,mirror)->(reflected_phase,mirror) bijective.
// This is metadata transport, not complex conjugation of an unknown quantum state.

`timescale 1ns/1ps
module w33_pass2959_chirality_mirror_metadata (
    input  wire [1:0] phase_sum_i,  // legal values 0,1,2
    input  wire       mirror_i,
    output reg  [1:0] phase_sum_o,
    output wire       mirror_o,
    output wire       legal_o,
    output wire       middle_class_a_o,
    output wire       middle_class_b_o
);
    assign legal_o = phase_sum_i != 2'd3;
    assign mirror_o = mirror_i;
    always_comb begin
        if (!legal_o) phase_sum_o = 2'd0;
        else if (!mirror_i || phase_sum_i == 2'd0) phase_sum_o = phase_sum_i;
        else if (phase_sum_i == 2'd1) phase_sum_o = 2'd2;
        else phase_sum_o = 2'd1;
    end
    assign middle_class_a_o = legal_o && phase_sum_o == 2'd1;
    assign middle_class_b_o = legal_o && phase_sum_o == 2'd2;
endmodule
