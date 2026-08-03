`timescale 1ns/1ps

module w33_pass2718_incidence_transceiver_tb;
    localparam integer W = 4;
    localparam integer OW = W + 7;

    reg  signed [40*W-1:0] in_forward;
    reg  signed [40*W-1:0] in_reverse;
    wire signed [40*OW-1:0] out_forward;
    wire signed [40*OW-1:0] out_reverse;

    w33_pass2717_incidence_core #(.W(W), .OW(OW), .REVERSE(1'b0)) forward_core (
        .in_flat(in_forward), .out_flat(out_forward)
    );
    w33_pass2717_incidence_core #(.W(W), .OW(OW), .REVERSE(1'b1)) reverse_core (
        .in_flat(in_reverse), .out_flat(out_reverse)
    );

    reg clk = 0;
    reg rst = 1;
    reg in_valid = 0;
    reg signed [W-1:0] in_data = 0;
    wire in_ready;
    wire out_valid;
    wire signed [OW-1:0] out_data;
    wire busy;

    w33_pass2717_incidence_serial #(.W(W), .OW(OW), .REVERSE(1'b0)) serial_core (
        .clk(clk), .rst(rst), .in_valid(in_valid), .in_data(in_data),
        .in_ready(in_ready), .out_valid(out_valid), .out_data(out_data), .busy(busy)
    );

    always #5 clk = ~clk;

    integer i;
    integer got;
    integer expected;
    integer seen;

    task check_forward_basis0;
        begin
            in_forward = 0;
            in_forward[0*W +: W] = 1;
            #1;
            for (i = 0; i < 40; i = i + 1) begin
                got = $signed(out_forward[i*OW +: OW]);
                expected = (i < 4) ? 9 : -1;
                if (got !== expected)
                    $fatal(1, "forward basis e0 mismatch lane=%0d got=%0d expected=%0d", i, got, expected);
            end
        end
    endtask

    task check_reverse_basis0;
        begin
            in_reverse = 0;
            in_reverse[0*W +: W] = 1;
            #1;
            for (i = 0; i < 40; i = i + 1) begin
                got = $signed(out_reverse[i*OW +: OW]);
                expected = (i < 4) ? 9 : -1;
                if (got !== expected)
                    $fatal(1, "reverse basis e0 mismatch lane=%0d got=%0d expected=%0d", i, got, expected);
            end
        end
    endtask

    task check_constants_killed;
        begin
            for (i = 0; i < 40; i = i + 1) begin
                in_forward[i*W +: W] = 1;
                in_reverse[i*W +: W] = -1;
            end
            #1;
            for (i = 0; i < 40; i = i + 1) begin
                if ($signed(out_forward[i*OW +: OW]) !== 0)
                    $fatal(1, "forward constant not killed at lane %0d", i);
                if ($signed(out_reverse[i*OW +: OW]) !== 0)
                    $fatal(1, "reverse constant not killed at lane %0d", i);
            end
        end
    endtask

    task check_serial_basis0;
        begin
            @(negedge clk);
            rst = 0;
            in_valid = 1;
            for (i = 0; i < 40; i = i + 1) begin
                in_data = (i == 0) ? 1 : 0;
                @(negedge clk);
            end
            in_valid = 0;
            in_data = 0;
            seen = 0;
            while (seen < 40) begin
                @(negedge clk);
                if (out_valid) begin
                    got = $signed(out_data);
                    expected = (seen < 4) ? 9 : -1;
                    if (got !== expected)
                        $fatal(1, "serial mismatch lane=%0d got=%0d expected=%0d", seen, got, expected);
                    seen = seen + 1;
                end
            end
            if (!in_ready)
                $fatal(1, "serial core did not return to loading state");
        end
    endtask

    initial begin
        in_forward = 0;
        in_reverse = 0;
        repeat (2) @(negedge clk);
        check_forward_basis0();
        check_reverse_basis0();
        check_constants_killed();
        check_serial_basis0();
        $display("PASS w33_pass2718_incidence_transceiver_tb");
        $finish;
    end
endmodule
