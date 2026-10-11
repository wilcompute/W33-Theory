"""TOE47: exact 40-cusp even-Weil 5D IC POVM and equivariant visible quotient."""
from pathlib import Path
import json,itertools,collections,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
import w33_pass11897_11898_kahler_moduli_two_qutrit_weil as K
O=R/"data/w33_20261010_toe47_even5_cusp_ic_povm.json"
rng=np.random.default_rng(47005)
Q,_=np.linalg.qr(K.even_basis())
g5={name:Q.conj().T@g@Q for name,g in K.GENS.items()}
sym={name:K.symplectic_image(g) for name,g in K.GENS.items()}
canon=lambda v:min(v,tuple(-int(x)%3 for x in v))
P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
ix={v:i for i,v in enumerate(P)}
sp=lambda u,v:(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
lines=set()
for i,u in enumerate(P):
 for v in P[i+1:]:
  if sp(u,v):continue
  lines.add(tuple(sorted({ix[canon(tuple((a*u[j]+b*v[j])%3 for j in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b})))
lines=sorted(lines);lineix={l:i for i,l in enumerate(lines)}
assert len(lines)==40
Aline=np.array([[int(i!=j and len(set(a)&set(b))==1) for j,b in enumerate(lines)] for i,a in enumerate(lines)])
N=np.zeros((40,40),dtype=int)
for j,l in enumerate(lines):N[j,list(l)]=1
assert np.all(N.T@N==4*np.eye(40,dtype=int)+np.array([[int(i!=j and sp(u,v)==0) for j,v in enumerate(P)] for i,u in enumerate(P)]))
zline=tuple(i for i,p in enumerate(P) if p[:2]==(0,0))
assert len(zline)==4
seed=Q.conj().T@np.eye(9)[:,K.IDX[(0,0)]]
def normalize(z):
 z=z/np.linalg.norm(z)
 j=np.argmax(np.abs(z)>1e-9)
 return z*np.conj(z[j])/abs(z[j])
def key(z):return tuple((np.round(np.r_[z.real,z.imag],9)+0).tolist())
start=normalize(seed)
orbit={key(start):(start,zline)}
queue=collections.deque([start])
while queue:
 v=queue.popleft();l=orbit[key(v)][1]
 for name,u in g5.items():
  w=normalize(u@v)
  newl=tuple(sorted(ix[canon(tuple((sym[name]@np.array(P[i]))%3))] for i in l))
  if key(w) not in orbit:
   orbit[key(w)]=(w,newl);queue.append(w)
  else:assert orbit[key(w)][1]==newl
assert len(orbit)==40
assert len({entry[1] for entry in orbit.values()})==40
rays={lineix[l]:v for v,l in orbit.values()}
ray=np.stack([rays[i] for i in range(40)])
projectors=np.einsum("pi,pj->pij",ray,ray.conj())
Gram=np.einsum("pij,qji->pq",projectors,projectors).real
Id=np.eye(40);J=np.ones((40,40))
wanted=Id+Aline/3+(J-Id-Aline)/9
assert np.max(abs(Gram-wanted))<3e-12
eig=np.linalg.eigvalsh(Gram)
assert np.max(abs(eig-np.array([0.]*15+[4/3]*24+[8.])))<2e-11
assert np.linalg.matrix_rank(Gram,tol=1e-9)==25
assert np.max(abs(projectors.sum(axis=0)-8*np.eye(5)))<3e-12
# 40 rank one projectors are a COMPLEX projective 2-design in C5.
# Sum |v><v| tensor |v><v| = (4/3)(I + SWAP) on C5 tensor C5.
swap=np.zeros((25,25),complex)
for i in range(5):
 for j in range(5):swap[i*5+j,j*5+i]=1
twosum=sum(np.kron(p,p) for p in projectors)
design_err=float(np.max(abs(twosum-(4/3)*(np.eye(25)+swap))))
assert design_err<3e-12,design_err
# POVM effects E_p=P_p/8. The 40 outcomes carry full 5x5
# informational completeness. Dual reconstruction:
# rho5 = 6 sum_r Pr(r) P_r - I5.
def sample():
 M=rng.normal(size=(5,5))+1j*rng.normal(size=(5,5))
 rho=M@M.conj().T;rho/=np.trace(rho).real
 prob=np.einsum("ij,pji->p",rho,projectors).real/8
 out=6*np.einsum("p,pij->ij",prob,projectors)-np.eye(5)
 return max(abs(out-rho).ravel()),prob
trials=[sample() for _ in range(30)]
max_rec=float(max(x[0] for x in trials))
assert max_rec<2e-12
# Physically well-defined lift to TWO QUTRITS: the five-dimensional
# even Weil subspace Q of C9. E_r^9=Q P_r Qdag/8, plus E_odd=I9-QQdag
# is a 41-outcome POVM. It reconstructs only the EVEN BLOCK of a
# general 9D density matrix; odd/coherence degrees are invisible.
effects=np.einsum("ai,pij,bj->pab",Q,projectors,Q.conj())/8
odd_effect=np.eye(9)-Q@Q.conj().T
assert np.max(abs(effects.sum(axis=0)+odd_effect-np.eye(9)))<2e-12
egram=np.einsum("pij,qji->pq",np.concatenate([effects,odd_effect[None]]),
               np.concatenate([effects,odd_effect[None]])).real
assert np.linalg.matrix_rank(egram,tol=1e-9)==26
lift_errors=[]
for _ in range(15):
 m=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
 r=m@m.conj().T;r/=np.trace(r).real
 p_even=float(np.trace(Q.conj().T@r@Q).real)
 pr=np.einsum("ab,pba->p",r,effects).real
 p_odd=float(np.trace(r@odd_effect).real)
 assert abs(pr.sum()+p_odd-1)<1e-12
 assert abs(pr.sum()-p_even)<1e-12
 even_block=Q.conj().T@r@Q
 reconstructed=6*np.einsum("p,pij->ij",pr,projectors)-p_even*np.eye(5)
 lift_errors.append(float(np.max(abs(even_block-reconstructed))))
assert max(lift_errors)<2e-12
# Explicit equivariance: 40 line permutation maps into conjugation on End C5
equiv_err=0.
char={}
for name,u in g5.items():
 perm=np.zeros((40,40))
 for j,line in enumerate(lines):
  ll=tuple(sorted(ix[canon(tuple((sym[name]@np.array(P[i]))%3))] for i in line))
  perm[lineix[ll],j]=1
 test=np.einsum("ab,pbc,dc->pad",u,projectors,u.conj())
 target=np.einsum("pq,qij->pij",perm.T,projectors)
 err=float(np.max(abs(test-target)));equiv_err=max(equiv_err,err)
 assert err<3e-12
 vis=np.eye(40)-(Aline-12*Id)@(Aline-2*Id)/96
 chi_target=float(np.trace(vis@perm).real)
 chi_end=float(abs(np.trace(u))**2)
 assert abs(chi_target-chi_end)<1e-10
 char[name]={"visible_character":chi_target,"End5_character":chi_end,"max_projector_equivariance_error":err}
# This is a 40-element labelled line orbit, not an interchange of
# point and line parabolic representations. The earlier non-isomorphic
# ternary point/line 13-designs stay non-isomorphic over F3.
out={"status":"EXACT_40_CUSP_COMPLEX_PROJECTIVE_2_DESIGN_AND_EVEN5_IC_POVM",
"cusp_rays":40,"even_weil_dimension":5,"projector_Hermitian_span_dimension":25,
"off_diagonal_squared_inner_product_counts":{"1/3":480,"1/9":1080},
"Gram_formula":"G=(8/9)I+(2/9)A_line+(1/9)J",
"Gram_eigenvalues":{"8":1,"4/3":24,"0":15},
"frame_operator_sum":"sum P_r=8 I5","projective_2_design":"sum P_r tensor P_r=4/3*(I25+SWAP)",
"max_projective_2_design_error":design_err,
"exact_IC_POVM":"E_r=P_r/8, sum E_r=I5, Pr(r)=Tr(rho E_r)",
"dual_reconstruction":"rho=6*sum_r Pr(r)*P_r-I5",
"max_30_random_mixed_reconstruction_error":max_rec,
"two_qutrit_41_outcome_embedding":{"even_outcomes":40,"odd_leakage_outcomes":1,
"effect_operator_span_dimension":26,"invisible_two_qutrit_traceless_directions":55,
"exact_effects":"E_r=Q P_r Qdag/8 (r=1..40), E_odd=I9-Q Qdag",
"unnormalized_even_block_reconstruction":"B=Qdag rho9 Q = 6 sum_r Pr_9(r)*P_r - p_even I5",
"max_15_random_two_qutrit_even_block_reconstruction_error":max(lift_errors)},
"max_generator_equivariance_error":equiv_err,
"seven_W33_line_action_character_checks":char,
"true_new_synthesis":"Pass11899 identifies 40 Kähler cusp RAYS in even Weil C5 and W33 LINES; here their rank-one projectors are shown to be a 5D projective 2-design and a 40-outcome informationally complete POVM, with explicit closed inverse and Sp4(3)-equivariant 25-dimensional quotient of the 40-line permutation module.",
"credit_and_boundary":"40 cusps and their even Weil 5D action were previously found in Pass11899; projective 2-designs and IC-POVM dual formulas are prior mathematics. This packet derives/tests their explicit joint specialization and operational reading. Not a measurement of string-theoretic cusps, does not turn a Kähler modulus into a photonic Hilbert space, and does not prove point/line 40-designs are isomorphic over F3."
}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"povm_dim":25,"error":max_rec,"design_error":design_err,"equivariance":equiv_err}),flush=True)
