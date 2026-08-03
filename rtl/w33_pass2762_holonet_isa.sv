// Passes 2762-2766 -- complete eight-opcode Holonet digital contract.
//
// Opcode map:
//   000 F_p          001 F_f
//   010 S_p          011 S_f
//   100 CX           direction=0 p->f, direction=1 f->p
//   101 sigma_5=Z    register_select=0 past, 1 future
//   110 D12 mirror   operand r^mirror_rot m^mirror_reflect
//   111 M36 magic    typed request, magic_index in 0..35
//
// The Clifford and D12 transitions are exact. M36 is deliberately a handshake
// to an external state-preparation/injection block; no non-Clifford unitary is
// invented in RTL.
`timescale 1ns/1ps

module w33_pass2762_f3_add(
    input  logic [1:0] a,
    input  logic [1:0] b,
    output logic [1:0] y
);
    logic [2:0] s;
    always_comb begin
        s = a + b;
        y = (s >= 3) ? s - 3 : s[1:0];
    end
endmodule

module w33_pass2762_f3_sub(
    input  logic [1:0] a,
    input  logic [1:0] b,
    output logic [1:0] y
);
    always_comb begin
        case ({a,b})
            4'b0000,4'b0101,4'b1010: y = 0;
            4'b0100,4'b1001,4'b0010: y = 1;
            default:                 y = 2;
        endcase
    end
endmodule

module w33_pass2762_frame_step(
    input  logic [1:0] xp,
    input  logic [1:0] zp,
    input  logic [1:0] xf,
    input  logic [1:0] zf,
    input  logic [2:0] opcode,
    input  logic       direction,
    input  logic       register_select,
    output logic [1:0] xp_next,
    output logic [1:0] zp_next,
    output logic [1:0] xf_next,
    output logic [1:0] zf_next
);
    logic [1:0] neg_zp, neg_zf;
    logic [1:0] zp_plus_xp, zf_plus_xf;
    logic [1:0] zp_minus_zf, zf_minus_zp;
    logic [1:0] xf_plus_xp, xp_plus_xf;
    logic [1:0] zp_plus_one, zf_plus_one;

    assign neg_zp = (zp == 0) ? 0 : (zp == 1) ? 2 : 1;
    assign neg_zf = (zf == 0) ? 0 : (zf == 1) ? 2 : 1;
    w33_pass2762_f3_add a0(.a(zp), .b(xp), .y(zp_plus_xp));
    w33_pass2762_f3_add a1(.a(zf), .b(xf), .y(zf_plus_xf));
    w33_pass2762_f3_add a2(.a(xf), .b(xp), .y(xf_plus_xp));
    w33_pass2762_f3_add a3(.a(xp), .b(xf), .y(xp_plus_xf));
    w33_pass2762_f3_add a4(.a(zp), .b(2'd1), .y(zp_plus_one));
    w33_pass2762_f3_add a5(.a(zf), .b(2'd1), .y(zf_plus_one));
    w33_pass2762_f3_sub s0(.a(zp), .b(zf), .y(zp_minus_zf));
    w33_pass2762_f3_sub s1(.a(zf), .b(zp), .y(zf_minus_zp));

    always_comb begin
        xp_next = xp; zp_next = zp; xf_next = xf; zf_next = zf;
        case (opcode)
            3'd0: begin xp_next = neg_zp; zp_next = xp; end
            3'd1: begin xf_next = neg_zf; zf_next = xf; end
            3'd2: begin zp_next = zp_plus_xp; end
            3'd3: begin zf_next = zf_plus_xf; end
            3'd4: begin
                if (!direction) begin
                    zp_next = zp_minus_zf;
                    xf_next = xf_plus_xp;
                end else begin
                    xp_next = xp_plus_xf;
                    zf_next = zf_minus_zp;
                end
            end
            3'd5: begin
                if (!register_select) zp_next = zp_plus_one;
                else                  zf_next = zf_plus_one;
            end
            default: begin end
        endcase
    end
endmodule

module w33_pass2762_basis_sum(
    input  logic [1:0] p,
    input  logic [1:0] f,
    input  logic       direction,
    output logic [1:0] p_out,
    output logic [1:0] f_out
);
    logic [1:0] f_plus_p, p_plus_f;
    w33_pass2762_f3_add a0(.a(f), .b(p), .y(f_plus_p));
    w33_pass2762_f3_add a1(.a(p), .b(f), .y(p_plus_f));
    always_comb begin
        if (!direction) begin p_out = p;        f_out = f_plus_p; end
        else            begin p_out = p_plus_f; f_out = f;       end
    end
endmodule

module w33_pass2762_d12_mul(
    input  logic [2:0] left_rot,
    input  logic       left_reflect,
    input  logic [2:0] right_rot,
    input  logic       right_reflect,
    output logic [2:0] out_rot,
    output logic       out_reflect
);
    integer temp;
    always_comb begin
        if (left_reflect) temp = left_rot - right_rot;
        else              temp = left_rot + right_rot;
        if (temp < 0) temp = temp + 6;
        if (temp >= 6) temp = temp - 6;
        out_rot = temp[2:0];
        out_reflect = left_reflect ^ right_reflect;
    end
endmodule

module w33_pass2762_holonet_isa(
    input  logic       clk,
    input  logic       rst,
    input  logic       valid,
    output logic       ready,
    input  logic [2:0] opcode,
    input  logic       direction,
    input  logic       register_select,
    input  logic [2:0] mirror_rot_operand,
    input  logic       mirror_reflect_operand,
    input  logic [5:0] magic_index,
    input  logic       magic_ack,

    output logic [1:0] xp,
    output logic [1:0] zp,
    output logic [1:0] xf,
    output logic [1:0] zf,
    output logic [2:0] mirror_rot,
    output logic       mirror_reflect,
    output logic       magic_req,
    output logic [5:0] magic_ray,
    output logic [1:0] magic_grade, // 0 deep, 1 mid, 2 shallow (BT822 order)
    output logic [15:0] magic_consumed,
    output logic       retired,
    output logic       fault
);
    logic [1:0] xp_n, zp_n, xf_n, zf_n;
    logic [2:0] mirror_rot_n;
    logic mirror_reflect_n;
    logic magic_pending;

    function automatic [1:0] grade36(input logic [5:0] ray);
        begin
            if (ray < 4) grade36 = 2;
            else if ((ray >= 20 && ray < 24) || (ray >= 28 && ray < 32))
                grade36 = 0;
            else grade36 = 1;
        end
    endfunction

    w33_pass2762_frame_step frame_step(
        .xp(xp), .zp(zp), .xf(xf), .zf(zf),
        .opcode(opcode), .direction(direction),
        .register_select(register_select),
        .xp_next(xp_n), .zp_next(zp_n),
        .xf_next(xf_n), .zf_next(zf_n)
    );

    w33_pass2762_d12_mul mirror_step(
        .left_rot(mirror_rot_operand),
        .left_reflect(mirror_reflect_operand),
        .right_rot(mirror_rot),
        .right_reflect(mirror_reflect),
        .out_rot(mirror_rot_n),
        .out_reflect(mirror_reflect_n)
    );

    assign ready = !magic_pending;
    assign magic_req = magic_pending;

    always_ff @(posedge clk) begin
        if (rst) begin
            xp <= 0; zp <= 0; xf <= 0; zf <= 0;
            mirror_rot <= 0; mirror_reflect <= 0;
            magic_pending <= 0; magic_ray <= 0; magic_grade <= 0;
            magic_consumed <= 0; retired <= 0; fault <= 0;
        end else begin
            retired <= 0;
            if (magic_pending) begin
                if (magic_ack) begin
                    magic_pending <= 0;
                    magic_consumed <= magic_consumed + 1'b1;
                    retired <= 1;
                end
            end else if (valid) begin
                case (opcode)
                    3'd0,3'd1,3'd2,3'd3,3'd4,3'd5: begin
                        xp <= xp_n; zp <= zp_n; xf <= xf_n; zf <= zf_n;
                        retired <= 1;
                    end
                    3'd6: begin
                        if (mirror_rot_operand < 6) begin
                            mirror_rot <= mirror_rot_n;
                            mirror_reflect <= mirror_reflect_n;
                        end else fault <= 1;
                        retired <= 1;
                    end
                    3'd7: begin
                        if (magic_index < 36) begin
                            magic_ray <= magic_index;
                            magic_grade <= grade36(magic_index);
                            magic_pending <= 1;
                        end else begin
                            fault <= 1;
                            retired <= 1;
                        end
                    end
                    default: begin fault <= 1; retired <= 1; end
                endcase
            end
        end
    end
endmodule
