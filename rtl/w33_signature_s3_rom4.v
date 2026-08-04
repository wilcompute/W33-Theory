// Passes 3286-3295: exact four-bit nonlinear signature S3 controller.
// op=0 applies R (order 3); op=1 applies S (order 2).
module w33_signature_s3_rom4(
    input wire [3:0] state, input wire op, output reg [3:0] next_state
);
  always @* begin
    case ({op,state})
      5'b0_0000:next_state=4'h0; 5'b0_0001:next_state=4'h4; 5'b0_0010:next_state=4'h6; 5'b0_0011:next_state=4'h2;
      5'b0_0100:next_state=4'h5; 5'b0_0101:next_state=4'h1; 5'b0_0110:next_state=4'h3; 5'b0_0111:next_state=4'hf;
      5'b0_1000:next_state=4'h9; 5'b0_1001:next_state=4'hd; 5'b0_1010:next_state=4'hc; 5'b0_1011:next_state=4'ha;
      5'b0_1100:next_state=4'hb; 5'b0_1101:next_state=4'h8; 5'b0_1110:next_state=4'h7; 5'b0_1111:next_state=4'he;
      5'b1_0000:next_state=4'h0; 5'b1_0001:next_state=4'h1; 5'b1_0010:next_state=4'h8; 5'b1_0011:next_state=4'h9;
      5'b1_0100:next_state=4'h5; 5'b1_0101:next_state=4'h4; 5'b1_0110:next_state=4'hd; 5'b1_0111:next_state=4'hc;
      5'b1_1000:next_state=4'h2; 5'b1_1001:next_state=4'h3; 5'b1_1010:next_state=4'hf; 5'b1_1011:next_state=4'he;
      5'b1_1100:next_state=4'h7; 5'b1_1101:next_state=4'h6; 5'b1_1110:next_state=4'hb; 5'b1_1111:next_state=4'ha;
      default: next_state=4'h0;
    endcase
  end
endmodule
