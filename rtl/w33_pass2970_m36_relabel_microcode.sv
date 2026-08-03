// Pass 2970: nine-gate deep-M36 branch after static output-wire relabeling.
module w33_pass2970_m36_relabel_microcode(
  input  logic [3:0] pc,
  output logic [2:0] opcode, // 0=NOP,1=H,2=CX,3=MZ
  output logic [1:0] q0,
  output logic [1:0] q1,
  output logic       expected
);
always_comb begin
  opcode=3'd0; q0=2'd0; q1=2'd0; expected=1'b0;
  unique case(pc)
    4'd0: begin opcode=3'd2; q0=2'd0; q1=2'd1; end
    4'd1: begin opcode=3'd2; q0=2'd0; q1=2'd2; end
    4'd2: begin opcode=3'd1; q0=2'd0; end
    4'd3: begin opcode=3'd2; q0=2'd1; q1=2'd3; end
    4'd4: begin opcode=3'd1; q0=2'd1; end
    4'd5: begin opcode=3'd2; q0=2'd1; q1=2'd3; end
    4'd6: begin opcode=3'd2; q0=2'd3; q1=2'd2; end
    4'd7: begin opcode=3'd2; q0=2'd0; q1=2'd3; end
    4'd8: begin opcode=3'd1; q0=2'd1; end
    4'd9: begin opcode=3'd3; q0=2'd2; expected=1'b0; end
    4'd10:begin opcode=3'd3; q0=2'd3; expected=1'b1; end
    default: ;
  endcase
end
endmodule
