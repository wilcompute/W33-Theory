`timescale 1ns/1ps
module tb_w33_pass2951_isodual_quarter_turn;
 logic [15:0] a,b,c,d,e;integer n,i;logic [1:0] t;
 w33_pass2951_isodual_quarter_turn q1(.in_trits(a),.out_trits(b));
 w33_pass2951_isodual_quarter_turn q2(.in_trits(b),.out_trits(c));
 w33_pass2951_isodual_quarter_turn q3(.in_trits(c),.out_trits(d));
 w33_pass2951_isodual_quarter_turn q4(.in_trits(d),.out_trits(e));
 function automatic [1:0] neg3(input [1:0] x);case(x)0:neg3=0;1:neg3=2;2:neg3=1;default:neg3=3;endcase endfunction
 initial begin
  for(n=0;n<6561;n=n+1)begin
   integer x;x=n;a='0;
   for(i=0;i<8;i=i+1)begin a[2*i +:2]=x%3;x=x/3;end
   #1;
   if(e!==a)$fatal(1,"D4 failure %0d",n);
   for(i=0;i<8;i=i+1)if(c[2*i +:2]!==neg3(a[2*i +:2]))$fatal(1,"D2 failure %0d %0d",n,i);
  end
  $display("PASS 6561/6561 D^2=-I and D^4=I");$finish;
 end
endmodule
