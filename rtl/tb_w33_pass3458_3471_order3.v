`timescale 1ns/1ps
`default_nettype none

module tb_w33_pass3458_3471_order3;
    reg [2:0] zero_mask;
    reg [2:0] row;
    reg [2:0] col;
    wire signed [4:0] factored_weight;
    wire signed [4:0] rom_weight;

    reg [1:0] in0, in1, in2, in3, in4;
    wire [1:0] a0, a1, a2, a3, a4;
    wire [1:0] b0, b1, b2, b3, b4;
    wire [1:0] c0, c1, c2, c3, c4;

    integer mask_i;
    integer row_i;
    integer col_i;
    integer state_i;
    integer tmp;

    w33_five_channel_symbol dut_factored(
        .zero_mask(zero_mask), .row(row), .col(col), .weight(factored_weight)
    );
    w33_five_channel_symbol_rom dut_rom(
        .zero_mask(zero_mask), .row(row), .col(col), .weight(rom_weight)
    );

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

    initial begin
        for (mask_i = 0; mask_i < 8; mask_i = mask_i + 1) begin
            zero_mask = mask_i[2:0];
            for (row_i = 0; row_i < 5; row_i = row_i + 1) begin
                row = row_i[2:0];
                for (col_i = 0; col_i < 5; col_i = col_i + 1) begin
                    col = col_i[2:0];
                    #1;
                    if (factored_weight !== rom_weight) begin
                        $display("FAIL symbol mask=%0d row=%0d col=%0d factored=%0d rom=%0d",
                                 mask_i, row_i, col_i, factored_weight, rom_weight);
                        $fatal(1);
                    end
                end
            end
        end

        for (mask_i = 0; mask_i < 8; mask_i = mask_i + 1) begin
            zero_mask = mask_i[2:0];
            for (state_i = 0; state_i < 243; state_i = state_i + 1) begin
                tmp = state_i;
                in0 = tmp % 3; tmp = tmp / 3;
                in1 = tmp % 3; tmp = tmp / 3;
                in2 = tmp % 3; tmp = tmp / 3;
                in3 = tmp % 3; tmp = tmp / 3;
                in4 = tmp % 3;
                #1;
                if ((c0 !== in0) || (c1 !== in1) || (c2 !== in2) ||
                    (c3 !== in3) || (c4 !== in4)) begin
                    $display("FAIL order3 mask=%0d state=%0d", mask_i, state_i);
                    $fatal(1);
                end
            end
        end

        $display("PASS literal_equivalence=200 order3_cases=1944");
        $finish;
    end
endmodule

`default_nettype wire
