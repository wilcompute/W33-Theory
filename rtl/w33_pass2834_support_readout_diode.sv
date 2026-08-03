// Pass 2834 -- the support readout, built as a DIODE, with a gate-level proof.
//
// Pass 2822 (parallel track) proved the architectural law:
//
//     support for readout, phase for execution
//
// because support is not a congruence -- (0,1,0,0) and (0,2,0,0) share the mask 0100,
// and Z_p sends them to masks 0100 and 0000.  A machine that stored only support could
// not predict its own next state.
//
// That is a theorem about the mathematics.  It is not, by itself, a property of any
// particular netlist: nothing stops an engineer from wiring the cheap 4-bit mask back
// into the execution path, and the resulting machine would pass simulation almost
// always, because support IS preserved by most operations.  It would drift the first
// time a translation fired on a register holding a 2.
//
// So the law needs to be enforced structurally, not documented.  This module is the
// enforcement: the frame engine and the support extractor, wired so that information
// flows in exactly one direction, plus the check that PROVES it at the gate level
// (scripts/check_information_flow.py, run on the flattened netlist).
//
//     frame flops  ---->  support mask        must be reachable
//     support mask ---->  frame flops         must be UNREACHABLE
//
// The second is the interesting one and it is what "typed" should mean in hardware: not
// a naming convention, a reachability proof over the synthesised gate graph.
//
// A tamper port is deliberately provided.  It exists so the check has something to bite
// on: `tamper_mask` is an input that a careless integration COULD route into the
// datapath, and the proof asserts that in this design it does not reach the frame.
// A guard that can only ever pass is not a guard (Pass 2781).

`timescale 1ns/1ps

module w33_support_readout_diode (
    input  wire       clk,
    input  wire       rst,
    input  wire       load,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,
    input  wire       valid,
    input  wire [1:0] opcode,
    input  wire [3:0] tamper_mask,      // must NOT reach the frame; see the header

    output wire [3:0] support_mask,     // the readout: 1 where the trit is nonzero
    output wire [1:0] xp_o, zp_o, xf_o, zf_o
);
    wire [1:0] xp, zp, xf, zf;

    w33_minimal_frame_engine engine (
        .clk(clk), .rst(rst), .load(load),
        .xp_in(xp_in), .zp_in(zp_in), .xf_in(xf_in), .zf_in(zf_in),
        .valid(valid), .opcode(opcode),
        .xp(xp), .zp(zp), .xf(xf), .zf(zf)
    );

    // The readout.  Purely combinational, purely downstream: four OR gates.
    assign support_mask = { (zf != 2'd0), (xf != 2'd0), (zp != 2'd0), (xp != 2'd0) };

    assign xp_o = xp; assign zp_o = zp; assign xf_o = xf; assign zf_o = zf;
endmodule


// The non-congruence, stated in the netlist so the theorem travels with the design.
// (0,1,0,0) and (0,2,0,0) have the same mask; after Z_p their masks differ.  If someone
// "optimises" the engine so that this stops being true, the engine is wrong.
module w33_support_noncongruence_formal (
    input wire [1:0] zp_a, zp_b
);
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] s;
        begin s = a + b; add3 = (s >= 3) ? s - 3 : s[1:0]; end
    endfunction

    wire legal   = (zp_a < 3) && (zp_b < 3);
    wire same_in = ((zp_a != 2'd0) == (zp_b != 2'd0));      // same support before
    wire [1:0] za = add3(zp_a, 2'd1), zb = add3(zp_b, 2'd1); // after Z_p
    wire same_out = ((za != 2'd0) == (zb != 2'd0));

    always_comb
        if (legal && (zp_a == 2'd1) && (zp_b == 2'd2)) begin
            // the explicit witness pair from Pass 2822
            assert (same_in);        // indistinguishable before
            assert (!same_out);      // distinguishable after
        end
endmodule
