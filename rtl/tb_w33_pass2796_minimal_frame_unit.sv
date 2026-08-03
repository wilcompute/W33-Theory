`timescale 1ns/1ps
module tb_w33_pass2796_minimal_frame_unit;
    reg clk=0,rst=1,load=0,valid=0;
    reg [1:0] xp_in,zp_in,xf_in,zf_in,micro_op;
    wire [1:0] xp,zp,xf,zf;
    w33_pass2796_minimal_frame_unit dut(.*);
    always #5 clk=~clk;
    task step(input [1:0] op); begin micro_op=op; valid=1; @(posedge clk); #1; valid=0; end endtask
    initial begin
        xp_in=1;zp_in=2;xf_in=2;zf_in=1;micro_op=0;
        repeat(2) @(posedge clk); rst=0; load=1; @(posedge clk); #1; load=0;
        if ({xp,zp,xf,zf} !== {2'd1,2'd2,2'd2,2'd1}) $fatal(1,"load");
        step(0); if ({xp,zp,xf,zf} !== {2'd1,2'd1,2'd2,2'd1}) $fatal(1,"Fp");
        step(1); if ({xp,zp,xf,zf} !== {2'd1,2'd0,2'd0,2'd1}) $fatal(1,"CXpf");
        step(2); if ({xp,zp,xf,zf} !== {2'd1,2'd0,2'd0,2'd1}) $fatal(1,"CXfp");
        step(3); if (zp !== 2'd1) $fatal(1,"Zp");
        $display("PASS w33_pass2796_minimal_frame_unit");
        $finish;
    end
endmodule
