`timescale 1ns/1ps
module tb_w33_pass3232_port_compiler;
    logic [5:0] block_id;
    logic [3:0] local_slot;
    logic valid;
    logic [7:0] support_edge;
    logic [1:0] port0, port1, port2;
    logic [13:0] expected [0:719];
    integer b, s, idx;

    w33_pass3232_port_compiler dut(
        .block_id(block_id), .local_slot(local_slot), .valid(valid),
        .support_edge(support_edge), .port0(port0), .port1(port1), .port2(port2)
    );

    initial begin
        $readmemh("data/bt3232_port_rom.mem", expected);
        for (b = 0; b < 45; b = b + 1) begin
            for (s = 0; s < 16; s = s + 1) begin
                block_id = b[5:0]; local_slot = s[3:0]; #1;
                idx = 16*b+s;
                if (!valid) $fatal(1, "valid low at block=%0d slot=%0d", b, s);
                if ({support_edge,port0,port1,port2} !== expected[idx])
                    $fatal(1, "ROM mismatch at %0d", idx);
            end
        end
        block_id = 6'd45; local_slot = 4'd0; #1;
        if (valid || {support_edge,port0,port1,port2} !== 14'd0)
            $fatal(1, "invalid block did not fail closed");
        $display("PASS 720/720 port compiler words and invalid-block gate");
        $finish;
    end
endmodule
