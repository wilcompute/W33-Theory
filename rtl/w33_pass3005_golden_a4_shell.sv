// Pass 3005: A4 syndrome shell with a structural type barrier around the D4 route core.
module w33_pass3005_golden_a4_shell(
  input logic clk, reset, enable,
  input logic [2:0] opcode,
  input logic [1:0] shell_translation,
  input logic core_authorized,
  output logic [1:0] shell_v,
  output logic [1:0] shell_k,
  output logic [1:0] core_r,
  output logic core_s,
  output logic expensive_slot,
  output logic illegal_cross_domain
);
localparam logic [2:0] OP_NOP=3'd0, OP_SHELL_ADD=3'd1, OP_SHELL_F=3'd2, OP_CORE_R=3'd5, OP_CORE_S=3'd6;
logic [7:0] golden_acc; logic [8:0] golden_sum; logic [1:0] f_shell_v;
always_comb begin
  // With vector bits (x,y)=(shell_v[1],shell_v[0]), F(x,y)=(y,x+y).
  f_shell_v={shell_v[0],shell_v[1]^shell_v[0]};
  golden_sum={1'b0,golden_acc}+9'd89;
  expensive_slot=(golden_sum>=9'd233);
  illegal_cross_domain=((opcode==OP_CORE_R)||(opcode==OP_CORE_S))&&!core_authorized;
end
// Shell domain: core opcodes cannot write these registers.
always_ff @(posedge clk) begin
 if(reset) begin shell_v<=0;shell_k<=0;golden_acc<=0;end
 else if(enable) begin
  golden_acc <= (golden_sum>=9'd233) ? golden_sum-9'd233 : golden_sum[7:0];
  unique case(opcode)
   OP_SHELL_ADD:shell_v<=shell_v^shell_translation;
   OP_SHELL_F:begin shell_v<=f_shell_v;shell_k<=(shell_k==2)?0:shell_k+1'b1;end
   default:begin shell_v<=shell_v;shell_k<=shell_k;end
  endcase
 end
end
// Protected D4 core r^a s^b. Only authorized core-typed operations reach this block.
always_ff @(posedge clk) begin
 if(reset) begin core_r<=0;core_s<=0;end
 else if(enable&&core_authorized) begin
  unique case(opcode)
   OP_CORE_R:core_r<=core_r+1'b1;
   OP_CORE_S:begin core_r<=-core_r;core_s<=~core_s;end
   default:begin core_r<=core_r;core_s<=core_s;end
  endcase
 end
end
endmodule
