"""TOE41: gauge-covariant overlap Dirac on *native* W33 Levi graph.

Build a local graph Wilson-type kernel from 40x40 gauged incidence M,
with same-sublattice two-hop regulator r M M^dagger and r M^dagger M.
Prove exact spectral pairing and zero index for all U(1) link gauges,
even though finite Ginsparg-Wilson symmetry is exact. This is an
obstruction specific to this symmetric bipartite regulator, not a
no-go for every possible W33 construction.
"""
import sys,json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/"data/w33_20261010_toe41_w33_overlap_index_obstruction.json"
ed,*_=wilson()
assert len(ed)==160 and all(0<=a<40<=b<80 for a,b in ed)
gam=np.diag(np.r_[np.ones(40),-np.ones(40)])
def kernel(M,r=.1,m=1.2):
 Kp=M@M.conj().T;Kl=M.conj().T@M
 top=r*Kp-m*np.eye(40);bottom=-r*Kl+m*np.eye(40)
 return np.block([[top,M],[M.conj().T,bottom]])
def overlap(M):
 H=kernel(M)
 lam,U=np.linalg.eigh(H)
 assert min(abs(lam))>1e-6
 sign=(U*np.sign(lam))@U.conj().T
 D=np.eye(80)+gam@sign
 gw=gam@D+D@gam-D@gam@D
 return dict(min_spectral_gap=float(min(abs(lam))),
   plus=int(sum(lam>0)),minus=int(sum(lam<0)),index=int(round(-.5*sum(np.sign(lam)))),
   gw_defect=float(np.max(abs(gw))),index_formula=float(-.5*sum(np.sign(lam)))),D
def matrix(phases):
 M=np.zeros((40,40),dtype=complex)
 for (a,b),phase in zip(ed,phases):M[a,b-40]=np.exp(1j*phase)
 return M
rng=np.random.default_rng(411)
M=matrix(np.zeros(160))
flat,D0=overlap(M)
assert flat["index"]==0 and flat["plus"]==flat["minus"]==40
random_M=matrix(rng.uniform(-np.pi,np.pi,160))
random_o,D=overlap(random_M)
assert random_o["index"]==0
# Gauge covariance under arbitrary U(1) site phases.
angles=rng.uniform(-np.pi,np.pi,80)
Gp=np.exp(1j*angles[:40]);Gl=np.exp(1j*angles[40:])
gauge_M=Gp[:,None]*random_M*Gl.conj()[None,:]
gauge_o,Dg=overlap(gauge_M)
G=np.diag(np.r_[Gp,Gl])
gauge_defect=float(np.max(abs(Dg-G@D@G.conj().T)))
assert gauge_defect<1e-10
assert flat["gw_defect"]<1e-10 and random_o["gw_defect"]<1e-10
# Analytic block-pair proof: each singular value s of M spans
# [[r*s²-m,s],[s,-r*s²+m]], eigenvalues +/- sqrt((r*s²-m)²+s²).
sv=np.linalg.svd(random_M,compute_uv=False)
predicted=np.sort(np.r_[-np.sqrt((.1*sv**2-1.2)**2+sv**2),
                           np.sqrt((.1*sv**2-1.2)**2+sv**2)])
actual=np.linalg.eigvalsh(kernel(random_M))
pairing_defect=float(max(abs(actual-predicted)))
assert pairing_defect<1e-10
out=dict(status="PASS_ZERO_INDEX_FOR_THIS_KERNEL",vertices=80,edges=160,
         full_gauge_covariance_defect=gauge_defect,spectral_pairing_defect=pairing_defect,
         zero_gauge=flat,random_link_phases=random_o,gauge_transformed=gauge_o,
         analytic_theorem="Under SVD M=U S V^dag, H=[r MM^dag-mI,M; M^dag,-r M^dag M+mI] decomposes into 40 traceless Hermitian 2x2 blocks with eigenvalues +/-sqrt((r s^2-m)^2+s^2). Hence Tr sign H=0 for every gauged M, so index(Dov)=-.5Tr sign(H)=0.",
         boundary="Native W33 Levi graph and local two-hop Wilson-style regulator. This is not a 4D anomaly-free continuum chiral construction or a theorem ruling out other regulators/topologies.")
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
