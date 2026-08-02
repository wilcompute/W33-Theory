module w33_pass2313_command_formal;
  (* anyconst *) reg [3:0] phase_in;
  (* anyconst *) reg conjugated_in;
  (* anyconst *) reg [1:0] step4;
  (* anyconst *) reg [2:0] step6;
  (* anyconst *) reg reflect;

  wire [3:0] phase_out;
  wire conjugated_out;
  wire [1:0] step4_duo = step4 + 2'd2;
  wire [2:0] step6_duo = (step6 >= 3) ? step6 - 3 : step6 + 3;
  wire [3:0] phase_out_duo;
  wire conjugated_out_duo;

  wire [5:0] raw = 6'd3*step4 + 6'd2*step6;
  wire [3:0] delta = (raw >= 12) ? raw - 12 : raw[3:0];
  wire [4:0] plus_tmp = {1'b0,phase_in}+{1'b0,delta};
  wire [3:0] plus_expected = (plus_tmp >= 12) ? plus_tmp - 12 : plus_tmp[3:0];
  wire [3:0] minus_expected = (phase_in >= delta) ? phase_in-delta : phase_in+12-delta;

  w33_single_j_action24 dut(
    .phase_in(phase_in), .conjugated_in(conjugated_in),
    .step4(step4), .step6(step6), .reflect(reflect),
    .phase_out(phase_out), .conjugated_out(conjugated_out)
  );
  w33_single_j_action24 dut_duo(
    .phase_in(phase_in), .conjugated_in(conjugated_in),
    .step4(step4_duo), .step6(step6_duo), .reflect(reflect),
    .phase_out(phase_out_duo), .conjugated_out(conjugated_out_duo)
  );

  always @* begin
    assume(phase_in < 12);
    assume(step6 < 6);
    assert(phase_out == (conjugated_in ? minus_expected : plus_expected));
    assert(conjugated_out == (conjugated_in ^ reflect));
    assert(phase_out_duo == phase_out);
    assert(conjugated_out_duo == conjugated_out);
  end
endmodule
