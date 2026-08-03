module tb_w33_pass2856_codec_benchmark_top;
  logic clk=0, load=0;
  logic [7:0] frame_in;
  logic [7:0] frame_out;
  logic [6:0] code_out;
  integer n, a;
  logic [1:0] x0,x1,x2,x3;
  always #5 clk=~clk;
  w33_pass2856_codec_benchmark_top dut(.*);
  initial begin
    frame_in=0;
    repeat(2) @(posedge clk);
    for(n=0;n<81;n=n+1) begin
      a=n;
      x0=a%3; a=a/3;
      x1=a%3; a=a/3;
      x2=a%3; a=a/3;
      x3=a%3;
      frame_in={x3,x2,x1,x0};
      load=1;
      @(posedge clk); #1;
      load=0;
      if(frame_out !== frame_in) $fatal(1,"roundtrip mismatch n=%0d in=%h out=%h",n,frame_in,frame_out);
    end
    $display("PASS 81/81 registered codec round trips");
    $finish;
  end
endmodule
