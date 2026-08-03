// Pass 2853: sequential nearest-neighbor decoder for the 24-bit affine-square code.
// It scans all 81 ternary frames. best_distance <= 1 is unique because d_min=4.
module w33_pass2853_affine_square_nn_decoder (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        start,
    input  logic [23:0] received,
    output logic        busy,
    output logic        done,
    output logic        corrected_valid,
    output logic [7:0]  decoded_frame,
    output logic [4:0]  best_distance
);
    logic [1:0] cand_xp, cand_zp, cand_xf, cand_zf;
    logic [6:0] candidate_index;
    logic [23:0] candidate_code;
    logic candidate_legal;
    logic [4:0] candidate_distance;
    logic [23:0] difference;
    integer i;

    w33_pass2848_affine_square_feature_encoder encoder (
        .x_p(cand_xp), .z_p(cand_zp), .x_f(cand_xf), .z_f(cand_zf),
        .code(candidate_code), .legal(candidate_legal)
    );

    always_comb begin
        difference = received ^ candidate_code;
        candidate_distance = 5'd0;
        for (i = 0; i < 24; i = i + 1)
            candidate_distance = candidate_distance + difference[i];
    end

    task automatic increment_ternary_candidate;
        begin
            if (cand_xp != 2'd2) cand_xp <= cand_xp + 2'd1;
            else begin
                cand_xp <= 2'd0;
                if (cand_zp != 2'd2) cand_zp <= cand_zp + 2'd1;
                else begin
                    cand_zp <= 2'd0;
                    if (cand_xf != 2'd2) cand_xf <= cand_xf + 2'd1;
                    else begin
                        cand_xf <= 2'd0;
                        cand_zf <= cand_zf + 2'd1;
                    end
                end
            end
        end
    endtask

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            busy <= 1'b0;
            done <= 1'b0;
            corrected_valid <= 1'b0;
            decoded_frame <= 8'd0;
            best_distance <= 5'd31;
            candidate_index <= 7'd0;
            cand_xp <= 2'd0;
            cand_zp <= 2'd0;
            cand_xf <= 2'd0;
            cand_zf <= 2'd0;
        end else begin
            done <= 1'b0;
            if (start && !busy) begin
                busy <= 1'b1;
                corrected_valid <= 1'b0;
                best_distance <= 5'd31;
                candidate_index <= 7'd0;
                cand_xp <= 2'd0;
                cand_zp <= 2'd0;
                cand_xf <= 2'd0;
                cand_zf <= 2'd0;
            end else if (busy) begin
                if (candidate_legal && candidate_distance < best_distance) begin
                    best_distance <= candidate_distance;
                    decoded_frame <= {cand_zf, cand_xf, cand_zp, cand_xp};
                end
                if (candidate_index == 7'd80) begin
                    busy <= 1'b0;
                    done <= 1'b1;
                    corrected_valid <= ((candidate_distance < best_distance ?
                                         candidate_distance : best_distance) <= 5'd1);
                end else begin
                    candidate_index <= candidate_index + 7'd1;
                    increment_ternary_candidate();
                end
            end
        end
    end
endmodule
