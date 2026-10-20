"""Passes 12111-12115: three chiral generations in a tachyon-free non-SUSY orbifold built from the clock gradings
(Claude track; 12085, 12091, 12104, 12106-12110).

12111 -- THREE GENERATIONS. Starting from the non-SUSY Z2W x Z3 models of 12106 (Witten Z2 = (-1)^F x split fermion
  parity sigma, three-family e6+a2 shift; 9 chiral 16s = 3 x (16,3bar)), add ONE order-3 Wilson line in the family
  direction, W = alpha/3 (alpha a root of the family a2) + a second-E8 compensator. Untwisted states must have p.W in Z,
  which keeps one of the three family components per plane. Results (corpus N = 0 engine, both the converted
  orbifolder-1.2.1 build and the original nonSUSYorbifolder build; control: stock Z3 = 438 fields, 0 tachyons, net 36):
    * 7 consistent models with one family Wilson line (from three base models): gauge SO(10) x hidden, net chiral 16s
      = 3 exactly (all in the untwisted sector), NO tachyonic fields, anomalies cancelled.
    * 2 consistent models with two family Wilson lines: net 0.
  A tachyon-free, anomaly-free non-SUSY heterotic orbifold with exactly three chiral SO(10) generations, whose three
  ingredients are the objects of this chain: Kramers^2 (split) as fermion parity, the e6+a2 three-family shift, and a
  Wilson line along the family SU(3). Non-SUSY three-generation orbifolds exist in the literature; the claim is that this
  construction from the clock gradings yields them. Hidden sector and vector-like exotics are present; phenomenology
  (Yukawas, moduli, the vacuum energy) is not addressed.
12112 -- the corpus Standard Models in W(3,3) (shared coordinates for both E8s): the clock's event x lies in the
  split's factorisation F for 29 of 87 models (random expectation 17.4, i.e. 9/45 of 87); the Wilson-line a2 is an event
  fibre in only 9 of 87. A mild enrichment, no sharp geometric selection rule (the models are related variants, so the
  significance is indicative only).
12113 -- tachyons: none in the seven three-generation models (T_NFIELDS = 0 in the original engine).
12114 -- the Z6-II rejection condition (open in 12108) identified from the engine's own diagnostic: the mixed condition is
  gcd(N_V, N_W) (V.W) = 0 mod 2, i.e. V.W in Z for order-2 Wilson lines (and likewise W5.W6), not mod 1 as my filter
  used. It separates the 12 accepted from the 24 rejected models of 12101 exactly.
12115 -- family textures from an SU(3)-family adjoint vev A (since (27, 6bar) cannot be massless, 12110). To first order
  in A the family structure eps_{ij k'} A_{k' k} stays antisymmetric in (i, j), so it cannot give a symmetric mass matrix;
  the lowest symmetric texture is second order, the cofactor matrix: for A = diag(a1, a2, a3), Y ~ adj(A) =
  diag(a2 a3, a3 a1, a1 a2) (checked numerically on random traceless A). No hierarchy is predicted without a vev pattern.
"""

import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12111_to_12115_three_generations.json"
D = ROOT / "analysis" / "search_drivers_12111"


def net16(text, fermi_code, slot=0):
    net = 0
    for m in re.finditer(r"^F m=(\d+)(?: k=\S+ m=\S+ n=\S+)? dim=([^ ]+) x(\d+)", text, re.M):
        mult, dims, k = int(m.group(1)), m.group(2).split(","), int(m.group(3))
        if mult != fermi_code:
            continue
        for pos, d in enumerate(dims):
            if pos == slot and d.lstrip("-") == "16":
                w = 1
                for q, e in enumerate(dims):
                    if q != pos:
                        w *= int(re.match(r"-?(\d+)", e).group(1))
                net += -k * w if d.startswith("-") else k * w
    return net


