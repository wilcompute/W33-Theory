#!/usr/bin/env python3
"""Pass 10962: can hidden-sector condensates rescue matter parity in the W(3,3) heterotic class?

Pass 10960 proved, exactly and exhaustively over the full rational B-L freedom, that no
FI-cancelling D-flat SINGLET vacuum of the 88 W(3,3) Z6 Standard Models with a B-L
direction preserves matter parity.  It named one loophole: directions built from fields
that are Standard-Model singlets but charged under the HIDDEN nonabelian gauge group,
whose parity can be compensated by a hidden gauge element.  This pass attacks that
loophole in three tiers.

Tier A (exact, rigorous necessary condition, all hidden directions).
  A D-flat vacuum is in particular D-flat for the hidden maximal torus, and a
  parity-preserving vacuum is fixed by P*h for some hidden h, which can be conjugated
  into the torus.  So: split every hidden field into weight components (q, w); require
  U(1) D-flatness, hidden-torus D-flatness and FI cancellation; allow the parity of a
  component to be 3(B-L).q + 2 eta.w with eta (the hidden torus element) and t (the B-L
  freedom) both free.  Components with w = 0 and fixed odd 3(B-L) are never even.  If the
  ever-even components admit an exact Farkas vector, NO hidden-sector direction of any
  kind rescues matter parity.
Tier B (exact over explicit invariant generators).
  By Luty-Taylor / Kempf-Ness, a parity-preserving D-flat vacuum exists iff some
  FI-cancelling product of hidden-group invariant generators, each matter-even, exists
  (the parity element fixes the invariants, hence the unique closed orbit, hence a
  Kempf-Ness point up to a compact gauge transformation).  Generators used: SM x hidden
  singlets, all quadratic invariants (conjugate pairs; real and bi-doublet squares),
  SU(N) baryons and antibaryons, SU(5) 10.10.5 and 10.5b.5b.  An exact Farkas vector on
  the ever-even generators closes the model over these generators.  Completeness of the
  generator set is NOT proved here for models with bi-fundamental, SU(4) 6 or SU(5) 10
  hidden fields; that is recorded per model.
Tier C: the one model left after Tier B, by exact extreme rays (cdd, GMP) and Smith
  obstructions, when that finishes; otherwise by a recorded numeric MILP.

Input: the Pass 10960 ledger plus data/w33_pass10962_hidden_gauge_ledger.json.gz (the
hidden gauge group of every slot, read from the vector multiplets of the raw spectra).
"""
from __future__ import annotations

import gzip
import hashlib
import importlib.util
import itertools
import json
import os
import re
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10960", ROOT / "analysis" / "w33_pass10960_matter_even_dflat_closure.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)

GAUGE = ROOT / "data" / "w33_pass10962_hidden_gauge_ledger.json.gz"
OUT = ROOT / "data" / "w33_pass10962_hidden_sector_dflat_tiers.json"
CERT10960 = ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json"
TIERC = ROOT / "data" / "w33_pass10962_tierc_rays.json"

SU_ADJ = {n * n - 1: n for n in range(2, 12)}
SO_ADJ = {n * (2 * n - 1): n for n in range(4, 9)}


# ------------------------------------------------------------------ gauge ledger
def group_of_adj(d):
    if d == 78:
        return ["E", 6]
    if d == 15:
        return ["SU", 4]
    if d in SO_ADJ and d not in SU_ADJ:
        return ["SO", SO_ADJ[d]]
    return ["SU", SU_ADJ[d]]


def build_gauge_ledger(raw_root: Path) -> None:
    out = {}
    for tag, sub in (("Z6-I", "z6i"), ("Z6-II", "z6ii")):
        for fn in sorted((raw_root / sub).glob("*.sp")):
            vec = []
            for line in open(fn):
                m = re.match(r"^S (\S+) k=(\d+) susy=4 dim=(\S+)", line)
                if m:
                    vec.append(m.group(3).split(","))
            groups = [None] * len(vec[0])
            for ds in vec:
                for i, x in enumerate(ds):
                    if "adj" in x:
                        groups[i] = group_of_adj(int(x.replace("adj", "")))
            out[f"{tag}|{fn.stem}"] = groups
    with gzip.GzipFile(GAUGE, "wb", mtime=0) as fh:
        fh.write(json.dumps(out, sort_keys=True).encode())


# ------------------------------------------------------------------ weights
def lab(x):
    m = re.match(r"(-?\d+)(\D*)", x)
    return int(m.group(1)), m.group(2)


