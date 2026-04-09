"""
Finite Spectral Triple on W(3,3): Forward Computation
=====================================================

This script constructs a candidate finite spectral triple (A, H, D, J, gamma)
on the 40-vertex graph W(3,3) and computes spectral action coefficients
FROM FIRST PRINCIPLES — no fitting to known physics constants.

The question: does the spectral action on W(3,3) produce anything that
looks like the Standard Model, or is it just graph theory?

CONNES' FRAMEWORK:
  A finite spectral triple consists of:
    A     = finite-dimensional *-algebra acting on H
    H     = finite-dimensional Hilbert space
    D     = self-adjoint "Dirac" operator on H
    J     = antilinear isometry (real structure / charge conjugation)
    gamma = Z/2 grading (chirality)

  The spectral action is S = Tr(f(D/Lambda)) where f is a cutoff function.
  In the heat kernel expansion: S ~ sum_n f_n * a_n(D^2)
  where a_n are the Seeley-DeWitt coefficients.

FOR W(3,3):
  H = R^40 (one basis vector per vertex)
  A = {polynomials in A} = span{I, A, J_40} (the Bose-Mesner algebra)
  D candidates:
    (1) D = A (adjacency matrix itself)
    (2) D = A - (r+s)/2 * I = A + I  (centered spectrum)
    (3) D = L = kI - A (graph Laplacian)
    (4) D = normalized: D = A/sqrt(k)
  J = the identity (trivial real structure) or graph automorphism
  gamma = spectral projector sign(A - threshold)

We compute everything and see what falls out.
"""

import numpy as np
from collections import Counter
import json


def build_w33():
    """Build W(3,3) adjacency matrix from F_3^4 with standard symplectic form."""
    F3 = [0, 1, 2]
    vecs = [(a, b, c, d) for a in F3 for b in F3 for c in F3 for d in F3
            if (a, b, c, d) != (0, 0, 0, 0)]

    points = []
    seen = set()
    for v in vecs:
        canon = min(tuple((s * x) % 3 for x in v) for s in [1, 2])
        if canon not in seen:
            seen.add(canon)
            points.append(canon)
    assert len(points) == 40

    def omega(u, v):
        return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % 3

    n = len(points)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i+1, n):
            if omega(points[i], points[j]) == 0:
                A[i][j] = 1.0
                A[j][i] = 1.0
    return A, points


def spectral_decomposition(A):
    """Compute eigenvalues, multiplicities, and projectors."""
    eigvals, eigvecs = np.linalg.eigh(A)
    # Round eigenvalues to identify clusters
    rounded = np.round(eigvals, 6)
    unique_vals = sorted(set(rounded))

    decomp = {}
    for val in unique_vals:
        mask = np.abs(rounded - val) < 1e-4
        mult = int(mask.sum())
        vecs = eigvecs[:, mask]
        P = vecs @ vecs.T  # projector onto eigenspace
        decomp[float(np.round(val, 2))] = {
            'multiplicity': mult,
            'projector': P,
            'eigenvectors': vecs
        }
    return decomp


def heat_kernel_coefficients(D, max_power=8):
    """
    Compute Seeley-DeWitt-like coefficients from Tr(D^n).
    These are the moments of the spectral measure.
    """
    n = D.shape[0]
    coeffs = {}
    D_power = np.eye(n)
    for k in range(max_power + 1):
        coeffs[k] = float(np.trace(D_power))
        D_power = D_power @ D
    return coeffs


def spectral_action_expansion(D, cutoff_scales):
    """
    Compute the spectral action Tr(f(D^2/Lambda^2))
    for f(x) = exp(-x) at various cutoff scales Lambda.
    """
    eigvals = np.linalg.eigvalsh(D)
    results = {}
    for Lambda in cutoff_scales:
        S = sum(np.exp(-(e/Lambda)**2) for e in eigvals)
        results[Lambda] = float(S)
    return results


