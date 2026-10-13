"""TOE57 fermionic holonomy: native 80-site spinless tight-binding
grand free-energy across W33 H1, versus TOE56 boson diamagnetic bound.

Not a chiral SM fermion, no self-consistent dynamical vacuum,
and no physical CP violation (A and -A have equal energy).
"""
import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
e=np.asarray(ed,dtype=int)
B=np.rint(gradient(ed,volts,np.zeros(3)).real)
P=np.rint(np.array([cycle_row(z,ed,volts,look,np.zeros(3)) for z in octs+comm]).real)
ev,U=np.linalg.eigh(P.T@P+B@B.T)
assert int(np.sum(ev<1e-8))==3
H=U[:,:3]
g=.7;kappa=1.;temp_inv=4.;rng=np.random.default_rng(57012)
def hermitian(A):
 z=np.exp(1j*g*A)
 mat=np.zeros((80,80),dtype=complex)
 for j,(a,b) in enumerate(e):
  mat[a,b]-=kappa*z[j];mat[b,a]-=kappa*z[j].conjugate()
 assert np.max(abs(mat-mat.conj().T))==0
 return mat
def fermi_F(A):
 vals=np.linalg.eigvalsh(hermitian(A))
 # spinless fermions at grand canonical mu=0
 return float(-np.logaddexp(0.,-temp_inv*vals).sum()/temp_inv)
def boson_F(A):
 D=np.zeros((160,80),dtype=complex)
 ix=np.arange(160)
 D[ix,e[:,0]]=-np.exp(1j*g*A);D[ix,e[:,1]]=1
 return float(np.linalg.slogdet(.8*np.eye(80)+.7*D.conj().T@D)[1].real)
A0=np.zeros(160);F0=fermi_F(A0);B0=boson_F(A0)
tests=[]
for t in [[0,0,0],[1,0,0],[3,0,0],[0,4,0],[0,0,-5],
          *[z.tolist() for z in rng.uniform(-10,10,size=(80,3))]]:
 A=H@np.array(t,dtype=float)
 assert np.linalg.norm(P@A)<1e-8
 diff=fermi_F(A)-F0
 bdiff=boson_F(A)-B0
 assert bdiff>-1e-9
 cp=abs(fermi_F(A)-fermi_F(-A))
 assert cp<1e-10
 tests.append({"H1_coordinates":t,"fermion_grand_energy_shift":diff,
               "boson_logdet_energy_shift":bdiff,"CP_conjugation_residual":cp})
chi=rng.normal(size=80)
A=H@np.array([3.,-4.,5.])
assert abs(fermi_F(A+B@chi/g)-fermi_F(A))<1e-10
best=min(tests,key=lambda t:t["fermion_grand_energy_shift"])
# Result is an observational scan: do not assert minima at nontrivial
# H1 unless actually found. Existence of samples below zero sufficient
# to exclude simple "boson-type theorem" for this fermion model.
out={"status":"PASS_TOE57_SPINLESS_FERMION_HOLONOMY_SURVEY",
"native_W33_sites":80,"native_links":160,"first_cohomology":3,
"fermion_model":"One spinless complex fermion on the native 80-site graph, nearest-neighbor gauge-covariant Hermitian hopping H_f=-κ Σ_ab[e^(igA_ab)|a><b|+h.c.], at inverse temp β=4, μ=0. F=-β^-1 Σ log(1+exp(-β epsilon_j)).",
"parameters":{"g":g,"hopping_kappa":kappa,"inverse_temperature":temp_inv},
"survey_count":len(tests),"zero_holonomy_fermion_free_energy":F0,
"sampled_min_fermion_free_energy_shift":best["fermion_grand_energy_shift"],
"sampled_minimizer_H1_coordinates":best["H1_coordinates"],
"n_fermion_lower_than_zero":sum(x["fermion_grand_energy_shift"]<-1e-7 for x in tests),
"n_boson_lower_than_zero":sum(x["boson_logdet_energy_shift"]<-1e-7 for x in tests),
"max_CP_reversal_energy_error":max(x["CP_conjugation_residual"] for x in tests),
"gauge_conjugation_free_energy_residual":abs(fermi_F(A+B@chi/g)-fermi_F(A)),
"local_flatness":"All sampled A are genuine native H1 harmonic cochains with P A=0. Their charged-matter spectrum may vary with global holonomy while the local compact Wilson plaquette energy stays zero.",
"important_boundary":"This is a finite 80-site, grand-canonical spinless lattice fermion free energy, NOT an anomaly-free Weyl regulator, self-consistent gauge+fermion vacuum, SM chiral generation count, spontaneous CP selection or experimental physics. Even if nonzero holonomies win at finite temperature, A and -A remain degenerate and selecting one needs dynamical symmetry breaking criteria.",
"data":tests}
(R/"data/w33_20261013_toe57_fermion_holonomy.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"survey":len(tests),"min":out["sampled_min_fermion_free_energy_shift"],"n_lower":out["n_fermion_lower_than_zero"],"boson_lower":out["n_boson_lower_than_zero"]}))
