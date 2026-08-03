// Pass 2960: minimum-incidence [5,4,2]_3 factorization of the optimal 15-probe observer.
module w33_pass2960_spc15_factorized_encoder(
  input  logic [1:0] x0, x1, x2, x3,
  output logic [14:0] support_bits
);
  logic [1:0] parity;
  function automatic [1:0] add3(input logic [1:0] a, input logic [1:0] b);
    logic [2:0] s;
    begin
      s = a + b;
      case (s)
        3,6: add3 = 0;
        4:   add3 = 1;
        5:   add3 = 2;
        default: add3 = s[1:0];
      endcase
    end
  endfunction
  function automatic [2:0] support3(input logic [1:0] t);
    begin
      case (t)
        0: support3 = 3'b110; // b=0,1,2 -> 0,1,1
        1: support3 = 3'b011; //              1,1,0
        2: support3 = 3'b101; //              1,0,1
        default: support3 = 3'bxxx;
      endcase
    end
  endfunction
  always_comb begin
    parity = add3(add3(x0,x1),add3(x2,x3));
    support_bits[2:0]   = support3(x0);
    support_bits[5:3]   = support3(x1);
    support_bits[8:6]   = support3(x2);
    support_bits[11:9]  = support3(x3);
    support_bits[14:12] = support3(parity);
  end
endmodule
