#!/usr/bin/env python3
"""Compact exact reconstruction of q=7 full distinct-index cubic tensor.
Derives all five PSp(4,7) unordered three-point orbit types, checks exhaustive
720300-support averages, and verifies the cubic zero-sum checksum.
"""
import sys,json,math
from pathlib import Path
from fractions import Fraction
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from even_line_sets_gf import build
def main():
 source=json.loads((ROOT/"data/w33_20261102_q7_exhaustive_triple_moments.json").read_text())
 assert source["orbit_supports"]==source["expected_full_orbit"]==720300
 moments={k:Fraction(v["orbit_average_fraction"]) for k,v in source["point_triples"].items()}
 expected={"line":Fraction(93,28),"two_edges":Fraction(-117,343),
           "one_edge":Fraction(57,1372),"nonisotropic_line":Fraction(-142,343),
           "independent":Fraction(1,196)}
 assert moments==expected,(moments,expected)
 q=7;v=(q+1)*(q*q+1);r=q*(q+1)
 counts={"line":v*math.comb(q+1,3),
         "two_edges":v*(math.comb(r,2)-(q+1)*math.comb(q,2)),
         "one_edge":(v*r//2)*(v-(2*r-(q-1))),
         "nonisotropic_line":((q*q+1)*(q*q+q+1)-v)*math.comb(q+1,3)}
 counts["independent"]=math.comb(v,3)-sum(counts.values())
 assert counts=={"line":22400,"two_edges":548800,"one_edge":3292800,
       "nonisotropic_line":137200,"independent":6585600}
 total=sum(counts[k]*expected[k] for k in expected)
 # x_s sum coordinates = 0, x_i^2=x_i+6, <x_i²>=6.
 # 0 = E[(sum_i x_i)^3] = 400*6 + 3*(-400*6) + 6 * sum_{distinct triples}E[x_ix_jx_k]
 # so distinct unordered moments weighted sum must equal 800.
 assert total==800,total
 pts,lines,N=build(q);pidx={p:i for i,p in enumerate(pts)}
 A=N@N.T-(q+1)*np.eye(v,dtype=np.int64)
 def point_norm(t):
  f=next(z for z in t if z)
  return tuple((z*pow(f,-1,q))%q for z in t)
 def classify(a,b,c):
  if a==b==c:return "diagonal"
  if a==b or a==c or b==c:return "repeated_pair_adj" if int(A[a,c if a==b else b]) else "repeated_pair_far" if a==b else ("repeated_pair_adj" if A[a,b] else "repeated_pair_far")
  s=int(A[a,b]+A[a,c]+A[b,c])
  if s==3:return "line"
  if s==2:return "two_edges"
  if s==1:return "one_edge"
  span={pidx[point_norm(tuple((pts[a][i]+t*pts[b][i])%q for i in range(4)))] for t in range(q)}|{b}
  return "nonisotropic_line" if c in span else "independent"
 # Check all five frozen witnesses; and thousands random configurations.
 for k,z in source["point_triples"].items():
  assert classify(*z["points"])==k,(k,z["points"],classify(*z["points"]))
 rng=np.random.default_rng(20261102)
 seen=set()
 for i in range(3000):
  a,b,c=map(int,rng.choice(v,3,replace=False))
  typ=classify(a,b,c);assert typ in expected
  seen.add(typ)
 assert "independent" in seen
 # Same x coordinate has values (3,-2), so x²=x+6.
 # E[x_i² x_j]=E[x_i x_j] via zero first moment and second moments.
 # Adjacent covariance = 9/14, far covariance = -6/49.
 diag=Fraction(6,1);repeat_adj=Fraction(9,14);repeat_far=Fraction(-6,49)
 out={"status":"PASS_FULL_Q7_CUBIC_TENSOR_TYPE_RECONSTRUCTION",
  "q":q,"point_count":v,"full_route_orbit":720300,"distinct_point_triple_total":math.comb(v,3),
  "distinct_triple_orbit_types":{k:{"count":counts[k],"moment":str(expected[k]),
           "float":float(expected[k]),"symmetry_stabilizer_order":138297600//counts[k]} for k in expected},
  "global_weighted_cubic_sum":str(total),
  "global_cubic_sum_expected_from_centering":"800",
  "all_distinct_index_tensor_entries_specified_by_five_orbit_types":True,
  "coincident_triple_moment":str(diag),
  "two_coincident_adjacent":str(repeat_adj),
  "two_coincident_nonadjacent":str(repeat_far),
  "line_moment_distinct_from_all_nonlines":all(expected["line"]!=x for k,x in expected.items() if k!="line"),
  "line_reconstruction":"For DISTINCT a,b,c, T_abc=93/28 iff all three lie on an isotropic W(3,7) line.",
  "orbit_transitivity_basis":"Witt symplectic extension lemma; for independent nonorthogonal triples at q=7 odd relabeling flips the square class of the product of pairings because -1 is nonsquare in GF7. Other edge-incidence classes transport by matching pairings/scalings. Projectively dependent triples lie on isotropic or nonisotropic lines; line stabilizers act as PGL2(7).",
  "caveats":"Five-orbit transitivity argument assumes full PSp4(7) automorphism action, not only a random walk. 720300 full line-support orbit enumerated exactly. Not a field-theory or physical dynamics result."}
 p=ROOT/"data/w33_20261102_q7_full_cubic_tensor_types.json"
 p.write_text(json.dumps(out,indent=2)+"\n")
 print("Q7_FULL_CUBIC_TYPES",json.dumps(out)[:4000],flush=True)
 return out
if __name__=="__main__":main()
