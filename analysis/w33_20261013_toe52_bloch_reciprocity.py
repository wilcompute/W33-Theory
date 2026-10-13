"""TOE52 spectral no-go: ±Bloch pairs add no new local information for real weights.

This relies on the current native P(k) being complex-conjugation symmetric.
"""
import json,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11956_local_electric_metric import prep,cycle_row
base=json.loads((R/"data/w33_pass11956_local_electric_metric.json").read_text())
w=np.array([float(v.split('/')[0])/float(v.split('/')[1]) if '/' in v else float(v) for v in base["electric_link_weights"]])
ed,volts,lookup,zero,comm,*_=prep()
modes=zero+comm
assert len(w)==160
def P(k):return np.asarray([cycle_row(z,ed,volts,lookup,np.asarray(k)) for z in modes])
ks=[(.83,.17,.29),(.47,.53,.41),(1.01,.91,.83)]
def run(k):
 V=P(k)
 Q=(V.conj().T@V)/np.sqrt(w[:,None]*w[None,:])
 powers=[];gradients=[]
 Rn=np.eye(160,dtype=complex)
 for n in (1,2,3):
  Rn=Rn@Q
  powers.append(float(np.trace(Rn).real))
  gradients.append((-n*Rn.diagonal().real/w).tolist())
 return powers,np.array(gradients)
checks=[]
der_plus=[];der_twosides=[]
for k in ks:
 u=tuple(-x for x in k)
 X=P(k);Y=P(u)
 matrix=float(np.max(abs(Y-X.conj())))
 plus,dp=run(k)
 minus,dm=run(u)
 difference=float(np.max(abs(np.array(plus)-np.array(minus))))
 grad=float(np.max(abs(dp-dm)))
 assert matrix<1e-12 and difference<1e-7 and grad<1e-7
 checks.append(dict(k=list(k),P_minus_vs_conjP_plus_error=matrix,
  max_trace_moment_error=difference,max_weight_gradient_error=grad))
 der_plus.extend(dp)
 der_twosides.extend(dp);der_twosides.extend(dm)
rplus=int(np.linalg.matrix_rank(np.asarray(der_plus),tol=1e-4))
rpair=int(np.linalg.matrix_rank(np.asarray(der_twosides),tol=1e-4))
assert rplus==rpair
out=dict(status="PASS",model="Native real-coefficient W33 magnetic Bloch row operator",
 statement="P(-k)=conjugate(P(k)); for positive REAL diagonal electric weights W, K(-k)=conjugate(K(k)); all trace moments Tr[(W^-1/2 K W^-1/2)^n] and all weight gradients are EVEN in k.",
 k_examples=checks,rank_3wavevectors_9moments=rplus,rank_with_three_opposite_wavevectors_18moments=rpair,
 practical_conclusion="Opposite momentum spectral traces may average independent detector noise but add NO new noiseless Jacobian rank. Optimize non-opposite k and observable type; broken reciprocity or phase-sensitive odd-in-k observables require extra physical structures.",
 scope="Finite native P(k) and positive real w; NOT a theorem for magnetic/nonreciprocal media or phase-resolved Bloch eigenvectors.")
(R/"data/w33_20261013_toe52_bloch_reciprocity.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","rplus":rplus,"rpaired":rpair,"max_P_error":max(z["P_minus_vs_conjP_plus_error"] for z in checks)}))
