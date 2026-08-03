// Pass 2951: order-four isodual map on eight ternary coordinates.
// Each trit is encoded 0,1,2; negation maps 1<->2 and fixes 0.
module w33_pass2951_isodual_quarter_turn(
 input logic [15:0] in_trits,
 output logic [15:0] out_trits
);
function automatic [1:0] neg3(input [1:0] x);
 case(x) 2'd0:neg3=0;2'd1:neg3=2;2'd2:neg3=1;default:neg3=3;endcase
endfunction
logic [1:0] a[0:7],b[0:7];integer i;
always_comb begin
 for(i=0;i<8;i=i+1)a[i]=in_trits[2*i +: 2];
 // old->new permutation [1,0,3,2,6,7,4,5], signs [+,−,−,+,+,+,−,−]
 b[1]=a[0]; b[0]=neg3(a[1]);
 b[3]=neg3(a[2]); b[2]=a[3];
 b[6]=a[4]; b[7]=a[5];
 b[4]=neg3(a[6]); b[5]=neg3(a[7]);
 for(i=0;i<8;i=i+1)out_trits[2*i +: 2]=b[i];
end
endmodule
