"""TOE47: Wilson-line point selects FOUR conditional qutrit MUBs in each charge."""
from pathlib import Path
import json,itertools
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/"data/w33_20261010_toe47_wilson_conditional_mubs.json"
omega=np.exp(2j*np.pi/3)
I=np.eye(3,dtype=complex);X=np.roll(I,1,axis=0);Z=np.diag([1,omega,omega*omega])
canon=lambda v:min(v,tuple(-int(x)%3 for x in v))
points=sorted({canon(p) for p in itertools.product(range(3),repeat=4) if any(p)})
idx={p:i for i,p in enumerate(points)}
sp=lambda p,q:(p[0]*q[2]+p[1]*q[3]-p[2]*q[0]-p[3]*q[1])%3
W=np.stack([np.kron(np.linalg.matrix_power(X,p[0])@np.linalg.matrix_power(Z,p[2]),
                   np.linalg.matrix_power(X,p[1])@np.linalg.matrix_power(Z,p[3])) for p in points])
lines=set()
for i,p in enumerate(points):
 for q in points[i+1:]:
  if sp(p,q):continue
  lines.add(tuple(sorted({idx[canon(tuple((a*p[j]+b*q[j])%3 for j in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b})))
lines=sorted(lines);assert len(lines)==40
p=idx[(0,0,0,1)]
plines=[l for l in lines if p in l]
assert len(plines)==4
def P3(w):
 return [(np.eye(9)+omega**(-j)*w+omega**(-2*j)*w@w)/3 for j in range(3)]
Q=np.stack(P3(W[p]))
assert np.max(abs(Q.sum(axis=0)-np.eye(9)))<1e-12
assert max(abs(np.trace(q)-3) for q in Q)<1e-12
families=[]
for l in plines:
 sec=next(i for i in l if i!=p)
 Rb=P3(W[sec])
 P=np.array([[Q[a]@Rb[b] for b in range(3)] for a in range(3)])
 assert max(abs(sum(P.reshape(9,9,9))-np.eye(9)).ravel())<1e-12
 assert max(abs(np.trace(t)-1) for t in P.reshape(9,9,9))<1e-12
 families.append(P)
families=np.stack(families)
overlap_err=0
for a in range(3):
 for u in range(4):
  for v in range(4):
   for b in range(3):
    for c in range(3):
     overlap=float(np.trace(families[u,a,b]@families[v,a,c]).real)
     expect=(float(b==c) if u==v else 1/3)
     overlap_err=max(overlap_err,abs(overlap-expect))
assert overlap_err<2e-12
crosscharge=max(abs(np.trace(families[0,a,b]@families[1,aa,c])) for a in range(3) for aa in range(3) for b in range(3) for c in range(3) if a!=aa)
assert crosscharge<1e-12
rng=np.random.default_rng(47003)
errs=[]
for t in range(44):
 M=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
 rho=M@M.conj().T;rho/=np.trace(rho)
 obs=float(np.sum(np.einsum("ab,lcjba->lcj",rho,families).real**2))
 blocks=np.array([q@rho@q for q in Q])
 w=np.array([np.trace(b).real for b in blocks])
 formula=float(sum(np.trace(b@b).real for b in blocks)+sum(w*w))
 assert abs(obs-formula)<1e-12
 errs.append(abs(obs-formula))
 # For a supported charge block, four full MUB contexts recover purity.
 v=Q[0]@(rng.normal(size=9)+1j*rng.normal(size=9))
 v=v/np.linalg.norm(v)
 sigma=np.outer(v,v.conj())
 collision=float(np.sum(np.einsum("ab,lcjba->lcj",sigma,families).real**2))
 assert abs(collision-2)<1e-11
# All 40 possible W33 holonomy points have exactly four incident lines;
# conjugation maps charge resolved bases by the symplectic Clifford action.
assert all(sum(p in l for l in lines)==4 for p in range(40))
out={"status":"EXACT_FOUR_QUTRIT_MUBS_PER_WILSON_CHARGE_SECTOR",
"canonical_Wilson_holonomy":"Z2", "projective_W33_vector":[0,0,0,1],
"wilson_point_index":p,"four_incident_W33_line_indices":[lines.index(l) for l in plines],
"charge_values":3,"rank_of_each_charge_sector":3,"bases_per_charge_sector":4,"basis_vectors_per_sector_per_context":3,
"maximum_conditional_MUB_overlap_error":overlap_err,"max_cross_charge_overlap":float(crosscharge),
"block_collision_identity":"Sum over 4 Wilson-compatible 9-outcome bases and all outcomes of p(basis,outcome)^2 = sum_charge (Tr(rho_charge²)+(Tr rho_charge)^2), rho_charge=Q_charge rho Q_charge",
"charge_supported_purity":"For normalized rho supported in one Wilson charge, sum of four basis collision probabilities=1+Tr rho² (four complete qutrit MUBs)",
"random_full_rank_density_trials":len(errs),"max_collision_block_identity_error":max(errs),
"physics_boundary":"Pauli Z2 is a chosen idealized Wilson holonomy on a two-qutrit representation; a physical heterotic Wilson line requires a verified gauge-bundle embedding. No inference that all 491 scanned models have this canonical W33 Pauli operator or that a holonomy selects allowed SM Yukawas."}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"overlap_error":overlap_err,"block_identity_max_error":max(errs),"contexts":out["four_incident_W33_line_indices"]}),flush=True)
