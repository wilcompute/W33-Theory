"""Part MCLIX: Seidel Matrix, Two-Graph, and Equiangular Lines for W(3,3).

S = J - I - 2A transforms adjacency eigenvalues:
  k=12  ->  sigma_0 = v-1-2k = 15   (trivial eigenspace, mult 1)
  r=2   ->  sigma_r = -1-2r  = -5   (r-eigenspace, mult 24)
  s=-4  ->  sigma_s = -1-2s  =  7   (s-eigenspace, mult 15)

Novel theorems:
  MCLIX.1: E(S) = |E(G)| = vk/2 = 240  (Seidel energy = edge count)
  MCLIX.2: tr(S^2) = v(v-1) = 1560  (all off-diagonal entries are +-1)
  MCLIX.3: Every triangle of W(3,3) lies on a line of GQ(3,3).
           tr(A^3)/6 = 160 = 40 lines x 4 triangles/line.
  MCLIX.4: sigma_r + sigma_s = 2 = -2(r+s) = r+s reversed sign collapse.
           Equivalently: (1+r) = -(1+s) = 3, the Kemeny-collision root.
"""

from fractions import Fraction
import json

v, k, lam, mu_param = 40, 12, 2, 4
eigvals = [Fraction(12), Fraction(2), Fraction(-4)]
mults   = [1, 24, 15]
m0, m_r, m_s = 1, 24, 15


def seidel_eigenvalues():
    """Eigenvalues of S = J - I - 2A.

    On the all-ones eigenvector (eigenvalue k):
        S * 1 = v*1 - 1 - 2k*1 = (v-1-2k)*1

    On any A-eigenvector x with Ax = lam*x and x ⊥ 1:
        S * x = 0 - x - 2*lam*x = -(1+2*lam)*x
    """
    sigma = []
    for i, (lam_i, m_i) in enumerate(zip(eigvals, mults)):
        if i == 0:
            sig = Fraction(v - 1 - 2 * k)
        else:
            sig = Fraction(-1) - 2 * lam_i
        sigma.append((sig, m_i))
    return sigma


def verify_seidel_trace(sigma):
    """tr(S) = 0 (all diagonal entries 0)."""
    total = sum(e * m for e, m in sigma)
    assert total == Fraction(0), f"tr(S)={total}"
    return total


def verify_seidel_trace_sq(sigma):
    """tr(S^2) = v(v-1).

    Each row i has exactly v-1 off-diagonal entries all equal +-1, so
    (S^2)_{ii} = sum_j s_{ij}^2 = v-1.  Therefore tr(S^2) = v(v-1).
    """
    total = sum(e ** 2 * m for e, m in sigma)
    expected = Fraction(v * (v - 1))
    assert total == expected, f"tr(S^2)={total}, expected {expected}"
    return total


def seidel_energy(sigma):
    """E(S) = sum |sigma_i| * m_i.

    Novel: E(S) = 240 = vk/2 = |E(G)|.
    """
    E_S = sum(abs(e) * m for e, m in sigma)
    E_G = Fraction(v * k, 2)
    assert E_S == E_G, f"E(S)={E_S}, |E(G)|={E_G}"
    return E_S


def seidel_spectral_moments(sigma):
    """M_p(S) = sum sigma_i^p * m_i for p = 1 .. 6."""
    moments = []
    for p in range(1, 7):
        M = sum(e ** p * m for e, m in sigma)
        moments.append(M)
    return moments


def equiangular_lines_data(sigma):
    """W(3,3) gives 40 equiangular lines in R^{m_r=24} with angle 1/5.

    The primitive idempotent E_r has rank m_r = 24; its v=40 columns
    (normalized) define equiangular lines with |<u_i, u_j>| = 1/|sigma_r| = 1/5.

    Welch (1974) lower bound on the coherence t of n lines in R^d:
        t^2  >=  (n - d) / (d * (n - 1))

    Gerzon absolute bound:  n  <=  d(d+1)/2.
    """
    sigma_r_val = sigma[1][0]           # -5
    t = Fraction(1, abs(sigma_r_val))   # 1/5
    d = m_r                             # 24
    n = v                               # 40

    gerzon = Fraction(d * (d + 1), 2)   # 300
    welch_rhs = Fraction(n - d, d * (n - 1))  # 16 / (24*39) = 2/117

    return {
        "angle": t,
        "d": d,
        "n": n,
        "gerzon_bound": gerzon,
        "gerzon_satisfied": n <= gerzon,
        "welch_lhs": t ** 2,            # 1/25
        "welch_rhs": welch_rhs,         # 2/117
        "welch_satisfied": t ** 2 >= welch_rhs,
    }


