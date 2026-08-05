`timescale 1ns/1ps
`default_nettype none

module tb_w33_pass3506_3519_min5;
    reg [1:0] a, b, c, d, e;
    wire [1:0] y0, y1, y2, y3, y4;

    reg [1:0] first0, first1, first2, first3, first4;
    reg [1:0] second0, second1, second2, second3, second4;
    integer state;
    integer temp;
    integer cases;

    w33_mod3_five_channel_min5 dut(
        .a(a), .b(b), .c(c), .d(d), .e(e),
        .y0(y0), .y1(y1), .y2(y2), .y3(y3), .y4(y4)
    );

    function automatic [1:0] add3;
        input [1:0] left;
        input [1:0] right;
        integer total;
        begin
            total = left + right;
            add3 = total % 3;
        end
    endfunction

    function automatic [1:0] neg3;
        input [1:0] value;
        begin
            neg3 = (value == 0) ? 0 : (3 - value);
        end
    endfunction

    function automatic [1:0] sub3;
        input [1:0] left;
        input [1:0] right;
        begin
            sub3 = add3(left, neg3(right));
        end
    endfunction

    task check_literal;
        input [1:0] ia, ib, ic, id, ie;
        begin
            if (y0 !== add3(add3(neg3(ia), ib), ic)) begin
                $display("FAIL y0 state=%0d", state); $fatal;
            end
            if (y1 !== add3(add3(neg3(ia), ib), id)) begin
                $display("FAIL y1 state=%0d", state); $fatal;
            end
            if (y2 !== add3(add3(neg3(ia), ic), id)) begin
                $display("FAIL y2 state=%0d", state); $fatal;
            end
            if (y3 !== add3(neg3(ib), neg3(ic))) begin
                $display("FAIL y3 state=%0d", state); $fatal;
            end
            if (y4 !== ie) begin
                $display("FAIL y4 state=%0d", state); $fatal;
            end
        end
    endtask

    initial begin
        cases = 0;
        for (state = 0; state < 243; state = state + 1) begin
            temp = state;
            a = temp % 3; temp = temp / 3;
            b = temp % 3; temp = temp / 3;
            c = temp % 3; temp = temp / 3;
            d = temp % 3; temp = temp / 3;
            e = temp % 3;
            #1;
            check_literal(a, b, c, d, e);
            first0 = y0; first1 = y1; first2 = y2; first3 = y3; first4 = y4;

            a = first0; b = first1; c = first2; d = first3; e = first4;
            #1;
            second0 = y0; second1 = y1; second2 = y2; second3 = y3; second4 = y4;

            a = second0; b = second1; c = second2; d = second3; e = second4;
            #1;
            temp = state;
            if (y0 !== temp % 3) begin $display("FAIL order3 a state=%0d", state); $fatal; end
            temp = temp / 3;
            if (y1 !== temp % 3) begin $display("FAIL order3 b state=%0d", state); $fatal; end
            temp = temp / 3;
            if (y2 !== temp % 3) begin $display("FAIL order3 c state=%0d", state); $fatal; end
            temp = temp / 3;
            if (y3 !== temp % 3) begin $display("FAIL order3 d state=%0d", state); $fatal; end
            temp = temp / 3;
            if (y4 !== temp % 3) begin $display("FAIL order3 e state=%0d", state); $fatal; end
            cases = cases + 1;
        end
        $display("PASS min5_cases=%0d order3_cases=%0d", cases, cases);
        $finish;
    end
endmodule

`default_nettype wire
