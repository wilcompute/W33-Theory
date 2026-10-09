"""Passes 11714-11716: the W(3,3) heterotic vacua read in two-qutrit levels -- chirality, the 2+1 family levels,
the top Yukawa as the nine-level determinant, and doublet-triplet splitting as the plane split of one level pair.

The two-qutrit E8 of Pass 11681 is e8 = sl(9) + Lambda^3 C^9 + Lambda^3 C^9* (operators, three-fermion states,
three-hole states).  The W(3,3) heterotic twist is the A8 Kac class (Passes 10979, 11089; Holotrade 68df33f): its
order-three gauge shift has centraliser SU(9), and the roots outside it are 84 + 84bar, i.e. exactly that
decomposition.  Every claim below is read off actual orbifolder 1.2 spectra (WSL ~/orb), frozen in
data/w33_pass11714_orbifolder_frozen_states.json; `--from-orbifolder` regenerates the frozen file.

11714 (the T^6/Z3 W(3,3) vacuum, shift (1/6^7, 5/6; 0^7, 2/3)).  orbifolder: gauge group SU(9) x SO(14) x U(1)
(anomalous, tr Q = 3888); chiral spectrum
        untwisted 3 (84,1) + 3 (1,14) + 3 (1,64),     twisted T(2,0) 27 (9bar,1).
Reading: the untwisted SU(9)-charged matter is the three-fermion grade of the two-qutrit E8, once per complex plane;
the 27 fixed points of T^6/Z3 = A2^3/(1-omega) = F_3^3 carry one dual two-qutrit state each.  The SU(9) anomaly cancels
as 3 x A(Lambda^3 C^9) = 3 x 9 = 27 = number of fixed points (A(Lambda^3 C^n) = (n-3)(n-6)/2).  Under the level split
9 = 5 + 1 + 3 (Georgi-Glashow levels, vacuum level, family levels; Passes 11707, 11713) each plane's net SU(5) tens are
exactly one family triplet (10,3): (10,4) - (10bar,1) = (10,3) + [(10,1) - (10bar,1)].  Prior art: the
SU(9) x SO(14) x U(1) Z3 model is classical (Z3 orbifold classifications); the level/plane reading is the content here.

11715 (census of the 87 Z6-I W(3,3) Standard Models of Pass 11089 / Holotrade 5b3f3ad).  47 have an A8 (SU(9)) half
in the theta^2 shift 2V; in 30 of those the SM SU(3) x SU(2) lies inside that SU(9) (colour on 3 levels, weak on 2,
four "flavour" levels left); in 28 the three net quark doublets are all untwisted, i.e. three-fermion states
colour ^ weak ^ o.  In all 28:
  * the four flavour levels split {a} | {b} | {c,d}: the untwisted 10-type states (Q, u^c, e^c) use the single levels a, b
    and the untwisted 5-type states use the pair {c,d}, disjointly;
  * 2+1 family levels: the two quark doublets from the degenerate G2 planes 1,2 share one flavour level, the one from
    the order-three "qutrit" plane 3 uses the other; Q and u^c (e^c) swap levels between plane 3 and planes 1,2.
  * flagship SM_20260917_3: the model's own hypercharge is 6Y = 2 (colour), -3 (weak), 0 (flavour levels): the
    Georgi-Glashow hypercharge vanishing on the four non-GUT levels -- the vacuum-annihilating Y of Pass 11708.
Prior art: Holotrade 3caf15e/ade6ba9 (families = the three untwisted planes; species-by-plane table 87/87); the
SU(9) level labelling is the content here.

11716 (couplings).  The cubic coupling of three untwisted fields is the E8 structure constant; for three-fermion
states it is the two-qutrit bracket of Pass 11681, [x,y] = *(x ^ y), so it is nonzero exactly when the three level
sets partition the nine levels, and then equals the sign of the permutation (|coupling| = g).  In all 28 models the
Q (planes 1,2) u^c (planes 1,2) H (plane 3, H = weak ^ c ^ d) couplings exist (24 weight-level couplings each) and every
one partitions the nine levels: y_top = g is the nine-level determinant.  H (plane 3) and its colour partner
T = colour ^ c ^ d (planes 1,2) are the weak and colour halves of ONE level-pair multiplet ^{c,d}: the doublet-triplet
splitting of Holotrade a6f1cae is the plane split of that multiplet.
Scope: dictionary statements on actual spectra; no new vacuum, F-flatness, masses beyond the cubic top, or physical
selection of these models is claimed.
"""

