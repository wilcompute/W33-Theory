`timescale 1ns/1ps
module tb_w33_pass3388_3399_fault_codes;
  reg [4:0] state5; wire [11:0] code12; wire valid12e;
  reg [11:0] rx12; wire [4:0] dec12; wire valid12d,corrected12; wire [3:0] dist12;
  wire [12:0] code13; reg [12:0] rx13; wire [4:0] dec13; wire valid13d,corrected13; wire [3:0] dist13;
  reg [3:0] state4,failed_state; reg op; wire [3:0] next_dyn; wire [4:0] pc,pt,h1,h2; wire [2:0] rlen;
  reg [3:0] bad_layers; wire [3:0] next_q6; wire [5:0] pc6,pt6; wire [1:0] layer6; wire valid6; wire [2:0] rlen6;
  integer s,i,j,cases12,cases13,casesdyn,casesq6,total,maxd;
  reg [11:0] err12; reg [12:0] err13;

  w33_envelope_nonlinear12_encode e12(.state(state5),.codeword(code12),.valid(valid12e));
  w33_envelope_nonlinear12_decode d12(.received(rx12),.state(dec12),.valid(valid12d),.corrected(corrected12),.distance(dist12));
  w33_linear13_encode e13(.state(state5),.codeword(code13));
  w33_linear13_decode d13(.received(rx13),.state(dec13),.valid(valid13d),.corrected(corrected13),.distance(dist13));
  w33_q5_dynamic_spare_router dr(.state(state4),.op(op),.failed_state(failed_state),.next_state(next_dyn),
    .physical_current(pc),.physical_target(pt),.hop1(h1),.hop2(h2),.route_length(rlen));
  w33_q6_triple_fault_router qr(.state(state4),.op(op),.bad_layers(bad_layers),.next_state(next_q6),
    .physical_current(pc6),.physical_target(pt6),.selected_layer(layer6),.valid_layer(valid6),.route_length(rlen6));

  function is_env; input [4:0] x; begin
    case(x)
      0,1,2,3,4,5,6,8,10,11,12,13,16,17,19,20,22,24,25,26,29,30:is_env=1'b1;
      default:is_env=1'b0;
    endcase
  end endfunction
  function [3:0] qmap; input [3:0] x; begin case(x)
    0:qmap=13;1:qmap=9;2:qmap=0;3:qmap=2;4:qmap=8;5:qmap=12;6:qmap=4;7:qmap=6;
    8:qmap=1;9:qmap=3;10:qmap=11;11:qmap=15;12:qmap=7;13:qmap=5;14:qmap=14;default:qmap=10;
  endcase end endfunction

  task check12; input [11:0] e; input [4:0] expected; begin
    rx12=code12^e; #1;
    if(!valid12d || dec12!==expected) begin $display("FAIL nonlinear12 state=%0d err=%h dec=%0d valid=%b d=%0d",expected,e,dec12,valid12d,dist12);$fatal;end
    cases12=cases12+1;
  end endtask
  task check13; input [12:0] e; input [4:0] expected; begin
    rx13=code13^e; #1;
    if(!valid13d || dec13!==expected) begin $display("FAIL linear13 state=%0d err=%h dec=%0d valid=%b d=%0d",expected,e,dec13,valid13d,dist13);$fatal;end
    cases13=cases13+1;
  end endtask

  initial begin
    cases12=0;cases13=0;casesdyn=0;casesq6=0;
    for(s=0;s<32;s=s+1) begin
      state5=s[4:0]; #1;
      if(valid12e!==is_env(state5)) begin $display("FAIL envelope valid state=%0d",s);$fatal;end
      if(is_env(state5)) begin
        check12(12'd0,state5);
        for(i=0;i<12;i=i+1) check12(12'd1<<i,state5);
        for(i=0;i<12;i=i+1) for(j=i+1;j<12;j=j+1) check12((12'd1<<i)|(12'd1<<j),state5);
      end
      check13(13'd0,state5);
      for(i=0;i<13;i=i+1) check13(13'd1<<i,state5);
      for(i=0;i<13;i=i+1) for(j=i+1;j<13;j=j+1) check13((13'd1<<i)|(13'd1<<j),state5);
    end
    if(cases12!=1738 || cases13!=2944) begin $display("FAIL code case counts %0d %0d",cases12,cases13);$fatal;end

    for(s=0;s<16;s=s+1) begin
      failed_state=s[3:0];total=0;maxd=0;
      for(op=0;op<2;op=op+1) begin
        for(i=0;i<16;i=i+1) begin
          state4=i[3:0];#1;
          if(pc=={1'b0,qmap(failed_state)} || pt=={1'b0,qmap(failed_state)}) begin $display("FAIL uses failed slot f=%0d s=%0d",s,i);$fatal;end
          if(rlen>2) begin $display("FAIL dynamic dilation f=%0d s=%0d op=%0d d=%0d",s,i,op,rlen);$fatal;end
          total=total+rlen;if(rlen>maxd)maxd=rlen;casesdyn=casesdyn+1;
        end
      end
      if(total!=34 || maxd!=2) begin $display("FAIL dynamic metrics f=%0d total=%0d max=%0d",s,total,maxd);$fatal;end
    end

    for(s=0;s<15;s=s+1) begin
      bad_layers=s[3:0];total=0;maxd=0;
      for(op=0;op<2;op=op+1) begin
        for(i=0;i<16;i=i+1) begin state4=i[3:0];#1;
          if(!valid6 || bad_layers[layer6]) begin $display("FAIL q6 layer mask=%h sel=%0d",bad_layers,layer6);$fatal;end
          if(rlen6>2) begin $display("FAIL q6 dilation");$fatal;end
          total=total+rlen6;if(rlen6>maxd)maxd=rlen6;casesq6=casesq6+1;
        end
      end
      if(total!=34 || maxd!=2) begin $display("FAIL q6 metrics mask=%h total=%0d max=%0d",bad_layers,total,maxd);$fatal;end
    end
    bad_layers=4'hf;state4=0;op=0;#1;if(valid6)begin $display("FAIL q6 fail closed");$fatal;end
    if(casesdyn!=512 || casesq6!=480)begin $display("FAIL route counts %0d %0d",casesdyn,casesq6);$fatal;end
    $display("PASS self-protecting cases=4682 dynamic_routes=512 q6_routes=480");
    $finish;
  end
endmodule
