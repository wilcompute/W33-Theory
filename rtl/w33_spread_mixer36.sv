// ===================================================================================
// DEPRECATED (Pass 2793).  DO NOT BUILD ON THIS FILE.  Use instead:
//
//     rtl/w33_pass2773_spread_mixer36_synth.sv   ->  w33_spread_mixer36_synth
//
// Despite the header below, this file is SYNTHESIZABLE BY NOTHING.  Both frontends in
// this repository reject it, for two different unsupported constructs:
//
//     yosys    line 7   syntax error, unexpected '['
//                       (unpacked array PORTS:  input logic signed [W-1:0] x [0:35])
//     iverilog line 10  sorry: unpacked array parameters are not supported yet
//                       (the MASK localparam)
//
// It has therefore never been simulated or synthesized since it was committed on
// 2026-08-02, and it is not a "structural RTL reference" in any usable sense -- no tool
// in this repo can read it.  Found by scripts/check_rtl_folds.py on its first
// repo-wide sweep (Pass 2772).
//
// The replacement is a PORT, not a redesign: identical arithmetic, with the unpacked
// ports replaced by one packed bus and the unpacked mask by a packed 1296-bit constant.
// It is SAT-proved on the signed-impulse class (1,097,152 variables / 3,185,010 clauses)
// and synthesises to 13,965 SB_LUT4 + 799 SB_CARRY at W = 16 -- which is 1.8x the
// HX8K's 7,680 logic cells, so the fully parallel mixer does not fit any iCE40 here.
// That is why rtl/w33_pass2612_serial_mixer.sv (4,048 LC, 19.65 MHz) exists.
//
// The text below is kept verbatim as the historical record.  It is not compiled.
// ===================================================================================
//
// Pass 2206: synthesizable reference datapaths for the exact W(3,3) spread mixer.
// This is a structural RTL reference, not a timing-closed FPGA result.
module w33_spread_mixer36 #(
    parameter int W = 16,
    parameter int OW = W + 4
) (
    input  logic signed [W-1:0]  x [0:35],
    output logic signed [OW-1:0] y [0:35]
);
    localparam logic [35:0] MASK [0:35] = '{
        36'h00a323cf6,36'h0094c5b6d,36'h00c81e79b,36'h6a0c4c0f6,
        36'hb20a3216d,36'hc6078119b,36'h39306099b,36'h4d610856d,
        36'h9550902f6,36'h950c4bd06,36'h4d0a35a85,36'h390786643,
        36'hc63066623,36'hb2610da15,36'h6a5093c0e,36'h27a55228c,
        36'h2792ac514,36'h8b9951451,36'h53a8a924a,36'h53c354922,
        36'h8bc4aa8a1,36'h74ac90c31,36'hac9b08a2a,36'hd8c66061c,
        36'hace435142,36'h74d24b0c1,36'hd8b986184,36'h007ff8007,
        36'he001f8fc0,36'h1c01ff038,36'h1a36197a0,36'h165d24cc8,
        36'h0e6ac2b50,36'hc1361e858,36'ha16ac54a8,36'h615d23330
    };
    integer i,j;
    always_comb begin
        for (i=0;i<36;i=i+1) begin
            y[i]='0;
            for (j=0;j<36;j=j+1)
                if (MASK[i][j]) y[i]=y[i]+{{(OW-W){x[j][W-1]}},x[j]};
        end
    end
endmodule

// Actual canonical single-J image.  C4 and C6 rotations share one phase circle,
// so they generate C12; adding conjugation gives D24, not a faithful order-48 image.
module w33_single_j_phase_controller (
    input logic clk,input logic rst_n,
    input logic [1:0] step4,input logic [2:0] step6,input logic reflect,
    output logic [3:0] phase12,output logic conjugated
);
    logic [5:0] raw; logic [3:0] delta12;
    always_comb begin raw=(3*step4)+(2*step6); delta12=raw%12; end
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin phase12<=4'd0; conjugated<=1'b0; end
        else if (reflect) begin phase12<=(phase12==0)?0:12-phase12; conjugated<=~conjugated; end
        else phase12<=(phase12+delta12)%12;
    end
endmodule
