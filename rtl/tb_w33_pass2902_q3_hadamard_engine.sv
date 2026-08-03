`timescale 1ns/1ps
module tb_w33_pass2902_q3_hadamard_engine;
    localparam integer IN_W=12;
    localparam integer OUT_W=24;
    logic clk=0, rst=1, start=0;
    logic signed [15*IN_W-1:0] in_flat;
    logic signed [15*OUT_W-1:0] dense_flat;
    logic busy, out_valid, done;
    logic [3:0] out_index;
    logic signed [OUT_W-1:0] out_value;
    integer i, probe, cycles, seen;
    integer value;

    always #5 clk = ~clk;

    w33_pass2902_q3_dense_reference #(.IN_W(IN_W),.OUT_W(OUT_W)) refm(
        .in_flat(in_flat), .out_flat(dense_flat));
    w33_pass2902_q3_hadamard_engine #(.IN_W(IN_W),.ACC_W(OUT_W)) dut(
        .clk(clk),.rst(rst),.start(start),.in_flat(in_flat),
        .busy(busy),.out_valid(out_valid),.out_index(out_index),
        .out_value(out_value),.done(done));

    task automatic run_one;
        begin
            @(posedge clk); start <= 1;
            @(posedge clk); start <= 0;
            cycles=0; seen=0;
            while (!done) begin
                @(posedge clk); #1; cycles=cycles+1;
                if (out_valid) begin
                    if ($signed(out_value) !== $signed(dense_flat[out_index*OUT_W +: OUT_W])) begin
                        $display("MISMATCH idx=%0d got=%0d expected=%0d", out_index,
                                 $signed(out_value), $signed(dense_flat[out_index*OUT_W +: OUT_W]));
                        $fatal(1);
                    end
                    seen=seen+1;
                end
                if (cycles > 60) $fatal(1,"timeout");
            end
            if (seen != 15) $fatal(1,"expected 15 outputs, saw %0d",seen);
            if (cycles != 47) $fatal(1,"expected 47 work cycles, saw %0d",cycles);
        end
    endtask

    initial begin
        in_flat='0;
        repeat(3) @(posedge clk);
        rst <= 0;
        // Fifteen basis vectors.
        for (i=0; i<15; i=i+1) begin
            in_flat='0;
            in_flat[i*IN_W +: IN_W]=1;
            run_one();
        end
        // Thirty-two deterministic signed probes used by the exact Python certificate.
        for (probe=0; probe<32; probe=probe+1) begin
            for (i=0; i<15; i=i+1) begin
                value = ((17*probe + 11*i + 5) % 15) - 7;
                in_flat[i*IN_W +: IN_W] = value;
            end
            run_one();
        end
        $display("PASS pass2902 dense/butterfly equivalence");
        $finish;
    end
endmodule
