// Pass 2811: exact support-first codec for F_3^4.
// 81 affine states -> codes 0..80 in seven bits.
// 40 projective nonzero classes -> addresses 0..39 in six bits.
module w33_pass2811_support_first_codec (
    input  logic [1:0] x0, x1, x2, x3,
    output logic [6:0] affine_code,
    output logic [5:0] projective_addr,
    output logic [3:0] support_mask,
    output logic [2:0] relative_phase,
    output logic       polarity,
    output logic       is_zero
);
    logic [1:0] pivot;
    logic [2:0] phase_tmp;
    logic [1:0] slot;
    logic [5:0] base;
    integer i;
    logic [1:0] trit [0:3];

    always_comb begin
        trit[0]=x0; trit[1]=x1; trit[2]=x2; trit[3]=x3;
        support_mask = {x3!=0, x2!=0, x1!=0, x0!=0};
        is_zero = (support_mask == 4'b0000);
        pivot = 0;
        polarity = 0;
        phase_tmp = 0;
        slot = 0;
        if (!is_zero) begin
            if (x0!=0) pivot=x0;
            else if (x1!=0) pivot=x1;
            else if (x2!=0) pivot=x2;
            else pivot=x3;
            polarity = (pivot == 2);
            for (i=0;i<4;i=i+1) begin
                if (trit[i]!=0 && ((i>0 && x0!=0) || (i>1 && x0==0 && x1!=0) ||
                    (i>2 && x0==0 && x1==0 && x2!=0))) begin
                    phase_tmp[slot] = (trit[i] != pivot);
                    slot = slot + 1;
                end
            end
        end
        relative_phase = phase_tmp;
        case (support_mask)
            4'h1: base=0;  4'h2: base=1;  4'h3: base=2;
            4'h4: base=4;  4'h5: base=5;  4'h6: base=7;  4'h7: base=9;
            4'h8: base=13; 4'h9: base=14; 4'hA: base=16; 4'hB: base=18;
            4'hC: base=22; 4'hD: base=24; 4'hE: base=28; 4'hF: base=32;
            default: base=0;
        endcase
        projective_addr = base + phase_tmp;
        affine_code = is_zero ? 0 : (1 + ({1'b0, projective_addr} << 1) + polarity);
    end
endmodule

module w33_pass2811_support_first_decoder (
    input  logic [6:0] affine_code,
    output logic [1:0] x0, x1, x2, x3
);
    logic [5:0] addr;
    logic polarity;
    logic [3:0] mask;
    logic [2:0] phase;
    logic [5:0] base;
    logic [1:0] val [0:3];
    logic [1:0] slot;
    integer i;

    always_comb begin
        x0=0; x1=0; x2=0; x3=0;
        addr=0; polarity=0; mask=0; phase=0; base=0; slot=0;
        for (i=0;i<4;i=i+1) val[i]=0;
        if (affine_code != 0) begin
            addr = (affine_code - 1) >> 1;
            polarity = (affine_code - 1) & 1;
            if      (addr < 1)  begin mask=4'h1; base=0;  end
            else if (addr < 2)  begin mask=4'h2; base=1;  end
            else if (addr < 4)  begin mask=4'h3; base=2;  end
            else if (addr < 5)  begin mask=4'h4; base=4;  end
            else if (addr < 7)  begin mask=4'h5; base=5;  end
            else if (addr < 9)  begin mask=4'h6; base=7;  end
            else if (addr < 13) begin mask=4'h7; base=9;  end
            else if (addr < 14) begin mask=4'h8; base=13; end
            else if (addr < 16) begin mask=4'h9; base=14; end
            else if (addr < 18) begin mask=4'hA; base=16; end
            else if (addr < 22) begin mask=4'hB; base=18; end
            else if (addr < 24) begin mask=4'hC; base=22; end
            else if (addr < 28) begin mask=4'hD; base=24; end
            else if (addr < 32) begin mask=4'hE; base=28; end
            else                begin mask=4'hF; base=32; end
            phase = addr - base;
            if (mask[0]) val[0]=1;
            else if (mask[1]) val[1]=1;
            else if (mask[2]) val[2]=1;
            else val[3]=1;
            for (i=0;i<4;i=i+1) begin
                if (mask[i] && val[i]==0) begin
                    val[i] = phase[slot] ? 2 : 1;
                    slot = slot + 1;
                end
            end
            if (polarity) begin
                for (i=0;i<4;i=i+1)
                    if (val[i]!=0) val[i] = 3 - val[i];
            end
            x0=val[0]; x1=val[1]; x2=val[2]; x3=val[3];
        end
    end
endmodule
