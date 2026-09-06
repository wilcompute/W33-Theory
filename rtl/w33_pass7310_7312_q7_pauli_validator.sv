`default_nettype none

// Passes 7310-7312: proof-carrying validator for the 33-point q=7 certificate.
// Coordinates are four GF(7) elements packed in 12 bits, three bits each.
// The sole geometric output is x^T J y != 0.  This finite Weyl-Heisenberg
// commutation test is not state preparation, quantum dynamics, or a device.

module w33_pass7310_pauli_pair_q7_naive (
    input  wire [11:0] x,
    input  wire [11:0] y,
    output wire        inputs_valid,
    output wire        noncommute
);
    wire [2:0] x0=x[2:0], x1=x[5:3], x2=x[8:6], x3=x[11:9];
    wire [2:0] y0=y[2:0], y1=y[5:3], y2=y[8:6], y3=y[11:9];
    wire [5:0] p01=x0*y1, p10=x1*y0, p23=x2*y3, p32=x3*y2;
    // Add 98 before subtraction: nonnegative and unchanged modulo seven.
    wire [7:0] raw = {2'b0,p01} + {2'b0,p23} + 8'd98
                   - {2'b0,p10} - {2'b0,p32};
    wire [2:0] sigma = raw % 7;
    assign inputs_valid = (|x) && (|y) &&
                          x0<7 && x1<7 && x2<7 && x3<7 &&
                          y0<7 && y1<7 && y2<7 && y3<7;
    assign noncommute = inputs_valid && (sigma != 0);
endmodule

// Seven is Mersenne: 2^3 = 1 mod 7.  A six-bit product reduces by adding
// its low and high three-bit chunks, followed by at most one subtraction.
module w33_pass7310_gf7_add(input wire [2:0] a,b, output wire [2:0] y);
    wire [3:0] s=a+b;
    assign y=(s>=7)?s-7:s[2:0];
endmodule

module w33_pass7310_gf7_neg(input wire [2:0] a, output wire [2:0] y);
    assign y=(a==0)?0:7-a;
endmodule

module w33_pass7310_gf7_mul(input wire [2:0] a,b, output wire [2:0] y);
    wire [5:0] p=a*b;
    wire [3:0] folded={1'b0,p[2:0]}+{1'b0,p[5:3]};
    assign y=(folded>=7)?folded-7:folded[2:0];
endmodule

module w33_pass7310_pauli_pair_q7 (
    input  wire [11:0] x,
    input  wire [11:0] y,
    output wire        inputs_valid,
    output wire        noncommute
);
    wire [2:0] x0=x[2:0], x1=x[5:3], x2=x[8:6], x3=x[11:9];
    wire [2:0] y0=y[2:0], y1=y[5:3], y2=y[8:6], y3=y[11:9];
    wire [2:0] p01,p10,p23,p32,n10,n32,s0,s1,sigma;
    w33_pass7310_gf7_mul m0(.a(x0),.b(y1),.y(p01));
    w33_pass7310_gf7_mul m1(.a(x1),.b(y0),.y(p10));
    w33_pass7310_gf7_mul m2(.a(x2),.b(y3),.y(p23));
    w33_pass7310_gf7_mul m3(.a(x3),.b(y2),.y(p32));
    w33_pass7310_gf7_neg n0(.a(p10),.y(n10));
    w33_pass7310_gf7_neg n1(.a(p32),.y(n32));
    w33_pass7310_gf7_add a0(.a(p01),.b(n10),.y(s0));
    w33_pass7310_gf7_add a1(.a(p23),.b(n32),.y(s1));
    w33_pass7310_gf7_add a2(.a(s0),.b(s1),.y(sigma));
    assign inputs_valid = (|x) && (|y) &&
                          x0<7 && x1<7 && x2<7 && x3<7 &&
                          y0<7 && y1<7 && y2<7 && y3<7;
    assign noncommute = inputs_valid && (sigma != 0);
endmodule

// One-cycle, all-528-pair reference.  It is deliberately retained as the
// latency endpoint of the measured area/latency frontier, not as a target fit.
module w33_pass7311_q7_parallel #(
    parameter integer N = 33
) (
    input  wire [12*N-1:0] points_flat,
    output wire             valid
);
    wire [N-1:0] point_valid;
    wire [N*N-1:0] pair_good;
    genvar i,j;
    generate
      for (i=0;i<N;i=i+1) begin : POINTS
        wire [11:0] p=points_flat[12*i +: 12];
        wire [2:0] p0=p[2:0],p1=p[5:3],p2=p[8:6],p3=p[11:9];
        assign point_valid[i]=(|p)&&p0<7&&p1<7&&p2<7&&p3<7;
      end
      for (i=0;i<N;i=i+1) begin : ROWS
        for (j=0;j<N;j=j+1) begin : COLS
          if (j<=i) begin
            assign pair_good[N*i+j]=1'b1;
          end else begin
            wire unused_valid;
            w33_pass7310_pauli_pair_q7 u_pair(
              .x(points_flat[12*i +: 12]),.y(points_flat[12*j +: 12]),
              .inputs_valid(unused_valid),.noncommute(pair_good[N*i+j]));
          end
        end
      end
    endgenerate
    assign valid=(&point_valid)&&(&pair_good);
endmodule

// One pair per cycle after loading: 33 load + 528 check + 1 done = 562 cycles.
module w33_pass7311_q7_serial #(
    parameter integer N=33,
    parameter integer IW=6
) (
    input wire clk,rst,in_valid,
    input wire [11:0] point_in,
    output wire in_ready,
    output reg done,accept,
    output reg [9:0] pairs_checked
);
    localparam [1:0] S_LOAD=0,S_CHECK=1,S_DONE=2;
    reg [1:0] state;
    reg [IW-1:0] load_count,i,j;
    reg bad;
    reg [11:0] mem[0:N-1];
    wire pair_inputs_valid,pair_noncommute;
    w33_pass7310_pauli_pair_q7 u_pair(.x(mem[i]),.y(mem[j]),
      .inputs_valid(pair_inputs_valid),.noncommute(pair_noncommute));
    assign in_ready=(state==S_LOAD);
    integer k;
    always @(posedge clk) begin
      if(rst) begin
        state<=S_LOAD;load_count<=0;i<=0;j<=1;bad<=0;done<=0;accept<=0;
        pairs_checked<=0;
        for(k=0;k<N;k=k+1)mem[k]<=0;
      end else begin
        done<=0;
        case(state)
          S_LOAD: if(in_valid) begin
            mem[load_count]<=point_in;
            if(load_count==N-1) begin
              state<=S_CHECK;i<=0;j<=1;bad<=0;pairs_checked<=0;
            end else load_count<=load_count+1'b1;
          end
          S_CHECK: begin
            pairs_checked<=pairs_checked+1'b1;
            if(!pair_inputs_valid||!pair_noncommute)bad<=1;
            if(i==N-2&&j==N-1) begin
              accept<=!(bad||!pair_inputs_valid||!pair_noncommute);state<=S_DONE;
            end else if(j==N-1) begin i<=i+1'b1;j<=i+2'd2;
            end else j<=j+1'b1;
          end
          S_DONE: begin done<=1;state<=S_LOAD;load_count<=0;end
          default: state<=S_LOAD;
        endcase
      end
    end
endmodule

// One synchronous RAM read per cycle: three cycles per pair.  Yosys maps the
// 396-bit payload to one SB_RAM40_4K instead of 396 point-storage flip-flops.
// Latency is 33 load + 3*528 check + 1 done = 1618 cycles.
module w33_pass7311_q7_bram #(
    parameter integer N=33,
    parameter integer IW=6
) (
    input wire clk,rst,in_valid,
    input wire [11:0] point_in,
    output wire in_ready,
    output reg done,accept,
    output reg [9:0] pairs_checked
);
    localparam [2:0] S_LOAD=0,S_READ_X=1,S_READ_Y=2,S_EVAL=3,S_DONE=4;
    reg [2:0] state;
    reg [IW-1:0] load_count,i,j;
    reg [11:0] mem[0:N-1];
    reg [11:0] read_data,x_reg;
    reg bad;
    wire pair_inputs_valid,pair_noncommute;
    w33_pass7310_pauli_pair_q7 u_pair(.x(x_reg),.y(read_data),
      .inputs_valid(pair_inputs_valid),.noncommute(pair_noncommute));
    assign in_ready=(state==S_LOAD);
    always @(posedge clk) begin
      done<=0;
      if(state==S_LOAD&&in_valid)mem[load_count]<=point_in;
      if(state==S_READ_X||state==S_READ_Y)
        read_data<=mem[(state==S_READ_X)?i:j];
      if(rst) begin
        state<=S_LOAD;load_count<=0;i<=0;j<=1;bad<=0;done<=0;accept<=0;
        pairs_checked<=0;x_reg<=0;
      end else case(state)
        S_LOAD: if(in_valid) begin
          if(load_count==N-1) begin
            state<=S_READ_X;i<=0;j<=1;bad<=0;pairs_checked<=0;
          end else load_count<=load_count+1'b1;
        end
        S_READ_X: state<=S_READ_Y;
        S_READ_Y: begin x_reg<=read_data;state<=S_EVAL;end
        S_EVAL: begin
          pairs_checked<=pairs_checked+1'b1;
          if(!pair_inputs_valid||!pair_noncommute)bad<=1;
          if(i==N-2&&j==N-1) begin
            accept<=!(bad||!pair_inputs_valid||!pair_noncommute);state<=S_DONE;
          end else begin
            if(j==N-1) begin i<=i+1'b1;j<=i+2'd2;end else j<=j+1'b1;
            state<=S_READ_X;
          end
        end
        S_DONE: begin done<=1;state<=S_LOAD;load_count<=0;end
        default: state<=S_LOAD;
      endcase
    end
endmodule

`default_nettype wire
