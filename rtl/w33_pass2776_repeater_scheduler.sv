// Pass 2776: fail-closed nested qutrit repeater scheduler.
module w33_pass2776_repeater_scheduler #(parameter integer MAX_SEGMENTS=64,parameter integer TIMEOUT_CYCLES=32'h00ff_ffff)(
 input logic clk,rst,start,input logic [7:0] segment_count,input logic [2:0] elementary_purify_rounds,swap_purify_rounds,
 input logic [31:0] cycle_counter,input logic [MAX_SEGMENTS-1:0] elementary_valid,input logic purify_accept,purify_done,swap_done,final_fidelity_ok,
 output logic busy,done,erasure,timeout_fault,protocol_fault,request_elementary,request_purify,request_swap,pair_ready,
 output logic [7:0] active_pairs,output logic [3:0] nesting_level,output logic [2:0] round_index);
 typedef enum logic[2:0]{IDLE,WAIT_LINKS,PURIFY_ELEM,SWAP,PURIFY_SWAP,VERIFY}state_t;state_t state;logic[31:0]deadline;logic[7:0]next_pairs;
 function automatic logic is_power_of_two(input logic[7:0]x);is_power_of_two=(x!=0)&&((x&(x-1'b1))==0);endfunction
 always_ff @(posedge clk)begin
  if(rst)begin state<=IDLE;busy<=0;done<=0;erasure<=0;timeout_fault<=0;protocol_fault<=0;request_elementary<=0;request_purify<=0;request_swap<=0;pair_ready<=0;active_pairs<=0;nesting_level<=0;round_index<=0;deadline<=0;next_pairs<=0;end
  else begin done<=0;
   if(busy&&cycle_counter>=deadline)begin timeout_fault<=1;erasure<=1;busy<=0;done<=1;request_elementary<=0;request_purify<=0;request_swap<=0;pair_ready<=0;state<=IDLE;end
   else case(state)
    IDLE:if(start)begin erasure<=0;timeout_fault<=0;protocol_fault<=0;pair_ready<=0;if(!is_power_of_two(segment_count)||segment_count>MAX_SEGMENTS)begin protocol_fault<=1;done<=1;end else begin busy<=1;active_pairs<=segment_count;nesting_level<=0;round_index<=0;request_elementary<=1;deadline<=cycle_counter+TIMEOUT_CYCLES;state<=WAIT_LINKS;end end
    WAIT_LINKS:if(&elementary_valid[segment_count-1:0])begin request_elementary<=0;round_index<=0;if(elementary_purify_rounds!=0)begin request_purify<=1;state<=PURIFY_ELEM;end else if(active_pairs==1)state<=VERIFY;else begin request_swap<=1;next_pairs<=active_pairs>>1;state<=SWAP;end end
    PURIFY_ELEM:if(purify_done)begin request_purify<=0;if(!purify_accept)begin erasure<=1;busy<=0;done<=1;state<=IDLE;end else if(round_index+1<elementary_purify_rounds)begin round_index<=round_index+1;request_purify<=1;end else if(active_pairs==1)state<=VERIFY;else begin round_index<=0;request_swap<=1;next_pairs<=active_pairs>>1;state<=SWAP;end end
    SWAP:if(swap_done)begin request_swap<=0;active_pairs<=next_pairs;nesting_level<=nesting_level+1;if(swap_purify_rounds!=0)begin round_index<=0;request_purify<=1;state<=PURIFY_SWAP;end else if(next_pairs==1)state<=VERIFY;else begin request_swap<=1;next_pairs<=next_pairs>>1;state<=SWAP;end end
    PURIFY_SWAP:if(purify_done)begin request_purify<=0;if(!purify_accept)begin erasure<=1;busy<=0;done<=1;state<=IDLE;end else if(round_index+1<swap_purify_rounds)begin round_index<=round_index+1;request_purify<=1;end else if(active_pairs==1)state<=VERIFY;else begin round_index<=0;request_swap<=1;next_pairs<=active_pairs>>1;state<=SWAP;end end
    VERIFY:begin busy<=0;done<=1;pair_ready<=final_fidelity_ok;erasure<=!final_fidelity_ok;state<=IDLE;end
    default:begin protocol_fault<=1;erasure<=1;busy<=0;done<=1;state<=IDLE;end
   endcase
  end
 end
endmodule
