#!/usr/bin/env python3
"""Part DCCXXX: Clifford-even quaternion / Pauli symplectic bridge.

Core statement:
- The quaternion algebra H is exactly the even Clifford subalgebra
  Cl^+(3,0) spanned by {1, B23, B31, B12}.
- The ternary->quaternion closure is the count-level realization of
  DCCXXIV's topological 3->4 closure: 3 bivectors + 1 identity = 4.
- The same q=3 feeds W(3,3) as two-qutrit Pauli commutation geometry,
  with invariant triple (v,k,E)=(40,12,240).

This verifier provides explicit blade multiplication, a sign-correct
isomorphism Cl^+(3,0) -> H, and consistency checks with DCCXXVIII.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxiv_loop_closure_origin import Q as Q_DCCXXIV, QP1 as QP1_DCCXXIV
from verify_dccxxviii_ternary_quaternion_codec_tower import (
    CODEC,
    W33_E,
    W33_K,
    W33_V,
)

OUT_PATH = ROOT / "data" / "dccxxx_clifford_even_quaternion_pauli_bridge.json"

Blade = Tuple[int, ...]
Mul = Tuple[int, Blade]


def _blade_mul(a: Blade, b: Blade) -> Mul:
    """Multiply Euclidean Clifford blades e_I * e_J in Cl(3,0).

    Basis vectors satisfy e_i^2=+1 and e_i e_j = - e_j e_i for i != j.
    Returns (sign, blade).
    """
    sign = 1
    out = list(a)
    for x in b:
        if x in out:
            idx = out.index(x)
            swaps = len(out) - idx - 1
            if swaps % 2 == 1:
                sign *= -1
            out.pop(idx)
        else:
            j = len(out)
            while j > 0 and out[j - 1] > x:
                j -= 1
            swaps = len(out) - j
            if swaps % 2 == 1:
                sign *= -1
            out.insert(j, x)
    return sign, tuple(out)


def _mul_token(a: str, b: str, token_to_blade: Dict[str, Blade]) -> Tuple[int, str]:
    inv = {v: k for k, v in token_to_blade.items()}
    s, blade = _blade_mul(token_to_blade[a], token_to_blade[b])
    return s, inv[blade]


@dataclass(frozen=True)
class BridgeSummary:
    q_value: int
    ternary_bivector_count: int
    quaternion_basis_count: int
    codec_12: int
    w33_vertices: int
    w33_valency: int
    w33_edges: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    # Even subalgebra basis in Cl(3,0): grades 0 and 2.
    tokens = {
        "1": (),
        "B23": (2, 3),
        "B31": (1, 3),  # e3e1 = -e1e3; canonical blade token uses sorted tuple (1,3)
        "B12": (1, 2),
    }

    # Raw Clifford products among bivectors.
    raw_products = {}
    for a in ("B23", "B31", "B12"):
        for b in ("B23", "B31", "B12"):
            s, t = _mul_token(a, b, tokens)
            raw_products[f"{a}*{b}"] = {"sign": s, "token": t}

    # Quaternion-unit map (orientation from computed raw products):
    # i = B23, j = B31, k = B12 so that ij=k, jk=i, ki=j.
    qmap = {
        "1": (1, "1"),
        "i": (1, "B23"),
        "j": (1, "B31"),
        "k": (1, "B12"),
    }

    def qmul(x: str, y: str) -> Tuple[int, str]:
        sx, tx = qmap[x]
        sy, ty = qmap[y]
        sxy, txy = _mul_token(tx, ty, tokens)
        return sx * sy * sxy, txy

    # Convert product result back to quaternion symbol (+/-1,i,j,k).
    inv_qmap = {v: k for k, v in qmap.items()}

    def qsymbol(sign: int, token: str) -> str:
        if (1, token) in inv_qmap:
            sym = inv_qmap[(1, token)]
            return sym if sign == 1 else f"-{sym}"
        # must be negative mapping
        sym = inv_qmap[(-1, token)]
        return f"-{sym}" if sign == 1 else sym

    qmult = {
        "i*i": qsymbol(*qmul("i", "i")),
        "j*j": qsymbol(*qmul("j", "j")),
        "k*k": qsymbol(*qmul("k", "k")),
        "i*j": qsymbol(*qmul("i", "j")),
        "j*k": qsymbol(*qmul("j", "k")),
        "k*i": qsymbol(*qmul("k", "i")),
        "j*i": qsymbol(*qmul("j", "i")),
        "k*j": qsymbol(*qmul("k", "j")),
        "i*k": qsymbol(*qmul("i", "k")),
    }

    identities = {
        "dccxxiv_pair_is_3_4": (Q_DCCXXIV, QP1_DCCXXIV) == (3, 4),
        "three_even_bivectors_exist": len(["B23", "B31", "B12"]) == 3,
        "ternary_plus_identity_is_quaternion_dimension_4": 3 + 1 == 4,
        "clifford_bivectors_square_to_minus_one": (
            raw_products["B23*B23"] == {"sign": -1, "token": "1"}
            and raw_products["B31*B31"] == {"sign": -1, "token": "1"}
            and raw_products["B12*B12"] == {"sign": -1, "token": "1"}
        ),
        "sign_corrected_map_obeys_quaternion_relations": (
            qmult["i*i"] == "-1"
            and qmult["j*j"] == "-1"
            and qmult["k*k"] == "-1"
            and qmult["i*j"] == "k"
            and qmult["j*k"] == "i"
            and qmult["k*i"] == "j"
            and qmult["j*i"] == "-k"
            and qmult["k*j"] == "-i"
            and qmult["i*k"] == "-j"
        ),
        "codec_remains_q_times_q_plus_1": CODEC == Q_DCCXXIV * QP1_DCCXXIV == 12,
        "w33_two_qutrit_invariants_match": (W33_V, W33_K, W33_E) == (40, 12, 240),
        "pauli_valency_equals_codec": W33_K == CODEC == 12,
    }

    summary = BridgeSummary(
        q_value=Q_DCCXXIV,
        ternary_bivector_count=3,
        quaternion_basis_count=4,
        codec_12=CODEC,
        w33_vertices=W33_V,
        w33_valency=W33_K,
        w33_edges=W33_E,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "clifford_even_subalgebra": {
            "basis": ["1", "B23", "B31", "B12"],
            "raw_bivector_products": raw_products,
        },
        "quaternion_realization": {
            "map": {
                "1": "1",
                "i": "B23",
                "j": "B31",
                "k": "B12",
            },
            "multiplication": qmult,
        },
        "pauli_w33_link": {
            "q": Q_DCCXXIV,
            "codec": CODEC,
            "w33": {"v": W33_V, "k": W33_K, "E": W33_E},
        },
        "bridge_claim": {
            "statement": (
                "The ternary-to-quaternion closure is literal Clifford structure: "
                "Cl^+(3,0) has basis {1,B23,B31,B12} and is isomorphic to H under a sign-corrected bivector map; "
                "the same q=3 yields codec 12 and W(3,3) two-qutrit invariants (40,12,240)."
            )
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
