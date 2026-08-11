// Pass 4944 -- qutrit-native hardware compiler for the Pass4872 local port matchings.
// Each selector realizes i -> (-1)^b i + r mod 3 with i,r in {0,1,2}.
// Binary encoding uses two wires per trit; 2'b11 is reserved/invalid and maps to 0.
`timescale 1ns/1ps

module w33_agl13_port_selector (
    input  wire [1:0] port_i,
    input  wire [1:0] rotation_r,
    input  wire       reflect_b,
    output reg  [1:0] port_o
);
    reg [1:0] signed_i;
    always @* begin
        // -i mod 3, with invalid encoding safely mapped to 0.
        if (!reflect_b) begin
            case (port_i)
                2'd0: signed_i = 2'd0;
                2'd1: signed_i = 2'd1;
                2'd2: signed_i = 2'd2;
                default: signed_i = 2'd0;
            endcase
        end else begin
            case (port_i)
                2'd0: signed_i = 2'd0;
                2'd1: signed_i = 2'd2;
                2'd2: signed_i = 2'd1;
                default: signed_i = 2'd0;
            endcase
        end
        // Add r modulo 3 without a divider.
        case (rotation_r)
            2'd0: port_o = signed_i;
            2'd1: begin
                case (signed_i)
                    2'd0: port_o = 2'd1;
                    2'd1: port_o = 2'd2;
                    default: port_o = 2'd0;
                endcase
            end
            2'd2: begin
                case (signed_i)
                    2'd0: port_o = 2'd2;
                    2'd1: port_o = 2'd0;
                    default: port_o = 2'd1;
                endcase
            end
            default: port_o = 2'd0;
        endcase
    end
endmodule

module w33_port_selector45 (
    input  wire [89:0] port_i_flat,
    input  wire [89:0] rotation_flat,
    input  wire [44:0] reflect_flat,
    output wire [89:0] port_o_flat
);
    genvar k;
    generate
        for (k = 0; k < 45; k = k + 1) begin : GEN_SELECTOR
            w33_agl13_port_selector u_sel (
                .port_i(port_i_flat[2*k +: 2]),
                .rotation_r(rotation_flat[2*k +: 2]),
                .reflect_b(reflect_flat[k]),
                .port_o(port_o_flat[2*k +: 2])
            );
        end
    endgenerate
endmodule
