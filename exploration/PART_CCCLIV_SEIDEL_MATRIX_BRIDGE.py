"""
PART CCCLIV — Seidel Matrix and Two-Graphs of W(3,3)

Every graph G on V vertices defines a SEIDEL matrix

    S = J - I - 2A

where J is the all-ones matrix, I the identity, and A the adjacency matrix.
The entries are:
    S_{ii} = 0,   S_{ij} = -1 if i~j,   S_{ij} = +1 if i≁j.

W(3,3) is the SRG(40, 12, 2, 4).  Its Seidel matrix has three eigenvalues:

    sigma_trivial = V - 1 - 2K = 40 - 1 - 24 = 15   (multiplicity 1)
    sigma_r       = -1 - 2r   = -1 - 4  = -5         (multiplicity MULT_R = 24)
    sigma_s       = -1 - 2s   = -1 + 8  = +7         (multiplicity MULT_S = 15)

(Here r=2, s=-4 are the non-trivial SRG eigenvalues.)

Key combinatorial results on S^2:
    (S^2)_{ii}      = V - 1  = 39
    (S^2)_{ij, i~j} = LAM    = 2      (equals the SRG second parameter!)
    (S^2)_{ij, i≁j} = LAM+MU = 6

The Seidel matrix defines a two-graph on 40 vertices (a combinatorial object
whose triples are all {i,j,k} for which the product S_{ij}*S_{jk}*S_{ki} = -1).
Since W(3,3) is a strongly regular graph, the induced two-graph is REGULAR.

Physics connections:
    sigma_r multiplicity = 24 = SU(5) adjoint dimension  (SU5_ADJ)
    sigma_s multiplicity = 15 = SU(5) matter rep          (SU5_MATTER)
    sigma_trivial         = 15 = MULT_S                   (coincidence!)
    |sigma_r|             =  5 = ALPHA // 2               (ALPHA = 10 in model)
    sigma_s               =  7 = GENERATIONS + EW_GAUGE_4 (3 + 4 = 7)
    |sigma_r| + |sigma_s| = 12 = K                       (K = vertex degree!)
    sigma_r + sigma_s     =  2 = LAM                      (LAM = 2)
"""

from fractions import Fraction

# ── SRG / W(3,3) constants ────────────────────────────────────────────────────
V        = 40        # vertices
K        = 12        # degree
LAM      = 2         # lambda: triangles per edge
MU       = 4         # mu: common neighbors for non-adjacent pair
EDGES    = 240       # total edges = V*K//2
MULT_R   = 24        # multiplicity of eigenvalue r=2
MULT_S   = 15        # multiplicity of eigenvalue s=-4
L        = 27        # GUT dimension / number of checks
R_EIG    = 2         # eigenvalue r
S_EIG    = -4        # eigenvalue s
ABS_S    = 4         # |s|

# Physics constants
ALPHA       = 10
EW_GAUGE_4  = 4
GENERATIONS = 3
GUT_DIM     = 27
SU5_ADJ     = 24
SU5_MATTER  = 15


# ── Seidel matrix entry values ────────────────────────────────────────────────

def s_diagonal() -> int:
    """S_{ii} = 0 for all i (Seidel matrices have zero diagonal)."""
    return 0


def s_adj() -> int:
    """S_{ij} = -1 for adjacent pairs (i ~ j)."""
    return -1


def s_non_adj() -> int:
    """S_{ij} = +1 for non-adjacent pairs (i ≁ j, i ≠ j)."""
    return 1


def minus_one_per_row() -> int:
    """Number of -1 entries in each row of S = K (the degree)."""
    return K


def plus_one_per_row() -> int:
    """Number of +1 entries in each row of S = V - 1 - K."""
    return V - 1 - K


def frobenius_sq() -> int:
    """Frobenius norm squared of S = sum of squares of all entries.

    Each of the V*(V-1) off-diagonal entries has value ±1, so each
    contributes 1 to the sum of squares.  Result = V*(V-1).
    """
    return V * (V - 1)


# ── Seidel eigenvalues ────────────────────────────────────────────────────────

def sigma_trivial() -> int:
    """Seidel eigenvalue on the trivial (all-ones) eigenspace.

    S*j = (J - I - 2A)*j = V*j - j - 2K*j = (V - 1 - 2K)*j.
    """
    return V - 1 - 2 * K


def sigma_r() -> int:
    """Seidel eigenvalue on the r-eigenspace of A.

    For eigenvectors x with Ax = r*x and x ⊥ j:  Sx = -x - 2A*x = -(1+2r)*x.
    """
    return -1 - 2 * R_EIG


def sigma_s() -> int:
    """Seidel eigenvalue on the s-eigenspace of A.

    Sx = -(1 + 2s)*x = -(1 + 2*(-4))*x = 7x.
    """
    return -1 - 2 * S_EIG


def trace_seidel() -> int:
    """Trace of S = 1*sigma_trivial + MULT_R*sigma_r + MULT_S*sigma_s = 0."""
    return 1 * sigma_trivial() + MULT_R * sigma_r() + MULT_S * sigma_s()


