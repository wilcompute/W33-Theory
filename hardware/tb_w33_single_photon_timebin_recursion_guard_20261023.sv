// Icarus deterministic scoreboard. Validates repeated 3-cycle, fresh storage
// obligations, invalid paths, clear, and ready/valid backpressure (2000 cycles).
module tb_w33_single_photon_timebin_recursion_guard;
reg clk=0;always #5 clk=~clk;
reg rst_n=0,cmd_valid=0,cmd_fresh=0,cmd_clear=0,out_ready=0;
reg [1:0] cmd_path=0;
wire cmd_ready,out_valid,out_fresh_storage_unimplemented;
wire out_returned_after_three_reuses,out_invalid_path;
wire [1:0] out_time_bin,out_reuse_round_mod3;
wire [7:0] out_fresh_registers_obligated;
w33_single_photon_timebin_recursion_guard dut(.*);
reg [31:0] rng=32'hf233badd;
reg expected_valid=0,expected_fresh_alarm=0,expected_returned=0,expected_invalid=0;
reg [1:0] expected_time=0,expected_round=0;
reg [7:0] expected_fresh=0;
reg can_accept;
integer k,accepted=0,stalls=0,freshes=0,reuses=0,invalids=0;
function automatic [1:0] add3(input reg [1:0] a,input reg [1:0] b);
integer v;begin v=a+b; if(v>=3) v=v-3; add3=v[1:0];end
endfunction
initial begin
 repeat(3) @(negedge clk);rst_n=1;
 for(k=0;k<2000;k=k+1)begin
   @(negedge clk);
   rng={rng[30:0],rng[31]^rng[21]^rng[1]^rng[0]};
   cmd_valid=rng[5];out_ready=rng[11];cmd_fresh=rng[8];
   cmd_path=rng[17:16];
   cmd_clear=(k%113==0);
   #1; can_accept=(!expected_valid || out_ready);
   if(cmd_ready!==can_accept)$fatal(1,"ready wrong at cycle %0d",k);
   if(!can_accept)stalls=stalls+1;
   if(can_accept)begin
     expected_valid=cmd_valid;
     if(cmd_valid)begin
       accepted=accepted+1;
       if(cmd_clear)begin expected_time=0;expected_round=0;expected_fresh=0;end
       expected_invalid=(cmd_path==3);
       expected_returned=0;
       expected_fresh_alarm=0;
       if(expected_invalid)invalids=invalids+1;
       else if(cmd_fresh)begin expected_fresh=expected_fresh+8'd1;expected_fresh_alarm=1;freshes=freshes+1;end
       else begin
         expected_time=add3(expected_time,cmd_path);
         expected_round=add3(expected_round,2'd1);
         expected_returned=(expected_round==0);
         reuses=reuses+1;
       end
     end
   end
   @(posedge clk);#1;
   if(out_valid!==expected_valid ||
      out_time_bin!==expected_time ||
      out_reuse_round_mod3!==expected_round ||
      out_fresh_registers_obligated!==expected_fresh ||
      out_fresh_storage_unimplemented!==expected_fresh_alarm ||
      out_returned_after_three_reuses!==expected_returned ||
      out_invalid_path!==expected_invalid)
      $fatal(1,"recursion scoreboard fail cycle %0d",k);
 end
 if(accepted<300||stalls<100||freshes<80||reuses<80||invalids<80)
   $fatal(1,"coverage insufficient");
 $display("PASS recursive metadata 2000 cycles: accepted=%0d stalls=%0d fresh=%0d reuse=%0d invalid=%0d",accepted,stalls,freshes,reuses,invalids);
 $finish;
end
endmodule
