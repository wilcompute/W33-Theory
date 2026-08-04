// Pass 3172: information-aware tri-ISA policy.
// For nonnegative collision price, fast6 dominates current4 in the frozen runtime model.
// fast6 remains gated by calibration and area; it yields to low4 above c=16.70164249.
module w33_pass3172_information_tri_isa_scheduler #(
  parameter logic [15:0] FAST_TO_LOW_Q8_8=16'd4276, // round(16.70164249*256)
  parameter logic [15:0] CURRENT_TO_LOW_Q8_8=16'd958 // round(3.74193382*256)
)(
  input logic clk,input logic rst,input logic [15:0] effective_collision_price_q8_8_i,
  input logic fast6_calibrated_i,input logic low4_calibrated_i,input logic fast6_area_available_i,
  output logic [1:0] mode_o, // 0 current4,1 low4,2 fast6
  output logic switch_o
);
  logic [1:0] next_mode;
  always_comb begin
    if(fast6_calibrated_i && fast6_area_available_i)
      next_mode=(effective_collision_price_q8_8_i<FAST_TO_LOW_Q8_8)?2'd2:(low4_calibrated_i?2'd1:2'd0);
    else if(low4_calibrated_i && effective_collision_price_q8_8_i>=CURRENT_TO_LOW_Q8_8) next_mode=2'd1;
    else next_mode=2'd0;
  end
  always_ff @(posedge clk) begin
    if(rst) begin mode_o<=0;switch_o<=0;end
    else begin switch_o<=(next_mode!=mode_o);mode_o<=next_mode;end
  end
endmodule
