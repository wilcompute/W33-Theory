`timescale 1ns/1ps
module tb_w33_pass2757_qutrit_cx;
 reg [1:0] p,f,xp,zp,xf,zf,yp,yzp,yf,yzf;
 wire [1:0] po,fo,x1,z1,y1,w1,x3,z3,y3,w3,u1,v1,s1,t1;
 integer a,b,c,d,e,g,h,k,before_form,after_form;
 w33_qutrit_cx_data du(p,f,po,fo);
 w33_qutrit_cx_frame_map mu(xp,zp,xf,zf,x1,z1,y1,w1);
 w33_qutrit_cx_order3 ou(xp,zp,xf,zf,x3,z3,y3,w3);
 w33_qutrit_cx_frame_map mv(yp,yzp,yf,yzf,u1,v1,s1,t1);
 function integer mod3(input integer q); begin mod3=q%3;if(mod3<0)mod3=mod3+3;end endfunction
 function integer symp(input integer ax,input integer az,input integer bx,input integer bz,input integer cx,input integer cz,input integer dx,input integer dz);
  begin symp=mod3(ax*cz-az*cx+bx*dz-bz*dx); end
 endfunction
 initial begin
  for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)begin
   p=a;f=b;#1;
   if(po!==a[1:0]||fo!==((a+b)%3))$fatal(1,"data");
  end
  for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(d=0;d<3;d=d+1)begin
   xp=a;zp=b;xf=c;zf=d;#1;
   if(x1!==a[1:0]||z1!==mod3(b-d)||y1!==mod3(c+a)||w1!==d[1:0])$fatal(1,"frame");
   if(x3!==a[1:0]||z3!==b[1:0]||y3!==c[1:0]||w3!==d[1:0])$fatal(1,"order3");
  end
  for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(d=0;d<3;d=d+1)
  for(e=0;e<3;e=e+1)for(g=0;g<3;g=g+1)for(h=0;h<3;h=h+1)for(k=0;k<3;k=k+1)begin
   xp=a;zp=b;xf=c;zf=d;yp=e;yzp=g;yf=h;yzf=k;#1;
   before_form=symp(a,b,c,d,e,g,h,k);after_form=symp(x1,z1,y1,w1,u1,v1,s1,t1);
   if(before_form!=after_form)$fatal(1,"symplectic");
  end
  $display("PASS: 9 basis states, 81 frames, order 3, and 81^2 symplectic pairs");$finish;
 end
endmodule
