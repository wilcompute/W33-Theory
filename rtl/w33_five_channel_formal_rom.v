`default_nettype none

module w33_five_channel_symbol_rom (
    input wire [2:0] zero_mask,
    input wire [2:0] row,
    input wire [2:0] col,
    output reg signed [4:0] weight
);
    always @* begin
        case ({zero_mask, row, col})
            9'b000000000: weight = -5'sd1;
            9'b000000001: weight = -5'sd2;
            9'b000000010: weight = -5'sd2;
            9'b000000011: weight = 5'sd0;
            9'b000000100: weight = 5'sd0;
            9'b000001000: weight = -5'sd1;
            9'b000001001: weight = -5'sd2;
            9'b000001010: weight = 5'sd0;
            9'b000001011: weight = -5'sd2;
            9'b000001100: weight = 5'sd0;
            9'b000010000: weight = -5'sd1;
            9'b000010001: weight = 5'sd0;
            9'b000010010: weight = -5'sd2;
            9'b000010011: weight = -5'sd2;
            9'b000010100: weight = 5'sd0;
            9'b000011000: weight = 5'sd0;
            9'b000011001: weight = -5'sd1;
            9'b000011010: weight = -5'sd1;
            9'b000011011: weight = -5'sd3;
            9'b000011100: weight = 5'sd0;
            9'b000100000: weight = 5'sd0;
            9'b000100001: weight = 5'sd0;
            9'b000100010: weight = 5'sd0;
            9'b000100011: weight = 5'sd0;
            9'b000100100: weight = 5'sd1;
            9'b001000000: weight = 5'sd2;
            9'b001000001: weight = -5'sd2;
            9'b001000010: weight = -5'sd2;
            9'b001000011: weight = 5'sd0;
            9'b001000100: weight = 5'sd0;
            9'b001001000: weight = -5'sd1;
            9'b001001001: weight = 5'sd1;
            9'b001001010: weight = 5'sd0;
            9'b001001011: weight = -5'sd2;
            9'b001001100: weight = 5'sd0;
            9'b001010000: weight = -5'sd1;
            9'b001010001: weight = 5'sd0;
            9'b001010010: weight = 5'sd1;
            9'b001010011: weight = -5'sd2;
            9'b001010100: weight = 5'sd0;
            9'b001011000: weight = 5'sd0;
            9'b001011001: weight = -5'sd1;
            9'b001011010: weight = -5'sd1;
            9'b001011011: weight = 5'sd0;
            9'b001011100: weight = 5'sd0;
            9'b001100000: weight = 5'sd0;
            9'b001100001: weight = 5'sd0;
            9'b001100010: weight = 5'sd0;
            9'b001100011: weight = 5'sd0;
            9'b001100100: weight = 5'sd4;
            9'b010000000: weight = -5'sd1;
            9'b010000001: weight = -5'sd2;
            9'b010000010: weight = 5'sd4;
            9'b010000011: weight = 5'sd0;
            9'b010000100: weight = 5'sd0;
            9'b010001000: weight = -5'sd1;
            9'b010001001: weight = -5'sd2;
            9'b010001010: weight = 5'sd0;
            9'b010001011: weight = 5'sd4;
            9'b010001100: weight = 5'sd0;
            9'b010010000: weight = 5'sd2;
            9'b010010001: weight = 5'sd0;
            9'b010010010: weight = 5'sd5;
            9'b010010011: weight = -5'sd2;
            9'b010010100: weight = 5'sd0;
            9'b010011000: weight = 5'sd0;
            9'b010011001: weight = 5'sd2;
            9'b010011010: weight = -5'sd1;
            9'b010011011: weight = 5'sd3;
            9'b010011100: weight = 5'sd0;
            9'b010100000: weight = 5'sd0;
            9'b010100001: weight = 5'sd0;
            9'b010100010: weight = 5'sd0;
            9'b010100011: weight = 5'sd0;
            9'b010100100: weight = -5'sd2;
            9'b011000000: weight = 5'sd2;
            9'b011000001: weight = -5'sd2;
            9'b011000010: weight = 5'sd4;
            9'b011000011: weight = 5'sd0;
            9'b011000100: weight = 5'sd0;
            9'b011001000: weight = -5'sd1;
            9'b011001001: weight = 5'sd1;
            9'b011001010: weight = 5'sd0;
            9'b011001011: weight = 5'sd4;
            9'b011001100: weight = 5'sd0;
            9'b011010000: weight = 5'sd2;
            9'b011010001: weight = 5'sd0;
            9'b011010010: weight = 5'sd8;
            9'b011010011: weight = -5'sd2;
            9'b011010100: weight = 5'sd0;
            9'b011011000: weight = 5'sd0;
            9'b011011001: weight = 5'sd2;
            9'b011011010: weight = -5'sd1;
            9'b011011011: weight = 5'sd6;
            9'b011011100: weight = 5'sd0;
            9'b011100000: weight = 5'sd0;
            9'b011100001: weight = 5'sd0;
            9'b011100010: weight = 5'sd0;
            9'b011100011: weight = 5'sd0;
            9'b011100100: weight = 5'sd1;
            9'b100000000: weight = -5'sd1;
            9'b100000001: weight = 5'sd4;
            9'b100000010: weight = -5'sd2;
            9'b100000011: weight = 5'sd0;
            9'b100000100: weight = 5'sd0;
            9'b100001000: weight = 5'sd2;
            9'b100001001: weight = 5'sd3;
            9'b100001010: weight = 5'sd0;
            9'b100001011: weight = -5'sd2;
            9'b100001100: weight = 5'sd0;
            9'b100010000: weight = -5'sd1;
            9'b100010001: weight = 5'sd0;
            9'b100010010: weight = -5'sd2;
            9'b100010011: weight = 5'sd4;
            9'b100010100: weight = 5'sd0;
            9'b100011000: weight = 5'sd0;
            9'b100011001: weight = -5'sd1;
            9'b100011010: weight = 5'sd2;
            9'b100011011: weight = 5'sd3;
            9'b100011100: weight = 5'sd0;
            9'b100100000: weight = 5'sd0;
            9'b100100001: weight = 5'sd0;
            9'b100100010: weight = 5'sd0;
            9'b100100011: weight = 5'sd0;
            9'b100100100: weight = -5'sd2;
            9'b101000000: weight = 5'sd2;
            9'b101000001: weight = 5'sd4;
            9'b101000010: weight = -5'sd2;
            9'b101000011: weight = 5'sd0;
            9'b101000100: weight = 5'sd0;
            9'b101001000: weight = 5'sd2;
            9'b101001001: weight = 5'sd6;
            9'b101001010: weight = 5'sd0;
            9'b101001011: weight = -5'sd2;
            9'b101001100: weight = 5'sd0;
            9'b101010000: weight = -5'sd1;
            9'b101010001: weight = 5'sd0;
            9'b101010010: weight = 5'sd1;
            9'b101010011: weight = 5'sd4;
            9'b101010100: weight = 5'sd0;
            9'b101011000: weight = 5'sd0;
            9'b101011001: weight = -5'sd1;
            9'b101011010: weight = 5'sd2;
            9'b101011011: weight = 5'sd6;
            9'b101011100: weight = 5'sd0;
            9'b101100000: weight = 5'sd0;
            9'b101100001: weight = 5'sd0;
            9'b101100010: weight = 5'sd0;
            9'b101100011: weight = 5'sd0;
            9'b101100100: weight = 5'sd1;
            9'b110000000: weight = -5'sd1;
            9'b110000001: weight = 5'sd4;
            9'b110000010: weight = 5'sd4;
            9'b110000011: weight = 5'sd0;
            9'b110000100: weight = 5'sd0;
            9'b110001000: weight = 5'sd2;
            9'b110001001: weight = 5'sd3;
            9'b110001010: weight = 5'sd0;
            9'b110001011: weight = 5'sd4;
            9'b110001100: weight = 5'sd0;
            9'b110010000: weight = 5'sd2;
            9'b110010001: weight = 5'sd0;
            9'b110010010: weight = 5'sd5;
            9'b110010011: weight = 5'sd4;
            9'b110010100: weight = 5'sd0;
            9'b110011000: weight = 5'sd0;
            9'b110011001: weight = 5'sd2;
            9'b110011010: weight = 5'sd2;
            9'b110011011: weight = 5'sd6;
            9'b110011100: weight = 5'sd0;
            9'b110100000: weight = 5'sd0;
            9'b110100001: weight = 5'sd0;
            9'b110100010: weight = 5'sd0;
            9'b110100011: weight = 5'sd0;
            9'b110100100: weight = -5'sd5;
            9'b111000000: weight = 5'sd2;
            9'b111000001: weight = 5'sd4;
            9'b111000010: weight = 5'sd4;
            9'b111000011: weight = 5'sd0;
            9'b111000100: weight = 5'sd0;
            9'b111001000: weight = 5'sd2;
            9'b111001001: weight = 5'sd6;
            9'b111001010: weight = 5'sd0;
            9'b111001011: weight = 5'sd4;
            9'b111001100: weight = 5'sd0;
            9'b111010000: weight = 5'sd2;
            9'b111010001: weight = 5'sd0;
            9'b111010010: weight = 5'sd8;
            9'b111010011: weight = 5'sd4;
            9'b111010100: weight = 5'sd0;
            9'b111011000: weight = 5'sd0;
            9'b111011001: weight = 5'sd2;
            9'b111011010: weight = 5'sd2;
            9'b111011011: weight = 5'sd9;
            9'b111011100: weight = 5'sd0;
            9'b111100000: weight = 5'sd0;
            9'b111100001: weight = 5'sd0;
            9'b111100010: weight = 5'sd0;
            9'b111100011: weight = 5'sd0;
            9'b111100100: weight = -5'sd2;
            default: weight = 5'sd0;
        endcase
    end
endmodule

module w33_mod3_order3_formal;
    (* anyconst *) wire [2:0] zero_mask;
    (* anyconst *) wire [1:0] in0;
    (* anyconst *) wire [1:0] in1;
    (* anyconst *) wire [1:0] in2;
    (* anyconst *) wire [1:0] in3;
    (* anyconst *) wire [1:0] in4;

    wire [1:0] a0, a1, a2, a3, a4;
    wire [1:0] b0, b1, b2, b3, b4;
    wire [1:0] c0, c1, c2, c3, c4;

    w33_mod3_five_channel_step step1(
        .zero_mask(zero_mask),
        .in0(in0), .in1(in1), .in2(in2), .in3(in3), .in4(in4),
        .out0(a0), .out1(a1), .out2(a2), .out3(a3), .out4(a4)
    );
    w33_mod3_five_channel_step step2(
        .zero_mask(zero_mask),
        .in0(a0), .in1(a1), .in2(a2), .in3(a3), .in4(a4),
        .out0(b0), .out1(b1), .out2(b2), .out3(b3), .out4(b4)
    );
    w33_mod3_five_channel_step step3(
        .zero_mask(zero_mask),
        .in0(b0), .in1(b1), .in2(b2), .in3(b3), .in4(b4),
        .out0(c0), .out1(c1), .out2(c2), .out3(c3), .out4(c4)
    );

    always @* begin
        assume(in0 <= 2);
        assume(in1 <= 2);
        assume(in2 <= 2);
        assume(in3 <= 2);
        assume(in4 <= 2);
        assert(c0 == in0);
        assert(c1 == in1);
        assert(c2 == in2);
        assert(c3 == in3);
        assert(c4 == in4);
    end
endmodule

`default_nettype wire
