`timescale 1ns/1ps
module w33_kraft_tb;
  reg [1:0] cls; reg chi; wire [2:0] w; wire [1:0] len;
  reg [2:0] bits; wire [1:0] dcls, dcons;
  integer errs, i, orbit[0:3], tot; real kraft, expw;
  w33_kraft_encode e (.cls(cls), .chiral_resolved(chi), .word(w), .len(len));
  w33_kraft_decode d (.bits(bits), .chiral_resolved(chi), .cls(dcls), .consumed(dcons));
  initial begin
    errs = 0;
    orbit[0]=648; orbit[1]=324; orbit[2]=162; orbit[3]=162;
    tot = orbit[0]+orbit[1]+orbit[2]+orbit[3];
    if (tot !== 1296) begin errs=errs+1; $display("FAIL orbit total %0d != 1296", tot); end

    // round-trip every class, chirality resolved
    chi = 1'b1;
    for (i = 0; i < 4; i = i + 1) begin
      cls = i[1:0]; #1;
      bits = w;            // left-aligned word feeds the decoder directly
      #1;
      if (dcls !== cls)  begin errs=errs+1; $display("FAIL rt cls %0d -> %0d", cls, dcls); end
      if (dcons !== len) begin errs=errs+1; $display("FAIL len cls %0d: enc %0d dec %0d", cls, len, dcons); end
    end

    // Kraft equality and expected word length, from the ORBIT SIZES
    kraft = 0.0; expw = 0.0;
    chi = 1'b1;
    for (i = 0; i < 4; i = i + 1) begin
      cls = i[1:0]; #1;
      kraft = kraft + 1.0 / (1 << len);
      expw  = expw  + (orbit[i] * 1.0 / 1296.0) * len;
    end
    $display("orbit sizes      : %0d %0d %0d %0d  (sum %0d)", orbit[0],orbit[1],orbit[2],orbit[3],tot);
    $display("Kraft sum        : %0.6f   (must be exactly 1)", kraft);
    $display("expected length  : %0.6f   (paper: 7/4 = 1.75)", expw);
    if (kraft != 1.0)  begin errs=errs+1; $display("FAIL Kraft != 1"); end
    if (expw != 1.75)  begin errs=errs+1; $display("FAIL expected length != 7/4"); end

    // W(E6) view: the two caches fuse to a 2-bit word
    chi = 1'b0;
    cls = 2'd2; #1; if (len !== 2'd2) begin errs=errs+1; $display("FAIL fused L len"); end
    cls = 2'd3; #1; if (len !== 2'd2) begin errs=errs+1; $display("FAIL fused R len"); end

    $display("Pass 2682 Kraft router: %0d errors", errs);
    if (errs == 0) $display("PASS  complete prefix code, Kraft = 1, expected length 7/4");
    $finish;
  end
endmodule
