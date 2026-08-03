// Pass 2902: sequential q=3 support-quotient engine.
// Four stages x eight local butterflies, then fifteen serial outputs.
module w33_pass2902_q3_hadamard_engine #(
    parameter integer IN_W  = 12,
    parameter integer ACC_W = 24
) (
    input  logic                         clk,
    input  logic                         rst,
    input  logic                         start,
    input  logic signed [15*IN_W-1:0]    in_flat,
    output logic                         busy,
    output logic                         out_valid,
    output logic [3:0]                   out_index,
    output logic signed [ACC_W-1:0]      out_value,
    output logic                         done
);
    typedef enum logic [1:0] {IDLE, BUTTERFLY, EMIT} state_t;
    state_t state;

    logic signed [ACC_W-1:0] lane [0:15];
    logic signed [ACC_W-1:0] original [0:14];
    logic signed [ACC_W-1:0] border;
    logic [1:0] stage;
    logic [2:0] pair_index;
    logic [3:0] emit_index;

    integer i;
    integer a_idx;
    integer b_idx;
    integer s_mask;
    integer tau_idx;
    logic signed [ACC_W-1:0] u;
    logic signed [ACC_W-1:0] v;
    logic signed [ACC_W-1:0] numerator;

    function automatic integer pair_a(input integer st, input integer k);
        begin
            case (st)
                0: pair_a = 2*k;
                1: pair_a = 4*(k/2) + (k%2);
                2: pair_a = 8*(k/4) + (k%4);
                default: pair_a = k;
            endcase
        end
    endfunction

    function automatic integer tau_mask(input integer m);
        integer out;
        begin
            out = 0;
            if (m & 1) tau_mask = out | 4; else tau_mask = out;
            out = tau_mask;
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

    function automatic integer weight(input integer m);
        integer w;
        begin
            w = popcount4(m);
            case (w)
                1: weight = 1;
                2: weight = 2;
                3: weight = 4;
                default: weight = 8;
            endcase
        end
    endfunction

    always_ff @(posedge clk) begin
        if (rst) begin
            state      <= IDLE;
            busy       <= 1'b0;
            out_valid  <= 1'b0;
            out_index  <= 4'd0;
            out_value  <= '0;
            done       <= 1'b0;
            stage      <= 2'd0;
            pair_index <= 3'd0;
            emit_index <= 4'd0;
            border     <= '0;
            for (i=0; i<16; i=i+1) lane[i] <= '0;
            for (i=0; i<15; i=i+1) original[i] <= '0;
        end else begin
            out_valid <= 1'b0;
            done      <= 1'b0;

            case (state)
                IDLE: begin
                    busy <= 1'b0;
                    if (start) begin
                        lane[0] <= '0;
                        border <= '0;
                        for (i=0; i<15; i=i+1) begin
                            original[i] <= $signed(in_flat[i*IN_W +: IN_W]);
                            lane[i+1]   <= $signed(in_flat[i*IN_W +: IN_W]);
                            border      <= border + weight(i+1) * $signed(in_flat[i*IN_W +: IN_W]);
                        end
                        // The nonblocking accumulation above would retain only the final term.
                        // Recompute with a blocking temporary encoded as an explicit sum.
                        border <=
                            1*$signed(in_flat[0*IN_W +: IN_W]) +
                            1*$signed(in_flat[1*IN_W +: IN_W]) +
                            2*$signed(in_flat[2*IN_W +: IN_W]) +
                            1*$signed(in_flat[3*IN_W +: IN_W]) +
                            2*$signed(in_flat[4*IN_W +: IN_W]) +
                            2*$signed(in_flat[5*IN_W +: IN_W]) +
                            4*$signed(in_flat[6*IN_W +: IN_W]) +
                            1*$signed(in_flat[7*IN_W +: IN_W]) +
                            2*$signed(in_flat[8*IN_W +: IN_W]) +
                            2*$signed(in_flat[9*IN_W +: IN_W]) +
                            4*$signed(in_flat[10*IN_W +: IN_W]) +
                            2*$signed(in_flat[11*IN_W +: IN_W]) +
                            4*$signed(in_flat[12*IN_W +: IN_W]) +
                            4*$signed(in_flat[13*IN_W +: IN_W]) +
                            8*$signed(in_flat[14*IN_W +: IN_W]);
                        stage      <= 2'd0;
                        pair_index <= 3'd0;
                        busy       <= 1'b1;
                        state      <= BUTTERFLY;
                    end
                end

                BUTTERFLY: begin
                    busy  <= 1'b1;
                    a_idx = pair_a(stage, pair_index);
                    b_idx = a_idx + (1 << stage);
                    u = lane[a_idx];
                    v = lane[b_idx];
                    lane[a_idx] <= u + (v <<< 1); // u + 2v
                    lane[b_idx] <= u - v;
                    if (pair_index == 3'd7) begin
                        pair_index <= 3'd0;
                        if (stage == 2'd3) begin
                            emit_index <= 4'd0;
                            state <= EMIT;
                        end else begin
                            stage <= stage + 2'd1;
                        end
                    end else begin
                        pair_index <= pair_index + 3'd1;
                    end
                end

                EMIT: begin
                    busy      <= 1'b1;
                    out_valid <= 1'b1;
                    out_index <= emit_index;
                    s_mask    = emit_index + 1;
                    tau_idx   = tau_mask(s_mask);
                    numerator = border + lane[tau_idx];
                    out_value <= numerator / 3 - original[emit_index];
                    if (emit_index == 4'd14) begin
                        done       <= 1'b1;
                        busy       <= 1'b0;
                        emit_index <= 4'd0;
                        state      <= IDLE;
                    end else begin
                        emit_index <= emit_index + 4'd1;
                    end
                end

                default: state <= IDLE;
            endcase
        end
    end
endmodule
