#!/usr/bin/env python3
"""Pass 10965: baryon triality is structurally impossible in the W(3,3) heterotic class.

After Pass 10960/10962/10964 (no matter parity survives the FI term), the other discrete
symmetry that can protect the proton in the MSSM is baryon triality
    B3 = exp(2 pi i (B - 2Y)/3),   charges mod 3:  q 0, u^c 1, d^c 2, e^c 1, L 1, H_d 1, H_u 2,
which forbids u^c d^c d^c and q q q l but allows the lepton-number-violating couplings
(Ibanez-Ross).  Holotrade b81ef8c ruled the escape out by operator counts (the three
dimension-four operators are locked).  This pass gives the structural reason, exactly:

  A gauge B3 must be a Z3 character chi of the U(1) charge lattice with
      chi(f) = B3(f) + m * 6Y(f)  (mod 3)   on every q, u^c, d^c, e^c,
  for some hypercharge shift m.  In every one of the 215 models the linear system over F3 is
  inconsistent.  The obstruction is SU(5): in 214 models there are single copies with
      Q(u^c) + Q(e^c) = 2 Q(q)        (an exact identity of U(1) charge vectors),
  i.e. the U(1)s act on the SU(5) 10 through the 10 itself.  Any character then has
  chi(u^c) + chi(e^c) - 2 chi(q) = 0, but B3 gives 1 + 1 - 0 = 2 and the hypercharge shift
  contributes 2 + 0 - 2 = 0 (mod 3): no m repairs it.  The remaining model is certified by
  an explicit integer relation among its q, u^c, d^c, e^c charge vectors with the same
  property.  Controls: with target zero the solver finds characters in every model.
"""
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction as F
from math import lcm
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10960", ROOT / "analysis" / "w33_pass10960_matter_even_dflat_closure.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)
OUT = ROOT / "data" / "w33_pass10965_baryon_triality_impossible.json"
B3 = {"q": 0, "bu": 1, "bd": 2, "be": 1}
Y6 = {"q": 1, "bu": 2, "bd": 2, "be": 0}


def solvable_mod3(A, b):
    M = sp.Matrix(A)
    aug = M.row_join(sp.Matrix(b))
    from sympy.polys.matrices import DomainMatrix
    from sympy import GF
    dm = DomainMatrix.from_Matrix(M).convert_to(GF(3))
    da = DomainMatrix.from_Matrix(aug).convert_to(GF(3))
    return dm.rank() == da.rank()


def relation_certificate(sm):
    """integer relation sum w_f Q_f = 0 with sum w B3 != 0 and sum w 6Y == 0 (mod 3)."""
    Mx = sp.Matrix([[sp.Rational(v.numerator, v.denominator) for v in f["q"]] for f in sm]).T
    for v in Mx.nullspace():
        den = lcm(*[int(sp.fraction(x)[1]) for x in v])
        w = [int(x * den) for x in v]
        b3 = sum(c * B3[f["base"]] for c, f in zip(w, sm)) % 3
        y6 = sum(c * Y6[f["base"]] for c, f in zip(w, sm)) % 3
        if b3 and not y6:
            return {f["name"]: c for c, f in zip(w, sm) if c}
    return None


def main():
    ledger, sha = P.load_ledger()
    res, summ = {}, dict(models=0, b3_possible=0, su5_single_copy_relation=0, relation_certificates=0,
                         zero_target_control_ok=0)
    for name in sorted(ledger):
        m = ledger[name]
        left = [dict(name=f["name"], base=P.base_of(f["name"]), q=[F(x) for x in f["q"]]) for f in m["left"]]
        rk, co = P.lattice_coords([f["q"] for f in left])
        idx = {f["name"]: i for i, f in enumerate(left)}
        sm = [f for f in left if f["base"] in B3]
        A = [co[idx[f["name"]]] for f in sm]
        possible = any(solvable_mod3(A, [(B3[f["base"]] + k * Y6[f["base"]]) % 3 for f in sm]) for k in range(3))
        control = solvable_mod3(A, [0] * len(sm))
        Q = [tuple(f["q"]) for f in sm if f["base"] == "q"]
        U = [tuple(f["q"]) for f in sm if f["base"] == "bu"]
        E = [tuple(f["q"]) for f in sm if f["base"] == "be"]
        su5 = any(all(a + b - 2 * c == 0 for a, b, c in zip(u, e, q)) for q in Q for u in U for e in E)
        cert = None if su5 else relation_certificate(sm)
        res[name] = dict(b3_possible=possible, su5_single_copy_relation=su5, relation_certificate=cert)
        summ["models"] += 1
        summ["b3_possible"] += possible
        summ["su5_single_copy_relation"] += su5
        summ["relation_certificates"] += cert is not None
        summ["zero_target_control_ok"] += control
    OUT.write_text(json.dumps(dict(pass_id=10965, ledger_sha256=sha, summary=summ, models=res), indent=1, sort_keys=True))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
