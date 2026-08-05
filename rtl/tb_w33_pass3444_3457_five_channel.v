`timescale 1ns/1ps
`default_nettype none

module tb_w33_pass3444_3457_five_channel;
    reg [2:0] zero_mask;
    reg [2:0] row;
    reg [2:0] col;
    wire signed [4:0] weight;

    reg [1:0] in0;
    reg [1:0] in1;
    reg [1:0] in2;
    reg [1:0] in3;
    reg [1:0] in4;

    wire [1:0] a0, a1, a2, a3, a4;
    wire [1:0] b0, b1, b2, b3, b4;
    wire [1:0] c0, c1, c2, c3, c4;

    integer mask_i;
    integer row_i;
    integer col_i;
    integer state_i;
    integer temp;
    integer expected;
    integer observed;
    integer cases_symbol;
    integer cases_state;

    w33_five_channel_symbol symbol_dut (
        .zero_mask(zero_mask), .row(row), .col(col), .weight(weight)
    );

    w33_mod3_five_channel_step step_a (
        .zero_mask(zero_mask),
        .in0(in0), .in1(in1), .in2(in2), .in3(in3), .in4(in4),
        .out0(a0), .out1(a1), .out2(a2), .out3(a3), .out4(a4)
    );
    w33_mod3_five_channel_step step_b (
        .zero_mask(zero_mask),
        .in0(a0), .in1(a1), .in2(a2), .in3(a3), .in4(a4),
        .out0(b0), .out1(b1), .out2(b2), .out3(b3), .out4(b4)
    );
    w33_mod3_five_channel_step step_c (
        .zero_mask(zero_mask),
        .in0(b0), .in1(b1), .in2(b2), .in3(b3), .in4(b4),
        .out0(c0), .out1(c1), .out2(c2), .out3(c3), .out4(c4)
    );

    function integer j_entry;
        input integer r;
        input integer c;
        begin
            j_entry = 0;
            case (r)
                0: case (c) 0: j_entry=2; 1: j_entry=1; 2: j_entry=1; default: j_entry=0; endcase
                1: case (c) 0: j_entry=2; 1: j_entry=1; 3: j_entry=1; default: j_entry=0; endcase
                2: case (c) 0: j_entry=2; 2: j_entry=1; 3: j_entry=1; default: j_entry=0; endcase
                3: case (c) 1: j_entry=2; 2: j_entry=2; default: j_entry=0; endcase
                4: if (c == 4) j_entry=1;
                default: j_entry=0;
            endcase
        end
    endfunction

    function integer reduce3_signed;
        input integer value;
        integer residue;
        begin
            residue = value % 3;
            if (residue < 0)
                residue = residue + 3;
            reduce3_signed = residue;
        end
    endfunction

    initial begin
        cases_symbol = 0;
        cases_state = 0;
        zero_mask = 0;
        row = 0;
        col = 0;
        in0 = 0;
        in1 = 0;
        in2 = 0;
        in3 = 0;
        in4 = 0;
        #1;

        for (mask_i = 0; mask_i < 8; mask_i = mask_i + 1) begin
            zero_mask = mask_i[2:0];
            for (row_i = 0; row_i < 5; row_i = row_i + 1) begin
                for (col_i = 0; col_i < 5; col_i = col_i + 1) begin
                    row = row_i[2:0];
                    col = col_i[2:0];
                    #1;
                    observed = $signed(weight);
                    expected = j_entry(row_i, col_i);
                    if (reduce3_signed(observed) !== expected) begin
                        $display("FAIL symbol mask=%0d row=%0d col=%0d weight=%0d mod3=%0d expected=%0d",
                                 mask_i, row_i, col_i, observed,
                                 reduce3_signed(observed), expected);
                        $fatal(1);
                    end
                    cases_symbol = cases_symbol + 1;
                end
            end

            for (state_i = 0; state_i < 243; state_i = state_i + 1) begin
                temp = state_i;
                in0 = temp % 3; temp = temp / 3;
                in1 = temp % 3; temp = temp / 3;
                in2 = temp % 3; temp = temp / 3;
                in3 = temp % 3; temp = temp / 3;
                in4 = temp % 3;
                #1;
                if ((c0 !== in0) || (c1 !== in1) || (c2 !== in2) ||
                    (c3 !== in3) || (c4 !== in4)) begin
                    $display("FAIL order3 mask=%0d state=%0d in=%0d%0d%0d%0d%0d out=%0d%0d%0d%0d%0d",
                             mask_i, state_i, in4,in3,in2,in1,in0,c4,c3,c2,c1,c0);
                    $fatal(1);
                end
                cases_state = cases_state + 1;
            end
        end

        if (cases_symbol != 200 || cases_state != 1944) begin
            $display("FAIL case counts symbols=%0d states=%0d", cases_symbol, cases_state);
            $fatal(1);
        end
        $display("PASS five-channel symbols=200 modular_order3_states=1944");
        $finish;
    end
endmodule

`default_nettype wire
