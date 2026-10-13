"""TOE55 controlled *free-band* a->0 scaling of the TOE54 W33 photons.

This is only a formal fixed-Bloch-symbol rescaling, not a
constructed W33 continuum quantum field theory or emergent gravity.
"""
import json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
v=json.loads((R/"data/w33_20261013_toe54_finite_lorentz_dispersion.json").read_text())
p0=.16
outrows=[]
for d in sorted(set(x["direction"] for x in v["samples"])):
 rows={round(x["radius"],4):x for x in v["samples"] if x["direction"]==d}
 ascale=[1.,.5,.25]
 series=[]
 for a in ascale:
  e=rows[round(p0*a,4)]
  omegas=np.asarray(e["light_omega_sq"])
  ph=omegas/(a*a*p0*p0)
  delta=abs(np.mean(ph)-2)
  split=abs(ph[1]-ph[0])
  series.append(dict(a=a, omega2_over_a2=(omegas/(a*a)).tolist(),
   squared_phase_speeds=ph.tolist(),
   mean_speed_squared=float(np.mean(ph)),
   mean_speed_squared_absolute_error=float(delta),
   squared_polarization_difference=float(split)))
 ratios=[series[i+1]["mean_speed_squared_absolute_error"]/
         series[i]["mean_speed_squared_absolute_error"] for i in (0,1)]
 splitratios=[series[i+1]["squared_polarization_difference"]/
         series[i]["squared_polarization_difference"] for i in (0,1)]
 assert all(.12<x<.38 for x in ratios),(d,ratios)
 assert all(.1<x<.45 for x in splitratios),(d,splitratios)
 outrows.append(dict(direction=d,sequence=series,mean_speed_error_halving_ratios=ratios,
                     polarization_split_halving_ratios=splitratios))
out={"status":"PASS_FORMAL_FIXED_FREE_BAND_A2_CORRECTION_SUPPRESSION",
 "model":"TOE54 actual native W33 two lowest positive bands; pphysical dimensionless comparison fixed |p|=0.16 and a in {1,1/2,1/4}",
 "definition":"omega_a²(p)=lambda_W33(a*p)/a², with external time rescaling; compare omega_a²/p² to 2.",
 "per_direction":outrows,"n_directions":len(outrows),
 "reference_scaling":"For a smooth even low-energy dispersion lambda(k)=2|k|² + O(|k|^4), the rescaled correction is O(a² |p|^4). The sampled halving ratios are compatible with this, not an exact proof of a differentiable interacting QFT continuum.",
 "physical_gate":"Scaling a formal Fourier variable and energy by hand does not determine a physical graph spacing or coarse-graining of interacting couplings, a renormalization-group flow, Ward identities of quantized photons, or gravity. A W33 sequence of refined local systems is not constructed.",
 "input_certificate":"data/w33_20261013_toe54_finite_lorentz_dispersion.json"}
(R/"data/w33_20261013_toe55_free_bloch_scaling.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"directions":len(outrows),
 "ratios":{x["direction"]:x["mean_speed_error_halving_ratios"] for x in outrows}}))
