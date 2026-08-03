// Pass 2767: fail-closed M36 preparation/witness/mapping/injection controller.
module w33_pass2767_m36_pipeline(
  input logic clk, rst, start,
  input logic [5:0] ray_id,
  input logic prep_ack,
  input logic witness_pass,
  input logic map_valid,
  input logic inject_ack,
  output logic busy, done, error,
  output logic prep_req, witness_req, map_required, inject_req,
  output logic [1:0] dark_mode, grade,
  output logic [2:0] phase6_0, phase6_1, phase6_2, phase6_3
);
  logic valid;
  logic [2:0] state;
  w33_pass2767_m36_factory rom(
    .ray_id(ray_id),.valid(valid),.dark_mode(dark_mode),.grade(grade),
    .phase6_0(phase6_0),.phase6_1(phase6_1),.phase6_2(phase6_2),.phase6_3(phase6_3)
  );
  always_ff @(posedge clk) begin
    if(rst) begin
      state<=0;busy<=0;done<=0;error<=0;prep_req<=0;witness_req<=0;map_required<=0;inject_req<=0;
    end else begin
      done<=0;error<=0;
      case(state)
        0: if(start) begin
          if(!valid) begin error<=1;done<=1; end
          else begin state<=1;busy<=1;prep_req<=1; end
        end
        1: if(prep_ack) begin prep_req<=0;witness_req<=1;state<=2; end
        2: begin
          witness_req<=0;
          if(!witness_pass) begin error<=1;done<=1;busy<=0;state<=0; end
          else if(!map_valid) begin map_required<=1;state<=3; end
          else begin inject_req<=1;state<=4; end
        end
        3: if(map_valid) begin map_required<=0;inject_req<=1;state<=4; end
        4: if(inject_ack) begin inject_req<=0;busy<=0;done<=1;state<=0; end
        default: begin state<=0;busy<=0;error<=1;done<=1; end
      endcase
    end
  end
endmodule
