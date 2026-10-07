"""Pass 11643: the Hamming null cube is the set of eight Clifford transvection ticks, and its arrow is the handedness of
the tick on the Hesse sphere.

OBJECTS.
  * Pass 11550: eight oriented rank-one symmetric matrices S = c v v^T over F3 (c = 1: Veronese sheet, chi = -1, Weil
    phase -i; c = 2 = -1: negative sheet, chi = +1, Weil phase +i).
  * The symplectic transvection t_S = I + S Omega on qutrit phase space F3^2 (coordinates (x, z), Weyl operators
    X^x Z^z, Omega = [[0,-1],[1,0]]).  (S Omega)^2 = 0, so t_S has order 3 and t_{-S} = t_S^{-1}.
  * Its Clifford gate U_S in the canonical Weil representation: U = V D_c V^dagger, where D_c = diag(omega^(2 c j^2))
    implements the shear (x, z) -> (x, z + c x) and V implements any element conjugating that shear to t_S.
    (A conjugate of D_c is independent of V's phase, so U_S and tr U_S are canonical.)
  * Its action R(U_S) = B^T U_S^(x3) B on the Hesse pencil (Pass 11641), an order-3 rotation of the Hesse Bloch sphere.

CHECKED (all eight, objectwise):
  1. tr U_S / |tr U_S| = Pass 11550's stored Weil phase (= i chi).
  2. U_{-S} = U_S^{-1}: Pass 11550's "outer temporal reversal" S -> -S is literally running the tick backwards.
  3. R(U_S) is a rotation by 120 degrees fixing the image m_v of the MUB of v (the eigenbasis of the Pauli along v).
     Its POSITIVE (right-handed) axis is +m_v (a stabiliser vertex, xyz > 0) on the Veronese sheet and -m_v (the
     antipodal T-magic vertex, Pass 11641) on the negative sheet.  So chi = -sign(xyz) of the positive axis.
  4. Unitary Cliffords preserve each sheet (the two conjugacy classes of order-3 unipotents in SL(2,3)); complex
     conjugation (Wigner time reversal) maps U_S to the gate of a negative-sheet matrix: the Hamming arrow of a tick is
     T-odd, although Pass 11550's congruence action of PSp = W(D3) preserves it (the det = -1 coset acts on ticks by
     congruence composed with -1).
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11643_hamming_cube_is_transvection_clock.json"
C11550 = ROOT / "data" / "PART_W33_PASS11550_VERONESE_WEIL_HAMMING_ORIENTATION.json"
C11600 = ROOT / "data" / "w33_pass11600_dynamical_hesse_flavor.json"

w = np.exp(2j * np.pi / 3)
Xq = np.roll(np.eye(3), 1, axis=0)
Zq = np.diag([1, w, w * w])
OM = np.array([[0, -1], [1, 0]])


def weyl(p):
    return np.linalg.matrix_power(Xq, p[0] % 3) @ np.linalg.matrix_power(Zq, p[1] % 3)


def implements(U, g):
    """U W(p) U^dagger proportional to W(g p) for the basis p = (1,0), (0,1)"""
    for p in ((1, 0), (0, 1)):
        A = U @ weyl(p) @ U.conj().T
        Bm = weyl(tuple(g @ np.array(p) % 3))
        lam = np.trace(Bm.conj().T @ A) / 3
        if not (abs(abs(lam) - 1) < 1e-9 and np.allclose(A, lam * Bm)):
            return False
    return True


def clifford_table():
    """projective Clifford unitaries for all 24 elements of SL(2,3), by BFS from the DFT and the shear D_1"""
    Fq = np.array([[w ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)
    D1 = np.diag([w ** (2 * j * j) for j in range(3)])
    gens = []
    for U in (Fq, D1):
        for g in itertools.product(range(3), repeat=4):
            g = np.array(g).reshape(2, 2)
            if round(np.linalg.det(g)) % 3 == 1 and implements(U, g):
                gens.append((g, U))
                break
    assert len(gens) == 2
    table = {(1, 0, 0, 1): np.eye(3, dtype=complex)}
    frontier = [(np.eye(2, dtype=int), np.eye(3, dtype=complex))]
    while frontier:
        new = []
        for g, U in frontier:
            for h, V in gens:
                gh = (h @ g) % 3
                key = tuple(gh.flatten())
                if key not in table:
                    table[key] = V @ U
                    new.append((gh, V @ U))
        frontier = new
    assert len(table) == 24
    for k, U in table.items():
        assert implements(U, np.array(k).reshape(2, 2))
    return table


def D(c):
    return np.diag([w ** (2 * c * j * j) for j in range(3)])


def shear(c):
    return np.array([[1, 0], [c % 3, 1]])


def gate(t, table):
    """canonical Weil gate of the order-3 unipotent t: conjugate of D_c"""
    for c in (1, 2):
        for k, V in table.items():
            g = np.array(k).reshape(2, 2)
            ginv = np.round(np.linalg.inv(g) * np.linalg.det(g)).astype(int) % 3     # adjugate; det g = 1
            if np.array_equal((g @ shear(c) @ ginv) % 3, t % 3):
                return c, V @ D(c) @ V.conj().T
    raise ValueError(t)


def pencil_R(U):
    import itertools as it
    d = np.zeros(27)
    s = np.zeros(27)
    for i in range(3):
        d[13 * i] = 1
    for p in it.permutations(range(3)):
        s[9 * p[0] + 3 * p[1] + p[2]] = 1
    B = np.stack([d / np.sqrt(3), s / np.sqrt(6)], 1)
    return B.T @ np.kron(np.kron(U, U), U) @ B


def so3(R2, T):
    """rotation of the Bloch vector r = (2Re(u0* u1), 2Im(u0* u1), |u0|^2-|u1|^2), in Pass 11600 axes n = T^T r"""
    paulis = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
    O = np.array([[0.5 * np.trace(paulis[i] @ R2 @ paulis[j] @ R2.conj().T).real for j in range(3)] for i in range(3)])
    return T.T @ O @ T


def positive_axis(O):
    """unit n with O n = n and O rotating by +120 degrees about n (right-handed)"""
    vals, vecs = np.linalg.eig(O)
    n = np.real(vecs[:, np.argmin(abs(vals - 1))])
    n /= np.linalg.norm(n)
    a = np.cross(n, [1, 0.3, 0.1])
    a /= np.linalg.norm(a)
    b = O @ a
    sin = np.dot(n, np.cross(a, b))
    cos = np.dot(a, b)
    ang = np.degrees(np.arctan2(sin, cos))
    return (n if ang > 0 else -n), abs(ang)


def main():
    cert = json.load(open(C11550))
    import sympy as sp
    T = np.array([[float(sp.sympify(x)) for x in row] for row in json.load(open(C11600))["tensor"]["Bloch_axes"]]).T
    T = T.T                                    # stored axes are columns (Pass 11641); n = T_cols^T r, see so3()
    table = clifford_table()
    # MUB images in Pass 11600 axes (Pass 11641): the Pauli along v = (x, z) has eigenbasis = MUB of slope v
    m = {}
    for v in ((0, 1), (1, 0), (1, 1), (1, 2)):
        _, V = np.linalg.eig(weyl(v))
        psi = V[:, 0]
        u0 = (psi ** 3).sum() / np.sqrt(3)
        u1 = np.sqrt(6) * psi.prod()
        c = np.conj(u0) * u1
        r = np.array([2 * c.real, 2 * c.imag, abs(u0) ** 2 - abs(u1) ** 2])
        n = T.T @ r
        m[v] = n / np.linalg.norm(n)
    rows = []
    for sheet, key, phase_key in (("veronese", "rank_one_matrices", "veronese_sheet"),
                                  ("negative", "rank_one_nonsquare_scaled_matrices", "negative_veronese_sheet")):
        block = cert[phase_key]
        for (a, b, cc), z in zip(block[key], block["hamming_images"]):
            S = np.array([[a, b], [b, cc]])
            t = (np.eye(2, dtype=int) + S @ OM) % 3
            cls, U = gate(t, table)
            tr = np.trace(U)
            ph = tr / abs(tr)
            tinv = (np.eye(2, dtype=int) - S @ OM) % 3
            _, Uinv = gate(tinv, table)
            O = so3(pencil_R(U), T)
            nplus, ang = positive_axis(O)
            v = next(vv for vv in m if np.allclose((t @ np.array(vv)) % 3, vv) and any(vv))
            side = "+m_v (stabiliser vertex)" if np.allclose(nplus, m[v], atol=1e-9) else (
                "-m_v (T-magic vertex)" if np.allclose(nplus, -m[v], atol=1e-9) else "other")
            # Wigner time reversal: conj(U) is the gate of J0 t J0, J0 = diag(1,-1)
            J0 = np.diag([1, 2])
            tK = (J0 @ t @ J0) % 3
            clsK, UK = gate(tK, table)
            SK = None
            for s in itertools.product(range(3), repeat=3):
                Sm = np.array([[s[0], s[1]], [s[1], s[2]]])
                if np.array_equal((np.eye(2, dtype=int) + Sm @ OM) % 3, tK):
                    SK = Sm
            rows.append(dict(
                sheet=sheet, S=[a, b, cc], hamming=z, chi=block["chi_value"], stored_weil_phase=block["old_weil_phase"],
                transvection=t.tolist(), shear_class_c=cls,
                trace_phase=[round(ph.real, 12), round(ph.imag, 12)],
                trace_phase_matches_stored=bool(np.isclose(ph, -1j if block["old_weil_phase"] == "-i" else 1j)),
                inverse_is_gate_of_minus_S=bool(np.allclose(Uinv, np.linalg.inv(U))),
                rotation_angle_deg=round(ang, 9), fixed_MUB_slope=list(v), positive_axis=side,
                xyz_sign_of_positive_axis=int(np.sign(np.prod(nplus))),
                conj_U_equals_gate_of_J0tJ0=bool(np.allclose(np.conj(U), UK)),
                time_reversed_S=None if SK is None else [int(SK[0, 0]), int(SK[0, 1]), int(SK[1, 1])],
                time_reversed_sheet_flips=None if SK is None else bool(
                    any(np.array_equal(SK % 3, (2 * np.outer(vv, vv)) % 3) for vv in itertools.product(range(3), repeat=2))
                    if sheet == "veronese" else
                    any(np.array_equal(SK % 3, np.outer(vv, vv) % 3) for vv in itertools.product(range(3), repeat=2)))))
    summary = dict(
        rows=len(rows),
        weil_phase_equals_trace_phase=int(sum(r["trace_phase_matches_stored"] for r in rows)),
        outer_reversal_is_inverse_tick=int(sum(r["inverse_is_gate_of_minus_S"] for r in rows)),
        rotation_120=int(sum(abs(r["rotation_angle_deg"] - 120) < 1e-6 for r in rows)),
        veronese_positive_axis_stabiliser=int(sum(r["positive_axis"].startswith("+m_v") for r in rows if r["sheet"] == "veronese")),
        negative_positive_axis_magic=int(sum(r["positive_axis"].startswith("-m_v") for r in rows if r["sheet"] == "negative")),
        chi_equals_minus_xyz_sign_of_positive_axis=int(sum(r["chi"] == -r["xyz_sign_of_positive_axis"] for r in rows)),
        conj_is_gate_of_reflected_tick=int(sum(r["conj_U_equals_gate_of_J0tJ0"] for r in rows)),
        wigner_reversal_flips_sheet=int(sum(bool(r["time_reversed_sheet_flips"]) for r in rows)),
        shear_class_by_sheet={s: sorted({r["shear_class_c"] for r in rows if r["sheet"] == s}) for s in ("veronese", "negative")},
    )
    print(summary)
    json.dump(dict(pass_id=11643, summary=summary, rows=rows,
                   conventions="phase space (x, z), W(x,z) = X^x Z^z, Omega = [[0,-1],[1,0]], t_S = I + S Omega, "
                               "D_c = diag(omega^(2 c j^2)) implements (x,z) -> (x, z + c x); Codex's matrix (a,b,c) is "
                               "[[a,b],[b,c]] in the same (x, z) order"),
              open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
