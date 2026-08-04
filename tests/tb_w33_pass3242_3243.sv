`timescale 1ns/1ps
module tb_w33_pass3242_3243;
  localparam W=12;
  reg signed [W-1:0] x0,x1,y0,y1;
  reg step,reflect;
  wire signed [W-1:0] nx0,nx1,ny0,ny1;
  reg [2:0] selector;
  reg [3:0] state_in;
  wire [3:0] state_out;
  wire valid;
  integer errors=0;
  reg signed [W-1:0] ax0,ax1,ay0,ay1;
  reg signed [W-1:0] bx0,bx1,by0,by1;

  w33_pass3242_real_spiral_controller #(.W(W)) dutR(
    .x0(x0),.x1(x1),.y0(y0),.y1(y1),.step(step),.reflect(reflect),
    .nx0(nx0),.nx1(nx1),.ny0(ny0),.ny1(ny1));
  w33_pass3243_s3_matching dutS(.selector(selector),.state_in(state_in),.state_out(state_out),.valid(valid));

  task check_s3;
    input [2:0] sel;
    input [3:0] vin;
    input [3:0] expected;
    begin
      selector=sel; state_in=vin; #1;
      if (!valid || state_out!==expected) begin
        $display("S3 fail sel=%0d in=%b got=%b exp=%b",sel,vin,state_out,expected);
        errors=errors+1;
      end
    end
  endtask

  task apply_step;
    begin
      step=1;reflect=0;#1;
      ax0=nx0;ax1=nx1;ay0=ny0;ay1=ny1;
      x0=ax0;x1=ax1;y0=ay0;y1=ay1;#1;
    end
  endtask
  task apply_reflect;
    begin
      step=0;reflect=1;#1;
      ax0=nx0;ax1=nx1;ay0=ny0;ay1=ny1;
      x0=ax0;x1=ax1;y0=ay0;y1=ay1;#1;
    end
  endtask

  initial begin
    x0=3;x1=-2;y0=5;y1=1; step=1;reflect=0;#1;
    if (nx0!==-3 || nx1!==3 || ny0!==2 || ny1!==5) errors=errors+1;

    step=0;reflect=1;#1;
    ax0=nx0;ax1=nx1;ay0=ny0;ay1=ny1;
    x0=ax0;x1=ax1;y0=ay0;y1=ay1;#1;
    ax0=nx0;ax1=nx1;ay0=ny0;ay1=ny1;
    if (ax0!==3 || ax1!==-2 || ay0!==5 || ay1!==1) errors=errors+1;

    x0=2;x1=1;y0=-1;y1=3;
    bx0=x0;bx1=x1;by0=y0;by1=y1;
    apply_step(); apply_reflect(); apply_step(); apply_reflect();
    if (x0!==bx0 || x1!==bx1 || y0!==by0 || y1!==by1) begin
      $display("reverser relation failed"); errors=errors+1;
    end

    check_s3(0,4'b1100,4'b1100); check_s3(0,4'b1011,4'b1011); check_s3(0,4'b0111,4'b0111);
    check_s3(1,4'b1100,4'b1011); check_s3(1,4'b1011,4'b0111); check_s3(1,4'b0111,4'b1100);
    check_s3(2,4'b1100,4'b0111); check_s3(2,4'b1011,4'b1100); check_s3(2,4'b0111,4'b1011);
    check_s3(3,4'b1100,4'b1100); check_s3(3,4'b1011,4'b0111); check_s3(3,4'b0111,4'b1011);
    check_s3(4,4'b1100,4'b0111); check_s3(4,4'b1011,4'b1011); check_s3(4,4'b0111,4'b1100);
    check_s3(5,4'b1100,4'b1011); check_s3(5,4'b1011,4'b1100); check_s3(5,4'b0111,4'b0111);
    selector=7;state_in=4'hf;#1;if(valid || state_out!==0) errors=errors+1;

    if(errors==0) $display("PASS SPIRAL/S3");
    else $display("FAIL errors=%0d",errors);
    $finish;
  end
endmodule