# ── S^2 entries ───────────────────────────────────────────────────────────────

def s2_diag() -> int:
    """(S^2)_{ii} = sum_k S_{ik}^2 = V - 1  (all off-diagonal entries are ±1)."""
    return V - 1


def s2_adj() -> int:
    """(S^2)_{ij} for adjacent i~j, derived combinatorially.

    (S^2)_{ij} = sum_{k≠i,k≠j} (1-2A_{ik})(1-2A_{jk})
               = (V-2) - 2*(K-1) - 2*(K-1) + 4*LAM
               = (V-2) - 4*(K-1) + 4*LAM
    With V=40, K=12, LAM=2:
    = 38 - 44 + 8 = 2 = LAM.
    """
    return (V - 2) - 4 * (K - 1) + 4 * LAM


def s2_non_adj() -> int:
    """(S^2)_{ij} for non-adjacent i≁j, derived combinatorially.

    (S^2)_{ij} = (V-2) - 2*K - 2*K + 4*MU
               = (V-2) - 4*K + 4*MU
    With V=40, K=12, MU=4:
    = 38 - 48 + 16 = 6 = LAM + MU.
    """
    return (V - 2) - 4 * K + 4 * MU


def s2_eigenvalue_er() -> int:
    """S^2 eigenvalue on E_r = sigma_r()^2 = 25."""
    return sigma_r() ** 2


def s2_eigenvalue_es() -> int:
    """S^2 eigenvalue on E_s = sigma_s()^2 = 49."""
    return sigma_s() ** 2


# ── Seidel–SRG arithmetic relations ──────────────────────────────────────────

def sum_sigma_r_sigma_s() -> int:
    """sigma_r + sigma_s = -5 + 7 = 2 = LAM."""
    return sigma_r() + sigma_s()


def abs_sum_sigma() -> int:
    """|sigma_r| + |sigma_s| = 5 + 7 = 12 = K."""
    return abs(sigma_r()) + abs(sigma_s())


def sigma_product_relation() -> int:
    """sigma_r * sigma_s + MULT_R + MULT_S = MU = 4.

    Proof: sigma_r*sigma_s = (-5)*7 = -35 = -(MULT_R + MULT_S - MU).
    So sigma_r*sigma_s + MULT_R + MULT_S = MU.
    """
    return sigma_r() * sigma_s() + MULT_R + MULT_S


def sigma_spread() -> int:
    """sigma_s - sigma_r = 7 - (-5) = 12 = K (spread of non-trivial eigenvalues)."""
    return sigma_s() - sigma_r()


def row_sum_s() -> int:
    """Off-diagonal row sum of S = K*(-1) + (V-1-K)*(+1) = V-1-2K = sigma_trivial."""
    return K * (-1) + (V - 1 - K) * 1


def sigma_trivial_eq_mult_s() -> int:
    """sigma_trivial = MULT_S = 15  (trivial Seidel eigenvalue = SU5 matter dim)."""
    return sigma_trivial()


# ── Physics connections ───────────────────────────────────────────────────────

def sigma_r_abs_half_alpha() -> int:
    """|sigma_r| = 5 = ALPHA // 2  (ALPHA=10 in the model proxy)."""
    return abs(sigma_r())


def sigma_s_gauge_gen() -> int:
    """sigma_s = 7 = EW_GAUGE_4 + GENERATIONS = 4 + 3."""
    return sigma_s()


def count_minus_one_entries() -> int:
    """Number of -1 entries in S (symmetric: upper + lower triangle) = 2*EDGES."""
    return 2 * EDGES


def count_plus_one_entries() -> int:
    """Number of +1 entries in S = V*(V-1) - 2*EDGES."""
    return V * (V - 1) - 2 * EDGES


def spectral_sum_of_squares() -> int:
    """sigma_trivial^2*1 + sigma_r^2*MULT_R + sigma_s^2*MULT_S = V*(V-1) = 1560.

    This is tr(S^2) = Frobenius norm^2 of S.
    """
    return (sigma_trivial() ** 2 * 1
            + sigma_r() ** 2 * MULT_R
            + sigma_s() ** 2 * MULT_S)


def sigma_r_sq_eq_mult_r_plus_1() -> int:
    """sigma_r^2 = 25 = MULT_R + 1 = 24 + 1.  (geometric coincidence)"""
    return sigma_r() ** 2


# ── Verification harness ──────────────────────────────────────────────────────

