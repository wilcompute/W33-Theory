"""
BRUTAL TRUTH CHECK
==================

Stops adding phases. Tests the load-bearing structural claims of the
W(3,3) cascade against actual mathematics. Specifically:

  CLAIM A (equipartition uniqueness):
    "f*(k-r) = g*(k-s) = E = 240 is unique to W(3,3) among GQ(q,q),
     and this is what kills mu^2_H at tree level and solves the
     hierarchy."  (W33_HIERARCHY_MECHANISM.json)

  CLAIM B (rank-3 spectral decomposition):
    "40 = 1 + 24 + 15 forces A_F = C (+) H (+) M_3(C)."
    (W33_SM_ALGEBRA.json)

  CLAIM C (alpha = 137 = 13 + 124 has structural meaning):
    "alpha^-1 = k^2 - Phi_6 = 137"  (W33_ALPHA_DOF.json)

  CLAIM D (hierarchy is a derivation, not curve-fit):
    "ln(M_Pl/v_EW) = s^2 * ln(Phi_4)"
    (W33_HIERARCHY_MECHANISM.json)

For each claim we ask: does it actually hold uniquely at q=3, or is it
either (i) a generic property of ALL GQ(q,q), or (ii) numerology?

Results are written to data/w33_brutal_truth.json with no spin.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
#  Closed-form SRG parameters of the symplectic GQ(q,q)
# ---------------------------------------------------------------------------

def gq_qq_params(q: int) -> Dict[str, int]:
    """Symplectic generalised quadrangle W(3,q): the SRG of its
    collinearity graph has the well-known parameters
        v = (q+1)(q^2+1),  k = q(q+1),  lam = q-1,  mu = q+1.
    Eigenvalues r = q-1, s = -(q+1) with multiplicities
        f = q(q+1)^2 / 2,  g = q(q^2+1)/2."""
    v = (q + 1) * (q * q + 1)
    k = q * (q + 1)
    lam = q - 1
    mu = q + 1
    r = q - 1
    s = -(q + 1)
    # f, g may be half-integers in pathological q; for prime powers they
    # come out integral when q+1 has the right parity.  Use rationals.
    f = Fraction(q * (q + 1) ** 2, 2)
    g = Fraction(q * (q * q + 1), 2)
    E = Fraction(v * k, 2)  # edges
    return dict(q=q, v=v, k=k, lam=lam, mu=mu, r=r, s=s, f=f, g=g, E=E)


def equipartition_check(q: int) -> Dict[str, object]:
    """Compute f*(k-r), g*(k-s), and E for GQ(q,q)."""
    p = gq_qq_params(q)
    f, g, k, r, s, E = p["f"], p["g"], p["k"], p["r"], p["s"], p["E"]
    bos = f * (k - r)
    fer = g * (k - s)
    return dict(
        q=q,
        f=str(f),
        g=str(g),
        k=k, r=r, s=s,
        bosonic_f_kmr=str(bos),
        fermionic_g_kms=str(fer),
        E=str(E),
        equipartition_holds=(bos == fer == E),
    )


def claim_A_equipartition_uniqueness() -> Dict[str, object]:
    """Test whether f(k-r) = g(k-s) = E is unique to q=3 or holds for ALL q."""
    rows = [equipartition_check(q) for q in (2, 3, 4, 5, 7, 8, 9, 11)]
    all_hold = all(r["equipartition_holds"] for r in rows)
    n_holding = sum(1 for r in rows if r["equipartition_holds"])
    return dict(
        claim="A: equipartition f(k-r)=g(k-s)=E is unique to W(3,3)",
        verdict="FALSE" if all_hold else ("TRUE" if n_holding == 1 else "PARTIAL"),
        explanation=(
            "Equipartition holds for ALL symplectic GQ(q,q) by direct algebra "
            "(see closed forms below). It is NOT unique to q=3, so it cannot "
            "be the reason q=3 is special, and cannot uniquely 'solve the "
            "hierarchy problem' for the Standard Model."
            if all_hold else
            "Equipartition fails for some q; uniqueness claim survives."
        ),
        algebraic_proof_general=(
            "f(k-r) = q(q+1)^2/2 * (q^2+1) = q(q+1)^2(q^2+1)/2 = E. "
            "g(k-s) = q(q^2+1)/2 * (q+1)^2 = q(q+1)^2(q^2+1)/2 = E. "
            "Both equal E independent of q."
        ),
        n_q_tested=len(rows),
        n_holding=n_holding,
        rows=rows,
    )


# ---------------------------------------------------------------------------
#  Direct construction of W(3,3) and verification of the spectrum
# ---------------------------------------------------------------------------

def build_w33_explicit() -> Tuple[List[Tuple[int, ...]], List[List[int]]]:
    """Build W(3,3) from F_3^4 with the standard symplectic form
    omega(x, y) = x0*y2 - x2*y0 + x1*y3 - x3*y1.

    Vertices = nonzero vectors mod scalar (so 80/2 = 40 of them).
    Adjacency = nonzero & symplectically orthogonal."""
    F = [0, 1, 2]
    nonzero = [v for v in product(F, repeat=4) if any(v)]

    # Reduce to projective points: keep one representative per F_3^* orbit.
    seen = set()
    points: List[Tuple[int, ...]] = []
    for v in nonzero:
        # Multiply by smallest scalar that makes leading nonzero entry 1.
        for i, x in enumerate(v):
            if x != 0:
                inv = pow(x, -1, 3)
                rep = tuple((c * inv) % 3 for c in v)
                break
        if rep not in seen:
            seen.add(rep)
            points.append(rep)
    assert len(points) == 40

    def omega(a, b):
        return (a[0] * b[2] - a[2] * b[0] + a[1] * b[3] - a[3] * b[1]) % 3

    n = 40
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
    return points, adj


def adjacency_eigenvalues(adj: List[List[int]]) -> Dict[str, object]:
    """Compute the multiset of eigenvalues by power-iteration / numpy."""
    try:
        import numpy as np
    except Exception:
        return dict(error="numpy unavailable")
    A = np.array(adj, dtype=float)
    eig = np.linalg.eigvalsh(A)  # symmetric
    eig_rounded = [round(float(x), 6) for x in eig]
    # Bucket
    buckets: Dict[float, int] = {}
    for x in eig_rounded:
        # snap to nearest integer if close
        snap = round(x)
        if abs(x - snap) < 1e-6:
            x = float(snap)
        buckets[x] = buckets.get(x, 0) + 1
    return dict(
        spectrum=sorted(buckets.items(), key=lambda kv: -kv[0]),
        n=len(eig),
    )


def srg_param_check(adj: List[List[int]]) -> Dict[str, object]:
    n = len(adj)
    # degree
    degs = [sum(row) for row in adj]
    k = degs[0]
    assert all(d == k for d in degs), "not regular"
    # lambda, mu
    lam_set = set()
    mu_set = set()
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(adj[i][t] & adj[j][t] for t in range(n))
            if adj[i][j]:
                lam_set.add(common)
            else:
                mu_set.add(common)
    return dict(
        n=n, k=k,
        lam=sorted(lam_set),
        mu=sorted(mu_set),
        is_srg=(len(lam_set) == 1 and len(mu_set) == 1),
        srg_params=(n, k, sorted(lam_set)[0], sorted(mu_set)[0]),
    )


def claim_B_rank3_decomposition() -> Dict[str, object]:
    pts, adj = build_w33_explicit()
    srg = srg_param_check(adj)
    spec = adjacency_eigenvalues(adj)
    rank3_holds = (
        srg["is_srg"]
        and srg["srg_params"] == (40, 12, 2, 4)
        and isinstance(spec.get("spectrum"), list)
        and dict(spec["spectrum"]) == {12.0: 1, 2.0: 24, -4.0: 15}
    )
    return dict(
        claim="B: 40 = 1 + 24 + 15 spectral decomposition",
        verdict="TRUE" if rank3_holds else "FALSE",
        explanation=(
            "The W(3,3) graph IS strongly regular with the claimed parameters "
            "and the adjacency spectrum is exactly {12^1, 2^24, (-4)^15}. "
            "This is a textbook fact and is verified directly by construction."
            if rank3_holds else
            "Direct construction does NOT reproduce the claimed parameters."
        ),
        srg_check=srg,
        spectrum=spec.get("spectrum"),
        caveat=(
            "The decomposition is REAL (rank-3 implies multiplicity-free as a "
            "PSp(4,3)-module). What is NOT proven by this fact alone is that "
            "the 15-dim irrep is the adjoint of su(4) or that the 24-dim irrep "
            "carries D_4 triality. Those are SEPARATE claims that go beyond "
            "rank-3 SRG theory and are NOT verified by the cascade scripts."
        ),
    )


# ---------------------------------------------------------------------------
#  Claim C: alpha^-1 = 137 numerology
# ---------------------------------------------------------------------------

def claim_C_alpha_137() -> Dict[str, object]:
    k, Phi6 = 12, 7
    integer_137 = k * k - Phi6
    actual = 137.035999084  # CODATA 2018
    error_ppm = abs(integer_137 - actual) / actual * 1e6
    # Try other Phi_n combinations to show how easy this is
    alternatives = []
    for kk in range(8, 16):
        for n in range(2, 14):
            for sign in (+1, -1):
                val = kk * kk + sign * n
                if abs(val - 137) <= 0:
                    alternatives.append((kk, sign * n, val))
    return dict(
        claim="C: alpha^-1 = k^2 - Phi_6 = 137 has structural meaning",
        verdict="NUMEROLOGY",
        integer_value=integer_137,
        actual_value=actual,
        error_ppm=error_ppm,
        explanation=(
            f"Integer 137 misses the true alpha^-1 = 137.036 by {error_ppm:.0f} ppm. "
            "More importantly, the form k^2 - Phi_6 has no derivation: it is a "
            "post-hoc identification of two W(3,3) integers whose subtraction "
            "happens to equal 137. There are MANY such combinations of small "
            "integers giving 137; choosing this one is curve-fitting, not "
            "physics. A real derivation would need to predict 137.036 (not 137) "
            "from the spectral action -- and no such derivation exists."
        ),
        other_easy_137_decompositions=alternatives[:8],
    )


# ---------------------------------------------------------------------------
#  Claim D: hierarchy is a derivation
# ---------------------------------------------------------------------------

def claim_D_hierarchy() -> Dict[str, object]:
    s_sq = 16
    Phi4 = 10
    theory = s_sq * math.log(Phi4)
    obs = math.log(2.435e18 / 246.22)
    err = abs(theory - obs) / obs * 100
    # If we instead use q=2 GQ params: s=-(q+1)=-3, s^2=9; Phi_4(q=2)=5
    q2_theory = 9 * math.log(5)
    return dict(
        claim="D: ln(M_Pl/v_EW) = s^2 * ln(Phi_4) is a derivation",
        verdict="POST-HOC FIT",
        theory_36_84=theory,
        observed_36_83=obs,
        error_pct=err,
        explanation=(
            "The numbers s^2=16 and Phi_4=10 are W(3,3) integers, and 16*ln(10)"
            " happens to land within 0.03% of the observed log-ratio. But the "
            "Coleman-Weinberg 'derivation' is not actually a derivation: it "
            "asserts that the radiative correction to mu^2_H equals exactly "
            "this combination, without computing the W(3,3) Yukawa and gauge "
            "couplings that would enter the CW formula. At q=2 (GQ(2,2)) the "
            "same construction would give 9*ln(5) ~= 14.48, so the framework "
            "predicts hierarchies of 5^9 ~ 2 million for q=2 universes. There "
            "is no falsifiable selection principle picking q=3."
        ),
        q2_alternative=q2_theory,
    )


# ---------------------------------------------------------------------------
#  Bottom line
# ---------------------------------------------------------------------------

def bottom_line() -> Dict[str, object]:
    A = claim_A_equipartition_uniqueness()
    B = claim_B_rank3_decomposition()
    C = claim_C_alpha_137()
    D = claim_D_hierarchy()
    return dict(
        title="W(3,3) Theory of Everything: brutal truth check",
        date="2026-04-08",
        method=(
            "Direct computational and algebraic verification of the four "
            "load-bearing structural claims of the W(3,3) cascade. No spin."
        ),
        results=[A, B, C, D],
        summary={
            "A_equipartition_uniqueness": A["verdict"],
            "B_rank3_decomposition": B["verdict"],
            "C_alpha_137_structural": C["verdict"],
            "D_hierarchy_derivation": D["verdict"],
        },
        what_is_actually_true=[
            "W(3,3) is the symplectic GQ(3,3) collinearity graph SRG(40,12,2,4).",
            "Adjacency spectrum is {12^1, 2^24, (-4)^15} (rank-3 fact).",
            "The 9 master integers and Phi_n(3) cyclotomic values match many "
            "exceptional Lie algebra dimensions exactly: 14, 52, 78, 133, 248. "
            "These are real polynomial identities; some are textbook formulas.",
            "Several SM mixing-angle combinations (sin^2 theta_12 = 4/13 etc.) "
            "match observation to ~1% -- this is also real, but is a numerical "
            "coincidence with no derivation principle.",
        ],
        what_is_NOT_true_or_unproven=[
            "EQUIPARTITION IS NOT UNIQUE TO W(3,3): f(k-r)=g(k-s)=E holds for "
            "ALL symplectic GQ(q,q). The cascade's central uniqueness pillar "
            "is FALSE. (See claim A.)",
            "alpha^-1 = 137 misses CODATA by 26 ppm; the form k^2 - Phi_6 is "
            "post-hoc curve-fitting, not derivation.",
            "The Coleman-Weinberg hierarchy 'derivation' does not actually "
            "compute the W(3,3) couplings; it asserts the result.",
            "The 15-dim eigenspace being adj(SU(4)) and the 24-dim being "
            "D_4-triality are claims beyond rank-3 SRG theory and are NOT "
            "verified by construction in the cascade scripts.",
        ],
        honest_status=(
            "W(3,3) is a beautiful finite geometry whose graph invariants "
            "DO encode several genuine polynomial identities for exceptional "
            "Lie algebra dimensions, and DO match a handful of SM observables "
            "to good accuracy. It is NOT a derivation of the Standard Model: "
            "key 'uniqueness' arguments fail (equipartition holds for all q), "
            "and the hierarchy / fine-structure 'proofs' are post-hoc fits "
            "rather than computations. The honest scientific status is "
            "'striking pattern-match worth investigating', not 'solved theory "
            "of everything'."
        ),
    )


def main() -> None:
    out = bottom_line()
    print("=" * 70)
    print("  W(3,3) BRUTAL TRUTH CHECK")
    print("=" * 70)
    for r in out["results"]:
        print()
        print(f"  {r['claim']}")
        print(f"    VERDICT: {r['verdict']}")
        print(f"    {r['explanation'][:300]}...")
    print()
    print("-" * 70)
    print("WHAT IS TRUE:")
    for s in out["what_is_actually_true"]:
        print(f"  + {s}")
    print()
    print("WHAT IS NOT TRUE / UNPROVEN:")
    for s in out["what_is_NOT_true_or_unproven"]:
        print(f"  - {s}")
    print()
    print("HONEST STATUS:")
    print(f"  {out['honest_status']}")
    print()

    out_path = Path(__file__).resolve().parents[1] / "data" / "w33_brutal_truth.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
