`default_nettype none
module w33_five_channel_torus_engine(
    input  wire [1:0] k0,
    input  wire [1:0] k1,
    input  wire [1:0] k2,
    input  wire [2:0] row_channel,
    input  wire [2:0] col_channel,
    output reg  signed [4:0] coefficient
);
    function automatic signed [4:0] character3(input [1:0] k);
        begin character3 = (k == 2'd0) ? 5'sd2 : -5'sd1; end
    endfunction
    function automatic signed [4:0] x_kernel(input [2:0] r, input [2:0] c);
        begin
            x_kernel = 0;
            case ({r,c})
                6'o01: x_kernel = 2;
                6'o10, 6'o11: x_kernel = 1;
                6'o23: x_kernel = 2;
                6'o32, 6'o33: x_kernel = 1;
                default: x_kernel = 0;
            endcase
        end
    endfunction
    function automatic signed [4:0] y_kernel(input [2:0] r, input [2:0] c);
        begin
            y_kernel = 0;
            case ({r,c})
                6'o02: y_kernel = 2;
                6'o13: y_kernel = 2;
                6'o20, 6'o22: y_kernel = 1;
                6'o31, 6'o33: y_kernel = 1;
                default: y_kernel = 0;
            endcase
        end
    endfunction
    always @* begin
        coefficient = 0;
        if ((row_channel < 4) && (col_channel < 4)) begin
            coefficient = character3(k0) * x_kernel(row_channel,col_channel)
                        + character3(k1) * y_kernel(row_channel,col_channel)
                        + ((row_channel == col_channel) ? character3(k2) : 0);
        end else if ((row_channel == 4) && (col_channel == 4)) begin
            coefficient = -character3(k0) - character3(k1) + character3(k2);
        end
    end
endmodule
`default_nettype wire
