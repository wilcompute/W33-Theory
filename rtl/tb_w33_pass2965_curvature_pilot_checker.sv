`timescale 1ns/1ps
module tb_w33_pass2965_curvature_pilot_checker;
logic [1:0] e0,e1,e2,o0,o1,o2;logic fault;
w33_pass2965_curvature_pilot_checker dut(.expected0(e0),.expected1(e1),.expected2(e2),.observed0(o0),.observed1(o1),.observed2(o2),.route_fault(fault));
initial begin e0=0;e1=1;e2=2;o0=0;o1=1;o2=2;#1;if(fault)$fatal(1,"false alarm");o2=3;#1;if(!fault)$fatal(1,"miss");$display("PASS curvature pilot checker");$finish;end
endmodule
