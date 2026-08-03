`timescale 1ns/1ps
module w33_cubic_tb;
  reg [17:0] x; wire [1:0] d;
  integer i,r,c,errs,n; reg [1:0] m[0:8]; integer det;
  w33_e6_cubic dut (.x_flat(x), .det(d));
  initial begin
    errs=0; n=0;
    for (i=0;i<19683;i=i+1) begin
      begin : mk
        integer t,v; t=i;
        for (v=0;v<9;v=v+1) begin m[v]=t%3; t=t/3; end
      end
      x = {m[8],m[7],m[6],m[5],m[4],m[3],m[2],m[1],m[0]};
      #1;
      det = m[0]*m[4]*m[8] + m[1]*m[5]*m[6] + m[2]*m[3]*m[7]
          - m[2]*m[4]*m[6] - m[0]*m[5]*m[7] - m[1]*m[3]*m[8];
      det = ((det % 3) + 3) % 3;
      n=n+1;
      if (d !== det[1:0]) begin
        errs=errs+1;
        if (errs<4) $display("FAIL i=%0d got %0d want %0d", i, d, det);
      end
    end
    $display("Pass 2632 E6 cubic: %0d matrices checked, %0d errors", n, errs);
    if (errs==0) $display("PASS  det over F3 correct on ALL 3^9 inputs");
    $finish;
  end
endmodule
