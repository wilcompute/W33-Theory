// Passes 3135 and 3139: fixed-point D4 Fourier prediction fused with the
// future-action causal-state controller, plus an isolated multi-context wrapper.
//
// The five gains are Q1.15 approximations to 43/50, 22/25, 9/10, 89/100,
// and 89/100.  This block performs only the linear prediction step.  Bayesian
// evidence multiplication, normalization, and the generated 470-state ROM remain
// explicit interfaces rather than being hidden behind an incorrect linear claim.
module w33_pass3135_fourier_causal_controller #(
    parameter integer W = 18
) (
    input  logic clk,
    input  logic rst,
    input  logic valid_i,
    input  logic signed [W-1:0] lane0_i,
    input  logic signed [W-1:0] lane1_i,
    input  logic signed [W-1:0] lane2_i,
    input  logic signed [W-1:0] lane3_i,
    input  logic signed [W-1:0] lane4_i,
    input  logic [8:0] next_causal_state_i,
    input  logic [3:0] next_action_i,
    output logic signed [W-1:0] lane0_o,
    output logic signed [W-1:0] lane1_o,
    output logic signed [W-1:0] lane2_o,
    output logic signed [W-1:0] lane3_o,
    output logic signed [W-1:0] lane4_o,
    output logic [8:0] causal_state_o,
    output logic [3:0] action_o,
    output logic stop_o
);
    localparam logic signed [15:0] C0 = 16'sd28180; // 0.85998535
    localparam logic signed [15:0] C1 = 16'sd28836; // 0.88000488
    localparam logic signed [15:0] C2 = 16'sd29491; // 0.89999390
    localparam logic signed [15:0] C3 = 16'sd29164; // 0.89001465
    localparam logic signed [15:0] C4 = 16'sd29164;

    logic signed [W+15:0] p0, p1, p2, p3, p4;
    always_comb begin
        p0 = $signed(lane0_i) * $signed(C0);
        p1 = $signed(lane1_i) * $signed(C1);
        p2 = $signed(lane2_i) * $signed(C2);
        p3 = $signed(lane3_i) * $signed(C3);
        p4 = $signed(lane4_i) * $signed(C4);
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            lane0_o <= '0; lane1_o <= '0; lane2_o <= '0;
            lane3_o <= '0; lane4_o <= '0;
            causal_state_o <= '0;
            action_o <= '0;
            stop_o <= 1'b1;
        end else if (valid_i) begin
            lane0_o <= p0 >>> 15;
            lane1_o <= p1 >>> 15;
            lane2_o <= p2 >>> 15;
            lane3_o <= p3 >>> 15;
            lane4_o <= p4 >>> 15;
            causal_state_o <= next_causal_state_i;
            action_o <= next_action_i;
            stop_o <= (next_action_i == 4'd0);
        end
    end
endmodule

// Cartesian-product context storage.  Only the selected guest can change on a
// dispatch; the shared Fourier datapath is read-only with respect to every guest.
module w33_pass3139_belief_hypervisor #(
    parameter integer NCTX = 4,
    parameter integer CTXW = (NCTX <= 2) ? 1 : $clog2(NCTX)
) (
    input  logic clk,
    input  logic rst,
    input  logic valid_i,
    input  logic [CTXW-1:0] ctx_i,
    input  logic [8:0] next_state_i,
    input  logic [CTXW-1:0] probe_ctx_i,
    output logic [8:0] selected_state_o,
    output logic [8:0] probe_state_o
);
    logic [8:0] state_mem [0:NCTX-1];
    integer k;
    always_ff @(posedge clk) begin
        if (rst) begin
            for (k=0;k<NCTX;k=k+1) state_mem[k] <= '0;
        end else if (valid_i) begin
            state_mem[ctx_i] <= next_state_i;
        end
    end
    always_comb begin
        selected_state_o = state_mem[ctx_i];
        probe_state_o = state_mem[probe_ctx_i];
    end
endmodule