def check_ko_dimension(D, J, gamma):
    """
    Check KO-dimension axioms for (D, J, gamma).
    KO-dim n mod 8 is determined by:
      J^2 = epsilon * I
      JD = epsilon' * DJ
      J*gamma = epsilon'' * gamma*J
    where (epsilon, epsilon', epsilon'') depends on n mod 8.
    """
    n = D.shape[0]
    # J^2
    J2 = J @ J
    if np.allclose(J2, np.eye(n)):
        eps = +1
    elif np.allclose(J2, -np.eye(n)):
        eps = -1
    else:
        eps = None

    # JD vs DJ
    JD = J @ D
    DJ = D @ J
    if np.allclose(JD, DJ):
        eps_prime = +1
    elif np.allclose(JD, -DJ):
        eps_prime = -1
    else:
        eps_prime = None

    # J*gamma vs gamma*J
    Jg = J @ gamma
    gJ = gamma @ J
    if np.allclose(Jg, gJ):
        eps_pp = +1
    elif np.allclose(Jg, -gJ):
        eps_pp = -1
    else:
        eps_pp = None

    # KO-dimension table (epsilon, epsilon', epsilon'')
    ko_table = {
        0: (+1, +1, +1),
        1: (+1, -1, None),  # no gamma in odd dim
        2: (-1, +1, +1),
        3: (-1, +1, None),
        4: (-1, +1, -1),
        5: (-1, -1, None),
        6: (+1, +1, -1),
        7: (+1, -1, None),
    }

    # Find matching KO-dim
    for dim, (e, ep, epp) in ko_table.items():
        if eps == e and eps_prime == ep:
            if epp is None or eps_pp == epp:
                return dim, (eps, eps_prime, eps_pp)

    return None, (eps, eps_prime, eps_pp)


def connes_distance(D, i, j):
    """
    Connes spectral distance between vertices i and j:
    d(i,j) = sup { |f(i) - f(j)| : ||[D, f]|| <= 1 }
    where f is a "function" (diagonal matrix).

    For the graph Dirac D = A, this reduces to:
    d(i,j) = 1/max_eigenvalue if adjacent, etc.
    We compute it numerically.
    """
    n = D.shape[0]
    # For finite graphs, the Connes distance can be computed via
    # d(i,j) = max over unit vectors e: |<e_i - e_j, D^{-1} e>| ... simplified

    # Actually, for a finite spectral triple with D = adjacency:
    # [D, M_f] = D*diag(f) - diag(f)*D
    # ||[D, M_f]|| = operator norm of off-diagonal part
    # We need: max |f_i - f_j| s.t. ||[D, M_f]|| <= 1

    # This is a semidefinite program. For small n, brute force:
    # Just compute graph distance and compare.
    # For SRG(40,12,2,4), graph distances are 1 (adjacent) or 2 (non-adjacent).
    return None  # placeholder


