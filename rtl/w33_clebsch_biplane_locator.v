`default_nettype none
module w33_clebsch_biplane_locator(
    input  wire [15:0] point_error,
    output wire [15:0] syndrome
);
    assign syndrome[0]  = ^(point_error & 16'h8117);
    assign syndrome[1]  = ^(point_error & 16'h422b);
    assign syndrome[2]  = ^(point_error & 16'h244d);
    assign syndrome[3]  = ^(point_error & 16'h188e);
    assign syndrome[4]  = ^(point_error & 16'h1871);
    assign syndrome[5]  = ^(point_error & 16'h24b2);
    assign syndrome[6]  = ^(point_error & 16'h42d4);
    assign syndrome[7]  = ^(point_error & 16'h81e8);
    assign syndrome[8]  = ^(point_error & 16'h1781);
    assign syndrome[9]  = ^(point_error & 16'h2b42);
    assign syndrome[10] = ^(point_error & 16'h4d24);
    assign syndrome[11] = ^(point_error & 16'h8e18);
    assign syndrome[12] = ^(point_error & 16'h7118);
    assign syndrome[13] = ^(point_error & 16'hb224);
    assign syndrome[14] = ^(point_error & 16'hd442);
    assign syndrome[15] = ^(point_error & 16'he881);
endmodule
`default_nettype wire