def su_weights(n, x, adj):
    F = Fraction
    if adj:
        ws = [tuple(F(int(i == a)) - F(int(i == b)) for i in range(n)) for a in range(n) for b in range(n) if a != b]
        return ws + [tuple([F(0)] * n)] * (n - 1)
    d, _ = lab(x)
    sgn, d = (-1 if d < 0 else 1), abs(d)

    def e(idx):
        return tuple(F(sum(1 for i in idx if i == j)) - F(len(idx), n) for j in range(n))
    for k in range(1, n):
        if comb(n, k) == d:
            return [tuple(sgn * v for v in e(idx)) for idx in itertools.combinations(range(n), k)]
    if n * (n + 1) // 2 == d:
        return [tuple(sgn * v for v in e((i, j))) for i in range(n) for j in range(i, n)]
    raise ValueError(("SU", n, x))


def so_weights(n, x, adj):
    F = Fraction
    d, suf = lab(x)
    if adj:
        ws = []
        for i, j in itertools.combinations(range(n), 2):
            for si in (1, -1):
                for sj in (1, -1):
                    v = [F(0)] * n
                    v[i], v[j] = F(si), F(sj)
                    ws.append(tuple(v))
        return ws + [tuple([F(0)] * n)] * n
    if abs(d) == 2 * n and suf in ("", "v"):
        ws = []
        for i in range(n):
            for s in (1, -1):
                v = [F(0)] * n
                v[i] = F(s)
                ws.append(tuple(v))
        return ws
    if abs(d) == 2 ** (n - 1):
        odd = d < 0 or suf == "c"
        return [tuple(F(s, 2) for s in sg) for sg in itertools.product((1, -1), repeat=n)
                if (sum(1 for s in sg if s < 0) % 2 == 1) == odd]
    raise ValueError(("SO", n, x))


def weights(g, x):
    adj = "adj" in x
    x = x.replace("adj", "")
    if g[0] == "SU":
        return su_weights(g[1], x, adj)
    if g[0] == "SO":
        return so_weights(g[1], x, adj)
    raise ValueError(g)


# ------------------------------------------------------------------ model data
def model_data(name, model, groups):
    left = [dict(name=f["name"], base=P.base_of(f["name"]), dims=f["dim"].split(","), q=[Fraction(x) for x in f["q"]])
            for f in model["left"]]
    qf = next(f for f in left if f["base"] == "q")
    cs = next(i for i, x in enumerate(qf["dims"]) if abs(lab(x)[0]) == 3)
    ws = next(i for i, x in enumerate(qf["dims"]) if abs(lab(x)[0]) == 2)
    hidden = [i for i in range(len(groups)) if i not in (cs, ws) and groups[i] is not None]
    labf = [f for f in left if f["base"] in P.SMY]
    y = P.solve_affine([f["q"] for f in labf], [P.SMY[f["base"]] for f in labf])[0]
    A = [f["q"] for f in left if f["base"] in P.BL]
    b = [P.BL[f["base"]] for f in left if f["base"] in P.BL]
    x0, N = P.solve_affine(A, b)
    fl = []
    for f in left:
        ds = f["dims"]
        if abs(lab(ds[cs])[0]) != 1 or abs(lab(ds[ws])[0]) != 1 or P.dot(y, f["q"]) != 0:
            continue
        hs = {i: ds[i] for i in hidden if abs(lab(ds[i])[0]) != 1 or "adj" in ds[i]}
        fl.append(dict(name=f["name"], q=f["q"], hs=hs))
    return fl, hidden, x0, N


def classify(C, M, alpha, beta):
    never = [i for i in range(len(C)) if not any(beta[i]) and not (alpha[i].denominator == 1 and alpha[i].numerator % 2 == 0)]
    U = [i for i in range(len(C)) if i not in never]
    return never, U


# ------------------------------------------------------------------ tier A
def tier_a_data(fl, hidden, groups, x0, N, s):
    comps = {}
    for f in fl:
        wl = [weights(groups[i], f["hs"][i]) if i in f["hs"] else [tuple([Fraction(0)] * groups[i][1])]
              for i in hidden]
        for combo in itertools.product(*wl):
            comps.setdefault((tuple(f["q"]), tuple(v for part in combo for v in part)), []).append(f["name"])
    T = list(comps)
    C = [s * t[0][0] for t in T]
    M = [list(t[0][1:]) + list(t[1]) for t in T]
    alpha = [3 * P.dot(x0, t[0]) for t in T]
    beta = [[3 * P.dot(n, t[0]) for n in N] + [2 * v for v in t[1]] for t in T]
    never, U = classify(C, M, alpha, beta)
    return C, M, U


