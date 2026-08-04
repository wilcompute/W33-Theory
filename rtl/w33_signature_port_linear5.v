// Passes 3286-3295: shared five-bit linear S3 controller.
// Same matrices preserve the signature alphabet, port alphabet, and minimal 22-state envelope.
module w33_signature_port_linear5(
 input wire [4:0] state,input wire op,output wire [4:0] next_state,
 output reg valid_signature,output reg valid_port,output reg valid_envelope,output wire guard);
  wire [4:0] r_state={state[3]^state[4],state[4],state[1],state[0],state[2]};
  wire [4:0] s_state={state[4],state[3]^state[4],state[1],state[2],state[0]};
  assign next_state=op?s_state:r_state;
  assign guard=~valid_envelope;
  always @* begin
    valid_signature=1'b0; valid_port=1'b0; valid_envelope=1'b0;
    case(state)
      5'd0,5'd1,5'd2,5'd4,5'd10,5'd11,5'd12,5'd13,5'd17,5'd19,5'd20,5'd22,5'd25,5'd26,5'd29,5'd30:valid_signature=1'b1;
      default:valid_signature=1'b0;
    endcase
    case(state)
      5'd0,5'd1,5'd2,5'd3,5'd4,5'd5,5'd6,5'd8,5'd10,5'd12,5'd16,5'd17,5'd20,5'd24,5'd25,5'd26:valid_port=1'b1;
      default:valid_port=1'b0;
    endcase
    case(state)
      5'd0,5'd1,5'd2,5'd3,5'd4,5'd5,5'd6,5'd8,5'd10,5'd11,5'd12,5'd13,5'd16,5'd17,5'd19,5'd20,5'd22,5'd24,5'd25,5'd26,5'd29,5'd30:valid_envelope=1'b1;
      default:valid_envelope=1'b0;
    endcase
  end
endmodule
