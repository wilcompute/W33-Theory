// Pass 2965: three distinct pilots determine an S4 route permutation.
module w33_pass2965_curvature_pilot_checker(
  input  logic [1:0] expected0, expected1, expected2,
  input  logic [1:0] observed0, observed1, observed2,
  output logic       route_fault
);
  always_comb route_fault = (expected0 != observed0) |
                            (expected1 != observed1) |
                            (expected2 != observed2);
endmodule
