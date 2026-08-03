// Pass 2778: four-quadrature metaplectic trace-sensor acquisition controller.
module w33_pass2778_metaplectic_sensor_controller #(
  parameter integer SHOTS_PER_QUADRATURE = 29579
)(
  input logic clk,rst,start,event_valid,event_bit,phase_lock_ok,determinant_valid,
  output logic busy,done,fault,
  output logic [1:0] power_k,quadrature,
  output logic [31:0] shot_index,ones_count,
  output logic [31:0] theta1_re_ones,theta1_im_ones,theta2_re_ones,theta2_im_ones
);
  always_ff @(posedge clk) begin
    if(rst) begin busy<=0;done<=0;fault<=0;power_k<=1;quadrature<=0;shot_index<=0;ones_count<=0;theta1_re_ones<=0;theta1_im_ones<=0;theta2_re_ones<=0;theta2_im_ones<=0; end
    else begin
      done<=0;
      if(!busy&&start) begin
        fault<=0;
        if(!phase_lock_ok||!determinant_valid) begin fault<=1;done<=1; end
        else begin busy<=1;power_k<=1;quadrature<=0;shot_index<=0;ones_count<=0;theta1_re_ones<=0;theta1_im_ones<=0;theta2_re_ones<=0;theta2_im_ones<=0; end
      end else if(busy) begin
        if(!phase_lock_ok||!determinant_valid) begin busy<=0;fault<=1;done<=1; end
        else if(event_valid) begin
          if(event_bit) ones_count<=ones_count+1;
          if(shot_index+1==SHOTS_PER_QUADRATURE) begin
            case({power_k[0],quadrature[0]})
              2'b10: theta1_re_ones<=ones_count+event_bit;
              2'b11: theta1_im_ones<=ones_count+event_bit;
              2'b00: theta2_re_ones<=ones_count+event_bit;
              2'b01: theta2_im_ones<=ones_count+event_bit;
            endcase
            shot_index<=0;ones_count<=0;
            if(power_k==2 && quadrature==1) begin busy<=0;done<=1; end
            else if(quadrature==0) quadrature<=1;
            else begin quadrature<=0;power_k<=2; end
          end else shot_index<=shot_index+1;
        end
      end
    end
  end
endmodule
