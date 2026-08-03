// Pass 2771: classical control plane for the exact entanglement-assisted remote qutrit SUM.
module w33_pass2771_remote_sum_link(
  input  logic       clk,
  input  logic       rst,
  input  logic       start,
  input  logic       link_valid,
  input  logic [1:0] meas_m,
  input  logic [1:0] meas_n,
  output logic       busy,
  output logic       done,
  output logic       erasure,
  output logic [2:0] action,
  output logic [1:0] x_correction_b,
  output logic       negate_b,
  output logic [1:0] z_frame_a
);
  logic [2:0] state;
  function automatic logic [1:0] neg3(input logic [1:0] x);
    case(x) 2'd0: neg3=2'd0; 2'd1: neg3=2'd2; default: neg3=2'd1; endcase
  endfunction
  always_ff @(posedge clk) begin
    if (rst) begin
      state<=0; busy<=0; done<=0; erasure<=0; action<=0;
      x_correction_b<=0; negate_b<=0; z_frame_a<=0;
    end else begin
      done<=0; erasure<=0;
      if (!busy && start) begin
        if (!link_valid) begin erasure<=1; done<=1; action<=0; end
        else begin busy<=1; state<=1; action<=1; end
      end else if (busy) begin
        case(state)
          1: begin state<=2; action<=2; end
          2: begin state<=3; action<=3; x_correction_b<=neg3(meas_m); negate_b<=1; end
          3: begin state<=4; action<=4; end
          4: begin state<=5; action<=5; end
          5: begin state<=6; action<=6; z_frame_a<=meas_n; end
          default: begin state<=0; action<=0; busy<=0; done<=1; negate_b<=0; end
        endcase
      end
    end
  end
endmodule
