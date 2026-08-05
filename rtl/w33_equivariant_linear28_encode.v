`default_nettype none
module w33_equivariant_linear28_encode(
    input  wire [4:0] message,
    output wire [27:0] codeword
);
    assign codeword[0]  = ^(message & 5'd1);
    assign codeword[1]  = ^(message & 5'd2);
    assign codeword[2]  = ^(message & 5'd4);
    assign codeword[3]  = ^(message & 5'd7);
    assign codeword[4]  = ^(message & 5'd8);
    assign codeword[5]  = ^(message & 5'd16);
    assign codeword[6]  = ^(message & 5'd24);
    assign codeword[7]  = ^(message & 5'd8);
    assign codeword[8]  = ^(message & 5'd16);
    assign codeword[9]  = ^(message & 5'd24);
    assign codeword[10] = ^(message & 5'd9);
    assign codeword[11] = ^(message & 5'd12);
    assign codeword[12] = ^(message & 5'd18);
    assign codeword[13] = ^(message & 5'd20);
    assign codeword[14] = ^(message & 5'd25);
    assign codeword[15] = ^(message & 5'd26);
    assign codeword[16] = ^(message & 5'd10);
    assign codeword[17] = ^(message & 5'd17);
    assign codeword[18] = ^(message & 5'd28);
    assign codeword[19] = ^(message & 5'd11);
    assign codeword[20] = ^(message & 5'd14);
    assign codeword[21] = ^(message & 5'd19);
    assign codeword[22] = ^(message & 5'd21);
    assign codeword[23] = ^(message & 5'd29);
    assign codeword[24] = ^(message & 5'd30);
    assign codeword[25] = ^(message & 5'd13);
    assign codeword[26] = ^(message & 5'd22);
    assign codeword[27] = ^(message & 5'd27);
endmodule
`default_nettype wire
