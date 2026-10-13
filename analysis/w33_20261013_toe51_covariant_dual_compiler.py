"""TOE51 front 4: seven-generator Sp4(3)-covariant 1+24+15 decoder.

Covariance is for the W33 line module. Holotrade K81 only has
an explicitly supplied H27 x C3 action, NOT a Sp4(3) intertwiner.
"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
import w33_20261013_toe50_dual_cusp_spread_decoder as prev
B=prev.B;G=prev.G;A=prev.A;L=prev.lines
point=prev.x["P"];pidx=prev.x["ix"];canon=prev.x["canon"];sym=prev.x["sym"]
lidx={tuple(x):i for i,x in enumerate(L)}
spridx={tuple(x):i for i,x in enumerate(prev.spreads)}
I=np.eye(40);J=np.ones((40,40));P0=J/40
P24=.75*(G-8*P0);P15=(B@B.T-90*P0)/18
assert max(abs(P0@P24).ravel())<1e-10
assert max(abs(P0@P15).ravel())<1e-10
assert max(abs(P24@P15).ravel())<1e-10
assert max(abs(P0+P24+P15-I).ravel())<1e-10
def matrix(name):
 M=sym[name];perm=np.zeros((40,40),int)
 for i,line in enumerate(L):
  mapped=tuple(sorted(pidx[canon(tuple((M@np.array(point[p]))%3))] for p in line))
  perm[lidx[mapped],i]=1
 assert np.all(perm.sum(0)==1) and np.all(perm.sum(1)==1)
 sp=np.zeros((36,36),int)
 for j,s in enumerate(prev.spreads):
  mapped=tuple(sorted(np.flatnonzero(perm[:,li])[0] for li in s))
  sp[spridx[mapped],j]=1
 assert np.array_equal(perm@B,B@sp)
 return perm,sp
checks={}
for name in sym:
 perm,ps=matrix(name)
 checks[name]=float(max(np.max(abs(perm@Z@perm.T-Z)) for Z in (P0,P24,P15,G)))
 assert checks[name]<1e-10
rng=np.random.default_rng(51004)
errs=[];cov=[]
for _ in range(40):
 y=rng.normal(size=40)
 for name in list(sym)[:2]:
  perm,sp=matrix(name)
  a=G@y
  b=B.T@y
  decoded=.75*a+B@b/18-y.sum()/4
  trans=.75*(G@(perm@y))+B@(sp@b)/18-y.sum()/4
  errs.append(float(max(abs(decoded-y))))
  cov.append(float(max(abs(trans-perm@decoded))))
assert max(cov)<1e-10
# Linear storage proof only: 40 orthonormal coordinate rails in C81,
# NO K81 group representation on those rails has been constructed.
E=np.eye(81)[:,:40]
assert np.allclose(E.T@E,np.eye(40))
sigma=.001
# Independent Gaussian noise on forty cusp readings and 36 spread
# readings, with global y-sum supplied EXACTLY.
noises=[]
for _ in range(1500):
 eta=rng.normal(0,sigma,40);zeta=rng.normal(0,sigma,36)
 q=.75*eta+B@zeta/18
 noises.append(float(q@q))
pred=sigma**2*(40*(.75**2)+np.trace(B@B.T)/18**2)
assert abs(np.mean(noises)/pred-1)<.15
out=dict(status="PASS",front="Sp4_covariant_dual_C40_decoder",
 exact_projector_decomposition="I40=P0+P24+P15 ranks 1,24,15; P0=J/40 P24=3/4(G-8P0) P15=(BBt-90P0)/18",
 n_checked_Sp4_generator_actions=len(checks),projector_commutator_errors=checks,
 n_random_covariance_checks=len(cov),max_covariance_error=max(cov),
 max_signal_reconstruction_error=max(errs),
 gaussian_sigma=sigma,simulated_mean_squared_l2_noise=float(np.mean(noises)),
 analytic_mean_squared_l2_noise=float(pred),
 noise_formula="E||delta y||²=σ²[(3/4)²*40+Tr(BBt)/18²] when all 76 channel noises independent, equal σ, and global sum known perfectly; no physical detector calibration is assumed",
 linear_storage_dimension_K81=81,real_line_signal_dimension=40,
 physical_K81_intertwiner_status="NOT CONSTRUCTED: embedding y->(y,0_41) is an isometric 81-coordinate storage map but Holotrade only supplies K81 regular H27xC3 action; no matching Sp4(3) action or compatible intertwiner on those K81 rails was specified. A dimension inequality 40<=81 is not an equivariance proof.",
 model_scope="Seven symplectic generators checked, finite real W33 line module, exact integer incidence and complex projective cusp geometry, not a compiled experiment.")
(R/"data/w33_20261013_toe51_covariant_dual_compiler.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"gens":len(checks),"max_cov":max(cov),"noise_empirical":np.mean(noises),"noise_theory":pred}))
