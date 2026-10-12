"""Pass 11937: the special Clifford orbits degenerate the compactification torus onto the elliptic points of its
boundary curve.

Displace the E8 Cartan vev off a Witting ray along a tangent direction u, c = (1, t u), and invert to the Siegel modulus
(Pass 11936). Near the ray Omega runs to a one-dimensional cusp: one diagonal entry goes to i infinity like
(3/pi) ln(1/t), the other stays finite -- it is the modulus tau' of the boundary elliptic curve. For the special orbits of
Pass 11926 (polished representatives):
* the log(8/5) orbit -- the direction selected by the E8 soft-supertrace dynamics (Pass 11935) -- gives tau' = i exactly
  (j = 1728): the boundary curve is the SQUARE torus;
* the T / log(9/5) orbit gives tau' = w exactly (j = 0): the HEXAGONAL torus;
* the stabiliser direction runs into the deeper cusp (both diagonal entries large);
* the strange direction leaves Omega fixed (a degenerate Maschke direction).
On the selected log(8/5) orbit the light theta-Yukawa ratio b/a (m_u/m_c at the cusp, Pass 11936) is 0.7962 for ALL 54
members (frozen scan: every member gives j = 1728, b/a = 0.796, s2/t = 0.465). On the T orbit b/a depends on the member
(0.65 / 0.49 seen): the 3x3 reshape is only invariant under the local Clifford group.
Reading: the up/charm ratio is decided by the boundary elliptic curve, and the E8 dynamics pins it to an elliptic point;
a small m_u/m_c would need the boundary curve itself to approach its own cusp (a second, slower degeneration: a corner
cusp with nome q' as the second small parameter), which the selected direction does not do.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11874_11878_siegel_fixed_points_cp_magic as S  # noqa: E402
import w33_pass11890_11892_vacuum_phase_diagram as V  # noqa: E402
import w33_pass11923_stabiliser_higgs_lock as H23  # noqa: E402
import w33_pass11926_g25_tangent_vacua as G26  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import j_of_tau, theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11937_boundary_elliptic_points.json"
FZ = ROOT / "data" / "w33_pass11926_orbit_reps_frozen.json"


def reduce_tau(tau):
    for _ in range(60):
        tau = tau - round(tau.real)
        if abs(tau) < 1 - 1e-12:
            tau = -1 / tau
        else:
            break
    return tau


def main():
    rng = np.random.default_rng(11937)
    G = G26.clifford()
    rows = {}
    for rec in json.loads(FZ.read_text())["orbits"]:
        u, st = G26.polish(np.array(rec["re"]) + 1j * np.array(rec["im"]), G)
        m2 = float(H23.magic(u))
        if m2 > 0.69:
            continue                     # strange orbit and the 0.6908 orbit: not a one-dimensional cusp at this t
        guess, sp = None, []
        for t in (0.01, 0.005):
            c = np.r_[1, t * u]
            c /= np.linalg.norm(c)
            Om, res, guess = V.invert(c, rng, guess)
            Om = S.siegel_reduce(Om)
            d = np.diag(Om)
            tau = reduce_tau(d[int(np.argmin(d.imag))])
            sv = np.linalg.svd(theta_null_2(Om, N=40).reshape(3, 3), compute_uv=False)
            sp.append(dict(t=t, residual=float(res), im_diag=[float(x) for x in d.imag], tau=[float(tau.real), float(tau.imag)],
                           j=[float(complex(j_of_tau(tau)).real), float(complex(j_of_tau(tau)).imag)],
                           s2=float(sv[1] / sv[0]), s3=float(sv[2] / sv[0])))
        rows["M2=%.4f" % m2] = dict(stabiliser=int(st), points=sp, b_over_a=sp[-1]["s3"] / sp[-1]["s2"])
    MEM = json.loads((ROOT / "data" / "w33_pass11937_log85_orbit_members_frozen.json").read_text())["members"]
    res = dict(pass_id=11937, orbits=rows, log85_members=len(MEM))
    L = rows["M2=0.4700"]["points"]
    T = rows["M2=0.5878"]["points"]
    W = np.exp(2j * np.pi / 3)
    dist = lambda p, z: min(abs(complex(*p["tau"]) - z), abs(complex(*p["tau"]) - z - 1), abs(complex(*p["tau"]) - z + 1))
    res["checks"] = {k: bool(v) for k, v in dict(
        inversions_converged=max(p["residual"] for r in rows.values() for p in r["points"]) < 1e-8,
        log85_boundary_is_square=all(dist(p, 1j) < 1e-8 and abs(p["j"][0] - 1728) < 1e-4 for p in L),
        t_orbit_boundary_is_hexagonal=all(min(dist(p, W), dist(p, W + 1)) < 1e-8 and abs(complex(*p["j"])) < 1e-4 for p in T),
        stabiliser_runs_to_deep_cusp=min(rows["M2=0.0000"]["points"][-1]["im_diag"]) > 10,
        log85_b_over_a=abs(rows["M2=0.4700"]["b_over_a"] - 0.7962) < 2e-3,
        log85_orbit_members_all_square=all(m["j"].startswith("1728") and abs(m["b_over_a"] - 0.796) < 2e-3 for m in MEM)
        and len(MEM) == 54,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"], {k: round(v["b_over_a"], 4) for k, v in rows.items()})


if __name__ == "__main__":
    main()
