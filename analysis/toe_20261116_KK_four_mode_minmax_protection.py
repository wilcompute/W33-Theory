"""Four-mode min-max protection of equal-flux square-torus BF instability.

Equal-flux square torus has 4 signed primitive |k|²=1 modes.
For each, the known sphere-odd gauge-constrained physical block
has mass eigenvalue m0 =3*pi-2-sqrt(4+48*pi)<-4.
Next shell |k|²=2 has lambda=6*pi>12, thus no other
instabilities in this particular branch on the square torus.
The 4 real cosine/sine modes span a degenerate negative subspace.

If physical unequal-flux and higher-derivative normalized
self-adjoint operators H_N exist on the same Hilbert space and
||H_N-H0||<= K*|eta(N)-1/2| + C*(lp/L)^6,
the min-max principle puts AT LEAST FOUR real BF-violating
modes below -4 whenever the right side < gap0.
K,C are UNKNOWN from the full 11D action. Numeric thresholds
are sufficient conditions GIVEN assumed constants, not new
physical 11D eigenvalues.
"""
from pathlib import Path
from decimal import Decimal
import json,math
import numpy as np
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_near_equal_flux_BF_scaling import case as near
OUT=ROOT/"data"/"toe_20261116_KK_four_mode_minmax_certificate.json"
PI=math.pi
LAMBDA=3*PI
M0=LAMBDA-2-math.sqrt(4+16*LAMBDA)
GAP=-4-M0
def testN(N,K=5.,C=100.):
    if N<1 or K<0 or C<0:raise ValueError("bad bounds")
    n=near(N)
    eta=float(Decimal(n["eta"]))
    eps=float(Decimal(n["lp_over_L_to_sixth"]))
    norm=K*abs(eta-.5)+C*eps
    return {"N":N,"eta":eta,"eta_displacement":abs(eta-.5),
      "hypothetical_K":K,"hypothetical_C":C,
      "operator_norm_upper":norm,
      "BF_gap_equal":GAP,
      "at_least_four_unstable_if_bound_proven":norm<GAP}
def wavevectors():
    return [(kx,ky) for kx in range(-2,3) for ky in range(-2,3)
            if 0<kx*kx+ky*ky<12/(3*PI)]
def verify():
    assert wavevectors()==[(-1,0),(0,-1),(0,1),(1,0)]
    rows=[testN(n) for n in (2,5,10,20,50,100,500)]
    assert rows[-1]["at_least_four_unstable_if_bound_proven"]
    for K in (1.,5.,10.,20.,50.):
        threshold=next((N for N in range(2,201)
                        if testN(N,K,100.)["at_least_four_unstable_if_bound_proven"]),None)
        assert threshold is not None
    else:
        threshold=None
    # A random self-adjoint 4x4 perturbation with spectral norm eps
    # cannot move any of the four modes through the BF bound.
    rng=np.random.default_rng(20261116)
    m=np.array([[float(x) for x in row] for row in
                [[1,2,-2,0],[2,0,4,1],[-2,4,-1,0],[0,1,0,1]]])
    m=(m+m.T)/2
    m=m/np.linalg.norm(m,ord=2)
    deltan=GAP*.75
    eig=np.linalg.eigvalsh(M0*np.eye(4)+deltan*m)
    assert len(eig)==4 and max(eig)<-4
    # An arbitrary perturbation with norm exceeding the gap can
    # lift a mode; continuity alone gives no finite-N theorem.
    bad=np.linalg.eigvalsh(M0*np.eye(4)+1.2*GAP*np.eye(4))
    assert min(bad)>-4
    thresholds=[]
    for K in (1.,5.,10.,20.,50.):
        Ns=range(2,201)
        first=next(N for N in Ns if testN(N,K,100.)["at_least_four_unstable_if_bound_proven"])
        thresholds.append({"assumed_norm_derivative_K":K,"assumed_R4_C":100.,
                           "first_N_with_sufficient_bound":first})
    return {"status":"PASS_FOUR_MODE_SQUARE_TORUS_KK_MINMAX_BOUND",
      "primitive_wavevectors":wavevectors(),
      "real_physical_cos_sin_mode_count":4,
      "equal_flux_lower_m2L2":M0,"classical_BF_gap":GAP,
      "next_shell_at_6pi_stable_in_this_branch":True,
      "minmax_theorem":"For a self-adjoint canonical H_N with >=4D subspace of H0 quadratic form <=-4-gap0, and ||H_N-H0||<gap0, H_N has >=4 eigenvalues below -4.",
      "hypothetical_physical_norm_bound":"||H_N-H_equal|| <= K*|eta(N)-1/2| + C*(lp/L)^6, where K and C MUST be computed from the actual gauge-constrained 11D operator.",
      "illustrative_sufficient_N":thresholds,
      "random_matrix_sanity":{"max_eigen_after_bounded_perturb":float(max(eig)),
                             "oversized_shift_can_heal_all":bool(min(bad)>-4)},
      "samples_for_K_5_C_100":rows,
      "no_physical_unequal_flux_spectrum_claimed":True}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(r["status"],r["illustrative_sufficient_N"])
