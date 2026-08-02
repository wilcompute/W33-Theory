module w33_pass2425_holonomy_commit_formal;
  (* anyconst *) logic [3:0] canonical_phase;
  (* anyconst *) logic [3:0] holonomy;
  (* anyconst *) logic       matrix_equal;
  (* anyconst *) logic       holonomy_valid;

  logic [3:0] phase_out;
  logic       collision;
  logic       accept;
  logic [4:0] sum;
  logic [3:0] expected;
  logic       expected_accept;

  w33_pass2425_holonomy_commit dut(
    .canonical_phase(canonical_phase),
    .holonomy(holonomy),
    .matrix_equal(matrix_equal),
    .holonomy_valid(holonomy_valid),
    .phase_out(phase_out),
    .collision(collision),
    .accept(accept)
  );

  always_comb begin
    sum = {1'b0, canonical_phase} + {1'b0, holonomy};
    expected = (sum >= 5'd12) ? sum - 5'd12 : sum[3:0];
    expected_accept = matrix_equal && holonomy_valid &&
                      (canonical_phase < 4'd12) && (holonomy < 4'd12);

    assert(accept == expected_accept);
    if (expected_accept) begin
      assert(phase_out == expected);
      assert(collision == (holonomy != 4'd0));
      assert(phase_out < 4'd12);
    end else begin
      assert(phase_out == 4'd0);
      assert(collision == 1'b0);
    end
  end
endmodule
