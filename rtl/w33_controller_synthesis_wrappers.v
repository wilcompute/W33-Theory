// Passes 3308-3319: common registered wrappers for fair synthesis comparison.

module w33_signature_s3_rom4_registered(
    input wire clk,
    input wire [3:0] state,
    input wire op,
    output reg [3:0] result
);
  wire [3:0] next_state;
  w33_signature_s3_rom4 core(.state(state),.op(op),.next_state(next_state));
  always @(posedge clk) result <= next_state;
endmodule

module w33_port_s3_linear4_registered(
    input wire clk,
    input wire [3:0] state,
    input wire op,
    output reg [3:0] result
);
  wire [3:0] next_state;
  w33_port_s3_linear4 core(.state(state),.op(op),.next_state(next_state));
  always @(posedge clk) result <= next_state;
endmodule

module w33_signature_port_linear5_registered(
    input wire clk,
    input wire [4:0] state,
    input wire op,
    output reg [4:0] result,
    output reg valid_envelope
);
  wire [4:0] next_state;
  wire valid_signature_wire,valid_port_wire,valid_envelope_wire,guard;
  w33_signature_port_linear5 core(
    .state(state),.op(op),.next_state(next_state),
    .valid_signature(valid_signature_wire),.valid_port(valid_port_wire),
    .valid_envelope(valid_envelope_wire),.guard(guard)
  );
  always @(posedge clk) begin
    result <= next_state;
    valid_envelope <= valid_envelope_wire;
  end
endmodule
