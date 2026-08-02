`timescale 1ns/1ps
module w33_pass2313_tb;
  reg [3:0] phase_in;
  reg conjugated_in;
  reg [1:0] step4;
  reg [2:0] step6;
  reg reflect;
  wire [3:0] phase_out;
  wire conjugated_out;

  w33_single_j_action24 dut(
    .phase_in(phase_in), .conjugated_in(conjugated_in),
    .step4(step4), .step6(step6), .reflect(reflect),
    .phase_out(phase_out), .conjugated_out(conjugated_out)
  );

  integer p,c,a,b,r;
  integer raw,delta,expected_phase,cases;
  reg [3:0] first_phase;
  reg first_conj;
  reg [1:0] duo4;
  reg [2:0] duo6;

  initial begin
    cases=0;
    phase_in=0; conjugated_in=0; step4=0; step6=0; reflect=0;
    #1;
    for(p=0;p<12;p=p+1) begin
      for(c=0;c<2;c=c+1) begin
        for(a=0;a<4;a=a+1) begin
          for(b=0;b<6;b=b+1) begin
            for(r=0;r<2;r=r+1) begin
              phase_in=p[3:0]; conjugated_in=c[0]; step4=a[1:0]; step6=b[2:0]; reflect=r[0];
              #1;
              raw=3*a+2*b;
              delta=raw%12;
              if(c==0) expected_phase=(p+delta)%12;
              else expected_phase=(p+12-delta)%12;
              if(phase_out !== expected_phase[3:0]) begin
                $display("FAIL phase p=%0d c=%0d a=%0d b=%0d r=%0d got=%0d exp=%0d",p,c,a,b,r,phase_out,expected_phase);
                $fatal(1);
              end
              if(conjugated_out !== (c^r)) begin
                $display("FAIL conjugation p=%0d c=%0d a=%0d b=%0d r=%0d",p,c,a,b,r);
                $fatal(1);
              end
              first_phase=phase_out; first_conj=conjugated_out;
              duo4=(a+2)%4;
              duo6=(b+3)%6;
              step4=duo4; step6=duo6;
              #1;
              if(phase_out !== first_phase || conjugated_out !== first_conj) begin
                $display("FAIL duo invariance p=%0d c=%0d a=%0d b=%0d r=%0d",p,c,a,b,r);
                $fatal(1);
              end
              cases=cases+1;
            end
          end
        end
      end
    end
    if(cases != 1152) $fatal(1,"wrong case count %0d",cases);
    $display("PASS2313 exhaustive command oracle cases=%0d",cases);
    $finish;
  end
endmodule
