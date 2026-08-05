`default_nettype none

module w33_mod3_five_channel_min5_formal;
`ifdef FORMAL
    (* anyconst *) reg [1:0] a;
    (* anyconst *) reg [1:0] b;
    (* anyconst *) reg [1:0] c;
    (* anyconst *) reg [1:0] d;
    (* anyconst *) reg [1:0] e;

    wire [1:0] f0a, f0b, f0c, f0d, f0e;
    wire [1:0] f1a, f1b, f1c, f1d, f1e;
    wire [1:0] f2a, f2b, f2c, f2d, f2e;

    w33_mod3_five_channel_min5 stage0(
        .a(a), .b(b), .c(c), .d(d), .e(e),
        .y0(f0a), .y1(f0b), .y2(f0c), .y3(f0d), .y4(f0e)
    );
    w33_mod3_five_channel_min5 stage1(
        .a(f0a), .b(f0b), .c(f0c), .d(f0d), .e(f0e),
        .y0(f1a), .y1(f1b), .y2(f1c), .y3(f1d), .y4(f1e)
    );
    w33_mod3_five_channel_min5 stage2(
        .a(f1a), .b(f1b), .c(f1c), .d(f1d), .e(f1e),
        .y0(f2a), .y1(f2b), .y2(f2c), .y3(f2d), .y4(f2e)
    );

    always @* begin
        assume(a < 3);
        assume(b < 3);
        assume(c < 3);
        assume(d < 3);
        assume(e < 3);
        assert(f2a == a);
        assert(f2b == b);
        assert(f2c == c);
        assert(f2d == d);
        assert(f2e == e);
    end
`endif
endmodule

`default_nettype wire
