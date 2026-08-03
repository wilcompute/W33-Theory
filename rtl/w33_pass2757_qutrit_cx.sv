// Pass 2757 -- qutrit controlled-add (SUM/CX) instruction.
//
// Computational data path: |p,f> -> |p,f+p mod 3>
// Pauli frame: (xp,zp,xf,zf) -> (xp,zp-zf,xf+xp,zf).
// The matrix has order 3 and (M-I)^2=0 with rank(M-I)=2: a
// rank-two Lagrangian unipotent (Jordan type 2+2), not a transvection.
`timescale 1ns/1ps

module w33_qutrit_cx_data(
    input wire [1:0] p, input wire [1:0] f,
    output wire [1:0] p_out, output wire [1:0] f_out
);
    function automatic [1:0] add3(input [1:0] a,input [1:0] b);
        reg [2:0] sum;
        begin sum=a+b; add3=(sum>=3)?sum-3:sum[1:0]; end
    endfunction
    assign p_out=p;
    assign f_out=add3(f,p);
endmodule

module w33_qutrit_cx_frame_map(
    input wire [1:0] xp,input wire [1:0] zp,
    input wire [1:0] xf,input wire [1:0] zf,
    output wire [1:0] xp_out,output wire [1:0] zp_out,
    output wire [1:0] xf_out,output wire [1:0] zf_out
);
    function automatic [1:0] add3(input [1:0] a,input [1:0] b);
        reg [2:0] sum;
        begin sum=a+b; add3=(sum>=3)?sum-3:sum[1:0]; end
    endfunction
    function automatic [1:0] sub3(input [1:0] a,input [1:0] b);
        begin
            case({a,b})
                {2'd0,2'd0}:sub3=2'd0; {2'd0,2'd1}:sub3=2'd2;
                {2'd0,2'd2}:sub3=2'd1; {2'd1,2'd0}:sub3=2'd1;
                {2'd1,2'd1}:sub3=2'd0; {2'd1,2'd2}:sub3=2'd2;
                {2'd2,2'd0}:sub3=2'd2; {2'd2,2'd1}:sub3=2'd1;
                default:sub3=2'd0;
            endcase
        end
    endfunction
    assign xp_out=xp;
    assign zp_out=sub3(zp,zf);
    assign xf_out=add3(xf,xp);
    assign zf_out=zf;
endmodule

module w33_qutrit_cx_frame(
    input wire clk,input wire rst,input wire apply_cx,
    output reg [1:0] xp,output reg [1:0] zp,
    output reg [1:0] xf,output reg [1:0] zf
);
    wire [1:0] xn,zn,yn,wn;
    w33_qutrit_cx_frame_map m(xp,zp,xf,zf,xn,zn,yn,wn);
    always_ff @(posedge clk) begin
        if(rst) begin xp<=0;zp<=0;xf<=0;zf<=0; end
        else if(apply_cx) begin xp<=xn;zp<=zn;xf<=yn;zf<=wn; end
    end
endmodule

module w33_qutrit_cx_order3(
    input wire [1:0] xp,input wire [1:0] zp,
    input wire [1:0] xf,input wire [1:0] zf,
    output wire [1:0] xp3,output wire [1:0] zp3,
    output wire [1:0] xf3,output wire [1:0] zf3
);
    wire [1:0] x1,z1,y1,w1,x2,z2,y2,w2;
    w33_qutrit_cx_frame_map m1(xp,zp,xf,zf,x1,z1,y1,w1);
    w33_qutrit_cx_frame_map m2(x1,z1,y1,w1,x2,z2,y2,w2);
    w33_qutrit_cx_frame_map m3(x2,z2,y2,w2,xp3,zp3,xf3,zf3);
endmodule