from __future__ import annotations

import itertools
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data" / "w33_pass11714_orbifolder_frozen_states.json"
OUT = ROOT / "data" / "w33_pass11714_11716_heterotic_two_qutrit_levels.json"


# ------------------------------------------------------------------ lattice helpers
def e8_roots():
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            v = [Fr(0)] * 8
            v[i], v[j] = Fr(si), Fr(sj)
            R.append(tuple(v))
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            R.append(tuple(Fr(s, 2) for s in signs))
    return R


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def su9_levels(v2):
    """SU(9) = roots with p.v2 integral; returns the nine level weights eps_i."""
    R = [r for r in e8_roots() if dot(r, v2).denominator == 1]
    assert len(R) == 72
    t = np.random.default_rng(1).normal(size=8)
    pos = [r for r in R if float(np.dot(np.array(r, float), t)) > 0]
    ps = set(pos)
    simple = [r for r in pos if not any(tuple(a - b for a, b in zip(r, s)) in ps for s in pos if s != r)]
    adj = {i: [j for j in range(8) if j != i and dot(simple[i], simple[j]) == -1] for i in range(8)}
    chain = [[i for i in range(8) if len(adj[i]) == 1][0]]
    while len(chain) < 8:
        chain.append([j for j in adj[chain[-1]] if j not in chain][0])
    a = [simple[i] for i in chain]
    eps = [tuple(sum(Fr(9 - k, 9) * a[k - 1][c] for k in range(1, 9)) for c in range(8))]
    for i in range(8):
        eps.append(tuple(x - y for x, y in zip(eps[-1], a[i])))
    assert all(dot(eps[i], eps[j]) == (Fr(8, 9) if i == j else Fr(-1, 9)) for i in range(9) for j in range(9))
    return eps


def level_set(p, eps):
    ip = [dot(p, e) for e in eps]
    if all(x in (Fr(2, 3), Fr(-1, 3)) for x in ip) and ip.count(Fr(2, 3)) == 3:
        return (1, tuple(i for i, x in enumerate(ip) if x == Fr(2, 3)))
    if all(x in (Fr(-2, 3), Fr(1, 3)) for x in ip) and ip.count(Fr(-2, 3)) == 3:
        return (-1, tuple(i for i, x in enumerate(ip) if x == Fr(-2, 3)))
    if sorted(ip) == [Fr(-1)] + [Fr(0)] * 7 + [Fr(1)]:
        return ("adj", ip.index(1), ip.index(-1))
    return None


def anomaly_wedge(n, k):
    """SU(n) cubic anomaly of Lambda^k C^n, by explicit weights."""
    t = [Fr(i * i + 1) for i in range(n)]          # a generic traceless Cartan generator
    m = sum(t) / n
    t = [x - m for x in t]
    rep = sum(sum(t[i] for i in S) ** 3 for S in itertools.combinations(range(n), k))
    return rep / sum(x ** 3 for x in t)


