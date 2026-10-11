"""TOE45: W33 cusp line-collision tomography and an exact physical blind sector.

Fuses known point/line incidence rank (Pass4952), TOE42 pure Pauli spectral
constraint, and Pass11899 cusp/Pass11900 Wilson-point interpretation.
No claim that classical GQ singular spectrum is new.
"""
from __future__ import annotations
from pathlib import Path
import itertools,json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe45_cusp_collision_tomography.json"
rng=np.random.default_rng(45010)
V=list(itertools.product(range(3),repeat=4))
canon=lambda v:min(v,tuple(-a%3 for a in v))
sp=lambda p,q:(p[0]*q[2]+p[1]*q[3]-p[2]*q[0]-p[3]*q[1])%3
pts=sorted({canon(v) for v in V if any(v)})
index={v:i for i,v in enumerate(pts)}
assert len(pts)==40
A=np.array([[int(i!=j and sp(p,q)==0) for j,q in enumerate(pts)]
            for i,p in enumerate(pts)],dtype=np.int64)
lines=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if sp(p,q):continue
  L=frozenset(index[canon(tuple((a*p[k]+b*q[k])%3 for k in range(4)))]
       for a,b in itertools.product(range(3),repeat=2) if a or b)
  assert len(L)==4
  lines.add(tuple(sorted(L)))
lines=sorted(lines)
assert len(lines)==40
N=np.zeros((40,40),dtype=np.int64)
for i,L in enumerate(lines):N[i,list(L)]=1
I=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
assert np.array_equal(N.T@N,4*I+A)
assert np.array_equal(N.sum(0),np.full(40,4))
assert np.array_equal(N.sum(1),np.full(40,4))
assert np.array_equal(A@A,12*I+2*A+4*(J-I-A))
project_minus=((A-12*I)@(A-2*I))/96
assert np.max(abs(N@project_minus))<1e-12
assert np.max(abs(project_minus@project_minus-project_minus))<1e-12
assert np.linalg.matrix_rank(N)==25
assert np.linalg.matrix_rank(N.T@N)==25
assert np.max(abs(np.linalg.svd(N,compute_uv=False)[:1]-4))<1e-12

# Every fixed Wilson-line point p is incident to 4 cusp contexts and
# nonincident to 36. A nonincident cusp has exactly one p-commuting Pauli.
for p in range(40):
 inc=int(N[:,p].sum())
 assert inc==4
 assert sum(sum(sp(pts[p],pts[x])==0 for x in L)==1
            for L in lines if p not in L)==36

omega=np.exp(2j*np.pi/3)
eye=np.eye(3,dtype=complex)
X=np.roll(eye,1,axis=0);Z=np.diag([1,omega,omega*omega])
W=np.stack([np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),
                    np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3])) for v in pts])
def powers(rho):
 expectations=np.einsum("ij,pji->p",rho,W)
 return 2*np.abs(expectations)**2
def purecheck(psi):
 psi=psi/np.linalg.norm(psi)
 rho=np.outer(psi,psi.conj())
 q=powers(rho)
 assert abs(q.sum()-8)<1e-10
 assert np.max(abs(A@q-2*q-2))<1e-10
 collisions=(1+N@q)/9
 qback=np.full(40,1/5)+(N.T@(9*collisions-1-4/5))/6
 return float(np.max(abs(q-qback))),float(np.max(abs(project_minus@q)))
pure_cases=[]
for _ in range(64):
 z=rng.normal(size=9)+1j*rng.normal(size=9)
 pure_cases.append(purecheck(z))
assert max(x[0] for x in pure_cases)<1e-12

# Full rank density operators with distinct 15-dimensional dark vectors
# but IDENTICAL 40 exact projective MUB-basis collision probabilities.
h=project_minus@np.arange(1,41,dtype=float)
h/=max(abs(h))
assert np.max(abs(N@h))<1e-12
t=1e-5
eps=2e-6
qplus=t*np.ones(40)+eps*h
qminus=t*np.ones(40)-eps*h
assert min(qplus.min(),qminus.min())>0
def state_from_q(q):
 # Since Tr((W_p+W_p^dag) W_q)=9 delta_{pq}, each expectation
 # is exactly mu_p=sqrt(q_p/2), with phase convention chosen real.
 mu=np.sqrt(q/2)
 assert 2*sum(mu)<1  # rigorous sufficient trace-norm bound for positivity
 perturb=np.einsum("p,pij->ij",mu,W+W.conj().transpose(0,2,1))
 rho=(np.eye(9)+perturb)/9
 assert np.max(abs(rho-rho.conj().T))<1e-12
 assert abs(np.trace(rho)-1)<1e-12
 assert np.linalg.eigvalsh(rho).min()>0
 assert np.max(abs(powers(rho)-q))<1e-12
 return rho
