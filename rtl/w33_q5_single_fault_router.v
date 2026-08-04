// Passes 3334-3335: exact mirrored-Q4 single-fault failover wrapper.
// A layer-local vertex or edge fault is avoided by routing the full dispatch
// in the opposite Q4 layer.  An interlayer-edge fault is avoided by staying
// in layer zero.  The underlying route remains the optimal 34-hop/dilation-2
// signature schedule.
module w33_q5_single_fault_router(
    input  wire [3:0] state,
    input  wire       op,
    input  wire       fault_is_interlayer,
    input  wire       fault_layer,
    output wire [3:0] next_state,
    output wire [4:0] q5_current,
    output wire [4:0] q5_target,
    output wire [4:0] hop1,
    output wire [4:0] hop2,
    output wire [1:0] route_length
);
  wire [3:0] q4_current, q4_target, q4_hop1, q4_hop2;
  wire safe_layer = fault_is_interlayer ? 1'b0 : ~fault_layer;
  w33_signature_q4_router base(
    .state(state), .op(op), .next_state(next_state),
    .q4_current(q4_current), .q4_target(q4_target),
    .hop1(q4_hop1), .hop2(q4_hop2), .route_length(route_length)
  );
  assign q5_current={safe_layer,q4_current};
  assign q5_target ={safe_layer,q4_target};
  assign hop1      ={safe_layer,q4_hop1};
  assign hop2      ={safe_layer,q4_hop2};
endmodule
