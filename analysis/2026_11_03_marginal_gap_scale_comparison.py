#!/usr/bin/env python3
"""Outside-box dynamic mass selection vs passive Pascal geometric RG.

One-dimensional lattice Dirac mean-field gap equation has logarithmic
infrared divergence and nonperturbative exponential gap. The gap equation
is an ASSUMED interacting model, not derived from W33, E8, or spacetime.
"""
from pathlib import Path
import numpy as np,math,json
from scipy.special import ellipk
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_marginal_gap_scale_comparison.json"
def gap_integral(m):
    return 2/(np.pi*np.sqrt(1+m*m))*ellipk(1/(1+m*m))
def run():
    rows=[]
    for g in (.2,.25,.3,.35,.4,.5,.7):
        m=brentq(lambda x:gap_integral(x)-1/g,1e-10,20.,xtol=1e-14)
        asym=4*math.exp(-math.pi/(2*g))
        assert abs(gap_integral(m)-1/g)<1e-8
        rows.append({"coupling_g":g,"mean_field_gap_over_lattice_UV":m,
                     "asymptotic_weak_coupling_formula":asym,
                     "gap_to_asymptotic_ratio":m/asym})
    assert abs(rows[0]["gap_to_asymptotic_ratio"]-1)<.01
    Ls=[64,256,1024,4096]
    finite=[]
    for L in Ls:
        k=2*np.pi*(np.arange(L)+.5)/L
        f0=float(np.mean(1/np.abs(np.sin(k))))
        gc=1/f0
        finite.append({"antiperiodic_lattice_sites":L,
          "finite_vol_critical_g":gc,
          "susceptibility_at_m_zero":f0})
    assert all(finite[i+1]["finite_vol_critical_g"]<
               finite[i]["finite_vol_critical_g"] for i in range(len(finite)-1))
    g=.2
    ratio=rows[0]["mean_field_gap_over_lattice_UV"]
    targets=[{"UV_inverse_length_inv_m":UV,
               "dimensional_gap_inv_m":UV*ratio,
               "gap_to_UV_ratio_invariant":ratio}
             for UV in (1.,1e6,1e30)]
    ans={"status":"PASS_MARGINAL_INTERACTING_GAP_VERSUS_PASCAL_LINEAR_RG",
      "gap_equation":"1/g=integral_{-pi}^pi dk/(2pi) 1/sqrt(sin(k)^2+m^2) = [2/(pi sqrt(1+m²))] K(1/(1+m²))",
      "asymptotic":"For weak g>0, m ~ 4 exp[-pi/(2g)] in the declared massless lattice 1+1D Dirac mean-field gap model. The logarithm arises from linear zeros of sin k.",
      "mass_gap_table":rows,
      "antiperiodic_finite_size_controls":finite,
      "mass_unit_reparameterization":targets,
      "physical_scale_boundary":"A dimensionless interaction can dynamically produce a highly suppressed mass-to-UV ratio through a marginal logarithmic instability. It does not fix g or the dimensionful UV cutoff. Multiplying UV by an arbitrary factor multiplies physical gap by that factor with all dimensionless observables unchanged.",
      "pascal_contrast":"Prior Pascal exact Schur flow c_(n+1)=(7/15)c_n+O(c_n²) is a hyperbolic linear contraction, not this marginal logarithmic gap. Identifying the two requires a separately constructed interacting Hamiltonian and renormalization matching.",
      "physics_scope":"An explicitly supplied 1+1D mean-field gap equation, not a proof of Gross-Neveu continuum, a 3+1D UV completion, observed particle masses, gravity, emergent Lorentz signature, or TOE.",
      "sources":["https://doi.org/10.1103/PhysRevD.10.3235"]
    }
    OUT.write_text(json.dumps(ans,indent=2)+"\n")
    print("MARGINAL GAP",[(round(x["coupling_g"],2),round(x["mean_field_gap_over_lattice_UV"],8)) for x in rows],
      "finite_vol_gc",finite)
if __name__=="__main__":run()
