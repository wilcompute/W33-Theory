// Passes 3169-3170: two-pass 48,826-hypothesis Bayesian stream.
// Factor reconstruction and exp/entropy LUTs are explicit interfaces; the controller owns
// ordering, max subtraction, normalization, 23x8 action bins, and final argmax scan.
module w33_pass3169_bayesian_stream #(
  parameter integer LOGW=32,parameter integer WEIGHT=32,parameter integer ACC=48
)(
  input logic clk,input logic rst,input logic start_i,
  output logic enum_start_o,output logic enum_advance_o,
  input logic enum_valid_i,input logic enum_done_i,input logic [15:0] hypothesis_index_i,
  output logic logweight_request_o,input logic logweight_valid_i,input logic signed [LOGW-1:0] logweight_i,
  input logic [68:0] outcomes_i, // 23 packed 3-bit D4 outcomes
  output logic exp_request_o,output logic signed [LOGW-1:0] exp_delta_o,
  input logic exp_valid_i,input logic [WEIGHT-1:0] exp_weight_i,
  output logic bins_valid_o,input logic [4:0] bin_action_i,input logic [2:0] bin_outcome_i,
  output logic [ACC-1:0] bin_value_o,output logic [ACC-1:0] normalizer_o,
  output logic signed [LOGW-1:0] max_logweight_o,output logic done_o,
  output logic [1:0] pass_o,output logic [16:0] accepted_hypotheses_o
);
  localparam logic signed [LOGW-1:0] MIN_LOGW = {1'b1,{(LOGW-1){1'b0}}};
  typedef enum logic [2:0] {IDLE,START_MAX,MAX_PASS,START_ACC,ACC_PASS,FINISH} st_t;
  st_t st;logic wait_logw,wait_exp;logic [68:0] pending_outcomes;
  logic [ACC-1:0] bins[0:183];integer i,a;logic [7:0] bindex;
  always_comb begin bindex={bin_action_i,bin_outcome_i};bin_value_o=bins[bindex];bins_valid_o=(st==FINISH);end
  always_ff @(posedge clk) begin
    enum_start_o<=0;enum_advance_o<=0;logweight_request_o<=0;exp_request_o<=0;done_o<=0;
    if(rst) begin st<=IDLE;wait_logw<=0;wait_exp<=0;max_logweight_o<=MIN_LOGW;
      normalizer_o<=0;pass_o<=0;accepted_hypotheses_o<=0;pending_outcomes<=0;
      for(i=0;i<184;i=i+1)bins[i]<=0;
    end else case(st)
      IDLE:if(start_i)begin st<=START_MAX;max_logweight_o<=MIN_LOGW;normalizer_o<=0;
        accepted_hypotheses_o<=0;for(i=0;i<184;i=i+1)bins[i]<=0;end
      START_MAX:begin enum_start_o<=1;pass_o<=1;st<=MAX_PASS;wait_logw<=0;end
      MAX_PASS:begin
        if(enum_valid_i&&!wait_logw)begin logweight_request_o<=1;wait_logw<=1;end
        if(logweight_valid_i&&wait_logw)begin if(logweight_i>max_logweight_o)max_logweight_o<=logweight_i;
          wait_logw<=0;enum_advance_o<=1;accepted_hypotheses_o<=accepted_hypotheses_o+1'b1;end
        if(enum_done_i&&!wait_logw)begin st<=START_ACC;accepted_hypotheses_o<=0;end
      end
      START_ACC:begin enum_start_o<=1;pass_o<=2;st<=ACC_PASS;wait_logw<=0;wait_exp<=0;end
      ACC_PASS:begin
        if(enum_valid_i&&!wait_logw&&!wait_exp)begin logweight_request_o<=1;wait_logw<=1;end
        if(logweight_valid_i&&wait_logw)begin exp_delta_o<=logweight_i-max_logweight_o;pending_outcomes<=outcomes_i;
          exp_request_o<=1;wait_logw<=0;wait_exp<=1;end
        if(exp_valid_i&&wait_exp)begin
          normalizer_o<=normalizer_o+exp_weight_i;
          for(a=0;a<23;a=a+1)bins[a*8+pending_outcomes[a*3 +: 3]]<=bins[a*8+pending_outcomes[a*3 +: 3]]+exp_weight_i;
          wait_exp<=0;enum_advance_o<=1;accepted_hypotheses_o<=accepted_hypotheses_o+1'b1;
        end
        if(enum_done_i&&!wait_logw&&!wait_exp)st<=FINISH;
      end
      FINISH:begin done_o<=1;if(start_i)st<=START_MAX;end
      default:st<=IDLE;
    endcase
  end
