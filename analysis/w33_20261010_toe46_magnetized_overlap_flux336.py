"""TOE46: full normalized flux-(3,3,-6) torus overlap benchmark.

Unit square coords z=x+tau*y, tau=i*T, A set to one.
The L2-normalized zero modes are Jacobi-theta Gaussian sums.
No Wilson line; valid for same background mode families.
"""
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe46_magnetized_overlap_flux336.json"
T=1.45
GRID=144
x,y=np.meshgrid(np.arange(GRID)/GRID,np.arange(GRID)/GRID,indexing="xy")
def psi(M,j):
 result=np.zeros_like(x,dtype=complex)
 for nn in range(-8,9):
  k=nn+j/M
  exponent=-np.pi*M*T*(k+y)**2+2j*np.pi*M*k*x
  result+=np.exp(exponent)
 return (2*M*T)**.25 * result * np.exp(1j*np.pi*M*x*y)
P3=np.array([psi(3,j) for j in range(3)])
P6=np.array([psi(6,k) for k in range(6)])
def inner(v,w):return np.mean(v.conj()*w)
G3=np.array([[inner(a,b) for b in P3] for a in P3])
G6=np.array([[inner(a,b) for b in P6] for a in P6])
assert np.max(abs(G3-np.eye(3)))<3e-5
assert np.max(abs(G6-np.eye(6)))<3e-5
Y=np.einsum("ixy,jxy,kxy->kij",P3,P3,P6.conj(),optimize=True)/(GRID*GRID)
# 3+3 -> 6 flux conservation and common magnetic translation:
# i+j = k (mod gcd(3,3,6)=3).
out_of_rule=max(abs(Y[k,i,j]) for k,i,j in itertools.product(range(6),range(3),range(3)) if (i+j-k)%3)
in_rule=min(abs(Y[k,i,j]) for k,i,j in itertools.product(range(6),range(3),range(3)) if (i+j-k)%3==0)
assert out_of_rule<1e-9 and in_rule>1e-6,(out_of_rule,in_rule)
assert np.max(abs(Y-Y.transpose(0,2,1)))<1e-12
def oneH(k):
 M=Y[k]
 h=M@M.conj().T
 sing=np.linalg.svd(M,compute_uv=False)
 off=h-np.diag(np.diag(h))
 assert np.max(abs(off))<1e-12
 assert min(abs(sing[0]-sing[1]),abs(sing[1]-sing[2]))<1e-10,(k,sing)
 return dict(higgs_index=k,nonzero_entries=[[i,j] for i in range(3) for j in range(3) if abs(M[i,j])>1e-5],
  normalized_singular_values=[float(a/max(sing)) for a in sing],
  singular_values=[float(a) for a in sing],
  YYdag_offdiagonal_max=float(np.max(abs(off))))
single=[oneH(k) for k in range(6)]
# Two Higgs condensates with coefficients changing the allowed families
# give an honest mixing LEVER; no claim to fit physical CKM from one torus.
Mu=Y[0]+(.4+0.2j)*Y[1]
Md=Y[2]+(-.2+.7j)*Y[4]
Hu=Mu@Mu.conj().T;Hd=Md@Md.conj().T
Ccomm=Hu@Hd-Hd@Hu
comm=np.linalg.norm(Ccomm)
cp_odd=float(np.imag(np.trace(Ccomm@Ccomm@Ccomm)))
eigU,Vu=np.linalg.eigh(Hu);eigD,Vd=np.linalg.eigh(Hd)
mix=np.abs(Vu.conj().T@Vd)
assert comm>1e-5
assert max(abs(mix-np.eye(3)).ravel())>.01
# Independent mode functions: if left and right share the same Gaussian
# family background, the k-fixed Yukawa is symmetric (Y_ij=Y_ji).
# This is why one localised Higgs is locked at two equal singular values.
data={"status":"FLUX336_NORMALIZED_OVERLAP_SELECTION_AND_SINGLE_HIGGS_DOUBLE_DEGENERACY",
 "flux_numbers":{"I_ab":3,"I_bc":3,"I_ca":-6,"gcd":3},
 "tau_im":T,"torus_coordinate_grid":GRID,"truncation_nmax":8,
 "max_L2_orthonormality_error_M3":float(np.max(abs(G3-np.eye(3)))),
 "max_L2_orthonormality_error_M6":float(np.max(abs(G6-np.eye(6)))),
 "max_forbidden_overlap":float(out_of_rule),"min_allowed_overlap":float(in_rule),
 "selection":"i+j-k = 0 mod 3 (with equal left/right Gaussian wavefunction background)",
 "all_six_fixed_Higgs_rows":single,
 "independent_two_Higgs_example":{"mass_matrix_commutator_norm":float(comm),
 "imag_trace_of_commutator_cubed":cp_odd,
 "absolute_mixing_matrix":mix.tolist(),"up_squared_masses":eigU.tolist(),
 "down_squared_masses":eigD.tolist()},
 "theorem":"For Iab=Ibc=3, Ica=-6 and identical left/right zero-mode backgrounds, each fixed Higgs index k has Y_ij=Y_ji and support i+j=k mod3. Thus Y_k is a 3x3 monomial reflection permutation matrix with a 2x2 transposition block; two nonzero singular values are exactly equal for ANY such symmetric overlaps. The third can differ. Every single-Higgs YY^dagger is diagonal, hence if up/down each use one fixed k, their left handed mass metrics commute and CKM mixing is zero up to mass degeneracies.",
 "limitation":"Minimal flux benchmark, NOT an actual anomaly-free Standard Model; identical left and right magnetic backgrounds and one Higgs zero mode are restrictive. Relative Wilson lines, distinct flux patterns, multi-Higgs mixing, warped metrics and full superpotential can break the degeneracy. Continuum grid is a numerical integration with checked convergence/selection, not a globally normalized string Yukawa matrix including all sectors."}
OUT.write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps({k:data[k] for k in ("status","max_L2_orthonormality_error_M3","max_forbidden_overlap","min_allowed_overlap","independent_two_Higgs_example")}))
