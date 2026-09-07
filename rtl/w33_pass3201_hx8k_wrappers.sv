`default_nettype none

// Placement wrappers preserve the production cores while preventing package I/O
// from dominating the HX8K experiment. They are evidence harnesses, not protocol
// replacements; the full-width interfaces remain in the production RTL.
module w33_pass3201_epoch_hx8k_top(
    input  wire       clk,
    input  wire       rst,
    input  wire       start,
    input  wire       symbol_valid,
    input  wire [4:0] symbol,
    input  wire       finish,
    output wire       done,
    output wire       accept,
    output wire [3:0] phase,
    output wire [3:0] distance,
    output wire       ambiguous
);
    w33_pass3196_epoch4_decoder core(
        .clk(clk), .rst(rst), .start(start), .symbol_valid(symbol_valid),
        .symbol(symbol), .finish(finish), .done(done), .accept(accept),
        .phase(phase), .distance(distance), .ambiguous(ambiguous));
endmodule

module w33_pass3201_envelope_hx8k_top(
    input  wire        clk,
    input  wire        rst,
    input  wire        start,
    input  wire        field_valid,
    input  wire [3:0]  field_id,
    input  wire        finish,
    input  wire [5:0]  policy_bits,
    input  wire [8:0]  shard_index,
    input  wire [8:0]  shard_count,
    input  wire [31:0] expected_digest_word,
    input  wire [31:0] computed_digest_word,
    output wire        done,
    output wire        authorize,
    output wire [7:0]  reject_reason,
    output wire [11:0] observed_fields
);
    wire [255:0] expected_digest = {8{expected_digest_word}};
    wire [255:0] computed_digest = {8{computed_digest_word}};
    w33_pass3197_proof_envelope_authorizer core(
        .clk(clk), .rst(rst), .start(start), .field_valid(field_valid),
        .field_id(field_id), .finish(finish), .schema_ok(policy_bits[0]),
        .provenance_ok(policy_bits[1]), .accepted_claim(policy_bits[2]),
        .independent_cert_pass(policy_bits[3]), .shard_index(shard_index),
        .shard_count(shard_count), .expected_digest(expected_digest),
        .computed_digest(computed_digest), .done(done), .authorize(authorize),
        .reject_reason(reject_reason), .observed_fields(observed_fields));
endmodule

module w33_pass3201_context_hx8k_top(
    input  wire        clk,
    input  wire        rst,
    input  wire        start,
    input  wire        prefix_event,
    input  wire        new_prefix,
    input  wire        branch_checkpoint,
    input  wire        finish,
    output wire        done,
    output wire [15:0] distinct_prefixes,
    output wire [15:0] checkpoints,
    output wire [21:0] context_bits
);
    w33_pass3198_context_trie_accountant core(
        .clk(clk), .rst(rst), .start(start), .prefix_event(prefix_event),
        .new_prefix(new_prefix), .branch_checkpoint(branch_checkpoint),
        .finish(finish), .done(done), .distinct_prefixes(distinct_prefixes),
        .checkpoints(checkpoints), .context_bits(context_bits));
endmodule

`default_nettype wire
