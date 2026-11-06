`timescale 1ns/1ps
`default_nettype none
module tb_w33_pass3216_3223_runtime_reset_proof;
  reg clk=0;always #5 clk=~clk;
  reg rst=1;
  reg [9:0] state=0;wire [101:0] word;wire [79:0] children;wire [7:0] mask;
  wire [5:0] hist;wire [6:0] action;wire terminal;
  reg marker=0,reset_request=0,reset_authorized=0,root_valid=0;
  wire locked,reset_pulse,denied;
  reg complete_runtime=0,complete_m36=0,independent=0;
  reg [255:0] expected=0,computed=0;wire root_match,runtime_promote,m36_authorize;
  reg [1:0] requested=0;reg low_placed=0,low_calibrated=0,fast_placed=0,fast_calibrated=0;
  wire [1:0] selected;wire fallback;

  w33_pass3216_curvature_rom rom(.clk(clk),.state_i(state),.word_o(word),
    .children_o(children),.valid_mask_o(mask),.curvature_histogram_o(hist),
    .action_o(action),.terminal_o(terminal));
  w33_pass3220_reset_supervisor supervisor(.clk(clk),.rst(rst),
    .phase_marker_accept_i(marker),.belief_reset_request_i(reset_request),
    .belief_reset_authorized_i(reset_authorized),.proof_root_valid_i(root_valid),
    .phase_locked_o(locked),.belief_reset_pulse_o(reset_pulse),.reset_denied_o(denied));
  w33_pass3217_proof_root_authorizer auth(.complete_runtime_i(complete_runtime),
    .complete_m36_i(complete_m36),.independent_cert_pass_i(independent),
    .expected_root_i(expected),.computed_root_i(computed),.root_match_o(root_match),
    .runtime_promote_o(runtime_promote),.m36_authorize_o(m36_authorize));
  w33_pass3215_tri_isa_evidence_gate isa(.requested_mode_i(requested),
    .low4_placed_i(low_placed),.low4_calibrated_i(low_calibrated),
    .fast6_placed_i(fast_placed),.fast6_calibrated_i(fast_calibrated),
    .selected_mode_o(selected),.fallback_o(fallback));

  task tick;begin @(negedge clk);@(posedge clk);#1;end endtask
  initial begin
    repeat(3)tick();rst=0;
    state=0;tick();
    if(^word===1'bx) $fatal(1,"quotient ROM state 0 is unknown");
    if(action>7'd127) $fatal(1,"invalid action width");
    state=10'd875;tick();
    if(^word===1'bx) $fatal(1,"quotient ROM state 875 is unknown");
    state=10'd900;tick();
    if(word!==102'd0) $fatal(1,"out-of-range ROM address did not fail closed");

    // Phase synchronization must not reset belief by itself.
    marker=1;tick();marker=0;
    if(!locked || reset_pulse || denied) $fatal(1,"phase marker contract failed");
    reset_request=1;tick();reset_request=0;
    if(reset_pulse || !denied) $fatal(1,"unauthorized belief reset was not denied");
    reset_authorized=1;root_valid=1;reset_request=1;tick();reset_request=0;
    if(!reset_pulse || denied) $fatal(1,"authorized proof-root reset failed");
    tick();if(reset_pulse) $fatal(1,"reset pulse persisted");

    expected=256'h1234;computed=256'h1234;complete_runtime=1;complete_m36=1;independent=1;#1;
    if(!root_match || !runtime_promote || !m36_authorize) $fatal(1,"valid root rejected");
    computed=256'h4321;#1;
    if(root_match || runtime_promote || m36_authorize) $fatal(1,"mismatched root promoted");

    requested=2;#1;
    if(selected!=0 || !fallback) $fatal(1,"unplaced fast6 did not fail closed");
    fast_placed=1;#1;
    if(selected!=0 || !fallback) $fatal(1,"uncalibrated fast6 did not fail closed");
    fast_calibrated=1;#1;
    if(selected!=2 || fallback) $fatal(1,"placed calibrated fast6 rejected");
    requested=1;low_placed=1;low_calibrated=1;#1;
    if(selected!=1 || fallback) $fatal(1,"placed calibrated low4 rejected");

    $display("PASS quotient ROM, synchronization rank boundary, proof root and tri-ISA gate");
    $finish;
  end
endmodule
`default_nettype wire