# ------------------------------------------------------------------ orbifolder extraction (optional)
def parse_dump(text):
    blocks, cur, mode = [], None, None
    for ln in text.split("\n"):
        if "twisted Sector" in ln:
            cur = dict(sector=ln.strip(), states=[], right=[])
            blocks.append(cur)
            mode = None
            continue
        if cur is None:
            continue
        if "label:" in ln:
            cur["label"] = ln.split("label:")[1].strip()
        elif "right-mover" in ln:
            mode = "right"
        elif "left-movers" in ln:
            mode = "left"
        else:
            m = re.match(r"\s*\(([^)]*)\),\s*\(([^)]*)\),\s*\(([^)]*)\)_(\w+)\s+(\S+)", ln)
            if m and mode == "left":
                cur["states"].append(dict(p1=[str(Fr(x.strip())) for x in m.group(1).split(",")],
                                          p2=[str(Fr(x.strip())) for x in m.group(2).split(",")],
                                          rep=[x.strip() for x in m.group(3).split(",")], chir=m.group(4), label=m.group(5)))
                continue
            m = re.match(r"\s*\(([^)]*)\)\s*$", ln)
            if m and mode == "right" and m.group(1).count(",") == 3:
                cur["right"].append([str(Fr(x.strip())) for x in m.group(1).split(",")])
    return blocks


def from_orbifolder():
    """Rebuild the frozen file from the WSL orbifolder installation (requires ~/orb and the libgsl link)."""
    sh = r"""
set -e
mkdir -p /tmp/su9/lib /tmp/su9/m87
ln -sf $HOME/orb/sysroot/usr/lib/x86_64-linux-gnu/libgsl.so.27 /tmp/su9/lib/libgsl.so.0
export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
cd /tmp/su9/m87 && rm -f m*.txt && awk '/begin model/{n++; f=sprintf("m%02d.txt", n)} {print > f}' $HOME/orb/p1109x/susy87.txt
cd $HOME/orb/bin
for f in /tmp/su9/m87/m*.txt; do lab=$(grep Label $f | sed 's/Label://' | tr -d '\r '); \
  printf "load orbifolds($f)\ncd $lab\ncd spectrum\nprint all states\nexit\nyes\n" | timeout 900 ./orbifolder > ${f%.txt}.states 2>&1; done
"""
    subprocess.run(["wsl", "-e", "bash", "-c", sh], check=True)
    models = []
    for i in range(1, 88):
        mt = subprocess.run(["wsl", "-e", "cat", f"/tmp/su9/m87/m{i:02d}.txt"], capture_output=True, text=True).stdout
        st = subprocess.run(["wsl", "-e", "cat", f"/tmp/su9/m87/m{i:02d}.states"], capture_output=True, text=True).stdout
        rows = [l for l in mt.split("\n") if re.match(r"\s*-?[0-9]", l)]
        blocks = parse_dump(st)
        keep = []
        for b in blocks:
            if b.get("label") == "U":
                keep.append(dict(label="U", sector=b["sector"], right=b["right"],
                                 states=[s for s in b["states"] if s["chir"] in ("l", "v")]))
            else:
                seen = Counter((s["label"], tuple(s["rep"]), s["chir"]) for s in b["states"] if s["chir"] == "l")
                keep.append(dict(label=b.get("label"), sector=b["sector"], right=[],
                                 states=[dict(label=k[0], rep=list(k[1]), chir=k[2], weights=v) for k, v in seen.items()]))
        models.append(dict(label=re.search(r"Label:(\S+)", mt).group(1),
                           shift=[str(Fr(x)) for x in rows[0].replace(",", " ").split()], blocks=keep))
    json.dump(dict(source="orbifolder 1.2, ~/orb/p1109x/susy87.txt (87 Z6-I W(3,3) SM parents)", models=models),
              open(FROZEN, "w"))


# ------------------------------------------------------------------ analysis
def plane(b):
    vecs = [[Fr(x) for x in r] for r in b["right"] if all(Fr(x).denominator == 1 for x in r)]
    return tuple(sorted({i for r in vecs for i in range(1, 4) if r[i] != 0}))


