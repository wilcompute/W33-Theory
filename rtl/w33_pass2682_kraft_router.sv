// Pass 2682 -- the Bell-compass parabolic router, in hardware.
//
// photonic_holonet_body.tex Theorem "Bell-compass parabolic router": the projective
// Siegel parabolic 3^3:S4 has four orbits on the 1296 incident compass pairs,
//
//     162_L + 162_R + 324 + 648
//
// whose normalised sizes satisfy the KRAFT EQUALITY exactly,
//
//     2^-3 + 2^-3 + 2^-2 + 2^-1 = 1,
//
// so they admit the complete prefix decoder
//
//     0   -> dark mirror  (648)     enter mirror bus
//     10  -> schedule     (324)     timetable-local route
//     110 -> left cache   (162_L)
//     111 -> right cache  (162_R)
//
// with expected word length (1/2)(1) + (1/4)(2) + 2(1/8)(3) = 7/4 under the invariant
// uniform measure.  The paper's point, which is the reason this is worth building:
// "the code lengths were not optimized from assumed traffic probabilities: they were
// read from exact group orbits."  A Huffman coder derives its tree from measured
// statistics; this tree is a theorem about PSp(4,3) orbits.
//
// The outer Weyl involution fuses the two 162 cache orbits, so W(E6) sees
// 324_cache + 324_schedule + 648_mirror and only PSp(4,3) resolves the chiral bit.
// That is exposed here as a `chiral_resolved` input: dropping it collapses 110/111
// to a two-bit 11, which is the W(E6) view.

`timescale 1ns/1ps

// ---------------------------------------------------------------------------
// Encoder: orbit class -> variable-length prefix word.
//   class 0 = mirror, 1 = schedule, 2 = left cache, 3 = right cache
// ---------------------------------------------------------------------------
module w33_kraft_encode (
    input  wire [1:0] cls,
    input  wire       chiral_resolved,   // 0 = W(E6) view, fuses the two caches
    output reg  [2:0] word,              // left-aligned, unused low bits zero
    output reg  [1:0] len                // 1, 2 or 3
);
    always_comb begin
        case (cls)
            2'd0: begin word = 3'b0__00; len = 2'd1; end          // 0
            2'd1: begin word = 3'b10_0;  len = 2'd2; end          // 10
            2'd2: begin
                     if (chiral_resolved) begin word = 3'b110; len = 2'd3; end
                     else                 begin word = 3'b11_0; len = 2'd2; end
                  end
            default: begin
                     if (chiral_resolved) begin word = 3'b111; len = 2'd3; end
                     else                 begin word = 3'b11_0; len = 2'd2; end
                  end
        endcase
    end
endmodule

// ---------------------------------------------------------------------------
// Decoder: self-delimiting, constant depth.  Consumes 1..3 bits.
// ---------------------------------------------------------------------------
module w33_kraft_decode (
    input  wire [2:0] bits,              // next up to three stream bits, MSB first
    input  wire       chiral_resolved,
    output reg  [1:0] cls,
    output reg  [1:0] consumed
);
    always_comb begin
        if (bits[2] == 1'b0)      begin cls = 2'd0; consumed = 2'd1; end   // 0
        else if (bits[1] == 1'b0) begin cls = 2'd1; consumed = 2'd2; end   // 10
        else if (!chiral_resolved) begin cls = 2'd2; consumed = 2'd2; end  // 11 fused
        else if (bits[0] == 1'b0) begin cls = 2'd2; consumed = 2'd3; end   // 110
        else                      begin cls = 2'd3; consumed = 2'd3; end   // 111
    end
endmodule

// ---------------------------------------------------------------------------
// The router: classify a compass pair by its orbit, emit the route word, and
// drive the four engineering actions the paper names.
// ---------------------------------------------------------------------------
module w33_bell_compass_router (
    input  wire        clk,
    input  wire        rst,
    input  wire        valid,
    input  wire [1:0]  orbit_class,
    input  wire        chiral_resolved,
    output wire [2:0]  route_word,
    output wire [1:0]  route_len,
    output reg         to_mirror_bus,
    output reg         to_timetable,
    output reg         to_cache_left,
    output reg         to_cache_right
);
    w33_kraft_encode enc (.cls(orbit_class), .chiral_resolved(chiral_resolved),
                          .word(route_word), .len(route_len));
    always_ff @(posedge clk) begin
        if (rst) begin
            to_mirror_bus <= 0; to_timetable <= 0;
            to_cache_left <= 0; to_cache_right <= 0;
        end else begin
            to_mirror_bus  <= valid && (orbit_class == 2'd0);
            to_timetable   <= valid && (orbit_class == 2'd1);
            to_cache_left  <= valid && (orbit_class == 2'd2);
            to_cache_right <= valid && (orbit_class == 2'd3);
        end
    end
endmodule
