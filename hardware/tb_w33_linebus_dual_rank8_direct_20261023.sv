module tb_w33_linebus_dual_rank8_direct_20261023;
reg clk=0;always #5 clk=~clk;
reg rst_n=0,valid_in=0;reg [5:0] addr_a=0,addr_b=0;
wire valid_out,invalid_addr,oracle_bit,local_phase_a,local_phase_b;
wire [7:0] cross_phase_flags;
w33_linebus_dual_rank8_direct_20261023 dut(.*);
reg [39:0] expected_rows[0:39];
integer i,j,valid_cases=0,invalid_cases=0;
initial begin
expected_rows[0]=40'h00003f111e;
expected_rows[1]=40'h249240222d;
expected_rows[2]=40'h494900444b;
expected_rows[3]=40'h9224808887;
expected_rows[4]=40'h0381c011e1;
expected_rows[5]=40'h50280922d2;
expected_rows[6]=40'h84141444b4;
expected_rows[7]=40'h2842228878;
expected_rows[8]=40'he00e001e11;
expected_rows[9]=40'h0a40942d22;
expected_rows[10]=40'h10a0624b44;
expected_rows[11]=40'h0511098788;
expected_rows[12]=40'h1c7000e111;
expected_rows[13]=40'h810522d222;
expected_rows[14]=40'h220289b444;
expected_rows[15]=40'h4088547888;
expected_rows[16]=40'h3118864821;
expected_rows[17]=40'h88a3052481;
expected_rows[18]=40'h4644438241;
expected_rows[19]=40'h4623304821;
expected_rows[20]=40'h8898a88241;
expected_rows[21]=40'h3144582481;
expected_rows[22]=40'h5013a48412;
expected_rows[23]=40'h2825514218;
expected_rows[24]=40'h8448ca2814;
expected_rows[25]=40'h0a1c4a4182;
expected_rows[26]=40'h052aa42148;
expected_rows[27]=40'h10c7118124;
expected_rows[28]=40'h8162511842;
expected_rows[29]=40'h40d48a1428;
expected_rows[30]=40'h2239241284;
expected_rows[31]=40'h2728128412;
expected_rows[32]=40'h4a94212814;
expected_rows[33]=40'h91c20c4218;
expected_rows[34]=40'h38850c1842;
expected_rows[35]=40'h5502921284;
expected_rows[36]=40'h8e08611428;
expected_rows[37]=40'hc4c0a14182;
expected_rows[38]=40'ha9204c8124;
expected_rows[39]=40'h7211122148;
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
$display("PASS native W33 line-bus Q43-dual rank8 oracle %0d valid and %0d invalid; 4 symplectic pairs",valid_cases,invalid_cases);
$finish;end
endmodule
