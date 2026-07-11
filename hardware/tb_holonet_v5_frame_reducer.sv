`timescale 1ns/1ps
module tb_holonet_v5_frame_reducer;
  logic clk=0, rst_n=0, iv=0, ir, ov, ordy=1, overflow;
  logic [63:0] ts=0, fts, lts;
  logic [4:0] ch=0;
  logic [31:0] fid;
  logic [23:0] c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15;
  holonet_v5_frame_reducer dut(clk,rst_n,iv,ir,ts,ch,ov,ordy,fid,fts,lts,overflow,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15);
  always #5 clk=~clk;
  task send(input [63:0] t, input [4:0] c);
    begin @(negedge clk); while(!ir) @(negedge clk); ts=t; ch=c; iv=1; @(negedge clk); iv=0; end
  endtask
  initial begin
    repeat(2) @(negedge clk); rst_n=1;
    send(64'd100,5'd0); send(64'd110,5'd0); send(64'd120,5'd3); send(64'd200,5'd16);
    @(posedge clk); #1;
    if (!ov || c0!==0 || c3!==0 || fts!==100 || lts!==200 || fid!==1) $fatal(1,"bad frame output");
    @(posedge clk); #1; $display("PASS"); $finish;
  end
endmodule
