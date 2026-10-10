"""TOE44 front4: exact channel-identification limits of W33 Pauli-power data.

Proves same output for a fixed input cannot identify CPTP channels, even if
all q=2|Tr(rho W)|^2, the -4 projector, and any higher moments are known.
Tests an extra probe and full phase-bearing Pauli expectation vector.
"""
from pathlib import Path
import json,itertools
import numpy as np
R=Path(__file__).resolve().parents[1]; O=R/"data/w33_20261010_toe44_channel_identifiability.json"
I=np.eye(9,dtype=complex);qI=np.eye(3,dtype=complex)
omega=np.exp(2j*np.pi/3);X=np.roll(qI,1,axis=0);Z=np.diag([1,omega,omega**2])
canon=lambda v:min(v,tuple(-t%3 for t in v))
P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
sp=lambda u,v:(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
A=np.array([[int(i!=j and sp(u,v)==0) for j,v in enumerate(P)] for i,u in enumerate(P)])
Pm=((A-12*np.eye(40))@(A-2*np.eye(40)))/96
W=np.stack([np.kron(np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,c),
                   np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,d)) for a,b,c,d in P])
assert np.max(abs(Pm@Pm-Pm))<1e-10
eta=.63
U=np.diag([1,1,-1,1,1,1,1,1,1])
assert np.max(abs(U.conj().T@U-I))<1e-12
def rho(v):return np.outer(v,v.conj())
primary=I[:,0]
secondary=(I[:,1]+I[:,2])/np.sqrt(2)
inputs={"primary_00":rho(primary),"secondary_interference_01_02":rho(secondary)}
def E0(s):return eta*s+(1-eta)*I/9
def E1(s):return eta*(U@s@U.conj().T)+(1-eta)*I/9
def features(s):
 exp=np.einsum("ab,pba->p",s,W)
 power=2*abs(exp)**2
 return {"purity":float(np.trace(s@s).real),
         "power":power.tolist(),
         "minus4_norm":float(np.linalg.norm(Pm@power)),
         "complex_expectations":[[float(z.real),float(z.imag)] for z in exp],
         "fourth_power_moment":float(np.sum(power**2)),
         "sixth_power_moment":float(np.sum(power**3))}
out={}
for label,s in inputs.items():
 a,b=E0(s),E1(s)
 assert abs(np.trace(a)-1)<1e-12 and abs(np.trace(b)-1)<1e-12
 q0,q1=features(a),features(b)
 eig=np.linalg.eigvalsh(a-b)
 trace_distance=float(sum(abs(eig))/2)
 power_difference=float(np.max(abs(np.array(q0["power"])-q1["power"])))
 phase_difference=float(np.max(abs(np.array(q0["complex_expectations"])-q1["complex_expectations"])))
 out[label]={"trace_distance":trace_distance,"max_power_difference":power_difference,
   "max_complex_exp_component_difference":phase_difference,
   "minus4_norm_E0":q0["minus4_norm"],"minus4_norm_E1":q1["minus4_norm"],
   "fourth_power_E0":q0["fourth_power_moment"],"fourth_power_E1":q1["fourth_power_moment"]}
assert out["primary_00"]["trace_distance"]<1e-12
assert out["primary_00"]["max_power_difference"]<1e-12
assert abs(out["secondary_interference_01_02"]["trace_distance"]-eta)<1e-12
assert out["secondary_interference_01_02"]["max_complex_exp_component_difference"]>.1
cert={"status":"CHANNEL_IDENTIFIABILITY_NO_GO_SINGLE_INPUT_EXACT",
"input_probe_results":out,
"channel_E0":"isotropic depolarizing E0(rho)=eta rho+(1-eta)I/9",
"channel_E1":"unitary-rotated depolarizing E1(rho)=eta U rho Udag+(1-eta)I/9, U=diag(1,1,-1,1,...,1)",
"eta":eta,
"theorem":"Since E0(|00><00|)=E1(|00><00|) but E0(psi2) != E1(psi2), no measurement or collection of W33 moments on the sole |00> output can identify which channel occurred.",
"proof":"Both maps CPTP for 0<=eta<=1; U stabilizes |00>. On psi2=(|01>+|02>)/sqrt2, U sends it to orthogonal psi2'=(|01>-|02>)/sqrt2, so outputs have trace distance eta.",
"limitation":"Channel identification requires multiple informationally complete input probes, not merely spectral invariants of a single output; phase-free q values may discard distinctions even with multiple probes."}
O.write_text(json.dumps(cert,indent=2)+"\n")
print(json.dumps({"status":cert["status"],"results":out}))
