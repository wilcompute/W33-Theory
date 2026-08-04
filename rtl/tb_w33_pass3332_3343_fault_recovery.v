`timescale 1ns/1ps
module tb_w33_pass3332_3343_fault_recovery;
  reg [4:0] observed; reg [3:0] tag; wire [4:0] corrected; wire valid,changed; wire [1:0] distance;
  reg [3:0] state; reg op,fault_is_interlayer,fault_layer;
  wire [3:0] next_state; wire [4:0] q5_current,q5_target,hop1,hop2; wire [1:0] route_length;
  integer x,mask,weight,cases;
  w33_envelope_clebsch_recovery dec(.observed(observed),.axis_tag(tag),.corrected(corrected),.valid(valid),.changed(changed),.distance(distance));
  w33_q5_single_fault_router router(.state(state),.op(op),.fault_is_interlayer(fault_is_interlayer),.fault_layer(fault_layer),.next_state(next_state),.q5_current(q5_current),.q5_target(q5_target),.hop1(hop1),.hop2(hop2),.route_length(route_length));
  function is_env; input integer y; begin case(y)
    0,1,2,3,4,5,6,8,10,11,12,13,16,17,19,20,22,24,25,26,29,30:is_env=1; default:is_env=0; endcase end endfunction
  function integer pop5; input integer y; begin pop5=(y&1)+((y>>1)&1)+((y>>2)&1)+((y>>3)&1)+((y>>4)&1); end endfunction
  initial begin
    cases=0;
    for (x=0;x<32;x=x+1) if (is_env(x)) begin
      tag = x[4] ? ~x[3:0] : x[3:0];
      for(mask=0;mask<32;mask=mask+1) begin
        weight=pop5(mask);
        if(weight<=2) begin
          observed=x^mask; #1;
          if(!valid || corrected!==x[4:0] || distance!==weight[1:0]) begin $display("FAIL recovery x=%0d mask=%0d",x,mask); $fatal; end
          cases=cases+1;
        end
      end
    end
    for(op=0;op<2;op=op+1) for(state=0;state<16;state=state+1) begin
      fault_is_interlayer=0; fault_layer=0; #1;
      if(q5_current[4]!==1'b1 || q5_target[4]!==1'b1 || route_length>2) $fatal;
      fault_layer=1; #1;
      if(q5_current[4]!==1'b0 || q5_target[4]!==1'b0 || route_length>2) $fatal;
      fault_is_interlayer=1; #1;
      if(q5_current[4]!==1'b0 || q5_target[4]!==1'b0 || route_length>2) $fatal;
    end
    if(cases!=352) $fatal;
    $display("PASS Clebsch recovery cases=352 and mirrored single-fault routes=96");
    $finish;
  end
endmodule
