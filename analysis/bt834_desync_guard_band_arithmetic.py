#!/usr/bin/env python3
"""
BT834 - Desync guard-band arithmetic.

BT830 found the first full route-epoch desync at n=5 with remainder 24.  BT834
explains it exactly.

    T(n) = 4(7^n - 1)
    route epoch = 8n

So full sync is equivalent to 2n | 7^n - 1.  For odd prime powers p^a | n
with p != 7, this requires ord_{p^a}(7) | n; if 7 | n, sync is impossible.
The first failing cover prime is 5 because ord_5(7)=4 does not divide 5, and
the remainder is 24=f.
"""
from __future__ import annotations

from math import gcd
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    x = n
    while d * d <= x:
        while x % d == 0:
            out[d] = out.get(d, 0) + 1
            x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        out[x] = out.get(x, 0) + 1
    return out


def multiplicative_order(a: int, m: int) -> int | None:
    if gcd(a, m) != 1:
        return None
    cur = 1
    for n in range(1, m * m + 1):
        cur = (cur * a) % m
        if cur == 1:
            return n
    raise AssertionError(f"order search failed for {a} mod {m}")


def commit_ticks(n: int) -> int:
    return 4 * (7**n - 1)


def blockers(n: int) -> list[dict]:
    rows = []
    for p, exp in sorted(factor(n).items()):
        if p == 2:
            continue
        modulus = p**exp
        order = multiplicative_order(7, modulus)
        ok = order is not None and n % order == 0
        rows.append({
            "prime": p,
            "power": modulus,
            "order_of_7": order,
            "order_divides_n": ok,
            "blocks_sync": not ok,
        })
    return rows


def level_row(n: int) -> dict:
    t = commit_ticks(n)
    route = 8 * n
    remainder = t % route
    return {
        "level": n,
        "factorization": factor(n),
        "route_epoch": route,
        "commit_ticks": t,
        "remainder": remainder,
        "sync": remainder == 0,
        "remainder_over_4": remainder // 4,
        "condition_remainder_mod_2n": (7**n - 1) % (2 * n),
        "blockers": blockers(n),
    }


def main() -> None:
    rows = [level_row(n) for n in range(1, 61)]
    desync = [row for row in rows if not row["sync"]]
    sync = [row for row in rows if row["sync"]]
    first = desync[0]
    cover_prime_rows = [level_row(k) for k in [3, 5, 7, 11, 13, 17, 19]]

    checks = {
        "sync_equivalence_holds": all((row["remainder"] == 0) == (row["condition_remainder_mod_2n"] == 0) for row in rows),
        "first_desync_is_5": first["level"] == 5,
        "first_desync_remainder_is_24": first["remainder"] == 24,
        "first_desync_blocker_is_prime_5_order_4": first["blockers"] == [{
            "prime": 5,
            "power": 5,
            "order_of_7": 4,
            "order_divides_n": False,
            "blocks_sync": True,
        }],
        "levels_1_to_4_sync": [row["level"] for row in rows[:4] if row["sync"]] == [1, 2, 3, 4],
        "cover_prime_3_syncs": cover_prime_rows[0]["sync"],
        "cover_prime_5_is_first_guard_band": cover_prime_rows[1]["level"] == 5 and not cover_prime_rows[1]["sync"],
        "cover_prime_7_blocks_by_non_coprime_base": cover_prime_rows[2]["blockers"][0]["order_of_7"] is None,
        "all_desync_rows_have_blockers": all(row["blockers"] and any(b["blocks_sync"] for b in row["blockers"]) for row in desync),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT834 check failed: {name}")

    out = {
        "theorem": "BT834 desync guard-band arithmetic",
        "criterion": {
            "full_sync": "8n divides T(n)=4(7^n-1)",
            "equivalent_condition": "2n divides 7^n-1",
            "odd_prime_power_rule": "for p^a | n and p != 7, ord_{p^a}(7) must divide n; if 7 | n, sync is impossible",
        },
        "levels_1_to_60": rows,
        "sync_levels_1_to_60": [row["level"] for row in sync],
        "desync_levels_1_to_60": [row["level"] for row in desync],
        "cover_prime_rows": cover_prime_rows,
        "interpretation": {
            "first_guard_band": "n=5 is the first cover index where the durable tomotope clock and the full route epoch separate",
            "remainder": "24=f, the local slot-stabilizer/runtime-lift size",
            "architecture": "cover-indexed storage begins to require a real guard band before the q=7 external tomotope clock appears",
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt834_desync_guard_band_arithmetic.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
