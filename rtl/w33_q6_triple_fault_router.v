// Passes 3364-3375: four-layer Q6 exact-schedule selector.
// If at most three Q4 layers are contaminated, choose one clean layer and retain work 34/dilation 2.
module w33_q6_triple_fault_router(
 input wire [3:0] state,input wire op,input wire [3:0] bad_layers,
 output wire [3:0] next_state,output reg [5:0] physical_current,output reg [5:0] physical_target,
 output reg [1:0] selected_layer,output reg valid_layer,output wire [2:0] route_length);
 w33_signature_s3_rom4 core(.state(state),.op(op),.next_state(next_state));
 function [3:0] qmap; input [3:0] s;begin case(s)
 4'h0:qmap=4'hd;4'h1:qmap=4'h9;4'h2:qmap=4'h0;4'h3:qmap=4'h2;
 4'h4:qmap=4'h8;4'h5:qmap=4'hc;4'h6:qmap=4'h4;4'h7:qmap=4'h6;
 4'h8:qmap=4'h1;4'h9:qmap=4'h3;4'ha:qmap=4'hb;4'hb:qmap=4'hf;
 4'hc:qmap=4'h7;4'hd:qmap=4'h5;4'he:qmap=4'he;default:qmap=4'ha;endcase end endfunction
 function [2:0] pop4; input [3:0] x;begin pop4=x[0]+x[1]+x[2]+x[3];end endfunction
 assign route_length=valid_layer?pop4(qmap(state)^qmap(next_state)):3'd0;
 always @* begin
  valid_layer=1'b1;selected_layer=2'd0;
  if(!bad_layers[0])selected_layer=2'd0;else if(!bad_layers[1])selected_layer=2'd1;
  else if(!bad_layers[2])selected_layer=2'd2;else if(!bad_layers[3])selected_layer=2'd3;
  else begin selected_layer=2'd0;valid_layer=1'b0;end
  physical_current={selected_layer,qmap(state)};physical_target={selected_layer,qmap(next_state)};
 end
endmodule
