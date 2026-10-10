"""W33 TOE40 Maxwell constrained Hamiltonian audit; read-only to prior certificates."""
import sys,json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,lookup,zero,comm,picked,counts=prep()
assert len(ed)==160 and len(zero)+len(comm)==1385
results=[]
for t in (.01,.02):
 k=np.array([t,0.,0.])
 B=gradient(ed,volts,k)
 P=np.array([cycle_row(w,ed,volts,lookup,k) for w in zero+comm])
 closure=float(np.max(abs(P@B)))
 assert closure<1e-10,closure
 # U columns 80:160 span transverse ker B^dagger.
 U,s,Vh=np.linalg.svd(B,full_matrices=True)
 assert min(s)>1e-6
 T=U[:,80:]
 C=P@T
 eig=np.linalg.eigvalsh(C.conj().T@C)
 assert min(eig)>-1e-8
 row={'k':t,'closure':closure,'curl_rank':int(np.linalg.matrix_rank(P,tol=1e-7)),'gradient_rank':int(np.linalg.matrix_rank(B,tol=1e-7)),'low_eigs':eig[:3].real.tolist(),'maxwell_light_modes':int(np.sum(eig<.01))}
 assert row['curl_rank']==80 and row['gradient_rank']==80 and row['maxwell_light_modes']==2
 # H(A,E)=1/2 (E^*E+ ||P A||^2), E constrained by B^* E=0.
 # Gauge invariance of potential: P (A+B phi) = P A.
 rng=np.random.default_rng(4040)
 A=rng.normal(size=160)+1j*rng.normal(size=160)
 phi=rng.normal(size=80)+1j*rng.normal(size=80)
 gauge_diff=float(abs(np.vdot(P@(A+B@phi),P@(A+B@phi))-np.vdot(P@A,P@A)))
 row['gauge_energy_difference']=gauge_diff
 assert gauge_diff<1e-8
 # Gauss constraint preserved by Hamilton flow: B^dagger P^dagger P A=0.
 row['gauss_force_residual']=float(np.max(abs(B.conj().T@(P.conj().T@(P@A)))))
 assert row['gauss_force_residual']<1e-8
 results.append(row)
slope=[results[1]['low_eigs'][i]/results[0]['low_eigs'][i] for i in (0,1)]
assert all(3.75<x<4.25 for x in slope),slope
out={'status':'PASS','substrate':'W33 Levi three-deck curl/gauge 2-complex (Round38)','Hamiltonian':'H=1/2 ||E||^2+1/2 ||P(k) A||^2, with B(k)^dag E=0; A~A+B(k)phi','linear_dispersion_eigenvalue_ratio_double_k':slope,'k_samples':results,'boundary':'This is a positive gauge-constrained *linear* Bloch model, not a quantized Maxwell theory. Continuous rotational/Lorentz invariance, physical units and photon-matter coupling are unproved.'}
Path('data/w33_20261010_toe40_native_maxwell_hamiltonian.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out),flush=True)
