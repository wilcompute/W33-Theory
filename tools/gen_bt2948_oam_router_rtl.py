#!/usr/bin/env python3
"""Generate source-complete spread-router RTL and exhaustive inverse testbench."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'data/PART_BT2948_OAM_SPREAD_FABRIC_results.json').read_text());M=r['directed_matchings']
lines=['// Pass 2948: exact W33 spread router. Ten OAM modes x four time/frequency slots.','module w33_pass2948_spread_router(input logic [3:0] src_line,dst_line,input logic [1:0] src_slot,output logic valid,output logic [1:0] dst_slot);',"always_comb begin valid=1'b1; dst_slot=2'b00; unique case ({src_line,dst_line})"]
for key,p in M.items():
 i,j=map(int,key.split('-'));items=' '.join(f"2'd{s}: dst_slot=2'd{o};" for s,o in enumerate(p));lines.append(f"  8'h{i:x}{j:x}: case(src_slot) {items} default: begin valid=0;dst_slot=0;end endcase")
lines += ["  default: begin valid=1'b0;dst_slot=2'b00;end","endcase end endmodule",'']
(ROOT/'rtl/w33_pass2948_spread_router.sv').write_text('\n'.join(lines))
tb='''`timescale 1ns/1ps
module tb_w33_pass2948_spread_router;
logic [3:0] s,d;logic [1:0] a,b,c;logic v,w;integer i,j,k;
w33_pass2948_spread_router f(.src_line(s),.dst_line(d),.src_slot(a),.valid(v),.dst_slot(b));
w33_pass2948_spread_router r(.src_line(d),.dst_line(s),.src_slot(b),.valid(w),.dst_slot(c));
initial begin for(i=0;i<10;i=i+1)for(j=0;j<10;j=j+1)for(k=0;k<4;k=k+1)begin s=i;d=j;a=k;#1;if(i==j)begin if(v)$fatal(1,"same line");end else begin if(!v||!w||c!==a)$fatal(1,"inverse %0d %0d %0d",i,j,k);end end $display("PASS 360 directed routes plus 40 same-line rejects");$finish;end endmodule
'''
(ROOT/'rtl/tb_w33_pass2948_spread_router.sv').write_text(tb)
print('generated 90 directed matching cases')
