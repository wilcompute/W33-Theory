"""
Part CCLXXI — Monster Group, Baby Monster & Monstrous Moonshine
Bridge every key parameter to W(3,3) closed-form integers.

Sections
--------
§1  Sporadic groups census          (B01–B05)
§2  Moonshine primes                (B06–B13)
§3  Monster order prime factorisation (B14–B22)
§4  Top-3 Monster primes & min rep  (B23–B27)
§5  Baby Monster order              (B28–B32)
§6  Moonshine representations / j   (B33–B38)
§7  String-theory cross-links       (B39–B40)

Checks: 40 / 40
"""

import json
from pathlib import Path

# ── W(3,3) strongly regular graph constants ──────────────────────────────────
V         = 40
K         = 12
LAM       = 2
MU        = 4
Q         = 3
M_LAM     = 27        # Q**Q = 3**3
PHI3      = 13        # eigenvalue multiplicity
PHI4      = 10
PHI6      = 7
EDGES     = 240       # V*K // 2
LAP_TOP   = 16
LAP_MID   = 10
AUT_ORDER = 51840

# ── Group orders (exact) ──────────────────────────────────────────────────────
# Monster group  M
MONSTER_ORDER = (
    2**46 * 3**20 * 5**9 * 7**6 * 11**2 * 13**3
    * 17 * 19 * 23 * 29 * 31 * 41 * 47 * 59 * 71
)

# Baby Monster  B
BABY_ORDER = (
    2**41 * 3**13 * 5**6 * 7**2
    * 11 * 13 * 17 * 19 * 23 * 31 * 47
)


def prime_exp(n: int, p: int) -> int:
    """Return exponent of prime p in the factorisation of n."""
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


# ── Check harness ─────────────────────────────────────────────────────────────
checks: list[dict] = []


def chk(bid: str, lhs: int, rhs: int, note: str = "") -> bool:
    ok = bool(lhs == rhs)
    checks.append({"id": bid, "lhs": int(lhs), "rhs": int(rhs),
                   "pass": ok, "note": note})
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {bid}: {lhs} == {rhs}  {note}")
    return ok


# ════════════════════════════════════════════════════════════════════════════
# §1  Sporadic groups census
# ════════════════════════════════════════════════════════════════════════════

chk("B01", 26, 2 * K + 2,
    "Total sporadic simple groups = 2K+2")

chk("B02", 20, EDGES // K,
    "Happy Family (Monster subquotients) = EDGES/K = 240/12")

chk("B03", 6, LAM * Q,
    "Pariah groups (outside Happy Family) = LAM*Q = 2×3")

chk("B04", 15, K + Q,
    "Distinct prime divisors of |Monster| = K+Q = 12+3")

chk("B05", 11, LAP_TOP - PHI6 + LAM,
    "Distinct prime divisors of |Baby Monster| = LAP_TOP-PHI6+LAM = 16-7+2")

# ════════════════════════════════════════════════════════════════════════════
# §2  Moonshine primes  (p such that (p+1) | 2K = 24)
# ════════════════════════════════════════════════════════════════════════════

MOONSHINE_PRIMES = [2, 3, 5, 7, 11, 23]
TWO_K = 2 * K  # = 24

chk("B06", len(MOONSHINE_PRIMES), LAM * Q,
    "Number of moonshine primes = LAM*Q = 6")

chk("B07", TWO_K % (2 + 1), 0,
    "2K divisible by 2+1=3=Q  (moonshine prime 2)")

chk("B08", TWO_K % (3 + 1), 0,
    "2K divisible by 3+1=4=MU  (moonshine prime 3)")

chk("B09", TWO_K % (5 + 1), 0,
    "2K divisible by 5+1=6=LAM*Q  (moonshine prime 5)")

chk("B10", TWO_K % (7 + 1), 0,
    "2K divisible by 7+1=8=2*MU  (moonshine prime 7)")

chk("B11", TWO_K % (11 + 1), 0,
    "2K divisible by 11+1=12=K  (moonshine prime 11)")

chk("B12", TWO_K % (23 + 1), 0,
    "2K divisible by 23+1=24=2K  (moonshine prime 23)")

chk("B13", sum(MOONSHINE_PRIMES), M_LAM + LAM * K,
    "Sum of moonshine primes = M_LAM+LAM*K = 27+24 = 51")

# ════════════════════════════════════════════════════════════════════════════
# §3  Monster order prime factorisation
# ════════════════════════════════════════════════════════════════════════════

chk("B14", prime_exp(MONSTER_ORDER, 2), 2 * K + LAP_TOP + MU + LAM,
    "v₂(|M|) = 46 = 2K+LAP_TOP+MU+LAM = 24+16+4+2")

chk("B15", prime_exp(MONSTER_ORDER, 3), EDGES // K,
    "v₃(|M|) = 20 = EDGES/K = 240/12")

chk("B16", prime_exp(MONSTER_ORDER, 5), Q ** 2,
    "v₅(|M|) = 9 = Q² = 3²")

chk("B17", prime_exp(MONSTER_ORDER, 7), LAM * Q,
    "v₇(|M|) = 6 = LAM*Q = 2×3")

chk("B18", prime_exp(MONSTER_ORDER, 11), LAM,
    "v₁₁(|M|) = 2 = LAM")

chk("B19", prime_exp(MONSTER_ORDER, 13), Q,
    "v₁₃(|M|) = 3 = Q")

