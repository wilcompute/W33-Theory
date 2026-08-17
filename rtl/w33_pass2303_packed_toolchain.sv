// Pass 2303: packed, tool-friendly exact W(3,3) mixer and D24 action.
module w33_spread_mixer36_packed #(
    parameter integer W = 16,
    parameter integer OW = W + 4
) (
    input  wire signed [36*W-1:0]  x_flat,
    output reg  signed [36*OW-1:0] y_flat
);
    function [35:0] mask;
      input integer idx;
      begin
        case (idx)
          0: mask=36'h00a323cf6; 1: mask=36'h0094c5b6d; 2: mask=36'h00c81e79b; 3: mask=36'h6a0c4c0f6;
          4: mask=36'hb20a3216d; 5: mask=36'hc6078119b; 6: mask=36'h39306099b; 7: mask=36'h4d610856d;
          8: mask=36'h9550902f6; 9: mask=36'h950c4bd06; 10: mask=36'h4d0a35a85; 11: mask=36'h390786643;
          12: mask=36'hc63066623; 13: mask=36'hb2610da15; 14: mask=36'h6a5093c0e; 15: mask=36'h27a55228c;
          16: mask=36'h2792ac514; 17: mask=36'h8b9951451; 18: mask=36'h53a8a924a; 19: mask=36'h53c354922;
          20: mask=36'h8bc4aa8a1; 21: mask=36'h74ac90c31; 22: mask=36'hac9b08a2a; 23: mask=36'hd8c66061c;
          24: mask=36'hace435142; 25: mask=36'h74d24b0c1; 26: mask=36'hd8b986184; 27: mask=36'h007ff8007;
          28: mask=36'he001f8fc0; 29: mask=36'h1c01ff038; 30: mask=36'h1a36197a0; 31: mask=36'h165d24cc8;
          32: mask=36'h0e6ac2b50; 33: mask=36'hc1361e858; 34: mask=36'ha16ac54a8; 35: mask=36'h615d23330;
          default: mask=36'b0;
        endcase
      end
    endfunction
    integer i,j;
    reg signed [OW-1:0] acc;
    reg signed [W-1:0] xj;
    reg [35:0] rowmask;
    always @* begin
        y_flat={36*OW{1'b0}};
        rowmask=0;
        for(i=0;i<36;i=i+1) begin
            acc={OW{1'b0}};
            rowmask=mask(i);
            for(j=0;j<36;j=j+1) begin
                xj=x_flat[j*W +: W];
                if(rowmask[j]) acc=acc+{{(OW-W){xj[W-1]}},xj};
            end
            y_flat[i*OW +: OW]=acc;
        end
    end
endmodule

module w33_d24_action(
    input wire [3:0] phase_in,input wire conjugated_in,
    input wire [3:0] step12,input wire reflect,
    output reg [3:0] phase_out,output wire conjugated_out
);
    reg [4:0] tmp;
    always @* begin
<<<<<<< ours
        if(!conjugated_in) begin
            tmp={1'b0,phase_in}+{1'b0,step12};
            phase_out=(tmp>=5'd12)?tmp-5'd12:tmp[3:0];
        end else begin
            phase_out=(phase_in>=step12)?phase_in-step12:phase_in+4'd12-step12;
        end
=======
        if(!conjugated_in) begin tmp={1'b0,phase_in}+{1'b0,step12};phase_out=(tmp>=12)?tmp-12:tmp[3:0];end
        else phase_out=(phase_in>=step12)?phase_in-step12:phase_in+12-step12;
>>>>>>> theirs
    end
    assign conjugated_out=conjugated_in^reflect;
endmodule

module w33_single_j_action24(
    input wire [3:0] phase_in,input wire conjugated_in,
    input wire [1:0] step4,input wire [2:0] step6,input wire reflect,
    output wire [3:0] phase_out,output wire conjugated_out
);
    wire [5:0] raw=6'd3*step4+6'd2*step6;
    wire [3:0] delta12=(raw>=6'd12)?raw-6'd12:raw[3:0];
    w33_d24_action u(.phase_in(phase_in),.conjugated_in(conjugated_in),.step12(delta12),.reflect(reflect),.phase_out(phase_out),.conjugated_out(conjugated_out));
endmodule
