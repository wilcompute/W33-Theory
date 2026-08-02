`timescale 1ns/1ps
module w33_pass2303_tb;
    reg signed [36*4-1:0] x;
    wire signed [36*8-1:0] y1;
    wire signed [36*12-1:0] y2;
    w33_spread_mixer36_packed #(.W(4),.OW(8)) m1(.x_flat(x),.y_flat(y1));
    w33_spread_mixer36_packed #(.W(8),.OW(12)) m2(.x_flat(y1),.y_flat(y2));
    reg [3:0] phase;reg conj;reg [1:0] a;reg [2:0] b;reg reflect;
    wire [3:0] po;wire eo;
    w33_single_j_action24 ctl(.phase_in(phase),.conjugated_in(conj),.step4(a),.step6(b),.reflect(reflect),.phase_out(po),.conjugated_out(eo));
    integer i,j,aa,bb,total,rhs,delta,expected_phase;
    initial begin
        x=0;
        for(i=0;i<36;i=i+1) x[i*4 +: 4]=(i%16)-8;
        #1;total=0;
        for(i=0;i<36;i=i+1) total=total+$signed(x[i*4 +: 4]);
        for(i=0;i<36;i=i+1) begin
            rhs=9*$signed(x[i*4 +: 4])+6*total;
            if($signed(y2[i*12 +: 12])!==rhs) $fatal(1,"mixer identity lane %0d",i);
        end
        for(i=0;i<12;i=i+1) for(j=0;j<2;j=j+1) begin
          phase=i;conj=j;
          for(aa=0;aa<4;aa=aa+1) for(bb=0;bb<6;bb=bb+1) begin
            a=aa;b=bb;reflect=0;#1;delta=(3*aa+2*bb)%12;
            expected_phase=conj?(phase-delta+12)%12:(phase+delta)%12;
            if(po!==expected_phase||eo!==conj) $fatal(1,"phase rotation");
            reflect=1;#1;
            if(po!==expected_phase||eo!==(conj^1)) $fatal(1,"phase reflection");
          end
          a=2;b=3;reflect=0;#1;
          if(po!==phase||eo!==conj) $fatal(1,"kernel");
        end
        $display("PASS w33_pass2303_tb");$finish;
    end
endmodule
