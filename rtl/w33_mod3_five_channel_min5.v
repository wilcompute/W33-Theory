`default_nettype none

module w33_mod3_five_channel_min5(
    input  wire [1:0] a,
    input  wire [1:0] b,
    input  wire [1:0] c,
    input  wire [1:0] d,
    input  wire [1:0] e,
    output wire [1:0] y0,
    output wire [1:0] y1,
    output wire [1:0] y2,
    output wire [1:0] y3,
    output wire [1:0] y4
);

    function automatic [1:0] add3;
        input [1:0] left;
        input [1:0] right;
        reg [2:0] total;
        begin
            total = {1'b0, left} + {1'b0, right};
            if (total >= 3)
                total = total - 3;
            add3 = total[1:0];
        end
    endfunction

    function automatic [1:0] neg3;
        input [1:0] value;
        begin
            case (value)
                2'd0: neg3 = 2'd0;
                2'd1: neg3 = 2'd2;
                2'd2: neg3 = 2'd1;
                default: neg3 = 2'bxx;
            endcase
        end
    endfunction

    function automatic [1:0] sub3;
        input [1:0] left;
        input [1:0] right;
        begin
            sub3 = add3(left, neg3(right));
        end
    endfunction

    // Five binary ternary operations.  Sign and copy are wiring operations.
    wire [1:0] sum_bc = add3(b, c);
    wire [1:0] diff_da = sub3(d, a);

    assign y0 = sub3(sum_bc, a);
    assign y1 = add3(diff_da, b);
    assign y2 = add3(diff_da, c);
    assign y3 = neg3(sum_bc);
    assign y4 = e;

endmodule

`default_nettype wire
