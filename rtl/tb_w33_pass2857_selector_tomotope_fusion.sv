module tb_w33_pass2857_selector_tomotope_fusion;
  logic [1:0] face, matching;
  logic [2:0] phase;
  logic valid, tetrahedral_cell;
  logic [3:0] sheet_id;
  logic [1:0] cell_index;
  integer f,m,p,count;
  w33_pass2857_selector_tomotope_fusion dut(.*);
  initial begin
    count=0;
    for (f=0;f<4;f=f+1)
      for (m=0;m<4;m=m+1)
        for (p=0;p<8;p=p+1) begin
          face=f; matching=m; phase=p; #1;
          if (m<3) begin
            if (!valid) $fatal(1,"valid control rejected");
            if (sheet_id != 3*f+m) $fatal(1,"sheet mismatch");
            if (tetrahedral_cell != ~(^phase)) $fatal(1,"parity mismatch");
            count=count+1;
          end else if (valid) $fatal(1,"invalid matching accepted");
        end
    if (count != 96) $fatal(1,"control count mismatch");
    $display("PASS 96/96 fused control words");
    $finish;
  end
endmodule
