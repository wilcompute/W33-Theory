"""TOE57 quantum-matter induced flat holonomy stiffness and competition.

A *finite one-loop tight-binding/Gaussian determinant model*; NOT SM,
cosmological vacuum, self-consistent quantum gauge theory or physical CP.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,lookup,octs,comm,*_=prep(); edges=np.asarray(ed,dtype=int)
B=np.rint(gradient(ed,volts,np.zeros(3)).real)
P=np.rint(np.asarray([cycle_row(c,ed,volts,lookup,np.zeros(3)) for c in octs+comm]).real)
a,h=np.linalg.eigh(P.T@P+B@B.T)
assert sum(a<1e-8)==3
H=h[:,:3];g=.7;tf=4.;kb=.7;mb2=.8
def energies(v):
 A=H@np.asarray(v)
 assert np.linalg.norm(P@A)<1e-8
 z=np.exp(1j*g*A)
 hf=np.zeros((80,80),dtype=complex)
 for j,(u,w) in enumerate(edges):
  hf[u,w]-=z[j];hf[w,u]-=z[j].conjugate()
 E=np.linalg.eigvalsh(hf)
 ff=-np.logaddexp(0.,-tf*E).sum()/tf
 D=np.zeros((160,80),dtype=complex)
 D[np.arange(160),edges[:,0]]=-z
 D[np.arange(160),edges[:,1]]=1
 K=mb2*np.eye(80)+kb*D.conj().T@D
 fb=np.linalg.slogdet(K)[1].real
 # Pure gauge local magnetic Wilson term identically zero.
 return float(ff),float(fb)
origin=np.zeros(3)
F0,B0=energies(origin)
eps=.2;HF=np.zeros((3,3));HB=np.zeros((3,3))
for j in range(3):
 x=np.eye(3)[j]
 fp,bp=energies(eps*x);fm,bm=energies(-eps*x)
 HF[j,j]=(fp+fm-2*F0)/eps**2
 HB[j,j]=(bp+bm-2*B0)/eps**2
 for k in range(j+1,3):
  y=np.eye(3)[k]
  fpp,bpp=energies(eps*(x+y))
  fpm,bpm=energies(eps*(x-y))
  fmp,bmp=energies(eps*(-x+y))
  fmm,bmm=energies(-eps*(x+y))
  HF[j,k]=HF[k,j]=(fpp-fpm-fmp+fmm)/(4*eps**2)
  HB[j,k]=HB[k,j]=(bpp-bpm-bmp+bmm)/(4*eps**2)
fe,fx=np.linalg.eigh(HF);be=np.linalg.eigvalsh(HB)
assert be.min()>0
# Positivity of HF + N_b HB iff N_b >= largest generalized eig(-HF,HB).
bb_e,bb_v=np.linalg.eigh(HB)
bw=bb_v@np.diag(1/np.sqrt(bb_e))@bb_v.T
threshold=float(max(np.linalg.eigvalsh(-bw@HF@bw).max(),0))
for N in (0.,threshold+.1):
 eig=np.linalg.eigvalsh(HF+N*HB)
 assert (eig.min() <0) if N==0 and fe.min()<0 else eig.min()>-1e-6
# Scan along the most negative eigenvector to show CP-reversed
# degenerate opposite ± holonomies with reduced finite-model F.
unstable=fx[:,0]
amps=[.0,.5,1.,2.,3.,5.,8.,12.]
scan=[]
for t in amps:
 f,b=energies(t*unstable)
 fm,bm=energies(-t*unstable)
 assert abs(f-fm)<1e-9 and abs(b-bm)<1e-9
 scan.append({"t":t,"fermion_F_minus_zero":f-F0,
              "boson_F_minus_zero":b-B0})
# No claim of global minima, the t_scan is only along a 1D direction.
# No projected spontaneous CP if continuum vacuum not chosen/stabilized.
out={"status":"PASS_TOE57_HARMONIC_ONE_LOOP_FERMION_BOSON_COMPETITION",
"finite_model":{"native_sites":80,"native_links":160,"H1_dimension":3,
"g":g,"fermion_beta":tf,"boson_mass2":mb2,"boson_kappa":kb},
"fermion_zero_holonomy_F":F0,"boson_zero_holonomy_F":B0,
"fermion_local_holonomy_hessian":HF.tolist(),
"fermion_hessian_eigenvalues":fe.tolist(),
"boson_local_holonomy_hessian":HB.tolist(),
"boson_hessian_eigenvalues":be.tolist(),
"number_boson_weight_threshold_to_stabilize_trivial_holonomy":threshold,
"threshold_rule":"For V_eff=F_one_spinless_fermion+N_b*F_one_Gaussian_boson, the local quadratic matrix is H_f+N_b H_b. Given H_b>0, zero holonomy becomes a strict local minimum if N_b is greater than largest eigenvalue of (-H_b^-1/2 H_f H_b^-1/2). This is a mathematical continuous determinant-weight parameter, not a fractional number of physical species.",
"sampled_negative_holonomy_direction":unstable.tolist(),
"sampled_CP_symmetric_line":scan,
"exact_magnetic_flatness":"For every H1 vector A=H t, P A=0, so compact magnetic energy is exactly zero and compact magnetic Hessian coincides with that at A=0. Quantum charged-matter determinants alone lift the formerly flat H1 energy directions.",
"physics_boundary":"One finite 80-site spinless hopping fermion at finite beta and one positive-mass Gaussian complex boson; no chiral Weyl fermions, gauge dynamics backreaction, charge and beta selected by W33, thermodynamic limit, 4D quantum determinant, dynamical vacuum uniqueness or physical spontaneous CP.",
"prior_art":"Magnetic flux-phase/diamagnetic finite lattice matter effects well known; novelty is exact W33 H1 3D determinant stiffness and explicit statistical competition in this specified toy model."}
(R/"data/w33_20261013_toe57_one_loop_competition.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"ferm_eig":fe.tolist(),"bos_eig":be.tolist(),"N_threshold":threshold,"scan":[x["fermion_F_minus_zero"] for x in scan]}))
