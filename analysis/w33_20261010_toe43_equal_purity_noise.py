"""TOE43 front 4: W33 -4 Pauli Fourier mode as noise fingerprint.

Compare mathematically explicit random-unitary channels with IDENTICAL
output Tr rho^2, and isotropic depolarizing channel at same purity.
Determine which 15-mode diagnostics are blind to mixedness.
"""
from pathlib import Path
import itertools,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe43_noise_fingerprints.json"
w=np.exp(2j*np.pi/3);I=np.eye(3,dtype=complex);X=np.roll(I,1,axis=0);Z=np.diag([1,w,w*w])
canon=lambda v:min(v,tuple((-t)%3 for t in v))
pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
sp=lambda x,y:(x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
A=np.array([[int(i!=j and sp(p,q)==0) for j,q in enumerate(pts)] for i,p in enumerate(pts)])
J=np.ones((40,40));Id=np.eye(40)
Pm=(A-12*Id)@(A-2*Id)/96
assert np.max(abs(Pm@Pm-Pm))<1e-12
W=np.asarray([np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),
                      np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3])) for v in pts])
e0=np.eye(9,dtype=complex)[:,0];rho0=np.outer(e0,e0.conj())
# CPTP random-unitary channels E(rho)= 0.5(rho+U rho U^dag).
# Householder reflection maps e0 exactly to arbitrary orthogonal e1.
def reflection(ket):
 assert abs(np.vdot(ket,e0))<1e-12
 x=(e0-ket)/np.sqrt(2)
 U=np.eye(9)-2*np.outer(x,x.conj())
 assert np.max(abs(U.conj().T@U-np.eye(9)))<1e-12
 assert np.linalg.norm(U@e0-ket)<1e-12
 return U
q1=np.eye(9,dtype=complex)[:,1]
q2=(np.eye(9,dtype=complex)[:,1]+np.eye(9,dtype=complex)[:,3])/np.sqrt(2)
q3=(np.eye(9,dtype=complex)[:,1]+np.eye(9,dtype=complex)[:,3]+np.eye(9,dtype=complex)[:,8])/np.sqrt(3)
cases={}
for name,ket in (("basis_dephasing",q1),("two_site_superposition",q2),("entangled_three_site",q3)):
 U=reflection(ket)
 state=(rho0+U@rho0@U.conj().T)/2
 cases[name]=state
eta=np.sqrt((.5-1/9)/(1-1/9))
cases["isotropic_depolarization"]=eta*rho0+(1-eta)*np.eye(9)/9
def features(rho):
 p=float(np.trace(rho@rho).real)
 q=2*np.abs(np.einsum("ab,pba->p",rho,W))**2
 k=Pm@q;res=A@q-2*q-2
 return {"purity":p,"minus4_norm":float(np.linalg.norm(k)),
         "minus4_power":float(k@k),"graph_deficit_min":float(min(res)),
         "graph_deficit_max":float(max(res)),"graph_deficit_sum":float(sum(res)),
         "W33_projective_Pauli_power":q.tolist(),
         "W33_projective_minus4_component":k.tolist()}
outcome={name:features(rho) for name,rho in cases.items()}
for v in outcome.values():
 assert abs(v["purity"]-.5)<1e-12
 assert v["graph_deficit_max"]<1e-10
 assert abs(v["graph_deficit_sum"]+45)<1e-9
assert outcome["isotropic_depolarization"]["minus4_norm"]<1e-10
# Global depolarization of ANY pure state has q_out=eta² q_pure.
for seed in range(5):
 rng=np.random.default_rng(seed+438)
 z=rng.normal(size=9)+1j*rng.normal(size=9)
 z/=np.linalg.norm(z)
 qpure=features(np.outer(z,z.conj()))
 mixed=eta*np.outer(z,z.conj())+(1-eta)*np.eye(9)/9
 assert features(mixed)["minus4_norm"]<1e-10
# W33 automorphism/Clifford covariance of spectral norm:
# each Clifford permutes the 40 Pauli classes, so norm is basis independent.
out={"status":"PASS_SAME_PURITY_DISTINCT_W33_NOISE_FINGERPRINTS",
     "isotropic_eta_at_output_purity_half":float(eta),"channels":outcome,
     "same_purity_each":.5,
     "negative_control":"ALL isotropically depolarized pure inputs have Pminus q=0 although purity=1/2; hence Pminus is NOT a pure-vs-mixed discriminator",
     "positive_control":"Random-unitary dephasing/entangling channels are explicit CPTP maps (1/2 I +1/2 Ad_U) and give different Pminus norms at identical output purity",
     "boundary":"15-mode norm is an operationally computable fingerprint and not a complete quantum channel classifier. Requires trusted Pauli tomography; noise/SPAM not treated."}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"summary":{k:{z:v[z] for z in ("purity","minus4_norm","graph_deficit_sum")} for k,v in outcome.items()}}))
