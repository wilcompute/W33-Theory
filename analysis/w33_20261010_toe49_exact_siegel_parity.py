"""TOE49 exact charge parity selection extends Pass11912 beyond Gaussian regime.

At theta argument 0, simultaneous n -> -n makes
Theta[(c/3,a/3)] = Theta[(-c/3,-a/3)] at EVERY symmetric
Siegel matrix with positive imaginary part.
For a=0, the c=1,2 light masses are EXACTLY locked even when
Omega12 entangles strongly, not only as Omega22->i infinity.
a=1 vs a=2 are exact mirrors at all finite Omega22.
"""
import json,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11912_entangling_modulus_is_the_wilson_line import Th2
rng=np.random.default_rng(49112)
residual_zero=[];residual_mirror=[];samples=[]
for t in range(36):
 A=rng.normal(size=(2,2));Im=A@A.T+np.eye(2)*1.3
 B=rng.normal(size=(2,2));Re=(B+B.T)/3
 Om=Re+1j*Im
 C=np.array([[Th2(c/3,a/3,Om) for c in range(3)] for a in range(3)])
 err0=abs(C[0,1]-C[0,2])
 err1=max(abs(C[1,c]-C[2,(-c)%3]) for c in range(3))
 residual_zero.append(float(err0));residual_mirror.append(float(err1))
 if t<5:samples.append({"Omega_real":Re.tolist(),"Omega_imag":Im.tolist(),
    "class_zero_light_difference":float(err0),"charge_mirror_error":float(err1)})
assert max(residual_zero)<2e-12
assert max(residual_mirror)<2e-12
# Invariance under unrestricted off-diagonal Omega12: take strongly mixed
# positive-definite 2x2 Siegel matrix NOT in Gaussian regime.
Om=np.array([[.17+2.0j,.46+1.23j],[.46+1.23j,.08+1.7j]])
assert np.linalg.eigvalsh(Om.imag).min()>0
C=np.array([[Th2(c/3,a/3,Om) for c in range(3)] for a in range(3)])
assert abs(C[0,1]-C[0,2])<2e-12
assert max(abs(C[1,c]-C[2,(-c)%3]) for c in range(3))<2e-12
out={"status":"TOE49_EXACT_FINITE_SIEGEL_CHARGE_PARITY_LOCK",
"n_random_positive_definite_complex_Siegel_moduli":36,
"max_class_zero_complex_light_amplitude_difference":max(residual_zero),
"max_class_1_2_charge_mirror_complex_difference":max(residual_mirror),
"strong_entangling_off_diagonal_Omega12":[float(Om[0,1].real),float(Om[0,1].imag)],
"examples":samples,
"proof":"At zero theta argument, Theta[alpha](0,Omega)=sum_{n in Z²} exp(i pi(n+alpha)^T Omega(n+alpha)) is exactly even under alpha->-alpha, by n->-n (with the integer-characteristic shift). Taking alpha=(c/3,0), 1/3 and 2/3 are negatives modulo integers, so the complex amplitudes coincide exactly FOR ALL symmetric Omega in the Siegel upper half-space. Taking alpha=(c/3,1/3) and (-c/3,2/3) gives exact class-1/class-2 charge mirroring at every finite Omega, not only the leading Gaussian term.",
"physics_consequence":"An off-diagonal W33-entangling complex-structure modulus alone cannot lift the a=0 light pair in a localized-Higgs zero-theta-argument sector, even outside the Gaussian approximation. For a=1,2 its mirror pair has the same multiset of masses. Wilson shifts, nonlocalized Higgs, additional characteristics, sector-changing couplings or other operators may change these identities.",
"boundary":"Exact special theta characteristics at zero argument; no dynamical moduli stabilization, physical Yang-Mills spectrum, or proof of actual flux vacuum."}
(R/"data/w33_20261010_toe49_exact_siegel_charge_parity.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"err_a0":max(residual_zero),"err_mirror":max(residual_mirror)}))
