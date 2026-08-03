#!/usr/bin/env python3
"""Pass 2949: extend the 81-word observer-to-rank map to a 256-state permutation."""
from __future__ import annotations
import itertools,collections,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2949_REVERSIBLE_TRANSCRIPT_results.json';RTL=ROOT/'rtl/w33_pass2949_reversible_transcript_permutation.sv';TB=ROOT/'rtl/tb_w33_pass2949_reversible_transcript_permutation.sv'
def cx(s):x,z,u,v=s;return (x,(z+2*v)%3,(x+u)%3,v)
def fp(s):x,z,u,v=s;return ((2*z)%3,x,u,v)
def zp(s):x,z,u,v=s;return (x,(z+1)%3,u,v)
ops=[cx,fp,zp,fp,zp,cx];coords=[(0,0),(0,1),(0,2),(1,1),(3,1),(5,1),(6,1),(6,2)]
def obs(s):
 tr=[s]
 for op in ops:tr.append(op(tr[-1]))
 return sum(int(tr[t][c]!=0)<<i for i,(t,c) in enumerate(coords))
def rank(s):return 27*s[0]+9*s[1]+3*s[2]+s[3]
def build():
 valid={obs(s):rank(s) for s in itertools.product(range(3),repeat=4)};assert len(valid)==81 and set(valid.values())==set(range(81));invalid_in=sorted(set(range(256))-set(valid));P=[None]*256
 for i,o in valid.items():P[i]=o
 for i,o in zip(invalid_in,range(81,256)):P[i]=o
 assert sorted(P)==list(range(256));Pinv=[0]*256
 for i,o in enumerate(P):Pinv[o]=i
 seen=set();cycles=[]
 for i in range(256):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=P[j]
  cycles.append(c)
 hist=collections.Counter(map(len,cycles));trans=sum(len(c)-1 for c in cycles);codes=list(valid);bitp=[sum((c>>i)&1 for c in codes)/81 for i in range(8)]
 def hb(p):return 0 if p in (0,1) else -(p*math.log2(p)+(1-p)*math.log2(1-p))
 marginal=sum(hb(p) for p in bitp)
 return {'schema':'w33.pass2949.reversible_transcript.v1','status':'COMPLETE_EXACT_SOURCE_RTL','valid_codewords':81,'permutation_size':256,'cycle_length_histogram':{str(k):v for k,v in sorted(hist.items())},'cycle_count':len(cycles),'transposition_floor':trans,'permutation_parity':'even' if trans%2==0 else 'odd','valid_output_range':[0,80],'invalid_output_range':[81,255],'known_zero_high_bit_on_valid_inputs':all(P[c]<128 for c in valid),'observer_joint_entropy_bits':math.log2(81),'observer_marginal_entropy_sum_bits':marginal,'reversible_correlation_compression_bits':marginal-math.log2(81),'eventual_rank_erasure_floor_bits':math.log2(81),'forward':P,'inverse':Pinv,'valid_map':{str(k):v for k,v in sorted(valid.items())},'claim_boundary':'The 256-state permutation and inverse are exact logical maps. Energy and area require a physical reversible implementation and observed synthesis.'}
def emit(name,arr):
 lines=[f'module {name}(input logic [7:0] in_byte, output logic [7:0] out_byte);','always_comb begin','  unique case (in_byte)']
 for i,o in enumerate(arr):lines.append(f"    8'h{i:02x}: out_byte = 8'h{o:02x};")
 return '\n'.join(lines+["    default: out_byte = 8'hxx;",'  endcase','end','endmodule',''])
def main():
 r=build();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');RTL.write_text('// Pass 2949: reversible observer-byte/rank permutation.\n'+emit('w33_pass2949_transcript_compress',r['forward'])+emit('w33_pass2949_transcript_expand',r['inverse']))
 TB.write_text('''`timescale 1ns/1ps
module tb_w33_pass2949_reversible_transcript_permutation;
logic [7:0] x,y,z;integer i;w33_pass2949_transcript_compress c(.in_byte(x),.out_byte(y));w33_pass2949_transcript_expand e(.in_byte(y),.out_byte(z));
initial begin for(i=0;i<256;i=i+1)begin x=i;#1;if(z!==x)$fatal(1,"inverse %0d",i);end $display("PASS 256/256 reversible transcript states");$finish;end endmodule
''');print('PASS 256/256',r['cycle_length_histogram'])
if __name__=='__main__':main()
