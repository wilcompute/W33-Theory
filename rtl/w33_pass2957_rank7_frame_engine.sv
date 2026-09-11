// Pass 2957 -- seven-bit radix-three candidate for the four-operation frame engine.
// The 7-bit storage theorem is exact; replacement of the measured 43-LC arithmetic
// engine is forbidden until the same workflow observes synthesis and place-and-route.

`timescale 1ns/1ps
module w33_pass2957_rank7_frame_engine (
    input  wire clk, rst, load, valid,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,
    input  wire [1:0] opcode,
    output wire [1:0] xp, zp, xf, zf,
    output reg  [6:0] rank
);
    function automatic [1:0] clamp3(input [1:0] value);
        clamp3 = value == 2'd3 ? 2'd0 : value;
    endfunction
    function automatic [1:0] add3(input [1:0] left, input [1:0] right);
        reg [2:0] total;
        begin total=left+right; add3=(total>=3)?total-3:total[1:0]; end
    endfunction
    function automatic [1:0] neg3(input [1:0] value);
        neg3 = value==0 ? 0 : value==1 ? 2 : 1;
    endfunction
    function automatic [1:0] sub3(input [1:0] left, input [1:0] right);
        sub3 = add3(left,neg3(right));
    endfunction
    function automatic [6:0] encode4(input [1:0] axp,azp,axf,azf);
        reg [8:0] total;
        begin total=axp*27+azp*9+axf*3+azf; encode4=total[6:0]; end
    endfunction

    reg [6:0] rem27,rem9,rem3;
    reg [1:0] dxp,dzp,dxf,dzf;
    always_comb begin
        if(rank>=54) begin dxp=2;rem27=rank-54;end
        else if(rank>=27) begin dxp=1;rem27=rank-27;end
        else begin dxp=0;rem27=rank;end
        if(rem27>=18) begin dzp=2;rem9=rem27-18;end
        else if(rem27>=9) begin dzp=1;rem9=rem27-9;end
        else begin dzp=0;rem9=rem27;end
        if(rem9>=6) begin dxf=2;rem3=rem9-6;end
        else if(rem9>=3) begin dxf=1;rem3=rem9-3;end
        else begin dxf=0;rem3=rem9;end
        dzf=rem3[1:0];
    end
    assign xp=dxp;assign zp=dzp;assign xf=dxf;assign zf=dzf;

    reg [1:0] nxp,nzp,nxf,nzf;
    reg [6:0] next_rank;
    always_comb begin
        nxp=dxp;nzp=dzp;nxf=dxf;nzf=dzf;
        case(opcode)
          2'b00:begin nxp=neg3(dzp);nzp=dxp;end
          2'b01:begin nzp=sub3(dzp,dzf);nxf=add3(dxf,dxp);end
          2'b10:begin nxp=add3(dxp,dxf);nzf=sub3(dzf,dzp);end
          2'b11:begin nzp=add3(dzp,1);end
        endcase
        next_rank=encode4(nxp,nzp,nxf,nzf);
    end
    always_ff @(posedge clk) begin
        if(rst) rank<=0;
        else if(load) rank<=encode4(clamp3(xp_in),clamp3(zp_in),clamp3(xf_in),clamp3(zf_in));
        else if(valid) rank<=next_rank;
    end
endmodule
