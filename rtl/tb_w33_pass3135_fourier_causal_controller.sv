`timescale 1ns/1ps
module tb_w33_pass3135_fourier_causal_controller;
    logic clk=0,rst=1,valid=0;
    logic signed [17:0] l0,l1,l2,l3,l4;
    logic [8:0] next_state;
    logic [3:0] next_action;
    logic signed [17:0] o0,o1,o2,o3,o4;
    logic [8:0] state_o;
    logic [3:0] action_o;
    logic stop_o;

    logic hv_valid;
    logic [1:0] hv_ctx,hv_probe;
    logic [8:0] hv_next,hv_selected,hv_probe_state;

    always #5 clk=~clk;
    w33_pass3135_fourier_causal_controller dut(
        .clk(clk),.rst(rst),.valid_i(valid),
        .lane0_i(l0),.lane1_i(l1),.lane2_i(l2),.lane3_i(l3),.lane4_i(l4),
        .next_causal_state_i(next_state),.next_action_i(next_action),
        .lane0_o(o0),.lane1_o(o1),.lane2_o(o2),.lane3_o(o3),.lane4_o(o4),
        .causal_state_o(state_o),.action_o(action_o),.stop_o(stop_o));

    w33_pass3139_belief_hypervisor #(.NCTX(4)) hv(
        .clk(clk),.rst(rst),.valid_i(hv_valid),.ctx_i(hv_ctx),
        .next_state_i(hv_next),.probe_ctx_i(hv_probe),
        .selected_state_o(hv_selected),.probe_state_o(hv_probe_state));

    task tick; begin @(negedge clk); @(posedge clk); #1; end endtask
    initial begin
        l0=0;l1=0;l2=0;l3=0;l4=0;next_state=0;next_action=0;
        hv_valid=0;hv_ctx=0;hv_probe=0;hv_next=0;
        repeat(2) tick(); rst=0;

        l0=18'sd1000;l1=-18'sd1000;l2=18'sd1000;l3=18'sd1000;l4=18'sd1000;
        next_state=9'd457;next_action=4'd6;valid=1;tick();valid=0;
        if (o0!==18'sd859) $fatal(1,"lane0 fixed-point mismatch: %0d",o0);
        if (o2!==18'sd899) $fatal(1,"lane2 fixed-point mismatch: %0d",o2);
        if (state_o!==9'd457 || action_o!==4'd6 || stop_o!==1'b0)
            $fatal(1,"causal/action update mismatch");

        next_state=9'd1;next_action=4'd0;valid=1;tick();valid=0;
        if (!stop_o) $fatal(1,"STOP action did not assert stop_o");

        hv_ctx=2'd1;hv_next=9'd77;hv_valid=1;tick();hv_valid=0;
        hv_ctx=2'd2;hv_next=9'd88;hv_valid=1;tick();hv_valid=0;
        hv_probe=2'd1;#1;
        if (hv_probe_state!==9'd77) $fatal(1,"guest 1 changed during guest 2 write");
        hv_probe=2'd2;#1;
        if (hv_probe_state!==9'd88) $fatal(1,"guest 2 state missing");

        $display("PASS Fourier-causal controller and belief-hypervisor isolation");
        $finish;
    end
endmodule
