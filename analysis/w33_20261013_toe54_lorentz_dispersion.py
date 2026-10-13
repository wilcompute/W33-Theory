"""TOE54 W33 physics: exact finite-Bloch no-Lorentz theorem + verified deviations.

Conditional statement: Fixed native 3-deck finite-cell Maxwell plaquette
operator, fixed positive 160 edge weights, no continuum scaling.
"""
import numpy as np,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
cert=json.loads((R/"data/w33_pass11956_local_electric_metric.json").read_text())
w=np.array([float(x.split('/')[0])/float(x.split('/')[1]) if '/' in x else float(x) for x in cert["electric_link_weights"]])
assert len(w)==160 and np.min(w)>1/8
edges,volts,lookup,zero,comm,*_=prep()
assert len(zero)>1000 and len(comm)==3
loops=zero+comm
ws=1/np.sqrt(w)
directions={"axis_x":[1,0,0],"axis_y":[0,1,0],"axis_z":[0,0,1],
           "diagonal_xy":[1,1,0],"diagonal_xyz":[1,1,1],
           "skew":[2,-1,3]}
radii=[0.02,0.04,0.08,0.16]
rows=[]
for name,d in directions.items():
 u=np.array(d,dtype=float);u/=np.linalg.norm(u)
 for r in radii:
  k=r*u
  P=np.array([cycle_row(z,edges,volts,lookup,k) for z in loops])
  H=(P.conj().T@P)*ws[:,None]*ws[None,:]
  eig=np.linalg.eigvalsh(H)
  positive=eig[eig>1e-7]
  assert len(positive)>=3, (name,r,eig[:90])
  close=np.max(abs(P@gradient(edges,volts,k)))
  assert close<1e-9,(name,r,close)
  va=positive[:2]/(r*r)
  rows.append({"direction":name,"radius":r,"light_omega_sq":positive[:2].tolist(),
    "light_phase_velocity_sq":va.tolist(),
    "mean_light_phase_velocity_sq":float(np.mean(va)),
    "fractional_pol_split":float((positive[1]-positive[0])/np.mean(positive[:2])),
    "third_gapped_omega_sq":float(positive[2]),
    "max_P_gradient":float(close)})
  print(name,r,*va,flush=True)
# Compare asymptotic phase speed and finite-k corrections, with r and
# r/2 giving O(k^2) estimators that are not assumed universal.
bydir={}
for name in directions:
 d=[z for z in rows if z["direction"]==name]
 vx=[z["mean_light_phase_velocity_sq"] for z in d]
 diff=[v-2. for v in vx]
 a=(vx[1]-vx[0])/(radii[1]**2-radii[0]**2)
 bydir[name]={"squared_speed_at_r0p02":vx[0],
   "squared_speed_at_r0p16":vx[-1],
   "fractional_shift_r0p16_vs_2":(vx[-1]-2)/2,
   "r0p02_to_r0p04_quartic_proxy_slope":float(a),
   "relative_polarization_split_r0p16":d[-1]["fractional_pol_split"]}
# Exact theorem proof does NOT infer anisotropy from a few samples:
# For any finite Bloch trigonometric P(k), bounded H(k), the function
# det(H(k)-c^2 |k|^2 I) is real analytic. Were an eigenvalue exactly
# c²|k|² on a nonempty open ball U, analytic continuation would force
# det =0 for all k. For |k| arbitrarily large, spectrum(H) bounded
# while c²|k|² unbounded, contradiction.
# Numeric spectral bound using Frobenius: sum row length²/ min w.
nrm_bound=float(sum((len(walk)-1)**2 for walk in loops))/min(w)
assert nrm_bound>0
# Integer deck winding makes the entire finite-Bloch operator periodic.
kr=np.array([.13,-.07,.19])
Pkr=np.array([cycle_row(z,edges,volts,lookup,kr) for z in loops])
period_errors=[]
for j in range(3):
 shifted=kr.copy();shifted[j]+=2*np.pi
 Pshift=np.array([cycle_row(z,edges,volts,lookup,shifted) for z in loops])
 period_errors.append(float(np.max(abs(Pshift-Pkr))))
assert max(period_errors)<1e-12
has_deviation=any(abs(z["fractional_shift_r0p16_vs_2"])>1e-6 for z in bydir.values())
assert has_deviation
out={"status":"PASS_TOE54_FINITE_BLOCH_EXACT_GLOBAL_LORENTZ_OBSTRUCTION",
"source":"TOE38 native zero-winding 8-cycle + three commutator 2-complex; Pass11956 positive rational-centered weights",
"strict_theorem":"For any finite-cell translation-equivariant Bloch Maxwell operator with finitely many finite-range loops, fixed real positive edge weights and nonzero continuum speed c, NO band of its finite-dimensional positive magnetic matrix H(k)=W^-1/2 P(k)^†P(k)W^-1/2 can equal c²||k||² on ANY open neighborhood of real k. Proof: real-analytic det(H(k)-c²||k||² I) vanishing on a ball implies globally zero, but H(k) is uniformly bounded in real k whereas c²||k||² grows unbounded, contradiction. A local cone can only be leading-order or asymptotic under a separately proved continuum limit.",
"boundedness_from_finite_loops":"For every real k, each loop row has L summands of unit complex modulus, so ||P(k)||_F² <= sum_loop L², hence ||H(k)|| <= sum_loop L²/min(w).",
"rigorous_uniform_operator_norm_bound":nrm_bound,
"max_three_axis_2pi_Bloch_periodicity_residual":max(period_errors),
"analyticity_caveat":"H(k) is real analytic in all three real k for fixed W, and the characteristic determinant is real analytic. Branch labeling at degenerate k=0 is irrelevant: the determinant argument applies to the existence of ANY exact quadratic branch for all k in an open ball.",
"n_samples":len(rows),"squared_continuum_speed_target":2.0,
"samples":rows,"directional_finite_k_summary":bydir,
"physics_boundary":"No exact Lorentz invariance at finite lattice spacing for this specified finite-band model; does NOT forbid Lorentz-invariant continuum limits, approximate emergent relativity, nonlocal actions, or interactions restoring symmetry. Does not establish photons or gravity.",
"prior_art":"Generic bounded periodic lattice dispersion versus continuum light cone is standard lattice field theory/homogenization. New scoped to the chosen W33 Bloch Maxwell operator and quantified here; no claim of original general no-go theorem."}
(R/"data/w33_20261013_toe54_finite_lorentz_dispersion.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE54",json.dumps({"status":out["status"],"summary":bydir},indent=2),flush=True)
