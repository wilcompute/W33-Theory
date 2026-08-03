// Pass 2938: protected support codec via an isodual [8,4,4]_3 outer code. The decoder uses a 16-entry correction table.
module w33_pass2938_isodual_support_encoder(
 input logic [1:0] x0,x1,x2,x3, output logic [15:0] code);
 logic [1:0] y[0:7];
 function automatic [1:0] m3(input integer v); integer t; begin t=v%3; if(t<0)t=t+3; m3=t[1:0]; end endfunction
 function automatic nz(input [1:0] v,input integer b); begin nz=(m3(v+b)!=0); end endfunction
 always_comb begin
  y[0]=m3(x0+2*x1+x2+2*x3); y[1]=m3(x0+x1+x2+2*x3);
  y[2]=m3(x1+2*x3); y[3]=m3(x0+2*x1+x2); y[4]=m3(x0);
  y[5]=m3(x2+x3); y[6]=m3(x0+x3); y[7]=m3(x2+2*x3);
  code='0;
  code[0]=nz(y[0],0); code[1]=nz(y[0],1);
  code[2]=nz(y[1],2); code[3]=nz(y[1],1);
  code[4]=nz(y[2],1); code[5]=nz(y[2],0);
  code[6]=nz(y[3],1); code[7]=nz(y[3],2);
  code[8]=nz(y[4],2); code[9]=nz(y[4],1);
  code[10]=nz(y[5],0); code[11]=nz(y[5],1);
  code[12]=nz(y[6],1); code[13]=nz(y[6],2);
  code[14]=nz(y[7],0); code[15]=nz(y[7],2);
 end
endmodule

module w33_pass2938_isodual_support_decoder(
 input logic [15:0] received, output logic valid,corrected,
 output logic [1:0] x0,x1,x2,x3);
 logic [1:0] y[0:7],trial[0:7];
 logic [1:0] s0,s1,s2,s3,emag;
 integer i,erasures,epos,candidate,zeros,errpos;
 logic hit;
 function automatic [1:0] m3(input integer v); integer t; begin t=v%3; if(t<0)t=t+3; m3=t[1:0]; end endfunction
 function automatic [1:0] decode_pair(input integer p,input logic a,b);
  logic [1:0] pair; begin pair={b,a};
   if(pair==0) decode_pair=3;
   else case(p)
    0,5: case(pair) 2'b10:decode_pair=0;2'b11:decode_pair=1;default:decode_pair=2;endcase
    1,4: case(pair) 2'b11:decode_pair=0;2'b10:decode_pair=1;default:decode_pair=2;endcase
    2: case(pair) 2'b01:decode_pair=0;2'b11:decode_pair=1;default:decode_pair=2;endcase
    3,6: case(pair) 2'b11:decode_pair=0;2'b01:decode_pair=1;default:decode_pair=2;endcase
    7: case(pair) 2'b10:decode_pair=0;2'b01:decode_pair=1;default:decode_pair=2;endcase
    default:decode_pair=3;
   endcase
  end
 endfunction
 task automatic syn(input logic [1:0] w[0:7],output logic [1:0] a,b,c,d); begin
  a=m3(w[0]+w[1]+w[2]+w[3]);
  b=m3(2*w[0]+2*w[2]+w[4]+w[5]);
  c=m3(2*w[0]+w[1]+w[2]+2*w[4]+w[6]);
  d=m3(w[0]+w[1]+w[4]+w[7]);
 end endtask
 always_comb begin
  valid=0;corrected=0;x0=0;x1=0;x2=0;x3=0;erasures=0;epos=-1;
  for(i=0;i<8;i=i+1) begin
   y[i]=decode_pair(i,received[2*i],received[2*i+1]);
   if(y[i]==3) begin erasures=erasures+1;epos=i;y[i]=0;end
  end
  if(erasures==1) begin
   zeros=0;
   for(candidate=0;candidate<3;candidate=candidate+1) begin
    for(i=0;i<8;i=i+1) trial[i]=y[i]; trial[epos]=candidate[1:0]; syn(trial,s0,s1,s2,s3);
    if({s0,s1,s2,s3}==0) begin zeros=zeros+1;for(i=0;i<8;i=i+1)y[i]=trial[i];end
   end
   if(zeros==1) begin valid=1;corrected=1;end
  end else if(erasures==0) begin
   syn(y,s0,s1,s2,s3);
   if({s0,s1,s2,s3}==0) valid=1;
   else begin hit=1;errpos=-1;emag=0;
    case({s0,s1,s2,s3})
     8'b01_10_10_01:begin errpos=0;emag=1;end 8'b10_01_01_10:begin errpos=0;emag=2;end
     8'b01_00_01_01:begin errpos=1;emag=1;end 8'b10_00_10_10:begin errpos=1;emag=2;end
     8'b01_10_01_00:begin errpos=2;emag=1;end 8'b10_01_10_00:begin errpos=2;emag=2;end
     8'b01_00_00_00:begin errpos=3;emag=1;end 8'b10_00_00_00:begin errpos=3;emag=2;end
     8'b00_01_10_01:begin errpos=4;emag=1;end 8'b00_10_01_10:begin errpos=4;emag=2;end
     8'b00_01_00_00:begin errpos=5;emag=1;end 8'b00_10_00_00:begin errpos=5;emag=2;end
     8'b00_00_01_00:begin errpos=6;emag=1;end 8'b00_00_10_00:begin errpos=6;emag=2;end
     8'b00_00_00_01:begin errpos=7;emag=1;end 8'b00_00_00_10:begin errpos=7;emag=2;end
     default:hit=0;
    endcase
    if(hit) begin y[errpos]=m3(y[errpos]-emag);syn(y,s0,s1,s2,s3);if({s0,s1,s2,s3}==0)begin valid=1;corrected=1;end end
   end
  end
  if(valid) begin x0=m3(y[4]);x1=m3(y[0]+2*y[1]);x2=m3(y[1]+2*y[2]+2*y[4]);x3=m3(y[0]+2*y[1]+2*y[2]);end
 end
endmodule
