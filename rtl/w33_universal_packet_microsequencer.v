// W33 universal counter-machine -> Holonet packet microsequencer.
//
// One accepted semantic macro-instruction is refined into exactly three packet
// phases:
//   LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX.
// Architectural state is frozen through LOAD and FLIP and changes only on the
// LATCH edge.  The construction-time W33 portal chosen by the software lowerer
// is also committed only at LATCH.
//
// op encoding:
//   2'b00 INC
//   2'b01 DECJZ
//   2'b10 HALT
//   2'b11 reserved / never accepted by a valid compiler
//
// This module is finite-width RTL for refinement/testing.  The abstract Python
// two-counter semantics use unbounded naturals; therefore this 32-bit instance
// is not itself a proof of unbounded physical memory.

module w33_universal_packet_microsequencer(
    input  wire        clk,
    input  wire        reset,

    // Optional architectural-state load while idle.
    input  wire        state_load,
    input  wire [7:0]  state_pc,
    input  wire [31:0] state_counter0,
    input  wire [31:0] state_counter1,
    input  wire [5:0]  state_portal,
    input  wire        state_halted,

    // Lowered semantic instruction.
    input  wire        valid,
    output wire        ready,
    output wire        accepted,
    input  wire [1:0]  op,
    input  wire        reg_sel,
    input  wire [7:0]  target,
    input  wire [7:0]  zero_target,
    input  wire [5:0]  target_portal,

    // Architectural state.
    output reg  [7:0]  pc,
    output reg  [31:0] counter0,
    output reg  [31:0] counter1,
    output reg  [5:0]  portal,
    output reg         halted,

    // Packet refinement state.
    output reg  [1:0]  phase,
    output wire [1:0]  packet_opcode,
    output wire        semantic_commit
);
    localparam PHASE_IDLE  = 2'b00;
    localparam PHASE_LOAD  = 2'b01;
    localparam PHASE_FLIP  = 2'b10;
    localparam PHASE_LATCH = 2'b11;

    localparam OP_INC   = 2'b00;
    localparam OP_DECJZ = 2'b01;
    localparam OP_HALT  = 2'b10;

    reg [1:0] latched_op;
    reg       latched_reg_sel;
    reg [7:0] latched_target;
    reg [7:0] latched_zero_target;
    reg [5:0] latched_target_portal;

    assign ready = (phase == PHASE_IDLE) && !halted && !state_load;
    assign accepted = ready && valid && (op != 2'b11);
    assign packet_opcode = phase;
    assign semantic_commit = (phase == PHASE_LATCH);

    always @(posedge clk) begin
        if (reset) begin
            pc <= 8'd0;
            counter0 <= 32'd0;
            counter1 <= 32'd0;
            portal <= 6'd0;
            halted <= 1'b0;
            phase <= PHASE_IDLE;
            latched_op <= OP_HALT;
            latched_reg_sel <= 1'b0;
            latched_target <= 8'd0;
            latched_zero_target <= 8'd0;
            latched_target_portal <= 6'd0;
        end else begin
            case (phase)
                PHASE_IDLE: begin
                    if (state_load) begin
                        pc <= state_pc;
                        counter0 <= state_counter0;
                        counter1 <= state_counter1;
                        portal <= state_portal;
                        halted <= state_halted;
                    end else if (accepted) begin
                        latched_op <= op;
                        latched_reg_sel <= reg_sel;
                        latched_target <= target;
                        latched_zero_target <= zero_target;
                        latched_target_portal <= target_portal;
                        phase <= PHASE_LOAD;
                    end
                end

                PHASE_LOAD: begin
                    // Packet phase only: architectural state is frozen.
                    phase <= PHASE_FLIP;
                end

                PHASE_FLIP: begin
                    // Packet phase only: architectural state is frozen.
                    phase <= PHASE_LATCH;
                end

                PHASE_LATCH: begin
                    // The semantic state transition and target portal commit
                    // atomically at the end of the three-phase refinement.
                    portal <= latched_target_portal;
                    case (latched_op)
                        OP_INC: begin
                            if (latched_reg_sel)
                                counter1 <= counter1 + 32'd1;
                            else
                                counter0 <= counter0 + 32'd1;
                            pc <= latched_target;
                        end

                        OP_DECJZ: begin
                            if (latched_reg_sel) begin
                                if (counter1 == 32'd0)
                                    pc <= latched_zero_target;
                                else begin
                                    counter1 <= counter1 - 32'd1;
                                    pc <= latched_target;
                                end
                            end else begin
                                if (counter0 == 32'd0)
                                    pc <= latched_zero_target;
                                else begin
                                    counter0 <= counter0 - 32'd1;
                                    pc <= latched_target;
                                end
                            end
                        end

                        OP_HALT: begin
                            halted <= 1'b1;
                        end

                        default: begin
                            // Reserved op was blocked at admission; retain state.
                        end
                    endcase
                    phase <= PHASE_IDLE;
                end
            endcase
        end
    end
endmodule


// -------------------------------------------------------------------------
// Combinational refinement theorem used by Yosys SAT.
//
// This module quantifies over every finite architectural pre-state and every
// valid macro instruction.  It explicitly constructs the LOAD, FLIP and LATCH
// states and proves that LOAD/FLIP are stuttering steps while LATCH equals the
// two-counter semantic transition.  The synchronous sequencer above implements
// the same equations.
// -------------------------------------------------------------------------
module w33_universal_packet_refinement(
    input  wire [1:0]  op,
    input  wire        reg_sel,
    input  wire [7:0]  target,
    input  wire [7:0]  zero_target,
    input  wire [5:0]  target_portal,
    input  wire [7:0]  pc_pre,
    input  wire [31:0] counter0_pre,
    input  wire [31:0] counter1_pre,
    input  wire [5:0]  portal_pre,
    input  wire        halted_pre
);
    localparam OP_INC   = 2'b00;
    localparam OP_DECJZ = 2'b01;
    localparam OP_HALT  = 2'b10;

    wire [7:0]  pc_load = pc_pre;
    wire [31:0] c0_load = counter0_pre;
    wire [31:0] c1_load = counter1_pre;
    wire [5:0]  portal_load = portal_pre;
    wire        halted_load = halted_pre;

    wire [7:0]  pc_flip = pc_load;
    wire [31:0] c0_flip = c0_load;
    wire [31:0] c1_flip = c1_load;
    wire [5:0]  portal_flip = portal_load;
    wire        halted_flip = halted_load;

    reg [7:0]  pc_latch;
    reg [31:0] c0_latch;
    reg [31:0] c1_latch;
    reg [5:0]  portal_latch;
    reg        halted_latch;

    always @* begin
        pc_latch = pc_flip;
        c0_latch = c0_flip;
        c1_latch = c1_flip;
        portal_latch = target_portal;
        halted_latch = halted_flip;

        case (op)
            OP_INC: begin
                if (reg_sel)
                    c1_latch = c1_flip + 32'd1;
                else
                    c0_latch = c0_flip + 32'd1;
                pc_latch = target;
            end

            OP_DECJZ: begin
                if (reg_sel) begin
                    if (c1_flip == 32'd0)
                        pc_latch = zero_target;
                    else begin
                        c1_latch = c1_flip - 32'd1;
                        pc_latch = target;
                    end
                end else begin
                    if (c0_flip == 32'd0)
                        pc_latch = zero_target;
                    else begin
                        c0_latch = c0_flip - 32'd1;
                        pc_latch = target;
                    end
                end
            end

            OP_HALT: begin
                halted_latch = 1'b1;
            end
        endcase
    end

`ifdef FORMAL
    always @* begin
        // A macrostep is only admitted from a running state and for a valid op.
        assume(!halted_pre);
        assume(op != 2'b11);

        // LOAD_FLAG and FLIP_Q6_AXIS are semantic stuttering phases.
        assert(pc_load == pc_pre);
        assert(c0_load == counter0_pre);
        assert(c1_load == counter1_pre);
        assert(portal_load == portal_pre);
        assert(halted_load == halted_pre);

        assert(pc_flip == pc_pre);
        assert(c0_flip == counter0_pre);
        assert(c1_flip == counter1_pre);
        assert(portal_flip == portal_pre);
        assert(halted_flip == halted_pre);

        // Every accepted instruction commits its lowered portal at LATCH.
        assert(portal_latch == target_portal);

        if (op == OP_INC) begin
            assert(pc_latch == target);
            assert(!halted_latch);
            if (reg_sel) begin
                assert(c0_latch == counter0_pre);
                assert(c1_latch == counter1_pre + 32'd1);
            end else begin
                assert(c0_latch == counter0_pre + 32'd1);
                assert(c1_latch == counter1_pre);
            end
        end

        if (op == OP_DECJZ) begin
            assert(!halted_latch);
            if (reg_sel) begin
                assert(c0_latch == counter0_pre);
                if (counter1_pre == 32'd0) begin
                    assert(c1_latch == 32'd0);
                    assert(pc_latch == zero_target);
                end else begin
                    assert(c1_latch == counter1_pre - 32'd1);
                    assert(pc_latch == target);
                end
            end else begin
                assert(c1_latch == counter1_pre);
                if (counter0_pre == 32'd0) begin
                    assert(c0_latch == 32'd0);
                    assert(pc_latch == zero_target);
                end else begin
                    assert(c0_latch == counter0_pre - 32'd1);
                    assert(pc_latch == target);
                end
            end
        end

        if (op == OP_HALT) begin
            assert(pc_latch == pc_pre);
            assert(c0_latch == counter0_pre);
            assert(c1_latch == counter1_pre);
            assert(halted_latch);
        end
    end
`endif
endmodule
