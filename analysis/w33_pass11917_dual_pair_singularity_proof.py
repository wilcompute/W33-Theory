"""Pass 11917: proof of the dual-pair singularity (Pass 11916) -- the down Yukawa is a level-3 theta two-qutrit state read
in a tensor frame fixed by the flux mod 3, and m_d = 0 is "factorised torus" (Pass 11872) in that frame.

Setup (Pass 11915/11916): 10 flux N1, 5bar flux N2 = 3 N1^{-1} (det 3), Higgs flux N1 + N2 = m 1 (Cayley-Hamilton),
period matrix Omega compatible (N Omega symmetric, hence Omega commutes with N1, N2).

1. Exact formula. Write x1 = y + (N2/m) u, x2 = y - (N1/m) u. Because N1 m^{-1} N2 = (3/m) 1 is scalar,
       x1 N1 Omega x1 + x2 N2 Omega x2 = m y Omega y + (3/m) u Omega u,
   and the product psi^{N1}_a psi^{N2}_b expands in psi^{m}_c with coefficient
       Y^c_{ab} = sum_{k in Z^2, N2 k = a + b - c (mod m)} exp(i pi (3/m) (k + (N2 a - N1 b)/3) Omega (k + (N2 a - N1 b)/3)).
   Checked against the 4D overlap integrals (ratio constant to 1e-8).
2. Reduction mod 3. gcd(m, 3) = 1 for every det-3 form (a + c = 0 mod 3 forces 9 | ac - b^2). By CRT the
   characteristic's mod-m part is -N1 c (independent of a, b), and its mod-3 part is N2 a - N1 b. N1 = lambda v v^T and
   N2 = mu w w^T mod 3 with v.w = 0 (N1 N2 = 3). Because x^2 + y^2 is anisotropic over F3, the pair of orthogonal lines
   {v, w} is either the AXES {(1,0),(0,1)} or the DIAGONALS {(1,1),(1,-1)}. Hence Y^c is the 3 x 3 coefficient matrix of
   the level-3 theta vector  f_c(q mod 3) = sum_{q' = q mod 3} g_c(q'),  g_c Gaussian of metric (m/3) Omega,
   in the tensor split F3^2 = <v> + <w> -- a two-qutrit state in the frame fixed by the flux.
3. Theorem. If Omega is diagonal in the integral lift of that frame (index 1 for axes, 2 for diagonals; coprime to 3),
   g_c factorises on each coset, so rank Y^c <= 1 (axes) or <= 2 (diagonals), for every Higgs mode and every Wilson line
   (Wilson lines add a linear phase (3/m) u.(zeta_Q - zeta_R), which also factorises). This is Pass 11872's
   "product state = factorised torus", with the 2-isogeny E+ x E- -> T4 supplying exactly one extra Schmidt rank.
4. Which pairs are forced. A compatible Omega is a polynomial in N1. The eigenframe of N1 IS its mod-3 frame for A2
   (eigenvectors (1, +-1)) and for x^2 + 3y^2 = diag(1,3); so for these two pairs EVERY compatible modulus is
   frame-diagonal and m_d = m_e = 0 for all moduli. For the four irrational pairs (1,+-1,4), (3,+-3,4) the eigenframe is
   irrational, a non-scalar compatible modulus Omega = i(t + y N1) un-factorises the frame, and the zero lifts at tree
   level -- linearly: s3/s2 is proportional to y (log-slope 1).
Correction to Pass 11916: the three axis-frame dual pairs have rank exactly 1, not 2, at frame-diagonal Omega.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11917_dual_pair_singularity_proof.json"
PAIRS = [([[1, 0], [0, 3]], [[3, 0], [0, 1]]), ([[2, 1], [1, 2]], [[2, -1], [-1, 2]]),
         ([[1, 1], [1, 4]], [[4, -1], [-1, 1]]), ([[1, -1], [-1, 4]], [[4, 1], [1, 1]]),
         ([[3, 3], [3, 4]], [[4, -3], [-3, 3]]), ([[3, -3], [-3, 4]], [[4, 3], [3, 3]])]


def formula(N1, N2, Om):
    N1, N2 = np.array(N1), np.array(N2)
    m = int(round(np.trace(N1 + N2) / 2))
    out = []
    for jc in F.chars(m * np.eye(2)):
        c = np.round(m * jc).astype(int)
        Y = np.zeros((3, 3), complex)
        for ia, ja in enumerate(F.chars(N1)):
            a = np.round(N1 @ ja).astype(int)
            for ib, jb in enumerate(F.chars(N2)):
                b = np.round(N2 @ jb).astype(int)
                sh = (N2 @ a - N1 @ b) / 3.0
                for k in itertools.product(range(-12, 13), repeat=2):
                    k = np.array(k)
                    if np.all((N2 @ k - (a + b - c)) % m == 0):
                        u = k + sh
                        Y[ia, ib] += np.exp(1j * np.pi * (3 / m) * (u @ Om @ u))
        out.append(Y)
    return out


def mod3_line(N):
    M = np.array(N) % 3
    col = M[:, 0] if M[:, 0].any() else M[:, 1]
    return tuple(int(x) for x in (col * pow(int(col[col != 0][0]), -1, 3)) % 3)


def frame(N1):
    return "axes" if mod3_line(N1) in ((1, 0), (0, 1)) else "diagonals"


def spectra(N1, N2, Om, zq, zr, G=12):
    T = F.T4(Om, G)
    zQ, zR = zq[:2] + Om @ zq[2:], zr[:2] + Om @ zr[2:]
    S = np.array([np.linalg.svd(Y, compute_uv=False) for Y in F.yukawas(T, N1, N2, zQ, zR)])
    return S / S[:, :1]


def main():
    rng = np.random.default_rng(11917)
    # 1. formula vs overlap integrals
    fchk = []
    for N1, N2, Om in ((PAIRS[1][0], PAIRS[1][1], 1.5j * np.array([[1, 0.3], [0.3, 1]])),
                       (PAIRS[2][0], PAIRS[2][1], 1j * (1.2 * np.eye(2) + 0.3 * np.array(PAIRS[2][0])))):
        Yn, Yf = F.yukawas(F.T4(Om, 14), N1, N2), formula(N1, N2, Om)
        big = max(abs(y).max() for y in Yf)
        r = np.array([Yn[k][i, j] / Yf[k][i, j] for k in range(len(Yn)) for i in range(3) for j in range(3)
                      if abs(Yf[k][i, j]) > 1e-8 * big])
        zero = max([abs(Yn[k][i, j]) for k in range(len(Yn)) for i in range(3) for j in range(3)
                    if abs(Yf[k][i, j]) <= 1e-8 * big] + [0.0])
        fchk.append(dict(N1=N1, ratio_rel_spread=float(np.ptp(abs(r)) / abs(r).mean()),
                         ratio_phase_spread=float(np.ptp(np.angle(r))), max_numeric_where_formula_zero=float(zero)))
    # 2. arithmetic: gcd(m,3) = 1, orthogonal mod-3 lines, only two orthogonal frames over F3
    forms = [[[a, b], [b, c]] for a in range(1, 13) for c in range(1, 13) for b in range(-12, 13) if a * c - b * b == 3]
    gcd_ok = all((f[0][0] + f[1][1]) % 3 != 0 for f in forms)
    orth_ok = all(np.dot(mod3_line(f), mod3_line((3 * np.linalg.inv(f)).round().astype(int))) % 3 == 0 for f in forms)
    lines = [(1, 0), (0, 1), (1, 1), (1, 2)]
    aniso = all((x * x + y * y) % 3 != 0 for x, y in lines)
    orth_pairs = sorted({tuple(sorted((p, q))) for p in lines for q in lines if p != q and (p[0] * q[0] + p[1] * q[1]) % 3 == 0})
    # 3. ranks at scalar Omega (frame-diagonal), random Wilson lines
    zq, zr = rng.random(4), rng.random(4)
    rank_rows = []
    for N1, N2 in PAIRS:
        S = spectra(N1, N2, 1.6j * np.eye(2), zq, zr)
        rank_rows.append(dict(N1=N1, frame=frame(N1), max_s2=float(S[:, 1].max()), max_s3=float(S[:, 2].max())))
    # 4. eigenframe vs mod-3 frame; non-scalar compatible Omega = i(1.2 + y N1)
    lift_rows = []
    for N1, N2 in PAIRS:
        ev = np.linalg.eigh(np.array(N1, float))[1]
        rational = all(np.allclose(abs(v) / abs(v).max(), np.round(abs(v) / abs(v).max())) for v in ev.T)
        S = spectra(N1, N2, 1j * (1.2 * np.eye(2) + 0.05 * np.array(N1)), zq, zr)
        lift_rows.append(dict(N1=N1, eigenframe_rational=bool(rational), y=0.05, max_s3=float(S[:, 2].max())))
    # 5. linear lift for (1,1,4)
    ys = [0.0003, 0.001, 0.003]
    r = [spectra(PAIRS[2][0], PAIRS[2][1], 1j * (1.2 * np.eye(2) + y * np.array(PAIRS[2][0])), zq, zr) for y in ys]
    lift = [float(np.median(S[:, 2] / S[:, 1])) for S in r]
    slope = float(np.polyfit(np.log(ys), np.log(lift), 1)[0])
    res = dict(pass_id=11917, formula_check=fchk, det3_forms_checked=len(forms), gcd_m_3_is_1=gcd_ok,
               dual_lines_orthogonal_mod3=orth_ok, f3_lines_anisotropic=aniso, orthogonal_frames=orth_pairs,
               scalar_omega_ranks=rank_rows, nonscalar_lift=lift_rows,
               linear_lift=dict(pair=PAIRS[2][0], ys=ys, median_s3_over_s2=lift, log_slope=slope))
    forced = [row for row in lift_rows if row["eigenframe_rational"]]
    free = [row for row in lift_rows if not row["eigenframe_rational"]]
    res["checks"] = {k: bool(v) for k, v in dict(
        formula_matches_overlaps=all(f["ratio_rel_spread"] < 1e-6 and f["max_numeric_where_formula_zero"] < 1e-6 for f in fchk),
        gcd_m_3_is_1=gcd_ok,
        dual_lines_orthogonal_mod3=orth_ok,
        exactly_two_orthogonal_frames=aniso and orth_pairs == [((0, 1), (1, 0)), ((1, 1), (1, 2))],
        axes_rank_one=all(r["max_s2"] < 1e-10 for r in rank_rows if r["frame"] == "axes"),
        diagonals_rank_two=all(r["max_s3"] < 1e-12 and r["max_s2"] > 1e-3 for r in rank_rows if r["frame"] == "diagonals"),
        rational_eigenframe_exactly_a2_and_rect=sorted(str(r["N1"]) for r in forced) == sorted(map(str, [PAIRS[0][0], PAIRS[1][0]])),
        forced_pairs_stay_singular=all(r["max_s3"] < 1e-12 for r in forced),
        irrational_pairs_lift=all(r["max_s3"] > 1e-10 for r in free),
        lift_is_linear=abs(slope - 1) < 0.1,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
