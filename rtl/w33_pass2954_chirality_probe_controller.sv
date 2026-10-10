// Pass 2954 -- frame-conditioned local-Y chirality probe controller.
//
// The quantum operation is local: select one qubit, apply S^dagger then H, and perform
// ordinary Z readout. This controller supplies the selected qubit and interprets the
// measured Y eigenvalue. It does NOT distinguish an unknown uniformly drawn class;
// the pair/frame identifier is required because both class ensembles equal I_4/4.

`timescale 1ns/1ps
module w33_pass2954_chirality_probe_controller (
    input  wire [3:0] pair_id,
    input  wire       measured_plus,
    output reg        valid,
    output reg        select_second_qubit,
    output reg        expected_plus_for_class_a,
    output wire       class_a_estimate
);
    always_comb begin
        valid = 1'b1;
        select_second_qubit = 1'b1; // IY by default
        expected_plus_for_class_a = 1'b0;
        case (pair_id)
            4'd0: begin select_second_qubit=1; expected_plus_for_class_a=0; end // 1 <-> 2
            4'd1: begin select_second_qubit=1; expected_plus_for_class_a=1; end // 3 <-> 6
            4'd2: begin select_second_qubit=0; expected_plus_for_class_a=0; end // 8 <-> 4
            4'd3: begin select_second_qubit=1; expected_plus_for_class_a=1; end // 10 <-> 11
            4'd4: begin select_second_qubit=1; expected_plus_for_class_a=0; end // 12 <-> 15
            4'd5: begin select_second_qubit=0; expected_plus_for_class_a=1; end // 17 <-> 13
            4'd6: begin select_second_qubit=0; expected_plus_for_class_a=0; end // 19 <-> 20
            4'd7: begin select_second_qubit=1; expected_plus_for_class_a=0; end // 21 <-> 24
            4'd8: begin select_second_qubit=1; expected_plus_for_class_a=1; end // 26 <-> 22
            4'd9: begin select_second_qubit=0; expected_plus_for_class_a=1; end // 28 <-> 29
            4'd10:begin select_second_qubit=1; expected_plus_for_class_a=1; end // 30 <-> 33
            4'd11:begin select_second_qubit=1; expected_plus_for_class_a=0; end // 35 <-> 31
            default: begin valid=0; select_second_qubit=0; expected_plus_for_class_a=0; end
        endcase
    end
    assign class_a_estimate = valid && (measured_plus == expected_plus_for_class_a);
endmodule
