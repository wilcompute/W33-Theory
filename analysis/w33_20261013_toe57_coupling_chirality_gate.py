"""TOE57 fifth front: bare-coupling/energy-unit nonidentifiability,
quantum rotor spectrum scaling, and honest 3+1D chirality gate.

Same two overlapping W33 loops from front1. Exact identity
H(g,beta)=g² H(1,beta/g^4) for equal native electric weights.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,lookup,octs,comm,*_=prep()
edges=np.asarray(ed,dtype=int)
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(int)
P=np.rint(np.asarray([cycle_row(c,ed,volts,lookup,np.zeros(3)) for c in octs+comm]).real).astype(int)
prior=json.loads((R/"data/w33_20261013_toe57_two_plaquette_quantum.json").read_text())
j=prior["selected_native_plaquette_rows"][1];c0=P[0];c1=P[j]
assert (c0@c1)==-4
N=4;grid=range(-N,N+1);st=[(a,b) for a in grid for b in grid];ids={x:i for i,x in enumerate(st)}
flux=np.asarray([a*c0+b*c1 for a,b in st])
D=np.sum(flux*flux,axis=1)
L=np.zeros((len(st),len(st)),dtype=float)
for idx,(a,b) in enumerate(st):
 for pair in ((a+1,b),(a,b+1)):
  if pair in ids:L[idx,ids[pair]]=L[ids[pair],idx]=-.5
mag=2*np.eye(len(st))+L
def matrix(g,beta):
 return g*g*np.diag(D/2)+beta/(g*g)*mag
lmbda=16.
couplings=[(.5,lmbda*.5**4),(1.,lmbda),(1.5,lmbda*1.5**4)]
base=matrix(1.,lmbda)
groups=[]
for g,beta in couplings:
 H=matrix(g,beta)
 assert np.max(abs(H/g**2-base))<1e-10
 spectrum=np.linalg.eigvalsh(H)
 e=spectrum/g**2
 b=np.linalg.eigvalsh(base)
 assert np.max(abs(e[:10]-b[:10]))<1e-9
 ratios=((spectrum[:5]-spectrum[0])/(spectrum[1]-spectrum[0])).tolist()
 groups.append({"g":g,"beta":beta,"lambda_beta_over_g_fourth":beta/g**4,
   "lowest_5_scaled_eigenvalues":e[:5].tolist(),
   "first_5_gaps_over_first_gap":ratios,
   "ground_energy_unscaled":float(spectrum[0])})
assert max(abs(groups[i]["first_5_gaps_over_first_gap"][k]-
               groups[0]["first_5_gaps_over_first_gap"][k])
    for i in range(3) for k in range(5))<1e-9
# Native site-fermion nearest-neighbor Hamiltonian has 40+40 Levi
# bipartition (40 original vertices,40 contexts), no 4D gamma algebra.
deg=np.bincount(edges.ravel(),minlength=80)
assert len(deg)==80 and np.all(deg==4)
# find 2-color classes using BFS rather than assuming stored vertex labels.
adj=[[] for _ in range(80)]
for a,b in edges:adj[a].append(b);adj[b].append(a)
colors={0:0};front=[0]
for u in front:
 for v in adj[u]:
  if v not in colors:colors[v]=1-colors[u];front.append(v)
  else:assert colors[v]!=colors[u]
assert len(colors)==80
sizes=[sum(c==j for c in colors.values()) for j in (0,1)]
assert sizes==[40,40]
T=np.zeros((80,80))
for a,b in edges:T[a,b]=T[b,a]=-1
gamma=np.diag([1 if colors[i]==0 else -1 for i in range(80)])
assert np.max(abs(gamma@T+T@gamma))==0
eig=np.linalg.eigvalsh(T)
assert np.max(abs(eig+eig[::-1]))<1e-10
# Balanced site-fermion sublattice grading has INDEX ZERO regardless
# of gauge link phases, independently of the other rectangular -80.
out={"status":"PASS_TOE57_ROTOR_PARAMETER_SCALE_DEGENERACY_CHIRALITY_GATE",
"two_native_plaquette_rows":[0,j],"flux_truncation_range":N,
"exact_spectral_scaling":"For fixed electric weights (here 1), no matter and native 2-plaquette flux basis, H(g,beta)=g² D/2+(beta/g²) M = g²[D/2+(beta/g^4)M]. Along beta/g^4=lambda, all eigenvalue ratios and normalized eigenvectors are identical for all positive g; absolute energies scale as g². Without an independently determined magnetic beta and physical energy normalization, quantum flux spectral ratios do not identify g or alpha.",
"coupling_groups":groups,"near_exact_max_norm_identity":float(max(np.max(abs(matrix(g,beta)/g**2-base)) for g,beta in couplings)),
"native_site_fermion":{"native_vertices":80,"bipartition_sizes":sizes,
"gamma_H_anticommutator_norm":float(np.max(abs(gamma@T+T@gamma))),
"positive_minus_negative_basis_index":sizes[0]-sizes[1],
"spectrum_chiral_pairing_max_residual":float(np.max(abs(eig+eig[::-1]))),
"result":"A balanced 40+40 80-site spinless fermion has bipartite chiral grading with zero sublattice index. TOE36 80+160 incidence Dirac has index -80 from orbital imbalance. Neither is a physical Weyl-family count or a 3+1D regulator."},
"five_physics_front_evidence":{
"two_plaquette_quantum":"EXECUTED GAUSS-preserving interacting 2-plaquette flux quantum model, truncated not full QED",
"fermionic_chirality":"EXECUTED 80-site spinless one-loop fermion holonomy and balanced chiral grading, no physical Weyl SM",
"native_gravity":"EXECUTED exact Gauss-sector no-go for any U(w) repair to tested link scaling D, not complete GR",
"interacting_continuum":"EXECUTED fermion/boson one-loop holonomy Hessian competition at fixed lattice and classical flat magnetic dynamics; no interacting continuum or RG",
"coupling_and_common_action":"EXECUTED beta/g^4 spectral degeneracy, no physical alpha or scale determined"},
"required_missing_physics":["full gauge+fermion quantum Hilbert space and controlled flux truncation convergence","true 4D chiral Weyl regulator with anomalies and SM charge selection","nonlinear native gravitational hypersurface-deformation algebra with spin2","interacting Lorentz continuum with UV/RG control and SI calibration","g,beta,physical length and all masses fixed by a common vacuum without input fits and out-of-sample prediction"],
"scope":"An exact parameter identifiability obstruction under limited tested observables. Does NOT imply all physical measurements leave g unidentified: charged matter, external normalization and nonlinear observables can constrain it, though prediction requires additional dynamics."}
(R/"data/w33_20261013_toe57_coupling_chirality_gate.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"basis":sizes,"param_groups":[(z["g"],z["beta"]) for z in groups],"spectral_residual":out["near_exact_max_norm_identity"]}))
