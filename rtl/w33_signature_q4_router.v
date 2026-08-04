// Passes 3308-3319: deterministic optimal Q4/toroidal-knight router.
// The state placement attains the exact 34-hop lower bound over all 32
// state/opcode transitions. Every route has length at most two.
module w33_signature_q4_router(
    input  wire [3:0] state,
    input  wire       op,
    output wire [3:0] next_state,
    output reg  [3:0] q4_current,
    output reg  [3:0] q4_target,
    output reg  [3:0] hop1,
    output reg  [3:0] hop2,
    output reg  [1:0] route_length
);
  w33_signature_s3_rom4 core(.state(state), .op(op), .next_state(next_state));

  function [3:0] qmap;
    input [3:0] logical_state;
    begin
      case (logical_state)
        4'h0:qmap=4'hd; 4'h1:qmap=4'h9; 4'h2:qmap=4'h0; 4'h3:qmap=4'h2;
        4'h4:qmap=4'h8; 4'h5:qmap=4'hc; 4'h6:qmap=4'h4; 4'h7:qmap=4'h6;
        4'h8:qmap=4'h1; 4'h9:qmap=4'h3; 4'ha:qmap=4'hb; 4'hb:qmap=4'hf;
        4'hc:qmap=4'h7; 4'hd:qmap=4'h5; 4'he:qmap=4'he; 4'hf:qmap=4'ha;
        default:qmap=4'h0;
      endcase
    end
  endfunction

  function [2:0] pop4;
    input [3:0] value;
    begin
      pop4=value[0]+value[1]+value[2]+value[3];
    end
  endfunction

  always @* begin
    q4_current = qmap(state);
    q4_target  = qmap(next_state);
    hop1       = q4_target;
    hop2       = q4_target;
    route_length = pop4(q4_current ^ q4_target);

    // The five forced two-hop R transitions use one exact congestion-three
    // shortest-path selection. All S transitions and the remaining R
    // transitions are direct Q4/knight links or fixed points.
    if (!op) begin
      case (state)
        4'h5: begin hop1=4'hd; hop2=4'h9; end // c -> d -> 9
        4'h6: begin hop1=4'h6; hop2=4'h2; end // 4 -> 6 -> 2
        4'h7: begin hop1=4'h2; hop2=4'ha; end // 6 -> 2 -> a
        4'h9: begin hop1=4'h1; hop2=4'h5; end // 3 -> 1 -> 5
        4'ha: begin hop1=4'hf; hop2=4'h7; end // b -> f -> 7
        default: begin hop1=q4_target; hop2=q4_target; end
      endcase
    end
  end
endmodule
