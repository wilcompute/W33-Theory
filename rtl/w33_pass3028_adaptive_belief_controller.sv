// Pass 3028: adaptive posterior/stopping core for a collision class of size <= 3.
//
// Calibrated log-likelihood increments are supplied by a separate sensor LUT.  This core
// stores three hypothesis scores, applies one observation, compares the top-two gap to a
// programmable stop threshold, and requests at most two escalation tests.  It is a
// synthesizable protocol core, not the complete 1,436-class ROM or a measured decoder.
module w33_pass3028_adaptive_belief_controller #(
    parameter SCORE_W = 18,
    parameter TEST_W  = 7
) (
    input  logic                       clk,
    input  logic                       rst_n,
    input  logic                       load_class,
    input  logic [1:0]                 class_size,
    input  logic signed [SCORE_W-1:0]  prior0,
    input  logic signed [SCORE_W-1:0]  prior1,
    input  logic signed [SCORE_W-1:0]  prior2,
    input  logic signed [SCORE_W-1:0]  stop_gap,
    input  logic [TEST_W-1:0]          first_test,
    input  logic [TEST_W-1:0]          second_test,
    input  logic                       observation_valid,
    input  logic signed [SCORE_W-1:0]  ll0,
    input  logic signed [SCORE_W-1:0]  ll1,
    input  logic signed [SCORE_W-1:0]  ll2,
    output logic                       busy,
    output logic                       request_valid,
    output logic [TEST_W-1:0]          requested_test,
    output logic                       stop_valid,
    output logic [1:0]                 decision,
    output logic [1:0]                 probes_used
);
    typedef enum logic [1:0] {IDLE, WAIT_OBSERVATION, EVALUATE} state_t;
    state_t state;
    logic [1:0] size_q;
    logic signed [SCORE_W-1:0] score0, score1, score2;
    logic signed [SCORE_W-1:0] threshold_q;
    logic [TEST_W-1:0] first_q, second_q;

    logic signed [SCORE_W-1:0] top_score, runner_score;
    logic [1:0] top_index;

    always_comb begin
        top_score = score0;
        top_index = 2'd0;
        runner_score = (size_q > 1) ? score1 : {1'b1,{(SCORE_W-1){1'b0}}};
        if ((size_q > 1) && (score1 > top_score)) begin
            runner_score = top_score;
            top_score = score1;
            top_index = 2'd1;
        end
        if (size_q > 2) begin
            if (score2 > top_score) begin
                runner_score = top_score;
                top_score = score2;
                top_index = 2'd2;
            end else if (score2 > runner_score) begin
                runner_score = score2;
            end
        end
    end

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            size_q <= 0;
            score0 <= 0;
            score1 <= 0;
            score2 <= 0;
            threshold_q <= 0;
            first_q <= 0;
            second_q <= 0;
            request_valid <= 0;
            requested_test <= 0;
            stop_valid <= 0;
            decision <= 0;
            probes_used <= 0;
        end else begin
            request_valid <= 1'b0;
            stop_valid <= 1'b0;
            case (state)
                IDLE: begin
                    if (load_class) begin
                        size_q <= class_size;
                        score0 <= prior0;
                        score1 <= prior1;
                        score2 <= prior2;
                        threshold_q <= stop_gap;
                        first_q <= first_test;
                        second_q <= second_test;
                        probes_used <= 0;
                        request_valid <= 1'b1;
                        requested_test <= first_test;
                        state <= WAIT_OBSERVATION;
                    end
                end
                WAIT_OBSERVATION: begin
                    if (observation_valid) begin
                        score0 <= score0 + ll0;
                        score1 <= score1 + ll1;
                        score2 <= score2 + ll2;
                        probes_used <= probes_used + 1'b1;
                        state <= EVALUATE;
                    end
                end
                EVALUATE: begin
                    if ((top_score - runner_score >= threshold_q) || (probes_used >= 2)) begin
                        stop_valid <= 1'b1;
                        decision <= top_index;
                        state <= IDLE;
                    end else begin
                        request_valid <= 1'b1;
                        requested_test <= second_q;
                        state <= WAIT_OBSERVATION;
                    end
                end
                default: state <= IDLE;
            endcase
        end
    end

    assign busy = (state != IDLE);
endmodule
