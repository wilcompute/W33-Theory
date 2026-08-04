`timescale 1ns/1ps
`default_nettype none

module tb_w33_pass3196_3201_epoch_envelope_virtualization;
    reg clk=0; always #5 clk=~clk;
    reg rst=1;

    reg epoch_start=0, symbol_valid=0, epoch_finish=0;
    reg [4:0] symbol=0;
    wire epoch_done, epoch_accept, epoch_ambiguous;
    wire [3:0] phase, distance;

    reg env_start=0, field_valid=0, env_finish=0;
    reg [3:0] field_id=0;
    reg schema_ok=0, provenance_ok=0, accepted_claim=0, independent_cert_pass=0;
    reg [8:0] shard_index=0, shard_count=0;
    reg [255:0] expected_digest=0, computed_digest=0;
    wire env_done, authorize;
    wire [7:0] reject_reason;
    wire [11:0] observed_fields;

    reg trie_start=0, prefix_event=0, new_prefix=0, branch_checkpoint=0, trie_finish=0;
    wire trie_done;
    wire [15:0] distinct_prefixes, checkpoints;
    wire [21:0] context_bits;

    w33_pass3196_epoch4_decoder epoch(
        .clk(clk),.rst(rst),.start(epoch_start),.symbol_valid(symbol_valid),.symbol(symbol),
        .finish(epoch_finish),.done(epoch_done),.accept(epoch_accept),.phase(phase),
        .distance(distance),.ambiguous(epoch_ambiguous));
    w33_pass3197_proof_envelope_authorizer envelope(
        .clk(clk),.rst(rst),.start(env_start),.field_valid(field_valid),.field_id(field_id),
        .finish(env_finish),.schema_ok(schema_ok),.provenance_ok(provenance_ok),
        .accepted_claim(accepted_claim),.independent_cert_pass(independent_cert_pass),
        .shard_index(shard_index),.shard_count(shard_count),.expected_digest(expected_digest),
        .computed_digest(computed_digest),.done(env_done),.authorize(authorize),
        .reject_reason(reject_reason),.observed_fields(observed_fields));
    w33_pass3198_context_trie_accountant trie(
        .clk(clk),.rst(rst),.start(trie_start),.prefix_event(prefix_event),.new_prefix(new_prefix),
        .branch_checkpoint(branch_checkpoint),.finish(trie_finish),.done(trie_done),
        .distinct_prefixes(distinct_prefixes),.checkpoints(checkpoints),.context_bits(context_bits));

    task pulse_epoch_start; begin
        @(negedge clk); epoch_start=1; @(negedge clk); epoch_start=0;
    end endtask
    task send_symbol(input [4:0] value); begin
        @(negedge clk); symbol=value; symbol_valid=1; @(negedge clk); symbol_valid=0;
    end endtask
    task finish_epoch; begin
        @(negedge clk); epoch_finish=1; @(negedge clk); epoch_finish=0;
        @(posedge clk); #1;
    end endtask
    task pulse_env_start; begin
        @(negedge clk); env_start=1; @(negedge clk); env_start=0;
    end endtask
    task send_field(input [3:0] value); begin
        @(negedge clk); field_id=value; field_valid=1; @(negedge clk); field_valid=0;
    end endtask
    task finish_env; begin
        @(negedge clk); env_finish=1; @(negedge clk); env_finish=0;
        @(posedge clk); #1;
    end endtask

    integer i;
    initial begin
        repeat(3) @(posedge clk); rst=0;

        pulse_epoch_start();
        for(i=0;i<5;i=i+1) send_symbol(8);
        send_symbol(0); send_symbol(2); send_symbol(7); send_symbol(23);
        finish_epoch();
        if(!epoch_accept || phase!=5 || distance!=4 || epoch_ambiguous) $fatal(1,"four-edit epoch decode failed");

        pulse_epoch_start();
        for(i=0;i<4;i=i+1) send_symbol(8);
        for(i=0;i<5;i=i+1) send_symbol(0);
        finish_epoch();
        if(epoch_accept || distance<5) $fatal(1,"radius-five word was accepted");

        pulse_env_start();
        schema_ok=1; provenance_ok=1; accepted_claim=1; independent_cert_pass=1;
        shard_index=9; shard_count=256;
        expected_digest=256'h1234; computed_digest=256'h1234;
        for(i=0;i<12;i=i+1) send_field(i[3:0]);
        finish_env();
        if(!authorize || reject_reason!=0) $fatal(1,"valid proof envelope rejected");

        pulse_env_start();
        for(i=0;i<12;i=i+1) send_field(i[3:0]);
        computed_digest=256'h4321;
        finish_env();
        if(authorize || !reject_reason[7]) $fatal(1,"digest mismatch authorized");

        @(negedge clk); trie_start=1; @(negedge clk); trie_start=0;
        for(i=0;i<70;i=i+1) begin
            @(negedge clk); prefix_event=1; new_prefix=1; branch_checkpoint=(i<63);
            @(negedge clk); prefix_event=0; new_prefix=0; branch_checkpoint=0;
        end
        @(negedge clk); trie_finish=1; @(negedge clk); trie_finish=0;
        @(posedge clk); #1;
        if(distinct_prefixes!=70 || checkpoints!=63 || context_bits!=3640)
            $fatal(1,"trie accounting mismatch");

        $display("PASS four-edit epoch, proof-envelope authorization, concurrent trie accounting");
        $finish;
    end
endmodule

`default_nettype wire
