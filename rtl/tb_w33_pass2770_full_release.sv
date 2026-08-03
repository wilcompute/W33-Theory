`timescale 1ns/1ps
module tb_w33_pass2770_full_release;
  logic clk=0, rst=1, start=0, operand=0, magic_ack=0;
  logic [2:0] opcode=0, d12_a_in=0, d12_c_in=0;
  logic d12_b_in=0, d12_d_in=0;
  logic [1:0] p_in=0,f_in=0,xp_in=0,zp_in=0,xf_in=0,zf_in=0;
  logic [5:0] magic_id=0;
  logic busy,done,error,magic_req,magic_valid;
  logic [1:0] p_out,f_out,xp_out,zp_out,xf_out,zf_out,magic_dark_mode,magic_grade;
  logic [2:0] d12_a_out,magic_phase6_0,magic_phase6_1,magic_phase6_2,magic_phase6_3;
  logic d12_b_out;
  logic rstart=0, rlink=0;
  logic [1:0] rm=0,rn=0,rx=0,rz=0;
  logic rbusy,rdone,rerasure,rneg;
  logic [2:0] raction;

  w33_pass2770_holonet_top dut(.*);
  w33_pass2771_remote_sum_link remote(
    .clk(clk),.rst(rst),.start(rstart),.link_valid(rlink),.meas_m(rm),.meas_n(rn),
    .busy(rbusy),.done(rdone),.erasure(rerasure),.action(raction),
    .x_correction_b(rx),.negate_b(rneg),.z_frame_a(rz)
  );
  always #5 clk=~clk;

  function automatic [1:0] add3(input [1:0] a,b);
    integer s; begin s=a+b; add3=(s>=3)?s-3:s; end
  endfunction
  function automatic [1:0] neg3(input [1:0] a);
    case(a) 0:neg3=0;1:neg3=2;default:neg3=1;endcase
  endfunction
  function automatic [2:0] add6(input [2:0] a,b);
    integer s; begin s=a+b; add6=(s>=6)?s-6:s; end
  endfunction
  function automatic [2:0] neg6(input [2:0] a);
    neg6=(a==0)?0:6-a;
  endfunction

  task automatic pulse;
    begin start=1; @(posedge clk); #1; start=0; end
  endtask
  // `expect` is a SystemVerilog assertion keyword.  Naming a task `expect` parsed in
  // some older simulators but fails in Icarus 12, so keep the contract task unambiguous.
  task automatic check_ok(input logic cond, input integer code);
    begin if(!cond) begin $display("FAIL code=%0d",code); $fatal(1); end end
  endtask
  task automatic expected_magic(input [5:0] id,
    output [1:0] edark,egrade, output [2:0] ep0,ep1,ep2,ep3);
    begin edark=0;egrade=0;ep0=0;ep1=0;ep2=0;ep3=0; case(id)
      6'd0: begin edark=0;egrade=2;ep2=3;end 6'd1:begin edark=0;egrade=1;ep2=3;ep3=2;end
      6'd2:begin edark=0;egrade=1;ep2=3;ep3=4;end 6'd3:begin edark=0;egrade=1;ep2=5;end
      6'd4:begin edark=0;egrade=1;ep2=5;ep3=2;end 6'd5:begin edark=0;egrade=0;ep2=5;ep3=4;end
      6'd6:begin edark=0;egrade=1;ep2=1;end 6'd7:begin edark=0;egrade=0;ep2=1;ep3=2;end
      6'd8:begin edark=0;egrade=1;ep2=1;ep3=4;end 6'd9:begin edark=1;egrade=2;ep2=3;ep3=3;end
      6'd10:begin edark=1;egrade=1;ep2=3;ep3=5;end 6'd11:begin edark=1;egrade=1;ep2=3;ep3=1;end
      6'd12:begin edark=1;egrade=1;ep2=5;ep3=3;end 6'd13:begin edark=1;egrade=1;ep2=5;ep3=5;end
      6'd14:begin edark=1;egrade=0;ep2=5;ep3=1;end 6'd15:begin edark=1;egrade=1;ep2=1;ep3=3;end
      6'd16:begin edark=1;egrade=0;ep2=1;ep3=5;end 6'd17:begin edark=1;egrade=1;ep2=1;ep3=1;end
      6'd18:begin edark=2;egrade=2;ep1=3;end 6'd19:begin edark=2;egrade=1;ep1=3;ep3=2;end
      6'd20:begin edark=2;egrade=1;ep1=3;ep3=4;end 6'd21:begin edark=2;egrade=1;ep1=5;end
      6'd22:begin edark=2;egrade=1;ep1=5;ep3=2;end 6'd23:begin edark=2;egrade=0;ep1=5;ep3=4;end
      6'd24:begin edark=2;egrade=1;ep1=1;end 6'd25:begin edark=2;egrade=0;ep1=1;ep3=2;end
      6'd26:begin edark=2;egrade=1;ep1=1;ep3=4;end 6'd27:begin edark=3;egrade=2;end
      6'd28:begin edark=3;egrade=1;ep2=2;end 6'd29:begin edark=3;egrade=1;ep2=4;end
      6'd30:begin edark=3;egrade=1;ep1=2;end 6'd31:begin edark=3;egrade=1;ep1=2;ep2=2;end
      6'd32:begin edark=3;egrade=0;ep1=2;ep2=4;end 6'd33:begin edark=3;egrade=1;ep1=4;end
      6'd34:begin edark=3;egrade=0;ep1=4;ep2=2;end 6'd35:begin edark=3;egrade=1;ep1=4;ep2=4;end
      default: egrade=3;
    endcase end
  endtask

  integer p,f,xp,zp,xf,zf,a,b,c,d,id,m,n;
  logic [1:0] edark,egrade;
  logic [2:0] ep0,ep1,ep2,ep3,ea;
  initial begin
    repeat(3) @(posedge clk); rst=0; @(posedge clk);
    for(p=0;p<3;p=p+1) for(f=0;f<3;f=f+1) begin
      p_in=p;f_in=f;xp_in=0;zp_in=0;xf_in=0;zf_in=0;opcode=3'b100;operand=0;pulse();
      check_ok(done && !error && p_out==p && f_out==add3(f,p),100+p*3+f);
      operand=1;pulse(); check_ok(done && !error && p_out==add3(p,f) && f_out==f,200+p*3+f);
    end
    p_in=0;f_in=0;
    for(xp=0;xp<3;xp=xp+1) for(zp=0;zp<3;zp=zp+1)
    for(xf=0;xf<3;xf=xf+1) for(zf=0;zf<3;zf=zf+1) begin
      xp_in=xp;zp_in=zp;xf_in=xf;zf_in=zf;
      opcode=3'b000;pulse(); check_ok(xp_out==neg3(zp)&&zp_out==xp&&xf_out==xf&&zf_out==zf,300);
      opcode=3'b001;pulse(); check_ok(xf_out==neg3(zf)&&zf_out==xf&&xp_out==xp&&zp_out==zp,301);
      opcode=3'b010;pulse(); check_ok(zp_out==add3(zp,xp),302);
      opcode=3'b011;pulse(); check_ok(zf_out==add3(zf,xf),303);
      opcode=3'b101;operand=0;pulse(); check_ok(zp_out==add3(zp,1),304);
      opcode=3'b101;operand=1;pulse(); check_ok(zf_out==add3(zf,1),305);
      opcode=3'b100;operand=0;pulse(); check_ok(zp_out==add3(zp,neg3(zf))&&xf_out==add3(xf,xp),306);
      opcode=3'b100;operand=1;pulse(); check_ok(xp_out==add3(xp,xf)&&zf_out==add3(zf,neg3(zp)),307);
    end
    opcode=3'b110;
    for(a=0;a<6;a=a+1) for(b=0;b<2;b=b+1)
    for(c=0;c<6;c=c+1) for(d=0;d<2;d=d+1) begin
      d12_a_in=a;d12_b_in=b;d12_c_in=c;d12_d_in=d;pulse();
      ea=add6(a,b?neg6(c):c); check_ok(done&&!error&&d12_a_out==ea&&d12_b_out==(b^d),400+a*24+b*12+c*2+d);
    end
    d12_a_in=6;d12_c_in=0;pulse();check_ok(error&&done,500);
    opcode=3'b111;
    for(id=0;id<36;id=id+1) begin
      magic_id=id;magic_ack=0;expected_magic(id,edark,egrade,ep0,ep1,ep2,ep3);pulse();
      check_ok(busy&&magic_req&&magic_valid&&!done&&!error,600+id);
      check_ok(magic_dark_mode==edark&&magic_grade==egrade,700+id);
      check_ok(magic_phase6_0==ep0&&magic_phase6_1==ep1&&magic_phase6_2==ep2&&magic_phase6_3==ep3,800+id);
      magic_ack=1;@(posedge clk);#1;magic_ack=0;check_ok(done&&!busy&&!magic_req,900+id);
    end
    magic_id=36;pulse();check_ok(error&&done&&!busy,1000);
    for(m=0;m<3;m=m+1) for(n=0;n<3;n=n+1) begin
      rm=m;rn=n;rlink=1;rstart=1;@(posedge clk);#1;rstart=0;
      repeat(5) @(posedge clk); #1; check_ok(raction==6&&rx==neg3(m)&&rneg&&rz==n,1100+m*3+n);
      @(posedge clk);#1;check_ok(rdone&&!rbusy,1200+m*3+n);
    end
    rlink=0;rstart=1;@(posedge clk);#1;rstart=0;check_ok(rdone&&rerasure&&!rbusy,1300);
    $display("PASS: Passes 2767-2771 exhaustive RTL contract");
    $finish;
  end
endmodule
