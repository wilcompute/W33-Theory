"""TOE41 native Albert E6 45-term signed cubic quantum phase.

N(A,B,C)=det(A)+det(B)+det(C)-tr(A B C).
Each squarefree signed term implements a commuting three-qutrit CCZ phase.
This is a 27-qutrit *mathematical* unitary; no hardware implementation claimed.
"""
import itertools,collections,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe41_e6_45_ccz_compiler.json"
terms=[]
for block in (0,9,18):
 for perm in itertools.permutations(range(3)):
  inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
  triple=tuple(block+3*i+perm[i] for i in range(3))
  terms.append((triple,(-1)**inv))
# -Tr(ABC) = -sum_i,j,k A_ij B_jk C_ki.
for i,j,k in itertools.product(range(3),repeat=3):
 terms.append(((3*i+j,9+3*j+k,18+3*k+i),-1))
assert len(terms)==45
assert len({tuple(sorted(t)) for t,s in terms})==45
assert collections.Counter(x for t,s in terms for x in t)=={i:5 for i in range(27)}
def signperm(p):
 return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
def det3(M):
 return sum(signperm(p)*math.prod(M[i][p[i]] for i in range(3)) for p in itertools.permutations(range(3)))
def cubic(x):
 return sum(sign*math.prod(x[j] for j in triple) for triple,sign in terms)
def as_matrix(x,b):return [list(x[b+3*i:b+3*i+3]) for i in range(3)]
def direct(x):
 A=as_matrix(x,0);B=as_matrix(x,9);C=as_matrix(x,18)
 T=sum(A[i][j]*B[j][k]*C[k][i] for i,j,k in itertools.product(range(3),repeat=3))
 return det3(A)+det3(B)+det3(C)-T
import numpy as np
rng=np.random.default_rng(410041)
for sample in range(300):
 x=rng.integers(0,3,size=27).tolist()
 assert cubic(x)==direct(x)
# Coefficients of the third finite difference on the *zero* configuration:
# for distinct indices, it equals the signed monomial coefficient mod 3.
def mixed_zero(indices):
 v=[0]*27
 s=0
 for bits in itertools.product((0,1),repeat=3):
  y=v.copy()
  for t,k in zip(indices,bits):y[t]=k
  s+=(-1)**(3-sum(bits))*cubic(y)
 return s%3
assert all(mixed_zero(t)==(sgn%3) for t,sgn in terms)
# For X_j shift on F3, U X_j U^dag is X_j times a diagonal
# in the Clifford group; its phase polynomial has degree <=2.
# Because (x+1 mod3)^2 contains a delta carry, do not claim the
# general Clifford hierarchy level from integer cubic alone.
def conjugation_phase(x,j):
 y=x.copy();y[j]=(y[j]+1)%3
 return (cubic(y)-cubic(x))%3
# The affected terms each contain index j once; shift is always +1 mod3.
for j in range(27):
 for _ in range(8):
  x=rng.integers(0,3,size=27).tolist()
  expected=sum(s*math.prod(x[k] for k in t if k!=j) for t,s in terms if j in t)%3
  assert conjugation_phase(x,j)==expected
# Schedule mutually disjoint 3-body gates. Greedy coloring of conflict graph
# uses no ancillas, with 45 CCZ primitives and 27 qutrits.
adj=[{j for j,(u,_) in enumerate(terms) if j!=i and set(t)&set(u)} for i,(t,_) in enumerate(terms)]
best=None
for seed in range(400):
 order=list(range(45));rng.shuffle(order)
 order.sort(key=lambda i:-len(adj[i]))
 colors={}
 for i in order:
  used={colors[j] for j in adj[i] if j in colors}
  colors[i]=next(c for c in range(20) if c not in used)
 size=max(colors.values())+1
 if best is None or size<best[0]:best=(size,colors)
 if size==5:break
layers=[sorted(i for i,c in best[1].items() if c==color) for color in range(best[0])]
assert len([i for layer in layers for i in layer])==45
assert all(len({v for i in layer for v in terms[i][0]})==3*len(layer) for layer in layers)
# No all-3^27 statevector allocation; sparse action is a diagonal phase oracle.
phase_test=[]
for x in ([0]*27,[1]*27, list(rng.integers(0,3,size=27))):
 p=int(cubic(x)%3)
 phase_test.append({"mod3_phase_exponent":p,"absolute_amplitude":1.0})
# Independently schedule *existing committed native triads*, not just
# standard three-matrix presentation; prior 45-CCZ opcode is Pass10944.
native_source=json.loads((ROOT/"artifacts/canonical_su3_gauge_and_cubic.json").read_text())
native=[(tuple(map(int,row["triple"])),int(row["sign"]))
        for row in native_source["solution"]["d_triples"]]
assert len(native)==45
assert len({tuple(sorted(t)) for t,s in native})==45
assert collections.Counter(v for t,s in native for v in t)=={j:5 for j in range(27)}
def native_layers_schedule(triples):
 conflicts=[{j for j,(u,_) in enumerate(triples) if j!=i and set(t)&set(u)}
            for i,(t,_) in enumerate(triples)]
 r=np.random.default_rng(10944)
 winner=None
 for trial in range(5000):
  order=list(range(45));r.shuffle(order);order.sort(key=lambda i:-len(conflicts[i]))
  c={}
  for i in order:
   used={c[j] for j in conflicts[i] if j in c}
   c[i]=next(z for z in range(20) if z not in used)
  layers_count=max(c.values())+1
  if winner is None or layers_count<winner[0]:winner=(layers_count,c)
  if layers_count==5:break
 assert winner[0]==5,("5-layer native proof failed",winner[0])
 layers=[[i for i,z in winner[1].items() if z==k] for k in range(5)]
 assert all(len(layer)==9 and len({v for i in layer for v in triples[i][0]})==27 for layer in layers)
 return layers
native_layers=native_layers_schedule(native)
out=dict(status="PASS_NATIVE_SIGNED_CUBIC_UNITARY",register_qutrits=27,
         determinant_monomials=18,trace_monomials=27,total_ccz_gates=len(terms),
         per_qutrit_terms=5,gate_depth_disjoint_upper_bound=best[0],
         gate_depth_degree_lower_bound=5,gate_layer_sizes=[len(x) for x in layers],
         native_source="artifacts/canonical_su3_gauge_and_cubic.json",
         native_gate_depth_optimum=5,native_layer_sizes=[len(x) for x in native_layers],
         native_layer_indices=native_layers,
         native_triples=[{"sites":list(t),"sign":int(s)} for t,s in native],
         prior_art="Pass10944 already established the exact 45 signed CCZ phase-kickback gate; TOE41 adds the optimal native 5-round 9-per-round disjoint schedule.",
         phases=phase_test,
         triples=[{"sites":list(t),"sign":s} for t,s in terms],
         invariant="N=det A+det B+det C-Tr(ABC); U|x>=exp(2pi i N(x)/3)|x>. Each term is a diagonal 3-body qutrit CCZ^sign. E6 complex cubic algebra invariance does not imply this quantum gate commutes with an E6 unitary representation.",
         boundary="This is an exactly specified 27-qutrit non-Clifford diagonal circuit, not a photonic device or a fault-tolerant E6 implementation. Physical three-body couplings and E6 unitary invariance are unproved.")
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="triples"}))
