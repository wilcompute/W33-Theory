// Pass 3169: exact 48,826-hypothesis enumerator for the sparse D4 posterior.
module w33_pass3169_hypothesis_enumerator(
  input logic clk,input logic rst,input logic start_i,input logic advance_i,
  output logic valid_o,output logic done_o,output logic [15:0] hypothesis_index_o,
  output logic unary1_valid_o,output logic [8:0] unary1_index_o,
  output logic unary2_valid_o,output logic [8:0] unary2_index_o,
  output logic correction_valid_o,output logic [11:0] correction_index_o,
  output logic [5:0] edge1_o,output logic [2:0] label1_o,
  output logic [5:0] edge2_o,output logic [2:0] label2_o
);
  logic [1:0] kind; // 0 no fault,1 single,2 double
  logic [5:0] e1,e2;logic [2:0] l1,l2;logic pair_valid;logic [6:0] pair_index;
  always_comb begin
    pair_valid=0;pair_index=0;
    case({e1,e2})
        12'h8e6: begin pair_valid=1'b1;pair_index=7'd0;end
        12'h8e9: begin pair_valid=1'b1;pair_index=7'd1;end
        12'h9a9: begin pair_valid=1'b1;pair_index=7'd2;end
        12'h4d7: begin pair_valid=1'b1;pair_index=7'd3;end
        12'h4e6: begin pair_valid=1'b1;pair_index=7'd4;end
        12'h5e6: begin pair_valid=1'b1;pair_index=7'd5;end
        12'h7a1: begin pair_valid=1'b1;pair_index=7'd6;end
        12'h7a5: begin pair_valid=1'b1;pair_index=7'd7;end
        12'h865: begin pair_valid=1'b1;pair_index=7'd8;end
        12'h495: begin pair_valid=1'b1;pair_index=7'd9;end
        12'h4a0: begin pair_valid=1'b1;pair_index=7'd10;end
        12'h560: begin pair_valid=1'b1;pair_index=7'd11;end
        12'h085: begin pair_valid=1'b1;pair_index=7'd12;end
        12'h09a: begin pair_valid=1'b1;pair_index=7'd13;end
        12'h15a: begin pair_valid=1'b1;pair_index=7'd14;end
        12'h007: begin pair_valid=1'b1;pair_index=7'd15;end
        12'h00f: begin pair_valid=1'b1;pair_index=7'd16;end
        12'h1cf: begin pair_valid=1'b1;pair_index=7'd17;end
        12'h24b: begin pair_valid=1'b1;pair_index=7'd18;end
        12'h252: begin pair_valid=1'b1;pair_index=7'd19;end
        12'h2d2: begin pair_valid=1'b1;pair_index=7'd20;end
        12'h28c: begin pair_valid=1'b1;pair_index=7'd21;end
        12'h299: begin pair_valid=1'b1;pair_index=7'd22;end
        12'h319: begin pair_valid=1'b1;pair_index=7'd23;end
        12'h61c: begin pair_valid=1'b1;pair_index=7'd24;end
        12'h621: begin pair_valid=1'b1;pair_index=7'd25;end
        12'h721: begin pair_valid=1'b1;pair_index=7'd26;end
        12'h0c8: begin pair_valid=1'b1;pair_index=7'd27;end
        12'h0e2: begin pair_valid=1'b1;pair_index=7'd28;end
        12'h222: begin pair_valid=1'b1;pair_index=7'd29;end
        12'h456: begin pair_valid=1'b1;pair_index=7'd30;end
        12'h45c: begin pair_valid=1'b1;pair_index=7'd31;end
        12'h59c: begin pair_valid=1'b1;pair_index=7'd32;end
        12'h862: begin pair_valid=1'b1;pair_index=7'd33;end
        12'h86c: begin pair_valid=1'b1;pair_index=7'd34;end
        12'h8ac: begin pair_valid=1'b1;pair_index=7'd35;end
        12'h38f: begin pair_valid=1'b1;pair_index=7'd36;end
        12'h3aa: begin pair_valid=1'b1;pair_index=7'd37;end
        12'h3ea: begin pair_valid=1'b1;pair_index=7'd38;end
        12'h2cd: begin pair_valid=1'b1;pair_index=7'd39;end
        12'h2df: begin pair_valid=1'b1;pair_index=7'd40;end
        12'h35f: begin pair_valid=1'b1;pair_index=7'd41;end
        12'h042: begin pair_valid=1'b1;pair_index=7'd42;end
        12'h051: begin pair_valid=1'b1;pair_index=7'd43;end
        12'h091: begin pair_valid=1'b1;pair_index=7'd44;end
        12'h6dd: begin pair_valid=1'b1;pair_index=7'd45;end
        12'h6eb: begin pair_valid=1'b1;pair_index=7'd46;end
        12'h76b: begin pair_valid=1'b1;pair_index=7'd47;end
        12'h290: begin pair_valid=1'b1;pair_index=7'd48;end
        12'h29d: begin pair_valid=1'b1;pair_index=7'd49;end
        12'h41d: begin pair_valid=1'b1;pair_index=7'd50;end
        12'h517: begin pair_valid=1'b1;pair_index=7'd51;end
        12'h529: begin pair_valid=1'b1;pair_index=7'd52;end
        12'h5e9: begin pair_valid=1'b1;pair_index=7'd53;end
        12'h65b: begin pair_valid=1'b1;pair_index=7'd54;end
        12'h664: begin pair_valid=1'b1;pair_index=7'd55;end
        12'h6e4: begin pair_valid=1'b1;pair_index=7'd56;end
        12'h006: begin pair_valid=1'b1;pair_index=7'd57;end
        12'h00e: begin pair_valid=1'b1;pair_index=7'd58;end
        12'h18e: begin pair_valid=1'b1;pair_index=7'd59;end
        12'h69c: begin pair_valid=1'b1;pair_index=7'd60;end
        12'h6a8: begin pair_valid=1'b1;pair_index=7'd61;end
        12'h728: begin pair_valid=1'b1;pair_index=7'd62;end
        12'h0c4: begin pair_valid=1'b1;pair_index=7'd63;end
        12'h0de: begin pair_valid=1'b1;pair_index=7'd64;end
        12'h11e: begin pair_valid=1'b1;pair_index=7'd65;end
        12'h7e0: begin pair_valid=1'b1;pair_index=7'd66;end
        12'h7e7: begin pair_valid=1'b1;pair_index=7'd67;end
        12'h827: begin pair_valid=1'b1;pair_index=7'd68;end
      default:begin pair_valid=0;pair_index=0;end
    endcase
    unary1_valid_o=(kind!=0);unary2_valid_o=(kind==2);
    unary1_index_o=e1*7+l1;unary2_index_o=e2*7+l2;
    correction_valid_o=(kind==2)&&pair_valid;
    correction_index_o=pair_index*49+l1*7+l2;
    edge1_o=e1;edge2_o=e2;label1_o=l1;label2_o=l2;
  end
  always_ff @(posedge clk) begin
    if(rst) begin valid_o<=0;done_o<=0;hypothesis_index_o<=0;kind<=0;e1<=0;e2<=1;l1<=0;l2<=0;end
    else begin
      done_o<=0;
      if(start_i) begin valid_o<=1;hypothesis_index_o<=0;kind<=0;e1<=0;e2<=1;l1<=0;l2<=0;end
      else if(valid_o&&advance_i) begin
        if(hypothesis_index_o==16'd48825) begin valid_o<=0;done_o<=1;end
        else begin
          hypothesis_index_o<=hypothesis_index_o+1'b1;
          if(kind==0) begin kind<=1;e1<=0;l1<=0;end
          else if(kind==1) begin
            if(e1==44&&l1==6) begin kind<=2;e1<=0;e2<=1;l1<=0;l2<=0;end
            else if(l1==6) begin l1<=0;e1<=e1+1'b1;end else l1<=l1+1'b1;
          end else begin
            if(l2<6) l2<=l2+1'b1;
            else if(l1<6) begin l2<=0;l1<=l1+1'b1;end
            else if(e2<44) begin l1<=0;l2<=0;e2<=e2+1'b1;end
            else begin l1<=0;l2<=0;e1<=e1+1'b1;e2<=e1+2'd2;end
          end
        end
      end
    end
  end
endmodule
