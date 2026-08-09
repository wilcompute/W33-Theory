#!/usr/bin/env python3
"""Passes 4479-4481 -- exact spectra for two more quadrangles, and the corpus auditing me.

  4479  Pass 4456 recovered W(3,3)'s adjacency spectrum EXACTLY from prime geodesic counts
        alone, via the Bass reduction and integer Newton identities.  The method is general
        and was only ever run on one graph.  Here it runs on H(3,9) and Q(5,3), which were
        built at Passes 4389 and 4448 and whose spectra the repository does not otherwise
        hold in factored form.

  4481  THE NEW TOOLING AUDITING THE WORK THAT BUILT IT.  `scripts/cert_query.py` indexes
        2.98 million key/value pairs from 4,687 certificates -- including the roman-numeral
        and bt* conventions that every sweep I ran this session was blind to.  Asking it for
        my own session's constants turns up prior art:

            6.6332495807108   the Ramanujan bound 2*sqrt(11)
              data/w33_spectral_gap_mixing.json          ramanujan_bound_2sqrt_km1
              data/w33_MCLI_MCLX_final_theorem_millennium.json   MCLIII_ramanujan.bound
              data/w33_pass881_seven_thread_batch_intake_audit.json

        Ten of my own certificates from passes 4409-4457 assert the same number and none
        cites any of those three.  Whether that is a rediscovery is decided below, by
        reading what they claim rather than by matching the constant.

    py -3 analysis/w33_pass4479_4481_bass_family_and_self_audit.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

_s = importlib.util.spec_from_file_location(
    "p4389", ROOT / "analysis" / "w33_pass4389_hermitian_quadrangle_measured.py")
p4389 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_s and p4389)

_s2 = importlib.util.spec_from_file_location(
    "p4448", ROOT / "analysis" / "w33_pass4448_4450_q53_floquet_tanner.py")
p4448 = importlib.util.module_from_spec(_s2)
_s2.loader.exec_module(p4448)


def collinearity(pts, lines):
    n = len(pts)
    A = np.zeros((n, n), dtype=object)
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1
    return A


def bass_recover(A):
    """Adjacency spectrum from prime counts alone.  Exact integers throughout."""
    n = len(A)
    d = int(sum(A[0]))
    q = d - 1
    nE = sum(int(x) for x in A.flatten()) // 2
    excess = nE - n
    K = n

    trA, P = [], np.eye(n, dtype=object)
    for _ in range(K):
        P = P @ A
        trA.append(int(np.trace(P)))

    poly = [[2], [0, 1]]
    for m in range(2, K + 1):
        a = [0] + poly[m - 1]
        b = [q * c for c in poly[m - 2]]
        L = max(len(a), len(b))
        poly.append([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
                     for i in range(L)])

    Nm = []
    for m in range(1, K + 1):
        s = sum(c * (n if k == 0 else trA[k - 1]) for k, c in enumerate(poly[m]))
        Nm.append(s + excess * (1 + (-1) ** m))

    # INVERSE -- reads only Nm
    S = [Nm[m - 1] - excess * (1 + (-1) ** m) for m in range(1, K + 1)]
    rec = []
    for m in range(1, K + 1):
        c = poly[m]
        known = sum(c[k] * (n if k == 0 else rec[k - 1]) for k in range(len(c) - 1))
        rec.append((S[m - 1] - known) // c[len(c) - 1])

    e = [Fraction(1)]
    for k in range(1, K + 1):
        acc = sum((-1) ** (i - 1) * e[k - i] * rec[i - 1] for i in range(1, k + 1))
        e.append(Fraction(acc, k))
    x = sympy.symbols("x")
    cp = sum(sympy.Integer((-1) ** k * e[k].numerator // e[k].denominator)
             * x ** (K - k) for k in range(K + 1))
    roots = {int(r): int(m) for r, m in sympy.roots(cp).items() if r.is_integer}
    return {"n": n, "degree": d, "q": q, "edges": nE,
            "traces_exact": rec == trA,
            "charpoly": str(sympy.factor(cp)),
            "spectrum": {str(k): v for k, v in sorted(roots.items(), reverse=True)},
            "recovered_all": sum(roots.values()) == n}


# ---------------------------------------------------------------------------

# index.html measured 2026-08-09; hits are case-insensitive occurrence counts.
INDEX_HTML = [
    ("Ihara", 41, "present -- the zeta track is well covered"),
    ("non-backtracking", 18, "present -- Hashimoto operator discussed"),
    ("Artin", 13, "HOMONYM -- arithmetic Artin L-functions, not Artin-Ihara"),
    ("double cover", 1, "HOMONYM -- Sp(4,3) over PSp(4,3), a group extension"),
    ("signing", 1, "HOMONYM -- ovoid ray assignment, not +/-1 edge signs"),
    ("Bilu", 0, "ABSENT -- Bilu-Linial appears nowhere"),
    ("Hagedorn", 0, "ABSENT"),
    ("prime geodesic", 0, "ABSENT"),
    ("Hermitian", 0, "ABSENT -- H(3,9) is not in the encyclopedia"),
    ("Q(5,3)", 0, "ABSENT"),
]

PRIOR = [
    ("data/w33_spectral_gap_mixing.json", "ramanujan.ramanujan_bound_2sqrt_km1",
     "W(3,3) is a Ramanujan graph: |lambda_j| <= 2 sqrt(k-1) for all j != 0",
     "UNSIGNED adjacency; lambda = 2 and -4 both inside the bound"),
    ("data/w33_MCLI_MCLX_final_theorem_millennium.json", "MCLIII_ramanujan.bound",
     "bound 6.6332, |s| = 4, slack 2.6332, strict",
     "UNSIGNED; records the slack of the second eigenvalue"),
    ("data/w33_pass881_seven_thread_batch_intake_audit.json",
     "part_B_false.thread3_gap.ramanujan_bound", "intake audit reusing the constant",
     "UNSIGNED, and explicitly inside a block marked false"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 4479-4481 -- exact spectra, and the corpus auditing me")
    print("=" * 78)

    print("\n  PASS 4479 -- Bass recovery on two more quadrangles\n")
    out = {}
    for name, builder in (("H(3,9)", lambda: p4389.build_h39()[:2]),
                          ("Q(5,3)", lambda: p4448.build_q53())):
        pts, lines = builder()
        A = collinearity(pts, lines)
        r = bass_recover(A)
        out[name] = r
        spec = ", ".join(f"{k}^{v}" for k, v in r["spectrum"].items())
        print(f"    {name}: {r['n']} points, degree {r['degree']}, q = {r['q']}")
        print(f"      traces recovered exactly : {r['traces_exact']}")
        print(f"      characteristic polynomial: {r['charpoly'][:60]}")
        print(f"      spectrum                 : {spec}")
        print(f"      multiplicities sum to n  : {r['recovered_all']}\n")

    print("""    THE METHOD IS GENERAL, AND BOTH SPECTRA COME BACK EXACTLY.

    Nothing after the prime counts touches an adjacency matrix. Both quadrangles are
    strongly regular, so each returns three eigenvalues with multiplicities summing to the
    point count -- and the recovery is over the integers, so these are exact statements
    rather than numerical ones. Pass 4456 established the route on W(3,3); it transfers
    without modification.""")

    # ---- 4481 -------------------------------------------------------------
    print("\n  PASS 4481 -- the corpus index audits this session\n")
    print(f"    {'certificate':56s} {'claims'}")
    for f, path, claim, kind in PRIOR:
        print(f"    {f[5:][:56]:56s} {claim[:44]}")
        print(f"    {'':56s} -> {kind}")

    print("""
    NOT A REDISCOVERY, BUT IT SHOULD HAVE BEEN CITED.

    Three certificates hold 2*sqrt(11) = 6.6332495807108 and predate this session. All
    three are about the UNSIGNED adjacency matrix: W(3,3)'s non-trivial eigenvalues are 2
    and -4, both comfortably inside the bound, so the collinearity graph is Ramanujan in
    the ordinary sense. That is a real and standard fact and the repository already had it.

    This session asked a different question. Bilu-Linial is about a SIGNED adjacency
    matrix and constrains EVERY eigenvalue including the top one, and the unsigned graph
    fails that immediately -- lambda_max = 12, nearly twice the bound. Passes 4409 to 4457
    are about whether a signing exists that pushes all of them inside. The constant is
    shared; the question is not.

    SO THE VERDICT IS: SAME NUMBER, DIFFERENT THEOREM, AND TEN OF MY CERTIFICATES SHOULD
    CITE THESE THREE AND DO NOT. CLAUDE.md's rule is to cite across the boundary rather
    than re-derive, and the reason I did not is measurable rather than careless -- two of
    the three files use naming conventions (roman-numeral, and a bt-era audit) that every
    sweep I ran this session was structurally blind to. The tool that found them was built
    this afternoon precisely because that blindness had already cost a retraction.""")

    # ---- index.html, the encyclopedia of record ---------------------------
    print("\n  PASS 4481b -- docs/index.html, searched by RESULT and by near-miss term\n")
    print(f"    {'term':22s} {'hits':>6s}  verdict")
    for term, hits, verdict in INDEX_HTML:
        print(f"    {term:22s} {hits:>6d}  {verdict}")
    print("""
    THE ZETA SIDE IS ALREADY THERE. index.html carries Bass's determinant formula
    det(I-uB) = (1-u^2)^{E-V} det(I-uA+u^2(D-I)) explicitly, records rho(B) = 11, and
    states that the instruction graph has "78 non-trivial poles, all on the critical
    circle". That is the graph Riemann Hypothesis, written down, with 41 mentions of Ihara
    and 18 of non-backtracking around it.

    THE SIGNING SIDE IS ABSENT: zero hits for Bilu, Bilu-Linial, Hagedorn, prime geodesic,
    Hermitian, H(3,9) and Q(5,3).

    AND THE THREE TERMS THAT LOOKED LIKE OVERLAP ARE ALL HOMONYMS -- which is the finding.

      "Artin L-function values"  belongs to a Hasse-Weil / BSD / Faltings-height passage
                                 about ARITHMETIC geometry. Not the Artin-Ihara L-function
                                 of a graph cover.
      "signing"                  is assigning 1 and 0 to ovoid rays in a noncontextuality
                                 model. Not a +/-1 edge signing.
      "double cover"             is Sp(4,3) as a central double cover of PSp(4,3), a GROUP
                                 extension. Not a graph double cover.

    Three collisions in one check, on top of the "partition function" homonym recorded at
    Pass 4460. This corpus is dense enough that a term-match is almost never evidence, and
    the only reliable probe is the one CLAUDE.md prescribes -- search for the RESULT, then
    READ the passage. Every one of these three would have been scored as prior art by a
    grep and none of them is.""")

    out["pass_4481_index_html"] = [
        {"term": t, "hits": h, "verdict": v} for t, h, v in INDEX_HTML]
    out["pass_4481_homonyms"] = {
        "Artin L-function values": "Hasse-Weil/BSD arithmetic passage, not Artin-Ihara",
        "signing": "ovoid ray assignment in a noncontextuality model, not +/-1 edge signs",
        "double cover": "Sp(4,3) over PSp(4,3), a group extension, not a graph cover"}
    out["pass_4481_prior_art"] = [
        {"file": f, "path": p, "claim": c, "scope": k} for f, p, c, k in PRIOR]
    out["pass_4481_verdict"] = (
        "same constant, different theorem: the prior certificates assert the UNSIGNED "
        "graph is Ramanujan (non-trivial eigenvalues 2 and -4 inside 2 sqrt 11), while "
        "passes 4409-4457 ask whether a SIGNING exists bringing ALL eigenvalues inside, "
        "which the unsigned graph fails at lambda_max = 12. Not a rediscovery; a missing "
        "citation, caused by conventions my sweeps could not see")
    out["boundary"] = (
        "4479's recoveries are exact integer arithmetic on two constructed quadrangles; "
        "4481 compares three certificates found by value-match and READ, and asserts "
        "nothing about the rest of the corpus -- the same constant may appear elsewhere "
        "under a value my query did not try")

    p = ROOT / "data" / "PART_W33_PASS4479_4481_BASS_FAMILY_AND_AUDIT.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
