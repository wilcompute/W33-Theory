// Compiler-derived exact W33 GF(2) oracle: seven symplectic pairs = 14 products.
// Requires local phases and coherent physical CZ hardware; HDL is classical control ONLY.
module w33_phase_oracle_rank14_20261023(
 input logic clk, rst_n, valid_in,
 input logic [5:0] addr_a, addr_b,
 output logic valid_out, invalid_addr, oracle_bit,
 output logic [13:0] cross_phase_flags,
 output logic local_phase_a,local_phase_b
);
  function automatic [14:0] decode_a(input logic [5:0] addr);
   case(addr)
    6'd0: decode_a=15'h0000;
    6'd1: decode_a=15'h0002;
    6'd2: decode_a=15'h000a;
    6'd3: decode_a=15'h002a;
    6'd4: decode_a=15'h40aa;
    6'd5: decode_a=15'h4001;
    6'd6: decode_a=15'h40ab;
    6'd7: decode_a=15'h0007;
    6'd8: decode_a=15'h001e;
    6'd9: decode_a=15'h007a;
    6'd10: decode_a=15'h00af;
    6'd11: decode_a=15'h00fa;
    6'd12: decode_a=15'h00be;
    6'd13: decode_a=15'h4288;
    6'd14: decode_a=15'h48c9;
    6'd15: decode_a=15'h4a41;
    6'd16: decode_a=15'h06c7;
    6'd17: decode_a=15'h2ef6;
    6'd18: decode_a=15'h1e9a;
    6'd19: decode_a=15'h044d;
    6'd20: decode_a=15'h1c38;
    6'd21: decode_a=15'h2c74;
    6'd22: decode_a=15'h7c88;
    6'd23: decode_a=15'h41c9;
    6'd24: decode_a=15'h7d41;
    6'd25: decode_a=15'h2bc7;
    6'd26: decode_a=15'h33f6;
    6'd27: decode_a=15'h1b9a;
    6'd28: decode_a=15'h174d;
    6'd29: decode_a=15'h2738;
    6'd30: decode_a=15'h0f74;
    6'd31: decode_a=15'h7e88;
    6'd32: decode_a=15'h49c9;
    6'd33: decode_a=15'h7741;
    6'd34: decode_a=15'h2dc7;
    6'd35: decode_a=15'h1df6;
    6'd36: decode_a=15'h059a;
    6'd37: decode_a=15'h134d;
    6'd38: decode_a=15'h3b38;
    6'd39: decode_a=15'h2374;
    default: decode_a=15'h0000;
   endcase
  endfunction
  function automatic [14:0] decode_b(input logic [5:0] addr);
   case(addr)
    6'd0: decode_b=15'h0000;
    6'd1: decode_b=15'h0001;
    6'd2: decode_b=15'h0005;
    6'd3: decode_b=15'h0015;
    6'd4: decode_b=15'h4055;
    6'd5: decode_b=15'h4002;
    6'd6: decode_b=15'h4057;
    6'd7: decode_b=15'h000b;
    6'd8: decode_b=15'h002d;
    6'd9: decode_b=15'h00b5;
    6'd10: decode_b=15'h005f;
    6'd11: decode_b=15'h00f5;
    6'd12: decode_b=15'h007d;
    6'd13: decode_b=15'h4144;
    6'd14: decode_b=15'h44c6;
    6'd15: decode_b=15'h4582;
    6'd16: decode_b=15'h09cb;
    6'd17: decode_b=15'h1df9;
    6'd18: decode_b=15'h2d65;
    6'd19: decode_b=15'h088e;
    6'd20: decode_b=15'h2c34;
    6'd21: decode_b=15'h1cb8;
    6'd22: decode_b=15'h7c44;
    6'd23: decode_b=15'h42c6;
    6'd24: decode_b=15'h7e82;
    6'd25: decode_b=15'h17cb;
    6'd26: decode_b=15'h33f9;
    6'd27: decode_b=15'h2765;
    6'd28: decode_b=15'h2b8e;
    6'd29: decode_b=15'h1b34;
    6'd30: decode_b=15'h0fb8;
    6'd31: decode_b=15'h7d44;
    6'd32: decode_b=15'h46c6;
    6'd33: decode_b=15'h7b82;
    6'd34: decode_b=15'h1ecb;
    6'd35: decode_b=15'h2ef9;
    6'd36: decode_b=15'h0a65;
    6'd37: decode_b=15'h238e;
    6'd38: decode_b=15'h3734;
    6'd39: decode_b=15'h13b8;
    default: decode_b=15'h0000;
   endcase
  endfunction
wire [14:0] da=decode_a(addr_a), db=decode_b(addr_b);
wire invalid_comb=(addr_a>=6'd40)||(addr_b>=6'd40);
wire [13:0] cross_comb=da[13:0]&db[13:0];
wire flip_comb=(^cross_comb)^da[14]^db[14];
always_ff @(posedge clk or negedge rst_n) begin
 if (!rst_n) begin valid_out<=0;invalid_addr<=0;oracle_bit<=0;
 cross_phase_flags<=0;local_phase_a<=0;local_phase_b<=0;end
 else begin
   valid_out<=valid_in;
   invalid_addr<=valid_in&&invalid_comb;
   oracle_bit<=valid_in&&!invalid_comb&&flip_comb;
   cross_phase_flags<=(valid_in&&!invalid_comb)?cross_comb:14'd0;
   local_phase_a<=valid_in&&!invalid_comb&&da[14];
   local_phase_b<=valid_in&&!invalid_comb&&db[14];
 end
end
endmodule
