`timescale 1ns/1ps
module tb_w33_pass2973_curvature_clock;
logic clk=0,reset=1,en=0,rev=0;logic[1:0]p,s;logic[3:0]t;integer i;reg[11:0]seen;
always #1 clk=~clk;
w33_pass2973_curvature_clock d(.clk(clk),.reset(reset),.enable(en),.reverse(rev),.phase3(p),.slot4(s),.tick12(t));
initial begin seen=0;#3;reset=0;en=1;for(i=0;i<12;i=i+1)begin #2;seen[t]=1;end if(seen!==12'hfff)$fatal(1,"not all ticks %h",seen);if(p!=0||s!=0)$fatal(1,"period");rev=1;#2;if(t!=11)$fatal(1,"reverse");$display("PASS D12 curvature clock 12 ticks and reversal");$finish;end
endmodule
