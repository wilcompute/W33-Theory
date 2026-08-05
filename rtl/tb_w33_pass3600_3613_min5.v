`timescale 1ns/1ps
`default_nettype none

module tb_w33_pass3600_3613_min5;
    reg [1:0] a, b, c, d, e;
    wire [1:0] y0, y1, y2, y3, y4;
    reg [1:0] f0, f1, f2, f3, f4;
    reg [1:0] s0, s1, s2, s3, s4;
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
        begin total = left + right; add3 = total % 3; end
    endfunction

    function automatic [1:0] neg3;
        input [1:0] value;
        begin neg3 = (value == 0) ? 0 : (3 - value); end
    endfunction

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
            if (y0 !== add3(add3(neg3(a), b), c)) $fatal;
            if (y1 !== add3(add3(neg3(a), b), d)) $fatal;
            if (y2 !== add3(add3(neg3(a), c), d)) $fatal;
            if (y3 !== add3(neg3(b), neg3(c))) $fatal;
            if (y4 !== e) $fatal;
            f0=y0; f1=y1; f2=y2; f3=y3; f4=y4;
            a=f0; b=f1; c=f2; d=f3; e=f4; #1;
            s0=y0; s1=y1; s2=y2; s3=y3; s4=y4;
            a=s0; b=s1; c=s2; d=s3; e=s4; #1;
            temp = state;
            if (y0 !== temp % 3) $fatal; temp = temp / 3;
            if (y1 !== temp % 3) $fatal; temp = temp / 3;
            if (y2 !== temp % 3) $fatal; temp = temp / 3;
            if (y3 !== temp % 3) $fatal; temp = temp / 3;
            if (y4 !== temp % 3) $fatal;
            cases = cases + 1;
        end
        $display("PASS pass3600_3613_min5_cases=%0d order3_cases=%0d", cases, cases);
        $finish;
    end
endmodule

`default_nettype wire
