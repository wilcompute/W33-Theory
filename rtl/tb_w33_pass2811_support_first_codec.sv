module tb_w33_pass2811_support_first_codec;
  logic [1:0] x0,x1,x2,x3,y0,y1,y2,y3;
  logic [6:0] code;
  logic [5:0] addr;
  logic [3:0] mask;
  logic [2:0] phase;
  logic polarity,is_zero;
  integer a,b,c,d,count;
  w33_pass2811_support_first_codec enc(.*);
  w33_pass2811_support_first_decoder dec(.affine_code(code),.x0(y0),.x1(y1),.x2(y2),.x3(y3));
  initial begin
    count=0;
    for(a=0;a<3;a=a+1) for(b=0;b<3;b=b+1)
      for(c=0;c<3;c=c+1) for(d=0;d<3;d=d+1) begin
        x0=a; x1=b; x2=c; x3=d; #1;
        if ({y3,y2,y1,y0} !== {x3,x2,x1,x0}) $fatal(1,"roundtrip failed");
        count=count+1;
      end
    if(count!=81) $fatal(1,"wrong census");
    $display("PASS 81/81");
    $finish;
  end
endmodule
