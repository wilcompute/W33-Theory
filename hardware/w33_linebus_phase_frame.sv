// W33 4-line-bus coherent phase-frame controller (logical optical phase only).
// Transfers one accepted XOR-mask command to registered metadata; no physical
// optical phase actuator is assumed. Designed for SystemVerilog-2012.
// NOTE: silicon synthesis/simulation tools were unavailable in this pass.
module w33_linebus_phase_frame (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       cmd_valid,
  output logic       cmd_ready,
  input  logic [1:0] cmd_mask,
  input  logic       cmd_clear,
  output logic       result_valid,
  input  logic       result_ready,
  output logic [1:0] result_mask,
  output logic [1:0] result_frame,
  output logic [1:0] result_correction
);
  logic [1:0] frame_reg;
  logic [1:0] popcount2;
  logic [1:0] frame_next;
  // popcount(2'b00)=0, 01/10=1, 11=2.
  always_comb begin
    case (cmd_mask)
      2'b00: popcount2 = 2'd0;
      2'b11: popcount2 = 2'd2;
      default: popcount2 = 2'd1;
    endcase
    frame_next = (cmd_clear ? 2'd0 : frame_reg) + popcount2;
    cmd_ready = !result_valid || result_ready;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      frame_reg         <= 2'd0;
      result_valid      <= 1'b0;
      result_mask       <= 2'd0;
      result_frame      <= 2'd0;
      result_correction <= 2'd0;
    end else if (cmd_ready) begin
      result_valid <= cmd_valid;
      if (cmd_valid) begin
        frame_reg         <= frame_next;
        result_mask       <= cmd_mask;
        result_frame      <= frame_next;
        result_correction <= 2'd0 - frame_next; // i^(-e), e in Z4
      end
    end
  end
endmodule
