`timescale 1ns/1ps
module tb_w33_pass3175_3183_curvature_routed_runtime;
 logic clk=0,rst=1,valid;logic [1:0] cls;logic [15:0] weight;logic [31:0] n,f,c;
 logic eval;logic [3:0] rlen;logic [47:0] counts;logic lock,amb;logic [3:0] phase;
 logic digest,prov,cert,wit,acc,auth;logic [2:0] a,b,x;logic flux;
 logic first,last,available;logic [4:0] action;logic [1:0] mode;logic signed [31:0] util,best;logic done;logic [4:0] ba;logic [1:0] bm;
 always #5 clk=~clk;
 w33_pass3175_curvature_accumulator ca(clk,rst,valid,cls,weight,n,f,c);
 w33_pass3178_three_edit_epoch_decoder ep(eval,rlen,counts,lock,amb,phase);
 w33_pass3179_m36_envelope_gate eg(digest,prov,cert,wit,acc,auth);
 w33_pass3181_d4_triangle_flux wf(a,b,x,flux);
 w33_pass3180_streamed_routed_utility ru(clk,rst,first,valid,last,available,action,mode,util,done,ba,bm,best);
 task tick;begin @(negedge clk);@(posedge clk);#1;end endtask
 initial begin
  valid=0;cls=0;weight=0;eval=0;rlen=0;counts=0;digest=0;prov=0;cert=0;wit=0;acc=0;
  a=0;b=0;x=0;first=0;last=0;available=0;action=0;mode=0;util=0;
  repeat(2)tick();rst=0;
  cls=0;weight=10;valid=1;tick();cls=1;weight=7;tick();cls=2;weight=5;tick();valid=0;
  if(n!=10||f!=7||c!=5)$fatal(1,"curvature accumulators");
  rlen=7;counts=0;counts[4*5 +:4]=4'd4;eval=1;#1;
  if(!lock||amb||phase!=5)$fatal(1,"three-edit epoch");
  digest=1;prov=1;cert=1;wit=1;acc=0;#1;if(auth)$fatal(1,"rejected envelope authorized");acc=1;#1;if(!auth)$fatal(1,"accepted envelope blocked");
  // reflections r^0s,r^1s,r^2s give two curved edges and zero triangle flux.
  a=3'b100;b=3'b101;x=3'b110;#1;if(flux!==0)$fatal(1,"D4 flux mismatch");
  first=1;valid=1;available=1;action=1;mode=0;util=100;tick();first=0;action=2;mode=2;util=130;tick();action=3;mode=1;util=120;last=1;tick();valid=0;last=0;
  if(!done||ba!=2||bm!=2||best!=130)$fatal(1,"utility argmax");
  $display("PASS curvature, three-edit epoch, envelope, Wilson flux and routed utility");$finish;
 end
endmodule
