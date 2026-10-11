"""Pass 11919: the tilt modulus -- magnetized fluxes are Humbert singular relations, and the forced first-generation zero
is the non-simplicity of the compactification abelian surface.

1. A flux N in the dx^dy block is (1,1) for Omega = [[t1,t2],[t2,t3]] iff N Omega = Omega N, i.e. iff Omega satisfies
   Humbert's singular relation  -N12 t1 + (N11 - N22) t2 + N12 t3 = 0  of discriminant
   Delta = (N11 - N22)^2 + 4 N12^2 = (tr N)^2 - 4 det N.  For a det-3 dual pair (Pass 11916/11917), Delta = m^2 - 12.
2. On the dual-pair slice Omega = x + y N1 the integral block fluxes are u + v N1, with index form
   det(u + v N1) = u^2 + m u v + 3 v^2 of discriminant m^2 - 12. The abelian surface contains an elliptic curve (a
   zero-index flux) iff this form is isotropic iff m^2 - 12 is a square iff m = 4 (the only solution of
   (m - k)(m + k) = 12): exactly the A2 and x^2 + 3y^2 pairs, whose zero-index fluxes A2 - 1, A2 - 3 (resp.
   diag(0,2), diag(-2,0)) are the mod-3 frame lines of Pass 11917. So: the zero is forced for every modulus iff the flux
   forces the abelian surface to be non-simple; for m = 5, 7 (Delta = 13, 37) the slice is a Hilbert modular surface for
   Q(sqrt Delta) whose generic member is simple, and the zero sits on the diagonal tau+ = tau- (E x E).
3. The Galois involution of Z[N1] sends N1 -> m - N1 = N2 (Cayley-Hamilton): it exchanges the 10 and 5bar fluxes. It is
   realised by the lattice rotation R (R^T N R = adj N), which maps (N10, N5, x + y N1) to (N5, N10, x + y N2) -- checked
   on the Yukawa spectra. At y = 0 it is an automorphism of the torus that swaps the two SU(5) sectors; since 10 != 5bar,
   no symmetry of the model protects (or forbids) the tilt.
4. Fluxes cannot produce a small tilt: any further block flux outside Q[N1] has commutant = scalars and forces y = 0
   (restoring m_d = 0). A nonzero tilt needs oblique fluxes (Humbert relations with a det-Omega term), which cut the
   Hilbert surface in curves and points -- arithmetic, O(1) values of y, not a small parameter.
Classical inputs: Humbert (1899) singular relations; NS(A) of abelian surfaces (Birkenhake-Lange ch. 10/11); magnetic
fluxes fixing complex structure (Antoniadis-Maillard 2004; Blumenhagen-Lust-Taylor 2003).
"""

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11919_tilt_modulus_humbert.json"
PAIRS = [([[1, 0], [0, 3]], [[3, 0], [0, 1]]), ([[2, 1], [1, 2]], [[2, -1], [-1, 2]]),
         ([[1, 1], [1, 4]], [[4, -1], [-1, 1]]), ([[3, 3], [3, 4]], [[4, -3], [-3, 3]])]


