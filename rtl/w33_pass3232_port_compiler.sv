module w33_pass3232_port_compiler (
    input  logic [5:0] block_id,
    input  logic [3:0] local_slot,
    output logic       valid,
    output logic [7:0] support_edge,
    output logic [1:0] port0,
    output logic [1:0] port1,
    output logic [1:0] port2
);
    logic [13:0] rom [0:719];
    logic [9:0] address;
    logic [13:0] word;

    initial $readmemh("data/bt3232_port_rom.mem", rom);

    always_comb begin
        address = {block_id, local_slot};
        valid = (block_id < 6'd45);
        word = valid ? rom[address] : 14'd0;
        support_edge = word[13:6];
        port0 = word[5:4];
        port1 = word[3:2];
        port2 = word[1:0];
    end
endmodule
