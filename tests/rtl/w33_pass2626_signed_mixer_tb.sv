// Pass 2626 -- the testbench that would have caught the Pass 2612 sign bug.
//
// The original bench checked only basis vectors e0 and e5, whose entries are 0 and +1,
// so it never drove a negative lane and never exercised the unsigned-ternary path.
// This one sweeps signed vectors and checks A^2 = 9I + 6J directly.
`timescale 1ns/1ps
module w33_pass2626_signed_tb;
  localparam W = 4, M = 12, O = 20;
  reg  signed [36*W-1:0] x;
  wire signed [36*M-1:0] y1;
  wire signed [36*O-1:0] y2;

  w33_mix_core #(.W(W), .OW(M)) a1 (.x_flat(x),  .y_flat(y1));
  w33_mix_core #(.W(M), .OW(O)) a2 (.x_flat(y1), .y_flat(y2));

  integer i, t, seed, errors, checked;
  reg signed [O-1:0] xs, want;

  task check_A2;
    begin
      xs = 0;
      for (i = 0; i < 36; i = i + 1) xs = xs + $signed(x[i*W +: W]);
      for (i = 0; i < 36; i = i + 1) begin
        want = 9 * $signed(x[i*W +: W]) + 6 * xs;
        checked = checked + 1;
        if ($signed(y2[i*O +: O]) !== want) begin
          errors = errors + 1;
          if (errors < 6)
            $display("FAIL lane %0d: got %0d want %0d (sum=%0d)",
                     i, $signed(y2[i*O +: O]), want, xs);
        end
      end
    end
  endtask

  initial begin
    errors = 0; checked = 0; seed = 32'd20260802;

    // 1. every NEGATIVE basis vector -- the case the old bench omitted
    for (t = 0; t < 36; t = t + 1) begin
      x = 0; x[t*W +: W] = -4'sd1; #1; check_A2;
    end

    // 2. every positive basis vector, for symmetry
    for (t = 0; t < 36; t = t + 1) begin
      x = 0; x[t*W +: W] = 4'sd1; #1; check_A2;
    end

    // 3. all-minus-one: the extreme mean-nonzero vector
    x = 0; for (i = 0; i < 36; i = i + 1) x[i*W +: W] = -4'sd1; #1; check_A2;

    // 4. mean-zero vectors, where A/3 must be an involution
    for (t = 0; t < 18; t = t + 1) begin
      x = 0;
      x[(2*t)*W     +: W] =  4'sd1;
      x[(2*t+1)*W   +: W] = -4'sd1;
      #1; check_A2;
    end

    // 5. random signed vectors in [-3, 3]
    for (t = 0; t < 300; t = t + 1) begin
      for (i = 0; i < 36; i = i + 1)
        x[i*W +: W] = ($random(seed) % 7) - 3;
      #1; check_A2;
    end

    $display("Pass 2626 signed mixer: %0d lane checks, %0d errors", checked, errors);
    if (errors == 0) $display("PASS  A^2 = 9I + 6J holds on signed inputs");
    else             $display("FAIL  %0d mismatches", errors);
    $finish;
  end
endmodule
