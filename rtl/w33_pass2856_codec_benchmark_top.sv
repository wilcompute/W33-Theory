// Pass 2856 benchmark wrapper: load an 8-bit four-trit frame, store the exact
// seven-bit enumerative code, and decode it continuously.  This separates the
// storage saving from the combinational codec cost under an observable load port.
module w33_pass2856_codec_benchmark_top (
    input  logic       clk,
    input  logic       load,
    input  logic [7:0] frame_in,
    output logic [7:0] frame_out,
    output logic [6:0] code_out
);
    logic [6:0] encoded;
    logic [5:0] projective_addr;
    logic [3:0] support_mask;
    logic [2:0] relative_phase;
    logic polarity, is_zero;
    logic [6:0] code_reg = 7'd0;
    logic [1:0] y0,y1,y2,y3;

    w33_pass2811_support_first_codec enc(
        .x0(frame_in[1:0]), .x1(frame_in[3:2]),
        .x2(frame_in[5:4]), .x3(frame_in[7:6]),
        .affine_code(encoded), .projective_addr(projective_addr),
        .support_mask(support_mask), .relative_phase(relative_phase),
        .polarity(polarity), .is_zero(is_zero)
    );
    always_ff @(posedge clk)
        if (load) code_reg <= encoded;
    w33_pass2811_support_first_decoder dec(
        .affine_code(code_reg), .x0(y0), .x1(y1), .x2(y2), .x3(y3)
    );
    always_comb begin
        code_out = code_reg;
        frame_out = {y3,y2,y1,y0};
    end
endmodule
