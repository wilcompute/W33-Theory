// Passes 3175-3183: typed curvature, epoch, envelope and routed-utility contracts.
module w33_pass3175_curvature_accumulator(
 input logic clk,input logic rst,input logic valid_i,input logic [1:0] class_i,input logic [15:0] weight_i,
 output logic [31:0] none_o,output logic [31:0] flat_o,output logic [31:0] curved_o);
 always_ff @(posedge clk) begin
  if(rst) begin none_o<=0;flat_o<=0;curved_o<=0;end
  else if(valid_i) case(class_i)
   2'd0:none_o<=none_o+weight_i;2'd1:flat_o<=flat_o+weight_i;2'd2:curved_o<=curved_o+weight_i;default:;
  endcase
 end
endmodule

module w33_pass3178_three_edit_epoch_decoder(
 input logic valid_i,input logic [3:0] received_length_i,input logic [47:0] phase_symbol_counts_i,
 output logic locked_o,output logic ambiguous_o,output logic [3:0] phase_o);
 integer p;integer c;integer mn;integer mx;integer d;integer hits;
 always_comb begin
  locked_o=0;ambiguous_o=0;phase_o=0;hits=0;
  if(valid_i) begin
   for(p=0;p<12;p=p+1) begin
    c=phase_symbol_counts_i[p*4 +: 4];mn=(c<7)?c:7;mx=(received_length_i>7)?received_length_i:7;d=mx-mn;
    if(d<=3) begin hits=hits+1;phase_o=p[3:0];end
   end
   locked_o=(hits==1);ambiguous_o=(hits>1);
  end
 end
endmodule

module w33_pass3179_m36_envelope_gate(
 input logic digest_valid_i,input logic provenance_valid_i,input logic certification_valid_i,
 input logic witnesses_complete_i,input logic accepted_i,output logic injection_authorized_o);
 always_comb injection_authorized_o=digest_valid_i&provenance_valid_i&certification_valid_i&witnesses_complete_i&accepted_i;
endmodule

module w33_pass3181_d4_triangle_flux(
 input logic [2:0] a_i,input logic [2:0] b_i,input logic [2:0] c_i,output logic flux_o);
 function automatic logic kappa(input logic [2:0] a,input logic [2:0] b);
  logic [1:0] ia,ib;logic ja,jb;
  begin ia=a[1:0];ib=b[1:0];ja=a[2];jb=b[2];
   if(!ja&&!jb) kappa=1'b0;
   else if(!ja&&jb) kappa=ia[0];
   else if(ja&&!jb) kappa=ib[0];
   else kappa=ia[0]^ib[0];
  end
 endfunction
 always_comb flux_o=kappa(a_i,b_i)^kappa(b_i,c_i)^kappa(c_i,a_i);
endmodule

module w33_pass3180_streamed_routed_utility(
 input logic clk,input logic rst,input logic first_i,input logic valid_i,input logic last_i,input logic available_i,
 input logic [4:0] action_i,input logic [1:0] mode_i,input logic signed [31:0] utility_i,
 output logic done_o,output logic [4:0] best_action_o,output logic [1:0] best_mode_o,output logic signed [31:0] best_utility_o);
 always_ff @(posedge clk) begin
  if(rst) begin done_o<=0;best_action_o<=0;best_mode_o<=0;best_utility_o<=-32'sh7fffffff;end
  else begin
   done_o<=0;
   if(first_i) begin best_action_o<=action_i;best_mode_o<=mode_i;best_utility_o<=available_i?utility_i:-32'sh7fffffff;end
   else if(valid_i&&available_i&&utility_i>best_utility_o) begin best_action_o<=action_i;best_mode_o<=mode_i;best_utility_o<=utility_i;end
   if(valid_i&&last_i) done_o<=1;
  end
 end
endmodule
