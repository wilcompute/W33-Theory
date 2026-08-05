// Pass 3507: objectwise RM(1,4) encoder on the S3-equivariant Q4 hyperplane.
module w33_rm14_equivariant_encode(
    input wire [4:0] message,
    output wire [15:0] codeword
);
    assign codeword[0]=^(message&5'd1); assign codeword[1]=^(message&5'd2);
    assign codeword[2]=^(message&5'd4); assign codeword[3]=^(message&5'd7);
    assign codeword[4]=^(message&5'd9); assign codeword[5]=^(message&5'd12);
    assign codeword[6]=^(message&5'd18); assign codeword[7]=^(message&5'd20);
    assign codeword[8]=^(message&5'd25); assign codeword[9]=^(message&5'd26);
    assign codeword[10]=^(message&5'd10); assign codeword[11]=^(message&5'd17);
    assign codeword[12]=^(message&5'd28); assign codeword[13]=^(message&5'd15);
    assign codeword[14]=^(message&5'd23); assign codeword[15]=^(message&5'd31);
endmodule