endmodule

// Serial 23x8 entropy scan.  The LUT supplies -p*log2(p) for each normalized bin.
module w33_pass3170_action_entropy_scan #(
  parameter integer TERM=32,parameter integer SCORE=40
)(
  input logic clk,input logic rst,input logic start_i,
  output logic [4:0] action_o,output logic [2:0] outcome_o,output logic term_request_o,
  input logic term_valid_i,input logic [TERM-1:0] entropy_term_i,
  output logic done_o,output logic [4:0] best_action_o,output logic [SCORE-1:0] best_score_o
);
  logic [SCORE-1:0] accum;logic waiting;logic [4:0] action;logic [2:0] outcome;
  always_comb begin action_o=action;outcome_o=outcome;end
  always_ff @(posedge clk) begin term_request_o<=0;done_o<=0;
    if(rst)begin action<=0;outcome<=0;accum<=0;waiting<=0;best_action_o<=0;best_score_o<=0;end
    else if(start_i)begin action<=0;outcome<=0;accum<=0;waiting<=0;best_action_o<=0;best_score_o<=0;end
    else begin
      if(!waiting)begin term_request_o<=1;waiting<=1;end
      if(waiting&&term_valid_i)begin
        waiting<=0;
        if(outcome==7)begin
          if(accum+entropy_term_i>best_score_o)begin best_score_o<=accum+entropy_term_i;best_action_o<=action;end
          accum<=0;outcome<=0;
          if(action==22)done_o<=1;else action<=action+1'b1;
        end else begin accum<=accum+entropy_term_i;outcome<=outcome+1'b1;end
      end
    end
  end
endmodule

// Low-pin digital placement wrapper.  The likelihood and outcome sources are deterministic
// internal stand-ins; this wrapper measures controller/enumerator/bin storage, not calibrated
// optical likelihood generation or numerical accuracy of a production exponential LUT.
module w33_pass3170_bayesian_place_wrapper(
  input logic clk,input logic rst,input logic start_i,input logic [7:0] seed_i,
  output logic done_o,output logic [7:0] normalizer_fold_o,output logic [1:0] pass_o
);
  logic enum_start,enum_advance,enum_valid,enum_done;
  logic [15:0] hidx;logic u1v,u2v,cv;logic [8:0]u1,u2;logic [11:0]ci;
  logic [5:0]e1,e2;logic [2:0]l1,l2;
  logic logreq,logvalid,expreq,expvalid,binsvalid;
  logic signed [31:0] logw,delta,maxlog;
  logic [31:0] expw;logic [68:0] outcomes;
  logic [47:0] binvalue,normalizer;logic [16:0] accepted;integer a;
  always_comb begin
    logvalid=logreq;logw=$signed({16'd0,hidx})-$signed({24'd0,seed_i});
    expvalid=expreq;expw=(delta<-32'sd65536)?32'd0:32'd1;
    for(a=0;a<23;a=a+1)outcomes[a*3 +: 3]=(hidx+a+seed_i)&3'h7;
    normalizer_fold_o=normalizer[7:0]^normalizer[15:8]^normalizer[23:16]^normalizer[31:24]
                      ^normalizer[39:32]^normalizer[47:40];
  end
  w33_pass3169_hypothesis_enumerator en(.clk,.rst,.start_i(enum_start),.advance_i(enum_advance),
    .valid_o(enum_valid),.done_o(enum_done),.hypothesis_index_o(hidx),
    .unary1_valid_o(u1v),.unary1_index_o(u1),.unary2_valid_o(u2v),.unary2_index_o(u2),
    .correction_valid_o(cv),.correction_index_o(ci),.edge1_o(e1),.label1_o(l1),.edge2_o(e2),.label2_o(l2));
  w33_pass3169_bayesian_stream stream(.clk,.rst,.start_i,
    .enum_start_o(enum_start),.enum_advance_o(enum_advance),.enum_valid_i(enum_valid),.enum_done_i(enum_done),
    .hypothesis_index_i(hidx),.logweight_request_o(logreq),.logweight_valid_i(logvalid),.logweight_i(logw),
    .outcomes_i(outcomes),.exp_request_o(expreq),.exp_delta_o(delta),.exp_valid_i(expvalid),.exp_weight_i(expw),
    .bins_valid_o(binsvalid),.bin_action_i(5'd0),.bin_outcome_i(3'd0),.bin_value_o(binvalue),
    .normalizer_o(normalizer),.max_logweight_o(maxlog),.done_o,.pass_o,.accepted_hypotheses_o(accepted));
endmodule
