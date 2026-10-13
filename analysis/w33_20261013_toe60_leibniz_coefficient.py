"""TOE60 front4: exact leading O(a) native Bloch Leibniz defect.

This does NOT prove gravity constraint closure, but analytically explains
TOE59's 0.5-halving trend without a continuum-field-theory fit.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11970_native_wilson_dirac import construction
edges,volts,J,*_=construction()
E=np.asarray(edges,int);V=np.asarray(volts,float);J=np.asarray(J,float)
p=np.array([.9,-.4,.35]);q=np.array([-.35,.6,.2])
# Boundary matrix oriented -1 at source, +1 at target
B=np.zeros((160,80))
for i,(u,v) in enumerate(E):B[i,u]=-1;B[i,v]=1
# D_i(k) 1 = C(k)^H diag(J_i) (exp(i k.V_e)-1).
# Expand to second order k: source vertex term = .5 J_e (i z-z²/2),
# target term=.5 J_e(i z+z²/2). Therefore mixed
# coefficient of D_i(a(p+q))-D_i(ap)-D_i(aq) at a² is
# + B.T ( J_i * (V.p) * (V.q) )/2.
bilinear=np.array([B.T@(J[:,i]*(V@p)*(V@q))/2 for i in range(3)])
def full_D(k):
 phase=np.exp(1j*(V@k))
 edge=phase-1
 vals=np.zeros((3,80),complex)
 for i in range(3):
  z=J[:,i]*edge/2
  np.add.at(vals[i],E[:,0],z)
  np.add.at(vals[i],E[:,1],np.conj(phase)*z)
 return vals
records=[]
for a in (.2,.1,.05,.025,.0125):
 defect=(full_D(a*(p+q))-full_D(a*p)-full_D(a*q))/a
 res=float(np.linalg.norm(defect/a-bilinear)/np.sqrt(defect.size))
 sig=float(np.linalg.norm(defect)/np.sqrt(defect.size))
 records.append({"a":a,"rms_error":sig,"limit_coefficient_residual":res,
                 "relative_vs_Oa_limit":float(np.linalg.norm(defect/a-bilinear)/np.linalg.norm(bilinear))})
assert records[-1]["limit_coefficient_residual"]<records[0]["limit_coefficient_residual"]/12
assert records[-1]["relative_vs_Oa_limit"]<.025
out={"status":"PASS_TOE60_EXACT_BLOCH_LEIBNIZ_ASYMPTOTIC_COEFFICIENT",
"formula":"Let B be the 160x80 native oriented gradient and V_e the 3D deck voltage. For constant internal scalar 1 and D_i(k)=C(k)^H diag(J_i) B(k), the restricted product defect [D_i(a(p+q))-D_i(ap)-D_i(aq)]1/a equals a/2 B.T diag(J_i) [(V p)(V q)] + O(a²). This follows by expanding each edge phase exp(i a V k); signs at source/target are opposite at quadratic order.",
"exact_leading_coeff_rms":float(np.linalg.norm(bilinear)/np.sqrt(bilinear.size)),
"test_momenta":[p.tolist(),q.tolist()],"rms_records":records,
"conclusion":"The observed approximately 0.5 ratio on lattice-spacing halving is a direct consequence of analytic Bloch phase Taylor expansion on constant internal plane-wave profiles. The same finite graph fails exact derivation on general vertex fields. An O(a) restricted defect is NOT Einstein constraint closure nor uniform RG.",
"prior_work":"TOE59 established empirical 0.5 halving. Pass11970 constructs the rational current derivative; this gives its explicit leading bilinear term."}
(R/"data/w33_20261013_toe60_leibniz_coefficient.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE60 Leibniz",out["exact_leading_coeff_rms"],records[-1])
