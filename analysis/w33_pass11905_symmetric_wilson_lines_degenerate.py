"""Pass 11905: symmetric Wilson lines are degenerate -- the up hierarchy needs a non-symmetric Wilson-line vacuum.

Setting (Pass 11904): one family qutrit (flux 3 on the family torus), localised Higgs, masses (top, charm, up) =
|theta[c/3, 0](z, Omega)|, c = 0, +1, -1, with z the (continuous, magnetized) Wilson-line argument.

The level-3 Heisenberg-reflection group acting on z:  z -> z + 1,  z -> z + Omega/3 (characteristic shift c -> c + 1),
z -> -z (c -> -c).  Its reflections z -> -z + m + k Omega/3 have fixed points

    z = m/2 + k Omega/6,      m in {0, 1},  k in Z_6.

Theorem. At every such point two of the three masses coincide exactly:
    k = 0 mod 3: the light pair (m_c = m_u);   k = 1 mod 3: top = up;   k = 2 mod 3: top = charm.
Proof. theta[a](-z + m + k Omega/3) = (unit phase) x theta[-a - k/3](z) (shift and reflection formulas); at a fixed
point |theta[a](z)| = |theta[-a - k/3](z)|, pairing c <-> -c - k mod 3. The theta-zero law of Pass 11904 is the case
m = 1, k = 3(1 - 2a) (where additionally one theta vanishes).
Checks: 16 random Omega x the 36 points (u + v Omega)/6: coincidence exactly when u in {0, 3} (all v), with the pair
set by v mod 3; the other 24 points (not fixed points) show no coincidence; a generic z shows none.

Reading. Modular/Jacobi-invariant potentials for the Wilson-line modulus have their symmetric critical points exactly
here, and none of them can host m_t >> m_c >> m_u: each forces a pair of equal masses. In the Gaussian regime the
fixed points sit at offsets delta in {0, 1/6} (mod 1/3): locked or top = light. The hierarchy point of Pass 11904
(delta = 0.060) is not symmetric, so in the magnetized home the up hierarchy is a property of a generic (dynamically
selected, not symmetry-selected) Wilson-line vacuum.
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11905_symmetric_wilson_lines_degenerate.json"
N = np.arange(-40, 41)


def th(a, z, Om):
    return np.sum(np.exp(1j * np.pi * (N + a) ** 2 * Om + 2j * np.pi * (N + a) * z))


def main():
    rng = np.random.default_rng(11905)
    table = {}
    exact_ok, nonfixed_clean = True, True
    worst_fixed, min_nonfixed = 0.0, 1.0
    for _ in range(16):
        Om = rng.normal() * 0.6 + 1j * (0.5 + 1.5 * rng.random())
        for u in range(6):
            for v in range(6):
                z = (u + v * Om) / 6
                m = np.array([abs(th(c / 3, z, Om)) for c in range(3)])
                m = m / m.max()
                d = {(i, j): abs(m[i] - m[j]) for i, j in ((0, 1), (0, 2), (1, 2))}
                eq = sorted(k for k, x in d.items() if x < 1e-12)
                fixed = u in (0, 3)
                if fixed:
                    k = v % 3
                    want = [(1, 2)] if k == 0 else ([(0, 2)] if k == 1 else [(0, 1)])
                    exact_ok &= eq == want
                    worst_fixed = max(worst_fixed, min(d.values()))
                else:
                    nonfixed_clean &= eq == []
                    min_nonfixed = min(min_nonfixed, min(d.values()))
                table.setdefault(f"{u},{v}", set()).add(str(eq))
    Om, z = 0.3 + 1.1j, 0.11 + 0.23j
    g = [abs(th(c / 3, z, Om)) for c in range(3)]
    generic_spread = float((max(g) - min(g)) / max(g))
    # Gaussian offsets of the fixed points (z = -i delta Im Omega convention): delta = -k/6 mod 1/3 -> {0, 1/6}
    offsets = sorted({round((k / 6) % (1 / 3), 6) for k in range(6)})
    res = dict(pass_id=11905, pair_table={k: sorted(v) for k, v in table.items()}, worst_fixed_point_pair_gap=worst_fixed,
               min_nonfixed_pair_gap=min_nonfixed, generic_spread=generic_spread, fixed_point_offsets=offsets,
               pass11904_hierarchy_offset=0.0603)
    res["checks"] = {k: bool(v) for k, v in dict(
        coincidence_exactly_at_fixed_points=exact_ok,
        pair_set_by_k_mod_3=exact_ok,
        no_coincidence_off_fixed_points=nonfixed_clean and min_nonfixed > 1e-6,
        generic_control=generic_spread > 0.05,
        fixed_offsets_0_and_one_sixth=offsets == [0.0, round(1 / 6, 6)],
        hierarchy_point_not_symmetric=all(abs(0.0603 - o) > 0.05 for o in offsets + [1 / 3]),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: res[k] for k in ("worst_fixed_point_pair_gap", "min_nonfixed_pair_gap", "fixed_point_offsets",
                                          "checks", "all_checks_pass")}, indent=1))


if __name__ == "__main__":
    main()
