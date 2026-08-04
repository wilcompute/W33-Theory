// Passes 3364-3375: minimum systematic self-protecting envelope code.
// Appends seven parity bits to each valid five-bit envelope state.
// The resulting 22-word length-12 code has minimum Hamming distance five.
module w33_envelope_systematic_d5_encoder(
  input  wire [4:0] state,
  output reg  [6:0] parity,
  output wire [11:0] codeword,
  output reg valid
);
  always @* begin
    valid=1'b1;
    case(state)
      5'd0: parity=7'd0;
      5'd1: parity=7'd15;
      5'd2: parity=7'd51;
      5'd3: parity=7'd60;
      5'd4: parity=7'd85;
      5'd5: parity=7'd98;
      5'd6: parity=7'd75;
      5'd8: parity=7'd105;
      5'd10: parity=7'd70;
      5'd11: parity=7'd81;
      5'd12: parity=7'd26;
      5'd13: parity=7'd55;
      5'd16: parity=7'd94;
      5'd17: parity=7'd101;
      5'd19: parity=7'd72;
      5'd20: parity=7'd57;
      5'd22: parity=7'd38;
      5'd24: parity=7'd52;
      5'd25: parity=7'd42;
      5'd26: parity=7'd13;
      5'd29: parity=7'd1;
      5'd30: parity=7'd127;
      default: begin parity=7'd0; valid=1'b0; end
    endcase
  end
  assign codeword={parity,state};
endmodule
