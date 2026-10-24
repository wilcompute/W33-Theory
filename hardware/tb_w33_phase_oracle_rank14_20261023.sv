module tb_w33_phase_oracle_rank14_20261023;
reg clk=0;always #5 clk=~clk;
reg rst_n=0,valid_in=0;reg [5:0] addr_a=0,addr_b=0;
wire valid_out,invalid_addr,oracle_bit,local_phase_a,local_phase_b;
wire [13:0] cross_phase_flags;
w33_phase_oracle_rank14_20261023 dut(.*);
reg [39:0] expected_rows[0:39];
integer i,j,ok=0,bad=0;
initial begin
 expected_rows[0]=40'h0381c0e070;
 expected_rows[1]=40'h2492492490;
 expected_rows[2]=40'h88c4623110;
 expected_rows[3]=40'h50a8542a10;
 expected_rows[4]=40'h0000001fef;
 expected_rows[5]=40'he070380051;
 expected_rows[6]=40'h1c0e070031;
 expected_rows[7]=40'h4924924412;
 expected_rows[8]=40'h31188c5014;
 expected_rows[9]=40'h8542a14818;
 expected_rows[10]=40'h9249248092;
 expected_rows[11]=40'h2a150a8218;
 expected_rows[12]=40'h4623118114;
 expected_rows[13]=40'h00003fc00f;
 expected_rows[14]=40'he00e00a381;
 expected_rows[15]=40'h1c70007c01;
 expected_rows[16]=40'h4949083242;
 expected_rows[17]=40'h31232028c4;
 expected_rows[18]=40'h8515102548;
 expected_rows[19]=40'h9224812922;
 expected_rows[20]=40'h2a428430a8;
 expected_rows[21]=40'h4618822624;
 expected_rows[22]=40'h007f80000f;
 expected_rows[23]=40'h1c01780381;
 expected_rows[24]=40'he000c71c01;
 expected_rows[25]=40'h9210525242;
 expected_rows[26]=40'h46404c48c4;
 expected_rows[27]=40'h2a20614548;
 expected_rows[28]=40'h4902648922;
 expected_rows[29]=40'h85084a90a8;
 expected_rows[30]=40'h3104518624;
 expected_rows[31]=40'hff0000000f;
 expected_rows[32]=40'h02f0070381;
 expected_rows[33]=40'h018e381c01;
 expected_rows[34]=40'h20a4a49242;
 expected_rows[35]=40'h80989188c4;
 expected_rows[36]=40'h40c28a8548;
 expected_rows[37]=40'h04c9124922;
 expected_rows[38]=40'h10952150a8;
 expected_rows[39]=40'h08a30c4624;
 repeat(2) @(negedge clk);rst_n=1;
 for(i=0;i<64;i=i+1) for(j=0;j<64;j=j+1)begin
  @(negedge clk); addr_a=i;addr_b=j;valid_in=1;
  @(posedge clk);#1;
  if(!valid_out)$fatal(1,"missing valid: %d,%d",i,j);
  if(i>=40 || j>=40)begin
    if(!invalid_addr || oracle_bit || cross_phase_flags || local_phase_a || local_phase_b)
       $fatal(1,"invalid address accepted at %d,%d",i,j);
    bad=bad+1;
  end else begin
    if(invalid_addr || oracle_bit!==expected_rows[i][j])
       $fatal(1,"oracle disagreement at %d,%d",i,j);
    if(oracle_bit!==((^cross_phase_flags)^local_phase_a^local_phase_b))
       $fatal(1,"local gauge and cross flags inconsistent at %d,%d",i,j);
    ok=ok+1;
  end
 end
 if(ok!=1600 || bad!=2496)$fatal(1,"coverage count");
 @(negedge clk);valid_in=0;
 @(posedge clk);#1;
 if(valid_out || oracle_bit || cross_phase_flags)$fatal(1,"no valid gating");
 $display("PASS 14-term oracle: all %0d W33 phases, %0d invalid addresses, 7 symplectic pairs",ok,bad);
 $finish;
end
endmodule
