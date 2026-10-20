"""Passes 12116-12120: physics of the three-generation models (Claude track; 12111-12115).

12116 -- toward the Standard Model. A second order-3 Wilson line on the seven SO(10) three-generation models (60 random
  consistent candidates, original non-SUSY engine): 19 load; 4 have first-E8 gauge group SU(3) x SU(2) x SU(2) x U(1)s
  with net three quark doublets (3,2) and net SIX colour-antitriplet singlets (three u^c- plus three d^c-type), no
  tachyonic fields, anomalies cancelled. Three generations of quarks with an extra SU(2); the lepton doublets are
  partly vector-like and hypercharge is not yet identified, so these are three-generation QUARK spectra, not a full SM.
12117 -- Bose-Fermi count of the massless spectrum (helicity states, representation-weighted): N_B - N_F = -686, -686, -686,
  -660, -494, -710, -494 for the seven three-generation models (control stock Z3: -1298). A fermion excess in every
  model; the one-loop cosmological constant itself (sign and size) needs the full modular integral and is not computed.
12118 -- NEGATIVE: no tree-level 16.16.10 Yukawa in the untwisted sector. Each model has one fermionic 16 and one scalar
  10 per plane (Higgs candidates exist), but no root triple 16 + 16 + 10 = 0: the family Wilson line keeps a single family
  component, and the E6 cubic is antisymmetric in families (corpus 11271), so the untwisted Yukawa vanishes. Masses need
  twisted-sector or higher-order couplings.
12119 -- NEGATIVE: the family a2 of the seven models is not a W(3,3) event fibre (0/7), so the generation-selecting
  Wilson line is not literally an event's tick.
12120 -- the corrected SUSY Z6-II scan (mixed conditions mod 2, 12114): 36 of 36 models consistent (no load failures),
  dimension-weighted net 16s/27s only 0 or +-1 -- the SUSY Z6-II route does not give three families; the non-SUSY Z3 route
  with a family Wilson line does.
"""

import itertools
import json
import re
import sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12116_to_12120_three_generation_physics.json"
D11 = ROOT / "analysis" / "search_drivers_12111"
D16 = ROOT / "analysis" / "search_drivers_12116"
BASES = ["N001_F1_04", "N004_F1_03", "N004_F1_04", "N004_F1_05", "N008_F1_02", "N008_F1_03", "N008_F1_04"]


def fields(text, code):
    out = []
    for m in re.finditer(r"^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]+) x(\d+)", text, re.M):
        if int(m.group(1)) == code:
            out.append((m.group(2).split(","), int(m.group(3))))
    return out


def dimw(dims, skip):
    w = 1
    for q, e in enumerate(dims):
        if q not in skip:
            w *= int(re.match(r"-?(\d+)", e).group(1))
    return w


