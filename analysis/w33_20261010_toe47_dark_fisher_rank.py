"""TOE47: local classical Fisher rank — 40 collisions vs ten full MUB bases."""
from pathlib import Path
import itertools,json
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/"data/w33_20261010_toe47_dark_fisher_information.json"
rng=np.random.default_rng(47004);omega=np.exp(2j*np.pi/3)
I3=np.eye(3,dtype=complex);X=np.roll(I3,1,axis=0);Z=np.diag([1,omega,omega**2])
canon=lambda v:min(v,tuple(-int(x)%3 for x in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
index={p:i for i,p in enumerate(pts)}
sp=lambda p,q:(p[0]*q[2]+p[1]*q[3]-p[2]*q[0]-p[3]*q[1])%3
W=np.stack([np.kron(np.linalg.matrix_power(X,p[0])@np.linalg.matrix_power(Z,p[2]),
                  np.linalg.matrix_power(X,p[1])@np.linalg.matrix_power(Z,p[3])) for p in pts])
lines=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if sp(p,q):continue
  L=tuple(sorted({index[canon(tuple((a*p[j]+b*q[j])%3 for j in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b}))
  lines.add(L)
lines=sorted(lines); assert len(lines)==40
N=np.zeros((40,40),dtype=int)
for i,l in enumerate(lines):N[i,list(l)]=1
A=N.T@N-4*np.eye(40,dtype=int)
Pminus=(A-12*np.eye(40))@(A-2*np.eye(40))/96
assert np.linalg.matrix_rank(N)==25 and np.linalg.matrix_rank(Pminus)==15
# Exactly real coordinates mu_p=x_p+i*y_p (80 independent Hermitian directions).
# rho=(I+sum conj(mu)Wp+mu Wpdag)/9.
tangents=np.stack([(w+w.conj().T)/9 for w in W]+[1j*(w.conj().T-w)/9 for w in W])
assert tangents.shape==(80,9,9)
G=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
rho=G@G.conj().T;rho/=np.trace(rho).real
mu=np.einsum("ab,pba->p",rho,W)
q=2*abs(mu)**2
assert np.min(q)>1e-8
# Explicit 40-line Bernoulli collision FIM via Jacobian in 80 coordinates.
D=np.zeros((40,80))
D[:,:40]=(4/9)*N@np.diag(mu.real)
D[:,40:]=(4/9)*N@np.diag(mu.imag)
cc=(1+N@q)/9
fc=D.T@np.diag(1/(cc*(1-cc)))@D
s=np.linalg.svd(D,compute_uv=False)
rank_collision=int(sum(s>1e-10))
assert rank_collision==25
# Fixed-purity tangent hyperplane strips off one row-space direction.
purity_derivative=4*np.r_[mu.real,mu.imag]
# Build a full MUB spread with 10 lines covering all 40 Pauli classes.
masks=[sum(1<<i for i in l) for l in lines]
at={p:[j for j,l in enumerate(lines) if p in l] for p in range(40)}
def spread(covered,selected):
 if covered==(1<<40)-1:return selected
 p=next(i for i in range(40) if not (covered>>i)&1)
 for j in at[p]:
  if masks[j]&covered:continue
  x=spread(covered|masks[j],selected+[j])
  if x is not None:return x
 return None
chosen=spread(0,[])
assert chosen and len(chosen)==10
def proj3(w):
 return [(np.eye(9)+omega**(-i)*w+omega**(-2*i)*w@w)/3 for i in range(3)]
proj=[]
for j in chosen:
 a,b=lines[j][:2]
 assert np.max(abs(W[a]@W[b]-W[b]@W[a]))<1e-12
 prod=np.array([u@v for u in proj3(W[a]) for v in proj3(W[b])])
 assert max(abs(prod.sum(axis=0)-np.eye(9)).ravel())<1e-12
 proj.extend(prod)
proj=np.array(proj)
p=np.einsum("ab,jba->j",rho,proj).real
assert p.min()>0 and abs(sum(p)-10)<1e-12
J=np.einsum("kab,jba->jk",tangents,proj).real
# Each setting has 9 independent probabilities summing 1, rank8.
assert np.max(abs(J.reshape(10,9,80).sum(axis=1)))<1e-12
FMUB=J.T@np.diag(1/p)@J
sing=np.linalg.svd(J,compute_uv=False)
full_rank=int(sum(sing>1e-9))
assert full_rank==80
# A smooth physical dark direction preserving q phase corresponds to
# dmu= h/(4 q) * mu, since dq=4 Re(conj(mu)dmu).
h=Pminus@np.arange(1,41,dtype=float);h/=np.linalg.norm(h)
dmu=h*mu/(2*q)  # dq=4 Re(conj(mu)*dmu)=h
v=np.r_[dmu.real,dmu.imag]
assert np.linalg.norm(D@v)<1e-10
assert abs(purity_derivative@v)<1e-10
score_full=J@v
assert np.linalg.norm(score_full)>1e-5
fisher_full=float(v@FMUB@v)
fisher_collision=float(v@fc@v)
assert fisher_full>1e-6 and abs(fisher_collision)<1e-9
# Phase-only local changes are also invisible to all q, dimension40.
out={"status":"EXACT_W33_40_COLLISION_FISHER_RANK25_VS_10_MUB_RANK80",
"state":{"min_eigenvalue":float(np.linalg.eigvalsh(rho).min()),"min_pauli_power":float(q.min())},
"real_density_parameter_count":80,
"collision_scalar_count":40,"collision_fisher_rank":rank_collision,
"collision_fisher_nullity":80-rank_collision,
"full_MUB_basis_count":10,"full_MUB_projector_outcomes":90,
"full_MUB_fisher_rank":full_rank,"full_MUB_fisher_nullity":80-full_rank,
"one_dark_fixed_purity_direction":{"collision_Fisher_quadratic":fisher_collision,"full_MUB_Fisher_quadratic":fisher_full,
"collision_score_norm":float(np.linalg.norm(D@v)),"full_MUB_score_norm":float(np.linalg.norm(score_full)),
"purity_tangent_derivative":float(purity_derivative@v)},
"proof":"At generic full-rank rho with nonzero Weyl expectations, dC=(1/9)N dq, dq=4(x dx+y dy) for each Pauli; thus collision Jacobian rank rank N=25, leaves 55 invisible real state dimensions (40 phases + 15 dark powers). Ten complete MUB bases form informationally complete projective 2-design: their probabilities span 80 real density directions; J rank80; explicit Fisher calculation confirms.",
"boundary":"Fisher rank concerns local identifiability and ideal repeated independent preparations, not channel QFI, optimum POVMs, finite sample confidence intervals or actual optics. Rank drops at special zero-expectation and rank-deficient states."}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"coll_rank":rank_collision,"full_rank":full_rank,"dark":out["one_dark_fixed_purity_direction"]}))
