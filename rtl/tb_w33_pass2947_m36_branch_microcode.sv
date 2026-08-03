`timescale 1ns/1ps
module tb_w33_pass2947_m36_branch_microcode;
 logic [4:0] step;logic valid;logic [1:0] kind,q0,q1;logic accept_value;integer i,cx,h,m;
 w33_pass2947_m36_branch_microcode d(.*);
 initial begin cx=0;h=0;m=0;
  for(i=0;i<17;i=i+1)begin step=i;#1;if(!valid)$fatal(1,"invalid step %0d",i);case(kind)0:cx=cx+1;1:h=h+1;2:m=m+1;endcase end
  if(cx!=12||h!=3||m!=2)$fatal(1,"counts %0d %0d %0d",cx,h,m);
  step=17;#1;if(valid)$fatal(1,"illegal step accepted");
  $display("PASS 12 CNOT + 3 H + 2 MZ microcode");$finish;
 end
endmodule
