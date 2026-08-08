`timescale 1ns/1ps
module tb2;
  reg clk=0, rst=1; reg [1:0] op=0; wire [7:0] frame;
  w33_isa4 dut(.clk(clk), .rst(rst), .op(op), .frame(frame));
  reg [1:0] seq [0:39];
  integer k;
  always #5 clk = ~clk;
  initial begin
    $readmemb("seq.txt", seq);
    @(negedge clk); rst=0;
    for (k=0; k<40; k=k+1) begin op = seq[k]; @(negedge clk); end
    $display("VERILOG final frame: (%0d, %0d, %0d, %0d)", frame[1:0], frame[3:2], frame[5:4], frame[7:6]);
    $finish;
  end
endmodule
