// Map 40 four-port physical W33 line-bus indexes to Q(4,3) point indexes.
// Q43 eight-term phase oracle remains a CLASSICAL metadata circuit only.
module w33_linebus_dual_q43_phase_bridge_20261023(
input logic clk,rst_n,valid_in,
input logic [5:0] addr_a,addr_b,
output logic valid_out,invalid_addr,oracle_bit,
output logic [7:0] cross_phase_flags,
output logic local_phase_a,local_phase_b
);
function automatic [5:0] to_q43(input logic [5:0] bus);
 case(bus)
  6'd0: to_q43=6'd0;
  6'd1: to_q43=6'd2;
  6'd2: to_q43=6'd3;
  6'd3: to_q43=6'd4;
  6'd4: to_q43=6'd7;
  6'd5: to_q43=6'd1;
  6'd6: to_q43=6'd11;
  6'd7: to_q43=6'd10;
  6'd8: to_q43=6'd9;
  6'd9: to_q43=6'd5;
  6'd10: to_q43=6'd15;
  6'd11: to_q43=6'd12;
  6'd12: to_q43=6'd8;
  6'd13: to_q43=6'd6;
  6'd14: to_q43=6'd13;
  6'd15: to_q43=6'd14;
  6'd16: to_q43=6'd33;
  6'd17: to_q43=6'd35;
  6'd18: to_q43=6'd34;
  6'd19: to_q43=6'd26;
  6'd20: to_q43=6'd28;
  6'd21: to_q43=6'd27;
  6'd22: to_q43=6'd16;
  6'd23: to_q43=6'd22;
  6'd24: to_q43=6'd31;
  6'd25: to_q43=6'd18;
  6'd26: to_q43=6'd24;
  6'd27: to_q43=6'd36;
  6'd28: to_q43=6'd20;
  6'd29: to_q43=6'd29;
  6'd30: to_q43=6'd38;
  6'd31: to_q43=6'd17;
  6'd32: to_q43=6'd23;
  6'd33: to_q43=6'd32;
  6'd34: to_q43=6'd19;
  6'd35: to_q43=6'd25;
  6'd36: to_q43=6'd37;
  6'd37: to_q43=6'd21;
  6'd38: to_q43=6'd30;
  6'd39: to_q43=6'd39;
  default:to_q43=6'd63;
 endcase
endfunction
wire [5:0] canonical_a=to_q43(addr_a);
wire [5:0] canonical_b=to_q43(addr_b);
q43_phase_oracle_rank8_20261023 target(
.clk(clk),.rst_n(rst_n),.valid_in(valid_in),
.addr_a(canonical_a),.addr_b(canonical_b),
.valid_out(valid_out),.invalid_addr(invalid_addr),
.oracle_bit(oracle_bit),.cross_phase_flags(cross_phase_flags),
.local_phase_a(local_phase_a),.local_phase_b(local_phase_b)
);
endmodule
