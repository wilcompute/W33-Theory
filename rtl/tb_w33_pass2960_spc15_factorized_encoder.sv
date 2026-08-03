`timescale 1ns/1ps
module tb_w33_pass2960_spc15_factorized_encoder;
logic [1:0] x0,x1,x2,x3;logic [14:0] y;logic [14:0] codes[0:80];integer a,b,c,d,i,j,k,dist,idx;
w33_pass2960_spc15_factorized_encoder dut(.x0(x0),.x1(x1),.x2(x2),.x3(x3),.support_bits(y));
initial begin idx=0;
 for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(d=0;d<3;d=d+1)begin x0=a;x1=b;x2=c;x3=d;#1;codes[idx]=y;
  if((y[0]+y[1]+y[2])!=2||(y[3]+y[4]+y[5])!=2||(y[6]+y[7]+y[8])!=2||(y[9]+y[10]+y[11])!=2||(y[12]+y[13]+y[14])!=2)$fatal(1,"triplet");idx=idx+1;end
 for(i=0;i<81;i=i+1)for(j=i+1;j<81;j=j+1)begin dist=0;for(k=0;k<15;k=k+1)dist=dist+(codes[i][k]^codes[j][k]);if(dist<4)$fatal(1,"distance %0d %0d %0d",i,j,dist);end
 $display("PASS 81 codewords dmin>=4");$finish;end
endmodule
