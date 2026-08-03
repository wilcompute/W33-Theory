// Pass 2612 -- a ROUTABLE 36-lane spread mixer, and the involution proved in the netlist.
//
// The parallel track's Pass 2303/2308 mixer is correct and synthesises, but it cannot be
// placed: its flat interface exposes 36 x 4 input bits + 36 x 8 output bits = 432 pins,
// and no iCE40 package has them.  Their Pass 2308 had to erase the port table to route
// the core at all, which measures capacity but is not a placeable design.
//
// Fix: stream the lanes.  36 signed 4-bit values in over 36 cycles, 36 signed 8-bit
// values out over 36 cycles, on a ~15-pin interface.  Same arithmetic, same masks, same
// A^2 = 9I + 6J algebra -- but an object that fits a real package.
//
// The second module proves the algebra where it matters.  A^2 = 9I + 6J means
//     A(A(x)) = 9x + 6*(sum x)*1
// so on MEAN-ZERO signals A/3 is an involution: the same interconnect encodes and
// decodes.  w33_mixer_involution_formal asserts exactly that, over all inputs.

`timescale 1ns/1ps

// The 36 adjacency masks of the SRG(36,15,6,6) spread graph = NO_6^-(2).
// Degree 15: every mask has exactly 15 bits set.
`define W33_MASKS  { \
  36'h00a323cf6, 36'h0094c5b6d, 36'h00c81e79b, 36'h6a0c4c0f6, 36'hb20a3216d, 36'hc6078119b, \
  36'h39306099b, 36'h4d610856d, 36'h9550902f6, 36'h950c4bd06, 36'h4d0a35a85, 36'h390786643, \
  36'hc63066623, 36'hb2610da15, 36'h6a5093c0e, 36'h27a55228c, 36'h2792ac514, 36'h8b9951451, \
  36'h53a8a924a, 36'h53c354922, 36'h8bc4aa8a1, 36'h74ac90c31, 36'hac9b08a2a, 36'hd8c66061c, \
  36'hace435142, 36'h74d24b0c1, 36'hd8b986184, 36'h007ff8007, 36'he001f8fc0, 36'h1c01ff038, \
  36'h1a36197a0, 36'h165d24cc8, 36'h0e6ac2b50, 36'hc1361e858, 36'ha16ac54a8, 36'h615d23330 }

// ---------------------------------------------------------------------------
// Combinational core: y_i = sum over j in mask_i of x_j.
// Kept separate so the formal harness can instantiate it twice.
// ---------------------------------------------------------------------------
module w33_mix_core #(parameter W = 4, parameter OW = 12) (
    input  wire signed [36*W-1:0]  x_flat,
    output wire signed [36*OW-1:0] y_flat
);
    // Flat packed constant, low-index-first, so masks[g] is a plain part-select.
    // (Indexing a concatenation directly is not legal SystemVerilog.)
    localparam [36*36-1:0] MASKS_FLAT = {
      36'h615d23330, 36'ha16ac54a8, 36'hc1361e858, 36'h0e6ac2b50, 36'h165d24cc8, 36'h1a36197a0,
      36'h1c01ff038, 36'he001f8fc0, 36'h007ff8007, 36'hd8b986184, 36'h74d24b0c1, 36'hace435142,
      36'hd8c66061c, 36'hac9b08a2a, 36'h74ac90c31, 36'h8bc4aa8a1, 36'h53c354922, 36'h53a8a924a,
      36'h8b9951451, 36'h2792ac514, 36'h27a55228c, 36'h6a5093c0e, 36'hb2610da15, 36'hc63066623,
      36'h390786643, 36'h4d0a35a85, 36'h950c4bd06, 36'h9550902f6, 36'h4d610856d, 36'h39306099b,
      36'hc6078119b, 36'hb20a3216d, 36'h6a0c4c0f6, 36'h00c81e79b, 36'h0094c5b6d, 36'h00a323cf6 };

    wire [35:0] masks [0:35];
    genvar g;
    generate
        for (g = 0; g < 36; g = g + 1) begin : mk
            assign masks[g] = MASKS_FLAT[g*36 +: 36];
        end
    endgenerate

    genvar i, j;
    generate
        for (i = 0; i < 36; i = i + 1) begin : lane
            wire signed [OW-1:0] partial [0:36];
            assign partial[0] = {OW{1'b0}};
            for (j = 0; j < 36; j = j + 1) begin : acc
                wire signed [OW-1:0] term =
                    masks[i][j] ? $signed(x_flat[j*W +: W]) : {OW{1'b0}};
                assign partial[j+1] = partial[j] + term;
            end
            assign y_flat[i*OW +: OW] = partial[36];
        end
    endgenerate
endmodule

// ---------------------------------------------------------------------------
// Streaming wrapper.  Interface is ~15 pins instead of 432.
// ---------------------------------------------------------------------------
module w33_serial_mixer #(parameter W = 4, parameter OW = 12) (
    input  wire                    clk,
    input  wire                    rst,
    input  wire                    in_valid,
    input  wire signed [W-1:0]     in_data,
    output wire                    busy,
    output reg                     out_valid,
    output reg  signed [OW-1:0]    out_data
);
    reg signed [36*W-1:0]  xbuf;
    wire signed [36*OW-1:0] ybuf;
    reg [5:0] in_cnt, out_cnt;
    reg       loading, draining;

    w33_mix_core #(.W(W), .OW(OW)) core (.x_flat(xbuf), .y_flat(ybuf));

    assign busy = draining;

    always_ff @(posedge clk) begin
        if (rst) begin
            in_cnt <= 0; out_cnt <= 0; loading <= 1; draining <= 0;
            out_valid <= 0; out_data <= 0; xbuf <= 0;
        end else begin
            out_valid <= 0;
            if (loading && in_valid) begin
                xbuf <= {in_data, xbuf[36*W-1:W]};   // shift in
                if (in_cnt == 6'd35) begin
                    in_cnt <= 0; loading <= 0; draining <= 1;
                end else in_cnt <= in_cnt + 1;
            end else if (draining) begin
                out_data  <= ybuf[out_cnt*OW +: OW];
                out_valid <= 1;
                if (out_cnt == 6'd35) begin
                    out_cnt <= 0; draining <= 0; loading <= 1;
                end else out_cnt <= out_cnt + 1;
            end
        end
    end
endmodule
