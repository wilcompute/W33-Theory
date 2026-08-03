#!/usr/bin/env python3
"""Algebraic verification of the retired Pass-2206 mixer arithmetic."""
from __future__ import annotations
import argparse,hashlib,json,random,re
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];RTL=ROOT/'rtl/w33_pass2773_spread_mixer36_synth.sv';CERT=ROOT/'data/w33_pass2206_rtl_reference.json'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build(path):
 text=path.read_text();vals=[int(x,16) for x in re.findall(r"36'h([0-9a-fA-F]{9})",text)];assert len(vals)==36;vals=list(reversed(vals))
 A=np.zeros((36,36),dtype=np.int64)
 for i,m in enumerate(vals):
  for j in range(36):A[i,j]=(m>>j)&1
 I=np.eye(36,dtype=np.int64);J=np.ones((36,36),dtype=np.int64)
 assert np.array_equal(A,A.T) and np.all(np.diag(A)==0) and set(map(int,A.sum(1)))=={15};assert np.array_equal(A@A,9*I+6*J);assert sorted((round(float(x)) for x in np.linalg.eigvalsh(A)),reverse=True)==[15]+[3]*15+[-3]*20
 rng=random.Random(2206);W=16;lo=-(1<<(W-1));hi=(1<<(W-1))-1;vectors=[]
 for i in range(36):
  v=[0]*36;v[i]=hi;vectors.append(v);v=[0]*36;v[i]=lo;vectors.append(v)
 vectors += [[rng.randint(lo,hi) for _ in range(36)] for _ in range(256)];mx=0
 for v in vectors:
  z=np.array(v,dtype=np.int64);y=A@z;mx=max(mx,max(map(abs,map(int,y))));assert np.array_equal(A@y,9*z+6*sum(v)*np.ones(36,dtype=np.int64));assert np.all(y>=-(1<<(W+3))) and np.all(y<(1<<(W+3)))
 phases={(3*a+2*b)%12 for a in range(4) for b in range(6)};ker=[(a,b) for a in range(4) for b in range(6) if (3*a+2*b)%12==0];assert phases==set(range(12)) and ker==[(0,0),(2,3)]
 checks={'36_masks_parsed_from_synthesizable_source':True,'symmetric_zero_diagonal':True,'degree_15':True,'A2_equals_9I_plus_6J':True,'spectrum_15_3_minus3':True,'signed_W_plus_4_bound':True,'two_hop_datapath_identity':True,'phase_image_C12':True,'phase_kernel_C2':True}
 out={'schema':'w33.pass2807.rtl_reference.v2','status':'PASS_SYNTHESIZABLE_RTL_REFERENCE','source':'rtl/w33_pass2773_spread_mixer36_synth.sv','retired_source':'rtl/w33_spread_mixer36.sv','mixer':{'lanes':36,'degree':15,'identity':'A^2=9I+6J','spectrum':{'15':1,'3':15,'-3':20},'input_width':W,'output_width':W+4,'maximum_tested_absolute_sum':mx},'phase_controller':{'rotation_states':12,'dihedral_image_order':24,'kernel':ker},'checks':checks,'boundaries':['The Python verifier checks literal masks and arithmetic semantics.','Synthesis, placement, timing, and power remain toolchain evidence.']};out['sha256_without_hash_field']=digest(out);return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rtl',type=Path,default=RTL);ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();out=build(a.rtl)
 if a.verify_frozen:assert json.loads(CERT.read_text())==out
 if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
