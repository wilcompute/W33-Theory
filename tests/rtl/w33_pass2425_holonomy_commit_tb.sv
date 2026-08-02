`timescale 1ns/1ps
module w33_pass2425_holonomy_commit_tb;
  logic [3:0] canonical_phase;
  logic [3:0] holonomy;
  logic       matrix_equal;
  logic       holonomy_valid;
  logic [3:0] phase_out;
  logic       collision;
  logic       accept;

  integer p, h, expected, cases;

  w33_pass2425_holonomy_commit dut(
    .canonical_phase(canonical_phase),
    .holonomy(holonomy),
    .matrix_equal(matrix_equal),
    .holonomy_valid(holonomy_valid),
    .phase_out(phase_out),
    .collision(collision),
    .accept(accept)
  );

  task check_reject;
    input [3:0] p0;
    input [3:0] h0;
    input me0;
    input hv0;
    begin
      canonical_phase = p0;
      holonomy = h0;
      matrix_equal = me0;
      holonomy_valid = hv0;
      #1;
      if (accept !== 1'b0 || phase_out !== 4'd0 || collision !== 1'b0) begin
        $display("FAIL reject p=%0d h=%0d me=%0d hv=%0d accept=%0d out=%0d collision=%0d",
                 p0, h0, me0, hv0, accept, phase_out, collision);
        $fatal(1);
      end
    end
  endtask

  initial begin
    cases = 0;
    canonical_phase = 0;
    holonomy = 0;
    matrix_equal = 0;
    holonomy_valid = 0;
    #1;

    for (p = 0; p < 12; p = p + 1) begin
      for (h = 0; h < 12; h = h + 1) begin
        canonical_phase = p[3:0];
        holonomy = h[3:0];
        matrix_equal = 1'b1;
        holonomy_valid = 1'b1;
        #1;
        expected = (p + h) % 12;
        if (accept !== 1'b1 || phase_out !== expected[3:0]) begin
          $display("FAIL valid p=%0d h=%0d got=%0d expected=%0d accept=%0d",
                   p, h, phase_out, expected, accept);
          $fatal(1);
        end
        if (collision !== (h != 0)) begin
          $display("FAIL collision p=%0d h=%0d collision=%0d", p, h, collision);
          $fatal(1);
        end
        cases = cases + 1;
      end
    end

    check_reject(4'd3, 4'd4, 1'b0, 1'b1);
    check_reject(4'd3, 4'd4, 1'b1, 1'b0);
    check_reject(4'd12, 4'd0, 1'b1, 1'b1);
    check_reject(4'd0, 4'd12, 1'b1, 1'b1);
    check_reject(4'd15, 4'd15, 1'b1, 1'b1);

    if (cases != 144) $fatal(1, "wrong valid case count %0d", cases);
    $display("PASS2425 exhaustive holonomy commit valid_cases=%0d reject_cases=5", cases);
    $finish;
  end
endmodule
