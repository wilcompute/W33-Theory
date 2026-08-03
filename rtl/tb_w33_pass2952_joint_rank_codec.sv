`timescale 1ns/1ps
module tb_w33_pass2952_joint_rank_codec;
 logic [6:0] frame,frame2;logic [3:0] line,line2;logic [1:0] slot,slot2;logic [11:0] rank;logic v1,v2;integer f,l,s;
 w33_pass2952_joint_rank_encode e(.frame_rank(frame),.oam_line(line),.slot(slot),.valid(v1),.joint_rank(rank));
 w33_pass2952_joint_rank_decode d(.joint_rank(rank),.valid(v2),.frame_rank(frame2),.oam_line(line2),.slot(slot2));
 initial begin
  for(f=0;f<81;f=f+1)for(l=0;l<10;l=l+1)for(s=0;s<4;s=s+1)begin frame=f;line=l;slot=s;#1;if(!v1||!v2||frame2!==frame||line2!==line||slot2!==slot)$fatal(1,"roundtrip %0d %0d %0d",f,l,s);end
  frame=81;line=0;slot=0;#1;if(v1)$fatal(1,"invalid frame");
  frame=0;line=10;#1;if(v1)$fatal(1,"invalid line");
  $display("PASS 3240/3240 joint rank states");$finish;
 end
endmodule
