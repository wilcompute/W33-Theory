`default_nettype none

// Pass 3216: canonical curvature-aware Moore quotient ROM.
// The generated 102-bit word packs eight 10-bit child IDs, an 8-bit outcome
// validity mask, three 2-bit curvature counts, a 7-bit action, and terminal.
module w33_pass3216_curvature_rom #(
    parameter MEMFILE="data/PART_BT3216_CURVATURE_QUOTIENT_ROM.memh"
)(
    input  wire         clk,
    input  wire [9:0]   state_i,
    output reg  [101:0] word_o,
    output wire [79:0]  children_o,
    output wire [7:0]   valid_mask_o,
    output wire [5:0]   curvature_histogram_o,
    output wire [6:0]   action_o,
    output wire         terminal_o
);
    reg [101:0] memory [0:875];
    initial $readmemh(MEMFILE,memory);
    always @(posedge clk) begin
        if (state_i < 10'd876) word_o <= memory[state_i];
        else word_o <= {102{1'b0}};
    end
    assign children_o=word_o[79:0];
    assign valid_mask_o=word_o[87:80];
    assign curvature_histogram_o=word_o[93:88];
    assign action_o=word_o[100:94];
    assign terminal_o=word_o[101];
endmodule

// Pass 3220: an epoch marker may synchronize the phase coordinate, but it is
// forbidden from silently resetting the 876-state epistemic coordinate.
module w33_pass3220_reset_supervisor(
    input  wire clk,
    input  wire rst,
    input  wire phase_marker_accept_i,
    input  wire belief_reset_request_i,
    input  wire belief_reset_authorized_i,
    input  wire proof_root_valid_i,
    output reg  phase_locked_o,
    output reg  belief_reset_pulse_o,
    output reg  reset_denied_o
);
    always @(posedge clk) begin
        if (rst) begin
            phase_locked_o<=1'b0;
            belief_reset_pulse_o<=1'b0;
            reset_denied_o<=1'b0;
        end else begin
            belief_reset_pulse_o<=1'b0;
            reset_denied_o<=1'b0;
            if (phase_marker_accept_i) phase_locked_o<=1'b1;
            if (belief_reset_request_i) begin
                if (belief_reset_authorized_i && proof_root_valid_i)
                    belief_reset_pulse_o<=1'b1;
                else reset_denied_o<=1'b1;
            end
        end
    end
endmodule

// Passes 3217/3222: compare a supplied computed root against the expected root.
// This is intentionally not a SHA-256 engine.  Completion and independent
// certification are separate required inputs.
module w33_pass3217_proof_root_authorizer(
    input  wire         complete_runtime_i,
    input  wire         complete_m36_i,
    input  wire         independent_cert_pass_i,
    input  wire [255:0] expected_root_i,
    input  wire [255:0] computed_root_i,
    output wire         root_match_o,
    output wire         runtime_promote_o,
    output wire         m36_authorize_o
);
    assign root_match_o=(expected_root_i==computed_root_i);
    assign runtime_promote_o=complete_runtime_i && root_match_o;
    assign m36_authorize_o=complete_m36_i && independent_cert_pass_i && root_match_o;
endmodule

// Pass 3215: current4 remains the fail-closed mode.  Alternative modes require
// both observed placement evidence and calibration evidence.
module w33_pass3215_tri_isa_evidence_gate(
    input  wire [1:0] requested_mode_i, // 0=current4, 1=low4, 2=fast6
    input  wire       low4_placed_i,
    input  wire       low4_calibrated_i,
    input  wire       fast6_placed_i,
    input  wire       fast6_calibrated_i,
    output reg  [1:0] selected_mode_o,
    output reg        fallback_o
);
    always @* begin
        selected_mode_o=2'd0;
        fallback_o=1'b0;
        case(requested_mode_i)
          2'd0:selected_mode_o=2'd0;
          2'd1:begin
              if(low4_placed_i && low4_calibrated_i) selected_mode_o=2'd1;
              else fallback_o=1'b1;
          end
          2'd2:begin
              if(fast6_placed_i && fast6_calibrated_i) selected_mode_o=2'd2;
              else fallback_o=1'b1;
          end
          default:fallback_o=1'b1;
        endcase
    end
endmodule

// Low-pin wrappers for HX8K evidence.  They preserve the internal logic under
// test while avoiding package-I/O failure from 102- and 512-bit interfaces.
module w33_pass3223_curvature_rom_hx8k_top(
    input wire clk,
    input wire [9:0] state_i,
    output wire signature_o
);
    wire [101:0] word;
    wire [79:0] children;
    wire [7:0] mask;
    wire [5:0] hist;
    wire [6:0] action;
    wire terminal;
    w33_pass3216_curvature_rom rom(.clk(clk),.state_i(state_i),.word_o(word),
      .children_o(children),.valid_mask_o(mask),.curvature_histogram_o(hist),
      .action_o(action),.terminal_o(terminal));
    assign signature_o=^word;
endmodule

module w33_pass3223_control_gate_hx8k_top(
    input wire clk,input wire rst,input wire marker,input wire reset_request,
    input wire reset_authorized,input wire root_valid,input wire [1:0] requested_mode,
    input wire low_ok,input wire fast_ok,output wire [3:0] status_o
);
    wire locked,reset_pulse,denied;wire [1:0] mode;wire fallback;
    w33_pass3220_reset_supervisor supervisor(.clk(clk),.rst(rst),
      .phase_marker_accept_i(marker),.belief_reset_request_i(reset_request),
      .belief_reset_authorized_i(reset_authorized),.proof_root_valid_i(root_valid),
      .phase_locked_o(locked),.belief_reset_pulse_o(reset_pulse),.reset_denied_o(denied));
    w33_pass3215_tri_isa_evidence_gate gate(.requested_mode_i(requested_mode),
      .low4_placed_i(low_ok),.low4_calibrated_i(low_ok),
      .fast6_placed_i(fast_ok),.fast6_calibrated_i(fast_ok),
      .selected_mode_o(mode),.fallback_o(fallback));
    assign status_o={denied,reset_pulse,fallback,locked} ^ {2'b00,mode};
endmodule

`default_nettype wire