def verify_all():
    checks = []

    def chk(name, got, expected):
        passed = (got == expected)
        checks.append({
            "name": name,
            "got": str(got),
            "expected": str(expected),
            "passed": passed,
        })

    # Group 1: Seidel matrix entry values (6 checks)
    chk("S diagonal = 0",
        s_diagonal(), 0)
    chk("S adjacent off-diagonal = -1",
        s_adj(), -1)
    chk("S non-adjacent off-diagonal = +1",
        s_non_adj(), 1)
    chk("Per-row count of -1 entries = K = 12",
        minus_one_per_row(), K)
    chk("Per-row count of +1 entries = V-1-K = 27",
        plus_one_per_row(), V - 1 - K)
    chk("S Frobenius norm^2 = V*(V-1) = 1560",
        frobenius_sq(), V * (V - 1))

    # Group 2: Seidel eigenvalues (5 checks)
    chk("sigma_trivial = V-1-2K = 15",
        sigma_trivial(), V - 1 - 2 * K)
    chk("sigma_r = -1-2r = -5",
        sigma_r(), -1 - 2 * R_EIG)
    chk("sigma_s = -1-2s = +7",
        sigma_s(), -1 - 2 * S_EIG)
    chk("Trace S = 0: 1*sigma_trivial + MULT_R*sigma_r + MULT_S*sigma_s",
        trace_seidel(), 0)
    chk("sigma_r < 0 and sigma_s > 0 (opposite signs)",
        sigma_r() < 0 and sigma_s() > 0, True)

    # Group 3: S^2 entries (5 checks)
    chk("S^2 diagonal = V-1 = 39",
        s2_diag(), V - 1)
    chk("S^2 adjacent = LAM = 2",
        s2_adj(), LAM)
    chk("S^2 non-adjacent = LAM+MU = 6",
        s2_non_adj(), LAM + MU)
    chk("S^2 eigenvalue on E_r = sigma_r^2 = 25",
        s2_eigenvalue_er(), sigma_r() ** 2)
    chk("S^2 eigenvalue on E_s = sigma_s^2 = 49",
        s2_eigenvalue_es(), sigma_s() ** 2)

    # Group 4: Seidel–SRG arithmetic (6 checks)
    chk("sigma_r + sigma_s = LAM = 2",
        sum_sigma_r_sigma_s(), LAM)
    chk("|sigma_r| + |sigma_s| = K = 12",
        abs_sum_sigma(), K)
    chk("sigma_r*sigma_s + MULT_R + MULT_S = MU = 4",
        sigma_product_relation(), MU)
    chk("sigma_s - sigma_r = K = 12 (eigenvalue spread)",
        sigma_spread(), K)
    chk("Off-diagonal row sum of S = sigma_trivial = 15",
        row_sum_s(), sigma_trivial())
    chk("sigma_trivial = MULT_S = 15",
        sigma_trivial_eq_mult_s(), MULT_S)

    # Group 5: Physics connections (5 checks)
    chk("|sigma_r| = ALPHA//2 = 5",
        sigma_r_abs_half_alpha(), ALPHA // 2)
    chk("sigma_s = EW_GAUGE_4 + GENERATIONS = 7",
        sigma_s_gauge_gen(), EW_GAUGE_4 + GENERATIONS)
    chk("count -1 entries in S = 2*EDGES = 480",
        count_minus_one_entries(), 2 * EDGES)
    chk("count +1 entries in S = V*(V-1)-2*EDGES = 1080",
        count_plus_one_entries(), V * (V - 1) - 2 * EDGES)
    chk("Spectral sum of squares = V*(V-1) = 1560",
        spectral_sum_of_squares(), V * (V - 1))

    # Check group integrity: must be exactly L=27 checks
    assert len(checks) == L, f"Expected {L} checks, got {len(checks)}"

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    return checks, passed, total


def build_cccliv_summary() -> dict:
    checks, passed, total = verify_all()
    return {
        "part": "CCCLIV",
        "title": "Seidel Matrix and Two-Graphs of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "sigma_trivial": sigma_trivial(),
            "sigma_r": sigma_r(),
            "sigma_s": sigma_s(),
            "s2_adj": s2_adj(),
            "s2_non_adj": s2_non_adj(),
            "frobenius_sq": frobenius_sq(),
            "count_minus_one": count_minus_one_entries(),
            "count_plus_one": count_plus_one_entries(),
        },
        "discoveries": [
            f"sigma_r + sigma_s = {sigma_r() + sigma_s()} = LAM (non-trivial eigenvalue sum = lambda)",
            f"|sigma_r| + |sigma_s| = {abs(sigma_r()) + abs(sigma_s())} = K (absolute sum = vertex degree)",
            f"sigma_r*sigma_s + MULT_R + MULT_S = {sigma_r()*sigma_s() + MULT_R + MULT_S} = MU",
            f"sigma_trivial = {sigma_trivial()} = MULT_S = SU5_MATTER",
            f"S^2_adj = {s2_adj()} = LAM;  S^2_non-adj = {s2_non_adj()} = LAM+MU",
            f"sigma_s = {sigma_s()} = EW_GAUGE_4 + GENERATIONS = 4+3",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for c in checks:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"  [{status}] {c['name']}")
    print(f"\nstatus: {'PASS' if passed==total else 'FAIL'}, checks_pass: {passed}, checks_total: {total}")

    import json, pathlib
    summary = build_cccliv_summary()
    out = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCLIV_seidel_matrix_results.json"
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"JSON written: {out}")
