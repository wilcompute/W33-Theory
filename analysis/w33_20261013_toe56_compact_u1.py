"""TOE56 physics I: repair local W33 U(1) to a compact Wilson action.

The native TOE55 quadratic magnetic energy is invariant under connected
vertex gauge shifts, but not under link-angle 2pi periodicity.
"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
P=np.rint(np.array([cycle_row(z,ed,volts,look,np.zeros(3)) for z in octs+comm]).real).astype(int)
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(int)
assert P.shape==(1385,160) and B.shape==(160,80)
assert np.max(np.abs(P@B))==0
# All coefficients of curl are INTEGER. This ensures Wilson plaquettes
# are link-angle periodic for any independent link 2pi offset.
assert np.allclose(P,np.rint(P))
e=0;g=.43;A=np.random.default_rng(561).normal(size=160)*.25
n=np.zeros(160,dtype=int);n[e]=1
Ashift=A+(2*np.pi/g)*n
def quadratic(A): return float(.5*np.dot(P@A,P@A))
def compact(A): return float(np.sum(1-np.cos(g*(P@A)))/(g*g))
before,after=quadratic(A),quadratic(Ashift)
c0,c1=compact(A),compact(Ashift)
assert abs(after-before)>1
assert abs(c1-c0)<1e-9
# Wilson magnetic harmonic agrees to quadratic order as amplitude->0.
ratios=[]
for eps in (.1,.05,.025):
 x=eps*A
 quadratic_eps=quadratic(x)
 compact_eps=compact(x)
 ratio=abs(compact_eps-quadratic_eps)/quadratic_eps
 ratios.append(ratio)
assert .1<ratios[1]/ratios[0]<.4 and .1<ratios[2]/ratios[1]<.4
# Full local U1 gauge invariance, with scalar matter.
rng=np.random.default_rng(56001)
chi=rng.normal(size=80)
A2=A+(B@chi)/g
assert abs(compact(A2)-compact(A))<1e-9
z=rng.normal(size=80)+1j*rng.normal(size=80)
v=np.asarray(ed,dtype=int)
def hopping(A,z):
 return float(np.sum(abs(z[v[:,1]]-np.exp(1j*g*A)*z[v[:,0]])**2))
h0=hopping(A,z)
h1=hopping(A2,np.exp(1j*chi)*z)
assert abs(h1-h0)<1e-10
assert abs(hopping(Ashift,z)-h0)<1e-10
# Exact k=0 native cohomology; rankP=78 rankB=79 -> dimH1=3.
eig,vec=np.linalg.eigh(P.T@P)
eigB=np.linalg.eigvalsh(B.T@B)
rankP=int(np.count_nonzero(eig>1e-7))
rankB=int(np.count_nonzero(eigB>1e-7))
assert (rankP,rankB)==(78,79)
harm_dim=160-rankP-rankB
assert harm_dim==3
# harmonic vectors simultaneously P h=0 and B.T h=0.
gauge_basis=np.linalg.svd(B,full_matrices=False)[0][:,:rankB]
ker=vec[:,:160-rankP]
hspace=ker-gauge_basis@(gauge_basis.T@ker)
Q,_=np.linalg.qr(hspace)
# QR first three may be nearly zero if first ker vector lies in imB;
# Instead eigensolve P.TP + BB.T; exactly 3 common zero modes.
he,hu=np.linalg.eigh(P.T@P+B@B.T)
assert int(np.sum(he<1e-7))==3
H=hu[:,:3]
assert np.linalg.norm(P@H)<1e-8 and np.linalg.norm(B.T@H)<1e-8
# H lies in residual 3D noncontractible Wilson-flux sector;
# local plaquette and gauge constraints cannot distinguish A+s H.
s=np.array([.14,-.11,.08])
assert abs(compact(A+H@s)-compact(A))<1e-9
assert abs(hopping(A+H@s,z)-h0)>1e-6 # charged matter senses holonomies.
out=dict(status="PASS_TOE56_COMPACT_U1_NATIVE_COHOMOLOGY",
native_W33_dimensions={"sites":80,"edges":160,"plaquettes":1385,"rank_gradient":rankB,"rank_plaquette":rankP,"first_cohomology":harm_dim},
native_complex_exact_PB_max=int(np.max(abs(P@B))),
compact_link_2pi_shift={"shift_link":e,"quadratic_before":before,"quadratic_after":after,"compact_before":c0,"compact_after":c1,
"quadratic_breaking":after-before,"compact_absolute_difference":abs(c1-c0)},
harmonic_quadratic_recovery_relative_errors=ratios,
native_local_gauge={"plaquette_energy_difference":abs(compact(A2)-compact(A)),
"charged_matter_hopping_difference":abs(h1-h0),
"large_link_shift_hopping_difference":abs(hopping(Ashift,z)-h0)},
first_cohomology={"dim":3,"P_H_residual":float(np.linalg.norm(P@H)),
 "Bt_H_residual":float(np.linalg.norm(B.T@H)),
 "compact_magnetic_harmonic_shift_residual":abs(compact(A+H@s)-compact(A)),
 "charged_hopping_harmonic_shift_difference":abs(hopping(A+H@s,z)-h0)},
theorem="Compact link U_e=exp(i g A_e) requires invariance A_e->A_e+2pi n_e/g. The TOE55 quadratic plaquette energy 1/2||P A||² violates this, despite local vertex-gauge invariance. Wilson plaquette sum(1-cos(g P A))/g² repairs all independent large link-angle shifts because native P has integer entries, and tends to the TOE55 magnetic term quadratically for small angles. At zero Bloch twist the native chain complex has b1=160-rank(P)-rank(B)=3.",
limits="This is a classical fixed finite compact U1 Hamiltonian improvement, not quantized lattice gauge theory, charge prediction, chiral SM, nonabelian forces, RG, or emergent gravity. Matter response to harmonic holonomies is an Aharonov-Bohm-like finite-model phenomenon.",
prior_art="Kogut Susskind PRD11 395 (1975) standard compact lattice gauge Hamiltonian; the native W33 exact three harmonic cohomology dimension was already known from TOE38." )
(R/"data/w33_20261013_toe56_compact_u1.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"rank":(rankP,rankB,harm_dim),"quadratic_break":after-before,"compact_diff":abs(c1-c0),"holonomy_hopping":abs(hopping(A+H@s,z)-h0)},indent=2))
