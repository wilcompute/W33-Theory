"""Pass 11856: s-channel (OPE) decomposition of the boundary four-point function of the finite AdS4.

Boundary operators O_x on the 40 contexts span the boundary 15 (Pass 11847).  The four-point structures of Pass 11852
(contact C, 15-exchange E15, hidden-20 exchange E20) and the disconnected generalised-free part D are restricted to the
15 and read as s-channel operators on 15 x 15 (pairs (ab) -> (cd)).  They are Sp(4,3)-equivariant; their joint
eigenspaces are the OPE channels.  Each channel is identified by dimension and by characters (Sym^2 / Alt^2 of the 15
against the known irreducibles), and the channel coefficients (lambda_C, lambda_15, lambda_20, lambda_D) give the
bootstrap data: which channel each bulk diagram feeds, and whether a channel is fed only by the hidden 20.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11834_11837_singletons_bulk_poincare_e8 as S  # noqa: E402
import w33_pass11847_finite_bulk_path_integral as BP  # noqa: E402
import w33_pass11852_bulk_four_point as FP  # noqa: E402

OUT = ROOT / "data" / "w33_pass11856_boundary_bootstrap_channels.json"


def to15(W, U):
    return np.einsum("xa,yb,zc,wd,xyzw->abcd", U, U, U, U, W, optimize=True)


def channel_characters():
    keys, mats, Vs, index, _ = S.weil_group()
    C = S.characters(keys, mats, Vs, index)
    chie, chio, sq, perm = C["chie"], C["chio"], C["sq"], C["perm"]
    s15 = S.sym2(chie, sq)
    irr = {"1": np.ones(C["N"]), "15_S": s15, "20_b": perm["kramers36"] - 1 - s15, "24": chie * np.conj(chie) - 1,
           "15_D": chio * np.conj(chio) - 1, "10": S.alt2(chie, sq), "10*": np.conj(S.alt2(chie, sq)),
           "20_c": chie * np.conj(chio), "20_c*": np.conj(chie * np.conj(chio))}
    sym, alt = S.sym2(s15, sq), S.alt2(s15, sq)
    out = {}
    for nm, ch in (("Sym2_15", sym), ("Alt2_15", alt)):
        dec = {k: round(float(np.real(S.ip(ch, v))), 6) for k, v in irr.items()}
        dec = {k: v for k, v in dec.items() if abs(v) > 1e-6}
        covered = sum(v * round(float(np.real(irr[k][0]))) for k, v in dec.items())
        out[nm] = dict(norm=round(float(np.real(S.ip(ch, ch))), 6), known_constituents=dec, dims_covered=covered,
                       dim=round(float(np.real(ch[0]))))
    return out


def main():
    K36, X, A, G, N, Cx = BP.setup()
    P = BP.eigenprojectors(A)
    P15, P20 = P[3.0], P[-3.0]
    G15 = 12 * P15
    Kb = N @ G15
    Pb = BP.eigenprojectors(Cx)[-4.0]
    w, V = np.linalg.eigh(Pb)
    U = V[:, w > 0.5]  # 40 x 15
    Cw = np.einsum("xp,yp,zp,wp->xyzw", Kb, Kb, Kb, Kb)
    E15 = FP.channels(Kb, G15)
    E20 = FP.channels(Kb, P20)
    G2 = Pb
    Dw = (np.einsum("xz,yw->xyzw", G2, G2) + np.einsum("xw,yz->xyzw", G2, G2) + np.einsum("xy,zw->xyzw", G2, G2))
    mats = {}
    for nm, W in (("C", Cw), ("E15", E15), ("E20", E20), ("D", Dw)):
        T4 = to15(W, U)
        mats[nm] = T4.reshape(225, 225)
    for nm in mats:
        mats[nm] = mats[nm] / np.max(abs(mats[nm]))
    swap = np.zeros((225, 225))
    for a in range(15):
        for b in range(15):
            swap[a * 15 + b, b * 15 + a] = 1
    gen = mats["C"] + np.pi * mats["E15"] + np.e * mats["E20"] + np.sqrt(2) * mats["D"] + 0.123 * swap
    gen = (gen + gen.T) / 2
    ev, Q = np.linalg.eigh(gen)
    clusters = []
    for i, x in enumerate(ev):
        if clusters and abs(x - clusters[-1]["val"]) < 1e-7:
            clusters[-1]["idx"].append(i)
        else:
            clusters.append(dict(val=x, idx=[i]))
    table = []
    for cl in clusters:
        Vk = Q[:, cl["idx"]]
        row = dict(dim=len(cl["idx"]))
        for nm, Mx in list(mats.items()) + [("swap", swap)]:
            R = Vk.T @ Mx @ Vk
            row[nm] = round(float(np.trace(R) / len(cl["idx"])), 6)
            row[nm + "_scalar"] = bool(np.allclose(R, row[nm] * np.eye(len(cl["idx"])), atol=1e-6))
        table.append(row)
    res = {"pass_id": 11856, "channels": table}
    res["all_structures_scalar_on_channels"] = all(all(v for k, v in r.items() if k.endswith("_scalar")) for r in table)
    only20 = [r for r in table if abs(r["E20"]) > 1e-6 and abs(r["C"]) < 1e-6 and abs(r["E15"]) < 1e-6]
    res["channels_fed_only_by_hidden_20"] = only20
    res["E20_support_dims"] = sorted(r["dim"] for r in table if abs(r["E20"]) > 1e-6)
    res["characters"] = channel_characters()
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
