// Passes 3364-3375: optimal six-spare dynamic Q5 recovery router.
// Six fixed layer-one coordinates 0..5 are necessary and sufficient to retain
// the original 34-hop, dilation-two controller schedule after any one layer-zero state loss.
module w33_q5_dynamic_spare_router(
 input wire [3:0] state,input wire op,input wire [3:0] failed_state,
 output wire [3:0] next_state,output wire [4:0] physical_current,output wire [4:0] physical_target,
 output reg [4:0] hop1,output wire [4:0] hop2,output wire [2:0] route_length);
 w33_signature_s3_rom4 core(.state(state),.op(op),.next_state(next_state));
 function [3:0] qmap; input [3:0] s; begin case(s)
 4'h0:qmap=4'hd;4'h1:qmap=4'h9;4'h2:qmap=4'h0;4'h3:qmap=4'h2;
 4'h4:qmap=4'h8;4'h5:qmap=4'hc;4'h6:qmap=4'h4;4'h7:qmap=4'h6;
 4'h8:qmap=4'h1;4'h9:qmap=4'h3;4'ha:qmap=4'hb;4'hb:qmap=4'hf;
 4'hc:qmap=4'h7;4'hd:qmap=4'h5;4'he:qmap=4'he;default:qmap=4'ha;endcase end endfunction
 function [4:0] pmap; input [3:0] f; input [3:0] s; begin pmap={1'b0,qmap(s)}; case({f,s})
      8'h00: pmap=5'd16;
      8'h11: pmap=5'd16;
      8'h14: pmap=5'd17;
      8'h15: pmap=5'd19;
      8'haa: pmap=5'd18;
      8'hab: pmap=5'd16;
      8'hac: pmap=5'd20;
      8'hae: pmap=5'd17;
      8'haf: pmap=5'd19;
      8'ha7: pmap=5'd21;
      8'hba: pmap=5'd18;
      8'hbb: pmap=5'd16;
      8'hbc: pmap=5'd20;
      8'hbe: pmap=5'd17;
      8'hbf: pmap=5'd19;
      8'hb7: pmap=5'd21;
      8'hca: pmap=5'd20;
      8'hcb: pmap=5'd16;
      8'hcc: pmap=5'd18;
      8'hce: pmap=5'd17;
      8'hcf: pmap=5'd21;
      8'hc7: pmap=5'd19;
      8'hdd: pmap=5'd17;
      8'hd6: pmap=5'd16;
      8'hea: pmap=5'd21;
      8'heb: pmap=5'd17;
      8'hec: pmap=5'd19;
      8'hee: pmap=5'd16;
      8'hef: pmap=5'd20;
      8'he7: pmap=5'd18;
      8'hfa: pmap=5'd19;
      8'hfb: pmap=5'd17;
      8'hfc: pmap=5'd21;
      8'hfe: pmap=5'd16;
      8'hff: pmap=5'd18;
      8'hf7: pmap=5'd20;
      8'h2d: pmap=5'd21;
      8'h22: pmap=5'd16;
      8'h23: pmap=5'd18;
      8'h26: pmap=5'd20;
      8'h28: pmap=5'd17;
      8'h29: pmap=5'd19;
      8'h33: pmap=5'd16;
      8'h39: pmap=5'd17;
      8'h41: pmap=5'd17;
      8'h44: pmap=5'd16;
      8'h45: pmap=5'd18;
      8'h51: pmap=5'd19;
      8'h54: pmap=5'd17;
      8'h55: pmap=5'd16;
      8'h6d: pmap=5'd17;
      8'h66: pmap=5'd16;
      8'h7a: pmap=5'd21;
      8'h7b: pmap=5'd17;
      8'h7c: pmap=5'd19;
      8'h7e: pmap=5'd16;
      8'h7f: pmap=5'd20;
      8'h77: pmap=5'd18;
      8'h8d: pmap=5'd20;
      8'h88: pmap=5'd16;
      8'h89: pmap=5'd18;
      8'h93: pmap=5'd16;
      8'h99: pmap=5'd17;
 default:pmap={1'b0,qmap(s)};endcase end endfunction
 function [2:0] pop5; input [4:0] x; integer i; begin pop5=0;for(i=0;i<5;i=i+1)pop5=pop5+x[i];end endfunction
 function [4:0] first_step; input [4:0] a;input [4:0] b; reg [4:0] d;begin d=a^b;
  if(d[0])first_step=a^5'b00001;else if(d[1])first_step=a^5'b00010;else if(d[2])first_step=a^5'b00100;
  else if(d[3])first_step=a^5'b01000;else if(d[4])first_step=a^5'b10000;else first_step=a;end endfunction
 assign physical_current=pmap(failed_state,state);assign physical_target=pmap(failed_state,next_state);
 assign route_length=pop5(physical_current^physical_target);assign hop2=physical_target;
 always @* begin if(route_length<=1)hop1=physical_target;else hop1=first_step(physical_current,physical_target);end
endmodule
