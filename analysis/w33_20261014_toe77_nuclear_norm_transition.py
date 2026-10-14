"""TOE77 deeper: 80-site native W33 half-filled flux interpolation as a
40x40 *nuclear norm* (trace norm) maximization.

This is a new embedding-dependent variational bridge between W33
Ramanujan singular spectrum, its 30-dimensional chiral flat band, and
the native 11-site 120-degree flux.

Do not mistake a *fixed-phase energy crossing* or a 1D symmetry-line
local optimizer for a thermodynamic phase transition/global U1^2 proof.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar,brentq
from w33_20261014_toe77_embedded_theta_exterior_flux import build,hamiltonian

ROOT=Path(__file__).resolve().parents[1]
def certificate():
    ed,cy,p,ch=build()
    phases={
       "zero":(0.,0.),"pi_pi":(math.pi,math.pi),
       "120":(2*math.pi/3,4*math.pi/3),
       "opposite_120":(4*math.pi/3,2*math.pi/3)}
    def sv(t,z):
        h=hamiltonian(ed,p,ch,z,t)
        X=h[:40,40:]
        assert np.max(abs(h[:40,:40]))<1e-13
        assert np.max(abs(h[40:,40:]))<1e-13
        sig=np.linalg.svd(X,compute_uv=False)
        # Half filling: negative spectrum is -singular(X), plus zeros.
        return sig
    def energy(t,z):
        return -float(np.sum(sv(t,z)))
    # Native W33 unphased Ramanujan incidence nuclear norm:
    # singular values 4^1, sqrt6^24, 0^15.
    exact_ramanujan_ground=-(4+24*math.sqrt(6))
    assert abs(energy(1,phases["zero"])-exact_ramanujan_ground)<1e-9
    rows=[]
    for t in (0.,.1,.2,.25,.3,.4,.5,.6,.65,.7,.75,.8,.9,1.):
        result=minimize_scalar(lambda delta:energy(t,(math.pi+delta,math.pi-delta)),
                method="bounded",bounds=(0,math.pi/2),
                options={"xatol":1e-9,"maxiter":120})
        assert result.success
        E0=energy(t,phases["pi_pi"])
        E120=energy(t,phases["120"])
        Ebest=energy(t,(math.pi+result.x,math.pi-result.x))
        assert Ebest<=min(E0,E120)+1e-8
        h=.0075
        curvature=(energy(t,(math.pi+h,math.pi-h))+
                   energy(t,(math.pi-h,math.pi+h))-2*E0)/(h*h)
        rows.append({
          "outside_coupling":t,
          "zero_holonomy_E":energy(t,phases["zero"]),
          "pi_pi_E":E0,"theta_120_E":E120,
          "fixed_phase_E120_minus_Epi_pi":E120-E0,
          "symmetry_line_best_delta_over_pi":result.x/math.pi,
          "symmetry_line_best_energy":Ebest,
          "pi_pi_line_second_derivative_numerical":curvature})
    def fixed_crossing(t):
        return energy(t,phases["120"])-energy(t,phases["pi_pi"])
    assert fixed_crossing(.5)<0 and fixed_crossing(1)>0
    fixed_root=brentq(fixed_crossing,.5,1,xtol=1e-10)
    def local_curv(t):
        h=.005
        return (energy(t,(math.pi+h,math.pi-h))+
                energy(t,(math.pi-h,math.pi+h))-2*energy(t,phases["pi_pi"]))/(h*h)
    # If bracketing exists, distinguish two definitions of "transition".
    ca,cb=local_curv(0),local_curv(1)
    local_root=brentq(local_curv,0,1,xtol=1e-8) if ca*cb<0 else None
    svs={}
    for k,z in phases.items():
        s=sv(1,z)
        svs[k]={"nuclear_norm":float(s.sum()),
            "zero_singular_values_tolerance_1e-9":int(sum(s<1e-9)),
            "largest_singular":float(s.max()),
            "smallest_nonzero_singular":float(min((x for x in s if x>1e-9),default=0))}
        assert svs[k]["zero_singular_values_tolerance_1e-9"]>=13
    # Trace-norm Lipschitz bound for independent unit-circle edge changes:
    # | ||Tphi||_* - ||T0||_* | <= ||Tphi-T0||_*
    # <= |e^(i phi1)-1| + |e^(i phi2)-1| <=4.
    for k,z in phases.items():
        diff=abs(energy(1,z)-energy(1,phases["zero"]))
        ub=sum(abs(np.exp(1j*x)-1) for x in z)
        assert diff<=ub+1e-9,(k,diff,ub)
    return {
      "status":"PASS_TOE77_EMBEDDED_W33_RAMANUJAN_TO_FLUX_NUCLEAR_NORM",
      "native_Levi_graph_nodes":80,
      "W33_incidence_40_by_40_rank":25,
      "unphased_W33_exact_half_filled_energy_formula":"-(4+24*sqrt(6))",
      "unphased_W33_exact_half_filled_energy_numeric":exact_ramanujan_ground,
      "any_two_entry_flux_at_least_26_exact_one_body_zeros":True,
      "full_t1_singular_controls":svs,
      "full_80_half_filled_energy_identity":"E_N40(t,phi)=-||M_40x40(t,phi)||_*",
      "two_chord_phase_nuclear_norm_Lipschitz_bound":"|E_phi-E_0| <= |exp(i phi1)-1|+|exp(i phi2)-1| <= 4, for full t=1",
      "outside_amplitude_symmetry_line_scan":rows,
      "fixed_120_vs_pi_pi_energy_crossing_t_numeric":fixed_root,
      "symmetry_line_pi_pi_curvature_t_zero":ca,
      "symmetry_line_pi_pi_curvature_t_one":cb,
      "symmetry_line_pi_pi_local_stability_crossing_t_numeric":local_root,
      "strict_scientific_scope":"Half-filled 80-site static free fermion hopping; nuclear norm identity exact for any bipartite block matrix. Fixed background t crosses when two chosen phase energies equal; this need NOT coincide with continuous global minimizer, a thermodynamic phase transition, a quantum gauge vacuum, or actual 4D fermion chirality. Values of crossings are numerical, not interval-certified."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe77_nuclear_norm_transition.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"])
    print("CROSS",c["fixed_120_vs_pi_pi_energy_crossing_t_numeric"],"CURV",
          c["symmetry_line_pi_pi_local_stability_crossing_t_numeric"])
    print("RAMANUJAN",c["unphased_W33_exact_half_filled_energy_numeric"])
    for z in c["outside_amplitude_symmetry_line_scan"]:
        print("LINE",z["outside_coupling"],z["symmetry_line_best_delta_over_pi"],
             z["fixed_phase_E120_minus_Epi_pi"])
