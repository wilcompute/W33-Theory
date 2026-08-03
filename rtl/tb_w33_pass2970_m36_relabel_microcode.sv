`timescale 1ns/1ps
module tb_w33_pass2970_m36_relabel_microcode;
logic [3:0] pc; logic [2:0] op; logic [1:0] q0,q1; logic ex; integer i,h,cx,m;
w33_pass2970_m36_relabel_microcode d(.pc(pc),.opcode(op),.q0(q0),.q1(q1),.expected(ex));
initial begin h=0;cx=0;m=0; for(i=0;i<11;i=i+1)begin pc=i;#1;if(op==1)h=h+1;if(op==2)cx=cx+1;if(op==3)m=m+1;end
 if(h!=3||cx!=6||m!=2)$fatal(1,"counts h=%0d cx=%0d m=%0d",h,cx,m);
 pc=9;#1;if(q0!=2||ex!=0)$fatal(1,"measure q2");pc=10;#1;if(q0!=3||ex!=1)$fatal(1,"measure q3");
 $display("PASS 9-gate M36 microcode: 6 CX, 3 H, 2 MZ");$finish;end
endmodule
