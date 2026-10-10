"""Pass 11861: reflection-positivity bounds on the bulk couplings of the finite AdS4 (physical normalisation).

Bulk action (Euclidean, on the 36 Kramers reversals):
  S = 1/2 phi G15^+ phi + 1/2 chi Pi20 chi + g3/3! sum phi^3 + g4/4! sum phi^4 + g'/2 sum phi^2 chi,
with the crosscap propagator G15 = 12 Pi_15 (Pass 11839) and the hidden 20 with unit propagator Pi_20.
Boundary operators are unit-normalised: O_x = sum_p N(x,p) phi_p / sqrt(216), so <O O> = Pi_15 (the boundary 15).
Tree-level boundary four-point function = D (disconnected) - g4 C + g3^2 E15 + g'^2 E20, with K = N G15 / sqrt(216).
Reflection positivity: the s-channel operator on 15 x 15 must be positive semidefinite.  Its channel eigenvalues
(Pass 11856) give linear inequalities in (g4, g3^2, g'^2): exact bounds are computed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11847_finite_bulk_path_integral as BP  # noqa: E402
import w33_pass11852_bulk_four_point as FP  # noqa: E402
import w33_pass11856_boundary_bootstrap_channels as BC  # noqa: E402

OUT = ROOT / "data" / "w33_pass11861_bootstrap_positivity_bounds.json"


def main():
    K36, X, A, G, N, Cx = BP.setup()
    P = BP.eigenprojectors(A)
    P15, P20 = P[3.0], P[-3.0]
    G15 = 12 * P15
    Kb = N @ G15 / np.sqrt(216)
    Pb = BP.eigenprojectors(Cx)[-4.0]
    w, V = np.linalg.eigh(Pb)
    U = V[:, w > 0.5]
    two = (N @ G15 @ N.T) / 216
    assert np.allclose(two, Pb)
    Cw = np.einsum("xp,yp,zp,wp->xyzw", Kb, Kb, Kb, Kb)
    E15 = FP.channels(Kb, G15)
    E20 = FP.channels(Kb, P20)
    Dw = (np.einsum("xz,yw->xyzw", Pb, Pb) + np.einsum("xw,yz->xyzw", Pb, Pb) + np.einsum("xy,zw->xyzw", Pb, Pb))
    mats = {nm: BC.to15(W, U).reshape(225, 225) for nm, W in (("C", Cw), ("E15", E15), ("E20", E20), ("D", Dw))}
    swap = np.zeros((225, 225))
    for a in range(15):
        for b in range(15):
            swap[a * 15 + b, b * 15 + a] = 1
    gen = mats["C"] / abs(mats["C"]).max() + np.pi * mats["E15"] / abs(mats["E15"]).max() + np.e * mats["E20"] / abs(mats["E20"]).max() \
        + np.sqrt(2) * mats["D"] + 0.123 * swap
    gen = (gen + gen.T) / 2
    ev, Qm = np.linalg.eigh(gen)
    clusters = []
    for i, x in enumerate(ev):
        if clusters and abs(x - clusters[-1]["val"]) < 1e-7:
            clusters[-1]["idx"].append(i)
        else:
            clusters.append(dict(val=x, idx=[i]))
    table = []
    for cl in clusters:
        Vk = Qm[:, cl["idx"]]
        row = dict(dim=len(cl["idx"]))
        for nm, Mx in list(mats.items()) + [("swap", swap)]:
            row[nm] = float(np.trace(Vk.T @ Mx @ Vk) / len(cl["idx"]))
        table.append(row)
    res = {"pass_id": 11861, "convention": "unit-normalised boundary operators; tree 4pt = D - g4 C + g3^2 E15 + g'^2 E20",
           "channels": [{k: (round(v, 8) if isinstance(v, float) else v) for k, v in r.items()} for r in table]}
    sym = [r for r in table if r["swap"] > 0]
    # bounds
    ch = {r["dim"]: r for r in sym}
    b = {}
    r60, r24 = ch[60], ch[24]
    if r60["E15"] < 0:
        b["g3_squared_max_from_60_channel"] = r60["D"] / -r60["E15"]
    if r24["E20"] < 0:
        b["g_prime_squared_max_at_g3_zero_from_24_channel"] = r24["D"] / -r24["E20"]
        b["24_channel_relation"] = f"{r24['D']:.6f} + {r24['E15']:.6f} g3^2 + {r24['E20']:.6f} g'^2 >= 0"
    for d in (1, 15, 20):
        r = ch[d]
        b[f"channel_{d}"] = f"{r['D']:.6f} - {r['C']:.6f} g4 + {r['E15']:.6f} g3^2 + {r['E20']:.6f} g'^2 >= 0"
    # quartic window at g3 = g' = 0
    lo, hi = -np.inf, np.inf
    for r in sym:
        if abs(r["C"]) > 1e-12:
            bound = r["D"] / r["C"]
            if r["C"] > 0:
                hi = min(hi, bound)
            else:
                lo = max(lo, bound)
    b["g4_window_at_g3_gprime_zero"] = [lo if np.isfinite(lo) else None, hi]
    res["bounds"] = b
    json.dump(res, open(OUT, "w"), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
