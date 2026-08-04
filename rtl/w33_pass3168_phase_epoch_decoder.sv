// Pass 3168: optimal phase-coded epoch decoder.
// Phase p is five repeats of payload-unused symbol U[p].  The detector scans every suffix
// length 3..7; for constant u^5, d_L=max(5,n)-min(5,count_u).  Radius-two balls are
// pairwise disjoint, so at most one phase can qualify.
module w33_pass3168_phase_epoch_decoder(
  input logic clk,input logic rst,input logic symbol_valid_i,input logic [4:0] symbol_i,
  output logic marker_seen_o,output logic phase_valid_o,output logic [3:0] phase_o,
  output logic ambiguous_o,output logic [15:0] epoch_count_o
);
  function automatic [4:0] phase_symbol(input [3:0] p);
    begin case(p)
      0:phase_symbol=5'd1;1:phase_symbol=5'd3;2:phase_symbol=5'd4;3:phase_symbol=5'd5;
      4:phase_symbol=5'd6;5:phase_symbol=5'd8;6:phase_symbol=5'd9;7:phase_symbol=5'd10;
      8:phase_symbol=5'd12;9:phase_symbol=5'd13;10:phase_symbol=5'd14;default:phase_symbol=5'd17;
    endcase end
  endfunction
  logic [4:0] hist[0:6],scan[0:6];logic [3:0] count,scan_count;
  logic [11:0] candidate_mask;logic [11:0] hit_mask;integer p,n,j,cu,dist,candidate_count;logic [3:0] chosen;
  always_comb begin
    scan[0]=symbol_i;for(j=1;j<7;j=j+1)scan[j]=hist[j-1];
    scan_count=(count<7)?count+1'b1:count;
    candidate_mask='0;hit_mask='0;candidate_count=0;chosen=0;
    if(symbol_valid_i)for(p=0;p<12;p=p+1)begin
      for(n=3;n<=7;n=n+1)if(scan_count>=n)begin
        cu=0;for(j=0;j<n;j=j+1)if(scan[j]==phase_symbol(p[3:0]))cu=cu+1;
        dist=((n>5)?n:5)-((cu>5)?5:cu);
        if(dist<=2)hit_mask[p]=1'b1;
      end
      if(hit_mask[p])begin candidate_mask[p]=1'b1;candidate_count=candidate_count+1;chosen=p[3:0];end
    end
    phase_valid_o=(candidate_count==1);ambiguous_o=(candidate_count>1);
  end
  always_ff @(posedge clk) begin
    if(rst)begin count<=0;marker_seen_o<=0;phase_o<=0;epoch_count_o<=0;for(j=0;j<7;j=j+1)hist[j]<=0;end
    else begin
      marker_seen_o<=0;
      if(symbol_valid_i)begin
        if(phase_valid_o)begin marker_seen_o<=1;phase_o<=chosen;epoch_count_o<=epoch_count_o+1'b1;count<=0;end
        else begin for(j=0;j<7;j=j+1)hist[j]<=scan[j];count<=scan_count;end
      end
    end
  end
endmodule
