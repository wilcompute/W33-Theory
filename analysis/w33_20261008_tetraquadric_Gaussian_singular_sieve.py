"""Exact finite set of cyclotomic Gaussian-rational candidate critical points
for the Oct8 sparse invariant tetraquadric. Positive singular witness
over Q(i) would prove particular polynomial singular over C.
No singular point found does NOT imply smoothness.
"""
from pathlib import Path
import itertools,json,sympy as sp
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/w33_20261008_tetraquadric_Gaussian_singular_sieve.json"
def product(vals):
 r=1
 for a in vals:r*=a
 return r
def at(coords):
 S=[];D=[];T=[];dS=[];dD=[];dT=[]
 for t in coords:
  if t=="inf":x,y=sp.Integer(0),sp.Integer(1);xs,ys=sp.Integer(1),sp.Integer(0)
  else:x,y=sp.Integer(1),t;xs,ys=sp.Integer(0),sp.Integer(1)
  S.append(x*x+y*y);D.append(x*x-y*y);T.append(2*x*y)
  dS.append(2*x*xs+2*y*ys);dD.append(2*x*xs-2*y*ys);dT.append(2*(xs*y+x*ys))
 f=product(S)+2*product(D)+3*product(T)
 grad=[dS[j]*product(S[:j]+S[j+1:])+2*dD[j]*product(D[:j]+D[j+1:])+3*dT[j]*product(T[:j]+T[j+1:]) for j in range(4)]
 return sp.expand(f),[sp.expand(g) for g in grad]
def main():
 trial=[0,1,-1,sp.I,-sp.I,"inf"]
 hits=[];zeros=0
 for x in itertools.product(trial,repeat=4):
  f,grad=at(x)
  if f==0:
   zeros+=1
   if all(g==0 for g in grad):hits.append([str(t) for t in x])
 return {"polynomial":"prod s+2 prod d+3 prod t",
  "projective_affine_candidate_coordinates":[str(x) for x in trial],
  "total_examined":len(trial)**4,
  "hypersurface_points_in_sieve":zeros,
  "actual_C_singular_points_with_all_four_gradient_zero":hits,
  "particular_sparse_polynomial_proven_singular_over_Qi":len(hits)>0,
  "no_singular_witness_not_smoothness_proof":True}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k!="projective_affine_candidate_coordinates"},flush=True)
 print("TETRAQUADRIC_GAUSSIAN_SIEVE_PASS")
