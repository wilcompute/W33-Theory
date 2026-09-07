`timescale 1ns/1ps
module tb_w33_pass3067_adaptive_belief_controller;
 localparam W=18;logic clk=0,rst_n=0,load_class=0,observation_valid=0;
 logic[1:0] class_size,decision,probes_used;logic signed[W-1:0] prior0,prior1,prior2,stop_gap,ll0,ll1,ll2;
 logic[6:0] first_test,second_test,requested_test;logic busy,request_valid,stop_valid;
 w33_pass3067_adaptive_belief_controller #(.SCORE_W(W),.TEST_W(7)) dut(.*);always #5 clk=~clk;
 task tick;begin @(posedge clk);#1;end endtask
 task load3(input[6:0]a,input[6:0]b,input signed[W-1:0]gap);begin class_size=3;prior0=0;prior1=0;prior2=0;stop_gap=gap;first_test=a;second_test=b;load_class=1;tick();load_class=0;if(!request_valid||requested_test!=a)$fatal(1,"first request");end endtask
 task observe(input signed[W-1:0]a,input signed[W-1:0]b,input signed[W-1:0]c);begin ll0=a;ll1=b;ll2=c;observation_valid=1;tick();observation_valid=0;tick();end endtask
 initial begin class_size=0;prior0=0;prior1=0;prior2=0;stop_gap=0;first_test=0;second_test=0;ll0=0;ll1=0;ll2=0;repeat(2)tick();rst_n=1;tick();
  load3(13,18,100);observe(140,-40,-60);if(!stop_valid||decision!=0||probes_used!=1)$fatal(1,"decisive stop");tick();
  load3(4,11,100);observe(0,0,0);if(!request_valid||requested_test!=11||probes_used!=1)$fatal(1,"erasure escalation");observe(-50,180,-70);if(!stop_valid||decision!=1||probes_used!=2)$fatal(1,"second decision");tick();
  load3(1,2,100);observe(0,0,0);if(!request_valid)$fatal(1,"horizon request");observe(0,0,0);if(!stop_valid||probes_used!=2)$fatal(1,"horizon stop");
  $display("PASS adaptive belief controller: decisive, erasure escalation, horizon");$finish;end
endmodule
