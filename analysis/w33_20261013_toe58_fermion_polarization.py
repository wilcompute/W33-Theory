"""TOE58 front4: native finite fermion vacuum polarization obeys U(1) Ward
and produces a harmonic-sector response absent from bare plaquette Maxwell.

This is static one-loop tight-binding susceptibility, NOT physical
3+1D QED vacuum polarization or interacting Lorentz continuum.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,lk,octs,comm,*_=prep();edges=np.asarray(ed,dtype=int)
B=np.rint(gradient(ed,volts,np.zeros(3)).real)
P=np.rint(np.asarray([cycle_row(x,ed,volts,lk,np.zeros(3)) for x in octs+comm]).real)
ev,U=np.linalg.eigh(P.T@P+B@B.T);assert sum(ev<1e-8)==3
harm=U[:,:3]
rng=np.random.default_rng(5804)
ch=rng.normal(size=(80,2))
gauge=B@ch
gauge=gauge/np.linalg.norm(gauge,axis=0)
cycle=np.asarray(P[[0,186]],float).T
cycle=cycle/np.linalg.norm(cycle,axis=0)
X=np.column_stack([harm,cycle,gauge])
g=.7;beta=4.;mu=0.
def free_energy(t):
 A=X@t;u=np.exp(1j*g*A);H=np.zeros((80,80),complex)
 for v,(a,b) in enumerate(edges):
  H[a,b]-=u[v];H[b,a]-=u[v].conjugate()
 energies=np.linalg.eigvalsh(H)
 return float(-np.logaddexp(0.,-beta*(energies-mu)).sum()/beta)
zero=np.zeros(X.shape[1]);F0=free_energy(zero)
step=.12;J=np.zeros((7,7))
for i in range(7):
 e=np.eye(7)[i];J[i,i]=(free_energy(step*e)+free_energy(-step*e)-2*F0)/step**2
 for j in range(i):
  f=np.eye(7)[j]
  J[i,j]=J[j,i]=(free_energy(step*(e+f))-free_energy(step*(e-f))-free_energy(step*(-e+f))+free_energy(-step*(e+f)))/(4*step**2)
# Direct local gauge invariance in a matter determinant: for ANY A,
# A+B chi/g unitarily conjugates fermion hopping on 80 native vertices.
q=rng.normal(size=80);A=rng.normal(size=160)*.1
def free_A(A):
 h=np.zeros((80,80),complex);z=np.exp(1j*g*A)
 for i,(a,b) in enumerate(edges):h[a,b]-=z[i];h[b,a]-=z[i].conjugate()
 ee=np.linalg.eigvalsh(h);return -np.logaddexp(0.,-beta*ee).sum()/beta
exact_gauge_err=abs(free_A(A)-free_A(A+B@q/g))
assert exact_gauge_err<1e-10
max_gauge_hessian=float(np.max(abs(J[-2:,:])))
assert max_gauge_hessian<1e-8, max_gauge_hessian
h_e=np.linalg.eigvalsh(J[:3,:3]);assert max(h_e)<0
plaq_e=np.linalg.eigvalsh(J[3:5,3:5])
assert np.max(abs(J[3:5,3:5]))>1e-5
# Bare magnetic stiffness is zero on harmonic H1, but fermion loops
# contribute finite negative curvature there. This is not local
# propagating Lorentzian vacuum polarization or a photon mass.
assert np.linalg.norm(P@harm)<1e-8
out={"status":"PASS_TOE58_NATIVE_FERMION_STATIC_WARD_POLARIZATION",
"basis":["harmonic1","harmonic2","harmonic3","plaquette0","plaquette186","gauge1","gauge2"],
"note":"Actual basis has 7 directions total, 3 harmonic plus 2 plaquette plus 2 pure-gauge.",
"finite_difference_step":step,"Hessian":J.tolist(),
"harmonic_Hessian_eigenvalues":h_e.tolist(),
"plaquette_Hessian_eigenvalues":plaq_e.tolist(),
"max_two_pure_gauge_rows_or_columns":max_gauge_hessian,
"finite_U1_gauge_free_energy_residual":float(exact_gauge_err),
"bare_magnetic_harmonic_curl_norm":float(np.linalg.norm(P@harm)),
"conclusion":"Integrating out the specified finite spinless fermion generates a gauge-invariant response that is nonzero in the harmonic H1 sector, which the bare Maxwell magnetic curl P cannot see. The static matter determinant respects exact local U1 Ward zero modes but makes trivial holonomy unstable.",
"scope":"A finite 80-site spinless static one-loop susceptibility at beta=4, not a 4D photon polarization tensor, physical Debye screening, anomaly cancellation, renormalized fine-structure constant or Lorentz-invariant interacting continuum."}
(R/"data/w33_20261013_toe58_fermion_polarization.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE58 polarization",h_e.tolist(),plaq_e.tolist(),max_gauge_hessian)
