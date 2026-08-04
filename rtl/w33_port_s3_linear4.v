// Passes 3286-3295: natural four-bit linear controller for V4 OA ports.
// state={b[1:0],a[1:0]} encodes (a,b,a+b); op=0 is R, op=1 is S.
module w33_port_s3_linear4(input wire [3:0] state,input wire op,output wire [3:0] next_state);
  wire a0=state[0],a1=state[1],b0=state[2],b1=state[3];
  assign next_state=op ? {a1^b1,a0^b0,a1,a0}:{a1,a0,a1^b1,a0^b0};
endmodule
