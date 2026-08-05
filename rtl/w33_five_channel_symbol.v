`default_nettype none

module w33_five_channel_symbol (
    input  wire [2:0] zero_mask,
    input  wire [2:0] row,
    input  wire [2:0] col,
    output reg signed [4:0] weight
);
    integer c1;
    integer c2;
    integer c3;
    integer ar;
    integer br;
    integer ac;
    integer bc;
    integer k1;
    integer k2;
    integer delta;
    integer value;

    function integer m_entry;
        input integer r;
        input integer c;
        begin
            if ((r == 0) && (c == 0))
                m_entry = 0;
            else if ((r == 0) && (c == 1))
                m_entry = 2;
            else
                m_entry = 1;
        end
    endfunction

    always @* begin
        c1 = zero_mask[0] ? 2 : -1;
        c2 = zero_mask[1] ? 2 : -1;
        c3 = zero_mask[2] ? 2 : -1;
        value = 0;

        if ((row < 4) && (col < 4)) begin
            ar = row[0];
            br = row[1];
            ac = col[0];
            bc = col[1];
            k1 = (br == bc) ? m_entry(ar, ac) : 0;
            k2 = (ar == ac) ? m_entry(br, bc) : 0;
            delta = (row == col) ? 1 : 0;
            value = c1 * k1 + c2 * k2 + c3 * delta;
        end else if ((row == 4) && (col == 4)) begin
            value = c3 - c1 - c2;
        end

        weight = value;
    end
endmodule

module w33_mod3_five_channel_step (
    input  wire [2:0] zero_mask,
    input  wire [1:0] in0,
    input  wire [1:0] in1,
    input  wire [1:0] in2,
    input  wire [1:0] in3,
    input  wire [1:0] in4,
    output reg  [1:0] out0,
    output reg  [1:0] out1,
    output reg  [1:0] out2,
    output reg  [1:0] out3,
    output reg  [1:0] out4
);
    integer v0;
    integer v1;
    integer v2;
    integer v3;

    function [1:0] reduce3;
        input integer value;
        integer residue;
        begin
            residue = value % 3;
            if (residue < 0)
                residue = residue + 3;
            reduce3 = residue[1:0];
        end
    endfunction

    always @* begin
        // Every one of the 27 momentum symbols reduces to this same map mod 3.
        // zero_mask is intentionally semantically inactive in this module.
        v0 = 2 * in0 + in1 + in2;
        v1 = 2 * in0 + in1 + in3;
        v2 = 2 * in0 + in2 + in3;
        v3 = 2 * in1 + 2 * in2;
        out0 = reduce3(v0);
        out1 = reduce3(v1);
        out2 = reduce3(v2);
        out3 = reduce3(v3);
        out4 = in4;
    end

    wire _unused = &{1'b0, zero_mask};
endmodule

`default_nettype wire