def analyse_model(mod):
    V = tuple(Fr(x) for x in mod["shift"])
    halves = [sum(1 for r in e8_roots() if dot(r, tuple(2 * x for x in V[8 * h:8 * h + 8])).denominator == 1) for h in (0, 1)]
    if 72 not in halves:
        return dict(label=mod["label"], A8_half=None)
    h = halves.index(72)
    eps = su9_levels(tuple(2 * x for x in V[8 * h:8 * h + 8]))
    blocks = mod["blocks"]
    mom = lambda s: (tuple(Fr(x) for x in (s["p2"] if h == 1 else s["p1"])),  # noqa: E731
                     tuple(Fr(x) for x in (s["p1"] if h == 1 else s["p2"])))
    factors = defaultdict(set)
    for b in blocks:
        for s in b["states"]:
            if s["chir"] == "v" and s["label"].startswith("V_"):
                pos = [i for i, x in enumerate(s["rep"]) if "adj" in x]
                if pos:
                    factors[(pos[0], s["rep"][pos[0]])].add(mom(s))
    fhalf = {k: (h if all(not any(o) for _, o in v) else (1 - h if all(not any(p) for p, _ in v) else None))
             for k, v in factors.items()}
    best = None
    for c3 in [k for k in factors if k[1] == "8_adj"]:
        for c2 in [k for k in factors if k[1] == "3_adj"]:
            cnt = Counter()
            for b in blocks:
                for s in b["states"]:
                    if s["chir"] == "l" and s["rep"][c3[0]] in ("3", "-3") and s["rep"][c2[0]] == "2":
                        cnt[(b.get("label") == "U", s["rep"][c3[0]])] += s.get("weights", 1)
            net = (cnt[(True, "3")] + cnt[(False, "3")] - cnt[(True, "-3")] - cnt[(False, "-3")]) // 6
            netU = (cnt[(True, "3")] - cnt[(True, "-3")]) // 6
            # the SM pair: exactly three net doublets, preferring a pair inside the SU(9) half (Holotrade criterion)
            score = (abs(net) == 3, fhalf[c3] == h and fhalf[c2] == h, abs(netU) == 3)
            if best is None or score > best[0]:
                best = (score, (c3, c2, net, netU))
    c3, c2, net, netU = best[1]
    res = dict(label=mod["label"], A8_half=h, net_32=net, net_32_untwisted=netU if net > 0 else -netU,
               sm_in_su9=fhalf[c3] == h and fhalf[c2] == h)
    if not res["sm_in_su9"]:
        return res
    col = {i for p, _ in factors[c3] for i in level_set(p, eps)[1:]}
    weak = {i for p, _ in factors[c2] for i in level_set(p, eps)[1:]}
    st = defaultdict(list)
    for b in blocks:
        if b.get("label") != "U":
            continue
        for s in b["states"]:
            p, o = mom(s)
            if s["chir"] != "l" or any(o):
                continue
            ls = level_set(p, eps)
            if not ls or ls[0] == "adj":
                continue
            kind = "".join(sorted("C" if i in col else "W" if i in weak else "o" for i in ls[1]))
            st[(kind, plane(b))].append((frozenset(ls[1]), p))
    flav = sorted(set(range(9)) - col - weak)
    fl = lambda kind, pl: sorted({tuple(sorted(i for i in L if i in flav)) for L, _ in st.get((kind, pl), [])})  # noqa: E731
    res.update(colour_levels=sorted(col), weak_levels=sorted(weak), flavour_levels=flav)
    table = {f"{k}@plane{''.join(map(str, pl))}": [list(x) for x in fl(k, pl)] for k, pl in st}
    res["untwisted_level_table"] = table
    ten = {x for k in ("CWo", "CCo", "WWo") for pl in ((1, 2), (3,)) for t in fl(k, pl) for x in t}
    five = {t for k in ("Coo", "Woo") for pl in ((1, 2), (3,)) for t in fl(k, pl)}
    res["flavour_partition"] = dict(ten_levels=sorted(ten), five_pairs=sorted(five),
                                    disjoint_cover=len(ten) == 2 and len(five) == 1 and len(list(five)[0]) == 2
                                    and set(ten) | set(list(five)[0]) == set(flav) and not (set(ten) & set(list(five)[0])))
    q3, q12, u3, u12 = fl("CWo", (3,)), fl("CWo", (1, 2)), fl("CCo", (3,)), fl("CCo", (1, 2))
    res["two_plus_one_with_swap"] = len(q3) == 1 and len(q12) == 1 and q3 != q12 and q3 == u12 and q12 == u3
    tops = part = 0
    for Lq, pq in st.get(("CWo", (1, 2)), []):
        for Lu, pu in st.get(("CCo", (1, 2)), []):
            for Lh, ph in st.get(("Woo", (3,)), []):
                if all(a + b + c == 0 for a, b, c in zip(pq, pu, ph)):
                    tops += 1
                    part += (Lq | Lu | Lh) == frozenset(range(9)) and len(Lq) + len(Lu) + len(Lh) == 9
    res["top_cubics"] = tops
    res["top_cubics_partitioning_nine_levels"] = part
    H = fl("Woo", (3,))
    T = fl("Coo", (1, 2))
    res["doublet_triplet_same_level_pair"] = H == T and len(H) == 1
    return res


