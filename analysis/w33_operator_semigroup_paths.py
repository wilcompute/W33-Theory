"""W(3,q) arithmetic-operator semigroup audit.

This script pushes beyond the May 19 single-operator closure wave. Instead of
asking whether one arithmetic operator lands back on the shift tower, it asks
whether short operator chains do so persistently across the tower.

The strongest outcome is the radical ladder on the cyclotomic pair

    Phi3(q) = q^2 + q + 1,
    Phi6(q) = q^2 - q + 1,

because Phi6(q+1) = Phi3(q) identically. In the extended q-window the ladder
fails exactly at the nonsquarefree points; the first defect is the local
Heawood cube

    Phi3(18) = Phi6(19) = 343 = 7^3 = Phi6(3)^3.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.arithmetic import ARITHMETIC_OPERATORS, prime_factorization, radical, safe_apply_operator_chain
from w33.shift_tower import build_shift_tower, build_shift_tower_reverse_lookup, shift_tower_primitives

Q_VALUES = range(3, 21)
CHAIN_LENGTHS = (2, 3)
DEFECT_SCAN_MAX_Q = 1000


def collect_matches() -> list[dict[str, int | str | bool | list[str]]]:
    tower = build_shift_tower(q_values=Q_VALUES)
    reverse = build_shift_tower_reverse_lookup(tower=tower, q_values=Q_VALUES)
    matches: list[dict[str, int | str | bool | list[str]]] = []

    chains = []
    names = list(ARITHMETIC_OPERATORS)
    for length in CHAIN_LENGTHS:
        chains.extend(product(names, repeat=length))

    for q, primitives in tower.items():
        for primitive_name, value in primitives.items():
            for chain in chains:
                image = safe_apply_operator_chain(value, chain)
                if image is None or image < 1:
                    continue
                for target_name, q_target in reverse.get(image, []):
                    matches.append(
                        {
                            "source_q": q,
                            "source_primitive": primitive_name,
                            "source_value": value,
                            "chain": list(chain),
                            "chain_key": "->".join(chain),
                            "image": image,
                            "target_q": q_target,
                            "target_primitive": target_name,
                            "delta_q": q_target - q,
                            "same_q": q_target == q,
                        }
                    )
    return matches


def persistent_patterns(matches: list[dict[str, int | str | bool | list[str]]]) -> list[dict[str, int | str | list[int]]]:
    counts: Counter[tuple[str, str, str, int]] = Counter()
    support: dict[tuple[str, str, str, int], set[int]] = defaultdict(set)

    for row in matches:
        key = (
            str(row["chain_key"]),
            str(row["source_primitive"]),
            str(row["target_primitive"]),
            int(row["delta_q"]),
        )
        counts[key] += 1
        support[key].add(int(row["source_q"]))

    persistent: list[dict[str, int | str | list[int]]] = []
    for (chain_key, source, target, delta_q), count in counts.items():
        q_support = sorted(support[(chain_key, source, target, delta_q)])
        if len(q_support) >= 3:
            persistent.append(
                {
                    "chain": chain_key,
                    "source": source,
                    "target": target,
                    "delta_q": delta_q,
                    "match_count": count,
                    "support_q": q_support,
                }
            )

    persistent.sort(key=lambda row: (-len(row["support_q"]), -row["match_count"], row["chain"], row["source"], row["target"], row["delta_q"]))
    return persistent


def radical_ladder_defects() -> dict[str, list[dict[str, object]]]:
    phi3_defects = []
    phi6_defects = []

    for q in range(3, 21):
        value = shift_tower_primitives(q)["Phi3"]
        if radical(value) != shift_tower_primitives(q + 1)["Phi6"]:
            phi3_defects.append(
                {
                    "q": q,
                    "value": value,
                    "radical": radical(value),
                    "prime_factorization": prime_factorization(value),
                }
            )

    for q in range(4, 21):
        value = shift_tower_primitives(q)["Phi6"]
        if radical(value) != shift_tower_primitives(q - 1)["Phi3"]:
            phi6_defects.append(
                {
                    "q": q,
                    "value": value,
                    "radical": radical(value),
                    "prime_factorization": prime_factorization(value),
                }
            )

    return {"phi3": phi3_defects, "phi6": phi6_defects}


def defect_prime_classes(max_q: int = DEFECT_SCAN_MAX_Q) -> dict[str, object]:
    repeated_primes: set[int] = set()

    for q in range(3, max_q + 1):
        packet = shift_tower_primitives(q)
        for name in ("Phi3", "Phi6"):
            for p, exponent in prime_factorization(packet[name]).items():
                if exponent > 1:
                    repeated_primes.add(p)

    sorted_primes = sorted(repeated_primes)
    classes = {
        "mod_0": [p for p in sorted_primes if p % 3 == 0],
        "mod_1": [p for p in sorted_primes if p % 3 == 1],
        "mod_2": [p for p in sorted_primes if p % 3 == 2],
    }
    return {
        "max_q": max_q,
        "repeated_primes": sorted_primes,
        "mod_3_classes": classes,
        "all_repeated_primes_are_1_mod_3": all(p % 3 == 1 for p in sorted_primes),
        "has_any_2_mod_3_repeat": any(p % 3 == 2 for p in sorted_primes),
    }


def build_payload() -> dict[str, object]:
    matches = collect_matches()
    persistent = persistent_patterns(matches)
    defects = radical_ladder_defects()
    prime_classes = defect_prime_classes()

    headline_checks = {
        "rad->rad(Phi3) = Phi3": [
            row for row in persistent
            if row["chain"] == "rad->rad" and row["source"] == "Phi3" and row["target"] == "Phi3" and row["delta_q"] == 0
        ],
        "rad->rad(Phi6) = Phi6": [
            row for row in persistent
            if row["chain"] == "rad->rad" and row["source"] == "Phi6" and row["target"] == "Phi6" and row["delta_q"] == 0
        ],
        "phi->d(Phi6) = mu": [
            row for row in persistent
            if row["chain"] == "phi->d" and row["source"] == "Phi6" and row["target"] == "mu" and row["delta_q"] == 0
        ],
        "cot->sigma_1->Omega(k) = lambda": [
            row for row in persistent
            if row["chain"] == "cot->sigma_1->Omega" and row["source"] == "k" and row["target"] == "lambda" and row["delta_q"] == 0
        ],
        "phi->d->d(v) = lambda": [
            row for row in persistent
            if row["chain"] == "phi->d->d" and row["source"] == "v" and row["target"] == "lambda" and row["delta_q"] == 0
        ],
    }

    return {
        "q_window": list(Q_VALUES),
        "chain_lengths": list(CHAIN_LENGTHS),
        "operator_names": list(ARITHMETIC_OPERATORS),
        "match_count": len(matches),
        "matches": matches,
        "persistent_patterns": persistent,
        "radical_ladder_defects": defects,
        "defect_prime_classes": prime_classes,
        "headline_checks": headline_checks,
        "summary": {
            "statement": (
                "Short arithmetic-operator chains on the W(3,q) shift tower reveal a genuine semigroup layer. The strongest extended family is the radical ladder: rad(Phi3(q)) = Phi6(q+1) and rad(Phi6(q)) = Phi3(q-1) whenever the shifted cyclotomic values are squarefree, while rad∘rad stabilizes the cyclotomic pair. On 3 <= q <= 20 the first and cleanest defect occurs at Phi3(18) = Phi6(19) = 343 = 7^3, so the first failure is exactly a Heawood-cube collapse rather than a generic breakdown. Extending the defect scan to q <= 1000 shows that every repeated prime factor lies in the split class p ≡ 1 (mod 3), with no repeated p ≡ 2 (mod 3) primes at all. More local composition families still survive on the original q=3..7 window, notably d(phi(Phi6(q))) = mu(q), Omega(sigma_1(cot(k(q)))) = lambda(q), and d(d(phi(v(q)))) = lambda(q)."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_operator_semigroup_paths.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) ARITHMETIC-OPERATOR SEMIGROUP AUDIT")
    print("=" * 88)
    print(f"q-window: {payload['q_window'][0]}..{payload['q_window'][-1]}")
    print(f"operators: {', '.join(payload['operator_names'])}")
    print(f"exact tower hits from chains of length 2/3: {payload['match_count']}")
    print("\nTop persistent patterns:")
    for row in payload["persistent_patterns"][:12]:
        support = ",".join(str(q) for q in row["support_q"])
        print(
            f"  {row['chain']}({row['source']}) -> {row['target']} with delta_q={row['delta_q']} "
            f"on q={support} (support={len(row['support_q'])})"
        )
    print("\nRadical-ladder defects:")
    for family, rows in payload["radical_ladder_defects"].items():
        if not rows:
            print(f"  {family}: none")
            continue
        for row in rows:
            print(f"  {family}: q={row['q']}, value={row['value']}, rad={row['radical']}, factors={row['prime_factorization']}")
    classes = payload["defect_prime_classes"]
    print("\nDefect-prime classes up to q={}:".format(classes["max_q"]))
    print(f"  repeated primes: {classes['repeated_primes']}")
    print(f"  mod 3 classes: {classes['mod_3_classes']}")
    print(f"  all repeated primes are 1 mod 3: {classes['all_repeated_primes_are_1_mod_3']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()