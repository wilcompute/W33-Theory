`timescale 1ns/1ps
`default_nettype none

module tb_w33_pass3254_3258_typed_reset_gate;
    logic [1:0] universe_id;
    logic [3:0] opcode_count;
    logic group_order_ok, manifest_valid, projection_valid;
    logic admitted, census_member, comparison_only, comparison_enabled;

    logic clk = 1'b0;
    logic rst_n, authorization_valid, proof_root_match, reset_request, passive_event;
    logic armed, reset_pulse;

    logic terminal_valid;
    logic [1:0] terminal_class, proposed_terminal_class, next_terminal_class;
    logic violation;

    always #5 clk = ~clk;

    w33_pass3254_universe_admission dut_universe (
        .universe_id(universe_id),
        .opcode_count(opcode_count),
        .group_order_ok(group_order_ok),
        .manifest_valid(manifest_valid),
        .projection_valid(projection_valid),
        .admitted(admitted),
        .census_member(census_member),
        .comparison_only(comparison_only),
        .comparison_enabled(comparison_enabled)
    );

    w33_pass3257_authorized_reset dut_reset (
        .clk(clk), .rst_n(rst_n),
        .authorization_valid(authorization_valid),
        .proof_root_match(proof_root_match),
        .reset_request(reset_request),
        .passive_event(passive_event),
        .armed(armed), .reset_pulse(reset_pulse)
    );

    w33_pass3258_passive_terminal_guard dut_guard (
        .terminal_valid(terminal_valid),
        .terminal_class(terminal_class),
        .passive_event(passive_event),
        .proposed_terminal_class(proposed_terminal_class),
        .next_terminal_class(next_terminal_class),
        .violation(violation)
    );

    task tick;
        begin
            @(posedge clk);
            #1;
        end
    endtask

    initial begin
        universe_id = 2'b00;
        opcode_count = 4;
        group_order_ok = 1'b1;
        manifest_valid = 1'b0;
        projection_valid = 1'b1;
        #1;
        if (!(admitted && comparison_only && !census_member && comparison_enabled))
            $fatal(1, "four-opcode baseline typing failed");

        universe_id = 2'b01;
        opcode_count = 4;
        #1;
        if (admitted) $fatal(1, "four-opcode record entered 194 census");

        opcode_count = 6;
        #1;
        if (!(admitted && census_member && !comparison_only))
            $fatal(1, "six-opcode census admission failed");

        projection_valid = 1'b0;
        #1;
        if (comparison_enabled) $fatal(1, "comparison enabled without projection");

        universe_id = 2'b10;
        opcode_count = 7;
        group_order_ok = 1'b1;
        manifest_valid = 1'b0;
        projection_valid = 1'b1;
        #1;
        if (admitted) $fatal(1, "future universe admitted without manifest");
        manifest_valid = 1'b1;
        #1;
        if (!(admitted && comparison_only && !census_member))
            $fatal(1, "manifested future universe admission failed");

        terminal_valid = 1'b1;
        terminal_class = 2'b10;
        passive_event = 1'b1;
        proposed_terminal_class = 2'b01;
        #1;
        if (!(violation && next_terminal_class == terminal_class))
            $fatal(1, "passive terminal mutation was not blocked");
        proposed_terminal_class = terminal_class;
        #1;
        if (violation) $fatal(1, "legal passive terminal hold flagged");

        authorization_valid = 1'b0;
        proof_root_match = 1'b0;
        reset_request = 1'b0;
        passive_event = 1'b0;
        rst_n = 1'b0;
        tick();
        rst_n = 1'b1;
        tick();
        if (armed || reset_pulse) $fatal(1, "reset state not clear");

        reset_request = 1'b1;
        proof_root_match = 1'b1;
        tick();
        if (reset_pulse || armed) $fatal(1, "unarmed reset emitted pulse");
        reset_request = 1'b0;

        authorization_valid = 1'b1;
        proof_root_match = 1'b0;
        tick();
        if (armed) $fatal(1, "invalid root armed reset");

        proof_root_match = 1'b1;
        tick();
        if (!armed) $fatal(1, "valid authorization did not arm");
        authorization_valid = 1'b0;

        passive_event = 1'b1;
        tick();
        if (!armed || reset_pulse) $fatal(1, "passive event altered authorization latch");
        passive_event = 1'b0;

        proof_root_match = 1'b0;
        reset_request = 1'b1;
        tick();
        if (reset_pulse || armed) $fatal(1, "mismatched reset did not fail closed");
        reset_request = 1'b0;

        authorization_valid = 1'b1;
        proof_root_match = 1'b1;
        tick();
        if (!armed) $fatal(1, "re-authorization failed");
        authorization_valid = 1'b0;
        reset_request = 1'b1;
        tick();
        if (!reset_pulse || armed) $fatal(1, "authorized reset pulse failed");
        reset_request = 1'b0;
        tick();
        if (reset_pulse) $fatal(1, "reset pulse persisted beyond one cycle");

        authorization_valid = 1'b1;
        reset_request = 1'b1;
        tick();
        if (reset_pulse || armed) $fatal(1, "one-cycle authorize/reset bypassed two-token contract");

        $display("PASS typed runtime universes, passive terminal guard, and two-token authorized reset");
        $finish;
    end
endmodule

`default_nettype wire
