`timescale 1ns/1ps
module w33_e6_cubic_tb;
  reg [53:0] x; wire [1:0] c;
  integer t,i,j,k,errs,n,seed; integer A[0:8],B[0:8],C[0:8]; integer want,tr,da,db,dc;
  w33_e6_cartan_cubic dut (.x_flat(x), .cubic(c));
  function integer d3(input integer m0,m1,m2,m3,m4,m5,m6,m7,m8);
    d3 = m0*(m4*m8-m5*m7) - m1*(m3*m8-m5*m6) + m2*(m3*m7-m4*m6);
  endfunction
  initial begin
    errs=0; n=0; seed=32'd424242;
    for (t=0;t<4000;t=t+1) begin
      for (i=0;i<9;i=i+1) begin
        A[i]=$unsigned($random(seed))%3; B[i]=$unsigned($random(seed))%3; C[i]=$unsigned($random(seed))%3;
      end
      for (i=0;i<9;i=i+1) begin
        x[i*2      +: 2] = A[i][1:0];
        x[(9+i)*2  +: 2] = B[i][1:0];
        x[(18+i)*2 +: 2] = C[i][1:0];
      end
      #1;
      da=d3(A[0],A[1],A[2],A[3],A[4],A[5],A[6],A[7],A[8]);
      db=d3(B[0],B[1],B[2],B[3],B[4],B[5],B[6],B[7],B[8]);
      dc=d3(C[0],C[1],C[2],C[3],C[4],C[5],C[6],C[7],C[8]);
      tr=0;
      for (i=0;i<3;i=i+1) for (j=0;j<3;j=j+1) for (k=0;k<3;k=k+1)
        tr = tr + A[i*3+j]*B[j*3+k]*C[k*3+i];
      want = da+db+dc-tr; want = ((want%3)+3)%3;
      n=n+1;
      if (c !== want[1:0]) begin
        errs=errs+1;
        if (errs<4) $display("FAIL t=%0d got %0d want %0d", t, c, want);
      end
    end
    $display("Pass 2660 E6 Cartan cubic: %0d random 27-trit vectors, %0d errors", n, errs);
    if (errs==0) $display("PASS  det A + det B + det C - tr(ABC) over F3");
    $finish;
  end
endmodule
