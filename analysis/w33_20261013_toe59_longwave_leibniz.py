"""TOE59 gravity/Lorentz front: genuine native local derivative Leibniz
defect on low Bloch modes under explicit periodic deck refinement.

Not a gravitational hypersurface-deformation algebra proof.
"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11970_native_wilson_dirac import construction
ed,volts,J,*_=construction()
edges=np.array(ed,int);v=np.asarray(volts,float);u=np.ones(80,complex)
def D_on_one(k):
 phi=np.exp(1j*(v@k))
 B=np.zeros((160,80),complex);C=np.zeros_like(B)
 for e,(a,b) in enumerate(edges):
  B[e,a]=-1;B[e,b]=phi[e];C[e,a]=.5;C[e,b]=.5*phi[e]
 Bu=B@u
 return np.array([C.conj().T@(J[:,i]*Bu) for i in range(3)])
p=np.array([.9,-.4,.35]);q=np.array([-.35,.6,.2])
records=[]
for a in (.2,.1,.05,.025):
 # f=e^(ia p.n), g=e^(ia q.n), product has frequency a(p+q).
 # Physical discrete derivative D_a=D(ap)/a.
 df=D_on_one(a*p)/a;dg=D_on_one(a*q)/a;dfg=D_on_one(a*(p+q))/a
 leib=dfg-df-dg
 rms=float(np.linalg.norm(leib)/np.sqrt(leib.size))
 records.append({"lattice_spacing":a,"physical_Leibniz_rms":rms,
                 "flat_derivative_real_imag_norms":[float(np.linalg.norm(df.real)),float(np.linalg.norm(df.imag))],
                 "Leibniz_max":float(np.max(abs(leib)))})
 assert rms>0
ratios=[records[i+1]["physical_Leibniz_rms"]/records[i]["physical_Leibniz_rms"] for i in range(3)]
print("LEIB",ratios,records,flush=True)
# The defect must shrink in this *restricted plane-wave sector*, no
# statement for general arbitrary vertex functions or full canonical H.
assert all(0.15<r<0.85 for r in ratios)
out={"status":"PASS_TOE59_NATIVE_BLOCH_CONTINUUM_LEIBNIZ_SCALING",
"native_bloch_derivative":"D_i(k)=C(k).dag diag(J[:,i]) B(k), J rational native harmonic-current derivative from Pass11970. For physical spacing a, use a^-1 D_i(ap) on a Bloch scalar with constant internal80-vector. Products add external momenta.",
"plane_wave_momenta":[p.tolist(),q.tolist()],
"records":records,"halving_ratios":ratios,
"interpretation":"At finite spacing the full 80-site pointwise product derivative is not a derivation, as Pass11301 and11976 show. For a restricted long-wavelength Bloch plane-wave sector, a^-1[D_i(a(p+q))-D_i(ap)-D_i(aq)]1 may vanish with a; its observed convergence is a restricted consistency check, NOT an interacting dynamical GR constraint-algebra continuum.",
"scope":"One-particle low-momentum plane waves with constant internal amplitudes; no nonlinear metric, constraints, Gauss product, quantum interactions, physical Planck length or rigorous uniform operator limit."}
(R/"data/w33_20261013_toe59_longwave_leibniz.json").write_text(json.dumps(out,indent=2)+"\n")