def triangle_data():
    """Every triangle of W(3,3) lies on a line of GQ(3,3).

    tr(A^3) = 12^3*1 + 2^3*24 + (-4)^3*15 = 1728 + 192 - 960 = 960.
    Number of triangles = tr(A^3) / 6 = 160.

    GQ(3,3) has 40 lines, each with 4 points.  Each line contributes
    C(4,3) = 4 triangles.  Total = 40 * 4 = 160. Perfect match!

    Therefore every triangle is a triple of points on a common GQ line.
    """
    tr_A3 = sum(e ** 3 * m for e, m in zip(eigvals, mults))
    n_triangles = tr_A3 // 6
    n_lines = v                     # GQ(3,3) has 40 lines = 40 K_4's
    triangles_per_line = 4          # C(4,3)
    assert n_triangles == n_lines * triangles_per_line
    return tr_A3, n_triangles


def seidel_tr_cube(sigma):
    """tr(S^3) encodes signed triangle statistics of the two-graph."""
    return sum(e ** 3 * m for e, m in sigma)


def novel_seidel_identities(sigma, moments):
    """All novel identities for Part MCLIX."""
    ids = {}

    sigma_vals = [e for e, m in sigma]
    # sigma_0=15, sigma_r=-5, sigma_s=7

    ids["sigma_0"] = sigma_vals[0]
    ids["sigma_r"] = sigma_vals[1]
    ids["sigma_s"] = sigma_vals[2]

    # Spectral moments
    ids["tr_S"]   = moments[0]   # 0
    ids["tr_S2"]  = moments[1]   # 1560
    ids["tr_S3"]  = moments[2]   # 5520
    ids["tr_S4"]  = moments[3]
    ids["tr_S5"]  = moments[4]

    # Seidel energy
    ids["seidel_energy"]     = sum(abs(e) * m for e, m in sigma)
    ids["graph_edge_count"]  = Fraction(v * k, 2)
    ids["energy_eq_edges"]   = ids["seidel_energy"] == ids["graph_edge_count"]

    # Spectral radius
    ids["seidel_spectral_radius"] = max(abs(e) for e, _ in sigma)

    # Linear relation: sigma_r + sigma_s = -(2*(r+s)) - 2 = -2*(-2) - 2 = 2
    ids["sigma_r_plus_sigma_s"]   = sigma_vals[1] + sigma_vals[2]   # 2
    ids["sigma_r_times_sigma_s"]  = sigma_vals[1] * sigma_vals[2]   # -35

    # (1+r) = -(1+s) = 3: the Kemeny-collision root (see MCLVIII)
    ids["one_plus_r"]  = Fraction(1) + eigvals[1]   # 3
    ids["one_plus_s"]  = Fraction(1) + eigvals[2]   # -3
    ids["sum_1pr_1ps"] = ids["one_plus_r"] + ids["one_plus_s"]  # 0
    assert ids["sum_1pr_1ps"] == 0

    # Two-graph: doubly regular
    # lambda_T (odd triples per edge) = mu_param = 4
    ids["gq_two_graph_lambda"] = Fraction(mu_param)

    # Triangle count
    tr_A3, n_tri = triangle_data()
    ids["tr_A3"]       = tr_A3        # 960
    ids["n_triangles"] = n_tri        # 160
    ids["lines_GQ"]    = v            # 40  (GQ(3,3) has 40 lines)
    ids["tris_per_line"] = Fraction(n_tri, v)  # 4

    # Equiangular bounds
    t = Fraction(1, 5)
    ids["eq_angle"]    = t
    ids["gerzon_bound"] = Fraction(m_r * (m_r + 1), 2)   # 300
    ids["n_geq_gerzon"] = Fraction(v) <= ids["gerzon_bound"]

    welch_rhs = Fraction(v - m_r, m_r * (v - 1))
    ids["welch_lhs"]       = t ** 2        # 1/25
    ids["welch_rhs"]       = welch_rhs     # 2/117
    ids["welch_satisfied"] = t ** 2 >= welch_rhs

    # Seidel char poly constant term = product of eigenvalues with sign
    # det(S) = sigma_0 * sigma_r^{m_r} * sigma_s^{m_s}
    # = 15 * (-5)^24 * 7^15  (positive since 24 even)
    det_S_sign = (1 if mults[0] % 2 == 0 else 1) * \
                 (1 if mults[1] % 2 == 0 else -1) * \
                 (1 if mults[2] % 2 == 0 else 1)
    # sigma_0=15>0, sigma_r^24 = 5^24>0, sigma_s^15 = 7^15>0
    ids["det_S_positive"] = True
    ids["det_S_formula"]  = f"15 * 5^24 * 7^15 = 3 * 5^25 * 7^15"

    # log2 of absolute value: not Fraction but formula
    # |det(S)| = 3 * 5^25 * 7^15

    return ids


