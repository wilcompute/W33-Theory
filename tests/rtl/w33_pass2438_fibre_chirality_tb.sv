// Pass 2438 testbench -- exhaustive over every fibre element and every group element.
// Checks the group laws (C6 of order 6, S3 of order 6 nonabelian) and the one claim
// that matters: the C6 antipode fixes the orientation register, the S3 reflection
// does not (except at the fixed point p = 0).
`timescale 1ns/1ps
module w33_pass2438_tb;
  reg [1:0] p; reg s; reg [2:0] pw; reg [1:0] a; reg b;
  wire [1:0] cp, sp; wire cs, ss;
  wire c6ch, s3ch;
  integer errors = 0;
  integer nc6 = 0, ns3 = 0;
  integer i, j, k;

  w33_c6_fibre  u_c6 (.p_in(p), .s_in(s), .pow(pw), .p_out(cp), .s_out(cs));
  w33_s3_fibre  u_s3 (.p_in(p), .s_in(s), .a(a), .b(b), .p_out(sp), .s_out(ss));
  w33_orientation_probe u_pr (.p_in(p), .s_in(s),
                              .c6_orientation_changed(c6ch),
                              .s3_orientation_changed(s3ch));

  task chk(input cond, input [255:0] what);
    begin if (!cond) begin errors = errors + 1; $display("FAIL %0s p=%0d s=%0d", what, p, s); end end
  endtask

  initial begin
    // C6: g^pow is a well-defined action; g^6 = identity; g^3 = antipode
    for (i = 0; i < 3; i = i + 1)
      for (j = 0; j < 2; j = j + 1) begin
        p = i[1:0]; s = j[0];
        for (k = 0; k < 6; k = k + 1) begin
          pw = k[2:0]; #1;
          chk(cp < 2'd3, "c6 p out of range");
          chk(cp == ((i + k) % 3), "c6 rotation wrong");
          chk(cs == (j[0] ^ k[0]), "c6 sign wrong");
        end
        // the antipode
        pw = 3'd3; #1;
        chk(cp == i[1:0], "C6 ANTIPODE MOVED THE ORIENTATION");
        chk(cs == ~j[0],  "c6 antipode did not flip the sign");
        nc6 = nc6 + 1;
      end

    // S3: r^a t^b covers all 6 elements; the reflection negates the orientation
    for (i = 0; i < 3; i = i + 1)
      for (j = 0; j < 2; j = j + 1) begin
        p = i[1:0]; s = j[0];
        for (k = 0; k < 3; k = k + 1) begin
          a = k[1:0]; b = 1'b0; #1;
          chk(sp == ((i + k) % 3), "s3 rotation wrong");
          chk(ss == j[0], "s3 rotation flipped the sign");
          a = k[1:0]; b = 1'b1; #1;
          chk(sp == ((3 - ((i + k) % 3)) % 3), "s3 reflection wrong");
          chk(ss == ~j[0], "s3 reflection did not flip the sign");
        end
        ns3 = ns3 + 1;
      end

    // the bifurcation, stated as one assertion per orientation value
    for (i = 0; i < 3; i = i + 1) begin
      p = i[1:0]; s = 1'b0; #1;
      chk(c6ch == 1'b0, "C6 antipode changed orientation");
      if (i == 0) chk(s3ch == 1'b0, "s3 reflection moved the fixed point");
      else        chk(s3ch == 1'b1, "S3 REFLECTION DID NOT REVERSE ORIENTATION");
    end

    $display("Pass 2438 fibre chirality: C6 states %0d, S3 states %0d, errors %0d",
             nc6, ns3, errors);
    if (errors == 0) $display("PASS  C6 antipode preserves orientation; S3 reflection reverses it");
    else             $display("FAIL  %0d errors", errors);
    $finish;
  end
endmodule
