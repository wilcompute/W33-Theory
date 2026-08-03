// Pass 2767: exact M36 preparation control ROM.
module w33_pass2767_m36_factory(
  input  logic [5:0] ray_id,
  output logic       valid,
  output logic [1:0] dark_mode,
  output logic [2:0] phase6_0, phase6_1, phase6_2, phase6_3,
  output logic [1:0] grade
);
  always_comb begin
    valid=1'b1; dark_mode=2'd0;
    phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd0; phase6_3=3'd0;
    grade=2'd0;
    case (ray_id)
      6'd0: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd3; phase6_3=3'd0; grade=2'd2; end
      6'd1: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd3; phase6_3=3'd2; grade=2'd1; end
      6'd2: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd3; phase6_3=3'd4; grade=2'd1; end
      6'd3: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd5; phase6_3=3'd0; grade=2'd1; end
      6'd4: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd5; phase6_3=3'd2; grade=2'd1; end
      6'd5: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd5; phase6_3=3'd4; grade=2'd0; end
      6'd6: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd1; phase6_3=3'd0; grade=2'd1; end
      6'd7: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd1; phase6_3=3'd2; grade=2'd0; end
      6'd8: begin dark_mode=2'd0; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd1; phase6_3=3'd4; grade=2'd1; end
      6'd9: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd3; phase6_3=3'd3; grade=2'd2; end
      6'd10: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd3; phase6_3=3'd5; grade=2'd1; end
      6'd11: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd3; phase6_3=3'd1; grade=2'd1; end
      6'd12: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd5; phase6_3=3'd3; grade=2'd1; end
      6'd13: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd5; phase6_3=3'd5; grade=2'd1; end
      6'd14: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd5; phase6_3=3'd1; grade=2'd0; end
      6'd15: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd1; phase6_3=3'd3; grade=2'd1; end
      6'd16: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd1; phase6_3=3'd5; grade=2'd0; end
      6'd17: begin dark_mode=2'd1; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd1; phase6_3=3'd1; grade=2'd1; end
      6'd18: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd3; phase6_2=3'd0; phase6_3=3'd0; grade=2'd2; end
      6'd19: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd3; phase6_2=3'd0; phase6_3=3'd2; grade=2'd1; end
      6'd20: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd3; phase6_2=3'd0; phase6_3=3'd4; grade=2'd1; end
      6'd21: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd5; phase6_2=3'd0; phase6_3=3'd0; grade=2'd1; end
      6'd22: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd5; phase6_2=3'd0; phase6_3=3'd2; grade=2'd1; end
      6'd23: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd5; phase6_2=3'd0; phase6_3=3'd4; grade=2'd0; end
      6'd24: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd1; phase6_2=3'd0; phase6_3=3'd0; grade=2'd1; end
      6'd25: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd1; phase6_2=3'd0; phase6_3=3'd2; grade=2'd0; end
      6'd26: begin dark_mode=2'd2; phase6_0=3'd0; phase6_1=3'd1; phase6_2=3'd0; phase6_3=3'd4; grade=2'd1; end
      6'd27: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd0; phase6_3=3'd0; grade=2'd2; end
      6'd28: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd2; phase6_3=3'd0; grade=2'd1; end
      6'd29: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd0; phase6_2=3'd4; phase6_3=3'd0; grade=2'd1; end
      6'd30: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd2; phase6_2=3'd0; phase6_3=3'd0; grade=2'd1; end
      6'd31: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd2; phase6_2=3'd2; phase6_3=3'd0; grade=2'd1; end
      6'd32: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd2; phase6_2=3'd4; phase6_3=3'd0; grade=2'd0; end
      6'd33: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd4; phase6_2=3'd0; phase6_3=3'd0; grade=2'd1; end
      6'd34: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd4; phase6_2=3'd2; phase6_3=3'd0; grade=2'd0; end
      6'd35: begin dark_mode=2'd3; phase6_0=3'd0; phase6_1=3'd4; phase6_2=3'd4; phase6_3=3'd0; grade=2'd1; end
      default: begin valid=1'b0; grade=2'd3; end
    endcase
  end
endmodule