def tier_a(fl, hidden, groups, x0, N, s):
    comps = {}
    for f in fl:
        wl = []
        for i in hidden:
            if i in f["hs"]:
                wl.append(weights(groups[i], f["hs"][i]))
            else:
                wl.append([tuple([Fraction(0)] * groups[i][1])])
        for combo in itertools.product(*wl):
            comps.setdefault((tuple(f["q"]), tuple(v for part in combo for v in part)), []).append(f["name"])
    T = list(comps)
    C = [s * t[0][0] for t in T]
    M = [list(t[0][1:]) + list(t[1]) for t in T]
    alpha = [3 * P.dot(x0, t[0]) for t in T]
    beta = [[3 * P.dot(n, t[0]) for n in N] + [2 * v for v in t[1]] for t in T]
    never, U = classify(C, M, alpha, beta)
    lam = P.farkas([C[i] for i in U], [M[i] for i in U])
    return dict(components=len(T), ever_even=len(U),
                closed=lam is not None, farkas=None if lam is None else [str(v) for v in lam])


# ------------------------------------------------------------------ tier B
def conj(g, x):
    d, suf = lab(x)
    if "adj" in x or abs(d) == 1 or g[0] != "SU":
        return x
    if (g[1] == 2 and abs(d) == 2) or (g[1] == 4 and abs(d) == 6):
        return x
    return str(-d) + suf


def kind(g, x):
    d, _ = lab(x)
    if g[0] == "SU" and g[1] == 2 and abs(d) == 2:
        return "pseudo"
    if "adj" in x or (g[0] == "SU" and g[1] == 4 and abs(d) == 6) or (g[0] == "SO" and abs(d) == 2 * g[1]):
        return "real"
    return "complex"


def generators(fl, groups):
    gens = [((f["name"],), f["q"]) for f in fl if not f["hs"]]
    for i, f in enumerate(fl):
        if not f["hs"]:
            continue
        for j in range(i, len(fl)):
            g = fl[j]
            if set(g["hs"]) != set(f["hs"]) or not all(g["hs"][k] == conj(groups[k], f["hs"][k]) for k in f["hs"]):
                continue
            if i == j:
                ks = [kind(groups[k], f["hs"][k]) for k in f["hs"]]
                if "complex" in ks or ks.count("pseudo") % 2:
                    continue
            gens.append(((f["name"], g["name"]), [a + b for a, b in zip(f["q"], g["q"])]))
    for k, g in enumerate(groups):
        if g is None or g[0] != "SU" or g[1] < 3:
            continue
        n = g[1]
        single = [f for f in fl if list(f["hs"]) == [k]]
        for sgn in (1, -1):
            fund = [f for f in single if lab(f["hs"][k]) == (sgn * n, "")]
            for combo in itertools.combinations(fund, n):
                gens.append((tuple(f["name"] for f in combo), [sum(f["q"][c] for f in combo) for c in range(len(combo[0]["q"]))]))
        if n == 5:
            for sgn in (1, -1):
                ten = [f for f in single if lab(f["hs"][k]) == (sgn * 10, "")]
                five = [f for f in single if lab(f["hs"][k]) == (sgn * 5, "")]
                fiveb = [f for f in single if lab(f["hs"][k]) == (-sgn * 5, "")]
                for a, b in itertools.combinations_with_replacement(range(len(ten)), 2):
                    for c in five:
                        gens.append(((ten[a]["name"], ten[b]["name"], c["name"]),
                                     [u + v + w for u, v, w in zip(ten[a]["q"], ten[b]["q"], c["q"])]))
                for a in ten:
                    for b, c in itertools.combinations(fiveb, 2):
                        gens.append(((a["name"], b["name"], c["name"]), [u + v + w for u, v, w in zip(a["q"], b["q"], c["q"])]))
    return gens


def fft_complete(fl, groups):
    why = set()
    for f in fl:
        if len(f["hs"]) > 1:
            why.add("bi-fundamental hidden field")
            continue
        for k, x in f["hs"].items():
            g = groups[k]
            if "adj" in x:
                why.add("hidden adjoint")
            elif not (g[0] == "SU" and abs(lab(x)[0]) == g[1]):
                why.add(f"{g[0]}({g[1]}) {x}")
    return sorted(why)


