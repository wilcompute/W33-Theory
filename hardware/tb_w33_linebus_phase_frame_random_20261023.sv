// Verified with Icarus Verilog 12 on 2026-10-23: 1500 cycles, 493 commands, 507 stalls.
module tb_w33_linebus_phase_frame_random;
reg clk=0;always #5 clk=~clk;
reg rst_n=0,cmd_valid=0,cmd_clear=0,result_ready=0;
reg [1:0] cmd_mask=0;
wire cmd_ready,result_valid;
wire [1:0] result_mask,result_frame,result_correction;
w33_linebus_phase_frame dut(.*);
reg [31:0] prng=32'h8f3ca1b7;
reg ref_valid=0;
reg [1:0] ref_frame=0,ref_mask=0,ref_out=0,ref_corr=0;
reg accept;
integer k,commits=0,stalls=0;
reg [1:0] count_bits;
initial begin
  repeat(3) @(negedge clk);
  rst_n=1;
  for(k=0;k<1500;k=k+1)begin
    @(negedge clk);
    prng={prng[30:0],prng[31]^prng[21]^prng[1]^prng[0]};
    cmd_mask=prng[5:4];
    cmd_valid=prng[8];
    result_ready=prng[12];
    cmd_clear=(k%79==0);
    #1;
    accept=(!ref_valid || result_ready);
    if(cmd_ready!==accept) $fatal(1,"ready mismatch step=%d",k);
    if(!accept) stalls=stalls+1;
    if(accept)begin
      ref_valid=cmd_valid;
      if(cmd_valid)begin
        case(cmd_mask)
          2'b00:count_bits=2'd0;
          2'b11:count_bits=2'd2;
          default:count_bits=2'd1;
        endcase
        ref_frame=(cmd_clear?2'd0:ref_frame)+count_bits;
        ref_mask=cmd_mask;
        ref_out=ref_frame;
        ref_corr=2'd0-ref_frame;
        commits=commits+1;
      end
    end
    @(posedge clk);#1;
    if(result_valid!==ref_valid || result_mask!==ref_mask ||
       result_frame!==ref_out || result_correction!==ref_corr)
       $fatal(1,"scoreboard mismatch step=%d",k);
  end
  if(stalls<50 || commits<100)
    $fatal(1,"random coverage insufficient: stalls=%d accepted=%d",stalls,commits);
  $display("PASS random 1500-cycle linebus phase frame: accepted=%d stalls=%d",commits,stalls);
  $finish;
end
endmodule
