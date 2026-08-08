`timescale 1ns/1ps
module tb;
  reg clk=0, rst=1; reg [1:0] op=0; wire [7:0] frame;
  w33_isa4 dut(.clk(clk), .rst(rst), .op(op), .frame(frame));
  integer k;
  always #5 clk = ~clk;
  initial begin
    @(negedge clk); rst=0;
    for (k=0; k<4; k=k+1) begin
      op = k[1:0]; @(negedge clk);
      $display("op=%0d frame=%0d %0d %0d %0d", k, frame[1:0], frame[3:2], frame[5:4], frame[7:6]);
    end
    $finish;
  end
endmodule
