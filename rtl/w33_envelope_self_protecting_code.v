// Passes 3388-3399: self-protecting envelope codes.
// Nonlinear code: 22 envelope states in 12 bits, exact d_min=5, seven parity bits are minimal.
// Linear code: all 32 five-bit words in 13 bits, exact d_min=5, eight parity bits are minimal.
module w33_envelope_nonlinear12_encode(
  input wire [4:0] state, output reg [11:0] codeword, output reg valid);
  reg [6:0] parity;
  always @* begin
    parity=7'd0; valid=1'b0;
    case(state)
      5'd0: begin parity=7'd0; valid=1'b1; end
      5'd1: begin parity=7'd99; valid=1'b1; end
      5'd2: begin parity=7'd60; valid=1'b1; end
      5'd3: begin parity=7'd27; valid=1'b1; end
      5'd4: begin parity=7'd89; valid=1'b1; end
      5'd5: begin parity=7'd45; valid=1'b1; end
      5'd6: begin parity=7'd71; valid=1'b1; end
      5'd8: begin parity=7'd127; valid=1'b1; end
      5'd10: begin parity=7'd74; valid=1'b1; end
      5'd11: begin parity=7'd100; valid=1'b1; end
      5'd12: begin parity=7'd38; valid=1'b1; end
      5'd13: begin parity=7'd82; valid=1'b1; end
      5'd16: begin parity=7'd15; valid=1'b1; end
      5'd17: begin parity=7'd54; valid=1'b1; end
      5'd19: begin parity=7'd85; valid=1'b1; end
      5'd20: begin parity=7'd106; valid=1'b1; end
      5'd22: begin parity=7'd18; valid=1'b1; end
      5'd24: begin parity=7'd112; valid=1'b1; end
      5'd25: begin parity=7'd73; valid=1'b1; end
      5'd26: begin parity=7'd35; valid=1'b1; end
      5'd29: begin parity=7'd28; valid=1'b1; end
      5'd30: begin parity=7'd109; valid=1'b1; end
      default: begin parity=7'd0; valid=1'b0; end
    endcase
    codeword={parity,state};
  end
endmodule

module w33_envelope_nonlinear12_decode(
  input wire [11:0] received, output reg [4:0] state, output reg valid,
  output reg corrected, output reg [3:0] distance);
  integer i,d,best,ties; reg [4:0] best_state;
  function [3:0] pop12; input [11:0] x; integer j; begin pop12=0; for(j=0;j<12;j=j+1) pop12=pop12+x[j]; end endfunction
  function [11:0] codeword; input integer idx; begin
    case(idx)
        0: codeword={7'd0,5'd0};
        1: codeword={7'd99,5'd1};
        2: codeword={7'd60,5'd2};
        3: codeword={7'd27,5'd3};
        4: codeword={7'd89,5'd4};
        5: codeword={7'd45,5'd5};
        6: codeword={7'd71,5'd6};
        7: codeword={7'd127,5'd8};
        8: codeword={7'd74,5'd10};
        9: codeword={7'd100,5'd11};
        10: codeword={7'd38,5'd12};
        11: codeword={7'd82,5'd13};
        12: codeword={7'd15,5'd16};
        13: codeword={7'd54,5'd17};
        14: codeword={7'd85,5'd19};
        15: codeword={7'd106,5'd20};
        16: codeword={7'd18,5'd22};
        17: codeword={7'd112,5'd24};
        18: codeword={7'd73,5'd25};
        19: codeword={7'd35,5'd26};
        20: codeword={7'd28,5'd29};
        21: codeword={7'd109,5'd30};
      default: codeword=12'd0;
    endcase
  end endfunction
  function [4:0] logical_state; input integer idx; begin
    case(idx)
        0: logical_state=5'd0;
        1: logical_state=5'd1;
        2: logical_state=5'd2;
        3: logical_state=5'd3;
        4: logical_state=5'd4;
        5: logical_state=5'd5;
        6: logical_state=5'd6;
        7: logical_state=5'd8;
        8: logical_state=5'd10;
        9: logical_state=5'd11;
        10: logical_state=5'd12;
        11: logical_state=5'd13;
        12: logical_state=5'd16;
        13: logical_state=5'd17;
        14: logical_state=5'd19;
        15: logical_state=5'd20;
        16: logical_state=5'd22;
        17: logical_state=5'd24;
        18: logical_state=5'd25;
        19: logical_state=5'd26;
        20: logical_state=5'd29;
        21: logical_state=5'd30;
      default: logical_state=5'd0;
    endcase
  end endfunction
  always @* begin
    best=13; ties=0; best_state=0;
    for(i=0;i<22;i=i+1) begin
      d=pop12(received ^ codeword(i));
      if(d<best) begin best=d; ties=1; best_state=logical_state(i); end
      else if(d==best) ties=ties+1;
    end
    state=best_state; distance=best[3:0]; valid=(best<=2 && ties==1); corrected=valid && (best!=0);
  end
endmodule

module w33_linear13_encode(
  input wire [4:0] state, output wire [12:0] codeword);
  wire [7:0] parity;
  assign parity[0]=^(state & 5'b00111);
  assign parity[1]=^(state & 5'b11011);
  assign parity[2]=^(state & 5'b10101);
  assign parity[3]=^(state & 5'b01001);
  assign parity[4]=^(state & 5'b10110);
  assign parity[5]=^(state & 5'b01010);
  assign parity[6]=^(state & 5'b01100);
  assign parity[7]=^(state & 5'b10000);
  assign codeword={parity,state};
endmodule

module w33_linear13_decode(
  input wire [12:0] received, output reg [4:0] state, output reg valid,
  output reg corrected, output reg [3:0] distance);
  integer i,d,best,ties; reg [4:0] best_state; reg [7:0] p;
  function [3:0] pop13; input [12:0] x; integer j; begin pop13=0; for(j=0;j<13;j=j+1) pop13=pop13+x[j]; end endfunction
  function [7:0] parity_of; input [4:0] s; begin
    parity_of[0]=^(s & 5'b00111);
    parity_of[1]=^(s & 5'b11011);
    parity_of[2]=^(s & 5'b10101);
    parity_of[3]=^(s & 5'b01001);
    parity_of[4]=^(s & 5'b10110);
    parity_of[5]=^(s & 5'b01010);
    parity_of[6]=^(s & 5'b01100);
    parity_of[7]=^(s & 5'b10000);
  end endfunction
  always @* begin
    best=14; ties=0; best_state=0;
    for(i=0;i<32;i=i+1) begin
      d=pop13(received ^ {parity_of(i[4:0]),i[4:0]});
      if(d<best) begin best=d; ties=1; best_state=i[4:0]; end
      else if(d==best) ties=ties+1;
    end
    state=best_state; distance=best[3:0]; valid=(best<=2 && ties==1); corrected=valid && (best!=0);
  end
endmodule
