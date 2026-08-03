// Pass 2691 -- exact multiplier-free digital form of the W(3,3) incidence transceiver.
//
// The manuscript's real operator is T = N - J/10 with T^T T = 6 E_24.
// Hardware carries the exact integer scale S = 10T = 10N - J:
//
//   y_i = 10 * sum_{j incident to i} x_j - sum_j x_j
//       = (local4 << 3) + (local4 << 1) - global40.
//
// Every mask has exactly four taps.  There are no general multipliers.
// REVERSE=0 maps point lanes to line lanes; REVERSE=1 maps line lanes to point lanes.
// OW=W+7 is a conservative signed width because every row has l1 norm 72.
//
// This is a digital fixed-point reference.  It does not implement the optical 1/sqrt(6)
// amplitude normalization, detector calibration, or loss model.
`timescale 1ns/1ps

module w33_pass2691_incidence_core #(
    parameter integer W = 8,
    parameter integer OW = W + 7,
    parameter bit REVERSE = 1'b0
) (
    input  wire signed [40*W-1:0]  in_flat,
    output wire signed [40*OW-1:0] out_flat
);
    localparam [40*40-1:0] FORWARD_MASKS = {
      40'h0084201000, 40'h2000841000, 40'h0420009000, 40'h0102200800,
      40'h4000440800, 40'h0810008800, 40'h0208200400, 40'h8001040400,
      40'h1040008400, 40'h1000500200, 40'h0210020200, 40'h8002004200,
      40'h0401100100, 40'h00c0020100, 40'h2008004100, 40'h0800900080,
      40'h0120020080, 40'h4004004080, 40'h4040080040, 40'h0808010040,
      40'h0101002040, 40'h8020080020, 40'h1004010020, 40'h0200802020,
      40'h2010080010, 40'h0402010010, 40'h0080402010, 40'h0015000008,
      40'h0042800008, 40'h0028400008, 40'h4600000004, 40'h3100000004,
      40'h8880000004, 40'h0000001242, 40'h0000000922, 40'h0000000492,
      40'h0000380001, 40'h0000070001, 40'h000000e001, 40'h000000000f };
    localparam [40*40-1:0] REVERSE_MASKS = {
      40'h0110040080, 40'h0800600200, 40'h4002008100, 40'h00c0020100,
      40'h0401100080, 40'h2008004200, 40'h0220010200, 40'h1000880100,
      40'h8004002080, 40'h0084200800, 40'h2000840400, 40'h0420009000,
      40'h0202100400, 40'h8000421000, 40'h1010004800, 40'h0108081000,
      40'h4001010800, 40'h0840002400, 40'h9200000008, 40'h0049000008,
      40'h0000248008, 40'h4900000004, 40'h0024800004, 40'h0000124004,
      40'h2480000002, 40'h0012400002, 40'h0000092002, 40'he000000040,
      40'h1c00000020, 40'h0380000010, 40'h0070000040, 40'h000e000020,
      40'h0001c00010, 40'h0000380040, 40'h0000070020, 40'h000000e010,
      40'h0000001c01, 40'h0000000381, 40'h0000000071, 40'h000000000f };

    wire signed [OW-1:0] global_sum [0:40];
    assign global_sum[0] = {OW{1'b0}};

    genvar g;
    generate
        for (g = 0; g < 40; g = g + 1) begin : global_acc
            wire signed [W-1:0]  xw   = $signed(in_flat[g*W +: W]);
            wire signed [OW-1:0] xext = {{(OW-W){xw[W-1]}}, xw};
            assign global_sum[g+1] = global_sum[g] + xext;
        end
    endgenerate

    genvar i, j;
    generate
        for (i = 0; i < 40; i = i + 1) begin : lane
            wire [39:0] forward_mask = FORWARD_MASKS[i*40 +: 40];
            wire [39:0] reverse_mask = REVERSE_MASKS[i*40 +: 40];
            wire [39:0] mask = REVERSE ? reverse_mask : forward_mask;

            wire signed [OW-1:0] local_sum [0:40];
            assign local_sum[0] = {OW{1'b0}};

            for (j = 0; j < 40; j = j + 1) begin : local_acc
                wire signed [W-1:0]  xw   = $signed(in_flat[j*W +: W]);
                wire signed [OW-1:0] xext = {{(OW-W){xw[W-1]}}, xw};
                wire signed [OW-1:0] zero = {OW{1'b0}};
                wire signed [OW-1:0] term = mask[j] ? xext : zero;
                assign local_sum[j+1] = local_sum[j] + term;
            end

            wire signed [OW-1:0] local_x8  = local_sum[40] <<< 3;
            wire signed [OW-1:0] local_x2  = local_sum[40] <<< 1;
            wire signed [OW-1:0] local_x10 = local_x8 + local_x2;
            assign out_flat[i*OW +: OW] = local_x10 - global_sum[40];
        end
    endgenerate

    initial begin
        if (OW < W + 7)
            $error("w33_pass2691_incidence_core requires OW >= W+7");
    end
endmodule


// Placeable serial wrapper: 40 input lanes are loaded, then 40 output lanes drain.
// The flat 40x40 arithmetic remains internal rather than becoming package pins.
module w33_pass2691_incidence_serial #(
    parameter integer W = 8,
    parameter integer OW = W + 7,
    parameter bit REVERSE = 1'b0
) (
    input  wire                 clk,
    input  wire                 rst,
    input  wire                 in_valid,
    input  wire signed [W-1:0]  in_data,
    output wire                 in_ready,
    output reg                  out_valid,
    output reg  signed [OW-1:0] out_data,
    output wire                 busy
);
    reg signed [40*W-1:0] xbuf;
    wire signed [40*OW-1:0] ybuf;
    reg [5:0] in_index;
    reg [5:0] out_index;
    reg loading;
    reg draining;

    w33_pass2691_incidence_core #(
        .W(W), .OW(OW), .REVERSE(REVERSE)
    ) core (
        .in_flat(xbuf),
        .out_flat(ybuf)
    );

    assign in_ready = loading;
    assign busy = draining;

    always_ff @(posedge clk) begin
        if (rst) begin
            xbuf <= 0;
            in_index <= 0;
            out_index <= 0;
            loading <= 1'b1;
            draining <= 1'b0;
            out_valid <= 1'b0;
            out_data <= 0;
        end else begin
            out_valid <= 1'b0;
            if (loading && in_valid) begin
                xbuf[in_index*W +: W] <= in_data;
                if (in_index == 6'd39) begin
                    in_index <= 0;
                    out_index <= 0;
                    loading <= 1'b0;
                    draining <= 1'b1;
                end else begin
                    in_index <= in_index + 1'b1;
                end
            end else if (draining) begin
                out_data <= ybuf[out_index*OW +: OW];
                out_valid <= 1'b1;
                if (out_index == 6'd39) begin
                    out_index <= 0;
                    loading <= 1'b1;
                    draining <= 1'b0;
                    xbuf <= 0;
                end else begin
                    out_index <= out_index + 1'b1;
                end
            end
        end
    end
endmodule
