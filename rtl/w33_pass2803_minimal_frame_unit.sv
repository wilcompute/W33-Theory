// Pass 2803 -- minimal exact affine frame micro-engine.
// 00 F_p, 01 CX_p->f, 10 CX_f->p, 11 Z_p.
// The linear trio generates Sp(4,3); the one translation completes ASp(4,3).
`timescale 1ns/1ps
module w33_pass2803_minimal_frame_unit(
 input wire clk,input wire rst,input wire load,
 input wire [1:0] xp_in,zp_in,xf_in,zf_in,
 input wire valid,input wire [1:0] micro_op,
 output reg [1:0] xp,zp,xf,zf);
 function automatic [1:0] clamp3(input [1:0] v);clamp3=(v==3)?0:v;endfunction
 function automatic [1:0] add3(input [1:0] a,input [1:0] b);reg[2:0] s;begin s=a+b;add3=(s>=3)?s-3:s[1:0];end endfunction
 function automatic [1:0] neg3(input [1:0] v);neg3=(v==0)?0:(v==1)?2:1;endfunction
 function automatic [1:0] sub3(input [1:0] a,input [1:0] b);sub3=add3(a,neg3(b));endfunction
 reg[1:0] nxp,nzp,nxf,nzf;
 always_comb begin
  nxp=xp;nzp=zp;nxf=xf;nzf=zf;
  case(micro_op)
   0:begin nxp=neg3(zp);nzp=xp;end
   1:begin nzp=sub3(zp,zf);nxf=add3(xf,xp);end
   2:begin nxp=add3(xp,xf);nzf=sub3(zf,zp);end
   3:nzp=add3(zp,1);
  endcase
 end
 always_ff @(posedge clk) begin
  if(rst)begin xp<=0;zp<=0;xf<=0;zf<=0;end
  else if(load)begin xp<=clamp3(xp_in);zp<=clamp3(zp_in);xf<=clamp3(xf_in);zf<=clamp3(zf_in);end
  else if(valid)begin xp<=nxp;zp<=nzp;xf<=nxf;zf<=nzf;end
 end
endmodule
