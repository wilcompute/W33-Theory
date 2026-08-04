`timescale 1ns/1ps
module tb_w33_pass3155_3160_factor_epoch_scheduler;
  localparam W=18;
  logic clk=0,rst=1,start,baseline_valid,factor_valid;
  logic signed [W-1:0] baseline;
  logic signed [7*W-1:0] bundle;
  logic rpair;logic [2:0] rbank;logic [8:0] raddr;logic signed [W-1:0] rdata,bout;
  logic busy,done;logic [9:0] cyc;logic pairp;logic [5:0] edge;logic [6:0] pidx;logic [2:0] label;
  logic symv;logic [4:0] sym;logic marker,elock;logic [3:0] phase;logic [15:0] epochs;
  logic [15:0] basecost,ceff;logic [7:0] entropy,route,conf;logic calibrated,lowmode,sw;
  integer i,b;
  always #5 clk=~clk;
  w33_pass3155_sparse_factor_engine #(.W(W)) factor(
    .clk(clk),.rst(rst),.start_i(start),.baseline_valid_i(baseline_valid),.baseline_i(baseline),
    .factor_valid_i(factor_valid),.factor_bundle_i(bundle),.read_pair_i(rpair),
    .read_bank_i(rbank),.read_addr_i(raddr),.read_data_o(rdata),.baseline_o(bout),
    .busy_o(busy),.done_o(done),.cycle_o(cyc),.pair_phase_o(pairp),
    .unary_edge_o(edge),.pair_index_o(pidx),.left_label_o(label));
  w33_pass3157_epoch_tracker epoch(.clk(clk),.rst(rst),.symbol_valid_i(symv),.symbol_i(sym),
    .marker_seen_o(marker),.epoch_locked_o(elock),.phase_o(phase),.epoch_count_o(epochs));
  w33_pass3160_dual_isa_scheduler sched(.clk(clk),.rst(rst),
    .base_collision_cost_q8_8_i(basecost),.causal_entropy_q4_4_i(entropy),
    .route_burden_q4_4_i(route),.calibration_confidence_q0_8_i(conf),
    .low_isa_calibrated_i(calibrated),.low_collision_mode_o(lowmode),.switch_o(sw),
    .effective_collision_cost_q8_8_o(ceff));
  task tick;begin @(negedge clk);@(posedge clk);#1;end endtask
  task send(input [4:0] x);begin @(negedge clk);sym=x;symv=1;@(posedge clk);#1;symv=0;end endtask
  initial begin
    start=0;baseline_valid=0;factor_valid=0;bundle='0;rpair=0;rbank=0;raddr=0;
    symv=0;sym=0;basecost=0;entropy=0;route=0;conf=8'hff;calibrated=1;
    repeat(2)tick();rst=0;
    baseline=18'sd77;baseline_valid=1;tick();baseline_valid=0;
    start=1;tick();start=0;
    for(i=0;i<528;i=i+1) begin
      for(b=0;b<7;b=b+1) bundle[b*W +: W]=i*10+b;
      factor_valid=1;tick();
      if(i==44 && pairp!==1'b1) $fatal(1,"pair phase did not begin after unary cycle");
    end
    factor_valid=0;
    if(!done || busy) $fatal(1,"factor sweep did not finish");
    if(bout!==18'sd77) $fatal(1,"baseline mismatch");
    rpair=0;rbank=3'd2;raddr=9'd44;tick();
    if(rdata!==18'sd442) $fatal(1,"unary read mismatch %0d",rdata);
    rpair=1;rbank=3'd6;raddr=9'd482;tick();
    if(rdata!==18'sd5276) $fatal(1,"correction read mismatch %0d",rdata);

    // Two adversarial corruptions inside ABABA still leave three rare symbols.
    send(5'd1);send(5'd7);send(5'd1);send(5'd2);send(5'd1);
    send(5'd7);send(5'd2);
    if(!elock || phase!==4'd2 || epochs!==16'd1) $fatal(1,"epoch reacquisition failed");

    // High effective collision price crosses the upward hysteresis threshold.
    basecost=16'd1024;entropy=8'd64;route=8'd32;conf=8'd128;tick();
    if(!lowmode || !sw) $fatal(1,"scheduler did not select low-collision ISA");
    calibrated=0;tick();
    if(lowmode || !sw) $fatal(1,"uncalibrated low ISA did not fail closed");
    calibrated=1;basecost=16'd256;entropy=0;route=0;conf=8'hff;tick();
    if(lowmode) $fatal(1,"low-cost state selected wrong ISA");
    $display("PASS split factor memories, robust epoch marker and adaptive dual ISA");
    $finish;
  end
endmodule
