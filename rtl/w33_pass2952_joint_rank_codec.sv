// Pass 2952: reversible logical rank for 81 frame states x 40 route addresses.
module w33_pass2952_joint_rank_encode(
 input logic [6:0] frame_rank,
 input logic [3:0] oam_line,
 input logic [1:0] slot,
 output logic valid,
 output logic [11:0] joint_rank
);
logic [5:0] address;logic [12:0] wide;
always_comb begin
 address={oam_line,slot};
 valid=(frame_rank<7'd81)&&(oam_line<4'd10);
 wide=({6'b0,frame_rank}<<5)+({6'b0,frame_rank}<<3)+address;
 joint_rank=valid?wide[11:0]:12'hfff;
end
endmodule

module w33_pass2952_joint_rank_decode(
 input logic [11:0] joint_rank,
 output logic valid,
 output logic [6:0] frame_rank,
 output logic [3:0] oam_line,
 output logic [1:0] slot
);
logic [5:0] address;
always_comb begin
 valid=(joint_rank<12'd3240);
 frame_rank=valid?(joint_rank/12'd40):7'h7f;
 address=valid?(joint_rank%12'd40):6'h3f;
 oam_line=address[5:2];slot=address[1:0];
end
endmodule
