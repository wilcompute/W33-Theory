// 24 Sep 2026: four-null-counter / tetracode / ADQC controller ABI.
// Trits use 2'b00,01,10 for 0,1,2; 2'b11 is invalid.
module w33_temporal_tetracode_adqc_controller(
    input  wire [1:0] n_inf,
    input  wire [1:0] n_zero,
    input  wire [1:0] n_plus,
    input  wire [1:0] n_minus,
    input  wire       c3_apply,
    input  wire       pw_enable,
    input  wire       pw_reverse,
    input  wire       t_enable,
    output reg  [1:0] hist_a,
    output reg  [1:0] hist_b,
    output reg  [1:0] hist_c,
    output reg        tetracode_plane,
    output reg  [1:0] common_mode_correction,
    output reg  [1:0] program_id,
    output reg        invalid_trit
);

  reg [1:0] m_inf, m_zero, m_plus, m_minus;
  reg [3:0] sum_a, sum_b, sum_c, sum_sigma;
  function [1:0] mod3;
    input [3:0] x;
    begin
      case (x)
        4'd0, 4'd3, 4'd6, 4'd9: mod3 = 2'd0;
        4'd1, 4'd4, 4'd7:       mod3 = 2'd1;
        default:                mod3 = 2'd2;
      endcase
    end
  endfunction

  function [1:0] neg3;
    input [1:0] x;
    begin
      case (x)
        2'd0: neg3 = 2'd0;
        2'd1: neg3 = 2'd2;
        default: neg3 = 2'd1;
      endcase
    end
  endfunction

  always @* begin
    invalid_trit = (n_inf   == 2'd3) ||
                   (n_zero  == 2'd3) ||
                   (n_plus  == 2'd3) ||
                   (n_minus == 2'd3);
    // C3 fixes infinity and cycles zero -> plus -> minus -> zero.
    if (c3_apply) begin
      m_inf   = n_inf;
      m_zero  = n_plus;
      m_plus  = n_minus;
      m_minus = n_zero;
    end else begin
      m_inf   = n_inf;
      m_zero  = n_zero;
      m_plus  = n_plus;
      m_minus = n_minus;
    end

    // Sym_2(F3) history coordinates.
    sum_a = {2'b00,m_zero} + {2'b00,m_plus} + {2'b00,m_minus};
    sum_b = {2'b00,m_plus} + ({2'b00,m_minus} << 1);
    sum_c = {2'b00,m_inf} + {2'b00,m_plus} + {2'b00,m_minus};
    hist_a = mod3(sum_a);
    hist_b = mod3(sum_b);
    hist_c = mod3(sum_c);

    // Standard tetracode is the plane a=0 with sigma=0 gauge.
    sum_sigma = {2'b00,m_inf} + {2'b00,m_plus}
                + ({2'b00,m_minus} << 1);
    tetracode_plane = (!invalid_trit) && (hist_a == 2'd0);
    if (tetracode_plane)
      common_mode_correction = neg3(mod3(sum_sigma));
    else
      common_mode_correction = 2'd0;

    // Analyzer program:
    // 0: F / Clifford baseline
    // 1: Page-Wootters forward R=Z
    // 2: Page-Wootters reverse R=Z^-1
    // 3: non-Clifford qutrit T (mu_9 analyzer)
    if (t_enable)
      program_id = 2'd3;
    else if (pw_enable && pw_reverse)
      program_id = 2'd2;
    else if (pw_enable)
      program_id = 2'd1;
    else
      program_id = 2'd0;
  end
endmodule
