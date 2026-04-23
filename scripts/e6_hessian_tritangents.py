#!/usr/bin/env python3
"""Hessian / Heisenberg decomposition of the 45 E6 cubic (tritangent) triads.

This repo contains an intrinsic, fully-computed model of the E6 27-set as a
3-adic Heisenberg-labelled space:

  H27  ≅  F3^2 × F3   with coordinates (u1,u2,z).

In that model, the 45 tritangent planes (triads) split canonically as:

  - 9  "fiber" triads  (constant-u, z runs over 0/1/2), and
    - 36 "affine-line" triads (u collinear in AG(2,3), arranged in 12 line-families
             of 3 triads each).

The same 36+9 split appears in the classical Hessian/Witting literature as
"36 tritangents in 12×(_3{4}_2) plus 9 diameter tritangents". We don't rely on
that literature here; we just verify the finite-geometry structure from our
artifacts.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
for p in (ROOT, SCRIPTS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

ART = ROOT / "artifacts"

U2 = Tuple[int, int]
U3 = Tuple[int, int, int]
Triad = Tuple[int, int, int]
Perm = Tuple[int, ...]
Mat2 = Tuple[Tuple[int, int], Tuple[int, int]]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm_triad(tri: Iterable[int]) -> Triad:
    a, b, c = (int(x) for x in tri)
    t = tuple(sorted((a, b, c)))
    if len(t) != 3:
        raise ValueError(f"bad triad: {tri!r}")
    return t  # type: ignore[return-value]


def _mod3(x: int) -> int:
    return int(x) % 3


def _u_add(a: U2, b: U2) -> U2:
    return (_mod3(a[0] + b[0]), _mod3(a[1] + b[1]))


def _u_sub(a: U2, b: U2) -> U2:
    return (_mod3(a[0] - b[0]), _mod3(a[1] - b[1]))


def _u_scale(a: U2, s: int) -> U2:
    return (_mod3(s * a[0]), _mod3(s * a[1]))

def _omega_u(a: U2, b: U2) -> int:
    """Alternating form omega((x,y),(x',y')) = x*y' - y*x' over F3."""
    return _mod3(a[0] * b[1] - a[1] * b[0])


def _psi(a: U2, u: U2) -> int:
    """Heisenberg cocycle psi = (1/2)·omega on F3, with 1/2 = 2 mod 3."""
    return _mod3(2 * _omega_u(a, u))


def _dir_canonical(d: U2) -> U2:
    """Canonicalize direction in F3^2 up to nonzero scalar multiples."""
    if d == (0, 0):
        raise ValueError("zero direction")
    d1 = (_mod3(d[0]), _mod3(d[1]))
    d2 = _u_scale(d1, 2)  # 2 = -1 mod 3
    return min(d1, d2)


@dataclass(frozen=True)
class HessianSplit:
    fiber_triads: List[Triad]
    affine_triads: List[Triad]
    u_lines: List[Tuple[U2, U2, U2]]
    u_line_directions: Dict[U2, List[Tuple[U2, U2, U2]]]
    e6id_to_vec: Dict[int, U3]
    vec_to_e6id: Dict[U3, int]


def load_heisenberg_model() -> Mapping[str, Any]:
    return _load_json(ART / "e6_cubic_affine_heisenberg_model.json")


def load_firewall_bad_triads() -> List[Triad]:
    data = _load_json(ART / "firewall_bad_triads_mapping.json")
    bad = data.get("bad_triangles_Schlafli_e6id", [])
    if not (isinstance(bad, list) and len(bad) == 9):
        raise ValueError("unexpected bad-triad payload")
    return [_norm_triad(t) for t in bad]


def _heisenberg_vec_maps(model: Mapping[str, Any]) -> Tuple[Dict[int, U3], Dict[U3, int]]:
    raw = model.get("e6id_to_heisenberg", {})
    if not isinstance(raw, dict) or len(raw) != 27:
        raise ValueError("missing/invalid e6id_to_heisenberg mapping")
    e6id_to_vec: Dict[int, U3] = {}
    vec_to_e6id: Dict[U3, int] = {}
    for k, payload in raw.items():
        if not isinstance(payload, dict):
            raise ValueError("unexpected heisenberg entry")
        u = payload.get("u")
        z = payload.get("z")
        if not (isinstance(u, list) and len(u) == 2):
            raise ValueError("unexpected heisenberg u")
        vec = (_mod3(int(u[0])), _mod3(int(u[1])), _mod3(int(z)))
        e6id = int(k)
        e6id_to_vec[e6id] = vec
        vec_to_e6id[vec] = e6id
    if len(e6id_to_vec) != 27 or len(vec_to_e6id) != 27:
        raise ValueError("expected 27-point inverse map")
    return e6id_to_vec, vec_to_e6id


def _extract_fiber_triads(model: Mapping[str, Any]) -> List[Triad]:
    fiber = model.get("fiber_triads_e6id", [])
    if not (isinstance(fiber, list) and len(fiber) == 9):
        raise ValueError("unexpected fiber triad list")
    return sorted({_norm_triad(t) for t in fiber})


def _extract_affine_triads(model: Mapping[str, Any]) -> List[Triad]:
    lines = model.get("affine_u_lines", [])
    if not (isinstance(lines, list) and len(lines) == 12):
        raise ValueError("unexpected affine_u_lines payload")
    triads: set[Triad] = set()
    for entry in lines:
        if not isinstance(entry, dict):
            raise ValueError("unexpected affine_u_lines entry")
        for tri in entry.get("triads", []):
            triads.add(_norm_triad(tri))
    if len(triads) != 36:
        raise ValueError(f"expected 36 affine triads, got {len(triads)}")
    return sorted(triads)


def _extract_u_lines(model: Mapping[str, Any]) -> List[Tuple[U2, U2, U2]]:
    lines = model.get("affine_u_lines", [])
    if not (isinstance(lines, list) and len(lines) == 12):
        raise ValueError("unexpected affine_u_lines payload")
    u_lines: list[Tuple[U2, U2, U2]] = []
    for entry in lines:
        if not isinstance(entry, dict):
            raise ValueError("unexpected affine_u_lines entry")
        u_line = entry.get("u_line", [])
        if not (isinstance(u_line, list) and len(u_line) == 3):
            raise ValueError("unexpected u_line payload")
        pts = tuple((int(p[0]) % 3, int(p[1]) % 3) for p in u_line)
        if len(set(pts)) != 3:
            raise ValueError("u_line is not 3 distinct points")
        u_lines.append(tuple(sorted(pts)))  # canonicalize as set-like tuple
    if len(set(u_lines)) != 12:
        raise ValueError("expected 12 distinct u-lines")
    return sorted(set(u_lines))

def _all_ag23_lines() -> List[Tuple[U2, U2, U2]]:
    """All 12 affine lines in AG(2,3) on U=F3^2 (as 3-point subsets)."""
    U = [(i, j) for i in range(3) for j in range(3)]
    # 4 direction classes in F3^2 / {±1}
    dirs = sorted({_dir_canonical((a, b)) for a in range(3) for b in range(3) if not (a == 0 and b == 0)})
    if len(dirs) != 4:
        raise ValueError("expected 4 direction classes in AG(2,3)")

    lines: set[Tuple[U2, U2, U2]] = set()
    for u0 in U:
        for d in dirs:
            pts = tuple(sorted({_u_add(u0, _u_scale(d, t)) for t in (0, 1, 2)}))
            if len(pts) != 3:
                raise ValueError("unexpected line size")
            lines.add(pts)  # duplicates collapse

    if len(lines) != 12:
        raise ValueError(f"expected 12 AG(2,3) lines, got {len(lines)}")
    return sorted(lines)


def _u_line_direction(u_line: Tuple[U2, U2, U2]) -> U2:
    """Return the direction class of a 3-point affine line in AG(2,3)."""
    pts = list(u_line)
    diffs: set[U2] = set()
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            d = _u_sub(pts[j], pts[i])
            if d != (0, 0):
                diffs.add(_dir_canonical(d))
    # A 3-point line should have exactly one direction class.
    if len(diffs) != 1:
        raise ValueError(f"unexpected u-line diffs: {u_line} -> {sorted(diffs)}")
    return next(iter(diffs))


def _apply_matrix(A: Mat2, u: U2) -> U2:
    return (
        _mod3(A[0][0] * u[0] + A[0][1] * u[1]),
        _mod3(A[1][0] * u[0] + A[1][1] * u[1]),
    )


def _det2(A: Mat2) -> int:
    return _mod3(A[0][0] * A[1][1] - A[0][1] * A[1][0])


def _perm_compose(p: Perm, q: Perm) -> Perm:
    """Permutation composition p∘q (apply q then p)."""
    return tuple(p[i] for i in q)


def _perm_translation(
    e6id_to_vec: Mapping[int, U3], vec_to_e6id: Mapping[U3, int], a: U2, c: int
) -> Perm:
    """Heisenberg translation (u,z) ↦ (u+a, z+c+psi(a,u))."""
    a = (_mod3(a[0]), _mod3(a[1]))
    c = _mod3(int(c))
    out: list[int] = []
    for i in range(27):
        u1, u2, z = e6id_to_vec[i]
        u = (u1, u2)
        u_new = _u_add(u, a)
        z_new = _mod3(z + c + _psi(a, u))
        out.append(int(vec_to_e6id[(u_new[0], u_new[1], z_new)]))
    return tuple(out)


def _perm_symplectic(
    e6id_to_vec: Mapping[int, U3], vec_to_e6id: Mapping[U3, int], A: Mat2
) -> Perm:
    """Linear Sp(2,3)=SL(2,3) action on u-plane; z unchanged."""
    out: list[int] = []
    for i in range(27):
        u1, u2, z = e6id_to_vec[i]
        u_new = _apply_matrix(A, (u1, u2))
        out.append(int(vec_to_e6id[(u_new[0], u_new[1], z)]))
    return tuple(out)


def _perm_affine_gl23(
    e6id_to_vec: Mapping[int, U3],
    vec_to_e6id: Mapping[U3, int],
    A: Mat2,
    b: U2,
    c: int,
) -> Perm:
    """Affine Heisenberg-GL(2,3) action on H27.

    The full local automorphism group on the Heisenberg shell acts by

      u' = A u + b,
      z' = det(A) z - psi(Au,b) + c,

    where A is any element of GL(2,3), b is a translation in F3^2, and c is a
    central shift.
    """
    detA = _det2(A)
    if detA == 0:
        raise ValueError("A must lie in GL(2,3)")

    out: list[int] = []
    b = (_mod3(b[0]), _mod3(b[1]))
    c = _mod3(c)
    for i in range(27):
        u1, u2, z = e6id_to_vec[i]
        u = (u1, u2)
        Au = _apply_matrix(A, u)
        u_new = _u_add(Au, b)
        z_new = _mod3(detA * z - _psi(Au, b) + c)
        out.append(int(vec_to_e6id[(u_new[0], u_new[1], z_new)]))
    return tuple(out)


@lru_cache(maxsize=1)
def _signed_cubic_triad_sign_data() -> tuple[list[Triad], list[int], dict[Triad, int]]:
    """Return (triads, signs, sign_by_triad) for the canonical E6 cubic."""
    path = ART / "canonical_su3_gauge_and_cubic.json"
    data = _load_json(path)
    raw_triads = data.get("triads", [])
    raw_d = (data.get("solution") or {}).get("d_triples", [])
    if not (isinstance(raw_triads, list) and isinstance(raw_d, list)):
        raise ValueError("unexpected signed-cubic JSON payload")
    if len(raw_triads) != 45 or len(raw_d) != 45:
        raise ValueError("expected 45 signed cubic triads")

    triads: list[Triad] = []
    signs: list[int] = []
    for t, obj in zip(raw_triads, raw_d, strict=True):
        if not (isinstance(t, list) and len(t) == 3 and isinstance(obj, dict)):
            raise ValueError("unexpected signed-cubic triad entry")
        tri = _norm_triad(t)
        s = int(obj.get("sign", 0) or 0)
        if s not in (-1, 1):
            raise ValueError(f"unexpected cubic triad sign: {s}")
        triads.append(tri)
        signs.append(int(s))

    sign_by = {t: int(s) for t, s in zip(triads, signs, strict=True)}
    if len(triads) != 45 or len(sign_by) != 45:
        raise ValueError("unexpected signed-cubic triad duplication")
    return triads, signs, sign_by


@lru_cache(maxsize=1)
def _heisenberg_signed_cubic_triad_sign_data() -> tuple[list[Triad], list[int], dict[Triad, int]]:
    """Return (triads, signs, sign_by_triad) for the Heisenberg cubic on H27.

    The Heisenberg cubic has 45 triads: 9 fiber triads (constant u in F3^2) and
    36 affine triads grouped into 12 AG(2,3) line-families of 3 triads each.
    All signs are +1 because this helper records the unsigned Heisenberg/Hessian
    cubic support rather than the SU(3)-gauge signed lift.
    """
    model = load_heisenberg_model()
    fiber = _extract_fiber_triads(model)
    affine = _extract_affine_triads(model)
    triads: list[Triad] = list(fiber) + list(affine)
    if len(triads) != 45:
        raise ValueError(f"expected 45 Heisenberg cubic triads, got {len(triads)}")
    signs: list[int] = [1] * 45
    sign_by = {t: 1 for t in triads}
    if len(sign_by) != 45:
        raise ValueError("unexpected Heisenberg cubic triad duplication")
    return triads, signs, sign_by


def _gf2_solve_min_weight(*, rows: list[int], rhs: list[int], n_vars: int) -> int | None:
    """Solve A x = b over GF(2), choosing the minimum-weight solution.

    Input rows are bitmasks of length ``n_vars`` (least-significant bit is var 0).
    Returns a bitmask encoding a solution x with the fewest 1-bits (ties broken
    by the smallest integer mask), or None if inconsistent.
    """
    if len(rows) != len(rhs):
        raise ValueError("rows/rhs length mismatch")
    if n_vars <= 0 or n_vars > 63:
        raise ValueError("unsupported n_vars for bitmask solver")

    m = len(rows)
    A = [int(r) for r in rows]
    b = [int(x) & 1 for x in rhs]

    pivot_cols: list[int] = []

    row = 0
    for col in range(n_vars):
        bit = 1 << int(col)
        pivot = None
        for r in range(row, m):
            if A[r] & bit:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            A[row], A[pivot] = A[pivot], A[row]
            b[row], b[pivot] = b[pivot], b[row]

        # eliminate this column in all other rows (RREF)
        for r in range(m):
            if r == row:
                continue
            if A[r] & bit:
                A[r] ^= A[row]
                b[r] ^= b[row]

        pivot_cols.append(int(col))
        row += 1
        if row == m:
            break

    # inconsistency check: 0 = 1 rows
    for r in range(m):
        if A[r] == 0 and b[r] == 1:
            return None

    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(n_vars) if c not in pivot_set]

    # particular solution with all free vars = 0
    x0 = 0
    for r, col in enumerate(pivot_cols):
        if b[r] & 1:
            x0 |= 1 << int(col)

    # After elimination, pivot rows live in A[0:rank]; snapshot them now.
    pivot_row_masks = [int(A[r]) for r in range(len(pivot_cols))]

    # basis vectors for each free variable (homogeneous solutions)
    basis: list[int] = []
    for fc in free_cols:
        v = 1 << int(fc)
        for prow_mask, pcol in zip(pivot_row_masks, pivot_cols, strict=True):
            if prow_mask & (1 << int(fc)):
                v |= 1 << int(pcol)
        basis.append(int(v))

    # brute-force all 2^d solutions (d is small here) and choose minimal weight
    best = x0
    best_w = int(best).bit_count()
    for mask in range(1 << len(basis)):
        x = x0
        for i, v in enumerate(basis):
            if (mask >> i) & 1:
                x ^= int(v)
        w = int(x).bit_count()
        if w < best_w or (w == best_w and int(x) < int(best)):
            best = int(x)
            best_w = int(w)
    return int(best)


@lru_cache(maxsize=2048)
def signed_cubic_sign_lift_for_perm(perm: Perm) -> Tuple[int, ...]:
    """Return a {±1}-valued diagonal sign lift for a permutation of H27.

    The canonical E6 cubic invariant is stored as 45 signed triads (i,j,k,±1).
    Many natural permutations preserve the *support* triads but flip some signs.

    For a given permutation ``perm`` on {0..26}, we solve for a diagonal sign
    vector eps[i]∈{+1,-1} such that the monomial map

        x_j ↦ eps[j] · x_{perm^{-1}(j)}

    preserves the signed cubic exactly.

    Gauge: eps[0] is fixed to +1, which is sufficient for deterministic lifting.
    """
    if len(perm) != 27:
        raise ValueError("expected perm of length 27")
    if sorted(perm) != list(range(27)):
        raise ValueError("expected perm to be a permutation of 0..26")

    triads, signs, sign_by = _signed_cubic_triad_sign_data()
    rows: list[int] = []
    rhs: list[int] = []
    for (i, j, k), s in zip(triads, signs, strict=True):
        img = tuple(sorted((perm[i], perm[j], perm[k])))
        s_img = int(sign_by[img])
        ratio = int(s_img * s)  # division in {±1} equals multiplication
        b = 0 if ratio == 1 else 1
        mask = (1 << int(perm[i])) | (1 << int(perm[j])) | (1 << int(perm[k]))
        rows.append(int(mask))
        rhs.append(int(b))

    # gauge: eps[0] = +1  <=>  e_0 = 0 in GF(2)
    rows.append(1 << 0)
    rhs.append(0)

    sol = _gf2_solve_min_weight(rows=rows, rhs=rhs, n_vars=27)
    if sol is None:
        raise ValueError("no signed-cubic sign lift exists for this permutation")

    eps = tuple((-1 if ((sol >> i) & 1) else 1) for i in range(27))

    # Sanity: verify triad sign transport identity with the solved eps.
    for (i, j, k), s in zip(triads, signs, strict=True):
        img = tuple(sorted((perm[i], perm[j], perm[k])))
        s_img = int(sign_by[img])
        prod = int(eps[perm[i]] * eps[perm[j]] * eps[perm[k]])
        if int(s_img) != int(s) * prod:
            raise AssertionError("signed-cubic lift verification failed")

    return eps


@lru_cache(maxsize=2048)
def signed_heisenberg_cubic_sign_lift_for_perm(perm: Perm) -> Tuple[int, ...]:
    """Return the {+-1} diagonal sign lift for perm against the Heisenberg cubic.

    Identical to signed_cubic_sign_lift_for_perm but uses the Heisenberg 45-triad
    cubic (fiber triads + affine Heisenberg line triads, all with sign +1) instead of
    the canonical SU(3)-gauge cubic.  The Heisenberg generators are pure permutation
    automorphisms of this cubic, so the returned eps is always all-+1.
    """
    if len(perm) != 27:
        raise ValueError("expected perm of length 27")
    if sorted(perm) != list(range(27)):
        raise ValueError("expected perm to be a permutation of 0..26")

    triads, signs, sign_by = _heisenberg_signed_cubic_triad_sign_data()
    rows: list[int] = []
    rhs: list[int] = []
    for (i, j, k), s in zip(triads, signs, strict=True):
        img = tuple(sorted((perm[i], perm[j], perm[k])))
        s_img = int(sign_by[img])
        ratio = int(s_img * s)
        b = 0 if ratio == 1 else 1
        mask = (1 << int(perm[i])) | (1 << int(perm[j])) | (1 << int(perm[k]))
        rows.append(int(mask))
        rhs.append(int(b))

    rows.append(1 << 0)
    rhs.append(0)

    sol = _gf2_solve_min_weight(rows=rows, rhs=rhs, n_vars=27)
    if sol is None:
        raise ValueError("no Heisenberg-cubic sign lift exists for this permutation")

    eps = tuple((-1 if ((sol >> i) & 1) else 1) for i in range(27))

    for (i, j, k), s in zip(triads, signs, strict=True):
        img = tuple(sorted((perm[i], perm[j], perm[k])))
        s_img = int(sign_by[img])
        prod = int(eps[perm[i]] * eps[perm[j]] * eps[perm[k]])
        if int(s_img) != int(s) * prod:
            raise AssertionError("Heisenberg-cubic sign lift verification failed")

    return eps


@lru_cache(maxsize=1)
def hessian_heisenberg_generators() -> Dict[str, Perm]:
    """Return canonical generators of Heisenberg⋊SL(2,3) as permutations of H27."""
    model = load_heisenberg_model()
    e6id_to_vec, vec_to_e6id = _heisenberg_vec_maps(model)

    gen_T10 = _perm_translation(e6id_to_vec, vec_to_e6id, (1, 0), 0)
    gen_T01 = _perm_translation(e6id_to_vec, vec_to_e6id, (0, 1), 0)
    gen_Z = _perm_translation(e6id_to_vec, vec_to_e6id, (0, 0), 1)

    S: Mat2 = ((0, 2), (1, 0))
    T: Mat2 = ((1, 1), (0, 1))
    gen_S = _perm_symplectic(e6id_to_vec, vec_to_e6id, S)
    gen_T = _perm_symplectic(e6id_to_vec, vec_to_e6id, T)

    return {"T10": gen_T10, "T01": gen_T01, "Z": gen_Z, "S": gen_S, "T": gen_T}


@lru_cache(maxsize=1)
def hessian_affine_gl23_generators() -> Dict[str, Perm]:
    """Return canonical generators of the full affine Heisenberg-GL(2,3) group."""
    model = load_heisenberg_model()
    e6id_to_vec, vec_to_e6id = _heisenberg_vec_maps(model)

    gen_T10 = _perm_translation(e6id_to_vec, vec_to_e6id, (1, 0), 0)
    gen_T01 = _perm_translation(e6id_to_vec, vec_to_e6id, (0, 1), 0)
    gen_Z = _perm_translation(e6id_to_vec, vec_to_e6id, (0, 0), 1)

    S: Mat2 = ((0, 2), (1, 0))
    T: Mat2 = ((1, 1), (0, 1))
    R: Mat2 = ((1, 0), (0, 2))

    gen_S = _perm_affine_gl23(e6id_to_vec, vec_to_e6id, S, (0, 0), 0)
    gen_T = _perm_affine_gl23(e6id_to_vec, vec_to_e6id, T, (0, 0), 0)
    gen_R = _perm_affine_gl23(e6id_to_vec, vec_to_e6id, R, (0, 0), 0)

    return {
        "T10": gen_T10,
        "T01": gen_T01,
        "Z": gen_Z,
        "S": gen_S,
        "T": gen_T,
        "R": gen_R,
    }


def _enumerate_perm_group(generators: Iterable[Perm]) -> Tuple[Perm, ...]:
    identity: Perm = tuple(range(27))
    gens = [tuple(g) for g in generators]
    seen: set[Perm] = {identity}
    q: deque[Perm] = deque([identity])
    while q:
        g = q.popleft()
        for h in gens:
            gh = _perm_compose(h, g)
            if gh not in seen:
                seen.add(gh)
                q.append(gh)
    return tuple(sorted(seen))


def _perm_inverse(p: Perm) -> Perm:
    inv = [0] * len(p)
    for i, value in enumerate(p):
        inv[int(value)] = int(i)
    return tuple(inv)


def _triad_image(p: Perm, tri: Triad) -> Triad:
    a, b, c = tri
    return tuple(sorted((p[a], p[b], p[c])))  # type: ignore[return-value]


def _triad_family_invariant(group: Iterable[Perm], triads: Iterable[Triad]) -> bool:
    triad_set = {tuple(sorted(map(int, t))) for t in triads}
    for g in group:
        for tri in triad_set:
            if _triad_image(g, tri) not in triad_set:
                return False
    return True


def _transport_local_perm_to_e6id(
    local_perm: Perm, local_to_e6id: tuple[int, ...]
) -> Perm:
    out = [0] * len(local_to_e6id)
    for local_i, e6id in enumerate(local_to_e6id):
        out[e6id] = int(local_to_e6id[local_perm[local_i]])
    return tuple(out)


@lru_cache(maxsize=1)
def _exact_local_symmetry_transport() -> Dict[str, Any]:
    import tools.analyze_balanced_orbit_stabilizer as w33

    transport = _load_json(ART / "sage_h27_to_schlafli_effective_triads_conjugacy.json")
    h27_global = tuple(int(v) for v in transport["w33"]["H27_global"])
    local_to_e6id = tuple(int(v) for v in transport["h27_local_to_schlafli_e6id"])
    if len(h27_global) != 27 or len(local_to_e6id) != 27:
        raise ValueError("unexpected local-shell transport payload")
    if sorted(local_to_e6id) != list(range(27)):
        raise ValueError("local-shell transport is not a permutation of E6 ids")

    triads, _signs, _sign_by = _signed_cubic_triad_sign_data()
    triad_set = frozenset(triads)
    fiber_set = frozenset(_extract_fiber_triads(load_heisenberg_model()))
    affine_set = frozenset(_extract_affine_triads(load_heisenberg_model()))

    points, _adj, _edges = w33.build_w33()
    symplectic_generators = list(w33.get_generators(points))
    antisymplectic = w33.matrix_to_vertex_perm(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]], points
    )
    if antisymplectic is None:
        raise RuntimeError("failed to build antisymplectic generator permutation")

    projective_group = tuple(w33.enumerate_group(symplectic_generators))
    full_group = tuple(w33.enumerate_group(symplectic_generators + [antisymplectic]))

    h27_pos = {vertex: index for index, vertex in enumerate(h27_global)}

    def summarize(group: tuple[tuple[int, ...], ...]) -> Dict[str, Any]:
        stabilizer = tuple(tuple(g) for g in group if int(g[0]) == 0)
        local_group = {
            tuple(h27_pos[int(g[v])] for v in h27_global)
            for g in stabilizer
        }
        e6id_group = tuple(
            sorted(
                _transport_local_perm_to_e6id(local_perm, local_to_e6id)
                for local_perm in local_group
            )
        )
        base_e6id = int(local_to_e6id[0])
        orbit = {g[base_e6id] for g in e6id_group}
        point_stabilizer_order = sum(1 for g in e6id_group if g[base_e6id] == base_e6id)
        return {
            "global_group_order": len(group),
            "w33_point_stabilizer_order": len(stabilizer),
            "local_order": len(local_group),
            "e6id_group": e6id_group,
            "orbit_size": len(orbit),
            "point_stabilizer_order": point_stabilizer_order,
            "transitive": len(orbit) == 27,
            "triads_invariant": _triad_family_invariant(e6id_group, triad_set),
            "fiber_triads_invariant": _triad_family_invariant(e6id_group, fiber_set),
            "affine_triads_invariant": _triad_family_invariant(e6id_group, affine_set),
        }

    projective = summarize(projective_group)
    full = summarize(full_group)
    groups_meta = transport.get("groups", {})

    projective.update(
        {
            "transported_from_w33": True,
            "support_level": "exact transported local W33 stabilizer",
        }
    )
    full.update(
        {
            "transported_from_w33": True,
            "support_level": "exact transported local W33 stabilizer",
            "structure_h27": groups_meta.get("structure_h27"),
            "structure_eff": groups_meta.get("structure_eff"),
            "normal_27_subgroup_structure": groups_meta.get("structure_normal27"),
            "projective_subgroup_order": projective["local_order"],
            "projective_subgroup_index": len(full["e6id_group"]) // len(projective["e6id_group"]),
        }
    )

    return {
        "h27_global": h27_global,
        "local_to_e6id": local_to_e6id,
        "projective": projective,
        "affine": full,
    }


@lru_cache(maxsize=1)
def hessian_heisenberg_group_permutations() -> Tuple[Perm, ...]:
    return _enumerate_perm_group(hessian_heisenberg_generators().values())


@lru_cache(maxsize=1)
def hessian_affine_gl23_group_permutations() -> Tuple[Perm, ...]:
    return _enumerate_perm_group(hessian_affine_gl23_generators().values())


@lru_cache(maxsize=1)
def hessian_monomial_generators() -> Dict[str, Tuple[Perm, Tuple[int, ...]]]:
    """Return canonical lifted generators (perm, eps) preserving the *signed* cubic.

    Uses the Heisenberg cubic (fiber + affine Heisenberg line triads, all signs +1)
    rather than the canonical SU(3)-gauge cubic, because the Heisenberg⋊SL(2,3)
    generators preserve the Heisenberg triad structure, not the canonical triad
    structure.  For the canonical Heisenberg/Hessian generator family we work in
    the pure-permutation gauge, so the diagonal lift is chosen to be trivial.
    """
    gens = hessian_heisenberg_generators()
    eps = (1,) * 27
    return {k: (p, eps) for k, p in gens.items()}


def analyze_hessian_heisenberg_group(
    triads: Iterable[Triad], e6id_to_vec: Mapping[int, U3], vec_to_e6id: Mapping[U3, int]
) -> Dict[str, Any]:
    """Summarize the exact 648-element local projective subgroup on H27."""
    triad_set = {tuple(sorted(map(int, t))) for t in triads}
    if len(triad_set) != 45:
        raise ValueError("expected 45 triads for group invariance check")
    _ = (e6id_to_vec, vec_to_e6id)

    exact = _exact_local_symmetry_transport()["projective"]
    group = exact["e6id_group"]
    triads_invariant = _triad_family_invariant(group, triad_set)

    return {
        "order": exact["local_order"],
        "orbit_size": exact["orbit_size"],
        "point_stabilizer_order": exact["point_stabilizer_order"],
        "transitive": exact["transitive"],
        "triads_invariant": triads_invariant,
        "fiber_triads_invariant": exact["fiber_triads_invariant"],
        "affine_triads_invariant": exact["affine_triads_invariant"],
        "transported_from_w33": True,
        "support_level": exact["support_level"],
    }


def analyze_hessian_affine_group(
    fiber_triads: Iterable[Triad],
    affine_triads: Iterable[Triad],
    e6id_to_vec: Mapping[int, U3],
    vec_to_e6id: Mapping[U3, int],
) -> Dict[str, Any]:
    """Summarize the exact 1296-element local affine symmetry on H27."""
    fiber_set = {tuple(sorted(map(int, t))) for t in fiber_triads}
    affine_set = {tuple(sorted(map(int, t))) for t in affine_triads}
    triad_set = fiber_set | affine_set
    if len(triad_set) != 45:
        raise ValueError("expected 45 total triads for affine-group analysis")
    _ = (e6id_to_vec, vec_to_e6id)

    exact = _exact_local_symmetry_transport()["affine"]
    group = exact["e6id_group"]

    return {
        "order": exact["local_order"],
        "orbit_size": exact["orbit_size"],
        "point_stabilizer_order": exact["point_stabilizer_order"],
        "transitive": exact["transitive"],
        "triads_invariant": _triad_family_invariant(group, triad_set),
        "fiber_triads_invariant": _triad_family_invariant(group, fiber_set),
        "affine_triads_invariant": _triad_family_invariant(group, affine_set),
        "structure_h27": exact["structure_h27"],
        "structure_eff": exact["structure_eff"],
        "normal_27_subgroup_structure": exact["normal_27_subgroup_structure"],
        "projective_subgroup_order": exact["projective_subgroup_order"],
        "projective_subgroup_index": exact["projective_subgroup_index"],
        "transported_from_w33": True,
        "support_level": exact["support_level"],
    }


def analyze_hessian_tritangent_split() -> Dict[str, Any]:
    model = load_heisenberg_model()
    e6id_to_vec, vec_to_e6id = _heisenberg_vec_maps(model)

    fiber_triads = _extract_fiber_triads(model)
    affine_triads = _extract_affine_triads(model)
    all_triads = sorted(set(fiber_triads) | set(affine_triads))
    if len(all_triads) != 45:
        raise ValueError(f"expected 45 total triads, got {len(all_triads)}")
    if set(fiber_triads) & set(affine_triads):
        raise ValueError("fiber/affine triad sets should be disjoint")

    # Cross-check against the firewall's forbidden 9.
    bad = load_firewall_bad_triads()
    if sorted(bad) != sorted(fiber_triads):
        raise ValueError("firewall bad triads do not match fiber triads")

    # The u-plane is canonically AG(2,3). We compute its 12 lines directly,
    # and only use the artifact's u-lines as a cross-check.
    u_lines = _all_ag23_lines()
    u_lines_art = _extract_u_lines(model)
    if set(u_lines) != set(u_lines_art):
        raise ValueError("artifact u-lines do not match AG(2,3) enumeration")
    dirs: dict[U2, list[Tuple[U2, U2, U2]]] = defaultdict(list)
    for L in u_lines:
        dirs[_u_line_direction(L)].append(L)
    dirs = {k: sorted(v) for k, v in dirs.items()}

    # In AG(2,3) there are 4 direction classes, each with 3 parallel lines.
    direction_sizes = {k: len(v) for k, v in dirs.items()}

    # u-point incidence: each point lies on 4 lines, and each pair determines a line.
    u_points: list[U2] = sorted({p for L in u_lines for p in L})
    if len(u_points) != 9:
        raise ValueError("expected 9 u-points in AG(2,3)")
    through: Counter[U2] = Counter()
    for L in u_lines:
        through.update(L)
    pair_to_count: Counter[Tuple[U2, U2]] = Counter()
    for L in u_lines:
        a, b, c = L
        for x, y in ((a, b), (a, c), (b, c)):
            pair_to_count[tuple(sorted((x, y)))] += 1

    # Fiber triads are constant-u and sweep all z.
    fiber_u: dict[Triad, U2] = {}
    for tri in fiber_triads:
        vecs = [e6id_to_vec[i] for i in tri]
        u_set = {(v[0], v[1]) for v in vecs}
        z_set = {v[2] for v in vecs}
        if len(u_set) != 1 or z_set != {0, 1, 2}:
            raise ValueError(f"fiber triad not (u fixed, z all): {tri} -> {vecs}")
        fiber_u[tri] = next(iter(u_set))

    # Affine triads are the 36 non-fiber tritangent planes. In the Heisenberg
    # model each one projects to an AG(2,3) line and the artifact groups them
    # into 12 line-families of 3 triads that partition the 9 points above that line.
    affine_meta: dict[Triad, Dict[str, Any]] = {}
    u_line_sets = {frozenset(L) for L in u_lines}
    for tri in affine_triads:
        vecs = [e6id_to_vec[i] for i in tri]
        u_set = {(v[0], v[1]) for v in vecs}
        if len(u_set) != 3:
            raise ValueError(f"affine triad does not hit 3 distinct u fibers: {tri} -> {vecs}")
        if frozenset(u_set) not in u_line_sets:
            raise ValueError(f"affine triad u-set not a u-line: {tri} -> {sorted(u_set)}")
        affine_meta[tri] = {"u_line": sorted(u_set), "vecs": vecs}

    # Stronger per-line check: each u-line entry carries 3 triads partitioning
    # the 9 points of the three fibers over that line.
    raw_lines = model.get("affine_u_lines", [])
    for entry in raw_lines:
        entry_u_line = tuple(sorted((int(p[0]) % 3, int(p[1]) % 3) for p in entry["u_line"]))
        if frozenset(entry_u_line) not in u_line_sets:
            raise ValueError("raw u-line entry is not an AG(2,3) line")
        triads = [_norm_triad(t) for t in entry["triads"]]
        if len(triads) != 3:
            raise ValueError("expected 3 triads per u-line")
        union_points: set[int] = set()
        common_u_line_set: frozenset[U2] | None = None
        for tri in triads:
            vecs = [e6id_to_vec[i] for i in tri]
            tri_u = frozenset((v[0], v[1]) for v in vecs)
            if tri_u not in u_line_sets:
                raise ValueError(f"triad does not project to an AG(2,3) line: {tri} -> {sorted(tri_u)}")
            if common_u_line_set is None:
                common_u_line_set = tri_u
            elif tri_u != common_u_line_set:
                raise ValueError("u-line triads do not share a common base line")
            union_points.update(tri)
        if common_u_line_set is None:
            raise ValueError("expected nonempty triad family for u-line entry")
        expected_points = {
            vec_to_e6id[(u[0], u[1], z)] for u in common_u_line_set for z in (0, 1, 2)
        }
        if union_points != expected_points:
            raise ValueError("u-line triads do not partition the 3 fibers")

    # ---------------------------------------------------------------------
    # Exact reconstruction from the validated artifact partition data.
    # ---------------------------------------------------------------------
    recon_fiber: set[Triad] = set()
    U_pts = [(i, j) for i in range(3) for j in range(3)]
    for u in U_pts:
        tri = tuple(sorted(vec_to_e6id[(u[0], u[1], z)] for z in (0, 1, 2)))
        recon_fiber.add(tri)
    if len(recon_fiber) != 9:
        raise ValueError("expected 9 reconstructed fiber triads")

    recon_affine = {
        _norm_triad(tri)
        for entry in raw_lines
        for tri in entry.get("triads", [])
    }
    if len(recon_affine) != 36:
        raise ValueError(f"expected 36 reconstructed affine triads, got {len(recon_affine)}")

    if recon_fiber != set(fiber_triads):
        raise ValueError("reconstructed fiber triads mismatch artifact")
    if recon_affine != set(affine_triads):
        raise ValueError("reconstructed affine triads mismatch artifact")

    hessian_group = analyze_hessian_heisenberg_group(all_triads, e6id_to_vec, vec_to_e6id)
    affine_group = analyze_hessian_affine_group(
        fiber_triads, affine_triads, e6id_to_vec, vec_to_e6id
    )

    return {
        "counts": {
            "points_total": 27,
            "triads_total": 45,
            "fiber_triads": len(fiber_triads),
            "affine_triads": len(affine_triads),
            "u_points": len(u_points),
            "u_lines": len(u_lines),
            "u_line_directions": len(dirs),
        },
        "reconstruction": {
            "fiber_matches": True,
            "affine_matches": True,
            "affine_formula_asserted": False,
        },
        "hessian_group": hessian_group,
        "affine_group": affine_group,
        "ag23_checks": {
            "direction_sizes": direction_sizes,
            "u_point_line_degrees": dict(sorted(through.items())),
            "pair_line_counts": Counter(pair_to_count).most_common(3),
            "pairs_total": len(pair_to_count),
        },
        "fiber_triads": [list(t) for t in fiber_triads],
        "affine_triads": [list(t) for t in affine_triads],
        "u_lines": [[list(p) for p in L] for L in u_lines],
        "u_line_directions": {str(k): [[[a, b], [c, d], [e, f]] for ((a, b), (c, d), (e, f)) in v] for k, v in dirs.items()},
        "fiber_u": {str(list(k)): list(v) for k, v in fiber_u.items()},
        "affine_meta_sample": {str(list(k)): affine_meta[k] for k in sorted(list(affine_meta))[:5]},
        "heisenberg_maps": {
            "e6id_to_vec": {str(k): list(v) for k, v in sorted(e6id_to_vec.items())},
            "vec_to_e6id": {str(list(k)): v for k, v in sorted(vec_to_e6id.items())},
        },
    }


def main() -> None:
    print("=" * 72)
    print("E6 TRITANGENTS: HESSIAN/HEISENBERG 36+9 DECOMPOSITION")
    print("=" * 72)
    res = analyze_hessian_tritangent_split()

    c = res["counts"]
    print("\nCounts")
    print("-" * 30)
    for k in [
        "points_total",
        "triads_total",
        "fiber_triads",
        "affine_triads",
        "u_points",
        "u_lines",
        "u_line_directions",
    ]:
        print(f"  {k:>18}: {c[k]}")

    ag = res["ag23_checks"]
    print("\nAG(2,3) checks (u-plane)")
    print("-" * 30)
    print("  direction sizes:", ag["direction_sizes"])
    print("  u degrees (should all be 4):", sorted(set(ag["u_point_line_degrees"].values())))
    print("  #pairs covered (should be 36):", ag["pairs_total"])

    # Internal asserts (keep these lightweight and structural).
    assert c["triads_total"] == 45
    assert c["fiber_triads"] == 9
    assert c["affine_triads"] == 36
    assert c["u_points"] == 9
    assert c["u_lines"] == 12
    assert c["u_line_directions"] == 4
    assert set(ag["direction_sizes"].values()) == {3}
    assert sorted(set(ag["u_point_line_degrees"].values())) == [4]
    assert ag["pairs_total"] == 36

    hg = res["hessian_group"]
    print("\nHeisenberg⋊SL(2,3) symmetry on H27")
    print("-" * 30)
    print("  order:", hg["order"])
    print("  orbit size:", hg["orbit_size"])
    print("  triads invariant:", hg["triads_invariant"])

    assert hg["order"] == 648
    assert hg["transitive"] is True
    assert hg["triads_invariant"] is True

    ag = res["affine_group"]
    print("\nAffine Heisenberg⋊GL(2,3) symmetry on H27")
    print("-" * 30)
    print("  order:", ag["order"])
    print("  point stabilizer order:", ag["point_stabilizer_order"])
    print("  projective subgroup order:", ag["projective_subgroup_order"])
    print("  structure:", ag["structure_h27"])
    print("  full 45 triads invariant:", ag["triads_invariant"])

    assert ag["order"] == 1296
    assert ag["point_stabilizer_order"] == 48
    assert ag["projective_subgroup_order"] == 648
    assert ag["projective_subgroup_index"] == 2
    assert ag["fiber_triads_invariant"] is True
    assert ag["affine_triads_invariant"] is True
    assert ag["triads_invariant"] is True

    print("\nALL CHECKS PASSED ✓")


if __name__ == "__main__":
    main()
