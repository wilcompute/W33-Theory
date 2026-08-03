`timescale 1ns/1ps
module tb_w33_pass2778_metaplectic_sensor_controller;
 logic clk=0,rst=1,start=0,event_valid=0,event_bit=0,phase_lock_ok=1,determinant_valid=1;
 logic busy,done,fault;logic[1:0]power_k,quadrature;logic[31:0]shot_index,ones_count,a,b,c,d;
 w33_pass2778_metaplectic_sensor_controller #(.SHOTS_PER_QUADRATURE(4)) dut(.clk,.rst,.start,.event_valid,.event_bit,.phase_lock_ok,.determinant_valid,.busy,.done,.fault,.power_k,.quadrature,.shot_index,.ones_count,.theta1_re_ones(a),.theta1_im_ones(b),.theta2_re_ones(c),.theta2_im_ones(d));
 always #5 clk=~clk;
 task ev(input logic x);begin event_bit=x;event_valid=1;@(posedge clk);#1;event_valid=0;end endtask
 initial begin repeat(2)@(posedge clk);rst=0;start=1;@(posedge clk);#1;start=0;repeat(4)ev(1);repeat(4)ev(0);repeat(4)ev(1);repeat(4)ev(0);if(!done||fault||a!=4||b!=0||c!=4||d!=0)$fatal(1);start=1;phase_lock_ok=0;@(posedge clk);#1;start=0;if(!done||!fault)$fatal(1);$display("PASS metaplectic sensor controller");$finish;end
endmodule
