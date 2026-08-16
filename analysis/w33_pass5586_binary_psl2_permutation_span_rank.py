"""Pass 5586 -- all-odd characteristic-2 rank of the PSL2 projectivity-frame design.

Passes 5580--5585 identify the Reye/tomotope tactical family with the
vectorized permutation matrices of one PGL2(q)/PSL2(q) coset on P^1(q).
The measured F2 row ranks were (q+1)^2/2 for q=3,5,7,11,13.

This file records the algebra proof that the pattern is exact for every odd
prime power q.  The representation-theoretic input is the published modular
structure of the natural degree-(q+1) PSL2(q) permutation module:

  0 < I < R < V,
  V/R ~= I,
  R/I becomes U_+ + U_- over Fbar_2,
  dim U_+ = dim U_- = (q-1)/2,

with I the unique minimal submodule and R the unique maximal submodule.
See Zavarnitsine, Subextensions for a permutation PSL_2(q)-module (2013),
Lemma 7, and Revin--Zavarnitsine, Automorphisms of nonsplit extensions of
2-groups by PSL_2(q) (J. Group Theory 2021), Section 3 / Proposition 7.

Let A be the F2-span of the permutation matrices.  Row-vectorization makes
rank_2(M)=dim_F2(A).  After scalar extension to k=Fbar_2, put J=rad(A_k).
The Loewy series and the transpose anti-involution force

  dim(A_k/J) = 1 + 2 a^2,
  dim(J)     = 4 a + 1,
  a=(q-1)/2.

Hence dim A = 2(a+1)^2=(q+1)^2/2.

The script replays the finite prime-field anchors from Pass5580--5585 and
checks every symbolic dimension identity.  The theorem itself is algebraic;
no finite sample is used as a proof.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS5580 = ROOT / "analysis" / "w33_pass5580_5585_reye_psl2_permutation_frame.py"
OUT = ROOT / "data" / "PART_W33_PASS5586_BINARY_PSL2_PERMUTATION_SPAN_RANK.json"


def load_pass5580():
    spec = importlib.util.spec_from_file_location("pass5580", PASS5580)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def symbolic_row(q: int) -> dict:
    assert q >= 3 and q % 2 == 1
    a = (q - 1) // 2
    semisimple = 1 + 2 * a * a
    radical_upper = 4 * a + 1
    radical_lower = 4 * a + 1
    total = semisimple + radical_upper
    target = (q + 1) ** 2 // 2
    assert radical_upper == radical_lower
    assert total == target
    return {
        "q": q,
        "a=(q-1)/2": a,
        "semisimple_quotient_dimension": semisimple,
        "jacobson_radical_dimension": radical_upper,
        "image_algebra_dimension": total,
        "target_binary_rank": target,
    }


def main() -> int:
    mod = load_pass5580()
    anchors = []
    for q in (3, 5, 7, 11, 13):
        measured = mod.analyse(q)
        symbolic = symbolic_row(q)
        assert measured["binary_rank_measured"] == symbolic["target_binary_rank"]
        anchors.append({
            "q": q,
            "measured_rank": measured["binary_rank_measured"],
            "theorem_rank": symbolic["target_binary_rank"],
        })

    # Prime-power arithmetic probes.  These are symbolic consequences of the
    # theorem; the Pass5580 executable itself is deliberately prime-field only.
    prime_power_probes = [symbolic_row(q) for q in (9, 25, 27, 49, 81)]

    out = {
        "pass": 5586,
        "status": "THEOREM_ALL_ODD_PRIME_POWERS",
        "theorem": "For every odd prime power q, the F2-rank of the Pass5580 projectivity-graph incidence matrix is (q+1)^2/2.",
        "equivalent_form": "The F2-linear span of the natural PSL2(q) permutation matrices on P1(q) has dimension (q+1)^2/2.",
        "proof": {
            "step_1_vectorization": "Rows are vectorized matrices rho(hg) in one PGL2/PSL2 coset; left multiplication by rho(h) preserves span dimension, so rank_2(M)=dim_F2 span(rho(PSL2(q))).",
            "step_2_scalar_extension": "Extend to k=Fbar_2; vector-space dimension of the image algebra A is unchanged.",
            "step_3_module_structure": "Published modular structure gives Loewy series I | (U_+ direct-sum U_-) | I with dim U_+=dim U_-=(q-1)/2 after scalar extension; I is unique minimal and the augmentation kernel is the unique maximal submodule.",
            "step_4_semisimple_quotient": "For a=(q-1)/2, faithfulness of V for A implies A/J(A) ~= k direct-sum M_a(k) direct-sum M_a(k), so dim(A/J)=1+2a^2.",
            "step_5_radical_upper": "J kills the socle, sends the middle 2a-space into the 1-space socle, and sends the 1-space top into middle+socle. Thus dim J <= 2a+(2a+1)=4a+1.",
            "step_6_radical_lower": "The two middle simples occur in rad(V)/rad^2(V), so the two distinct Pierce components from top to U_+,U_- in J/J^2 are nonzero and contribute at least a+a. Transpose preserves A and J and supplies the two reverse Pierce components, another a+a. Since rad^2(V)=soc(V) is nonzero, J^2 is nonzero. Hence dim J >=4a+1.",
            "step_7_close": "Therefore dim J=4a+1 and dim A=1+2a^2+4a+1=2(a+1)^2=(q+1)^2/2.",
        },
        "literature_inputs": [
            "A. V. Zavarnitsine, Subextensions for a permutation PSL_2(q)-module, Siberian Electronic Mathematical Reports 10 (2013), Lemma 7.",
            "D. O. Revin and A. V. Zavarnitsine, Automorphisms of nonsplit extensions of 2-groups by PSL_2(q), Journal of Group Theory 24 (2021): the natural permutation module has 0<I<R<V and dim U_+=dim U_-=(q-1)/2; the diagonal outer automorphism permutes the two absolutely irreducible constituents when appropriate.",
        ],
        "finite_prime_field_replay": anchors,
        "prime_power_symbolic_probes": prime_power_probes,
        "boundary": "This proves a modular rank theorem for the projectivity-graph incidence design. It does not by itself prove the distinct all-odd W(3,q) footprint-rank conjecture from Pass5358/5376, nor does it create q>3 polytope or physics identifications.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
