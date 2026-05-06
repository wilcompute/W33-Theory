"""
PART CCCXLV -- Krein Coupling Constants: Dual Algebra Structure of W(3,3)
=========================================================================
The Bose-Mesner algebra of W(3,3) is closed under both ordinary matrix
multiplication (intersection-number structure) AND the entry-wise (Hadamard)
product.  In the idempotent basis {E_0, E_1, E_2} the Hadamard structure
constants are the Krein parameters:

    E_i o E_j  =  (1/V) * sum_l  q[i][j][l]  E_l

We compute all 27 entries of the Krein tensor q[i][j][l] exactly as
Fractions via the dual linear system, verify the Krein condition (all >= 0),
and show how the non-trivial parameters encode W(3,3) / SU(5) physics.

Key exact identities:
  q[1][1][0] = MULT_R = 24 = SU5_ADJ        (R-sector self-coupling)
  q[2][2][0] = MULT_S = 15 = SU5_MATTER     (S-sector self-coupling)
  q[1][2][0] = 0                             (no trivial output from gauge x matter)
  q[2][2][1] / q[2][2][2] = |s| / r = 2     (eigenvalue ratio in dual algebra)
  q[1][1][1] + q[1][1][2] = V - K = 28      (gauge self-coupling sector sum)
  q[2][2][1] + q[2][2][2] = K - r = 10      (matter self-coupling sector sum)
  q[1][2][1] + q[1][2][2] = (V - r) / 2     (cross-coupling sector sum)
"""

from fractions import Fraction
import json
from pathlib import Path

# ── W(3,3) SRG constants ─────────────────────────────────────────────────────
V      = 40
K      = 12
LAM    = 2
MU     = 4
R_EIG  = 2
S_EIG  = -4
ABS_S  = 4
MULT_R = 24
MULT_S = 15
L      = V - K - 1       # = 27, valency of complement relation A_2

# SU(5) GUT constants (from CCCXLIV)
SU5_DIM            = 5
SU5_ADJ            = SU5_DIM ** 2 - 1   # 24
SU5_MATTER_PER_GEN = 15
GENERATIONS        = 3
GUT_DIM            = 27
EW_GAUGE_4         = 4
ALPHA              = 10

# ── Association-scheme data ───────────────────────────────────────────────────
# M_MULT[j] = multiplicity of j-th idempotent
M_MULT = [Fraction(1), Fraction(MULT_R), Fraction(MULT_S)]

# P_MAT[s][j] = eigenvalue of relation A_s on eigenspace of E_j
#   s=0: A_0 = I (identity)
#   s=1: A_1 = A (adjacency matrix of W(3,3))
#   s=2: A_2 = J - I - A (complement / non-adjacency)
#   j=0: trivial eigenspace (eigenvalue k of A)
#   j=1: R-sector    (eigenvalue r=2 of A)
#   j=2: S-sector    (eigenvalue s=-4 of A)
P_MAT = [
    [Fraction(1),       Fraction(1),         Fraction(1)        ],   # A_0 = I
    [Fraction(K),       Fraction(R_EIG),      Fraction(S_EIG)    ],   # A_1 = A
    [Fraction(L),       Fraction(-R_EIG - 1), Fraction(-S_EIG - 1)],  # A_2 = J-I-A
]

# Valencies: k_s = number of pairs in relation s at each vertex
K_VAL = [Fraction(1), Fraction(K), Fraction(L)]

# ── 3x3 exact matrix inverse (Fraction arithmetic) ───────────────────────────
def _inv3(mat):
    """Return exact inverse of a 3x3 matrix over Fractions."""
    a = [[Fraction(mat[i][j]) for j in range(3)] for i in range(3)]

    def cof(r, c):
        rs = [i for i in range(3) if i != r]
        cs = [j for j in range(3) if j != c]
        return ((-1) ** (r + c)) * (
            a[rs[0]][cs[0]] * a[rs[1]][cs[1]]
            - a[rs[0]][cs[1]] * a[rs[1]][cs[0]]
        )

    cofs = [[cof(i, j) for j in range(3)] for i in range(3)]
    det = sum(a[0][j] * cofs[0][j] for j in range(3))
    # adjugate is transpose of cofactor matrix
    return [[cofs[j][i] / det for j in range(3)] for i in range(3)]


def _mv(mat, vec):
    """Multiply 3x3 matrix by 3-vector over Fractions."""
    return [sum(mat[i][j] * vec[j] for j in range(3)) for i in range(3)]


