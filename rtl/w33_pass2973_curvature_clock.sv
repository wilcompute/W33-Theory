// Pass 2973: logical Z3 x Z4 curvature clock with reversible direction.
module w33_pass2973_curvature_clock(
 input logic clk, reset, enable, reverse,
 output logic [1:0] phase3,
 output logic [1:0] slot4,
 output logic [3:0] tick12
);
function automatic [1:0] inc3(input [1:0] x); inc3=(x==2)?0:x+1; endfunction
function automatic [1:0] dec3(input [1:0] x); dec3=(x==0)?2:x-1; endfunction
always_ff @(posedge clk) begin
 if(reset) begin phase3<=0; slot4<=0; end
 else if(enable) begin
   if(reverse) begin phase3<=dec3(phase3); slot4<=slot4-1'b1; end
   else begin phase3<=inc3(phase3); slot4<=slot4+1'b1; end
 end
end
// CRT lookup: unique n in 0..11 with n mod3=phase3 and n mod4=slot4.
always_comb begin
 tick12=0;
 unique case({phase3,slot4})
  4'b0000:tick12=0;  4'b0001:tick12=9;  4'b0010:tick12=6;  4'b0011:tick12=3;
  4'b0100:tick12=4;  4'b0101:tick12=1;  4'b0110:tick12=10; 4'b0111:tick12=7;
  4'b1000:tick12=8;  4'b1001:tick12=5;  4'b1010:tick12=2;  4'b1011:tick12=11;
  default:tick12=0;
 endcase
end
endmodule
