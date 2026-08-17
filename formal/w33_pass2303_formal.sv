// Pass 2303 formal properties for the exact mixer and D24 controller.
module w33_mixer_formal;
    (* anyconst *) reg signed [36*4-1:0] x_flat;
    wire signed [36*8-1:0] y1;
    wire signed [36*12-1:0] y2;
    w33_spread_mixer36_packed #(.W(4),.OW(8)) m1(.x_flat(x_flat),.y_flat(y1));
    w33_spread_mixer36_packed #(.W(8),.OW(12)) m2(.x_flat(y1),.y_flat(y2));
    integer i,j;
    reg signed [9:0] total;
    reg signed [11:0] rhs;
    always @* begin
        total=0;
        for(j=0;j<36;j=j+1) total=total+$signed(x_flat[j*4 +: 4]);
        for(i=0;i<36;i=i+1) begin
            rhs=9*$signed(x_flat[i*4 +: 4])+6*$signed(total);
            assert($signed(y2[i*12 +: 12])==rhs);
        end
    end
endmodule

module w33_phase_formal;
    (* anyconst *) reg [3:0] phase0;
    (* anyconst *) reg conj0;
    (* anyconst *) reg [3:0] u;
    (* anyconst *) reg fu;
    (* anyconst *) reg [3:0] v;
    (* anyconst *) reg fv;
    wire [3:0] p1,p2,pc;wire e1,e2,ec;
    reg [4:0] tmp;reg [3:0] uv;
    w33_d24_action a1(.phase_in(phase0),.conjugated_in(conj0),.step12(u),.reflect(fu),.phase_out(p1),.conjugated_out(e1));
    w33_d24_action a2(.phase_in(p1),.conjugated_in(e1),.step12(v),.reflect(fv),.phase_out(p2),.conjugated_out(e2));
    w33_d24_action ac(.phase_in(phase0),.conjugated_in(conj0),.step12(uv),.reflect(fu^fv),.phase_out(pc),.conjugated_out(ec));
    wire [3:0] pk;wire ek;
    w33_single_j_action24 kernel(.phase_in(phase0),.conjugated_in(conj0),.step4(2'd2),.step6(3'd3),.reflect(1'b0),.phase_out(pk),.conjugated_out(ek));
    always @* begin
<<<<<<< ours
        assume(phase0<4'd12);assume(u<4'd12);assume(v<4'd12);
        if(!fu) begin
            tmp={1'b0,u}+{1'b0,v};
            uv=(tmp>=5'd12)?tmp-5'd12:tmp[3:0];
        end else begin
            uv=(u>=v)?u-v:u+4'd12-v;
        end
=======
        assume(phase0<12);assume(u<12);assume(v<12);
        if(!fu) begin tmp={1'b0,u}+{1'b0,v};uv=(tmp>=12)?tmp-12:tmp[3:0];end
        else uv=(u>=v)?u-v:u+12-v;
>>>>>>> theirs
        assert(p2==pc);assert(e2==ec);
        assert(pk==phase0);assert(ek==conj0);
    end
endmodule
