// Pass 2947: microcode for the compiled deep-M36 branch.
// Gate kind: 0=CX, 1=H, 2=MZ. Accept decoded measurement bits q0q1=01.
module w33_pass2947_m36_branch_microcode(
 input logic [4:0] step,
 output logic valid,
 output logic [1:0] kind,
 output logic [1:0] q0,q1,
 output logic accept_value
);
always_comb begin
 valid=1'b1;kind=0;q0=0;q1=0;accept_value=0;
 unique case(step)
  0: begin kind=0;q0=0;q1=1;end
  1: begin kind=0;q0=0;q1=2;end
  2: begin kind=1;q0=0;end
  3: begin kind=0;q0=1;q1=3;end
  4: begin kind=1;q0=1;end
  5: begin kind=0;q0=1;q1=3;end
  6: begin kind=0;q0=3;q1=2;end
  7: begin kind=0;q0=0;q1=3;end
  // SWAP(0,2)
  8: begin kind=0;q0=0;q1=2;end
  9: begin kind=0;q0=2;q1=0;end
 10: begin kind=0;q0=0;q1=2;end
  // SWAP(1,3)
 11: begin kind=0;q0=1;q1=3;end
 12: begin kind=0;q0=3;q1=1;end
 13: begin kind=0;q0=1;q1=3;end
 14: begin kind=1;q0=3;end // logical H
 15: begin kind=2;q0=0;accept_value=0;end
 16: begin kind=2;q0=1;accept_value=1;end
 default: begin valid=0;kind=0;q0=0;q1=0;accept_value=0;end
 endcase
end
endmodule
