// Pass 2828 -- finite-delay support observer for the 81-state ternary frame.
//
// support_i ordering:
//   support_i[3] = supp(x_p)
//   support_i[2] = supp(z_p)
//   support_i[1] = supp(x_f)
//   support_i[0] = supp(z_f)
//
// op_o encoding (the exact Pass-2803 internal micro-ISA):
//   2'b00 = F_p
//   2'b01 = CX_{p->f}
//   2'b10 = CX_{f->p}
//   2'b11 = Z_p
//
// Canonical diagnostic word:
//   CX_{p->f}, F_p, Z_p, F_p, Z_p, CX_{p->f}
//
// Protocol:
//   * assert start_i for one cycle while idle; support_i is the t=0 support;
//   * while busy_o, op_valid_o/op_o present the next operation;
//   * pulse advance_i after that operation has been applied and support_i contains
//     the post-operation support snapshot;
//   * done_o pulses with code_o valid after the sixth advance.
//
// code_o ordering is the canonical minimal selector
// (flattened support columns 0,1,2,5,13,21,25,26):
//   [7] t0 x_p, [6] t0 z_p, [5] t0 x_f, [4] t1 z_p,
//   [3] t3 z_p, [2] t5 z_p, [1] t6 z_p, [0] t6 x_f.
//
// The exact verifier proves that no seven support taps identify all 81 states,
// while this eight-tap code does.  This block sequences and samples the code; an
// 81-entry generated ROM performs code_o -> ternary-frame decoding.

module w33_pass2828_support_observer (
    input  logic       clk_i,
    input  logic       rst_ni,
    input  logic       start_i,
    input  logic       advance_i,
    input  logic [3:0] support_i,
    output logic       busy_o,
    output logic       done_o,
    output logic       op_valid_o,
    output logic [1:0] op_o,
    output logic [7:0] code_o
);

  logic [2:0] step_q;
  logic [7:0] code_q;

  localparam logic [1:0] OP_FP    = 2'b00;
  localparam logic [1:0] OP_CX_PF = 2'b01;
  localparam logic [1:0] OP_ZP    = 2'b11;

  always_comb begin
    unique case (step_q)
      3'd0: op_o = OP_CX_PF;
      3'd1: op_o = OP_FP;
      3'd2: op_o = OP_ZP;
      3'd3: op_o = OP_FP;
      3'd4: op_o = OP_ZP;
      3'd5: op_o = OP_CX_PF;
      default: op_o = OP_FP;
    endcase
  end

  assign op_valid_o = busy_o;
  assign code_o = code_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_o <= 1'b0;
      done_o <= 1'b0;
      step_q <= 3'd0;
      code_q <= 8'b0;
    end else begin
      done_o <= 1'b0;

      if (!busy_o) begin
        if (start_i) begin
          // t=0 mandatory/selected taps.
          code_q[7] <= support_i[3];  // x_p
          code_q[6] <= support_i[2];  // z_p
          code_q[5] <= support_i[1];  // x_f
          code_q[4:0] <= 5'b0;
          step_q <= 3'd0;
          busy_o <= 1'b1;
        end
      end else if (advance_i) begin
        unique case (step_q)
          3'd0: begin
            // post-op time t=1
            code_q[4] <= support_i[2];  // z_p
            step_q <= 3'd1;
          end
          3'd1: begin
            // time t=2: no selected tap
            step_q <= 3'd2;
          end
          3'd2: begin
            // post-op time t=3
            code_q[3] <= support_i[2];  // z_p
            step_q <= 3'd3;
          end
          3'd3: begin
            // time t=4: no selected tap
            step_q <= 3'd4;
          end
          3'd4: begin
            // post-op time t=5
            code_q[2] <= support_i[2];  // z_p
            step_q <= 3'd5;
          end
          3'd5: begin
            // post-op time t=6
            code_q[1] <= support_i[2];  // z_p
            code_q[0] <= support_i[1];  // x_f
            busy_o <= 1'b0;
            done_o <= 1'b1;
            step_q <= 3'd0;
          end
          default: begin
            busy_o <= 1'b0;
            step_q <= 3'd0;
          end
        endcase
      end
    end
  end

`ifdef FORMAL
  logic [3:0] advances_q;
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni || (start_i && !busy_o)) begin
      advances_q <= 4'd0;
    end else if (busy_o && advance_i) begin
      advances_q <= advances_q + 4'd1;
    end
  end

  // The observer finishes after exactly six accepted advances.
  always_ff @(posedge clk_i) begin
    if (rst_ni && done_o) begin
      assert (advances_q == 4'd6);
      assert (!busy_o);
    end
    if (rst_ni && busy_o) begin
      assert (step_q <= 3'd5);
      assert (op_valid_o);
    end
  end
`endif

endmodule
