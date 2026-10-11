"""TOE49 audit Pass11910 actual CKM entries rather than fourth-largest magnitude.

The published Pass11910 control picks sorted fourth-largest |V| element.
It is not always the physical |V_us| in mass-ordered eigenbases.
"""
import json,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"analysis"))
from w33_pass11910_cross_sector_invariant_and_ckm import yuk_matrix,DATA_MZ
O=R/"data/w33_20261010_toe49_ckm_mass_label_audit.json"
target={"Vus":.225,"Vcb":.041,"Vub":.0037,"J":3e-5}
def ckm(Yu,Yd):
 # SVD sorted DESCENDING; reverse to mass labels (u,c,t)/(d,s,b).
 Uu,su,_=np.linalg.svd(Yu)
 Ud,sd,_=np.linalg.svd(Yd)
 V=Uu[:,::-1].conj().T@Ud[:,::-1]
 J=float(np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0])))
 return np.abs(V),J,su[::-1],sd[::-1]
tau_u=4.2j; tau_d=2.6j
zu=.12*tau_u;zd=.03+.07*tau_d
records=[]
for ku in range(3):
 for kd in range(3):
  Yu=yuk_matrix(zu,tau_u,k=ku)
  Yd=yuk_matrix(zd,tau_d,k=kd)
  P,J,su,sd=ckm(Yu,Yd)
  for kh in range(3):
   if kh==kd:continue
   H=yuk_matrix(zd,tau_d,k=kh)
   for ep in [0,.001,.002,.003,.004,.006]:
    V,J,su,sd=ckm(Yu,Yd+ep*H)
    v={"Vus":float(V[0,1]),"Vcb":float(V[1,2]),"Vub":float(V[0,2]),"J":J}
    records.append(dict(ku=ku,kd=kd,kh=kh,eps=ep,**v,
       fourth_largest=float(sorted(V.ravel())[-4]),
       Vabs=V.tolist() if ep in (0,.003) else None,
       massratios_up=(su/su[-1]).tolist() if ep==0 else None,
       massratios_down=(sd/sd[-1]).tolist() if ep==0 else None))
# Show that physically specified Cabibbo position can differ from
# the repository's permutation-blind fourth-largest statistic.
nonzero=[r for r in records if r["eps"]==.003]
best=min(nonzero,key=lambda r:sum((r[k]-target[k])**2/(target[k]**2+.001) for k in ("Vus","Vcb","Vub")))
repo_equivalent=next(r for r in records if (r["ku"],r["kd"],r["kh"],r["eps"])==(0,1,2,.003))
# Search independent complex phases and amplitude while keeping the
# same two tau moduli and one extra Higgs in down: mass-labelled full CKM.
scan=[]
for ku in range(3):
 Yu=yuk_matrix(zu,tau_u,k=ku)
 for kd in range(3):
  base=yuk_matrix(zd,tau_d,k=kd)
  for kh in range(3):
   if kh==kd:continue
   H=yuk_matrix(zd,tau_d,k=kh)
   for ep in np.geomspace(.0001,.2,22):
    for phi in np.linspace(0,2*np.pi,16,endpoint=False):
     V,J,_,_=ckm(Yu,base+ep*np.exp(1j*phi)*H)
     values=dict(Vus=float(V[0,1]),Vcb=float(V[1,2]),Vub=float(V[0,2]),J=J)
     # Low sensitivity to target uncertainties: ratios and absolute errors
     score=sum((values[k]/target[k]-1)**2 for k in ("Vus","Vcb","Vub"))
     scan.append({"score":float(score),"ku":ku,"kd":kd,"kh":kh,"eps":float(ep),
                  "phi":float(phi),**values})
top=sorted(scan,key=lambda r:r["score"])[:5]
all3_close=sum(all(.5<r[k]/target[k]<2 for k in ("Vus","Vcb","Vub")) for r in scan)
# Guaranteed analytic fact: if the theta slice is real-imag so all
# up and down Yukawa entries can be made real, CP invariant =0;
# here these particular inputs generally complex so test no overclaim.
out={"status":"TOE49_PASS11910_PHYSICAL_CKM_ENTRY_AUDIT",
"pass11910_measurement":"fourth largest magnitude of nine CKM entries is permutation-invariant; it is not literally the mass-ordered CKM (u,s) entry",
"target_reference_approximate":target,
"fixed_inputs":{"tau_up":str(tau_u),"tau_down":str(tau_d),
"up_zeta":str(zu),"down_zeta":str(zd),
"warning":"Different tau_up and tau_down contradict Pass11910's shared family-torus hypothesis; here used only to reproduce prior example and isolate the mixing metric."},
"repo_analog_at_eps_003":repo_equivalent,
"best_of_18_fixed_sector_choices_at_eps_003":best,
"extended_amplitude_phase_scan":{"count":len(scan),"all_3_target_entries_within_factor2_count":all3_close,"top_five":top},
"full_scan":records,
"physical_limit":"No global anomaly/tadpole-consistent compactification. CKM target is an approximate PDG-level comparator. VEV admixture coefficients chosen by hand and may not align with physical mass ordering. This checks the measurement of actual entries, not whether a scanned model predicts them."}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"repo":{k:repo_equivalent[k] for k in ("Vus","Vcb","Vub","J","fourth_largest")},"best":{k:best[k] for k in ("ku","kd","kh","Vus","Vcb","Vub","J")}}))
