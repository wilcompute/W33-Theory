"""TOE46: generic physical dark fibers and an unbiased ten-MUB quartic gap assay.

All computational claims have fixed RNG seed and frozen small JSON; the
operator identities are exact up to double precision. No optical hardware claim.
"""
import json,itertools
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe46_dark_and_mub_quartic.json"
rng=np.random.default_rng(46160)
omega=np.exp(2j*np.pi/3)
I3=np.eye(3,dtype=complex)
X=np.roll(I3,1,axis=0)
Z=np.diag([1,omega,omega**2])
canon=lambda v:min(v,tuple(-x%3 for x in v))
pts=sorted({canon(x) for x in itertools.product(range(3),repeat=4) if any(x)})
idx={v:i for i,v in enumerate(pts)}
sp=lambda u,v:(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
A=np.array([[int(i!=j and sp(p,q)==0) for j,q in enumerate(pts)] for i,p in enumerate(pts)])
I40=np.eye(40)
Pm=(A-12*I40)@(A-2*I40)/96.
P2=(A-12*I40)@(A+4*I40)/(-60.)
assert np.linalg.matrix_rank(Pm)==15 and np.linalg.matrix_rank(P2)==24
W=np.stack([np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3])) for v in pts])
lines=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if sp(p,q):continue
  lines.add(tuple(sorted({idx[canon(tuple((a*p[k]+b*q[k])%3 for k in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b})))
lines=sorted(lines)
assert len(lines)==40
N=np.zeros((40,40),dtype=int)
for j,line in enumerate(lines):N[j,list(line)]=1
assert np.array_equal(N.T@N,4*np.eye(40,dtype=int)+A)
def expvec(rho):
 return np.einsum("ij,pji->p",rho,W)
def rhofrom(mu):
 return (np.eye(9)+np.einsum("p,pij->ij",mu.conj(),W)+np.einsum("p,pij->ij",mu,W.conj().transpose(0,2,1)))/9
def qfrom(rho):return 2*abs(expvec(rho))**2
def newrho(q,phase):
 return rhofrom(phase*np.sqrt(q/2))
G=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
rho=G@G.conj().T;rho/=np.trace(rho).real
q=qfrom(rho);mu=expvec(rho);phase=mu/abs(mu)
assert np.min(q)>0 and np.linalg.eigvalsh(rho).min()>0
assert np.max(abs(rhofrom(mu)-rho))<1e-13
assert np.linalg.matrix_rank(Pm)>0
h=Pm@np.arange(1,41,dtype=float);h/=max(abs(h))
assert np.max(abs(N@h))<1e-12
# Bound the Hermitian operator displacement using the triangle inequality.
# dmu <= |delta q|/(2sqrt(2*(q-|delta q|))) for each coordinate.
eps=min(.05*np.min(q), 1e-7)
assert eps>0
drbound=(2/9)*sum(eps/(2*np.sqrt(2*(q-eps))))
assert drbound<np.linalg.eigvalsh(rho).min()
rp=newrho(q+eps*h,phase);rm=newrho(q-eps*h,phase)
for r in (rp,rm):
 assert np.linalg.eigvalsh(r).min()>0
 assert abs(np.trace(r)-1)<1e-12
assert np.max(abs(qfrom(rp)-(q+eps*h)))<1e-12
assert np.max(abs(qfrom(rm)-(q-eps*h)))<1e-12
assert np.max(abs(N@(qfrom(rp)-qfrom(rm))))<1e-11
assert abs(np.trace(rp@rp).real-np.trace(rm@rm).real)<1e-12
assert np.linalg.norm(Pm@(qfrom(rp)-qfrom(rm)))>0
# Exact context spread, 10 bases covering all 40 Pauli powers
masks=[sum(1<<j for j in line) for line in lines]
pointlines={p:[i for i,L in enumerate(lines) if p in L] for p in range(40)}
def search(occupied,sel):
 if occupied==(1<<40)-1:return sel
 p=next(i for i in range(40) if not occupied>>i&1)
 for l in pointlines[p]:
  if masks[l]&occupied:continue
  found=search(occupied|masks[l],sel+[l])
  if found is not None:return found
 return None
sel=search(0,[])
assert len(sel)==10 and sorted(x for l in sel for x in lines[l])==list(range(40))
def eigenproj(M):
 return np.stack([(np.eye(9)+omega**(-j)*M+omega**(-2*j)*(M@M))/3 for j in range(3)])
settings=[]
for li in sel:
 line=lines[li];i,j=line[:2]
 projs=np.stack([u@v for u in eigenproj(W[i]) for v in eigenproj(W[j])])
 assert max(abs(np.sum(projs,axis=0)-np.eye(9)).ravel())<1e-12
 L=np.stack([np.trace(P@W[p]) for p in line for P in projs]).reshape(4,9)
 assert np.max(abs(abs(L)-1))<1e-12
 settings.append((li,line,projs,L))
# A four-split estimator qAB and qCD is unbiased for q; their cross-product
# estimates a quartic function of rho without using a shot twice.
# Four blocks of n samples in each of 10 MUBs, total 40n state preps.
n=960
trials=160
def simulate(rho):
 trueq=qfrom(rho)
 truegap=float((2/135)*np.linalg.norm(Pm@trueq)**2)
 runs=[]
 for _ in range(trials):
  estimates=np.zeros((4,40),dtype=complex)
  for li,line,P,L in settings:
   prob=np.real(np.einsum("ij,pji->p",rho,P))
   prob/=prob.sum()
   outcomes=rng.choice(9,size=(4,n),p=prob)
   ev=np.stack([L[:,outcomes[b]].mean(axis=1) for b in range(4)])
   estimates[:,list(line)]=ev
  qab=2*np.real(estimates[0]*estimates[1].conj())
  qcd=2*np.real(estimates[2]*estimates[3].conj())
  guess=float((2/135)*np.dot(Pm@qab,Pm@qcd))
  runs.append(guess)
 runs=np.array(runs)
 return dict(true_gap=truegap,estimate_mean=float(runs.mean()),
  standard_error_of_MC_mean=float(runs.std(ddof=1)/np.sqrt(trials)),
  sample_standard_deviation=float(runs.std(ddof=1)),
  fraction_estimates_negative=float(np.mean(runs<0)))
# Pure random and mixed Wishart; off-null variance more detectable than tiny small-q.
psi=rng.normal(size=9)+1j*rng.normal(size=9);psi/=np.linalg.norm(psi)
pure=np.outer(psi,psi.conj())
mix=simulate(rho)
pure_res=simulate(pure)
assert pure_res["true_gap"]<1e-24
for val in (mix,pure_res):
 err=abs(val["estimate_mean"]-val["true_gap"])
 assert err<5*val["standard_error_of_MC_mean"]+1e-7,(err,val)
payload={
 "status":"EXACT_LOCAL_15D_DARK_FIBER_AND_UNBIASED_TEN_MUB_GAP_ESTIMATOR",
 "full_rank_state_min_eigen":float(np.linalg.eigvalsh(rho).min()),
 "min_pauli_power":float(min(q)),"dark_sector_dimension":int(np.linalg.matrix_rank(Pm)),
 "local_physical_fiber_dimension":"at least 15 independent Pauli-power perturbations around ANY positive-definite rho with all q_p>0; the Weyl inverse rho(mu) stays positive by openness",
 "analytic_perturbation_upper_bound":float(drbound),"chosen_power_epsilon":float(eps),
 "physical_plus_min_eigen":float(np.linalg.eigvalsh(rp).min()),
 "physical_minus_min_eigen":float(np.linalg.eigvalsh(rm).min()),
 "same_purity_abs_difference":float(abs(np.trace(rp@rp)-np.trace(rm@rm))),
 "same_cusp_max_difference":float(max(abs(N@(qfrom(rp)-qfrom(rm))))/9),
 "different_density_frobenius":float(np.linalg.norm(rp-rm)),
 "measurement":{"settings":10,"distinct_context_lines":sel,"four_independent_blocks":4,
  "shots_per_basis_per_block":n,"prepared_copies_per_trial":40*n,
  "trials":trials,"formula":"qab_p=2 Re(muA_p conj(muB_p)); qcd similarly; ghat=(2/135) (P-4 qab) dot (P-4 qcd). E ghat=g exactly assuming independent ideal identically prepared copies. Negative estimates allowed."},
 "random_mixed_Wishart":mix,"random_pure_Haar":pure_res,
 "scientific_boundary":"Full 15D fiber applies to strictly full-rank rho with every Pauli expectation nonzero, not every boundary/low-rank state. Ten MUB implementation is ideal; readout bias, shot correlations, optical implementation and confidence guarantees are untested. Mixedness witness gap is one-sided and zero for some mixed states."
}
OUT.write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps({"status":payload["status"],"mixed":mix,"pure":pure_res,
"physical_fiber":payload["different_density_frobenius"]}))
