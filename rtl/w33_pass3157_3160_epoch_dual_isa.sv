// Passes 3157-3158: in-band epoch delimiter and clean two-symbol reacquisition.
// Marker symbols 1 and 22 are absent from the payload cycle.  Seeing at least three
// marker-alphabet symbols in a seven-symbol window is impossible for a payload under at
// most two edits and unavoidable for the five-symbol marker under at most two edits.
module w33_pass3157_epoch_tracker(
    input  logic clk,input logic rst,
    input  logic symbol_valid_i,input logic [4:0] symbol_i,
    output logic marker_seen_o,output logic epoch_locked_o,
    output logic [3:0] phase_o,output logic [15:0] epoch_count_o
);
    logic [6:0] rare_hist;
    logic marker_latched,acquiring,have_first;
    logic [4:0] first_symbol;
    logic [3:0] decoded_phase;
    logic decoded_valid;
    integer k;logic [3:0] rare_count_next;

    function automatic logic is_rare(input logic [4:0] s);
        is_rare=(s==5'd1)||(s==5'd22);
    endfunction
    task automatic decode_pair(input logic [4:0] a,input logic [4:0] b,
                               output logic valid,output logic [3:0] phase);
      begin valid=1'b1;
        case({a,b})
          {5'd7,5'd2}:phase=4'd2; {5'd2,5'd16}:phase=4'd3;
          {5'd16,5'd23}:phase=4'd4; {5'd23,5'd20}:phase=4'd5;
          {5'd20,5'd15}:phase=4'd6; {5'd15,5'd0}:phase=4'd7;
          {5'd0,5'd2}:phase=4'd8; {5'd2,5'd7}:phase=4'd9;
          {5'd7,5'd11}:phase=4'd10; {5'd11,5'd16}:phase=4'd11;
          {5'd16,5'd19}:phase=4'd0; {5'd19,5'd7}:phase=4'd1;
          default:begin valid=1'b0;phase=4'd0;end
        endcase
      end
    endtask

    always_comb begin
        rare_count_next=0;
        for(k=0;k<6;k=k+1) rare_count_next=rare_count_next+rare_hist[k];
        rare_count_next=rare_count_next+is_rare(symbol_i);
        decode_pair(first_symbol,symbol_i,decoded_valid,decoded_phase);
    end

    always_ff @(posedge clk) begin
      if(rst) begin
        rare_hist<='0;marker_latched<=0;acquiring<=0;have_first<=0;
        marker_seen_o<=0;epoch_locked_o<=0;phase_o<=0;epoch_count_o<=0;
      end else begin
        marker_seen_o<=0;epoch_locked_o<=0;
        if(symbol_valid_i) begin
          rare_hist<={rare_hist[5:0],is_rare(symbol_i)};
          if(rare_count_next<3) marker_latched<=0;
          if(!marker_latched && rare_count_next>=3) begin
            marker_latched<=1;marker_seen_o<=1;acquiring<=1;have_first<=0;
          end else if(acquiring && !is_rare(symbol_i)) begin
            if(!have_first) begin first_symbol<=symbol_i;have_first<=1;end
            else if(decoded_valid) begin
              phase_o<=decoded_phase;epoch_count_o<=epoch_count_o+1'b1;
              epoch_locked_o<=1;acquiring<=0;have_first<=0;
            end else first_symbol<=symbol_i;
          end
        end
      end
    end
endmodule

// Pass 3160: equal-footprint current4 versus low-collision4 scheduler.
// Fixed-point format: base cost Q8.8, entropy/route Q4.4, confidence Q0.8.
module w33_pass3160_dual_isa_scheduler(
    input logic clk,input logic rst,
    input logic [15:0] base_collision_cost_q8_8_i,
    input logic [7:0] causal_entropy_q4_4_i,
    input logic [7:0] route_burden_q4_4_i,
    input logic [7:0] calibration_confidence_q0_8_i,
    input logic low_isa_calibrated_i,
    output logic low_collision_mode_o,output logic switch_o,
    output logic [15:0] effective_collision_cost_q8_8_o
);
    localparam logic [15:0] UP_THRESHOLD=16'd1188;   // 4.6407986
    localparam logic [15:0] DOWN_THRESHOLD=16'd728; // 2.8430691 rounded down
    logic [23:0] entropy_product;
    logic [15:0] entropy_term,route_term,calibration_term;
    always_comb begin
      entropy_product=causal_entropy_q4_4_i*8'd90;
      entropy_term=entropy_product>>4;
      route_term={5'd0,route_burden_q4_4_i,3'd0};
      calibration_term=16'd256-{8'd0,calibration_confidence_q0_8_i};
      effective_collision_cost_q8_8_o=base_collision_cost_q8_8_i+
          entropy_term+route_term+calibration_term;
    end
    always_ff @(posedge clk) begin
      if(rst) begin low_collision_mode_o<=0;switch_o<=0;end
      else begin
        switch_o<=0;
        if(!low_isa_calibrated_i && low_collision_mode_o) begin
          low_collision_mode_o<=0;switch_o<=1;
        end else if(!low_collision_mode_o && low_isa_calibrated_i &&
                    effective_collision_cost_q8_8_o>UP_THRESHOLD) begin
          low_collision_mode_o<=1;switch_o<=1;
        end else if(low_collision_mode_o &&
                    effective_collision_cost_q8_8_o<DOWN_THRESHOLD) begin
          low_collision_mode_o<=0;switch_o<=1;
        end
      end
    end
endmodule
