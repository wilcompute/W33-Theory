`timescale 1ns/1ps
module tb_w33_pass2938_isodual_support_codec;
 logic [1:0] x0,x1,x2,x3,dx0,dx1,dx2,dx3; logic [15:0] code,received; logic valid,corrected; integer a,b,c,d,k;
 w33_pass2938_isodual_support_encoder e(.x0,.x1,.x2,.x3,.code);
 w33_pass2938_isodual_support_decoder q(.received,.valid,.corrected,.x0(dx0),.x1(dx1),.x2(dx2),.x3(dx3));
 initial begin
  for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(d=0;d<3;d=d+1)begin
   x0=a;x1=b;x2=c;x3=d;#1;received=code;#1;if(!valid||{dx0,dx1,dx2,dx3}!={x0,x1,x2,x3})$fatal(1,"clean");
   for(k=0;k<16;k=k+1)begin received=code^(16'b1<<k);#1;if(!valid||!corrected||{dx0,dx1,dx2,dx3}!={x0,x1,x2,x3})$fatal(1,"bit %0d",k);end
  end
  $display("PASS 81 clean + 1296 one-bit corrections");$finish;
 end
endmodule
