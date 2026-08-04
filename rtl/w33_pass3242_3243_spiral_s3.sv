`default_nettype none

module w33_pass3242_real_spiral_controller #(
    parameter integer W = 16
) (
    input  wire signed [W-1:0] x0,
    input  wire signed [W-1:0] x1,
    input  wire signed [W-1:0] y0,
    input  wire signed [W-1:0] y1,
    input  wire                 step,
    input  wire                 reflect,
    output reg  signed [W-1:0]  nx0,
    output reg  signed [W-1:0]  nx1,
    output reg  signed [W-1:0]  ny0,
    output reg  signed [W-1:0]  ny1
);
    always @* begin
        nx0=x0; nx1=x1; ny0=y0; ny1=y1;
        if (reflect) begin
            nx0=x1; nx1=x0; ny0=y1; ny1=y0;
        end else if (step) begin
            // R = [[0,-1,-1,0],[1,0,0,0],[1,0,0,-1],[0,0,1,0]]
            nx0=-x1-y0;
            nx1=x0;
            ny0=x0-y1;
            ny1=y0;
        end
    end
endmodule

module w33_pass3243_s3_matching (
    input  wire [2:0] selector,
    input  wire [3:0] state_in, // state_in[k] is coordinate k over F2
    output reg  [3:0] state_out,
    output reg        valid
);
    wire v0=state_in[0], v1=state_in[1], v2=state_in[2], v3=state_in[3];
    always @* begin
        valid=1'b1;
        case (selector)
          3'd0: begin // r0: identity
            state_out[0]=v0; state_out[1]=v1; state_out[2]=v2; state_out[3]=v3;
          end
          3'd1: begin // r1
            state_out[0]=v3; state_out[1]=v1^v2; state_out[2]=v1; state_out[3]=v0^v3;
          end
          3'd2: begin // r2
            state_out[0]=v0^v3; state_out[1]=v2; state_out[2]=v1^v2; state_out[3]=v0;
          end
          3'd3: begin // s
            state_out[0]=v1; state_out[1]=v0; state_out[2]=v3; state_out[3]=v2;
          end
          3'd4: begin // sr
            state_out[0]=v1^v2; state_out[1]=v3; state_out[2]=v0^v3; state_out[3]=v1;
          end
          3'd5: begin // sr^2
            state_out[0]=v2; state_out[1]=v0^v3; state_out[2]=v0; state_out[3]=v1^v2;
          end
          default: begin
            state_out=4'b0000; valid=1'b0;
          end
        endcase
    end
endmodule

`default_nettype wire
