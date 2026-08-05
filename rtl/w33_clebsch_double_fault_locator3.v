// Pass 3522: minimum three-bit companion locator for Clebsch biplane collisions.
module w33_clebsch_double_fault_locator3(
    input  wire [3:0] axis,
    output reg  [2:0] label
);
    // The unique ANF is cubic; this table is its literal fail-closed realization.
    always @* begin
        case (axis)
            4'h0: label = 3'd0;
            4'h1: label = 3'd0;
            4'h2: label = 3'd0;
            4'h3: label = 3'd0;
            4'h4: label = 3'd0;
            4'h5: label = 3'd1;
            4'h6: label = 3'd2;
            4'h7: label = 3'd3;
            4'h8: label = 3'd0;
            4'h9: label = 3'd2;
            4'ha: label = 3'd3;
            4'hb: label = 3'd4;
            4'hc: label = 3'd5;
            4'hd: label = 3'd6;
            4'he: label = 3'd1;
            4'hf: label = 3'd7;
            default: label = 3'd0;
        endcase
    end
endmodule
