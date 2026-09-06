`default_nettype none

// Pass 7310 universal arithmetic check.  Inputs are unconstrained 12-bit words.
// The optimized Mersenne-fold circuit must agree with both the signed integer
// definition of x^T J y mod 7 and the deliberately naive '%' implementation.
module w33_pass7310_q7_pair_equiv_formal;
  (* anyconst *) reg [11:0] x;
  (* anyconst *) reg [11:0] y;
  wire valid,noncommute,naive_valid,naive_noncommute;
  wire [2:0] x0=x[2:0],x1=x[5:3],x2=x[8:6],x3=x[11:9];
  wire [2:0] y0=y[2:0],y1=y[5:3],y2=y[8:6],y3=y[11:9];
  integer reference;

  w33_pass7310_pauli_pair_q7 dut(
    .x(x),.y(y),.inputs_valid(valid),.noncommute(noncommute));
  w33_pass7310_pauli_pair_q7_naive naive(
    .x(x),.y(y),.inputs_valid(naive_valid),.noncommute(naive_noncommute));

  always @* begin
    reference=($signed({1'b0,x0})*$signed({1'b0,y1})
              -$signed({1'b0,x1})*$signed({1'b0,y0})
              +$signed({1'b0,x2})*$signed({1'b0,y3})
              -$signed({1'b0,x3})*$signed({1'b0,y2}))%7;
    if(reference<0)reference=reference+7;
    assert(noncommute==(valid&&reference!=0));
    assert({valid,noncommute}=={naive_valid,naive_noncommute});
    assert(!valid||(x0<7&&x1<7&&x2<7&&x3<7&&
                    y0<7&&y1<7&&y2<7&&y3<7&&|x&&|y));
  end
endmodule

`default_nettype wire
