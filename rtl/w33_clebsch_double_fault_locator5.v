// Pass 3566: minimum five-bit companion locator with compound distance three.
module w33_clebsch_double_fault_locator5(
    input  wire [3:0] axis,
    output reg  [4:0] label
);
    always @* begin
        case (axis)
            4'h0: label = 5'd0;
            4'h1: label = 5'd0;
            4'h2: label = 5'd0;
            4'h3: label = 5'd0;
            4'h4: label = 5'd30;
            4'h5: label = 5'd25;
            4'h6: label = 5'd0;
            4'h7: label = 5'd7;
            4'h8: label = 5'd0;
            4'h9: label = 5'd27;
            4'ha: label = 5'd13;
            4'hb: label = 5'd22;
            4'hc: label = 5'd14;
            4'hd: label = 5'd18;
            4'he: label = 5'd29;
            4'hf: label = 5'd1;
            default: label = 5'd0;
        endcase
    end
endmodule
