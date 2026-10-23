// Actual Icarus simulation scoreboard for two coupled Walsh qutrit frames.
// 1200 deterministic pseudorandom cycles, stalls, clears and XOR composition.
module tb_w33_walsh_qutrit_frame;
reg clk=0;always #5 clk=~clk;
reg rst_n=0,cmd_valid=0,cmd_clear=0,out_ready=0;
reg [1:0] cmd_mask=0;
wire cmd_ready,out_valid;
wire [1:0] out_mask,out_phase_frame,out_logical_mask_frame;
wire [1:0] out_phase_correction,out_logical_mask_correction;
w33_walsh_qutrit_frame dut(.*);
reg [31:0] rng=32'h932fcb17;
reg ref_valid=0;
reg [1:0] ref_phase=0,ref_logical=0,ref_mask=0;
reg accept;
reg [1:0] popcount;
integer k,updates=0,stalls=0;
initial begin
 repeat(3) @(negedge clk);
 rst_n=1;
 for(k=0;k<1200;k=k+1)begin
   @(negedge clk);
   rng={rng[30:0],rng[31]^rng[21]^rng[1]^rng[0]};
   cmd_mask=rng[4:3];
   cmd_valid=rng[9];
   out_ready=rng[15];
   cmd_clear=(k%97==0);
   #1;
   accept=(!ref_valid||out_ready);
   if(cmd_ready!==accept) $fatal(1,"ready mismatch %d",k);
   if(!accept) stalls=stalls+1;
   if(accept)begin
     ref_valid=cmd_valid;
     if(cmd_valid)begin
       case(cmd_mask)
         2'b00:popcount=2'd0;
         2'b11:popcount=2'd2;
         default:popcount=2'd1;
       endcase
       ref_phase=(cmd_clear?2'd0:ref_phase)+popcount;
       ref_logical=(cmd_clear?2'd0:ref_logical)^cmd_mask;
       ref_mask=cmd_mask;
       updates=updates+1;
     end
   end
   @(posedge clk);#1;
   if(out_valid!==ref_valid ||
      out_mask!==ref_mask ||
      out_phase_frame!==ref_phase ||
      out_logical_mask_frame!==ref_logical ||
      out_phase_correction!==(2'd0-ref_phase) ||
      out_logical_mask_correction!==ref_logical)
       $fatal(1,"Walsh phase/logical scoreboard mismatch cycle=%d, phase=%d, logical=%d",k,out_phase_frame,out_logical_mask_frame);
 end
 if(stalls<70||updates<200)$fatal(1,"coverage too low");
 $display("PASS W33 Walsh qutrit dual frame 1200 cycles; updates=%d stalls=%d",updates,stalls);
 $finish;
end
endmodule
