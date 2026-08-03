`timescale 1ns/1ps
module tb_w33_pass2781_repeater_scheduler;
 localparam MAX_SEGMENTS=8;
 logic clk=0,rst=1,start=0,purify_accept=1,purify_done=0,swap_done=0,final_fidelity_ok=1;
 logic [7:0] segment_count=4;logic [2:0] elementary_purify_rounds=1,swap_purify_rounds=1;logic [31:0] cycle_counter=0;logic [MAX_SEGMENTS-1:0] elementary_valid=0;
 logic busy,done,erasure,timeout_fault,protocol_fault,request_elementary,request_purify,request_swap,pair_ready;logic[7:0]active_pairs;logic[3:0]nesting_level;logic[2:0]round_index;
 w33_pass2781_repeater_scheduler #(.MAX_SEGMENTS(MAX_SEGMENTS),.TIMEOUT_CYCLES(1000)) dut(.*);
 always #5 clk=~clk;always@(posedge clk)cycle_counter<=cycle_counter+1;
 task pulse(input integer which);begin case(which)0:start=1;1:purify_done=1;2:swap_done=1;endcase @(posedge clk);#1;start=0;purify_done=0;swap_done=0;end endtask
 task check(input logic cond,input integer code);begin if(!cond)begin $display("FAIL %0d",code);$fatal(1);end end endtask
 initial begin repeat(3)@(posedge clk);rst=0;@(posedge clk);pulse(0);check(busy&&request_elementary,1);elementary_valid=8'h0f;@(posedge clk);#1;check(request_purify,2);pulse(1);check(request_swap,3);pulse(2);check(request_purify&&active_pairs==2&&nesting_level==1,4);pulse(1);check(request_swap,5);pulse(2);check(request_purify&&active_pairs==1&&nesting_level==2,6);pulse(1);@(posedge clk);#1;check(done&&pair_ready&&!erasure,7);segment_count=3;pulse(0);check(done&&protocol_fault&&!busy,8);segment_count=2;elementary_purify_rounds=0;swap_purify_rounds=0;elementary_valid=0;final_fidelity_ok=0;pulse(0);elementary_valid=2'b11;@(posedge clk);#1;pulse(2);@(posedge clk);#1;check(done&&erasure&&!pair_ready,9);$display("PASS repeater scheduler");$finish;end
endmodule
