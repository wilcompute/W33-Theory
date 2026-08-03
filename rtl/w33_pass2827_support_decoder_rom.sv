// Pass 2827 -- generated 81-entry support telemetry decoder.
// Input code ordering is defined by w33_pass2828_support_observer.sv.
// Output packs four ternary coordinates as two-bit fields:
//   state_o[7:6]=x_p, [5:4]=z_p, [3:2]=x_f, [1:0]=z_f.
// Only 00, 01, and 10 occur in each field. Unused 8-bit codes are invalid.

module w33_pass2827_support_decoder_rom (
    input  logic [7:0] code_i,
    output logic [7:0] state_o,
    output logic       valid_o
);
  always_comb begin
    state_o = 8'b0;
    valid_o = 1'b0;
    unique case (code_i)
      8'b00001111: begin state_o = 8'b00000000; valid_o = 1'b1; end
      8'b00011111: begin state_o = 8'b00000001; valid_o = 1'b1; end
      8'b00011011: begin state_o = 8'b00000010; valid_o = 1'b1; end
      8'b00101110: begin state_o = 8'b00000100; valid_o = 1'b1; end
      8'b00111110: begin state_o = 8'b00000101; valid_o = 1'b1; end
      8'b00111010: begin state_o = 8'b00000110; valid_o = 1'b1; end
      8'b00101111: begin state_o = 8'b00001000; valid_o = 1'b1; end
      8'b00111111: begin state_o = 8'b00001001; valid_o = 1'b1; end
      8'b00111011: begin state_o = 8'b00001010; valid_o = 1'b1; end
      8'b01011001: begin state_o = 8'b00010000; valid_o = 1'b1; end
      8'b01001101: begin state_o = 8'b00010001; valid_o = 1'b1; end
      8'b01011101: begin state_o = 8'b00010010; valid_o = 1'b1; end
      8'b01111000: begin state_o = 8'b00010100; valid_o = 1'b1; end
      8'b01101100: begin state_o = 8'b00010101; valid_o = 1'b1; end
      8'b01111100: begin state_o = 8'b00010110; valid_o = 1'b1; end
      8'b01111001: begin state_o = 8'b00011000; valid_o = 1'b1; end
      8'b01101101: begin state_o = 8'b00011001; valid_o = 1'b1; end
      8'b01111101: begin state_o = 8'b00011010; valid_o = 1'b1; end
      8'b01011111: begin state_o = 8'b00100000; valid_o = 1'b1; end
      8'b01011011: begin state_o = 8'b00100001; valid_o = 1'b1; end
      8'b01001111: begin state_o = 8'b00100010; valid_o = 1'b1; end
      8'b01111110: begin state_o = 8'b00100100; valid_o = 1'b1; end
      8'b01111010: begin state_o = 8'b00100101; valid_o = 1'b1; end
      8'b01101110: begin state_o = 8'b00100110; valid_o = 1'b1; end
      8'b01111111: begin state_o = 8'b00101000; valid_o = 1'b1; end
      8'b01111011: begin state_o = 8'b00101001; valid_o = 1'b1; end
      8'b01101111: begin state_o = 8'b00101010; valid_o = 1'b1; end
      8'b10001111: begin state_o = 8'b01000000; valid_o = 1'b1; end
      8'b10011111: begin state_o = 8'b01000001; valid_o = 1'b1; end
      8'b10011011: begin state_o = 8'b01000010; valid_o = 1'b1; end
      8'b10101110: begin state_o = 8'b01000100; valid_o = 1'b1; end
      8'b10111110: begin state_o = 8'b01000101; valid_o = 1'b1; end
      8'b10111010: begin state_o = 8'b01000110; valid_o = 1'b1; end
      8'b10101111: begin state_o = 8'b01001000; valid_o = 1'b1; end
      8'b10111111: begin state_o = 8'b01001001; valid_o = 1'b1; end
      8'b10111011: begin state_o = 8'b01001010; valid_o = 1'b1; end
      8'b11011001: begin state_o = 8'b01010000; valid_o = 1'b1; end
      8'b11001101: begin state_o = 8'b01010001; valid_o = 1'b1; end
      8'b11011101: begin state_o = 8'b01010010; valid_o = 1'b1; end
      8'b11111000: begin state_o = 8'b01010100; valid_o = 1'b1; end
      8'b11101100: begin state_o = 8'b01010101; valid_o = 1'b1; end
      8'b11111100: begin state_o = 8'b01010110; valid_o = 1'b1; end
      8'b11111001: begin state_o = 8'b01011000; valid_o = 1'b1; end
      8'b11101101: begin state_o = 8'b01011001; valid_o = 1'b1; end
      8'b11111101: begin state_o = 8'b01011010; valid_o = 1'b1; end
      8'b11011111: begin state_o = 8'b01100000; valid_o = 1'b1; end
      8'b11011011: begin state_o = 8'b01100001; valid_o = 1'b1; end
      8'b11001111: begin state_o = 8'b01100010; valid_o = 1'b1; end
      8'b11111110: begin state_o = 8'b01100100; valid_o = 1'b1; end
      8'b11111010: begin state_o = 8'b01100101; valid_o = 1'b1; end
      8'b11101110: begin state_o = 8'b01100110; valid_o = 1'b1; end
      8'b11111111: begin state_o = 8'b01101000; valid_o = 1'b1; end
      8'b11111011: begin state_o = 8'b01101001; valid_o = 1'b1; end
      8'b11101111: begin state_o = 8'b01101010; valid_o = 1'b1; end
      8'b10000111: begin state_o = 8'b10000000; valid_o = 1'b1; end
      8'b10010111: begin state_o = 8'b10000001; valid_o = 1'b1; end
      8'b10010011: begin state_o = 8'b10000010; valid_o = 1'b1; end
      8'b10100110: begin state_o = 8'b10000100; valid_o = 1'b1; end
      8'b10110110: begin state_o = 8'b10000101; valid_o = 1'b1; end
      8'b10110010: begin state_o = 8'b10000110; valid_o = 1'b1; end
      8'b10100111: begin state_o = 8'b10001000; valid_o = 1'b1; end
      8'b10110111: begin state_o = 8'b10001001; valid_o = 1'b1; end
      8'b10110011: begin state_o = 8'b10001010; valid_o = 1'b1; end
      8'b11010001: begin state_o = 8'b10010000; valid_o = 1'b1; end
      8'b11000101: begin state_o = 8'b10010001; valid_o = 1'b1; end
      8'b11010101: begin state_o = 8'b10010010; valid_o = 1'b1; end
      8'b11110000: begin state_o = 8'b10010100; valid_o = 1'b1; end
      8'b11100100: begin state_o = 8'b10010101; valid_o = 1'b1; end
      8'b11110100: begin state_o = 8'b10010110; valid_o = 1'b1; end
      8'b11110001: begin state_o = 8'b10011000; valid_o = 1'b1; end
      8'b11100101: begin state_o = 8'b10011001; valid_o = 1'b1; end
      8'b11110101: begin state_o = 8'b10011010; valid_o = 1'b1; end
      8'b11010111: begin state_o = 8'b10100000; valid_o = 1'b1; end
      8'b11010011: begin state_o = 8'b10100001; valid_o = 1'b1; end
      8'b11000111: begin state_o = 8'b10100010; valid_o = 1'b1; end
      8'b11110110: begin state_o = 8'b10100100; valid_o = 1'b1; end
      8'b11110010: begin state_o = 8'b10100101; valid_o = 1'b1; end
      8'b11100110: begin state_o = 8'b10100110; valid_o = 1'b1; end
      8'b11110111: begin state_o = 8'b10101000; valid_o = 1'b1; end
      8'b11110011: begin state_o = 8'b10101001; valid_o = 1'b1; end
      8'b11100111: begin state_o = 8'b10101010; valid_o = 1'b1; end
      default: begin state_o = 8'b0; valid_o = 1'b0; end
    endcase
  end
endmodule
