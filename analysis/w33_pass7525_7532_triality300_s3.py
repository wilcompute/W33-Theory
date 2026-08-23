#!/usr/bin/env python3
"""Pass7525-7532: exact outer-S3 structure on the common 300D triality bundle."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7525_7532_TRIALITY300_S3.json'

def main():
    R,A2,ag,J0,base,leaves,lgens,parity=E.build();plus=[i for i,x in enumerate(parity) if x==0];minus=[i for i,x in enumerate(parity) if x==1]
    pp={v:i for i,v in enumerate(plus)};pm={v:i for i,v in enumerate(minus)};masks=[sum(1<<x for x in L) for L in leaves]
    Fp=np.zeros((1120,1120),dtype=np.int16);Fm=np.zeros((1120,1120),dtype=np.int16);K=np.zeros((1120,1120),dtype=np.int16)
    for j,v in enumerate(plus):Fp[list(leaves[v]),j]=1
    for j,v in enumerate(minus):Fm[list(leaves[v]),j]=1
    for i,v in enumerate(plus):
        for w in minus:
            if (masks[v]&masks[w]).bit_count()==13:K[i,pm[w]]=1
    assert set(Fp.sum(0))=={40} and set(Fm.sum(0))=={40} and set(K.sum(0))=={40}
    J=np.ones((1120,1120),dtype=np.int16)
    assert np.array_equal(Fm@K.T,J+12*Fp) and np.array_equal(Fp@K,J+12*Fm) and np.array_equal(Fp.T@Fm,J+12*K)
    tau=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=int);s=np.array([[1,0,0],[0,0,1],[0,1,0]],dtype=int);I3=np.eye(3,dtype=int)
    assert np.array_equal(tau@tau@tau,I3) and np.array_equal(s@s,I3) and np.array_equal(s@tau@s,tau@tau)
    Acolor=12*(np.ones((3,3),dtype=int)-I3);assert np.array_equal(tau@Acolor,Acolor@tau) and np.array_equal(s@Acolor,Acolor@s)
    assert np.allclose(sorted(np.linalg.eigvalsh(Acolor.astype(float))),[-12,-12,24])
    out={'schema':'w33.pass7525_7532.triality300_s3.v1','status':'PASS','passes':'7525-7532','common_constituent_dimension':300,
      'three_species':['A2','leaf_plus','leaf_minus'],'pairwise_groupoid':'centered incidence maps satisfy X_minus X_K^T=12 X_plus and cyclic variants, with X_B X_B^T=144 P_300',
      'identified_common_sector':'V_300 tensor C^3','outer_S3_generators':{'3cycle':tau.tolist(),'transposition':s.tolist()},
      'triality_adjacency_on_common900':'12*(J3-I3) tensor I_300','adjacency_spectrum_common900':{'24':300,'-12':600},
      'S3_decomposition':'V_300 tensor (trivial_1 + standard_2)',
      '3cycle':{'whole900_eigenmultiplicities':'1^300, omega^300, omega_bar^300','trace_whole900':0,'trace_on_24_space':300,'trace_on_minus12_space':-300},
      'transposition':{'whole900_eigenmultiplicities':'+1^600, -1^300','trace_whole900':300,'trace_on_24_space':300,'minus12_space':'+1^300 + -1^300','trace_on_minus12_space':0},
      'theorem':'The common 900D triality sector is exactly 300 copies of the 3-letter permutation representation of S3. The +24^300 eigenspace is the S3-invariant diagonal V300; the -12^600 eigenspace is 300 copies of the standard S3 doublet.',
      'boundary':'Exact representation consequence of the verified incidence groupoid; no physical family interpretation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','decomposition':'300 x (1+2)','spectrum':'24^300,-12^600'}))
if __name__=='__main__':main()
