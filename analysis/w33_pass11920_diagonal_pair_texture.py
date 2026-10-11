"""Pass 11920: the diagonal-pair texture -- quantised Gaussian slopes, robust m_d = m_e = 0, and what the A2 model can and
cannot reach once SU(5) is broken by a hypercharge Wilson line.

1. Slopes. At a scalar modulus Omega = i t 1 and symmetric (zero) Wilson lines, every single-Higgs log singular-value ratio
   is linear in t with slope an integer multiple of pi/3 (checked: slope * 3 / pi within 1e-2 of an integer):
   A2 down delta = s2/s1: -4/3, -2/3 (and 0); A2 up: -4/3 (s2/s1), -2/3 (s3/s2); (1,1,4) down: -5/3, -1, -1/3.
   The quantum is pi m/3 times a coset norm (the (3/m)-metric Gaussian of Pass 11917).
2. Up degeneracy at symmetric Wilson lines: the A2 up spectrum is always (1, x, x) or (1, 1, x) (Pass 11918's lemma),
   so a parameter-free fit of (t, beta) to m_c/m_t, m_u/m_c has no solution; the hypercharge Wilson line is required.
3. Robust zeros: with the hypercharge Wilson line the A2 down AND lepton Yukawas remain dual-pair Yukawas, so by Pass
   11917 m_d = m_e = 0 exactly for every modulus, Wilson line and Higgs mode (scan maxima ~1e-7 are theta-truncation residuals at K = 4; the worst sample recomputed with K = 7 gives 3e-15).
4. Frozen scan (data/w33_pass11920_a2_scan_frozen.json): distributions of m_s/m_b, m_mu/m_tau and the up ratios,
   best fits, and the down/lepton splitting produced by w.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11918_hypercharge_wilson_scan as S  # noqa: E402

OUT = ROOT / "data" / "w33_pass11920_diagonal_pair_texture.json"
FROZEN = ROOT / "data" / "w33_pass11920_a2_scan_frozen.json"
A2, A2m = [[2, 1], [1, 2]], [[2, -1], [-1, 2]]
P114, P114d = [[1, 1], [1, 4]], [[4, -1], [-1, 1]]


def slopes(N1, N2, ts=(1.2, 1.6, 2.0, 2.4), G=12):
    rows = []
    for t in ts:
        T = F.T4(1j * t * np.eye(2), G)
        rows.append(np.array([np.linalg.svd(Y, compute_uv=False) for Y in F.yukawas(T, N1, N2)]))
    R = np.array(rows)
    out = {}
    for name, (i, j) in (("s2/s1", (1, 0)), ("s3/s2", (2, 1))):
        r = R[:, :, i] / R[:, :, j]
        ok = np.all(r > 1e-12, 0)
        sl = np.polyfit(ts, np.log(r[:, ok]), 1)[0] * 3 / np.pi
        out[name] = sl
    return out


def main():
    res = dict(pass_id=11920)
    sl = {"A2 down": slopes(A2, A2m), "A2 up": slopes(A2, A2), "114 down": slopes(P114, P114d)}
    flat = np.concatenate([v for d in sl.values() for v in d.values()])
    res["slopes_times_3_over_pi"] = {k: {kk: sorted(set(np.round(vv, 3).tolist())) for kk, vv in d.items()} for k, d in sl.items()}
    res["slope_max_dev_from_integer"] = float(np.max(abs(flat - np.round(flat))))
    # up degeneracy at symmetric Wilson lines (A2, entangled modulus)
    J = np.array([[0, 1], [1, 0]])
    gaps = []
    for t, b in ((1.0, 0.3), (1.5, -0.4), (2.0, 0.6)):
        for Y in F.yukawas(F.T4(1j * t * (np.eye(2) + b * J), 12), A2, A2):
            s = np.linalg.svd(Y, compute_uv=False)
            gaps.append(min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0])
    res["a2_up_symmetric_wilson_max_gap"] = float(max(gaps))
    # one reproducible sample of the frozen scan
    fz = json.loads(FROZEN.read_text())
    rows = S.sample(fz["check_seed"], 1, "A2")
    res["reproduced_rows_max_diff"] = float(np.max(abs(rows[:, 5:] - np.array(fz["check_rows"])[:, 5:])))
    res["frozen"] = {k: v for k, v in fz.items() if k not in ("check_rows",)}
    # the frozen maxima of m_d/m_s, m_e/m_mu (~1e-7) are theta-truncation residuals: recompute the worst sample with K = 7
    worst = S.sample(5, 47, "A2", only=[46], K=7)
    res["worst_sample_K7_max_md_ms"] = float(worst[:, 5].max())
    res["worst_sample_K7_max_me_mmu"] = float(worst[:, 9].max())
    res["checks"] = {k: bool(v) for k, v in dict(
        slopes_are_multiples_of_pi_over_3=res["slope_max_dev_from_integer"] < 1e-2,
        a2_up_degenerate_at_symmetric_wilson=res["a2_up_symmetric_wilson_max_gap"] < 1e-10,
        a2_md_me_zero_under_hypercharge=fz["max_md_ms"] < 1e-6 and fz["max_me_mmu"] < 1e-6
        and res["worst_sample_K7_max_md_ms"] < 1e-12 and res["worst_sample_K7_max_me_mmu"] < 1e-12,
        no_realistic_mass_row_has_hierarchical_ckm=fz["realistic_mass_and_hier_nonzero_ckm"] == 0,
        frozen_scan_reproduces=res["reproduced_rows_max_diff"] < 1e-8,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
