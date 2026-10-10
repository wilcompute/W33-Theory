`timescale 1ns/1ps
module tb_w33_pass2954_2959_chirality_control;
    reg [3:0] pair_id;
    reg measured_plus;
    wire valid, select_second_qubit, expected_plus_for_class_a, class_a_estimate;
    reg [1:0] phase_sum_i;
    reg mirror_i;
    wire [1:0] phase_sum_o;
    wire mirror_o, legal_o, middle_class_a_o, middle_class_b_o;
    integer pair, outcome, phase, mirror;

    w33_pass2954_chirality_probe_controller probe(
        .pair_id(pair_id), .measured_plus(measured_plus), .valid(valid),
        .select_second_qubit(select_second_qubit),
        .expected_plus_for_class_a(expected_plus_for_class_a),
        .class_a_estimate(class_a_estimate));
    w33_pass2959_chirality_mirror_metadata metadata(
        .phase_sum_i(phase_sum_i), .mirror_i(mirror_i), .phase_sum_o(phase_sum_o),
        .mirror_o(mirror_o), .legal_o(legal_o),
        .middle_class_a_o(middle_class_a_o), .middle_class_b_o(middle_class_b_o));

    initial begin
        for (pair=0; pair<12; pair=pair+1) begin
            pair_id=pair;
            for (outcome=0; outcome<2; outcome=outcome+1) begin
                measured_plus=outcome; #1;
                if (!valid) $fatal(1,"valid pair rejected");
                if (class_a_estimate !== (measured_plus == expected_plus_for_class_a))
                    $fatal(1,"class interpretation mismatch");
            end
        end
        pair_id=12; measured_plus=0; #1;
        if (valid) $fatal(1,"invalid pair accepted");

        for (phase=0; phase<3; phase=phase+1)
          for (mirror=0; mirror<2; mirror=mirror+1) begin
            phase_sum_i=phase; mirror_i=mirror; #1;
            if (!legal_o || mirror_o!==mirror_i) $fatal(1,"metadata legality/reversibility failure");
            if (!mirror && phase_sum_o!==phase) $fatal(1,"identity mirror mismatch");
            if (mirror && phase==1 && phase_sum_o!==2) $fatal(1,"1->2 mismatch");
            if (mirror && phase==2 && phase_sum_o!==1) $fatal(1,"2->1 mismatch");
            if (mirror && phase==0 && phase_sum_o!==0) $fatal(1,"0 fixed mismatch");
          end
        phase_sum_i=3; mirror_i=0; #1;
        if (legal_o) $fatal(1,"illegal phase accepted");
        $display("PASS 24 probe outcomes and 6 reversible metadata states");
        $finish;
    end
endmodule
