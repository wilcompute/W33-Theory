`timescale 1ns/1ps
module tb_w33_pass2966_antisymplectic_phase_transducer;
logic [1:0] x0,x1,x2,x3,p0,p1,p2,p3,sigma,kx0,kx1,kx2,kx3,kp0,kp1,kp2,kp3;logic commute;logic [2:0] sup;integer a,b,c,d,e,f,g,h,raw,expected_sigma,count;
w33_pass2966_antisymplectic_phase_transducer dut(.x0(x0),.x1(x1),.x2(x2),.x3(x3),.p0(p0),.p1(p1),.p2(p2),.p3(p3),.sigma(sigma),.commute(commute),.support_triplet(sup),.kx0(kx0),.kx1(kx1),.kx2(kx2),.kx3(kx3),.kp0(kp0),.kp1(kp1),.kp2(kp2),.kp3(kp3));
initial begin count=0;
 for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(d=0;d<3;d=d+1)
 for(e=0;e<3;e=e+1)for(f=0;f<3;f=f+1)for(g=0;g<3;g=g+1)for(h=0;h<3;h=h+1)begin
  x0=a;x1=b;x2=c;x3=d;p0=e;p1=f;p2=g;p3=h;#1;raw=a*f-b*e+c*h-d*g;expected_sigma=((raw%3)+3)%3;if(sigma!==expected_sigma[1:0])$fatal(1,"sigma");if(commute!==(expected_sigma==0))$fatal(1,"commute");if((sup[0]+sup[1]+sup[2])!=2)$fatal(1,"support");if(kx0!==b||kx1!==a||kx2!==d||kx3!==c||kp0!==f||kp1!==e||kp2!==h||kp3!==g)$fatal(1,"K");count=count+1;end
 $display("PASS %0d symplectic transducer states",count);$finish;end
endmodule
