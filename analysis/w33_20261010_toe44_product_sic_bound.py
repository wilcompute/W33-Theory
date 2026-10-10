"""TOE44 algebraic, sharp product-state lower bound for W33 purity variance.
General entangled-state SIC endpoint is not settled here.
"""
import json,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
I=np.eye(3,dtype=complex);w=np.exp(2j*np.pi/3);X=np.roll(I,1,axis=0);Z=np.diag([1,w,w*w])
canon=lambda v:min(v,tuple((-t)%3 for t in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
Ws=[np.kron(np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,c),
            np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,d)) for a,b,c,d in pts]
def variance(z):
 z=z.reshape(9);z=z/np.linalg.norm(z)
 q=np.array([2*abs(np.vdot(z,W@z))**2 for W in Ws])
 assert abs(sum(q)-8)<1e-10
 return float((q@q-8/5)/135),q
# Pure product state: local projective powers u_1..u_4, v_1..v_4
# with sum u=sum v=2. Joint 32 powers = u_i*v_j/2, twice.
# Thus sum_p q_p² = U+V+UV/2 >= 1+1+1/2=5/2.
# Equality iff local U=V=1, i.e. all 4 local powers = 1/2.
# Hesse qutrit fiducial (0,1,-1)/sqrt2 is an explicit saturator.
fid=np.array([0,1,-1],complex)/np.sqrt(2)
local=[]
for a,c in [(0,1),(1,0),(1,1),(1,2)]:
 W=np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,c)
 local.append(2*abs(np.vdot(fid,W@fid))**2)
assert np.max(abs(np.array(local)-.5))<1e-12,local
value,q=variance(np.kron(fid,fid))
assert abs(value-1/150)<1e-12
rng=np.random.default_rng(44001)
min_product=1.
for _ in range(300):
 a=rng.normal(size=3)+1j*rng.normal(size=3);a/=np.linalg.norm(a)
 b=rng.normal(size=3)+1j*rng.normal(size=3);b/=np.linalg.norm(b)
 v,_=variance(np.kron(a,b))
 min_product=min(min_product,v)
 assert v>=1/150-1e-12,v
# The previous unconstrained 48-start numerical search reaches lower
# values, so entanglement can beat the product-only exact lower bound.
prev=json.loads((R/"data/w33_20261010_toe43_sic_search.json").read_text())
assert prev["best_purity_variance"]<1/150
out={"status":"EXACT_SHARP_SEPARABLE_PURE_SIC_NO_GO",
"theorem":"For every pure product two-qutrit psi=a tensor b, sum_p q_p^2=U+V+(U*V)/2 >=5/2 with U=sum four local u_i^2>=1 and V analogous. Therefore W33 90-frame variance >=(5/2-8/5)/135=1/150. Equality for tensor product of two Hesse qutrit SIC fiducials.",
"product_lower_bound_variance":"1/150","exact_Hesse_local_projective_powers":"1/2 each",
"saturation_product_vector":[[[float(z.real),float(z.imag)] for z in fid]]*2,
"numeric_saturation_variance":value,
"random_product_cases":300,"minimum_random_product_variance":min_product,
"previous_global_entangled_48start_best_variance":prev["best_purity_variance"],
"consequence":"A hypothetical elementary-abelian dimension-9 SIC fiducial must be entangled. This alone neither proves existence nor nonexistence of such fiducials.",
"proof":"Single qutrit pure-state Pauli Parseval: sum u_i=2 and sum v_i=2, so by Cauchy Schwarz U,V>=1. For two qutrits the 40 projective classes consist of 4 local A, 4 local B and 32 two-site Paulis; each pair (i,j) produces two q=u_i v_j/2."}
(R/"data/w33_20261010_toe44_product_sic_bound.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ["status","product_lower_bound_variance","numeric_saturation_variance","previous_global_entangled_48start_best_variance"]}))
