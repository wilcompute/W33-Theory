`timescale 1ns/1ps
module tb_w33_signature_q4_router;
  reg [3:0] state;
  reg op;
  wire [3:0] next_state, q4_current, q4_target, hop1, hop2;
  wire [1:0] route_length;
  integer s, o, total, max_route;

  w33_signature_q4_router dut(
    .state(state), .op(op), .next_state(next_state),
    .q4_current(q4_current), .q4_target(q4_target),
    .hop1(hop1), .hop2(hop2), .route_length(route_length)
  );

  function integer hd4;
    input [3:0] a;
    input [3:0] b;
    reg [3:0] d;
    begin
      d=a^b;
      hd4=d[0]+d[1]+d[2]+d[3];
    end
  endfunction

  initial begin
    total=0;
    max_route=0;
    for (o=0;o<2;o=o+1) begin
      for (s=0;s<16;s=s+1) begin
        state=s[3:0];
        op=o[0:0];
        #1;
        if (route_length !== hd4(q4_current,q4_target)) begin
          $display("FAIL route length state=%0d op=%0d",s,o);
          $fatal;
        end
        if (route_length==0) begin
          if (hop1!==q4_target || hop2!==q4_target) $fatal;
        end else if (route_length==1) begin
          if (hop1!==q4_target || hop2!==q4_target) $fatal;
          if (hd4(q4_current,hop1)!==1) $fatal;
        end else if (route_length==2) begin
          if (hd4(q4_current,hop1)!==1) $fatal;
          if (hd4(hop1,hop2)!==1) $fatal;
          if (hop2!==q4_target) $fatal;
        end else begin
          $display("FAIL dilation state=%0d op=%0d len=%0d",s,o,route_length);
          $fatal;
        end
        total=total+route_length;
        if (route_length>max_route) max_route=route_length;
      end
    end
    if (total!==34 || max_route!==2) begin
      $display("FAIL total=%0d max=%0d",total,max_route);
      $fatal;
    end
    $display("PASS signature Q4 router total_hops=34 dilation=2");
    $finish;
  end
endmodule