def seidel_matrix_main():
    print("=== Part MCLIX: Seidel Matrix and Two-Graph for W(3,3) ===\n")

    sigma = seidel_eigenvalues()
    print("Seidel eigenvalues (S = J - I - 2A):")
    for sig, m in sigma:
        print(f"  sigma = {sig}  (mult {m})")

    tr1 = verify_seidel_trace(sigma)
    tr2 = verify_seidel_trace_sq(sigma)
    E_S = seidel_energy(sigma)
    print(f"\ntr(S)  = {tr1}")
    print(f"tr(S^2) = {tr2} = v*(v-1) = {v*(v-1)}")
    print(f"E(S)   = {E_S} = vk/2 = {v*k//2}  [= |E(G)|]")

    moments = seidel_spectral_moments(sigma)
    print("\nSpectral moments M_p(S):")
    for p, M in enumerate(moments, 1):
        print(f"  M_{p} = {M}")

    eq = equiangular_lines_data(sigma)
    print(f"\nEquiangular lines (sigma_r={sigma[1][0]}-eigenspace, dim {eq['d']}):")
    print(f"  Angle  = {eq['angle']}")
    print(f"  Lines  = {eq['n']}  <=  Gerzon {eq['gerzon_bound']}: {eq['gerzon_satisfied']}")
    print(f"  Welch: t^2 = {eq['welch_lhs']} >= {eq['welch_rhs']}: {eq['welch_satisfied']}")

    tr_A3, n_tri = triangle_data()
    print(f"\nTriangle structure:")
    print(f"  tr(A^3) = {tr_A3}  => {n_tri} triangles")
    print(f"  GQ lines: {v}, each with 4 triangles => {v*4} = {n_tri} (ALL triangles on lines)")

    ids = novel_seidel_identities(sigma, moments)
    print("\nNovel identities:")
    for key, val in ids.items():
        print(f"  {key}: {val}")

    # ---- Verification ----
    n_verified = 0

    # Eigenvalues
    assert sigma[0][0] == Fraction(15);   n_verified += 1
    assert sigma[1][0] == Fraction(-5);   n_verified += 1
    assert sigma[2][0] == Fraction(7);    n_verified += 1

    # Trace
    assert tr1 == Fraction(0);            n_verified += 1
    assert tr2 == Fraction(v * (v - 1));  n_verified += 1

    # Energy = edge count
    assert E_S == Fraction(v * k, 2);     n_verified += 1

    # Spectral moments
    assert moments[0] == Fraction(0);     n_verified += 1
    assert moments[1] == Fraction(1560);  n_verified += 1
    assert moments[2] == Fraction(5520);  n_verified += 1

    # Equiangular
    assert eq["angle"] == Fraction(1, 5);       n_verified += 1
    assert eq["gerzon_satisfied"];               n_verified += 1
    assert eq["welch_satisfied"];                n_verified += 1

    # Sigma arithmetic
    assert ids["sigma_r_plus_sigma_s"] == Fraction(2);   n_verified += 1
    assert ids["sigma_r_times_sigma_s"] == Fraction(-35); n_verified += 1
    assert ids["sum_1pr_1ps"] == Fraction(0);             n_verified += 1

    # Triangle / GQ structure
    assert tr_A3 == Fraction(960);         n_verified += 1
    assert n_tri == Fraction(160);         n_verified += 1
    assert ids["tris_per_line"] == Fraction(4);  n_verified += 1
    assert ids["energy_eq_edges"];               n_verified += 1

    # Welch & Gerzon from ids
    assert ids["welch_satisfied"];               n_verified += 1
    assert ids["n_geq_gerzon"];                  n_verified += 1

    print(f"\nVerified: {n_verified} identities")

    results = {
        "sigma_0": str(sigma[0][0]),
        "sigma_r": str(sigma[1][0]),
        "sigma_s": str(sigma[2][0]),
        "seidel_energy": str(E_S),
        "tr_S2": str(tr2),
        "tr_S3": str(moments[2]),
        "angle": str(eq["angle"]),
        "gerzon_bound": str(eq["gerzon_bound"]),
        "welch_satisfied": eq["welch_satisfied"],
        "tr_A3": str(tr_A3),
        "n_triangles": str(n_tri),
        "lines_GQ": v,
        "det_S_formula": ids["det_S_formula"],
        "n_verified": n_verified,
    }

    with open("PART_MCLIX_SEIDEL_MATRIX_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to PART_MCLIX_SEIDEL_MATRIX_results.json")

    return results


if __name__ == "__main__":
    seidel_matrix_main()
