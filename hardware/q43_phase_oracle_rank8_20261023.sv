// Four hyperbolic pairs (8 cross terms), plus two local sign lookups.
// Purely CLASSICAL codeword phase metadata; no coherent physical CZ implemented.
module q43_phase_oracle_rank8_20261023(
input logic clk,rst_n,valid_in,
input logic [5:0] addr_a,addr_b,
output logic valid_out,invalid_addr,oracle_bit,
output logic [7:0] cross_phase_flags,
output logic local_phase_a,local_phase_b
);
function automatic [8:0] decode_a(input logic [5:0] addr);
  case(addr)
    6'd0: decode_a=9'h000;
    6'd1: decode_a=9'h002;
    6'd2: decode_a=9'h10a;
    6'd3: decode_a=9'h101;
    6'd4: decode_a=9'h10b;
    6'd5: decode_a=9'h007;
    6'd6: decode_a=9'h00f;
    6'd7: decode_a=9'h128;
    6'd8: decode_a=9'h1a5;
    6'd9: decode_a=9'h18d;
    6'd10: decode_a=9'h083;
    6'd11: decode_a=9'h0a9;
    6'd12: decode_a=9'h0a6;
    6'd13: decode_a=9'h084;
    6'd14: decode_a=9'h02e;
    6'd15: decode_a=9'h02c;
    6'd16: decode_a=9'h06a;
    6'd17: decode_a=9'h04a;
    6'd18: decode_a=9'h01a;
    6'd19: decode_a=9'h0da;
    6'd20: decode_a=9'h07a;
    6'd21: decode_a=9'h09a;
    6'd22: decode_a=9'h0f6;
    6'd23: decode_a=9'h034;
    6'd24: decode_a=9'h0ce;
    6'd25: decode_a=9'h0cc;
    6'd26: decode_a=9'h1c8;
    6'd27: decode_a=9'h1f5;
    6'd28: decode_a=9'h13d;
    6'd29: decode_a=9'h033;
    6'd30: decode_a=9'h0f9;
    6'd31: decode_a=9'h0b4;
    6'd32: decode_a=9'h056;
    6'd33: decode_a=9'h1e8;
    6'd34: decode_a=9'h1bd;
    6'd35: decode_a=9'h155;
    6'd36: decode_a=9'h059;
    6'd37: decode_a=9'h0b3;
    6'd38: decode_a=9'h0ec;
    6'd39: decode_a=9'h0ee;
    default: decode_a=9'h000;
  endcase
endfunction
function automatic [8:0] decode_b(input logic [5:0] addr);
  case(addr)
    6'd0: decode_b=9'h000;
    6'd1: decode_b=9'h001;
    6'd2: decode_b=9'h105;
    6'd3: decode_b=9'h102;
    6'd4: decode_b=9'h107;
    6'd5: decode_b=9'h00b;
    6'd6: decode_b=9'h00f;
    6'd7: decode_b=9'h114;
    6'd8: decode_b=9'h15a;
    6'd9: decode_b=9'h14e;
    6'd10: decode_b=9'h043;
    6'd11: decode_b=9'h056;
    6'd12: decode_b=9'h059;
    6'd13: decode_b=9'h048;
    6'd14: decode_b=9'h01d;
    6'd15: decode_b=9'h01c;
    6'd16: decode_b=9'h095;
    6'd17: decode_b=9'h085;
    6'd18: decode_b=9'h025;
    6'd19: decode_b=9'h0e5;
    6'd20: decode_b=9'h0b5;
    6'd21: decode_b=9'h065;
    6'd22: decode_b=9'h0f9;
    6'd23: decode_b=9'h038;
    6'd24: decode_b=9'h0cd;
    6'd25: decode_b=9'h0cc;
    6'd26: decode_b=9'h1c4;
    6'd27: decode_b=9'h1fa;
    6'd28: decode_b=9'h13e;
    6'd29: decode_b=9'h033;
    6'd30: decode_b=9'h0f6;
    6'd31: decode_b=9'h078;
    6'd32: decode_b=9'h0a9;
    6'd33: decode_b=9'h1d4;
    6'd34: decode_b=9'h17e;
    6'd35: decode_b=9'h1aa;
    6'd36: decode_b=9'h0a6;
    6'd37: decode_b=9'h073;
    6'd38: decode_b=9'h0dc;
    6'd39: decode_b=9'h0dd;
    default: decode_b=9'h000;
  endcase
endfunction
wire [8:0] da=decode_a(addr_a), db=decode_b(addr_b);
wire invalid_comb=(addr_a>=6'd40)||(addr_b>=6'd40);
wire [7:0] cross_comb=da[7:0]&db[7:0];
wire flip_comb=(^cross_comb)^da[8]^db[8];
always_ff @(posedge clk or negedge rst_n) begin
 if(!rst_n) begin
  valid_out<=0;invalid_addr<=0;oracle_bit<=0;
  cross_phase_flags<=0;local_phase_a<=0;local_phase_b<=0;
 end else begin
  valid_out<=valid_in;
  invalid_addr<=valid_in&&invalid_comb;
  oracle_bit<=valid_in&&!invalid_comb&&flip_comb;
  cross_phase_flags<=(valid_in&&!invalid_comb)?cross_comb:8'd0;
  local_phase_a<=valid_in&&!invalid_comb&&da[8];
  local_phase_b<=valid_in&&!invalid_comb&&db[8];
 end
end
endmodule
