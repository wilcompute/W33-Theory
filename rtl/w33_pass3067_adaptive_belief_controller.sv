module w33_pass3067_adaptive_belief_controller #(
 parameter SCORE_W=18, parameter TEST_W=7
)(
 input logic clk,rst_n,load_class,observation_valid,
 input logic [1:0] class_size,
 input logic signed [SCORE_W-1:0] prior0,prior1,prior2,stop_gap,ll0,ll1,ll2,
 input logic [TEST_W-1:0] first_test,second_test,
 output logic busy,request_valid,stop_valid,
 output logic [TEST_W-1:0] requested_test,
 output logic [1:0] decision,probes_used
);
 typedef enum logic[1:0]{IDLE,WAIT_OBS,EVAL} state_t; state_t state;
 logic[1:0] size_q; logic signed[SCORE_W-1:0] s0,s1,s2,threshold;
 logic[TEST_W-1:0] first_q,second_q;
 logic signed[SCORE_W-1:0] top,runner; logic[1:0] top_i;
 always_comb begin
  top=s0;top_i=0;runner=(size_q>1)?s1:{1'b1,{(SCORE_W-1){1'b0}}};
  if(size_q>1&&s1>top)begin runner=top;top=s1;top_i=1;end
  if(size_q>2)begin if(s2>top)begin runner=top;top=s2;top_i=2;end else if(s2>runner)runner=s2;end
 end
 always_ff @(posedge clk or negedge rst_n)begin
  if(!rst_n)begin state<=IDLE;size_q<=0;s0<=0;s1<=0;s2<=0;threshold<=0;first_q<=0;second_q<=0;request_valid<=0;requested_test<=0;stop_valid<=0;decision<=0;probes_used<=0;end
  else begin
   request_valid<=0;stop_valid<=0;
   case(state)
    IDLE:if(load_class)begin size_q<=class_size;s0<=prior0;s1<=prior1;s2<=prior2;threshold<=stop_gap;first_q<=first_test;second_q<=second_test;probes_used<=0;request_valid<=1;requested_test<=first_test;state<=WAIT_OBS;end
    WAIT_OBS:if(observation_valid)begin s0<=s0+ll0;s1<=s1+ll1;s2<=s2+ll2;probes_used<=probes_used+1'b1;state<=EVAL;end
    EVAL:if(top-runner>=threshold||probes_used>=2)begin stop_valid<=1;decision<=top_i;state<=IDLE;end else begin request_valid<=1;requested_test<=second_q;state<=WAIT_OBS;end
    default:state<=IDLE;
   endcase
  end
 end
 assign busy=(state!=IDLE);
endmodule
