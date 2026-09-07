module tb_w33_pass3005_golden_a4_shell;
logic clk=0,reset,enable,core_authorized;logic[2:0]opcode;logic[1:0]shell_translation;
logic[1:0]shell_v,shell_k,core_r;logic core_s,expensive_slot,illegal_cross_domain;
w33_pass3005_golden_a4_shell dut(.*);always #1 clk=~clk;
task step(input[2:0]op,input[1:0]tr,input auth);opcode=op;shell_translation=tr;core_authorized=auth;enable=1;@(posedge clk);#0;endtask
integer i,pulses;logic prev;
initial begin
 reset=1;enable=0;opcode=0;shell_translation=0;core_authorized=0;@(posedge clk);reset=0;
 step(1,2'b11,0);if(shell_v!==2'b11||core_r!==0||core_s!==0)$fatal;
 step(2,0,0);step(2,0,0);step(2,0,0);if(shell_v!==2'b11||shell_k!==0)$fatal;
 step(5,0,0);if(core_r!==0||!illegal_cross_domain)$fatal;
 repeat(4)step(5,0,1);if(core_r!==0)$fatal;
 step(6,0,1);step(6,0,1);if(core_r!==0||core_s!==0)$fatal;
 reset=1;@(posedge clk);reset=0;pulses=0;prev=0;
 for(i=0;i<233;i=i+1)begin #0;if(expensive_slot)begin pulses=pulses+1;if(prev)$fatal;end prev=expensive_slot;step(0,0,0);end
 if(pulses!=89)$fatal;$display("PASS A4 shell, D4 barrier, and 89/233 scheduler");$finish;
end
endmodule
