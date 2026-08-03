// Pass 2848: 24-sample distance-four affine-square support code.
// Each active affine feature is emitted twice. Inputs must be legal trits 0,1,2.
module w33_pass2848_affine_square_feature_encoder (
    input  logic [1:0] x_p,
    input  logic [1:0] z_p,
    input  logic [1:0] x_f,
    input  logic [1:0] z_f,
    output logic [23:0] code,
    output logic        legal
);
    logic [1:0] feature [0:11];
    logic [11:0] support_bits;
    integer i;

    function automatic logic [1:0] add3(input logic [1:0] a, input logic [1:0] b);
        logic [2:0] s;
        begin
            s = a + b;
            if (s >= 3) add3 = s - 3;
            else        add3 = s[1:0];
        end
    endfunction

    function automatic logic [1:0] neg3(input logic [1:0] a);
        begin
            case (a)
                2'd0: neg3 = 2'd0;
                2'd1: neg3 = 2'd2;
                2'd2: neg3 = 2'd1;
                default: neg3 = 2'd0;
            endcase
        end
    endfunction

    function automatic logic [1:0] sub3(input logic [1:0] a, input logic [1:0] b);
        begin
            sub3 = add3(a, neg3(b));
        end
    endfunction

    always_comb begin
        legal = (x_p != 2'd3) && (z_p != 2'd3) &&
                (x_f != 2'd3) && (z_f != 2'd3);

        feature[0]  = x_p;
        feature[1]  = z_p;
        feature[2]  = x_f;
        feature[3]  = z_f;
        feature[4]  = sub3(z_p, z_f);
        feature[5]  = add3(x_p, x_f);
        feature[6]  = add3(x_p, 2'd1);
        feature[7]  = add3(sub3(z_p, z_f), 2'd2);
        feature[8]  = add3(z_p, 2'd2);
        feature[9]  = add3(x_f, 2'd2);
        feature[10] = add3(sub3(x_p, x_f), 2'd1);
        feature[11] = add3(z_f, 2'd2);

        for (i = 0; i < 12; i = i + 1)
            support_bits[i] = legal && (feature[i] != 2'd0);

        // Two independent samples per feature give the exact distance-four code.
        for (i = 0; i < 12; i = i + 1) begin
            code[2*i]   = support_bits[i];
            code[2*i+1] = support_bits[i];
        end
    end
endmodule
