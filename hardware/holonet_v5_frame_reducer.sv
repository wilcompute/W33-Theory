`timescale 1ns/1ps
module holonet_v5_frame_reducer (
    input  logic         clk,
    input  logic         rst_n,
    input  logic         s_axis_tvalid,
    output logic         s_axis_tready,
    input  logic [63:0]  s_axis_timestamp_ps,
    input  logic [4:0]   s_axis_channel,
    output logic         m_axis_tvalid,
    input  logic         m_axis_tready,
    output logic [31:0]  m_axis_frame_id,
    output logic [63:0]  m_axis_first_timestamp_ps,
    output logic [63:0]  m_axis_last_timestamp_ps,
    output logic         overflow,
    output logic [23:0]  count0, count1, count2, count3,
    output logic [23:0]  count4, count5, count6, count7,
    output logic [23:0]  count8, count9, count10, count11,
    output logic [23:0]  count12, count13, count14, count15
);
    logic [23:0] counts [0:15];
    logic [63:0] first_ts;
    logic        have_first;
    integer i;

    assign s_axis_tready = ~m_axis_tvalid;
    assign count0=counts[0]; assign count1=counts[1]; assign count2=counts[2]; assign count3=counts[3];
    assign count4=counts[4]; assign count5=counts[5]; assign count6=counts[6]; assign count7=counts[7];
    assign count8=counts[8]; assign count9=counts[9]; assign count10=counts[10]; assign count11=counts[11];
    assign count12=counts[12]; assign count13=counts[13]; assign count14=counts[14]; assign count15=counts[15];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            m_axis_tvalid <= 1'b0;
            m_axis_frame_id <= 32'd0;
            m_axis_first_timestamp_ps <= 64'd0;
            m_axis_last_timestamp_ps <= 64'd0;
            first_ts <= 64'd0;
            have_first <= 1'b0;
            overflow <= 1'b0;
            for (i=0; i<16; i=i+1) counts[i] <= 24'd0;
        end else begin
            if (m_axis_tvalid && m_axis_tready)
                m_axis_tvalid <= 1'b0;
            if (s_axis_tvalid && s_axis_tready) begin
                if (s_axis_channel == 5'd16) begin
                    m_axis_tvalid <= 1'b1;
                    m_axis_first_timestamp_ps <= have_first ? first_ts : s_axis_timestamp_ps;
                    m_axis_last_timestamp_ps <= s_axis_timestamp_ps;
                    m_axis_frame_id <= m_axis_frame_id + 1'b1;
                    first_ts <= 64'd0;
                    have_first <= 1'b0;
                    overflow <= 1'b0;
                    for (i=0; i<16; i=i+1) counts[i] <= 24'd0;
                end else if (s_axis_channel < 5'd16) begin
                    if (!have_first) begin
                        first_ts <= s_axis_timestamp_ps;
                        have_first <= 1'b1;
                    end
                    if (counts[s_axis_channel] == 24'hffffff)
                        overflow <= 1'b1;
                    else
                        counts[s_axis_channel] <= counts[s_axis_channel] + 1'b1;
                end
            end
        end
    end
endmodule
