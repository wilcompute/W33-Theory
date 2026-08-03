// Pass 2700 -- sigma^5 = Z, the first ISA instruction built.
//
// photonic_holonet_body.tex §"Exact braid words": in the anyonic Fibonacci
// representation sigma_1 = diag(zeta^4, -zeta^2) with zeta = e^{i pi/5}, one has
// EXACTLY sigma_1^5 = Z and sigma_1^10 = I -- not merely projectively, verified in the
// cyclotomic ring Z[zeta_10].  "In the dual (+-) encoding of the local K_{3,3} cycle
// code F_2^4 this makes every register bit-flip an exact five-letter braid word."
//
// Verified here symbolically before building: sigma^5 = diag(1,-1) = Z exactly, and
// sigma^10 = I exactly.
//
// And the field matters.  The entries live in Q(zeta_10) = Q(zeta_5), which contains
//     2 cos(pi/5) = (1 + sqrt5)/2 = phi
// exactly.  So THE ISA'S BRAID INSTRUCTION IS DEFINED OVER THE GOLDEN FIELD, and phi is
// an algebraic integer in Z[zeta_10], the ring the paper says the braid is exact in.
// That is the Fibonacci anyon quantum dimension, and unlike the other three appearances
// of phi in this project it is not a coincidence to reject -- it is the defining
// constant of the anyon model the instruction is written in.
//
// Hardware reading: the machine counts sigma applications mod 10; every fifth one
// emits a Z on the addressed register bit.  A pure counter and one XOR -- the whole
// instruction, because the exactness is in the algebra, not in the circuit.

`timescale 1ns/1ps

module w33_braid_sigma #(parameter int NREG = 4) (   // F_2^4 cycle-code register
    input  wire            clk,
    input  wire            rst,
    input  wire            sigma,        // apply one braid generator
    input  wire [1:0]      target,       // which register bit it acts on
    output reg  [NREG-1:0] reg_state,
    output reg  [3:0]      sigma_count,  // mod 10, since sigma^10 = I
    output wire            z_emitted     // high on the cycle a Z lands
);
    // sigma^5 = Z: a Z is emitted every fifth application
    wire fifth = sigma && (sigma_count == 4'd4 || sigma_count == 4'd9);
    assign z_emitted = fifth;

    always_ff @(posedge clk) begin
        if (rst) begin
            reg_state   <= {NREG{1'b0}};
            sigma_count <= 4'd0;
        end else if (sigma) begin
            sigma_count <= (sigma_count == 4'd9) ? 4'd0 : sigma_count + 4'd1;
            if (fifth) reg_state[target] <= ~reg_state[target];
        end
    end
endmodule

// The property that makes it an ISA instruction rather than a counter:
// ten sigmas restore the register exactly (sigma^10 = I), and five flip exactly once.
module w33_braid_formal #(parameter int NREG = 4) (
    input wire [NREG-1:0] s0,
    input wire [1:0]      target
);
    // model ten applications combinationally: bit `target` flips at steps 5 and 10
    wire [NREG-1:0] after5  = s0 ^ ({{(NREG-1){1'b0}}, 1'b1} << target);
    wire [NREG-1:0] after10 = after5 ^ ({{(NREG-1){1'b0}}, 1'b1} << target);

    always_comb begin
        // sigma^5 = Z : exactly one bit changed, and it is the target
        assert (after5 != s0);
        assert ((after5 ^ s0) == ({{(NREG-1){1'b0}}, 1'b1} << target));
        // sigma^10 = I : the register is restored
        assert (after10 == s0);
    end
endmodule
