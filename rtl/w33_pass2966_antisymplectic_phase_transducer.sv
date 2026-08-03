// Pass 2966: anti-symplectic K and sigma=x^T J p over F3.
module w33_pass2966_antisymplectic_phase_transducer(
  input  logic [1:0] x0,x1,x2,x3,
  input  logic [1:0] p0,p1,p2,p3,
  output logic [1:0] sigma,
  output logic       commute,
  output logic [2:0] support_triplet,
  output logic [1:0] kx0,kx1,kx2,kx3,
  output logic [1:0] kp0,kp1,kp2,kp3
);
  integer raw;
  function automatic [1:0] mod3(input integer v);
    integer r;
    begin r = v % 3; if (r < 0) r = r + 3; mod3 = r[1:0]; end
  endfunction
  function automatic [2:0] support3(input logic [1:0] t);
    begin case(t) 0:support3=3'b110; 1:support3=3'b011; 2:support3=3'b101; default:support3=3'bxxx; endcase end
  endfunction
  always_comb begin
    raw = x0*p1 - x1*p0 + x2*p3 - x3*p2;
    sigma = mod3(raw);
    commute = (sigma == 0);
    support_triplet = support3(sigma);
    kx0=x1; kx1=x0; kx2=x3; kx3=x2;
    kp0=p1; kp1=p0; kp2=p3; kp3=p2;
  end
endmodule