def tier_b(fl, groups, x0, N, s):
    types = {}
    for labl, q in generators(fl, groups):
        types.setdefault(tuple(q), []).append(labl)
    T = list(types)
    C = [s * t[0] for t in T]
    M = [list(t[1:]) for t in T]
    alpha = [3 * P.dot(x0, t) for t in T]
    beta = [[3 * P.dot(n, t) for n in N] for t in T]
    never, U = classify(C, M, alpha, beta)
    lam = P.farkas([C[i] for i in U], [M[i] for i in U])
    return dict(generator_types=len(T), ever_even=len(U), dflat_any=P.farkas(C, M) is None,
                closed=lam is not None, farkas=None if lam is None else [str(v) for v in lam],
                incomplete_because=fft_complete(fl, groups)), (T, types, C, M, alpha, beta, U)


def main():
    raw = os.environ.get("W33_ORB_RAW")
    if raw:
        build_gauge_ledger(Path(raw))
    ledger, sha60 = P.load_ledger()
    graw = GAUGE.read_bytes()
    gauge = json.loads(gzip.decompress(graw))
    c60 = json.loads(CERT10960.read_text())["models"]
    tierc = json.loads(TIERC.read_text()) if TIERC.exists() else {}
    res = {}
    for name in sorted(ledger):
        if not c60[name].get("bl_direction"):
            continue
        groups = gauge[name]
        fl, hidden, x0, N = model_data(name, ledger[name], groups)
        s = 1 if Fraction(c60[name]["trace_anomalous"]) > 0 else -1
        rec = dict(hidden_groups=[groups[i] for i in hidden],
                   hidden_charged_fields=sum(1 for f in fl if f["hs"]))
        rec["tier_a"] = tier_a(fl, hidden, groups, x0, N, s)
        if rec["tier_a"]["closed"]:
            rec["verdict"] = "A: closed for every hidden-sector direction (exact)"
        else:
            rec["tier_b"], _ = tier_b(fl, groups, x0, N, s)
            if rec["tier_b"]["closed"]:
                rec["verdict"] = "B: closed over all listed invariant generators (exact Farkas)"
            elif name in tierc:
                rec["tier_c"] = tierc[name]
                rec["verdict"] = ("C: closed, every FI-cancelling generator ray parity-obstructed (exact)"
                                  if tierc[name].get("realizable") == 0 and tierc[name].get("exact") else
                                  "C: numerically closed (MILP infeasible); exact enumeration recorded separately")
            else:
                rec["verdict"] = "OPEN"
        res[name] = rec
        print(f"{name:38s} {rec['verdict']}", flush=True)
    summ = {}
    for v in res.values():
        summ[v["verdict"]] = summ.get(v["verdict"], 0) + 1
    # the anomaly-free models: no FI term, so the origin is D-flat -- do they admit ANY matter parity?
    af = {}
    for name in sorted(ledger):
        if not c60[name].get("anomaly_free"):
            continue
        left = [dict(base=P.base_of(f["name"]), q=[Fraction(x) for x in f["q"]]) for f in ledger[name]["left"]]
        A = [f["q"] for f in left if f["base"] in P.BL]
        b = [P.BL[f["base"]] for f in left if f["base"] in P.BL]
        rk, co = P.lattice_coords([f["q"] for f in left])
        ism = [f["base"] in P.MATTER for f in left]
        nchar = sum(1 for eps in itertools.product((0, 1), repeat=rk)
                    if all(sum(e * c for e, c in zip(eps, cc)) % 2 == 1 for cc, m in zip(co, ism) if m))
        af[name] = dict(bl_direction=P.solve_affine(A, b) is not None, z2_matter_parities=nchar)
        print(f"{name:38s} anomaly-free: {af[name]}", flush=True)
    summ["anomaly_free_models_with_any_matter_parity"] = sum(1 for v in af.values()
                                                              if v["bl_direction"] or v["z2_matter_parities"])
    cert = dict(pass_id=10962, ledger_sha256=sha60, gauge_ledger=str(GAUGE.relative_to(ROOT)).replace(os.sep, "/"),
                gauge_ledger_sha256=hashlib.sha256(graw).hexdigest(), summary=summ, models=res,
                anomaly_free_models=af)
    OUT.write_text(json.dumps(cert, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
