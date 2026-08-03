// Pass 2902: combinational dense 15x15 reference for the q=3 support quotient.
module w33_pass2902_q3_dense_reference #(
    parameter integer IN_W  = 12,
    parameter integer OUT_W = 24
) (
    input  logic signed [15*IN_W-1:0]  in_flat,
    output logic signed [15*OUT_W-1:0] out_flat
);
    integer s;
    integer t;
    integer coeff;
    integer acc;

    function automatic integer tau_mask(input integer m);
        integer out;
        begin
            out = 0;
            if (m & 1) out = out | 4;
            if (m & 2) out = out | 8;
            if (m & 4) out = out | 1;
            if (m & 8) out = out | 2;
            tau_mask = out;
        end
    endfunction

    function automatic integer popcount4(input integer m);
        begin
            popcount4 = (m&1) + ((m>>1)&1) + ((m>>2)&1) + ((m>>3)&1);
        end
    endfunction

    function automatic integer pow2(input integer n);
        begin
            case (n)
                0: pow2 = 1;
                1: pow2 = 2;
                2: pow2 = 4;
                3: pow2 = 8;
                default: pow2 = 16;
            endcase
        end
    endfunction

    function automatic integer zero_sum_count(input integer r);
        begin
            case (r)
                0: zero_sum_count = 1;
                1: zero_sum_count = 0;
                2: zero_sum_count = 2;
                3: zero_sum_count = 2;
                default: zero_sum_count = 6;
            endcase
        end
    endfunction

    function automatic integer qentry(input integer sm, input integer tm);
        integer r;
        integer wt;
        integer num;
        begin
            r = popcount4(tm & tau_mask(sm));
            wt = popcount4(tm);
            num = pow2(wt-r) * zero_sum_count(r);
            qentry = num/2 - ((sm == tm) ? 1 : 0);
        end
    endfunction

    always_comb begin
        out_flat = '0;
        for (s=1; s<=15; s=s+1) begin
            acc = 0;
            for (t=1; t<=15; t=t+1) begin
                coeff = qentry(s,t);
                acc = acc + coeff * $signed(in_flat[(t-1)*IN_W +: IN_W]);
            end
            out_flat[(s-1)*OUT_W +: OUT_W] = acc;
        end
    end
endmodule
