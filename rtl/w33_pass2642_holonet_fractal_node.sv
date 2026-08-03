// Pass 2642 -- a ternary recursion demonstrator.
//
// RELABELLED at Pass 2686.  This was published as "a node whose network has the same
// shape as the node", justified by the E8 > A2 + E6 branching.  That justification is
// WITHDRAWN, for three independent reasons:
//   1. the holonet fractal is 40-ary (BT827: replace each of the 40 POINTS), not 3-ary;
//   2. photonic_holonet_body.tex line 680 states that the E6 x A2 < E8 branching action
//      and the transitive W33-code action are NONCONJUGATE with different root-orbit
//      fingerprints;
//   3. the same line calls using it "a chamber calibration rather than a
//      symmetry-forced device frame".
//
// What remains true is only about this circuit: it is a recursive module with an
// identical port signature at every depth, placed at depths 0-3, with the exact
// measured law LC(d) = 75*3^d - 2.  It models no object in this project.
//
// The brief: minimal hardware that replicates itself, so that the machine, the program
// and the network are one object, self-similar inward and outward.
//
// The substrate answers it rather than the designer.  E8 has a maximal subalgebra
// A2 + E6, and the adjoint branches as
//
//     248 = (8,1) + (1,78) + (3,27) + (3bar,27bar)          8 + 78 + 81 + 81 = 248
//
// read as architecture:
//     (1,78)   one E6 machine core
//     (8,1)    the A2 qutrit PHASE BUS  (8 = adjoint of su(3))
//     (3,27)   THREE copies of the 27-register, indexed by a qutrit
//
// So one E8 node is three E6 nodes tied by an A2 bus.  The branching factor is 3
// because q = 3.  The self-similarity is not a design choice -- it is the branching
// rule of the GKP tower A2 < D4 < E8 the corpus already names.
//
// Realised here as a recursive module.  A node of depth d:
//     holds 9 * 3^d trits          (depth 0 = one 27, i.e. a 3x3 F3 matrix)
//     instantiates THREE nodes of depth d-1
//     emits ONE trit of phase, the F3 sum of its children's phases
//
// The register widens by 3 per level; the PHASE INTERFACE IS IDENTICAL AT EVERY DEPTH.
// That is the precise sense in which the network of nodes is itself a node: a depth-d
// assembly presents exactly the port signature of a depth-0 leaf.  Same shape, different
// scale -- self-similarity, not mere repetition.
//
// The leaf is the Pass 2632 E6 cubic (det over F3 on the 27), exhaustively verified on
// all 3^9 inputs.  So the fractal is built from a gate that is already proved correct.

`timescale 1ns/1ps

module w33_holonet_node #(parameter int DEPTH = 0) (
    input  wire                          clk,
    input  wire                          rst,
    input  wire                          en,
    input  wire [18*(3**DEPTH)-1:0]      x_flat,   // 9*3^DEPTH trits, 2 bits each
    output wire [1:0]                    phase     // ONE trit -- same at every depth
);
    generate
        if (DEPTH == 0) begin : leaf
            // a single E6 cubic: 9 trits -> det mod 3, accumulated on the mu_3 clock
            w33_cubic_phase_gate g (
                .clk(clk), .rst(rst), .en(en),
                .x_flat(x_flat[17:0]), .phase(phase));
        end else begin : branch
            localparam int CW = 18*(3**(DEPTH-1));   // child register width in bits
            wire [1:0] cp [0:2];
            genvar c;
            for (c = 0; c < 3; c = c + 1) begin : child
                w33_holonet_node #(.DEPTH(DEPTH-1)) n (
                    .clk(clk), .rst(rst), .en(en),
                    .x_flat(x_flat[c*CW +: CW]),
                    .phase(cp[c]));
            end
            // the A2 bus: the parent's phase is the F3 sum of its children's
            wire [1:0] s01;
            w33_f3_add b0 (.a(cp[0]), .b(cp[1]), .y(s01));
            w33_f3_add b1 (.a(s01),   .b(cp[2]), .y(phase));
        end
    endgenerate
endmodule

// Concrete instances to measure the scaling law.  Each presents the SAME phase port.
module w33_holonet_d0 (input wire clk, rst, en, input wire [17:0]    x, output wire [1:0] p);
    w33_holonet_node #(.DEPTH(0)) u (.clk(clk), .rst(rst), .en(en), .x_flat(x), .phase(p));
endmodule
module w33_holonet_d1 (input wire clk, rst, en, input wire [53:0]    x, output wire [1:0] p);
    w33_holonet_node #(.DEPTH(1)) u (.clk(clk), .rst(rst), .en(en), .x_flat(x), .phase(p));
endmodule
module w33_holonet_d2 (input wire clk, rst, en, input wire [161:0]   x, output wire [1:0] p);
    w33_holonet_node #(.DEPTH(2)) u (.clk(clk), .rst(rst), .en(en), .x_flat(x), .phase(p));
endmodule
module w33_holonet_d3 (input wire clk, rst, en, input wire [485:0]   x, output wire [1:0] p);
    w33_holonet_node #(.DEPTH(3)) u (.clk(clk), .rst(rst), .en(en), .x_flat(x), .phase(p));
endmodule
