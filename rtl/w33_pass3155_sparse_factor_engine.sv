// Passes 3155-3156: exact 3,697-factor posterior schedule.
// Physical shape: one 45x(7W) unary memory plus seven 483xW correction banks,
// plus one baseline register.  This preserves the 528-cycle schedule while fitting
// the iCE40 EBR aspect ratios in 29 blocks before tool observation.
module w33_pass3155_sparse_factor_engine #(
    parameter integer W=18
)(
    input  logic clk,
    input  logic rst,
    input  logic start_i,
    input  logic baseline_valid_i,
    input  logic signed [W-1:0] baseline_i,
    input  logic factor_valid_i,
    input  logic signed [7*W-1:0] factor_bundle_i,
    input  logic read_pair_i,
    input  logic [2:0] read_bank_i,
    input  logic [8:0] read_addr_i,
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
    logic signed [7*W-1:0] unary_mem[0:44];
    logic signed [W-1:0] corr0[0:482];
    logic signed [W-1:0] corr1[0:482];
    logic signed [W-1:0] corr2[0:482];
    logic signed [W-1:0] corr3[0:482];
    logic signed [W-1:0] corr4[0:482];
    logic signed [W-1:0] corr5[0:482];
    logic signed [W-1:0] corr6[0:482];
    logic signed [7*W-1:0] unary_read_word;
    logic [8:0] correction_write_addr;

    always_comb begin
        pair_phase_o=(cycle_o>=10'd45);
        unary_edge_o=pair_phase_o?6'd0:cycle_o[5:0];
        correction_write_addr=cycle_o-10'd45;
        if(!read_pair_i) read_data_o=unary_read_word[read_bank_i*W +: W];
    end

    always_ff @(posedge clk) begin
        if(!read_pair_i) begin
            unary_read_word<=unary_mem[read_addr_i[5:0]];
        end else begin
            case(read_bank_i)
              3'd0:read_data_o<=corr0[read_addr_i];
              3'd1:read_data_o<=corr1[read_addr_i];
              3'd2:read_data_o<=corr2[read_addr_i];
              3'd3:read_data_o<=corr3[read_addr_i];
              3'd4:read_data_o<=corr4[read_addr_i];
              3'd5:read_data_o<=corr5[read_addr_i];
              default:read_data_o<=corr6[read_addr_i];
            endcase
        end
        if(rst) begin
            baseline_o<='0;busy_o<=1'b0;done_o<=1'b0;cycle_o<='0;
            pair_index_o<='0;left_label_o<='0;read_data_o<='0;unary_read_word<='0;
        end else begin
            done_o<=1'b0;
            if(baseline_valid_i) baseline_o<=baseline_i;
            if(start_i) begin
                busy_o<=1'b1;cycle_o<=10'd0;pair_index_o<=7'd0;left_label_o<=3'd0;
            end else if(busy_o && factor_valid_i) begin
                if(cycle_o<10'd45) begin
                    unary_mem[cycle_o[5:0]]<=factor_bundle_i;
                end else begin
                    corr0[correction_write_addr]<=factor_bundle_i[0*W +: W];
                    corr1[correction_write_addr]<=factor_bundle_i[1*W +: W];
                    corr2[correction_write_addr]<=factor_bundle_i[2*W +: W];
                    corr3[correction_write_addr]<=factor_bundle_i[3*W +: W];
                    corr4[correction_write_addr]<=factor_bundle_i[4*W +: W];
                    corr5[correction_write_addr]<=factor_bundle_i[5*W +: W];
                    corr6[correction_write_addr]<=factor_bundle_i[6*W +: W];
                end
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