def main():
    checks, res = {}, {}
    # 12116
    sm = json.loads((D16 / "smwl_3.json").read_text())
    loaded = [r for r in sm if r["gauge"] != "LOADFAIL"]
    three = [r for r in loaded if r["gauge"].startswith("A2 + A1 + A1 and") and abs(r["net32"]) == 3]
    det = {}
    for r in three:
        o = (D16 / "smwl" / (r["label"] + ".out")).read_text()
        f = fields(o, 19)
        n32, j = max(((sum((-k if d[0].startswith("-") else k) * dimw(d, (0, jj)) for d, k in f if d[0].lstrip("-") == "3" and d[jj] == "2"), jj)
                      for jj in (1, 2)), key=lambda t: abs(t[0]))
        n3b = sum((-k if d[0].startswith("-") else k) * dimw(d, (0,)) for d, k in f if d[0].lstrip("-") == "3" and d[1] == "1" and d[2] == "1")
        det[r["label"]] = dict(net_32=n32, net_colour_singlet_triplets=n3b, tachyonic=r["tachyonic"], anomaly_ok=r["anomaly_ok"])
    res["12116"] = dict(attempts=len(sm), loaded=len(loaded), three_generation_quark_models=det)
    checks["12116: 60 attempts, 19 load, 4 SU(3)xSU(2)xSU(2) models with net |(3,2)| = 3, net 3bar singlets = 2 x net (3,2), tachyon- and anomaly-free"] = (
        len(sm) == 60 and len(loaded) == 19 and len(det) == 4
        and all(abs(v["net_32"]) == 3 and v["net_colour_singlet_triplets"] == -2 * v["net_32"] and v["tachyonic"] == 0 and v["anomaly_ok"] for v in det.values()))
    # 12117
    BOS, FER = {8, 9, 13, 14, 15, 16, 17, 18}, {19, 20}
    bf = {}
    for lab in ["control_z3_nsodump"] + BASES:
        o = (D11 / (lab + ".out" if lab.startswith("control") else lab + "_9.out")).read_text()
        b = f = 0
        for m in re.finditer(r"^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]+) x(\d+)", o, re.M):
            c, dims, k = int(m.group(1)), m.group(2).split(","), int(m.group(3))
            n = k * dimw(dims, ())
            b += n if c in BOS else 0
            f += n if c in FER else 0
        bf[lab] = b - f
    res["12117_NB_minus_NF"] = bf
    checks["12117: N_B - N_F = -686,-686,-686,-660,-494,-710,-494 (control -1298): fermion excess"] = (
        [bf[b] for b in BASES] == [-686, -686, -686, -660, -494, -710, -494] and bf["control_z3_nsodump"] == -1298)
    # 12118 + 12119
    g = Gradings()
    R, fib = g.R, g.fib
    ptof = {i: x for x in range(40) for i in fib[x]}
    key = {tuple(np.round(r * 2).astype(int)): i for i, r in enumerate(R)}
    y_ok, fam_fibre = True, 0
    for base in BASES:
        rows = (D11 / (base + "_9.txt")).read_text().split("Shifts and Wilsonlines:")[1].split("end model")[0].strip().split("\n")
        vec = [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]
        V0, V1, W = vec[0], vec[1], vec[3]
        pV0, pV1, pW = R @ V0, R @ V1, R @ W
        integ = lambda a: np.abs(a - np.round(a)) < 1e-9  # noqa: E731
        gauge = integ(pV0) & integ(pV1) & integ(pW)
        d5 = next(c for c in g.comps(gauge) if len(c) == 40)
        Bd = np.linalg.svd(R[d5])[2][:5]
        proj = np.array([np.sum((Bd @ R[a]) ** 2) for a in range(240)])
        ph13 = np.abs((pV1 % 1) - 1 / 3) < 1e-9
        odd = np.abs((pV0 % 1) - 0.5) < 1e-9
        f16 = [a for a in range(240) if ph13[a] and odd[a] and integ(pW[a]) and np.isclose(proj[a], 1.25)]
        b10 = set(a for a in range(240) if ph13[a] and not odd[a] and integ(pW[a]) and np.isclose(proj[a], 1.0))
        trip = sum(1 for a, b in itertools.combinations_with_replacement(f16, 2)
                   if key.get(tuple(np.round(-(R[a] + R[b]) * 2).astype(int))) in b10)
        y_ok &= len(f16) == 16 and len(b10) == 10 and trip == 0
        ph = np.round(3 * pV1).astype(int) % 3
        fam = next(c for c in g.comps(ph == 0) if len(c) == 6)
        fam_fibre += len({ptof[i] for i in fam}) == 1
    checks["12118: one fermionic 16 (16 roots) and one scalar 10 (10 roots) per plane, but no 16+16+10 = 0 root triple"] = bool(y_ok)
    checks["12119: the family a2 is an event fibre in 0 of 7 models"] = fam_fibre == 0
    # 12120
    z2 = json.loads((D16 / "z6scan2_4.json").read_text())
    rc = json.loads((D16 / "z6recount2_4.json").read_text())
    checks["12120: corrected SUSY Z6-II scan: 36/36 consistent, dimension-weighted nets only 0 or +-1"] = (
        len(z2) == 36 and all(s[2] != "LOAD FAILED" for s in z2) and len(rc) == 36 and all(all(abs(v) <= 1 for v in r[2].values()) for r in rc))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
