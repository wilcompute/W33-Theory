module tb_q43_phase_oracle_rank8_20261023;
reg clk=0;always #5 clk=~clk;
reg rst_n=0,valid_in=0;reg [5:0] addr_a=0,addr_b=0;
wire valid_out,invalid_addr,oracle_bit,local_phase_a,local_phase_b;
wire [7:0] cross_phase_flags;
q43_phase_oracle_rank8_20261023 dut(.*);
reg [39:0] expected_rows[0:39];
integer i,j,valid_cases=0,invalid_cases=0;
initial begin
expected_rows[0]=40'h0e1c00039c;
expected_rows[1]=40'h3264000ce4;
expected_rows[2]=40'h00003f007b;
expected_rows[3]=40'h50c280a815;
expected_rows[4]=40'ha12140540d;
expected_rows[5]=40'h4512409246;
expected_rows[6]=40'h8889806126;
expected_rows[7]=40'h0180c30f03;
expected_rows[8]=40'h60221862c1;
expected_rows[9]=40'h90412491a1;
expected_rows[10]=40'h480a245892;
expected_rows[11]=40'h841118a48a;
expected_rows[12]=40'h028498c630;
expected_rows[13]=40'h030464c948;
expected_rows[14]=40'h1450033550;
expected_rows[15]=40'h2828033a28;
expected_rows[16]=40'h24c854c084;
expected_rows[17]=40'h1930a8c084;
expected_rows[18]=40'h1907112604;
expected_rows[19]=40'h2487221904;
expected_rows[20]=40'hc230851904;
expected_rows[21]=40'hc2484a2604;
expected_rows[22]=40'h02b32120b0;
expected_rows[23]=40'h034b1210c8;
expected_rows[24]=40'h1428cc0a50;
expected_rows[25]=40'h2850cc0528;
expected_rows[26]=40'h01f80c3003;
expected_rows[27]=40'h6015a18441;
expected_rows[28]=40'h900e524821;
expected_rows[29]=40'h4845528112;
expected_rows[30]=40'h8426a1420a;
expected_rows[31]=40'hd8044910c8;
expected_rows[32]=40'he4048620b0;
expected_rows[33]=40'h3c00f03003;
expected_rows[34]=40'h4b41094821;
expected_rows[35]=40'h86a2068441;
expected_rows[36]=40'h629106420a;
expected_rows[37]=40'h930a098112;
expected_rows[38]=40'h15a8300528;
expected_rows[39]=40'h29d0300a50;
repeat(2) @(negedge clk);rst_n=1;
for(i=0;i<64;i=i+1)for(j=0;j<64;j=j+1)begin
 @(negedge clk);addr_a=i;addr_b=j;valid_in=1;
 @(posedge clk);#1;
 if(!valid_out)$fatal(1,"valid missing");
 if(i>=40||j>=40)begin
   if(!invalid_addr||oracle_bit||cross_phase_flags||local_phase_a||local_phase_b)
     $fatal(1,"invalid address accepted %d,%d",i,j);
   invalid_cases=invalid_cases+1;
 end else begin
   if(invalid_addr || oracle_bit!==expected_rows[i][j])
     $fatal(1,"Q43 oracle wrong %d,%d",i,j);
   if(oracle_bit!==((^cross_phase_flags)^local_phase_a^local_phase_b))
     $fatal(1,"Q43 gauge wrong %d,%d",i,j);
   valid_cases=valid_cases+1;
 end
end
if(valid_cases!=1600||invalid_cases!=2496)$fatal(1,"coverage");
@(negedge clk);valid_in=0;
@(posedge clk);#1;
if(valid_out||oracle_bit||cross_phase_flags)$fatal(1,"invalid deassert");
$display("PASS Q43 8-term oracle %0d valid and %0d invalid; 4 symplectic pairs",valid_cases,invalid_cases);
$finish;end
endmodule