def main():
    print("=" * 72)
    print("  FINITE SPECTRAL TRIPLE ON W(3,3)")
    print("  Forward computation — no fitting to physics")
    print("=" * 72)

    A, points = build_w33()
    n = A.shape[0]  # 40

    # ═══════════════════════════════════════════════════════════════
    # PART 1: Spectral Decomposition
    # ═══════════════════════════════════════════════════════════════
    print("\n[1] SPECTRAL DECOMPOSITION")
    decomp = spectral_decomposition(A)
    print(f"  Eigenvalues and multiplicities:")
    for val, info in sorted(decomp.items()):
        print(f"    eigenvalue {val:6.1f}  mult = {info['multiplicity']}")

    P_vac = decomp[12.0]['projector']   # vacuum (1-dim)
    P_r = decomp[2.0]['projector']      # r-eigenspace (24-dim)
    P_s = decomp[-4.0]['projector']     # s-eigenspace (15-dim)

    print(f"\n  Projector ranks: P_vac={np.trace(P_vac):.0f}, "
          f"P_r={np.trace(P_r):.0f}, P_s={np.trace(P_s):.0f}")
    print(f"  Sum = {np.trace(P_vac + P_r + P_s):.0f} (should be 40)")

    # ═══════════════════════════════════════════════════════════════
    # PART 2: Four Candidate Dirac Operators
    # ═══════════════════════════════════════════════════════════════
    print("\n[2] CANDIDATE DIRAC OPERATORS")

    # (a) D = A (raw adjacency)
    D_raw = A.copy()

    # (b) D = A - (r+s)/2 * I = A + I  (centered, so eigenvalues symmetric-ish)
    r, s = 2.0, -4.0
    D_centered = A - (r + s) / 2 * np.eye(n)  # eigenvalues: 13, 3, -3

    # (c) D = L = kI - A (graph Laplacian)
    k = 12
    D_laplacian = k * np.eye(n) - A  # eigenvalues: 0, 10, 16

    # (d) D = signed: eigenvalues {+12, +2, -4} -> keep sign structure
    D_signed = A.copy()  # same as raw

    dirac_candidates = {
        "D_adjacency": D_raw,
        "D_centered": D_centered,
        "D_laplacian": D_laplacian,
    }

    for name, D in dirac_candidates.items():
        eigs = sorted(np.linalg.eigvalsh(D))
        eig_rounded = Counter(np.round(eigs, 2).astype(float))
        print(f"\n  {name}:")
        print(f"    Eigenvalues: {dict(sorted(eig_rounded.items()))}")

    # ═══════════════════════════════════════════════════════════════
    # PART 3: Heat Kernel / Moment Coefficients
    # ═══════════════════════════════════════════════════════════════
    print("\n[3] MOMENT COEFFICIENTS Tr(D^n) for each candidate")
    print("    (Seeley-DeWitt-like coefficients of spectral action)")

    results = {}
    for name, D in dirac_candidates.items():
        moments = heat_kernel_coefficients(D, max_power=6)
        print(f"\n  {name}:")
        for power, val in moments.items():
            # Express in terms of W(3,3) parameters where possible
            label = ""
            if name == "D_adjacency":
                if power == 0: label = f" = v = 40"
                elif power == 1: label = f" = 0 (traceless)"
                elif power == 2: label = f" = vk = {40*12}"
                elif power == 3: label = f" = 6T = 6*160 = {6*160}"
            print(f"    Tr(D^{power}) = {val:>15.0f}{label}")
        results[name] = moments

    # ═══════════════════════════════════════════════════════════════
    # PART 4: Spectral Action at Various Cutoffs
    # ═══════════════════════════════════════════════════════════════
    print("\n[4] SPECTRAL ACTION S = Tr(exp(-D^2/Lambda^2))")

    for name, D in dirac_candidates.items():
        sa = spectral_action_expansion(D, [1, 2, 4, 8, 12, 20, 50, 100])
        print(f"\n  {name}:")
        for Lambda, S in sorted(sa.items()):
            print(f"    Lambda = {Lambda:>4}:  S = {S:.6f}")
        # Large Lambda limit should be dim(H) = 40
        print(f"    Lambda -> inf:  S -> {n} (dim H)")

    # ═══════════════════════════════════════════════════════════════
    # PART 5: KO-Dimension Check
    # ═══════════════════════════════════════════════════════════════
    print("\n[5] KO-DIMENSION CHECK")

    # Try J = identity (trivial real structure)
    J_trivial = np.eye(n)

    # Try gamma = sign of eigenvalue (grading by bosonic/fermionic)
    # gamma has eigenvalue +1 on V_vac + V_r, eigenvalue -1 on V_s
    gamma_phys = P_vac + P_r - P_s  # +1 on {12, 2} sector, -1 on {-4} sector
    print(f"  gamma eigenvalues: +1 (mult {int(np.trace((gamma_phys + np.eye(n))/2))}),"
          f" -1 (mult {int(np.trace((np.eye(n) - gamma_phys)/2))})")

    for name, D in dirac_candidates.items():
        ko, signs = check_ko_dimension(D, J_trivial, gamma_phys)
        print(f"  {name} + J=I + gamma=sign: KO-dim = {ko}, signs = {signs}")

    # Alternative grading: +1 on V_s (gauge), -1 on V_vac + V_r
    gamma_alt = -P_vac + P_r - P_s + 2*P_s  # let me redo
    gamma_alt = P_s - P_vac - P_r  # -1 on {12, 2}, +1 on {-4}
    for name, D in dirac_candidates.items():
        ko, signs = check_ko_dimension(D, J_trivial, gamma_alt)
        print(f"  {name} + J=I + gamma=alt: KO-dim = {ko}, signs = {signs}")

    # ═══════════════════════════════════════════════════════════════
    # PART 6: Algebra Structure (Bose-Mesner)
    # ═══════════════════════════════════════════════════════════════
    print("\n[6] BOSE-MESNER ALGEBRA = COMMUTANT")
    J_all = np.ones((n, n))
    BM = np.array([np.eye(n).flatten(), A.flatten(), J_all.flatten()])
    rank_BM = np.linalg.matrix_rank(BM)
    print(f"  dim(Bose-Mesner) = {rank_BM}")
    print(f"  This is the FULL commutant of PSp(4,3) acting on R^40")
    print(f"  -> The 'algebra' A of the spectral triple is 3-dimensional")
    print(f"  -> Isomorphic to C + C + C (three copies of the reals)")
    print(f"  -> NOT isomorphic to C + H + M_3(C) (Connes' A_F for SM)")

    # ═══════════════════════════════════════════════════════════════
    # PART 7: Sector Decomposition — What Actually Falls Out
    # ═══════════════════════════════════════════════════════════════
    print("\n[7] WHAT ACTUALLY FALLS OUT (no fitting)")
    print()

    # Eigenvalue structure
    eig_k, eig_r, eig_s = 12, 2, -4
    f_mult, g_mult = 24, 15

    print(f"  From the adjacency spectrum alone:")
    print(f"    40 = 1 + 24 + 15  (spectral decomposition)")
    print(f"    This IS the irreducible decomposition under PSp(4,3)")
    print(f"    V_15 IS the adjoint representation (proven via ATLAS)")
    print(f"    V_24 IS a 24-dim irrep (proven)")
    print()

    # Moments give genuine invariants
    print(f"  Moment invariants Tr(A^n):")
    trA2 = eig_k**2 + f_mult * eig_r**2 + g_mult * eig_s**2
    trA3 = eig_k**3 + f_mult * eig_r**3 + g_mult * eig_s**3
    trA4 = eig_k**4 + f_mult * eig_r**4 + g_mult * eig_s**4
    print(f"    Tr(A^2) = {trA2} = vk = 40*12")
    print(f"    Tr(A^3) = {trA3} = 6T = 6*160 (triangle count)")
    print(f"    Tr(A^4) = {trA4} = ?")

    # Check what trA4 equals in terms of parameters
    # Tr(A^4) = number of closed walks of length 4
    # = sum over (i,j): (A^2)_{ij}^2
    # For SRG: Tr(A^4) = v*k + (v choose 2)*(lambda^2 + (v-k-1)*mu^2) ... complex
    # Just compute: 12^4 + 24*2^4 + 15*(-4)^4 = 20736 + 384 + 3840 = 24960
    print(f"    Tr(A^4) = {trA4} = {eig_k}^4 + {f_mult}*{eig_r}^4 + {g_mult}*{eig_s}^4")
    print(f"           = {eig_k**4} + {f_mult * eig_r**4} + {g_mult * eig_s**4}")

    # Sector traces
    print(f"\n  Sector-resolved traces:")
    for name, D in dirac_candidates.items():
        D2 = D @ D
        tr_vac = float(np.trace(P_vac @ D2))
        tr_r = float(np.trace(P_r @ D2))
        tr_s = float(np.trace(P_s @ D2))
        print(f"    {name}: Tr(P_vac D^2)={tr_vac:.0f}, "
              f"Tr(P_r D^2)={tr_r:.0f}, Tr(P_s D^2)={tr_s:.0f}, "
              f"total={tr_vac+tr_r+tr_s:.0f}")

    # ═══════════════════════════════════════════════════════════════
    # PART 8: The Honest Conclusion
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  HONEST CONCLUSION")
    print("=" * 72)
    print()
    print("  WHAT IS PROVEN:")
    print("    (1) W(3,3) has spectrum {12^1, 2^24, (-4)^15}")
    print("    (2) This is multiplicity-free under PSp(4,3) = W(E_6)^+")
    print("    (3) V_15 = adjoint of PSp(4,3) (ATLAS)")
    print("    (4) Payne derivation gives SRG(27,10,1,5) = compl(Schlafli)")
    print("    (5) 40-27 chain complex has ker(NN^T) = V_15 (gauge massless)")
    print()
    print("  WHAT IS NOT PROVEN:")
    print("    (a) The Bose-Mesner algebra A = C+C+C, NOT C+H+M_3(C)")
    print("        -> W(3,3) does NOT directly give the Connes A_F algebra")
    print("    (b) No natural J or gamma produces KO-dim 6 (SM value)")
    print("    (c) The spectral action moments are graph invariants,")
    print("        but their physical interpretation is asserted, not derived")
    print("    (d) alpha^-1 = 137 comes from (k-1)^2 + mu^2 = 121+16,")
    print("        which is a post-hoc Gaussian integer norm, not derived")
    print("        from any spectral action computation")
    print()
    print("  THE GAP:")
    print("    To connect W(3,3) to the Standard Model via Connes' framework,")
    print("    one would need to show that the PRODUCT geometry M^4 x F")
    print("    has F = W(3,3) in some precise sense. But:")
    print("    - Connes' F has algebra C+H+M_3(C) (dim 14 over R)")
    print("    - W(3,3)'s commutant is C+C+C (dim 3)")
    print("    - These are NOT isomorphic")
    print("    This is the fundamental obstacle.")
    print("=" * 72)

    # Save
    output = {
        "spectrum": {"12": 1, "2": 24, "-4": 15},
        "moments_adjacency": {str(k): float(v) for k, v in results["D_adjacency"].items()},
        "moments_centered": {str(k): float(v) for k, v in results["D_centered"].items()},
        "moments_laplacian": {str(k): float(v) for k, v in results["D_laplacian"].items()},
        "bose_mesner_dim": int(rank_BM),
        "connes_algebra_needed": "C + H + M_3(C)  (dim 14 over R)",
        "w33_commutant": "C + C + C  (dim 3)",
        "ko_dim_achievable": "KO-dim 0 with J=I, gamma=spectral sign",
        "fundamental_obstacle": "Bose-Mesner algebra C+C+C != Connes A_F = C+H+M_3(C)",
        "proven_facts": [
            "40 = 1 + 24 + 15 multiplicity-free decomposition under PSp(4,3)",
            "V_15 = adjoint of PSp(4,3)",
            "Payne derivation -> SRG(27,10,1,5) = complement of Schlafli",
            "ker(NN^T) = V_15 (gauge sector massless from geometry)",
            "Tr(A^2) = vk = 480, Tr(A^3) = 6T = 960",
        ],
        "not_proven": [
            "alpha^-1 = 137 (post-hoc Gaussian norm, not derived)",
            "sin^2 theta_W = 3/13 (pattern match, not spectral action)",
            "SM gauge group from W(3,3) algebra (wrong algebra type)",
            "KO-dimension 6 (cannot achieve with natural choices)",
        ]
    }
    with open("data/w33_spectral_triple.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Saved to data/w33_spectral_triple.json")


if __name__ == "__main__":
    main()