def main():
    rng = np.random.default_rng(11919)
    # 1. compatibility <=> singular relation; discriminant identity
    hum = []
    for _ in range(200):
        a, c = rng.integers(1, 9, 2)
        b = int(rng.integers(-6, 7))
        N = np.array([[a, b], [b, c]], float)
        x, y = rng.normal(size=2) + 1j * rng.normal(size=2)
        Om_on = x * np.eye(2) + y * N
        Om_off = Om_on + 0.3 * np.array([[1, 0], [0, -1]]) * (1 + 1j)
        rel = lambda O: -N[0, 1] * O[0, 0] + (N[0, 0] - N[1, 1]) * O[0, 1] + N[0, 1] * O[1, 1]
        comm = lambda O: np.max(abs(N @ O - O @ N))
        hum.append([abs(rel(Om_on)), comm(Om_on), abs(rel(Om_off)) > 1e-9 or N[0, 1] == 0, comm(Om_off) > 1e-9 or b == 0])
        assert (a - c) ** 2 + 4 * b * b == (a + c) ** 2 - 4 * (a * c - b * b)
    hum = np.array(hum, float)
    # 2. index form and isotropy
    u, v, m = sp.symbols("u v m")
    forms_ok = True
    for N1, _ in PAIRS:
        M = sp.Matrix(N1)
        mm = int(M.trace())
        forms_ok &= sp.expand((u * sp.eye(2) + v * M).det() - (u ** 2 + mm * u * v + 3 * v ** 2)) == 0
    square_m = [mm for mm in range(1, 400) if mm * mm - 12 >= 0 and sp.sqrt(mm * mm - 12).is_integer]
    zero_index = {}
    for N1, _ in PAIRS[:2]:
        M = np.array(N1)
        zs = [M - k * np.eye(2, dtype=int) for k in (1, 3)]
        lines = []
        for Z in zs:
            col = Z[:, 0] if Z[:, 0].any() else Z[:, 1]
            g = np.gcd.reduce(col)
            col = col // g
            col = col if col[col != 0][0] > 0 else -col
            lines.append(tuple(int(t) for t in col))
        zero_index[str(N1)] = dict(dets=[int(round(np.linalg.det(Z))) for Z in zs], lines=lines)
    # 3. Galois swap realised by R: spectra of (N1, N2, x + y N1) == spectra of (N2, N1, x + y N2)
    R = np.array([[0, -1], [1, 0]])
    gal = []
    for N1, N2 in PAIRS[1:3]:
        assert (R.T @ np.array(N1) @ R == np.array(N2)).all()
        Om = 1j * (1.1 * np.eye(2) + 0.15 * np.array(N1)) + 0.1 * np.eye(2)
        Om2 = R.T @ Om @ R
        S1 = sorted(tuple(np.round(np.linalg.svd(Y, compute_uv=False), 9)) for Y in F.yukawas(F.T4(Om, 12), N1, N2))
        S2 = sorted(tuple(np.round(np.linalg.svd(Y, compute_uv=False), 9)) for Y in F.yukawas(F.T4(Om2, 12), N2, N1))
        gal.append(dict(N1=N1, omega2_is_x_plus_y_N2=bool(np.allclose(Om2, 1j * (1.1 * np.eye(2) + 0.15 * np.array(N2)) + 0.1 * np.eye(2))),
                        max_spectrum_diff=float(np.max(abs(np.array(S1) - np.array(S2))))))
    # 4. commutant of {N1, N'} for N' outside span{1, N1}
    comm_dims = []
    for N1, _ in PAIRS:
        for Np in ([[1, 0], [0, 2]], [[2, 1], [1, 3]], [[1, 2], [2, 5]]):
            A = np.array(N1, float)
            B = np.array(Np, float)
            if np.linalg.matrix_rank(np.array([np.eye(2).ravel(), A.ravel(), B.ravel()])) < 3:
                continue
            rows = []
            for E in (np.array([[1, 0], [0, 0]]), np.array([[0, 1], [1, 0]]), np.array([[0, 0], [0, 1]])):
                rows.append(np.concatenate([(A @ E - E @ A).ravel(), (B @ E - E @ B).ravel()]))
            comm_dims.append(3 - np.linalg.matrix_rank(np.array(rows).T))
    res = dict(pass_id=11919, humbert_on_slice_max=float(hum[:, :2].max()), humbert_off_slice_detects=bool(hum[:, 2:].all()),
               index_form_ok=bool(forms_ok), m_with_square_discriminant=square_m, zero_index_fluxes=zero_index,
               galois_swap=gal, commutant_dims_with_extra_flux=sorted(set(int(d) for d in comm_dims)),
               humbert_discriminants={str(N1): int(np.trace(N1) ** 2 - 12) for N1, _ in PAIRS})
    res["checks"] = {k: bool(val) for k, val in dict(
        compatibility_is_singular_relation=res["humbert_on_slice_max"] < 1e-12 and res["humbert_off_slice_detects"],
        index_form_u2_muv_3v2=forms_ok,
        square_discriminant_only_m4=square_m == [4],
        zero_index_fluxes_are_frame_lines=sorted(zero_index[str(PAIRS[0][0])]["lines"]) == [(0, 1), (1, 0)]
        and sorted(zero_index[str(PAIRS[1][0])]["lines"]) == [(1, -1), (1, 1)]
        and all(d == 0 for z in zero_index.values() for d in z["dets"]),
        galois_swap_is_rotation=all(g["omega2_is_x_plus_y_N2"] and g["max_spectrum_diff"] < 1e-8 for g in gal),
        extra_flux_forces_scalar_omega=res["commutant_dims_with_extra_flux"] == [1],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
