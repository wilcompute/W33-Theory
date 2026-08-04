`timescale 1ns/1ps
module tb_w33_pass3148_3150_recursive_execution;
    logic clk=0,rst=1;
    always #5 clk=~clk;

    logic [1:0] x0,x1,x2,x3,op;
    logic [1:0] cy0,cy1,cy2,cy3,ay0,ay1,ay2,ay3;
    w33_pass3148_affine_dispatch current_dispatch(
        .x0_i(x0),.x1_i(x1),.x2_i(x2),.x3_i(x3),.opcode_i(op),
        .y0_o(cy0),.y1_o(cy1),.y2_o(cy2),.y3_o(cy3));
    w33_pass3148_affine_dispatch #(.ALTERNATIVE_ISA(1'b1)) alternative_dispatch(
        .x0_i(x0),.x1_i(x1),.x2_i(x2),.x3_i(x3),.opcode_i(op),
        .y0_o(ay0),.y1_o(ay1),.y2_o(ay2),.y3_o(ay3));

    logic [3:0] ctx;
    logic context_reset,inference_valid,epoch,blind,symbol_valid,edit_enable;
    logic signed [17:0] l0,l1,l2,l3,l4,o0,o1,o2,o3,o4;
    logic [8:0] next_state,state_o;
    logic [3:0] tier,action_o,next_ctx;
    logic [4:0] symbol;
    logic cal_load,cal_bank,cal_commit;
    logic [6:0] cal_addr;
    logic [15:0] cal_data,cal_q;
    logic stop_o,sync_locked,sync_valid;
    logic [11:0] phase_mask;
    logic [3:0] phase;

    w33_pass3149_recursive_execution_controller #(.NCTX(16)) dut(
        .clk(clk),.rst(rst),.ctx_i(ctx),.context_reset_i(context_reset),
        .inference_valid_i(inference_valid),
        .lane0_i(l0),.lane1_i(l1),.lane2_i(l2),.lane3_i(l3),.lane4_i(l4),
        .next_causal_state_i(next_state),.budget_tier_i(tier),
        .epoch_i(epoch),.blind_acquire_i(blind),.symbol_valid_i(symbol_valid),
        .edit_enable_i(edit_enable),.symbol_i(symbol),
        .calibration_load_i(cal_load),.calibration_load_bank_i(cal_bank),
        .calibration_addr_i(cal_addr),.calibration_data_i(cal_data),
        .calibration_commit_i(cal_commit),.calibration_data_o(cal_q),
        .lane0_o(o0),.lane1_o(o1),.lane2_o(o2),.lane3_o(o3),.lane4_o(o4),
        .causal_state_o(state_o),.action_o(action_o),.stop_o(stop_o),
        .phase_mask_o(phase_mask),.phase_o(phase),.sync_locked_o(sync_locked),
        .sync_valid_o(sync_valid),.next_round_robin_ctx_o(next_ctx));

    task tick; begin @(negedge clk); @(posedge clk); #1; end endtask
    task clear_controls; begin
        context_reset=0;inference_valid=0;epoch=0;blind=0;symbol_valid=0;
        edit_enable=0;cal_load=0;cal_commit=0;
    end endtask

    initial begin
        x0=1;x1=2;x2=0;x3=1;op=0;
        ctx=0;clear_controls();
        l0=0;l1=0;l2=0;l3=0;l4=0;next_state=0;tier=0;symbol=0;
        cal_bank=0;cal_addr=0;cal_data=0;
        repeat(2) tick();rst=0;

        #1;
        if ({cy0,cy1,cy2,cy3} !== {2'd1,2'd1,2'd0,2'd1})
            $fatal(1,"current F_p dispatch mismatch");
        op=2;#1;
        if ({ay0,ay1,ay2,ay3} !== {2'd1,2'd2,2'd2,2'd0})
            $fatal(1,"alternative F_f dispatch mismatch");
        op=3;#1;
        if (ay0!==2'd2) $fatal(1,"alternative Z0 dispatch mismatch");

        // Clean blind acquisition: the pair (7,2) uniquely identifies phase two.
        ctx=0;blind=1;tick();clear_controls();
        symbol=5'd7;symbol_valid=1;tick();clear_controls();
        symbol=5'd2;symbol_valid=1;tick();clear_controls();
        if (!sync_valid || !sync_locked || phase!==4'd2)
            $fatal(1,"two-symbol blind acquisition failed: mask=%h phase=%0d",phase_mask,phase);

        // Double-buffered calibration load and atomic bank commit.
        cal_bank=1;cal_addr=7'd5;cal_data=16'h1234;cal_load=1;tick();clear_controls();
        cal_bank=1;cal_commit=1;tick();clear_controls();
        cal_addr=7'd5;#1;
        if (cal_q!==16'h1234) $fatal(1,"calibration bank commit failed");

        // Context two receives a V4 action; context three receives full D4.
        ctx=2;l0=18'sd1000;l1=-18'sd1000;l2=18'sd1000;l3=18'sd1000;l4=18'sd1000;
        next_state=9'd77;tier=4'd4;inference_valid=1;tick();clear_controls();
        if (state_o!==9'd77 || action_o!==4'd3 || o0!==18'sd859)
            $fatal(1,"context two inference mismatch");
        ctx=3;next_state=9'd88;tier=4'd10;inference_valid=1;tick();clear_controls();
        if (state_o!==9'd88 || action_o!==4'd5)
            $fatal(1,"context three inference mismatch");
        ctx=2;#1;
        if (state_o!==9'd77 || action_o!==4'd3)
            $fatal(1,"context isolation failed");

        context_reset=1;tick();clear_controls();
        if (state_o!==0 || action_o!==0 || !stop_o)
            $fatal(1,"selected context reset failed");

        ctx=15;#1;
        if (next_ctx!==0) $fatal(1,"round-robin wrap failed");

        $display("PASS universal dispatch, blind acquisition, calibration and recursive contexts");
        $finish;
    end
endmodule
