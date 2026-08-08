`timescale 1ns/1ps
module tb_w33_machine_b;
  reg clk=0, rst=1; reg [2:0] op=0; wire [7:0] frame;
  w33_machine_b dut(.clk(clk), .rst(rst), .op(op), .frame(frame));
  reg [2:0] seq [0:49];
  integer k;
  always #5 clk = ~clk;
  initial begin
    $readmemb("w33_machine_b_seq.txt", seq);
    @(negedge clk); rst=0;
    for (k=0; k<50; k=k+1) begin op = seq[k]; @(negedge clk); end
    $display("FRAME (%0d, %0d, %0d, %0d)",
             frame[1:0], frame[3:2], frame[5:4], frame[7:6]);
    $finish;
  end
endmodule
