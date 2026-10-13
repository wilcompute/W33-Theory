"""TOE65 signed native edge-product adversary: exact rational upper bound.

Derives integer polynomial for a fixed actual 160-edge 0/1 high/low
pattern; integer negative Rayleigh gives proof pi is not a local min.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261013_toe65_edge_product_adversary import C,W,SGN
from w33_20261013_toe64_signed_square_flux_robustness import certificate as robust_cert

def certificate():
    previous=json.loads((ROOT/"data/w33_20261013_toe65_edge_product_adversary.json").read_text())
    wit=previous["rational_30_percent_counterexample"]
    pattern=np.asarray(wit["high_edge_bits"],int)
    q=np.asarray(wit["integer_test_direction"],int)
    assert len(pattern)==160 and len(q)==3
    high_counts=(C@pattern).astype(int)
    coeff=[sum(int(SGN[i])*int(np.dot(W[i],q))**2
               for i,h in enumerate(high_counts) if h==j) for j in range(9)]
    assert len(coeff)==9
    def ray(e):
        return sum(coeff[j]*(1+e)**j*(1-e)**(8-j) for j in range(9))
    def integer_ray_at_fraction(n,d):
        return sum(coeff[j]*(d+n)**j*(d-n)**(8-j) for j in range(9))
    assert integer_ray_at_fraction(3,10)==wit["exact_integer_rayleigh_numerator"]
    assert ray(0)>0 and ray(.3)<0
    root=float(brentq(ray,0,.3,xtol=5e-16))
    p=next(i for i in range(1,300) if integer_ray_at_fraction(i,1000)<0)
    upper=int(p)
    assert integer_ray_at_fraction(p-1,1000)>=0
    strict_negative=int(integer_ray_at_fraction(p,1000))
    assert strict_negative<0
    lower=float(robust_cert()["critical_epsilon"])
    assert lower<upper/1000<.3
    return {"status":"PASS_TOE65_EXACT_RATIONAL_NATIVE_EDGE_DISORDER_COUNTEREXAMPLE",
            "native_winding_octagons":len(W),"native_edge_count":160,
            "edge_high_bits":pattern.tolist(),
            "integer_phase_test_direction":q.tolist(),
            "integer_polynomial_coeff_by_high_edge_count":coeff,
            "test_polynomial":"P(epsilon) = sum_{j=0}^8 A_j (1+epsilon)^j (1-epsilon)^(8-j), with A_j exact displayed integer coefficients; P = q^T Hess_pi q.",
            "polynomial_root_approx_for_this_fixed_pattern_and_direction":root,
            "first_negative_grid_epsilon_rational":f"{upper}/1000",
            "previous_grid_epsilon_rational":f"{upper-1}/1000",
            "exact_negative_integer_at_upper_fraction":strict_negative,
            "TOE64_proved_universal_lower_threshold":lower,
            "rigorous_universal_tolerance_interval":{
                "certified_at_least":lower,
                "cannot_reach":upper/1000,
            },
            "claim":"An explicitly given 160-edge positive rational hopping pattern at epsilon=p/1000 gives q^T Hess_pi q < 0 as an EXACT integer calculation, hence three-pi fails to be a local minimizer of the native leading high-temperature holonomy potential for this valid edge weighting. This is an actual W33 edge-product counterexample, not a relaxation of Fourier coefficients.",
            "scope":"Upper bound applies only to universal worst-case robustness of the leading beta7 term. No claim that the minimax threshold is sharp, nor that finite/all-temperature free-fermion or dynamical gauge minima agree."
    }
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261013_toe65_exact_edge_disorder_bracket.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["first_negative_grid_epsilon_rational"],c["exact_negative_integer_at_upper_fraction"],flush=True)