rho_plus=state_from_q(qplus)
rho_minus=state_from_q(qminus)
qp=powers(rho_plus);qm=powers(rho_minus)
yp=N@qp;ym=N@qm
assert np.max(abs(yp-ym))<1e-12
purp=float(np.trace(rho_plus@rho_plus).real)
purm=float(np.trace(rho_minus@rho_minus).real)
assert abs(purp-purm)<1e-12
assert np.linalg.norm(project_minus@qp-project_minus@qm)>1e-7
assert np.linalg.norm(rho_plus-rho_minus)>1e-8

# Full stabilizer-basis projectors, independently verifying exact collision
# relation for selected lines on the two physical mixed states.
def eigenprojectors(M):
 return [(np.eye(9)+omega**(-j)*M+
          omega**(-2*j)*M@M)/3 for j in range(3)]
collision_proj_checks=[]
for line in (lines[0],lines[17],lines[-1]):
 i,j=line[:2]
 U,V=W[i],W[j]
 assert np.max(abs(U@V-V@U))<1e-12
 P=[a@b for a in eigenprojectors(U) for b in eigenprojectors(V)]
 assert np.max(abs(sum(P)-np.eye(9)))<1e-12
 for rho in (rho_plus,rho_minus):
  probabilities=np.array([np.trace(rho@p).real for p in P])
  assert abs(probabilities.sum()-1)<1e-12
  expected=(1+(N@powers(rho))[lines.index(line)])/9
  err=float(abs(np.sum(probabilities**2)-expected))
  collision_proj_checks.append(err)
  assert err<1e-12

# The OTHER 90 symplectic (non-isotropic) qutrit frames were used in
# TOE41/42. Their purity variance has a quadratic excess over the 40-cusp
# collision variance that is EXACTLY the norm of the 15 dark Fourier modes.
planes=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if not sp(p,q):continue
  pl=frozenset(index[canon(tuple((a*p[k]+b*q[k])%3 for k in range(4)))]
        for a,b in itertools.product(range(3),repeat=2) if a or b)
  assert len(pl)==4
  planes.add(tuple(sorted(pl)))
planes=sorted(planes)
assert len(planes)==90
H=np.zeros((90,40),dtype=np.int64)
for j,pl in enumerate(planes):H[j,list(pl)]=1
assert np.array_equal(H.T@H,8*I+J-A)
def variances(q):
 factor_purity=(1+H@q)/3
 cusp_collision=(1+N@q)/9
 vf=float(np.var(factor_purity))
 vc=float(np.sum((cusp_collision-cusp_collision.mean())**2)/10)
 dark=float((2/135)*np.linalg.norm(project_minus@q)**2)
 assert abs(vf-vc-dark)<5e-15,(vf,vc,dark)
 return vf,vc,dark
z=rng.normal(size=9)+1j*rng.normal(size=9)
z=z/np.linalg.norm(z)
pure_variance=variances(powers(np.outer(z,z.conj())))
assert pure_variance[2]<1e-20

rho_baseline=state_from_q(t*np.ones(40))
qb=powers(rho_baseline)
assert np.max(abs(N@qb-N@qp))<1e-12
assert abs(float(np.trace(rho_baseline@rho_baseline).real)-purp)<1e-12
variance_dark=variances(qp)
variance_baseline=variances(qb)
assert variance_dark[0]>variance_baseline[0]+1e-14
assert abs(variance_dark[1]-variance_baseline[1])<1e-15
assert variance_dark[2]>1e-14
random_mixed_variances=[]
for _ in range(20):
 G=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
 candidate=G@G.conj().T
 candidate/=np.trace(candidate).real
 q=powers(candidate)
 vv=variances(q)
 assert vv[0]>=vv[1]-5e-13
 assert vv[2]>=-1e-20
 random_mixed_variances.append(vv)
assert max(v[2] for v in random_mixed_variances)>1e-6
# All forty cusp probabilities have the same mean (1+state purity)/10,
# including for general mixed states.
for rho in (rho_plus,rho_minus,rho_baseline):
 q=powers(rho);cp=(1+N@q)/9
 assert abs(cp.mean()-(1+np.trace(rho@rho).real)/10)<1e-12

# The general mixed-state line collision reconstruction sees const+lambda2
# but entirely loses Pminus. It does NOT equal q for the two positive states.
def visible_reconstruct(q):
 y=N@q
 mu=float(q.sum()/40)
 return mu*np.ones(40)+(N.T@(y-4*mu))/6
vplus=visible_reconstruct(qp)
vminus=visible_reconstruct(qm)
assert np.max(abs(vplus-vminus))<1e-12
assert np.max(abs(vplus-(qp-project_minus@qp)))<1e-12
assert np.max(abs(vminus-(qm-project_minus@qm)))<1e-12

