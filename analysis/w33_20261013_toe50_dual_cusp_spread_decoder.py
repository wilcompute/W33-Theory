"""TOE50: exact dual-visibility identity on 40 W33 LINES.

Synthesizes earlier Pass3694-3700 spread rank15 and TOE47 cusp
even-Weil operator rank25 into one perfect 40-channel decoder.
Not a new identification of 36 spread states with 40 point regions.
"""
import json,runpy
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
x=runpy.run_path(str(R/"analysis/w33_20261010_toe47_cusp_even5_ic_povm.py"))
lines=x["lines"];G=x["Gram"];P=x["projectors"];A=x["Aline"]
assert len(lines)==40
onpt=[[j for j,l in enumerate(lines) if p in l] for p in range(40)]
masks=[sum(1<<int(p) for p in l) for l in lines];full=(1<<40)-1
solutions=set()
def rec(chosen,used):
 if used==full:solutions.add(tuple(sorted(chosen)));return
 uncovered=[p for p in range(40) if not ((used>>p)&1)]
 pivot=min(uncovered,key=lambda p:sum(not(used&masks[j]) for j in onpt[p]))
 for j in onpt[pivot]:
  if used&masks[j]:continue
  rec(chosen+[j],used|masks[j])
rec([],0)
spreads=sorted(solutions)
assert len(spreads)==36
B=np.zeros((40,36),dtype=np.int64)
for j,sp in enumerate(spreads):B[list(sp),j]=1
assert np.array_equal(B.sum(axis=0),np.full(36,10))
assert np.array_equal(B.sum(axis=1),np.full(40,9))
I=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
S=B@B.T
assert np.array_equal(S,6*I-3*A+3*J)
GC9=8*I+2*A+J
assert np.max(abs(9*G-GC9))<2e-11
# all coefficients are rational; exact cancel denominators:
# I=(3/4)G+(1/18)BB^T-(1/4)J
# Clear denominators by 36: 36I = 27G +2S -9J
# 27G=3(9G)=3GC9.
assert np.array_equal(36*I,3*GC9+2*S-9*J)
# Removing the constant packet gives strictly orthogonal visible modes:
# 5*(9G-8P0*9) = 5 GC9-9J, 4*(S-90P0)=4S-9J.
assert np.array_equal((5*GC9-9*J)@(4*S-9*J),np.zeros((40,40),dtype=np.int64))
assert np.linalg.matrix_rank(G,tol=1e-8)==25
assert np.linalg.matrix_rank(S,tol=1e-8)==16
assert np.linalg.matrix_rank(np.vstack([G,B.T]),tol=1e-8)==40
rng=np.random.default_rng(50001)
recon=[]
for _ in range(50):
 y=rng.normal(size=40)
 # cusp observable = 5D operator X=Σ y_L P_L;
 # its 40 analysis values are tr(P_j X)=(G y)_j.
 X=np.einsum("p,pij->ij",y,P)
 gy=np.einsum("pij,ji->p",P,X).real
 bs=B.T@y
 pred=.75*gy+(B@bs)/18 -y.sum()/4
 recon.append(float(np.max(abs(pred-y))))
assert max(recon)<1e-11
out={"status":"EXACT_DUAL_40_LINE_RECONSTRUCTION_FROM_EVEN5_AND_36_SPREADS",
"data":"Same 40 W33 line labels index cusp projectors and 36 spread membership columns",
"counts":{"W33_lines":40,"W33_spreads":36,"lines_per_spread":10,"spreads_per_line":9},
"cusp_projector_Gram":"G=(8I+2Aline+J)/9 ; rank25; kernel line A=-4 packet dimension15",
"spread_Gram":"S=B B^T=6I-3Aline+3J ; rank16; kernel line A=+2 packet dimension24",
"exact_identity":"36I=3(9G)+2BB^T-9J, or I=(3/4)G+(1/18)BB^T-(1/4)J",
"positive_orthogonal_resolution":"I=P0+(3/4)(G-8P0)+(1/18)(BB^T-90P0), with P0=J/40; all three summands positive-semidefinite mutually orthogonal projectors of ranks 1,24,15",
"exact_centered_orthogonality":"(5*(9G)-9J)*(4*(BB^T)-9J)=0 in integer arithmetic",
"rank_of_combined_cusp_spread_measurement":40,
"random_arbitrary_real_40_channel_reconstructions":50,
"max_reconstruction_error":max(recon),
"representation":"line module 40=1+24+15. Cusp even5 operator channel 25=1+24 sees all but15; spread channel 16=1+15 sees all but24; overlap is the constant1. Joint kernel zero.",
"physical_reading":"A general arbitrary 40-line signal y is recovered from its even5 operator synthesis X=sum(y_L P_L), 36 spread sums B^T y and the single global sum 1^T y. This is complementary coherent-information / combinatorial-information algebra, NOT complete physical state tomography of C9. Unlike the retracted hypervisor claim, it does not equate the 36 spreads to 36-point retention regions.",
"prior_art":"Pass3694-3700 proved spread 15D ETF and 36 spreads; exploration/w33_point_line_spread_rank_one_bridge proved 1+15 vs1+24 incidence cancellation; TOE47 established cusp 25D operator frame. New packet cross-multiplies the two exact operators on SAME 40 W33 line labels, deriving an integer-denominator-free reconstruction identity. Check prior repo claims before priority attribution.",
"science_boundary":"This is a finite geometry linear algebra theorem with numerical complex projector implementation; no S-matrix, SM fit, measured physical channel, or TOE."}
(R/"data/w33_20261013_toe50_dual_cusp_spread_decoder.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"max_err":max(recon),"rank":out["rank_of_combined_cusp_spread_measurement"]}))
