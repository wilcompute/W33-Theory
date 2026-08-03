// Pass 2770: complete eight-opcode Holonet controller with M36 and remote-link control.
module w33_pass2770_holonet_top(
  input logic clk, rst, start,
  input logic [2:0] opcode,
  input logic operand,
  input logic [1:0] p_in, f_in, xp_in, zp_in, xf_in, zf_in,
  input logic [2:0] d12_a_in, d12_c_in,
  input logic d12_b_in, d12_d_in,
  input logic [5:0] magic_id,
  input logic magic_ack,
  output logic busy, done, error,
  output logic [1:0] p_out, f_out, xp_out, zp_out, xf_out, zf_out,
  output logic [2:0] d12_a_out,
  output logic d12_b_out,
  output logic magic_req, magic_valid,
  output logic [1:0] magic_dark_mode, magic_grade,
  output logic [2:0] magic_phase6_0, magic_phase6_1, magic_phase6_2, magic_phase6_3
);
  logic factory_valid;
  logic [1:0] factory_dark, factory_grade;
  logic [2:0] ph0,ph1,ph2,ph3;
  w33_pass2767_m36_factory factory(
    .ray_id(magic_id), .valid(factory_valid), .dark_mode(factory_dark),
    .phase6_0(ph0), .phase6_1(ph1), .phase6_2(ph2), .phase6_3(ph3), .grade(factory_grade)
  );

  function automatic logic [1:0] add3(input logic [1:0] a, input logic [1:0] b);
    logic [2:0] s; begin s=a+b; add3=(s>=3)?s-3:s; end
  endfunction
  function automatic logic [1:0] neg3(input logic [1:0] a);
    case(a) 2'd0:neg3=0; 2'd1:neg3=2; default:neg3=1; endcase
  endfunction
  function automatic logic [1:0] sub3(input logic [1:0] a, input logic [1:0] b);
    sub3=add3(a,neg3(b));
  endfunction
  function automatic logic [2:0] add6(input logic [2:0] a, input logic [2:0] b);
    logic [3:0] s; begin s=a+b; add6=(s>=6)?s-6:s; end
  endfunction
  function automatic logic [2:0] neg6(input logic [2:0] a);
    neg6=(a==0)?0:6-a;
  endfunction

  always_ff @(posedge clk) begin
    if (rst) begin
      busy<=0; done<=0; error<=0; magic_req<=0; magic_valid<=0;
      p_out<=0; f_out<=0; xp_out<=0; zp_out<=0; xf_out<=0; zf_out<=0;
      d12_a_out<=0; d12_b_out<=0; magic_dark_mode<=0; magic_grade<=0;
      magic_phase6_0<=0; magic_phase6_1<=0; magic_phase6_2<=0; magic_phase6_3<=0;
    end else begin
      done<=0; error<=0;
      if (!busy && start) begin
        p_out<=p_in; f_out<=f_in; xp_out<=xp_in; zp_out<=zp_in; xf_out<=xf_in; zf_out<=zf_in;
        d12_a_out<=d12_a_in; d12_b_out<=d12_b_in; magic_req<=0; magic_valid<=0;
        case(opcode)
          3'b000: begin xp_out<=neg3(zp_in); zp_out<=xp_in; done<=1; end
          3'b001: begin xf_out<=neg3(zf_in); zf_out<=xf_in; done<=1; end
          3'b010: begin zp_out<=add3(zp_in,xp_in); done<=1; end
          3'b011: begin zf_out<=add3(zf_in,xf_in); done<=1; end
          3'b100: begin
            if (!operand) begin f_out<=add3(f_in,p_in); zp_out<=sub3(zp_in,zf_in); xf_out<=add3(xf_in,xp_in); end
            else begin p_out<=add3(p_in,f_in); xp_out<=add3(xp_in,xf_in); zf_out<=sub3(zf_in,zp_in); end
            done<=1;
          end
          3'b101: begin if (!operand) zp_out<=add3(zp_in,1); else zf_out<=add3(zf_in,1); done<=1; end
          3'b110: begin
            if (d12_a_in>5 || d12_c_in>5) begin error<=1; done<=1; end
            else begin d12_a_out<=add6(d12_a_in,d12_b_in?neg6(d12_c_in):d12_c_in); d12_b_out<=d12_b_in^d12_d_in; done<=1; end
          end
          3'b111: begin
            if (!factory_valid) begin error<=1; done<=1; end
            else begin
              busy<=1; magic_req<=1; magic_valid<=1; magic_dark_mode<=factory_dark; magic_grade<=factory_grade;
              magic_phase6_0<=ph0; magic_phase6_1<=ph1; magic_phase6_2<=ph2; magic_phase6_3<=ph3;
            end
          end
          default: begin error<=1; done<=1; end
        endcase
      end else if (busy && magic_ack) begin
        busy<=0; magic_req<=0; done<=1;
      end
    end
  end
endmodule
