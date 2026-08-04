`timescale 1ns/1ps
module tb_w33_pass3163_3172_proof_runtime;
  logic clk=0,rst=1;always #5 clk=~clk;
  // tri decoder
  logic [7:0] frame_i,frame_o;logic [1:0] mode;logic [2:0] opcode;logic dvalid;
  w33_pass3164_tri_isa_decoder dec(.frame_i,.mode_i(mode),.opcode_i(opcode),.frame_o,.valid_o(dvalid));
  // epoch
  logic symv;logic [4:0] sym;logic marker,pvalid,amb;logic [3:0] phase;logic [15:0] epochs;
  w33_pass3168_phase_epoch_decoder ep(.clk,.rst,.symbol_valid_i(symv),.symbol_i(sym),
    .marker_seen_o(marker),.phase_valid_o(pvalid),.phase_o(phase),.ambiguous_o(amb),.epoch_count_o(epochs));
  // curvature
  logic [2:0] ll,rr;logic cvalid,curved;
  w33_pass3171_d4_curvature curv(.left_label_i(ll),.right_label_i(rr),.valid_o(cvalid),.curvature_o(curved));
  // scheduler
  logic [15:0] price;logic fastcal,lowcal,area;logic [1:0] smode;logic sw;
  w33_pass3172_information_tri_isa_scheduler sch(.clk,.rst,.effective_collision_price_q8_8_i(price),
    .fast6_calibrated_i(fastcal),.low4_calibrated_i(lowcal),.fast6_area_available_i(area),.mode_o(smode),.switch_o(sw));
  // enumerator
  logic estart,eadv,evalid,edone,u1v,u2v,cv;logic [15:0] hi;logic [8:0]u1,u2;logic [11:0]ci;
  logic [5:0]e1,e2;logic [2:0]l1,l2;
  w33_pass3169_hypothesis_enumerator en(.clk,.rst,.start_i(estart),.advance_i(eadv),.valid_o(evalid),.done_o(edone),
    .hypothesis_index_o(hi),.unary1_valid_o(u1v),.unary1_index_o(u1),.unary2_valid_o(u2v),.unary2_index_o(u2),
    .correction_valid_o(cv),.correction_index_o(ci),.edge1_o(e1),.label1_o(l1),.edge2_o(e2),.label2_o(l2));
  integer i,j,total,corr;
  task tick;begin @(negedge clk);@(posedge clk);#1;end endtask
  task send(input [4:0]x);begin @(negedge clk);sym=x;symv=1;@(posedge clk);#1;symv=0;end endtask
  initial begin
    frame_i=0;mode=0;opcode=0;symv=0;sym=0;ll=0;rr=0;price=0;fastcal=0;lowcal=1;area=0;estart=0;eadv=0;
    repeat(2)tick();rst=0;
    // Exact translations in each ISA.
    frame_i={2'd0,2'd1,2'd2,2'd1};mode=0;opcode=3;#1;
    if(!dvalid||frame_o[3:2]!==2'd0)$fatal(1,"current Z1 mapping");
    mode=1;opcode=3;#1;if(frame_o[1:0]!==2'd2)$fatal(1,"low Z0 mapping");
    mode=2;opcode=5;#1;if(frame_o[7:6]!==2'd1)$fatal(1,"fast Z3 mapping");
    // Curvature census: 24 of 49 ordered nonidentity pairs.
    corr=0;for(i=0;i<7;i=i+1)for(j=0;j<7;j=j+1)begin ll=i;rr=j;#1;if(!cvalid)$fatal(1,"curv valid");if(curved)corr=corr+1;end
    if(corr!=24)$fatal(1,"curvature count %0d",corr);
    // Phase 4 marker (symbol 6) with two substitutions.
    send(6);send(7);send(6);send(2);send(6);tick();
    if(phase!==4||epochs!==1||amb)$fatal(1,"phase-coded marker substitution case");
    // Phase 1 marker with two deletions: received 3,3,3.
    send(3);send(3);send(3);tick();
    if(phase!==1||epochs!==2||amb)$fatal(1,"phase-coded marker deletion case");
    // Tri scheduler: fast6 dominates at low cost when physically available.
    fastcal=1;area=1;price=16'd256;tick();if(smode!==2)$fatal(1,"fast6 selection");
    price=16'd5000;tick();if(smode!==1)$fatal(1,"low4 high-price selection");
    fastcal=0;area=0;price=0;tick();if(smode!==0)$fatal(1,"current fail-closed selection");
    // Exhaust exact hypothesis enumeration and count shared-pair corrections.
    estart=1;tick();estart=0;total=0;corr=0;
    while(!edone)begin
      if(evalid)begin total=total+1;if(cv)corr=corr+1;eadv=1;end else eadv=0;
      tick();
    end
    eadv=0;
    if(total!=48826)$fatal(1,"hypothesis count %0d",total);
    if(corr!=3381)$fatal(1,"correction count %0d",corr);
    $display("PASS tri-ISA, phase-coded epoch, D4 curvature and 48,826 enumerator");$finish;
  end
endmodule
