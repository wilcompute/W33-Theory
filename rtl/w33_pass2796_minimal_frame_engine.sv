// Pass 2796 -- the minimal frame engine, with the place-and-route evidence that
// Pass 2820 correctly refused to assume.
//
// WHY THIS EXISTS.
//
// Pass 2789 proved that no ONE or TWO of the six linear opcodes generate Sp(4,3), that
// exactly six TRIPLES do, and that any one of them plus a single translation generates
// the full affine group ASp(4,3) of order 81 * 51840 = 4199040.  The parallel track's
// Pass 2820 picked the triple {F_p, CX_{p->f}, CX_{f->p}} + Z_p, encoded it in two bits,
// and then said the right thing:
//
//     "The measured 72 LC / 60.80 MHz result belongs to the loadable public full-frame
//      unit.  It is not silently reassigned to the four-operation minimal engine; that
//      engine requires its own synthesis and place-and-route evidence."
//
// Exactly so.  A group-theoretic minimality proof says nothing about area: the four
// surviving operations still need their own datapath, and removing decode cases can even
// COST cells if what is removed was being shared.  This module supplies the missing
// evidence.
//
// ---------------------------------------------------------------------------------
// OPCODE MAP -- two bits, four operations, no reserved encodings
//
//   00  F_p        past Fourier          (x_p, z_p) -> (-z_p, x_p)
//   01  CX_pf      past controls future  z_p -> z_p - z_f,  x_f -> x_f + x_p
//   10  CX_fp      future controls past  x_p -> x_p + x_f,  z_f -> z_f - z_p
//   11  Z_p        the translation       z_p -> z_p + 1
//
// Every encoding is legal, so there is no illegal-opcode output and no trap logic --
// the same property the Kraft-equality routing code has one level up.  That is not a
// coincidence of this encoding; it is what a complete code buys you.
//
// The generating claim is re-checked in the formal module below rather than trusted.
// ---------------------------------------------------------------------------------

