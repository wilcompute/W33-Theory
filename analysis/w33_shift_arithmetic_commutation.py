"""W(3,3) shift-tower / arithmetic-operator commutation audit.

This script extends the May 19 shift-tower theorem by applying the three
classical arithmetic functions

    phi(n)    Euler totient
    d(n)      divisor count
    sigma_1(n) divisor sum

and then lifting further to the strongest exact next operators discovered
after the first closure wave:

    rad(n)      squarefree kernel
    Omega(n)    total prime-factor count
    cot(n)      cototient n - phi(n)
    J2(n)       Jordan totient J_2
    J4(n)       Jordan totient J_4
    D(n)        arithmetic derivative

not just to the q=3 substrate, but to the full shift tower q=3..7:

    v    = (q + 1)(q^2 + 1)
    k    = q(q + 1)
    lam  = q - 1
    mu   = q + 1
    Phi3 = q^2 + q + 1
    Phi4 = q^2 + 1
    Phi6 = q^2 - q + 1

The output tracks exact hits where an arithmetic image of one primitive at q
lands on another primitive at q' in the same q-window, producing a finite
commutation dictionary between the arithmetic layer and the shift layer.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.arithmetic import (
    arithmetic_derivative,
    cototient,
    divisor_count,
    divisor_sum,
    euler_totient,
    jordan_totient,
    operator_lift_headlines,
    radical,
    total_prime_factor_count,
)
from w33.shift_tower import build_shift_tower, build_shift_tower_reverse_lookup

Q_VALUES = range(3, 8)

OPS = {
    "phi": euler_totient,
    "d": divisor_count,
    "sigma_1": divisor_sum,
    "rad": radical,
    "Omega": total_prime_factor_count,
    "cot": cototient,
    "J2": lambda n: jordan_totient(n, 2),
    "J4": lambda n: jordan_totient(n, 4),
    "D": arithmetic_derivative,
}


def arithmetic_matches() -> list[dict[str, int | str | bool]]:
    tower = build_shift_tower(q_values=Q_VALUES)
    reverse = build_shift_tower_reverse_lookup(tower=tower, q_values=Q_VALUES)
    matches: list[dict[str, int | str | bool]] = []
    for q, primitives in tower.items():
        for primitive_name, value in primitives.items():
            for op_name, fn in OPS.items():
                image = fn(value)
                for target_name, q_target in reverse.get(image, []):
                    matches.append(
                        {
                            "source_q": q,
                            "source_primitive": primitive_name,
                            "source_value": value,
                            "operation": op_name,
                            "image": image,
                            "target_q": q_target,
                            "target_primitive": target_name,
                            "delta_q": q_target - q,
                            "same_q": q_target == q,
                        }
                    )
    return matches


def persistent_patterns(matches: list[dict[str, int | str | bool]]) -> list[dict[str, int | str]]:
    pattern_counts: Counter[tuple[str, str, str, int]] = Counter()
    source_q_support: dict[tuple[str, str, str, int], set[int]] = defaultdict(set)
    for match in matches:
        key = (
            str(match["operation"]),
            str(match["source_primitive"]),
            str(match["target_primitive"]),
            int(match["delta_q"]),
        )
        pattern_counts[key] += 1
        source_q_support[key].add(int(match["source_q"]))

    persistent = []
    for (operation, source, target, delta_q), count in pattern_counts.items():
        q_support = sorted(source_q_support[(operation, source, target, delta_q)])
        if len(q_support) >= 2:
            persistent.append(
                {
                    "operation": operation,
                    "source": source,
                    "target": target,
                    "delta_q": delta_q,
                    "match_count": count,
                    "support_q": q_support,
                }
            )
    persistent.sort(key=lambda row: (-row["match_count"], row["operation"], row["source"], row["target"], row["delta_q"]))
    return persistent


def build_payload() -> dict[str, object]:
    tower = build_shift_tower(q_values=Q_VALUES)
    matches = arithmetic_matches()
    targets = Counter(f"{row['target_primitive']}@{row['target_q']}" for row in matches)
    persistent = persistent_patterns(matches)
    same_q_matches = sum(1 for row in matches if row["same_q"])
    cross_q_matches = sum(1 for row in matches if not row["same_q"])

    headline_checks = {
        "phi(Phi3(q)) = k(q) support": [
            row for row in persistent
            if row["operation"] == "phi" and row["source"] == "Phi3" and row["target"] == "k" and row["delta_q"] == 0
        ],
        "phi(Phi6(q)) = k(q-1) support": [
            row for row in persistent
            if row["operation"] == "phi" and row["source"] == "Phi6" and row["target"] == "k" and row["delta_q"] == -1
        ],
        "sigma_1(lambda(q)) = lambda(q+1) support": [
            row for row in persistent
            if row["operation"] == "sigma_1" and row["source"] == "lambda" and row["target"] == "lambda" and row["delta_q"] == 1
        ],
        "rad(Phi3(q)) = Phi6(q+1) support": [
            row for row in persistent
            if row["operation"] == "rad" and row["source"] == "Phi3" and row["target"] == "Phi6" and row["delta_q"] == 1
        ],
        "rad(Phi6(q)) = Phi3(q-1) support": [
            row for row in persistent
            if row["operation"] == "rad" and row["source"] == "Phi6" and row["target"] == "Phi3" and row["delta_q"] == -1
        ],
        "largest repeated target": targets.most_common(10),
        "same_q_matches": same_q_matches,
        "cross_q_matches": cross_q_matches,
    }

    return {
        "q_window": [3, 4, 5, 6, 7],
        "operator_names": list(OPS.keys()),
        "tower": tower,
        "match_count": len(matches),
        "matches": matches,
        "persistent_patterns": persistent,
        "target_histogram": targets.most_common(),
        "q3_operator_lifts": operator_lift_headlines(),
        "headline_checks": headline_checks,
        "summary": {
            "statement": (
                f"The arithmetic layer and the shift tower do not behave independently. Across q=3..7, exact operator images land back on shifted primitive values {len(matches)} times, with {cross_q_matches} cross-q hits. Beyond the original phi/d/sigma_1 packet, the strongest new families are the squarefree cyclotomic ladder rad(Phi3(q)) -> Phi6(q+1) on q=3,4,5,6 and rad(Phi6(q)) -> Phi3(q-1) on q=4,5,6,7, together with the q=3 operator lifts J2(lambda)=q, J2(q)=2^q, J2(mu)=k, J4(mu)=|E|, rad(v)=Phi4, cot(v)=f, Omega(v)=mu, Omega(|E|)=q!, D(2^q)=k, D(Phi4)=Phi6, and D(q^q)=q^q."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_shift_arithmetic_commutation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,3) SHIFT-TOWER / ARITHMETIC COMMUTATION AUDIT")
    print("=" * 88)
    print(f"q-window: {payload['q_window']}")
    print(f"operators: {', '.join(payload['operator_names'])}")
    print(f"exact primitive hits: {payload['match_count']}")
    print(f"same-q hits: {payload['headline_checks']['same_q_matches']}")
    print(f"cross-q hits: {payload['headline_checks']['cross_q_matches']}")
    print("\nq=3 operator lifts:")
    for item in payload["q3_operator_lifts"]:
        if item["match"]:
            print(f"  {item['identity']}  {item['substrate']}")
    print("\nTop repeated targets:")
    for target, count in payload["headline_checks"]["largest repeated target"][:10]:
        print(f"  {target:<14s} {count}")
    print("\nPersistent patterns:")
    for row in payload["persistent_patterns"][:12]:
        support = ",".join(str(q) for q in row["support_q"])
        print(
            f"  {row['operation']}({row['source']}) -> {row['target']} with delta_q={row['delta_q']} "
            f"on q={support} (count={row['match_count']})"
        )
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
