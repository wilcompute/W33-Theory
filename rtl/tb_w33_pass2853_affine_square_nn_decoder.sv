`timescale 1ns/1ps
module tb_w33_pass2853_affine_square_nn_decoder;
    logic clk = 0;
    logic rst_n = 0;
    logic start = 0;
    logic [23:0] received;
    logic busy, done, corrected_valid;
    logic [7:0] decoded_frame;
    logic [4:0] best_distance;
    logic [23:0] clean_code;
    logic clean_legal;

    always #5 clk = ~clk;

    w33_pass2848_affine_square_feature_encoder reference_encoder (
        .x_p(2'd1), .z_p(2'd2), .x_f(2'd0), .z_f(2'd1),
        .code(clean_code), .legal(clean_legal)
    );

    w33_pass2853_affine_square_nn_decoder dut (
        .clk(clk), .rst_n(rst_n), .start(start), .received(received),
        .busy(busy), .done(done), .corrected_valid(corrected_valid),
        .decoded_frame(decoded_frame), .best_distance(best_distance)
    );

    initial begin
        repeat (3) @(posedge clk);
        rst_n <= 1;
        @(posedge clk);
        if (!clean_legal) $fatal(1, "reference trits rejected");
        received <= clean_code ^ 24'h000001;
        start <= 1;
        @(posedge clk);
        start <= 0;
        wait(done);
        if (!corrected_valid) $fatal(1, "one-bit word not accepted");
        if (decoded_frame !== 8'h49) $fatal(1, "decoded frame %h != 49", decoded_frame);
        if (best_distance !== 5'd1) $fatal(1, "distance %0d != 1", best_distance);
        $display("PASS decoder corrected frame 0x49 at distance one");
        $finish;
    end
endmodule