chk("B20", 29, M_LAM + LAM,
    "29 = M_LAM+LAM = 27+2  (Monster prime with exponent 1)")

chk("B21", 31, V - Q ** 2,
    "31 = V-Q² = 40-9  (Monster prime; also: 744 = 31×24 = j-function constant)")

chk("B22", 41, V + 1,
    "41 = V+1 = 40+1  (Monster prime with exponent 1)")

# ════════════════════════════════════════════════════════════════════════════
# §4  Top-3 Monster primes and dimension of smallest representation
# ════════════════════════════════════════════════════════════════════════════

P47 = V + MU + Q                    # = 40+4+3   = 47
P59 = V + PHI3 + PHI4 - MU         # = 40+13+10-4 = 59
P71 = V + PHI3 + LAP_TOP + LAM     # = 40+13+16+2 = 71

chk("B23", P47, 47,
    "47 = V+MU+Q = 40+4+3  (Monster & Baby Monster prime)")

chk("B24", P59, 59,
    "59 = V+PHI3+PHI4-MU = 40+13+10-4  (Monster prime)")

chk("B25", P71, 71,
    "71 = V+PHI3+LAP_TOP+LAM = 40+13+16+2  (Monster prime)")

DIM_SMALLEST = P47 * P59 * P71     # = 196 883

chk("B26", DIM_SMALLEST, 196883,
    "47×59×71 = 196883 = dim(smallest non-trivial Monster representation)")

chk("B27", 29 + 41 + 59 + 71, MU * (V + LAP_MID),
    "Sum of Monster-only primes = 200 = MU*(V+LAP_MID) = 4×50")

# ════════════════════════════════════════════════════════════════════════════
# §5  Baby Monster order
# ════════════════════════════════════════════════════════════════════════════

chk("B28", prime_exp(BABY_ORDER, 2), V + 1,
    "v₂(|B|) = 41 = V+1 = 40+1")

chk("B29", prime_exp(BABY_ORDER, 3), PHI3,
    "v₃(|B|) = 13 = PHI3")

chk("B30", prime_exp(BABY_ORDER, 5), LAM * Q,
    "v₅(|B|) = 6 = LAM*Q = 2×3")

chk("B31", prime_exp(BABY_ORDER, 7), LAM,
    "v₇(|B|) = 2 = LAM")

MONSTER_PRIMES = frozenset({2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71})
BABY_PRIMES    = frozenset({2, 3, 5, 7, 11, 13, 17, 19, 23, 31, 47})
UNIQUE_TO_M    = MONSTER_PRIMES - BABY_PRIMES   # = {29, 41, 59, 71}

chk("B32", len(UNIQUE_TO_M), MU,
    "Primes in |M| not in |B| = {29,41,59,71}: count = MU = 4")

# ════════════════════════════════════════════════════════════════════════════
# §6  Monstrous moonshine representations and j-function
# ════════════════════════════════════════════════════════════════════════════

# Leech kissing number (CCLXX)
KISSING = EDGES * Q ** 2 * PHI6 * PHI3     # = 196 560

# h(E₇) = K+MU+LAM = 18 (CCLXIX)
H_E7 = K + MU + LAM                         # = 18

DIM_V_NATURAL = KISSING + H_E7 ** 2         # = 196 560 + 324 = 196 884

chk("B33", DIM_V_NATURAL, 196884,
    "dim(V♮) = EDGES·Q²·Φ₆·Φ₃ + (K+MU+LAM)² = 196560+324")

chk("B34", DIM_V_NATURAL - DIM_SMALLEST, 1,
    "dim(V♮) − dim(min rep) = 196884 − 196883 = 1  (trivial rep gap)")

chk("B35", 744, (V - Q ** 2) * TWO_K,
    "j-function constant 744 = (V-Q²)·2K = 31×24")

chk("B36", 23, TWO_K - 1,
    "Largest moonshine prime 23 = 2K-1 = 24-1")

chk("B37", 194, LAM + K * LAP_TOP,
    "Monster conjugacy classes = 194 = LAM+K·LAP_TOP = 2+12×16")

chk("B38", sum(sorted(MONSTER_PRIMES)), LAM * M_LAM * PHI6,
    "Sum of all 15 Monster primes = 378 = LAM·M_LAM·PHI6 = 2×27×7")

# ════════════════════════════════════════════════════════════════════════════
# §7  String-theory dimensional cross-links
# ════════════════════════════════════════════════════════════════════════════

chk("B39", 26, 2 * K + 2,
    "Bosonic string critical dim = 26 = 2K+2  (same as sporadic-group count!)")

chk("B40", 10, PHI4,
    "Superstring critical dim = 10 = PHI4")

# ── Summary ───────────────────────────────────────────────────────────────────
n_pass  = sum(c["pass"] for c in checks)
n_total = len(checks)
print(f"\n{'='*60}")
print(f"CCLXXI Monster/Baby/Moonshine bridge: {n_pass}/{n_total} PASS")
print(f"{'='*60}")

# ── Write JSON ────────────────────────────────────────────────────────────────
result = {
    "part":           "CCLXXI",
    "title":          "Monster Group, Baby Monster & Monstrous Moonshine",
    "checks_passed":  n_pass,
    "checks_total":   n_total,
    "verified":       (n_pass == n_total),
    "bridge_checks":  checks,
}

out_path = Path(__file__).parent.parent / "PART_CCLXXI_monster_results.json"
out_path.write_text(json.dumps(result, indent=2))
print(f"JSON written → {out_path.name}")
