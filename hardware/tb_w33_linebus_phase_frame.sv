// Portable, self-checking SV testbench for w33_linebus_phase_frame.
// Run when Icarus/Verilator becomes available; NOT simulated in this pass.
// iverilog -g2012 -s tb_w33_linebus_phase_frame -o phase_tb
//   hardware/w33_linebus_phase_frame.sv hardware/tb_w33_linebus_phase_frame.sv
// vvp phase_tb
module tb_w33_linebus_phase_frame;
  logic clk=0;
  always #5 clk=~clk;
  logic rst_n=0,cmd_valid=0,cmd_ready,cmd_clear=0;
  logic [1:0] cmd_mask=0;
  logic result_valid,result_ready=1;
  logic [1:0] result_mask,result_frame,result_correction;
  w33_linebus_phase_frame dut(.*);

  task automatic push(input logic [1:0] mask,
                      input logic clear_frame,
                      input logic [1:0] expect_frame);
    @(negedge clk);
    if (!cmd_ready) $fatal(1,"unexpected backpressure");
    cmd_mask=mask;cmd_clear=clear_frame;cmd_valid=1;
    @(posedge clk);#1;
    if (!result_valid || result_mask!==mask ||
        result_frame!==expect_frame ||
        result_correction!==(2'd0-expect_frame))
      $fatal(1,"incorrect phase frame: mask=%d got=%d expected=%d",
             mask,result_frame,expect_frame);
    @(negedge clk);cmd_valid=0;
  endtask

  initial begin
    repeat(2) @(negedge clk);rst_n=1;
    push(2'd1,1'b0,2'd1);
    push(2'd2,1'b0,2'd2);
    push(2'd3,1'b0,2'd0);
    push(2'd3,1'b0,2'd2);
    push(2'd1,1'b1,2'd1);
    @(negedge clk);
    result_ready=0;cmd_mask=2'd3;cmd_valid=1;
    @(posedge clk);#1;
    if (!result_valid || result_frame!==2'd3)
      $fatal(1,"first stall transfer frame");
    @(negedge clk);
    cmd_mask=2'd2;
    @(posedge clk);#1;
    if (cmd_ready || result_frame!==2'd3 || result_mask!==2'd3)
      $fatal(1,"backpressure did not hold registered phase");
    @(negedge clk);result_ready=1;cmd_mask=2'd2;
    @(posedge clk);#1;
    if (!result_valid || result_frame!==2'd0 || result_mask!==2'd2)
      $fatal(1,"ready/valid replacement failed");
    @(negedge clk);cmd_valid=0;
    @(posedge clk);#1;
    if (result_valid) $fatal(1,"valid should clear");
    $display("PASS w33_linebus_phase_frame SV testbench");
    $finish;
  end
endmodule
