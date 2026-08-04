`timescale 1ns/1ps
module tb_w33_pass3252_s3_decoder;
    logic valid; logic [2:0] syndrome; logic [7:0] r0,r1,r2;
    logic detected,tie,sideinfo,blind; logic [1:0] edge; logic [2:0] correction;
    w33_pass3252_s3_reliability_decoder dut(
      .valid(valid),.syndrome(syndrome),.reliability0(r0),.reliability1(r1),.reliability2(r2),
      .detected(detected),.tie(tie),.edge_select(edge),.correction(correction),
      .sideinfo_correction_valid(sideinfo),.blind_guarantee(blind));
    function automatic [2:0] inv(input [2:0] g);
      case(g) 3:inv=4; 4:inv=3; default:inv=g; endcase
    endfunction
    integer s;
    initial begin
      valid=1; syndrome=0; r0=1;r1=2;r2=3; #1;
      if(detected || correction!=0 || blind) $fatal(1,"identity control failed");
      for(s=1;s<=5;s=s+1) begin
        syndrome=s; r0=9;r1=2;r2=1; #1;
        if(!detected || tie || edge!=0 || correction!=s || !sideinfo || blind) $fatal(1,"edge0 failed");
        r0=1;r1=9;r2=2; #1;
        if(tie || edge!=1 || correction!=s) $fatal(1,"edge1 failed");
        r0=1;r1=2;r2=9; #1;
        if(tie || edge!=2 || correction!=inv(s)) $fatal(1,"edge2 inverse failed");
        r0=7;r1=7;r2=1; #1;
        if(!tie || sideinfo) $fatal(1,"tie gate failed");
      end
      valid=0; syndrome=3; r0=9;r1=1;r2=1; #1;
      if(detected || correction!=0) $fatal(1,"valid gate failed");
      $display("PASS S3 RELIABILITY DECODER");
      $finish;
    end
endmodule
