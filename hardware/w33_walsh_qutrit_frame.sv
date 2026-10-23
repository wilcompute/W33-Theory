// W33 Walsh-character qutrit routing frame, logical control only.
// Two commuting bookkeeping domains:
//   phase_e in Z4 accumulates popcount(mask) (ideal cross MZI scalar i)
//   logical_m in (Z2)^2 accumulates XOR mask (Walsh qutrit sign D_m).
// D_m = diag((-1)^(s dot m)), s=1,2,3. Hence D_m^(-1)=D_m.
// Optical phase corrections and logical operations are NOT applied here;
// the module only emits correction metadata for a calibrated controller.
module w33_walsh_qutrit_frame (
  input  logic       clk,
  input  logic       rst_n,
  input  logic       cmd_valid,
  output logic       cmd_ready,
  input  logic [1:0] cmd_mask,
  input  logic       cmd_clear,
  output logic       out_valid,
  input  logic       out_ready,
  output logic [1:0] out_mask,
  output logic [1:0] out_phase_frame,
  output logic [1:0] out_logical_mask_frame,
  output logic [1:0] out_phase_correction,
  output logic [1:0] out_logical_mask_correction
);
  logic [1:0] phase_reg, mask_reg;
  logic [1:0] pc, phase_next, mask_next;
  always_comb begin
    case (cmd_mask)
      2'b00: pc = 2'd0;
      2'b11: pc = 2'd2;
      default: pc = 2'd1;
    endcase
    phase_next = (cmd_clear ? 2'd0 : phase_reg) + pc;
    mask_next  = (cmd_clear ? 2'd0 : mask_reg) ^ cmd_mask;
    cmd_ready = !out_valid || out_ready;
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      phase_reg <= 2'd0;
      mask_reg <= 2'd0;
      out_valid <= 1'b0;
      out_mask <= 2'd0;
      out_phase_frame <= 2'd0;
      out_logical_mask_frame <= 2'd0;
      out_phase_correction <= 2'd0;
      out_logical_mask_correction <= 2'd0;
    end else if (cmd_ready) begin
      out_valid <= cmd_valid;
      if (cmd_valid) begin
        phase_reg <= phase_next;
        mask_reg <= mask_next;
        out_mask <= cmd_mask;
        out_phase_frame <= phase_next;
        out_logical_mask_frame <= mask_next;
        out_phase_correction <= 2'd0 - phase_next;
        out_logical_mask_correction <= mask_next;
      end
    end
  end
endmodule