# ── Krein parameter computation ───────────────────────────────────────────────
def compute_krein():
    """Return q[i][j][l] for 0 <= i,j,l <= 2 as exact Fractions.

    The Krein parameters satisfy the linear system
        sum_l q[i][j][l] * M_MULT[l] * P_MAT[s][l] = M_MULT[i]*M_MULT[j]*P_MAT[s][i]*P_MAT[s][j] / K_VAL[s]
    for each s in {0,1,2}, derived by equating entries of E_i o E_j in the
    three relation classes (diagonal, adjacent, non-adjacent).
    """
    # System matrix: Msys[s][l] = M_MULT[l] * P_MAT[s][l]
    Msys = [[M_MULT[l] * P_MAT[s][l] for l in range(3)] for s in range(3)]
    Minv = _inv3(Msys)

    q = [[[Fraction(0)] * 3 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(i, 3):
            b = [
                M_MULT[i] * M_MULT[j] * P_MAT[s][i] * P_MAT[s][j] / K_VAL[s]
                for s in range(3)
            ]
            sol = _mv(Minv, b)
            for l in range(3):
                q[i][j][l] = sol[l]
                q[j][i][l] = sol[l]   # symmetry q[i][j] = q[j][i]
    return q


# Module-level Krein tensor (computed once)
_Q = compute_krein()


def krein(i, j, l):
    """Return exact Fraction Krein parameter q[i][j][l]."""
    return _Q[i][j][l]


# ── Verification: 27 checks in 5 groups ──────────────────────────────────────
def verify_all():
    checks = []

    def chk(name, val, exp):
        checks.append({
            "name": name,
            "passed": bool(val == exp),
            "got": str(val),
            "expected": str(exp),
        })

    # -- Group 1: E_0 coupling (identity sector acts as identity, 5 checks) --
    # E_0 = J/V; E_0 o E_j = (1/V) E_j, so q[0][j][l] = delta_{jl}
    chk("q[0][0][0] = 1 (E_0 trivial identity)",
        krein(0, 0, 0), Fraction(1))
    chk("q[0][1][1] = 1 (E_0 passes R-sector through)",
        krein(0, 1, 1), Fraction(1))
    chk("q[0][2][2] = 1 (E_0 passes S-sector through)",
        krein(0, 2, 2), Fraction(1))
    chk("q[0][1][0] = 0 (E_0 x E_1 has no trivial output)",
        krein(0, 1, 0), Fraction(0))
    chk("q[0][2][0] = 0 (E_0 x E_2 has no trivial output)",
        krein(0, 2, 0), Fraction(0))

    # -- Group 2: Trivial-output self-couplings (6 checks) --
    chk("q[1][1][0] = MULT_R = 24",
        krein(1, 1, 0), Fraction(MULT_R))
    chk("q[2][2][0] = MULT_S = 15",
        krein(2, 2, 0), Fraction(MULT_S))
    chk("q[1][2][0] = 0 (gauge x matter: no trivial output)",
        krein(1, 2, 0), Fraction(0))
    chk("q[1][1][0] + q[2][2][0] = V - 1",
        krein(1, 1, 0) + krein(2, 2, 0), Fraction(V - 1))
    chk("q[1][1][0] = SU5_ADJ (gauge self-coupling = SU(5) adjoint dim)",
        krein(1, 1, 0), Fraction(SU5_ADJ))
    chk("q[2][2][0] = SU5_MATTER (matter self-coupling = SU(5) matter/gen)",
        krein(2, 2, 0), Fraction(SU5_MATTER_PER_GEN))

    # -- Group 3: Exact rational Krein values for non-trivial sectors (6 checks) --
    chk("q[1][1][1] = 44/3",
        krein(1, 1, 1), Fraction(44, 3))
    chk("q[1][1][2] = 40/3",
        krein(1, 1, 2), Fraction(40, 3))
    chk("q[1][2][1] = 25/3",
        krein(1, 2, 1), Fraction(25, 3))
    chk("q[1][2][2] = 32/3",
        krein(1, 2, 2), Fraction(32, 3))
    chk("q[2][2][1] = 20/3",
        krein(2, 2, 1), Fraction(20, 3))
    chk("q[2][2][2] = 10/3",
        krein(2, 2, 2), Fraction(10, 3))

    # -- Group 4: Krein condition, symmetry, and sum rules (5 checks) --
    all_nonneg = all(
        krein(i, j, l) >= 0
        for i in range(3) for j in range(3) for l in range(3)
    )
    checks.append({
        "name": "Krein condition: all q[i][j][l] >= 0",
        "passed": bool(all_nonneg),
        "got": str(all_nonneg),
        "expected": "True",
    })

    sym_ok = all(
        krein(i, j, l) == krein(j, i, l)
        for i in range(3) for j in range(3) for l in range(3)
    )
    checks.append({
        "name": "Krein symmetry: q[i][j][l] = q[j][i][l]",
        "passed": bool(sym_ok),
        "got": str(sym_ok),
        "expected": "True",
    })

    s11 = sum(krein(1, 1, l) * M_MULT[l] for l in range(3))
    chk("sum_l q[1][1][l]*m_l = m_1^2 = 576",
        s11, Fraction(MULT_R ** 2))
    s12 = sum(krein(1, 2, l) * M_MULT[l] for l in range(3))
    chk("sum_l q[1][2][l]*m_l = m_1*m_2 = 360",
        s12, Fraction(MULT_R * MULT_S))
    s22 = sum(krein(2, 2, l) * M_MULT[l] for l in range(3))
    chk("sum_l q[2][2][l]*m_l = m_2^2 = 225",
        s22, Fraction(MULT_S ** 2))

    # -- Group 5: Physical ratio identities (5 checks) --
    chk("q[2][2][1] / q[2][2][2] = ABS_S / R_EIG = 2",
        krein(2, 2, 1) / krein(2, 2, 2), Fraction(ABS_S, R_EIG))
    chk("q[1][1][1] + q[1][1][2] = V - K = 28",
        krein(1, 1, 1) + krein(1, 1, 2), Fraction(V - K))
    chk("q[2][2][1] + q[2][2][2] = K - R_EIG = 10",
        krein(2, 2, 1) + krein(2, 2, 2), Fraction(K - R_EIG))
    chk("q[1][2][1] + q[1][2][2] = (V - R_EIG) / 2 = 19",
        krein(1, 2, 1) + krein(1, 2, 2), Fraction(V - R_EIG, 2))
    chk("q[1][1][2] / q[2][2][2] = V / (K - R_EIG) = 4",
        krein(1, 1, 2) / krein(2, 2, 2), Fraction(V, K - R_EIG))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    return checks, passed, total


# ── Summary and JSON output ───────────────────────────────────────────────────
def build_cccxlv_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCXLV",
        "title": "Krein Coupling Constants: Dual Algebra Structure of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V, "K": K, "MULT_R": MULT_R, "MULT_S": MULT_S,
            "L": L,
            "q_11_0": str(krein(1, 1, 0)),
            "q_11_1": str(krein(1, 1, 1)),
            "q_11_2": str(krein(1, 1, 2)),
            "q_12_0": str(krein(1, 2, 0)),
            "q_12_1": str(krein(1, 2, 1)),
            "q_12_2": str(krein(1, 2, 2)),
            "q_22_0": str(krein(2, 2, 0)),
            "q_22_1": str(krein(2, 2, 1)),
            "q_22_2": str(krein(2, 2, 2)),
            "krein_ratio_22": str(krein(2, 2, 1) / krein(2, 2, 2)),
            "gauge_sector_sum": str(krein(1, 1, 1) + krein(1, 1, 2)),
            "matter_sector_sum": str(krein(2, 2, 1) + krein(2, 2, 2)),
            "cross_sector_sum": str(krein(1, 2, 1) + krein(1, 2, 2)),
        },
        "discoveries": [
            "q[1][1][0] = MULT_R = SU5_ADJ = 24: R-sector self-coupling saturates at the SU(5) adjoint dimension",
            "q[2][2][0] = MULT_S = SU5_MATTER = 15: S-sector self-coupling saturates at the SU(5) matter dimension",
            "q[1][2][0] = 0: gauge x matter Hadamard product has no trivial (scalar) output -- charge neutrality",
            "q[2][2][1] / q[2][2][2] = ABS_S / R_EIG = 2: the SRG eigenvalue ratio appears in the dual algebra",
            "q[1][1][1]+q[1][1][2] = V-K and q[2][2][1]+q[2][2][2] = K-R_EIG: sector sums equal graph degree gaps",
            "q[1][2][1]+q[1][2][2] = (V-R_EIG)/2: cross-sector sum is the arithmetic mean of the sector sums",
            "q[1][1][2]/q[2][2][2] = V/(K-R_EIG) = 4: ratio of gauge/matter non-trivial outputs = ABS_S^2/R_EIG^2",
        ],
    }


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    checks, passed, total = verify_all()
    print(f"\nPart CCCXLV: Krein Coupling Constants: Dual Algebra Structure of W(3,3)")
    print(f"status: {'PASS' if passed == total else 'FAIL'}, "
          f"checks_pass: {passed}, checks_total: {total}")

    for c in checks:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"  [{status}] {c['name']}")

    summary = build_cccxlv_summary()
    out_path = Path(__file__).resolve().parents[1] / "PART_CCCXLV_krein_coupling_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nJSON written: {out_path}")
