module w33_pass2425_holonomy_commit(
  input  logic [3:0] canonical_phase,
  input  logic [3:0] holonomy,
  input  logic       matrix_equal,
  input  logic       holonomy_valid,
  output logic [3:0] phase_out,
  output logic       collision,
  output logic       accept
);
  logic [4:0] sum;
  logic       fields_valid;

  always_comb begin
    fields_valid = (canonical_phase < 4'd12) && (holonomy < 4'd12);
    accept = matrix_equal && holonomy_valid && fields_valid;
    sum = {1'b0, canonical_phase} + {1'b0, holonomy};
    if (!accept) begin
      phase_out = 4'd0;
      collision = 1'b0;
    end else begin
      phase_out = (sum >= 5'd12) ? sum - 5'd12 : sum[3:0];
      collision = (holonomy != 4'd0);
    end
  end
endmodule
