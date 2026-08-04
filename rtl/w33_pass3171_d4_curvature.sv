// Pass 3171: one-bit gauge-invariant D4 commutator syndrome.
// Label encoding 0..6 = r,r2,r3,s,rs,r2s,r3s.
module w33_pass3171_d4_curvature(
  input logic [2:0] left_label_i,input logic [2:0] right_label_i,
  output logic valid_o,output logic curvature_o
);
  logic [1:0] la,ra;logic lb,rb;
  always_comb begin
    valid_o=(left_label_i<7 && right_label_i<7);
    case(left_label_i)
      0:{la,lb}={2'd1,1'b0};1:{la,lb}={2'd2,1'b0};2:{la,lb}={2'd3,1'b0};
      3:{la,lb}={2'd0,1'b1};4:{la,lb}={2'd1,1'b1};5:{la,lb}={2'd2,1'b1};
      default:{la,lb}={2'd3,1'b1};endcase
    case(right_label_i)
      0:{ra,rb}={2'd1,1'b0};1:{ra,rb}={2'd2,1'b0};2:{ra,rb}={2'd3,1'b0};
      3:{ra,rb}={2'd0,1'b1};4:{ra,rb}={2'd1,1'b1};5:{ra,rb}={2'd2,1'b1};
      default:{ra,rb}={2'd3,1'b1};endcase
    curvature_o=valid_o & ((lb & ra[0]) ^ (rb & la[0]));
  end
endmodule
