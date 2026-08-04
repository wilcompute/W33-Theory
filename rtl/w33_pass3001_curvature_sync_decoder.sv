// Pass 3001: optimal 12-tick four-slot curvature synchronizer.
module w33_pass3001_curvature_sync_decoder(
  input  logic [23:0] rx_symbols,
  output logic [3:0]  phase,
  output logic [3:0]  distance,
  output logic        valid_unique
);
  integer p, i;
  logic [3:0] d;
  logic [3:0] best;
  logic tie;

  function automatic logic [1:0] base_symbol(input integer idx);
    begin
      case (idx)
        0: base_symbol=2'd1;  1: base_symbol=2'd0;
        2: base_symbol=2'd2;  3: base_symbol=2'd3;
        4: base_symbol=2'd3;  5: base_symbol=2'd2;
        6: base_symbol=2'd0;  7: base_symbol=2'd0;
        8: base_symbol=2'd1;  9: base_symbol=2'd1;
       10: base_symbol=2'd2; 11: base_symbol=2'd3;
       default: base_symbol=2'bxx;
      endcase
    end
  endfunction

  always_comb begin
    best=4'd15;
    phase=4'd0;
    tie=1'b0;
    for (p=0; p<12; p=p+1) begin
      d=4'd0;
      for (i=0; i<12; i=i+1)
        if (rx_symbols[2*i +: 2] != base_symbol((p+i)%12)) d=d+1'b1;
      if (d < best) begin
        best=d;
        phase=p[3:0];
        tie=1'b0;
      end else if (d == best) begin
        tie=1'b1;
      end
    end
    distance=best;
    valid_unique=(!tie && best<=4);
  end
endmodule
