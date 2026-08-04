`timescale 1ns/1ps
module tb_w33_pass3028_adaptive_belief_controller;
    localparam W=18;
    logic clk=0, rst_n=0, load_class=0, observation_valid=0;
    logic [1:0] class_size;
    logic signed [W-1:0] prior0,prior1,prior2,stop_gap,ll0,ll1,ll2;
    logic [6:0] first_test,second_test,requested_test;
    logic busy,request_valid,stop_valid;
    logic [1:0] decision,probes_used;

    w33_pass3028_adaptive_belief_controller #(.SCORE_W(W),.TEST_W(7)) dut(.*);
    always #5 clk=~clk;

    task tick; begin @(posedge clk); #1; end endtask
    task load3(input [6:0] a,input [6:0] b,input signed [W-1:0] gap);
      begin
        class_size=3; prior0=0; prior1=0; prior2=0; stop_gap=gap;
        first_test=a; second_test=b; load_class=1; tick(); load_class=0;
        if (!request_valid || requested_test!=a) $fatal(1,"first request mismatch");
      end
    endtask
    task observe(input signed [W-1:0] a,input signed [W-1:0] b,input signed [W-1:0] c);
      begin
        ll0=a;ll1=b;ll2=c;observation_valid=1;tick();observation_valid=0;tick();
      end
    endtask

    initial begin
      class_size=0;prior0=0;prior1=0;prior2=0;stop_gap=0;
      first_test=0;second_test=0;ll0=0;ll1=0;ll2=0;
      repeat(2) tick(); rst_n=1; tick();

      // One decisive observation stops after the first requested test.
      load3(7'd13,7'd18,18'sd100);
      observe(18'sd140,-18'sd40,-18'sd60);
      if (!stop_valid || decision!=0 || probes_used!=1) $fatal(1,"decisive stop failed");
      tick();

      // An erasure-like equal likelihood requests the second test; the second outcome
      // then decides hypothesis one.
      load3(7'd4,7'd11,18'sd100);
      observe(0,0,0);
      if (!request_valid || requested_test!=7'd11 || probes_used!=1) $fatal(1,"escalation failed");
      observe(-18'sd50,18'sd180,-18'sd70);
      if (!stop_valid || decision!=1 || probes_used!=2) $fatal(1,"second-probe decision failed");
      tick();

      // Horizon guard: after two uninformative probes the core must terminate.
      load3(7'd1,7'd2,18'sd100);
      observe(0,0,0);
      if (!request_valid) $fatal(1,"second probe was not requested");
      observe(0,0,0);
      if (!stop_valid || probes_used!=2) $fatal(1,"horizon stop failed");

      $display("PASS adaptive belief controller: decisive, erasure escalation, horizon");
      $finish;
    end
endmodule