out={
"status":"PASS_EXACT_W33_CUSP_COLLISION_RECONSTRUCTION_AND_MIXED_DARK_NOGO",
"geometry":{"points":40,"cusps_context_lines":40,"line_size":4,
"incidence_shape":[40,40],"point_valence":4,"line_valence":4,
"gram":"N^T N=4I+A_W33","rank":25,
"singular_values_squared":{"16":1,"6":24,"0":15},
"one_Wilson_point_incident_cusps":4,"nonincident_cusps":36,
"one_nonincident_cusp_commuting_points_with_Wilson":1,
"incident_flag_total":160,"nonincident_pair_total":1440},
"exact_cusp_collision_law":"C_L=sum_outcome_j Pr_L(j)^2=(1+sum_{p in L}q_p)/9",
"pure_reconstruction":"For rho pure: q=1/5 * 1 + (1/6) N^T (9C-1-4/5 * 1).",
"pure_cases":len(pure_cases),"max_pure_reconstruction_error":max(v[0] for v in pure_cases),
"max_pure_minus_sector":max(v[1] for v in pure_cases),
"mixed_reconstruction":"For arbitrary rho: m=(9Trrho²-1)/40; q_visible=m*1 + (N^T(Nq-4m*1))/6=(P_const+P_2)q. All 15 P_-4 dimensions are annihilated by N.",
"cusp_factorization_variance_duality":{"nondegenerate_frame_count":90,
"identity_general":"Var_{90}(P_L) = (1/10) sum_{40 cusps}(C_L-mean(C))^2 + (2/135)||P_-4 q||^2 >= (1/10)sum(C_L-mean(C))^2",
"mean_C_general":"(1+Tr(rho^2))/10","mean_virtual_purity_general":"3*(1+Tr(rho^2))/10",
"pure_equality":"The gap vanishes for every pure two-qutrit rho, regardless of entanglement.",
"dark_mixed_variance":variance_dark[0],
"dark_mixed_cusp_variance":variance_dark[1],
"dark_mixed_predicted_gap":variance_dark[2],
"baseline_same_cusps_mixed_variance":variance_baseline[0],
"pure_example_frame_and_cusp_variance":list(pure_variance),
"random_mixed_cases":len(random_mixed_variances),
"random_mixed_max_dark_variance_gap":max(v[2] for v in random_mixed_variances)},
"positive_counterexample":{"q_baseline":t,"dark_delta_scale":eps,
"rigorous_perturbation_norm_upper_bound":float(2*np.sum(np.sqrt(qplus/2))),
"rigorous_lower_bound_on_rho_eigenvalues":float((1-2*np.sum(np.sqrt(qplus/2)))/9),
"min_eigenvalue_rho_plus":float(np.linalg.eigvalsh(rho_plus).min()),
"min_eigenvalue_rho_baseline":float(np.linalg.eigvalsh(rho_baseline).min()),
"min_eigenvalue_rho_minus":float(np.linalg.eigvalsh(rho_minus).min()),
"purity_rho_plus":purp,"purity_rho_minus":purm,
"max_cusp_collision_difference":float(np.max(abs(yp-ym))/9),
"baseline_vs_dark_max_cusp_collision_difference":float(np.max(abs(N@qp-N@qb))/9),
"dark_sector_difference_norm":float(np.linalg.norm(project_minus@qp-project_minus@qm)),
"density_operator_difference_norm":float(np.linalg.norm(rho_plus-rho_minus)),
"max_full_MUB_projector_collision_check":max(collision_proj_checks)},
"proof_of_existence":"For any sufficiently small strictly positive q, rho=(I+sum_p sqrt(q_p/2)*(W_p+W_p^dag))/9 has exactly Pauli powers q. It is rigorously positive since each W_p is unitary and ||sum mu_p(W_p+W_pdag)|| <= 2 sum mu_p <1; the numeric minimum eigenvalue independently corroborates this. Taking qplus/qminus=t1 +/- epsilon*h with h in ker N generates physical density matrices of equal purity and identical all-context collision observables but different P_minus q.",
"research_credit":"Classical 40x40 point-line incidence singular rank 25 is previously in Pass4952. Pure-sector identity Aq=2q+2 from TOE42. New here is their fusion with Pass11899 40 cusp lines, Pass11900 holonomy point, explicit pure-state reconstruction and a physical two-density-matrix cusp-collision no-go.",
"boundary":"Cusps are algebraically identified with maximal commuting Pauli contexts; the 40 collision statistics are experimentally defined but no actual Kähler cusp is a laboratory measurement apparatus. The theorem applies to Pauli-context collision observables, not full nine-outcome distributions (which contain more information). No inference that a physical TOE has been established."}
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":out["status"],"rank":25,
                  "pure_error":out["max_pure_reconstruction_error"],
                  "mixed":out["positive_counterexample"]}),flush=True)
