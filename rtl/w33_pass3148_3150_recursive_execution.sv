// Passes 3148--3150: universal-ISA comparison hardware and recursive execution fabric.
//
// This source integrates the fixed-point spectral predictor from Pass 3135 with
// context-local causal state, a two-edit Levenshtein mask bank, a frozen
// action-rate-distortion selector, double-buffered calibration memory, and explicit
// reset boundaries.  Tool-observed area, timing and power remain evidence-gated.

module w33_pass3148_affine_dispatch #(
    parameter bit ALTERNATIVE_ISA = 1'b0
) (
    input  logic [1:0] x0_i, x1_i, x2_i, x3_i,
    input  logic [1:0] opcode_i,
    output logic [1:0] y0_o, y1_o, y2_o, y3_o
);
    function automatic logic [1:0] add3(input logic [1:0] a, input logic [1:0] b);
        logic [2:0] s;
        begin
            s = a + b;
            add3 = (s >= 3) ? s - 3 : s[1:0];
        end
    endfunction
    function automatic logic [1:0] neg3(input logic [1:0] a);
        begin
            case (a)
                2'd0: neg3 = 2'd0;
                2'd1: neg3 = 2'd2;
                default: neg3 = 2'd1;
            endcase
        end
    endfunction

    always_comb begin
        y0_o = x0_i; y1_o = x1_i; y2_o = x2_i; y3_o = x3_i;
        if (!ALTERNATIVE_ISA) begin
            // Current: F_p, CX_pf, CX_fp, Z1.
            case (opcode_i)
                2'd0: begin y0_o = neg3(x1_i); y1_o = x0_i; end
                2'd1: begin y1_o = add3(x1_i, neg3(x3_i)); y2_o = add3(x0_i, x2_i); end
                2'd2: begin y0_o = add3(x0_i, x2_i); y3_o = add3(neg3(x1_i), x3_i); end
                default: y1_o = add3(x1_i, 2'd1);
            endcase
        end else begin
            // Minimum-collision universal choice: CX_fp, CX_pf, F_f, Z0.
            case (opcode_i)
                2'd0: begin y0_o = add3(x0_i, x2_i); y3_o = add3(neg3(x1_i), x3_i); end
                2'd1: begin y1_o = add3(x1_i, neg3(x3_i)); y2_o = add3(x0_i, x2_i); end
                2'd2: begin y2_o = neg3(x3_i); y3_o = x2_i; end
                default: y0_o = add3(x0_i, 2'd1);
            endcase
        end
    end
endmodule

module w33_pass3149_edit_mask_bank #(
    parameter integer NCTX = 16,
    parameter integer CTXW = (NCTX <= 2) ? 1 : $clog2(NCTX)
) (
    input  logic clk,
    input  logic rst,
    input  logic [CTXW-1:0] ctx_i,
    input  logic context_reset_i,
    input  logic epoch_i,
    input  logic blind_acquire_i,
    input  logic symbol_valid_i,
    input  logic edit_enable_i,
    input  logic [4:0] symbol_i,
    output logic [11:0] phase_mask_o,
    output logic [3:0] phase_o,
    output logic locked_o,
    output logic valid_o
);
    logic [11:0] m0 [0:NCTX-1];
    logic [11:0] m1 [0:NCTX-1];
    logic [11:0] m2 [0:NCTX-1];
    logic valid_mem [0:NCTX-1];
    logic [11:0] c0, c1, c2, n0, n1, n2, union_mask;
    integer p, k;

    function automatic logic [11:0] rot1(input logic [11:0] x);
        rot1 = {x[10:0], x[11]};
    endfunction
    function automatic logic [4:0] sync_symbol(input integer phase);
        begin
            case (phase)
                0: sync_symbol=5'd7;  1: sync_symbol=5'd2;
                2: sync_symbol=5'd16; 3: sync_symbol=5'd23;
                4: sync_symbol=5'd20; 5: sync_symbol=5'd15;
                6: sync_symbol=5'd0;  7: sync_symbol=5'd2;
                8: sync_symbol=5'd7;  9: sync_symbol=5'd11;
                10: sync_symbol=5'd16; default: sync_symbol=5'd19;
            endcase
        end
    endfunction

    always_comb begin
        c0 = m0[ctx_i]; c1 = m1[ctx_i]; c2 = m2[ctx_i];
        if (edit_enable_i) begin
            c1 = c1 | rot1(c0);            // one epsilon deletion
            c2 = c2 | rot1(c1);            // second deletion, including two from m0
        end
        n0 = '0; n1 = '0; n2 = '0;
        for (p=0; p<12; p=p+1) begin
            if (c0[p]) begin
                if (sync_symbol(p) == symbol_i) n0[(p+1)%12] = 1'b1;
                else if (edit_enable_i) n1[(p+1)%12] = 1'b1; // substitution
                if (edit_enable_i) n1[p] = 1'b1;             // insertion
            end
            if (c1[p]) begin
                if (sync_symbol(p) == symbol_i) n1[(p+1)%12] = 1'b1;
                else if (edit_enable_i) n2[(p+1)%12] = 1'b1;
                if (edit_enable_i) n2[p] = 1'b1;
            end
            if (c2[p] && sync_symbol(p) == symbol_i) n2[(p+1)%12] = 1'b1;
        end
        union_mask = m0[ctx_i] | m1[ctx_i] | m2[ctx_i];
        phase_mask_o = union_mask;
        locked_o = (union_mask != 0) && ((union_mask & (union_mask - 1'b1)) == 0);
        phase_o = '0;
        for (p=0; p<12; p=p+1) if (union_mask[p]) phase_o = p[3:0];
        valid_o = valid_mem[ctx_i];
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            for (k=0; k<NCTX; k=k+1) begin
                m0[k] <= '0; m1[k] <= '0; m2[k] <= '0; valid_mem[k] <= 1'b0;
            end
        end else if (context_reset_i) begin
            m0[ctx_i] <= '0; m1[ctx_i] <= '0; m2[ctx_i] <= '0; valid_mem[ctx_i] <= 1'b0;
        end else if (epoch_i) begin
            m0[ctx_i] <= 12'b000000000001;
            m1[ctx_i] <= '0; m2[ctx_i] <= '0; valid_mem[ctx_i] <= 1'b1;
        end else if (blind_acquire_i) begin
            m0[ctx_i] <= 12'hfff;
            m1[ctx_i] <= '0; m2[ctx_i] <= '0; valid_mem[ctx_i] <= 1'b1;
        end else if (symbol_valid_i && valid_mem[ctx_i]) begin
            m0[ctx_i] <= n0; m1[ctx_i] <= n1; m2[ctx_i] <= n2;
        end
    end
endmodule

module w33_pass3149_recursive_execution_controller #(
    parameter integer NCTX = 16,
    parameter integer CTXW = (NCTX <= 2) ? 1 : $clog2(NCTX),
    parameter integer W = 18
) (
    input  logic clk,
    input  logic rst,
    input  logic [CTXW-1:0] ctx_i,
    input  logic context_reset_i,
    input  logic inference_valid_i,
    input  logic signed [W-1:0] lane0_i, lane1_i, lane2_i, lane3_i, lane4_i,
    input  logic [8:0] next_causal_state_i,
    input  logic [3:0] budget_tier_i,
    input  logic epoch_i,
    input  logic blind_acquire_i,
    input  logic symbol_valid_i,
    input  logic edit_enable_i,
    input  logic [4:0] symbol_i,
    input  logic calibration_load_i,
    input  logic calibration_load_bank_i,
    input  logic [6:0] calibration_addr_i,
    input  logic [15:0] calibration_data_i,
    input  logic calibration_commit_i,
    output logic [15:0] calibration_data_o,
    output logic signed [W-1:0] lane0_o, lane1_o, lane2_o, lane3_o, lane4_o,
    output logic [8:0] causal_state_o,
    output logic [3:0] action_o,
    output logic stop_o,
    output logic [11:0] phase_mask_o,
    output logic [3:0] phase_o,
    output logic sync_locked_o,
    output logic sync_valid_o,
    output logic [CTXW-1:0] next_round_robin_ctx_o
);
    logic [8:0] causal_mem [0:NCTX-1];
    logic [3:0] action_mem [0:NCTX-1];
    logic [15:0] cal0 [0:71];
    logic [15:0] cal1 [0:71];
    logic active_bank;
    logic [3:0] selected_action;
    logic [8:0] spectral_state_unused;
    logic [3:0] spectral_action_unused;
    logic spectral_stop_unused;
    integer k;

    function automatic logic [3:0] frontier_action(input logic [3:0] tier);
        begin
            if (tier <= 3) frontier_action = 4'd0;       // stop/no route sensing
            else if (tier <= 5) frontier_action = 4'd3;  // V4 alphabet
            else if (tier <= 9) frontier_action = 4'd4;  // conjugacy alphabet
            else frontier_action = 4'd5;                 // full D4
        end
    endfunction

    always_comb begin
        selected_action = frontier_action(budget_tier_i);
        causal_state_o = causal_mem[ctx_i];
        action_o = action_mem[ctx_i];
        stop_o = (action_mem[ctx_i] == 4'd0);
        calibration_data_o = active_bank ? cal1[calibration_addr_i] : cal0[calibration_addr_i];
        next_round_robin_ctx_o = (ctx_i == NCTX-1) ? '0 : ctx_i + 1'b1;
    end

    w33_pass3135_fourier_causal_controller #(.W(W)) spectral(
        .clk(clk), .rst(rst), .valid_i(inference_valid_i),
        .lane0_i(lane0_i), .lane1_i(lane1_i), .lane2_i(lane2_i),
        .lane3_i(lane3_i), .lane4_i(lane4_i),
        .next_causal_state_i(next_causal_state_i), .next_action_i(selected_action),
        .lane0_o(lane0_o), .lane1_o(lane1_o), .lane2_o(lane2_o),
        .lane3_o(lane3_o), .lane4_o(lane4_o),
        .causal_state_o(spectral_state_unused), .action_o(spectral_action_unused),
        .stop_o(spectral_stop_unused)
    );

    w33_pass3149_edit_mask_bank #(.NCTX(NCTX), .CTXW(CTXW)) sync_bank(
        .clk(clk), .rst(rst), .ctx_i(ctx_i), .context_reset_i(context_reset_i),
        .epoch_i(epoch_i), .blind_acquire_i(blind_acquire_i),
        .symbol_valid_i(symbol_valid_i), .edit_enable_i(edit_enable_i), .symbol_i(symbol_i),
        .phase_mask_o(phase_mask_o), .phase_o(phase_o), .locked_o(sync_locked_o), .valid_o(sync_valid_o)
    );

    always_ff @(posedge clk) begin
        if (rst) begin
            active_bank <= 1'b0;
            for (k=0; k<NCTX; k=k+1) begin
                causal_mem[k] <= '0;
                action_mem[k] <= '0;
            end
        end else begin
            if (context_reset_i) begin
                causal_mem[ctx_i] <= '0;
                action_mem[ctx_i] <= '0;
            end else if (inference_valid_i) begin
                causal_mem[ctx_i] <= next_causal_state_i;
                action_mem[ctx_i] <= selected_action;
            end
            if (calibration_load_i && calibration_addr_i < 72) begin
                if (calibration_load_bank_i) cal1[calibration_addr_i] <= calibration_data_i;
                else cal0[calibration_addr_i] <= calibration_data_i;
            end
            if (calibration_commit_i) active_bank <= calibration_load_bank_i;
        end
    end
endmodule
