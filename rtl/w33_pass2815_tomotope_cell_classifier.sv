// Pass 2815: parity-code controller for the signed-support tomotope.
// phase[0],phase[1],phase[2] mark minus signs on coordinates 1,2,3
// after projective normalization of coordinate 0 to +1.
module w33_pass2815_tomotope_cell_classifier(
    input  logic [2:0] phase,
    output logic       is_hemioctahedron,
    output logic [1:0] cell_index
);
    always_comb begin
        is_hemioctahedron = ^phase;
        if (!(^phase)) begin
            case (phase)
                3'b000: cell_index = 2'd0;
                3'b011: cell_index = 2'd1;
                3'b101: cell_index = 2'd2;
                default: cell_index = 2'd3;
            endcase
        end else begin
            case (phase)
                3'b001: cell_index = 2'd1;
                3'b010: cell_index = 2'd2;
                3'b100: cell_index = 2'd3;
                default: cell_index = 2'd0;
            endcase
        end
    end
endmodule
