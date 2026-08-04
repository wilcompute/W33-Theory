// Pass 3164: three exact affine ISA maps on the four-trit Pauli frame.
// Trits use 2-bit encodings 0,1,2; 3 is illegal and fails closed.
module w33_pass3164_tri_isa_decoder #(
    parameter integer FIXED_MODE = -1  // -1 runtime, 0 current4, 1 low4, 2 fast6
)(
    input  logic [7:0] frame_i,      // {zf,xf,zp,xp}, two bits each
    input  logic [1:0] mode_i,
    input  logic [2:0] opcode_i,
    output logic [7:0] frame_o,
    output logic valid_o
);
    logic [1:0] xp,zp,xf,zf,nxp,nzp,nxf,nzf;
    logic [1:0] mode;
    function automatic [1:0] add3(input [1:0] a,input [1:0] b);
      integer t; begin t=a+b; add3=(t>=3)?t-3:t; end
    endfunction
    function automatic [1:0] sub3(input [1:0] a,input [1:0] b);
      integer t; begin t=a+3-b; sub3=(t>=3)?t-3:t; end
    endfunction
    function automatic [1:0] neg3(input [1:0] a);
      begin case(a) 2'd0:neg3=0;2'd1:neg3=2;2'd2:neg3=1;default:neg3=3;endcase end
    endfunction
    task automatic apply_fp; begin nxp=neg3(zp);nzp=xp;end endtask
    task automatic apply_ff; begin nxf=neg3(zf);nzf=xf;end endtask
    task automatic apply_cxpf; begin nzp=sub3(zp,zf);nxf=add3(xf,xp);end endtask
    task automatic apply_cxfp; begin nxp=add3(xp,xf);nzf=sub3(zf,zp);end endtask
    always_comb begin
      xp=frame_i[1:0];zp=frame_i[3:2];xf=frame_i[5:4];zf=frame_i[7:6];
      nxp=xp;nzp=zp;nxf=xf;nzf=zf;valid_o=(xp<3 && zp<3 && xf<3 && zf<3);
      mode=(FIXED_MODE<0)?mode_i:FIXED_MODE[1:0];
      if(valid_o) begin
        case(mode)
          2'd0: case(opcode_i) // current4 = Fp,CXpf,CXfp,Z1
            0:apply_fp();1:apply_cxpf();2:apply_cxfp();3:nzp=add3(zp,1);default:valid_o=0;endcase
          2'd1: case(opcode_i) // low4 = CXfp,CXpf,Ff,Z0
            0:apply_cxfp();1:apply_cxpf();2:apply_ff();3:nxp=add3(xp,1);default:valid_o=0;endcase
          2'd2: case(opcode_i) // fast6 = Ff,CXpf,CXfp,Z0,Z1,Z3
            0:apply_ff();1:apply_cxpf();2:apply_cxfp();3:nxp=add3(xp,1);
            4:nzp=add3(zp,1);5:nzf=add3(zf,1);default:valid_o=0;endcase
          default:valid_o=0;
        endcase
      end
      frame_o=valid_o?{nzf,nxf,nzp,nxp}:frame_i;
    end
endmodule

module w33_pass3164_current4(input logic [7:0] frame_i,input logic [2:0] opcode_i,output logic [7:0] frame_o,output logic valid_o);
  w33_pass3164_tri_isa_decoder #(.FIXED_MODE(0)) u(.frame_i,.mode_i('0),.opcode_i,.frame_o,.valid_o);
endmodule
module w33_pass3164_low4(input logic [7:0] frame_i,input logic [2:0] opcode_i,output logic [7:0] frame_o,output logic valid_o);
  w33_pass3164_tri_isa_decoder #(.FIXED_MODE(1)) u(.frame_i,.mode_i('0),.opcode_i,.frame_o,.valid_o);
endmodule
module w33_pass3164_fast6(input logic [7:0] frame_i,input logic [2:0] opcode_i,output logic [7:0] frame_o,output logic valid_o);
  w33_pass3164_tri_isa_decoder #(.FIXED_MODE(2)) u(.frame_i,.mode_i('0),.opcode_i,.frame_o,.valid_o);
endmodule
