// Recursive single-photon qutrit time-bin bookkeeping; NO optical memory.
// Every accepted REUSE operation advances reuse_round_mod3 and path-controlled
// timebin label t <- t+path mod3. A FRESH op increments the count of new
// orthogonal time factors REQUIRED; it DOES NOT create those factors.
// Ready/valid backpressure keeps all metadata stable.
module w33_single_photon_timebin_recursion_guard (
 input logic clk, rst_n,
 input logic cmd_valid,
 output logic cmd_ready,
 input logic [1:0] cmd_path,
 input logic cmd_fresh,
 input logic cmd_clear,
 output logic out_valid,
 input logic out_ready,
 output logic [1:0] out_time_bin,
 output logic [1:0] out_reuse_round_mod3,
 output logic [7:0] out_fresh_registers_obligated,
 output logic out_fresh_storage_unimplemented,
 output logic out_returned_after_three_reuses,
 output logic out_invalid_path
);
 logic [1:0] state_t,state_round;
 logic [7:0] state_fresh;
 logic [1:0] base_t,base_round;
 logic [7:0] base_fresh;
 logic [1:0] next_t,next_round;
 logic [7:0] next_fresh;
 logic invalid_path;
 function automatic [1:0] add3(input logic [1:0] x,input logic [1:0] y);
   logic [2:0] s;
   begin
     s={1'b0,x}+{1'b0,y};
     if(s>=3) s=s-3;
     add3=s[1:0];
   end
 endfunction
 always_comb begin
   cmd_ready=!out_valid || out_ready;
   base_t=cmd_clear?2'd0:state_t;
   base_round=cmd_clear?2'd0:state_round;
   base_fresh=cmd_clear?8'd0:state_fresh;
   invalid_path=(cmd_path==2'd3);
   next_t=base_t;
   next_round=base_round;
   next_fresh=base_fresh;
   if(!invalid_path)begin
     if(cmd_fresh)next_fresh=base_fresh+8'd1;
     else begin
       next_round=add3(base_round,2'd1);
       next_t=add3(base_t,cmd_path);
     end
   end
 end
 always_ff @(posedge clk or negedge rst_n)begin
   if(!rst_n)begin
     state_t<=0;state_round<=0;state_fresh<=0;
     out_valid<=0;out_time_bin<=0;out_reuse_round_mod3<=0;
     out_fresh_registers_obligated<=0;
     out_fresh_storage_unimplemented<=0;
     out_returned_after_three_reuses<=0;out_invalid_path<=0;
   end else if(cmd_ready)begin
     out_valid<=cmd_valid;
     if(cmd_valid)begin
       state_t<=next_t;
       state_round<=next_round;
       state_fresh<=next_fresh;
       out_time_bin<=next_t;
       out_reuse_round_mod3<=next_round;
       out_fresh_registers_obligated<=next_fresh;
       out_fresh_storage_unimplemented<=cmd_fresh && !invalid_path;
       out_returned_after_three_reuses<=!cmd_fresh && !invalid_path && next_round==0;
       out_invalid_path<=invalid_path;
     end
   end
 end
endmodule