def flagship_hypercharge():
    """SM_20260917_3 hypercharge (Holotrade 5b3f3ad certificate) on the SU(9) levels."""
    V = [Fr(x) for x in "0 0 0 0 1/6 1/6 1/3 2/3 0 0 0 1/6 1/6 1/6 1/6 2/3".split()]
    tY = [Fr(x) for x in "1/6 -1/6 -1/6 1/2 0 1/2 0 1/2".split()]
    eps = su9_levels(tuple(2 * x for x in V[8:]))
    return [int(6 * dot(e, tY)) for e in eps]


def z3_vacuum_record():
    return dict(shift="(1/6^7, 5/6 ; 0^7, 2/3) on Geometry_Z3_SU3^3", gauge="SU(9) x SO(14) x U(1)", tr_Q_anomalous=3888,
                untwisted=["3 (84,1)_0", "3 (1,14)_-18", "3 (1,64)_9"], twisted_T20=["27 (9bar,1)_12"],
                su9_anomaly_lambda3=str(anomaly_wedge(9, 3)), anomaly_balance="3 x 9 - 27 x 1 = 0",
                fixed_points=27, two_qutrit_reading="84 = three-fermion grade of e8 = sl9 + 84 + 84bar; 27 = |F_3^3|")


def main():
    if "--from-orbifolder" in sys.argv:
        from_orbifolder()
    data = json.load(open(FROZEN))
    rows = [analyse_model(m) for m in data["models"]]
    a8 = [r for r in rows if r["A8_half"] is not None]
    insu9 = [r for r in a8 if r["sm_in_su9"]]
    unt = [r for r in insu9 if abs(r["net_32_untwisted"]) == 3 and abs(r["net_32"]) == 3]
    res = dict(pass_ids=[11714, 11715, 11716], z3_vacuum=z3_vacuum_record(),
               models=len(rows), with_A8_half=len(a8), sm_in_su9=len(insu9), all_three_doublets_untwisted=len(unt),
               flavour_partition_holds=sum(r["flavour_partition"]["disjoint_cover"] for r in unt),
               two_plus_one_with_swap=sum(r["two_plus_one_with_swap"] for r in unt),
               top_cubic_exists=sum(r["top_cubics"] > 0 for r in unt),
               every_top_cubic_partitions_levels=sum(r["top_cubics"] == r["top_cubics_partitioning_nine_levels"] for r in unt),
               doublet_triplet_same_pair=sum(r["doublet_triplet_same_level_pair"] for r in unt),
               flagship_6Y_on_levels=flagship_hypercharge(),
               flagship=[r for r in rows if r["label"] == "SM_20260917_3"][0], per_model=rows)
    print(json.dumps({k: v for k, v in res.items() if k not in ("per_model",)}, indent=1, default=str)[:4000])
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
