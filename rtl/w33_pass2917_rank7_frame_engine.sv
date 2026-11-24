// Pass 2917 -- seven-bit rank-coded implementation of the four-operation frame engine.
//
// State code:
//   rank = 27*x_p + 9*z_p + 3*x_f + z_f,  0 <= rank <= 80.
//
// This stores all 81 frames in seven flip-flops, which is information-theoretically
// optimal.  It is deliberately measured against w33_pass2796_minimal_frame_engine.sv;
// fewer state bits do not imply fewer logic cells because decode/re-encode logic costs
// area.  The same load/opcode/output interface is retained for a fair harness.

`timescale 1ns/1ps

module w33_pass2917_rank7_frame_engine (
    input  wire       clk,
    input  wire       rst,
    input  wire       load,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,
    input  wire       valid,
    input  wire [1:0] opcode,
    output wire [1:0] xp, zp, xf, zf,
    output reg  [6:0] rank
);
    localparam [1:0] OP_FP    = 2'b00,
                     OP_CX_PF = 2'b01,
                     OP_CX_FP = 2'b10,
                     OP_ZP    = 2'b11;

    function automatic [1:0] clamp3(input [1:0] v);
        clamp3 = (v == 2'd3) ? 2'd0 : v;
    endfunction
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] sum;
        begin
            sum = a + b;
            add3 = (sum >= 3) ? sum - 3 : sum[1:0];
        end
    endfunction
    function automatic [1:0] neg3(input [1:0] v);
        neg3 = (v == 0) ? 0 : (v == 1) ? 2 : 1;
    endfunction
    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        sub3 = add3(a, neg3(b));
    endfunction
    function automatic [6:0] encode4(
        input [1:0] axp, input [1:0] azp,
        input [1:0] axf, input [1:0] azf
    );
        reg [8:0] total;
        begin
            total = axp * 7'd27 + azp * 7'd9 + axf * 7'd3 + azf;
            encode4 = total[6:0];
        end
    endfunction

    // Constant-radix decode without general division hardware.
    reg [6:0] rem27, rem9, rem3;
    reg [1:0] dxp, dzp, dxf, dzf;
    always_comb begin
        if (rank >= 7'd54) begin dxp = 2; rem27 = rank - 54; end
        else if (rank >= 7'd27) begin dxp = 1; rem27 = rank - 27; end
        else begin dxp = 0; rem27 = rank; end

        if (rem27 >= 7'd18) begin dzp = 2; rem9 = rem27 - 18; end
        else if (rem27 >= 7'd9) begin dzp = 1; rem9 = rem27 - 9; end
        else begin dzp = 0; rem9 = rem27; end

        if (rem9 >= 7'd6) begin dxf = 2; rem3 = rem9 - 6; end
        else if (rem9 >= 7'd3) begin dxf = 1; rem3 = rem9 - 3; end
        else begin dxf = 0; rem3 = rem9; end
        dzf = rem3[1:0];
    end

    assign xp = dxp;
    assign zp = dzp;
    assign xf = dxf;
    assign zf = dzf;

    reg [1:0] nxp, nzp, nxf, nzf;
    reg [6:0] next_rank;
    always_comb begin
        nxp = dxp; nzp = dzp; nxf = dxf; nzf = dzf;
        case (opcode)
            OP_FP:    begin nxp = neg3(dzp);      nzp = dxp;            end
            OP_CX_PF: begin nzp = sub3(dzp, dzf); nxf = add3(dxf, dxp); end
            OP_CX_FP: begin nxp = add3(dxp, dxf); nzf = sub3(dzf, dzp); end
            OP_ZP:    begin nzp = add3(dzp, 1);                         end
        endcase
        next_rank = encode4(nxp, nzp, nxf, nzf);
    end

    always_ff @(posedge clk) begin
        if (rst)
            rank <= 0;
        else if (load)
            rank <= encode4(clamp3(xp_in), clamp3(zp_in), clamp3(xf_in), clamp3(zf_in));
        else if (valid)
            rank <= next_rank;
    end
endmodule
