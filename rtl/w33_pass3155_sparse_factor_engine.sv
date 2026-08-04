// Passes 3155-3156: exact seven-bank schedule for the 3,697-factor posterior.
// One baseline register plus seven banks x 528 words x W bits.  Reads are synchronous
// so Yosys can infer block RAM rather than a large asynchronous LUT memory.
module w33_pass3155_sparse_factor_engine #(
    parameter integer W=18,
    parameter integer DEPTH=528
)(
    input  logic clk,
    input  logic rst,
    input  logic start_i,
    input  logic baseline_valid_i,
    input  logic signed [W-1:0] baseline_i,
    input  logic factor_valid_i,
    input  logic signed [7*W-1:0] factor_bundle_i,
    input  logic [2:0] read_bank_i,
    input  logic [9:0] read_addr_i,
    output logic signed [W-1:0] read_data_o,
    output logic signed [W-1:0] baseline_o,
    output logic busy_o,
    output logic done_o,
    output logic [9:0] cycle_o,
    output logic pair_phase_o,
    output logic [5:0] unary_edge_o,
    output logic [6:0] pair_index_o,
    output logic [2:0] left_label_o
);
    logic signed [W-1:0] bank0[0:DEPTH-1];
    logic signed [W-1:0] bank1[0:DEPTH-1];
    logic signed [W-1:0] bank2[0:DEPTH-1];
    logic signed [W-1:0] bank3[0:DEPTH-1];
    logic signed [W-1:0] bank4[0:DEPTH-1];
    logic signed [W-1:0] bank5[0:DEPTH-1];
    logic signed [W-1:0] bank6[0:DEPTH-1];

    always_comb begin
        pair_phase_o=(cycle_o>=10'd45);
        unary_edge_o=pair_phase_o?6'd0:cycle_o[5:0];
    end

    always_ff @(posedge clk) begin
        case(read_bank_i)
          3'd0:read_data_o<=bank0[read_addr_i];
          3'd1:read_data_o<=bank1[read_addr_i];
          3'd2:read_data_o<=bank2[read_addr_i];
          3'd3:read_data_o<=bank3[read_addr_i];
          3'd4:read_data_o<=bank4[read_addr_i];
          3'd5:read_data_o<=bank5[read_addr_i];
          default:read_data_o<=bank6[read_addr_i];
        endcase
        if(rst) begin
            baseline_o<='0;busy_o<=1'b0;done_o<=1'b0;cycle_o<='0;
            pair_index_o<='0;left_label_o<='0;read_data_o<='0;
        end else begin
            done_o<=1'b0;
            if(baseline_valid_i) baseline_o<=baseline_i;
            if(start_i) begin
                busy_o<=1'b1;cycle_o<=10'd0;pair_index_o<=7'd0;left_label_o<=3'd0;
            end else if(busy_o && factor_valid_i) begin
                bank0[cycle_o]<=factor_bundle_i[0*W +: W];
                bank1[cycle_o]<=factor_bundle_i[1*W +: W];
                bank2[cycle_o]<=factor_bundle_i[2*W +: W];
                bank3[cycle_o]<=factor_bundle_i[3*W +: W];
                bank4[cycle_o]<=factor_bundle_i[4*W +: W];
                bank5[cycle_o]<=factor_bundle_i[5*W +: W];
                bank6[cycle_o]<=factor_bundle_i[6*W +: W];
                if(cycle_o==10'd527) begin
                    busy_o<=1'b0;done_o<=1'b1;
                end else begin
                    cycle_o<=cycle_o+1'b1;
                    if(cycle_o==10'd44) begin pair_index_o<=7'd0;left_label_o<=3'd0;end
                    else if(cycle_o>=10'd45) begin
                        if(left_label_o==3'd6) begin left_label_o<=3'd0;pair_index_o<=pair_index_o+1'b1;end
                        else left_label_o<=left_label_o+1'b1;
                    end
                end
            end
        end
    end
endmodule
