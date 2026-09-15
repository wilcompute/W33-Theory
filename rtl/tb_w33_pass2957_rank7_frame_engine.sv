`timescale 1ns/1ps
module tb_w33_pass2957_rank7_frame_engine;
  reg clk=0,rst=0,load=0,valid=0;
  reg [1:0] xp_in,zp_in,xf_in,zf_in,opcode;
  wire [1:0] xp,zp,xf,zf;wire [6:0] rank;
  integer a,b,c,d,op;reg [1:0] ex_xp,ex_zp,ex_xf,ex_zf;
  w33_pass2957_rank7_frame_engine dut(.clk(clk),.rst(rst),.load(load),.valid(valid),
    .xp_in(xp_in),.zp_in(zp_in),.xf_in(xf_in),.zf_in(zf_in),.opcode(opcode),
    .xp(xp),.zp(zp),.xf(xf),.zf(zf),.rank(rank));
  always #1 clk=~clk;
  function [1:0] add3(input [1:0] x,input [1:0] y);integer t;begin t=x+y;add3=t>=3?t-3:t;end endfunction
  function [1:0] neg3(input [1:0] x);begin neg3=x==0?0:x==1?2:1;end endfunction
  function [1:0] sub3(input [1:0] x,input [1:0] y);begin sub3=add3(x,neg3(y));end endfunction
  task load_state(input integer ia,ib,ic,id);begin
    xp_in=ia;zp_in=ib;xf_in=ic;zf_in=id;load=1;valid=0;@(posedge clk);#0.1;load=0;
  end endtask
  initial begin
    rst=1;@(posedge clk);#0.1;rst=0;
    for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(d=0;d<3;d=d+1)begin
      load_state(a,b,c,d);
      if(rank!==27*a+9*b+3*c+d)$fatal(1,"load rank mismatch");
      for(op=0;op<4;op=op+1)begin
        ex_xp=a;ex_zp=b;ex_xf=c;ex_zf=d;
        case(op)
          0:begin ex_xp=neg3(b);ex_zp=a;end
          1:begin ex_zp=sub3(b,d);ex_xf=add3(c,a);end
          2:begin ex_xp=add3(a,c);ex_zf=sub3(d,b);end
          3:begin ex_zp=add3(b,1);end
        endcase
        load_state(a,b,c,d);opcode=op;valid=1;@(posedge clk);#0.1;valid=0;
        if(xp!==ex_xp||zp!==ex_zp||xf!==ex_xf||zf!==ex_zf)$fatal(1,"transition mismatch");
        if(rank!==27*ex_xp+9*ex_zp+3*ex_xf+ex_zf)$fatal(1,"transition rank mismatch");
      end
    end
    $display("PASS 324/324 rank7 transitions");$finish;
  end
endmodule
