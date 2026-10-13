"""TOE56 bonus physical vacuum test: 3 native H1 holonomies and bosonic logdet.

Exact diamagnetic closed-walk proof bounds bosonic Gaussian determinant
below by zero-holonomy. Not a generic SM vacuum theorem.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
edges=np.array(ed,dtype=int)
deg=np.bincount(edges.ravel(),minlength=80)
assert np.unique(deg).tolist()==[4]
P=np.rint(np.array([cycle_row(z,ed,volts,look,np.zeros(3)) for z in octs+comm]).real)
B=np.rint(gradient(ed,volts,np.zeros(3)).real)
ev,H=np.linalg.eigh(P.T@P+B@B.T)
assert sum(ev<1e-7)==3
basis=H[:,:3]
g=.43;kappa=.7;mass2=.8
def matter_matrix(A):
 # 80-site single complex Gaussian scalar, positive kinetic Laplacian
 D=np.zeros((160,80),dtype=complex)
 ix=np.arange(160)
 D[ix,edges[:,0]]=-np.exp(1j*g*A)
 D[ix,edges[:,1]]=1
 return mass2*np.eye(80)+kappa*(D.conj().T@D)
def logdet(A):
 K=matter_matrix(A)
 sign,ld=np.linalg.slogdet(K)
 assert abs(sign-1)<1e-10
 return float(ld.real)
base=logdet(np.zeros(160))
rng=np.random.default_rng(560912)
tests=[]
for t in [[.8,0,0],[0,.8,0],[0,0,.8],[.7,-.6,.4],
          *[x.tolist() for x in rng.normal(size=(28,3))]]:
 A=basis@np.array(t)
 pos=logdet(A)-base
 anti=logdet(-A)-base
 assert pos>-1e-9,(t,pos)
 assert abs(pos-anti)<1e-9
 tests.append({"t":t,"free_energy_minus_zero":pos})
chi=rng.normal(size=80)
gauge_error=abs(logdet(A+B@chi/g)-logdet(A))
assert gauge_error<1e-9
# finite diff Hessian of scalar 1loop logdet on H1.
eps=.15;V=np.eye(3);Hess=np.zeros((3,3))
for a in range(3):
 x=V[a]
 Hess[a,a]=(logdet(basis@(eps*x))+logdet(basis@(-eps*x))-2*base)/(eps*eps)
 for b in range(a+1,3):
  y=V[b]
  fpp=logdet(basis@(eps*x+eps*y))
  fpm=logdet(basis@(eps*x-eps*y))
  fmp=logdet(basis@(-eps*x+eps*y))
  fmm=logdet(basis@(-eps*x-eps*y))
  Hess[a,b]=Hess[b,a]=(fpp-fpm-fmp+fmm)/(4*eps**2)
eig=np.linalg.eigvalsh(Hess)
assert eig.min()>1e-6,(eig,Hess)
# Exact proof for arbitrary compact phases on this 4-regular graph:
# K(A)=(m²+4κ)I-κ T(A). The Hermitian adjacency T(A) has
# |Tr T(A)^n|<=Tr T(0)^n termwise by closed-walk phases and
# tr T(A)^n <= tr T(0)^n. Since κ*||T||/(m²+4κ) < 1, the
# logdet series converges:
# logdet K(A)-logdet K(0)
#  =Σ_{n>=1} κ^n/[n(m²+4κ)^n] (TrT(0)^n-TrT(A)^n)>=0.
degree=4
rho_upper=kappa*degree/(mass2+kappa*degree)
assert rho_upper<1
out={"status":"PASS_TOE56_BOSONIC_ONE_LOOP_HOLONOMY_NO_SPONTANEOUS_CP",
"native_graph":{"vertices":80,"oriented_edges":160,"regular_degree":4,"harmonic_U1_flat_connections":3},
"scalar_parameters":{"g":g,"kappa":kappa,"positive_mass_squared":mass2},
"one_loop_free_energy":"F_B(A)=log det[m² I+κ D_A† D_A], with oriented D_A e=(z_b-exp(i g A_e)z_a). This is a one complex Gaussian bosonic scalar determinant, NOT the full gauge+fermion effective action.",
"exact_global_theorem":"For 4-regular graph, K(A)=(m²+4κ)I−κ T(A). With positive m², κ, the absolutely convergent -log series and closed-walk phase bound Tr T(A)^n<=Tr T(0)^n imply F_B(A)>=F_B(0) for EVERY compact link connection A. Every closed walk contributes cos(phase)<=1; no boson-only Gaussian holonomy can lower the free energy below trivial holonomy.",
"convergence_ratio_upper_bound":rho_upper,
"zero_holonomy_free_energy":base,
"sampled_holonomy_cases":tests,
"minimum_sampled_energy_difference":min(x["free_energy_minus_zero"] for x in tests),
"maximum_CP_reversal_deviation":max(abs(logdet(basis@np.array(x["t"]))-logdet(-basis@np.array(x["t"]))) for x in tests),
"local_harmonic_Hessian":Hess.tolist(),
"local_harmonic_Hessian_eigenvalues":eig.tolist(),
"gauge_transform_logdet_residual":gauge_error,
"negative_conclusion":"A single positive-mass minimally coupled Gaussian complex scalar on the exact W33 4-regular 80-site cover CANNOT spontaneously prefer a nontrivial H1 holonomy over A=0, even though three harmonic U1 modes exist. This rules out a proposed simple boson-only quantum vacuum-selection mechanism; chiral fermions, competing interactions or other dynamical sectors would be needed. Does NOT exclude CP breaking in realistic models.",
"prior_art":"Discrete diamagnetic inequality and closed-walk log-determinant expansion are standard spectral-graph/magnetic Schrödinger results; applying them to this W33 cover is a model-specific negative control."}
(R/"data/w33_20261013_toe56_holonomy_scalar_one_loop.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"min_hessian":float(eig.min()),"min_sampled":out["minimum_sampled_energy_difference"],"max_gauge_err":gauge_error}))
