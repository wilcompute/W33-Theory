// Pass 3508: minimum three-bit companion locator for Clebsch biplane collisions.
module w33_clebsch_double_fault_locator3(
    input wire [3:0] axis,
    output reg [2:0] label
);
    always @* begin
        case(axis)
            4'h0:label=0; 4'h1:label=0; 4'h2:label=0; 4'h3:label=0;
            4'h4:label=0; 4'h5:label=1; 4'h6:label=2; 4'h7:label=3;
            4'h8:label=0; 4'h9:label=2; 4'ha:label=3; 4'hb:label=4;
            4'hc:label=5; 4'hd:label=6; 4'he:label=1; 4'hf:label=7;
            default:label=0;
        endcase
    end
endmodule
