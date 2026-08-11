`timescale 1ns/1ps
module tb_w33_pass4944_port_selector45;
    reg [1:0] i,r; reg b; wire [1:0] o;
    reg [89:0] pi,rr; reg [44:0] bb; wire [89:0] po;
    integer ii,jj,kk,lane,expect;
    w33_agl13_port_selector one(.port_i(i),.rotation_r(r),.reflect_b(b),.port_o(o));
    w33_port_selector45 all45(.port_i_flat(pi),.rotation_flat(rr),.reflect_flat(bb),.port_o_flat(po));
    initial begin
        // Exhaust every one of the 18 valid AGL(1,3) input/state combinations.
        for (kk=0;kk<2;kk=kk+1) begin
            for (jj=0;jj<3;jj=jj+1) begin
                for (ii=0;ii<3;ii=ii+1) begin
                    b=kk; r=jj; i=ii; #1;
                    expect = (((kk ? (3-ii)%3 : ii) + jj) % 3);
                    if (o !== expect[1:0]) begin
                        $display("FAIL one i=%0d r=%0d b=%0d got=%0d exp=%0d",ii,jj,kk,o,expect);$fatal(1);
                    end
                end
            end
        end
        // Drive all 45 lanes with a deterministic mixture and check every lane.
        pi='0;rr='0;bb='0;
        for (lane=0;lane<45;lane=lane+1) begin
            pi[2*lane +: 2]=lane%3;
            rr[2*lane +: 2]=(lane/3)%3;
            bb[lane]=(lane/9)%2;
        end
        #1;
        for (lane=0;lane<45;lane=lane+1) begin
            ii=lane%3;jj=(lane/3)%3;kk=(lane/9)%2;
            expect=(((kk ? (3-ii)%3 : ii)+jj)%3);
            if (po[2*lane +: 2] !== expect[1:0]) begin
                $display("FAIL lane=%0d got=%0d exp=%0d",lane,po[2*lane +: 2],expect);$fatal(1);
            end
        end
        $display("PASS Pass4944 exhaustive one-selector 18/18 plus 45-lane mixed vector");
        $finish;
    end
endmodule