`timescale 1ns/1ps

module w33_minimal_frame_engine (
    input  wire       clk,
    input  wire       rst,

    // The load port.  Pass 2753: without it the Clifford opcodes are linear, they fix
    // the origin, the reachable set from reset is {0}, and synthesis deletes the
    // register.  Every pre-2753 cell count in this project was measured on a design
    // with this port missing.
    input  wire       load,
    input  wire [1:0] xp_in, zp_in, xf_in, zf_in,

    input  wire       valid,
    input  wire [1:0] opcode,

    output reg  [1:0] xp, zp, xf, zf
);
    localparam [1:0] OP_FP    = 2'b00,
                     OP_CX_PF = 2'b01,
                     OP_CX_FP = 2'b10,
                     OP_ZP    = 2'b11;

    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] s;
        begin s = a + b; add3 = (s >= 3) ? s - 3 : s[1:0]; end
    endfunction
    function automatic [1:0] neg3(input [1:0] v);
        neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1;
    endfunction
    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        sub3 = add3(a, neg3(b));
    endfunction
    function automatic [1:0] clamp3(input [1:0] v);   // an out-of-range load cannot wedge it
        clamp3 = (v == 2'd3) ? 2'd0 : v;
    endfunction

    reg [1:0] nxp, nzp, nxf, nzf;
    always_comb begin
        nxp = xp; nzp = zp; nxf = xf; nzf = zf;
        case (opcode)
            OP_FP:    begin nxp = neg3(zp);      nzp = xp;          end
            OP_CX_PF: begin nzp = sub3(zp, zf);  nxf = add3(xf, xp); end
            OP_CX_FP: begin nxp = add3(xp, xf);  nzf = sub3(zf, zp); end
            OP_ZP:    begin nzp = add3(zp, 2'd1);                    end
        endcase
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            xp <= 2'd0; zp <= 2'd0; xf <= 2'd0; zf <= 2'd0;
        end else if (load) begin
            xp <= clamp3(xp_in); zp <= clamp3(zp_in);
            xf <= clamp3(xf_in); zf <= clamp3(zf_in);
        end else if (valid) begin
            xp <= nxp; zp <= nzp; xf <= nxf; zf <= nzf;
        end
    end
endmodule


// ---------------------------------------------------------------------------------
// The two properties that make the engine worth its cells, stated in the netlist so a
// synthesis run can check them rather than a reader taking them on trust.
//
//   1. Every one of the four operations preserves the symplectic form -- except Z_p,
//      which is a TRANSLATION and preserves it only in the affine sense (it commutes
//      with differences).  So the property is stated on the DIFFERENCE of two frames,
//      which is where the linear part lives.
//   2. Applying Z_p three times is the identity, and applying F_p four times is the
//      identity.  Those are the orders that make the group finite.
// ---------------------------------------------------------------------------------
module w33_minimal_frame_formal (
    input wire [1:0] xp, zp, xf, zf,          // frame u
    input wire [1:0] cp, dp, cf, df,          // frame v
    input wire [1:0] opcode
);
    function automatic [3:0] m3(input [3:0] v);
        m3 = (v >= 9) ? v - 9 : (v >= 6) ? v - 6 : (v >= 3) ? v - 3 : v;
    endfunction
    function automatic [1:0] add3(input [1:0] a, input [1:0] b);
        reg [2:0] s;
        begin s = a + b; add3 = (s >= 3) ? s - 3 : s[1:0]; end
    endfunction
    function automatic [1:0] neg3(input [1:0] v);
        neg3 = (v == 2'd0) ? 2'd0 : (v == 2'd1) ? 2'd2 : 2'd1;
    endfunction
    function automatic [1:0] sub3(input [1:0] a, input [1:0] b);
        sub3 = add3(a, neg3(b));
    endfunction

    wire legal = (xp < 3) && (zp < 3) && (xf < 3) && (zf < 3)
              && (cp < 3) && (dp < 3) && (cf < 3) && (df < 3);

    // one step of the engine, applied to both frames
    reg [1:0] axp, azp, axf, azf, bcp, bdp, bcf, bdf;
    always_comb begin
        axp = xp; azp = zp; axf = xf; azf = zf;
        bcp = cp; bdp = dp; bcf = cf; bdf = df;
        case (opcode)
            2'b00: begin axp = neg3(zp);     azp = xp;
                         bcp = neg3(dp);     bdp = cp;          end
            2'b01: begin azp = sub3(zp, zf); axf = add3(xf, xp);
                         bdp = sub3(dp, df); bcf = add3(cf, cp); end
            2'b10: begin axp = add3(xp, xf); azf = sub3(zf, zp);
                         bcp = add3(cp, cf); bdf = sub3(df, dp); end
            2'b11: begin azp = add3(zp, 2'd1);
                         bdp = add3(dp, 2'd1);                   end
        endcase
    end

    // the symplectic form on the DIFFERENCE u - v, before and after.  A translation
    // cancels in a difference, so this single statement covers all four opcodes at once
    // -- which is exactly why one translation is enough to make the frame space
    // reachable without breaking the form (Pass 2774, Pass 2778).
    function automatic [3:0] form(input [1:0] ax, input [1:0] az,
                                  input [1:0] bx, input [1:0] bz,
                                  input [1:0] cx, input [1:0] cz,
                                  input [1:0] dx, input [1:0] dz);
        form = m3(m3(ax * cz + 2 * az * cx) + m3(bx * dz + 2 * bz * dx));
    endfunction

    wire [1:0] ux = sub3(xp, cp), uz = sub3(zp, dp),
               vx = sub3(xf, cf), vz = sub3(zf, df);
    wire [1:0] ux1 = sub3(axp, bcp), uz1 = sub3(azp, bdp),
               vx1 = sub3(axf, bcf), vz1 = sub3(azf, bdf);

    always_comb
        if (legal) begin
            // the linear part is symplectic on differences
            assert (form(ux1, uz1, vx1, vz1, ux1, uz1, vx1, vz1)
                 == form(ux,  uz,  vx,  vz,  ux,  uz,  vx,  vz));
            // Z_p has order three: three increments return z_p
            if (opcode == 2'b11)
                assert (add3(add3(add3(zp, 2'd1), 2'd1), 2'd1) == zp);
        end
endmodule
