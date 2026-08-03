// Pass 2796 -- minimal exact affine frame engine.
//
// The public Holonet ISA remains unchanged.  This is the compressed frame micro-engine
// underneath it.  Its four operations are enough to generate ASp(4,3):
//
//   00 F_p       (xp,zp) -> (-zp,xp)
//   01 CX_p->f   zp -> zp-zf, xf -> xf+xp
//   10 CX_f->p   xp -> xp+xf, zf -> zf-zp
//   11 Z_p       zp -> zp+1
//
// The first three generate all 51,840 elements of Sp(4,3); conjugating the one nonzero
// translation Z_p by that group spans all 81 translations.  Z_f/register_select is not
// required in this micro-engine.
`timescale 1ns/1ps

module w33_pass2796_minimal_frame_unit (
    input  wire       clk,
    input  wire       rst,
    input  wire       load,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,
    input  wire       valid,
    input  wire [1:0] micro_op,
    output reg  [1:0] xp, zp, xf, zf
);
    function automatic [1:0] clamp3(input [1:0] value);
        clamp3 = (value == 2'd3) ? 2'd0 : value;
    endfunction
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] sum;
        begin
            sum = a + b;
            add3 = (sum >= 3) ? sum - 3 : sum[1:0];
        end
    endfunction
    function automatic [1:0] neg3(input [1:0] value);
        neg3 = (value == 0) ? 0 : (value == 1) ? 2 : 1;
    endfunction
    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        sub3 = add3(a, neg3(b));
    endfunction

    reg [1:0] nxp, nzp, nxf, nzf;
    always_comb begin
        nxp = xp; nzp = zp; nxf = xf; nzf = zf;
        case (micro_op)
            2'd0: begin nxp = neg3(zp); nzp = xp; end
            2'd1: begin nzp = sub3(zp, zf); nxf = add3(xf, xp); end
            2'd2: begin nxp = add3(xp, xf); nzf = sub3(zf, zp); end
            2'd3: begin nzp = add3(zp, 2'd1); end
        endcase
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            xp <= 0; zp <= 0; xf <= 0; zf <= 0;
        end else if (load) begin
            xp <= clamp3(xp_in); zp <= clamp3(zp_in);
            xf <= clamp3(xf_in); zf <= clamp3(zf_in);
        end else if (valid) begin
            xp <= nxp; zp <= nzp; xf <= nxf; zf <= nzf;
        end
    end
endmodule
