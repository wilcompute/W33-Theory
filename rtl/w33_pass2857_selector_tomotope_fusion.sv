// Pass 2857: fused Type-A selector and parity-coded tomotope cell controller.
// Valid control words: face 0..3, matching 0..2, phase 0..7 => 96 states.
module w33_pass2857_selector_tomotope_fusion (
    input  logic [1:0] face,
    input  logic [1:0] matching,
    input  logic [2:0] phase,
    output logic       valid,
    output logic [3:0] sheet_id,
    output logic       tetrahedral_cell,
    output logic [1:0] cell_index
);
    logic parity;
    always_comb begin
        valid = (matching != 2'b11);
        sheet_id = valid ? ({2'b00, face} * 4'd3 + {2'b00, matching}) : 4'hf;
        parity = phase[2] ^ phase[1] ^ phase[0];
        tetrahedral_cell = ~parity;
        cell_index = 2'b00;
        if (!parity) begin
            case (phase)
                3'b000: cell_index = 2'd0;
                3'b011: cell_index = 2'd1;
                3'b101: cell_index = 2'd2;
                3'b110: cell_index = 2'd3;
                default: cell_index = 2'd0;
            endcase
        end else begin
            case (phase)
                3'b111: cell_index = 2'd0;
                3'b100: cell_index = 2'd1;
                3'b010: cell_index = 2'd2;
                3'b001: cell_index = 2'd3;
                default: cell_index = 2'd0;
            endcase
        end
    end
endmodule
