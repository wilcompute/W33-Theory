`default_nettype none

module w33_pass3196_epoch4_decoder(
    input  wire       clk,
    input  wire       rst,
    input  wire       start,
    input  wire       symbol_valid,
    input  wire [4:0] symbol,
    input  wire       finish,
    output reg        done,
    output reg        accept,
    output reg [3:0]  phase,
    output reg [3:0]  distance,
    output reg        ambiguous
);
    localparam integer PHASES = 12;
    reg [4:0] phase_symbol [0:PHASES-1];
    reg [3:0] count [0:PHASES-1];
    reg [4:0] received_length;
    integer i;
    integer d;
    integer winners;
    integer best;

    initial begin
        phase_symbol[0]=1;  phase_symbol[1]=3;  phase_symbol[2]=4;
        phase_symbol[3]=5;  phase_symbol[4]=6;  phase_symbol[5]=8;
        phase_symbol[6]=9;  phase_symbol[7]=10; phase_symbol[8]=12;
        phase_symbol[9]=13; phase_symbol[10]=14; phase_symbol[11]=17;
    end

    always @(posedge clk) begin
        if (rst || start) begin
            received_length <= 0;
            done <= 0;
            accept <= 0;
            phase <= 0;
            distance <= 15;
            ambiguous <= 0;
            for (i=0;i<PHASES;i=i+1) count[i] <= 0;
        end else begin
            done <= 0;
            if (symbol_valid) begin
                received_length <= received_length + 1'b1;
                for (i=0;i<PHASES;i=i+1)
                    if (symbol == phase_symbol[i]) count[i] <= count[i] + 1'b1;
            end
            if (finish) begin
                winners = 0;
                best = 15;
                phase = 0;
                for (i=0;i<PHASES;i=i+1) begin
                    d = ((received_length > 9) ? received_length : 9)
                      - ((count[i] > 9) ? 9 : count[i]);
                    if (d <= 4) begin
                        winners = winners + 1;
                        if (d < best) begin
                            best = d;
                            phase = i[3:0];
                        end
                    end
                end
                done <= 1;
                accept <= (winners == 1);
                ambiguous <= (winners > 1);
                distance <= best[3:0];
            end
        end
    end
endmodule

module w33_pass3197_proof_envelope_authorizer(
    input  wire         clk,
    input  wire         rst,
    input  wire         start,
    input  wire         field_valid,
    input  wire [3:0]   field_id,
    input  wire         finish,
    input  wire         schema_ok,
    input  wire         provenance_ok,
    input  wire         accepted_claim,
    input  wire         independent_cert_pass,
    input  wire [8:0]   shard_index,
    input  wire [8:0]   shard_count,
    input  wire [255:0] expected_digest,
    input  wire [255:0] computed_digest,
    output reg          done,
    output reg          authorize,
    output reg [7:0]    reject_reason,
    output reg [11:0]   observed_fields
);
    localparam [11:0] REQUIRED = 12'hfff;
    reg duplicate_field;

    always @(posedge clk) begin
        if (rst || start) begin
            done <= 0;
            authorize <= 0;
            reject_reason <= 0;
            observed_fields <= 0;
            duplicate_field <= 0;
        end else begin
            done <= 0;
            if (field_valid) begin
                if (field_id < 12) begin
                    if (observed_fields[field_id]) duplicate_field <= 1;
                    observed_fields[field_id] <= 1;
                end else begin
                    duplicate_field <= 1;
                end
            end
            if (finish) begin
                done <= 1;
                reject_reason[0] <= (observed_fields != REQUIRED);
                reject_reason[1] <= duplicate_field;
                reject_reason[2] <= !schema_ok;
                reject_reason[3] <= !provenance_ok;
                reject_reason[4] <= !accepted_claim;
                reject_reason[5] <= !independent_cert_pass;
                reject_reason[6] <= (shard_count == 0) || (shard_index >= shard_count);
                reject_reason[7] <= (expected_digest != computed_digest);
                authorize <= (observed_fields == REQUIRED)
                          && !duplicate_field
                          && schema_ok
                          && provenance_ok
                          && accepted_claim
                          && independent_cert_pass
                          && (shard_count != 0)
                          && (shard_index < shard_count)
                          && (expected_digest == computed_digest);
            end
        end
    end
endmodule

module w33_pass3198_context_trie_accountant #(
    parameter COUNT_W = 16
)(
    input  wire               clk,
    input  wire               rst,
    input  wire               start,
    input  wire               prefix_event,
    input  wire               new_prefix,
    input  wire               branch_checkpoint,
    input  wire               finish,
    output reg                done,
    output reg [COUNT_W-1:0]  distinct_prefixes,
    output reg [COUNT_W-1:0]  checkpoints,
    output wire [COUNT_W+5:0] context_bits
);
    assign context_bits = distinct_prefixes * 7'd52;
    always @(posedge clk) begin
        if (rst || start) begin
            done <= 0;
            distinct_prefixes <= 0;
            checkpoints <= 0;
        end else begin
            done <= 0;
            if (prefix_event && new_prefix)
                distinct_prefixes <= distinct_prefixes + 1'b1;
            if (prefix_event && branch_checkpoint)
                checkpoints <= checkpoints + 1'b1;
            if (finish)
                done <= 1;
        end
    end
endmodule

`default_nettype wire
