module w33_pass3252_s3_reliability_decoder (
    input  logic       valid,
    input  logic [2:0] syndrome,
    input  logic [7:0] reliability0,
    input  logic [7:0] reliability1,
    input  logic [7:0] reliability2,
    output logic       detected,
    output logic       tie,
    output logic [1:0] edge_select,
    output logic [2:0] correction,
    output logic       sideinfo_correction_valid,
    output logic       blind_guarantee
);
    function automatic logic [2:0] s3_inverse(input logic [2:0] g);
        case (g)
            3'd0: s3_inverse = 3'd0;
            3'd1: s3_inverse = 3'd1;
            3'd2: s3_inverse = 3'd2;
            3'd3: s3_inverse = 3'd4;
            3'd4: s3_inverse = 3'd3;
            3'd5: s3_inverse = 3'd5;
            default: s3_inverse = 3'd0;
        endcase
    endfunction

    logic [7:0] max_rel;
    always_comb begin
        detected = valid && (syndrome != 3'd0) && (syndrome <= 3'd5);
        edge_select = 2'd0;
        max_rel = reliability0;
        if (reliability1 > max_rel) begin
            max_rel = reliability1;
            edge_select = 2'd1;
        end
        if (reliability2 > max_rel) begin
            max_rel = reliability2;
            edge_select = 2'd2;
        end
        tie = detected && (((reliability0 == max_rel) ? 1 : 0)
                        + ((reliability1 == max_rel) ? 1 : 0)
                        + ((reliability2 == max_rel) ? 1 : 0) > 1);
        correction = 3'd0;
        if (detected) begin
            correction = (edge_select == 2'd2) ? s3_inverse(syndrome) : syndrome;
        end
        sideinfo_correction_valid = detected && !tie;
        // The exact non-Abelian code distance is two. Syndrome alone therefore
        // provides detection but no guaranteed correction radius.
        blind_guarantee = 1'b0;
    end
endmodule