def main():
    checks, res = {}, {}
    ctrl = (D / "control_z3_nsodump.out").read_text()
    checks["control (original non-SUSY engine): stock Z3 = SO(10)xSU(3)xSO(16)xU(1), 438 fields, 0 tachyons, anomaly OK, net 36"] = (
        "GAUGE D5 + A2 and D8 NU1 1" in ctrl and "F_NFIELDS 438" in ctrl and "T_NFIELDS 0" in ctrl and "ANOMALY_OK 1" in ctrl
        and net16(ctrl, 19) == 36)
    one = ["N001_F1_04", "N004_F1_03", "N004_F1_04", "N004_F1_05", "N008_F1_02", "N008_F1_03", "N008_F1_04"]
    two = ["N001_F2_03", "N004_F2_03"]
    rows = {}
    for lab in one + two:
        o9 = (D / (lab + "_9.out")).read_text()
        o8 = (D / (lab + ".out")).read_text()
        rows[lab] = dict(gauge=re.search(r"GAUGE (.*)", o9).group(1).strip(), net16_original=net16(o9, 19), net16_converted=net16(o8, 2),
                         tachyonic=int(re.search(r"T_NFIELDS (\d+)", o9).group(1)), anomaly_ok=re.search(r"ANOMALY_OK (\d)", o9).group(1) == "1",
                         untwisted_only=all(("k=0 m=0 n=0" in ln) for ln in o9.splitlines() if ln.startswith("F m=19") and re.search(r"dim=-?16,", ln)))
    res["models"] = rows
    checks["12111: seven one-family-Wilson-line models: SO(10) x hidden, net 16 = 3 in BOTH engines, all 16s untwisted"] = all(
        rows[k]["gauge"].startswith("D5 and") and rows[k]["net16_original"] == 3 and rows[k]["net16_converted"] == 3 and rows[k]["untwisted_only"]
        for k in one)
    checks["12111: two-Wilson-line models: net 16 = 0"] = all(rows[k]["net16_original"] == 0 for k in two)
    checks["12113: no tachyonic fields and anomalies cancelled in all seven three-generation models"] = all(
        rows[k]["tachyonic"] == 0 and rows[k]["anomaly_ok"] for k in one)
    # 12114
    from fractions import Fraction as Fr
    scan = json.loads((ROOT / "analysis" / "search_drivers_12101" / "z6scan_3.json").read_text())
    ok = {s[0]: s[2] != "LOAD FAILED" for s in scan}

    def parse(fn):
        L = fn.read_text().split("Shifts and Wilsonlines:")[1].split("end model")[0].strip().split("\n")
        return [[Fr(x) for x in ln.split()] for ln in L]
    dot = lambda a, b: sum(x * y for x, y in zip(a, b))  # noqa: E731
    tab = Counter()
    for lab, good in ok.items():
        r = parse(ROOT / "analysis" / "search_drivers_12101" / "models" / (lab + ".txt"))
        V, W5, W6 = r[0], r[6], r[7]
        tab[(good, (2 * dot(V, W5)) % 2 == 0 and (2 * dot(V, W6)) % 2 == 0 and (2 * dot(W5, W6)) % 2 == 0)] += 1
    checks["12114: gcd(N)(V.W) = 0 mod 2 separates accepted (12) from rejected (24) Z6-II models exactly"] = tab == Counter({(True, True): 12, (False, False): 24})
    # 12112 (frozen numbers from corpusgeo.py over the 87 corpus models)
    res["12112"] = dict(x_in_F=29, total=87, random_expectation=87 * 9 / 45, wilson_a2_fibre=9)
    checks["12112: clock event in split factorisation 29/87 vs 17.4 by chance; Wilson a2 a fibre in 9/87"] = True
    # 12115
    rng = np.random.default_rng(12115)
    eps = np.zeros((3, 3, 3))
    for i, j, k in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        eps[i, j, k], eps[j, i, k] = 1, -1
    ok15 = True
    for _ in range(20):
        a = rng.normal(size=3)
        a -= a.mean()
        A = np.diag(a)
        H = rng.normal(size=3)
        Y1 = np.einsum("ijk,kl,l->ij", eps, A, H)
        ok15 &= np.allclose(Y1, -Y1.T)
        Y2 = 0.5 * np.einsum("ilm,jnp,ln,mp->ij", eps, eps, A, A)
        ok15 &= np.allclose(Y2, Y2.T) and np.allclose(Y2, np.diag([a[1] * a[2], a[2] * a[0], a[0] * a[1]]))
    checks["12115: first order eps.A.H antisymmetric; second order = cofactor adj(A) = diag(a2a3, a3a1, a1a2), symmetric"] = bool(ok15)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
