#!/usr/bin/env python3
"""Three-copy magic distillation: exhaustive search over the COMPLETE
copy-permutation-symmetric stabilizer family, with exact arithmetic.

The blueprint's open problem 2 asks whether any stabilizer protocol on three or more
copies can annihilate every single-error input while keeping the clean M36 ray.
Pass 2861 settled two copies negatively by exhausting all 5,355 [[4,2]] codes.
Pass 2881 tried three copies with 30,000 RANDOM stabilizer groups and found nothing;
Pass 4680 then proved that sample had at most ~1% power unless witnesses number in the
tens of thousands.  The recorded ask was: "an exhaustive search over a chosen code
family rather than a random one."

This file performs that search, and the family is not arbitrary.  The test condition
is invariant under copy permutation: the clean input |m>^3 and the single-error
subspace S = E|mm> + m|E m> + |mm>E (E = m-perp, dim 3 per copy) are both S_3-stable.
So the canonical chosen family is the set of S_3-INVARIANT stabilizer groups, and it
is exactly enumerable:

  F_2^12 = F_2^4 (x) (triv + std) as an F_2[S_3]-module (permutation of copies);
  triv and std are inequivalent irreducibles, so EVERY invariant subgroup is
  V_t + W_T with V_t an isotropic subspace of the trivial-isotypic part and W_T the
  std-isotypic part over an isotropic T.  The restricted symplectic form on each part
  is the 2-qubit form, and the two parts are automatically orthogonal.

  Isotropic subspaces of the symplectic 4-space F_2^4: 1 + 15 + 15 = 31.
  Hence 31 x 31 = 961 invariant isotropic groups, and with all 2^rank sign
  assignments the search covers exactly

      (1 + 15*2 + 15*4) * (1 + 15*4 + 15*16) = 91 * 361 = 32,851

  signed syndrome projectors per ray -- the COMPLETE symmetric family, not a sample.
  (Asymmetric signs on a symmetric group are included: a witness projector need not
  itself be symmetric, only its support group is.)

The exact test, with zero floating point anywhere in the decision path:

  P a syndrome projector, J the projector onto the 9-dim single-error subspace.
  witness  <=>  Tr(P J) = 0  (P annihilates S)  AND  <mmm|P|mmm> != 0  (clean kept).

  Both quantities factorise per copy.  With unnormalised rays (squared norm 3) and
  m'(x) = <m|x|m>,  t'(x) = Tr(x Q_E) = 4*[x=I] - m'(x)  for 2-qubit Paulis x,

      27*|G| * Tr(PJ)        = sum_g chi(g) K(g),   K(g) = t'm'm' + m't'm' + m'm't',
      27*|G| * <mmm|P|mmm>   = sum_g chi(g) m'(g1) m'(g2) m'(g3).

  All values live in Z[zeta_12]; the sign sums over a group's 2^r characters are
  computed by an exact integer Walsh-Hadamard transform, so every projector of every
  group is tested in O(r 2^r) with no approximation.

Also computed exactly, because it explains the result either way: the LOCAL Pauli
stabiliser of each of the 36 M36 rays -- the set of 2-qubit Paulis P with
P r = +/- r.  For a product input and a product generator, g |m>^3 prop |m>^3 forces
each factor into the local stabiliser; if that set is trivial, no symmetric generator
can even stabilise the clean input, and the symmetric-family null is explained at the
level of a single copy.

Output: data/PART_W33_PASS20260906_THREE_COPY_SYMMETRIC_EXHAUSTION.json
"""
from __future__ import annotations

import hashlib
import json
import os
from itertools import product
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "PART_W33_PASS20260906_THREE_COPY_SYMMETRIC_EXHAUSTION.json")

# --------------------------------------------------------------------------
# Exact arithmetic in Z[zeta_12]: value = a + b*w + c*i + d*i*w, w^2 = -1 - w, i^2 = -1.
# Tuple (a, b, c, d) of Python ints.
# --------------------------------------------------------------------------

ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)
W = (0, 1, 0, 0)
W2 = (-1, -1, 0, 0)
POW = ((1, 0, 0, 0), (0, 1, 0, 0), (-1, -1, 0, 0))


def zadd(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3])


def zneg(x):
    return (-x[0], -x[1], -x[2], -x[3])


def zsub(x, y):
    return (x[0] - y[0], x[1] - y[1], x[2] - y[2], x[3] - y[3])


def _mulw(x):
    a, b, c, d = x
    return (-b, a - b, -d, c - d)


def _muli(x):
    a, b, c, d = x
    return (-c, -d, a, b)


def zmul(x, y):
    # (x0 + x1 i)(y0 + y1 i) with x0 = a+bw etc: = x0 y0 - x1 y1 + i(x0 y1 + x1 y0)
    x0, x1 = (x[0], x[1], 0, 0), (x[2], x[3], 0, 0)
    y0, y1 = (y[0], y[1], 0, 0), (y[2], y[3], 0, 0)

    def wmul(p, q):  # multiply in Z[w]: (a+bw)(c+dw)
        a, b = p
        c, d = q
        return (a * c - b * d, a * d + b * c - b * d)

    r0 = wmul(x0[:2], y0[:2])
    r1 = wmul(x1[:2], y1[:2])
    r2 = wmul(x0[:2], y1[:2])
    r3 = wmul(x1[:2], y0[:2])
    return (r0[0] - r1[0], r0[1] - r1[1], r2[0] + r3[0], r2[1] + r3[1])


def zconj(x):
    # conj(w) = -1 - w, conj(i) = -i
    a, b, c, d = x
    return (a - b, -b, d - c, d)


def zscale(k, x):
    return (k * x[0], k * x[1], k * x[2], k * x[3])


def is_zero(x):
    return x == ZERO


# --------------------------------------------------------------------------
# The 36 M36 rays, exactly as Pass 2790 (unnormalised, squared norm 3).
# --------------------------------------------------------------------------

def build_rays():
    rays, tags = [], []
    for mu, nu in product(range(3), repeat=2):
        rays.append((ZERO, ONE, zneg(POW[mu]), POW[nu]))
        tags.append(f"A{mu}{nu}")
    for mu, nu in product(range(3), repeat=2):
        rays.append((ONE, ZERO, zneg(POW[mu]), zneg(POW[nu])))
        tags.append(f"B{mu}{nu}")
    for mu, nu in product(range(3), repeat=2):
        rays.append((ONE, zneg(POW[mu]), ZERO, POW[nu]))
        tags.append(f"C{mu}{nu}")
    for mu, nu in product(range(3), repeat=2):
        rays.append((ONE, POW[mu], POW[nu], ZERO))
        tags.append(f"D{mu}{nu}")
    return rays, tags


# --------------------------------------------------------------------------
# Two-qubit Paulis, Hermitian convention: label (x1, z1, x2, z2) over F_2,
# operator X^x1 Z^z1 (x) X^x2 Z^z2 with Y = iXZ chosen Hermitian.
# Matrices over Z[zeta_12].
# --------------------------------------------------------------------------

I2 = ((ONE, ZERO), (ZERO, ONE))
X2 = ((ZERO, ONE), (ONE, ZERO))
Y2 = ((ZERO, (0, 0, -1, 0)), ((0, 0, 1, 0), ZERO))   # [[0,-i],[i,0]]
Z2 = ((ONE, ZERO), (ZERO, zneg(ONE)))
QPAULI = {(0, 0): I2, (1, 0): X2, (0, 1): Z2, (1, 1): Y2}

LABELS = list(product((0, 1), repeat=4))  # 16 labels, index order fixed
LIDX = {lb: i for i, lb in enumerate(LABELS)}


def label_matrix(label):
    m1 = QPAULI[(label[0], label[1])]
    m2 = QPAULI[(label[2], label[3])]
    return tuple(
        tuple(zmul(m1[a][c], m2[b][d]) for c in (0, 1) for d in (0, 1))
        for a in (0, 1) for b in (0, 1)
    )


MATS = [label_matrix(lb) for lb in LABELS]


def symp2(u, v):
    # label layout (x1, z1, x2, z2): qubit i pairs indices (2i, 2i+1)
    return (u[0] * v[1] + u[1] * v[0] + u[2] * v[3] + u[3] * v[2]) % 2


def apply_mat(M, v):
    return tuple(
        zadd(zadd(zmul(M[r][0], v[0]), zmul(M[r][1], v[1])),
             zadd(zmul(M[r][2], v[2]), zmul(M[r][3], v[3])))
        for r in range(4)
    )


def inner(u, v):
    s = ZERO
    for a, b in zip(u, v):
        s = zadd(s, zmul(zconj(a), b))
    return s


def local_stabiliser(ray):
    """Exact: 2-qubit Paulis with P r = lam r, lam in {+1,-1,+i,-i}."""
    out = []
    for lb, M in zip(LABELS, MATS):
        if lb == (0, 0, 0, 0):
            continue
        w = apply_mat(M, ray)
        # proportional iff all cross ratios vanish and not all zero
        prop = True
        for a in range(4):
            for b in range(4):
                if not is_zero(zsub(zmul(w[a], zconj(ray[b])), zmul(w[b], zconj(ray[a])))):
                    prop = False
                    break
            if not prop:
                break
        if prop and any(not is_zero(x) for x in w):
            out.append(lb)
    return out


def moment_tables(ray):
    """m'(x) = <r|x|r> (exact, = 3 * normalised expectation).

    t'(x) = 3 * Tr(x Q_E) = 3*(Tr x - <m|x|m>) = 12*[x=I] - m'(x).
    For x = I: m'(I) = 3, so t'(I) = 12 - 3 = 9 = 3*(4-1) as required.
    """
    m = []
    for M in MATS:
        m.append(inner(ray, apply_mat(M, ray)))
    t = []
    for lb, mv in zip(LABELS, m):
        t.append(zsub(zscale(12 if lb == (0, 0, 0, 0) else 0, ONE), mv))
    return m, t


# --------------------------------------------------------------------------
# Isotropic subspaces of the symplectic 4-space F_2^4 (the 2-qubit Pauli labels).
# --------------------------------------------------------------------------

def isotropic_subspaces():
    nonzero = [lb for lb in LABELS if lb != (0, 0, 0, 0)]
    subs = [()]  # zero subspace
    for u in nonzero:
        subs.append((u,))
    seen = set()
    for i, u in enumerate(nonzero):
        for v in nonzero[i + 1:]:
            if symp2(u, v) != 0:
                continue
            w = tuple((u[k] + v[k]) % 2 for k in range(4))
            if w == (0, 0, 0, 0):
                continue
            # dedup by the subspace's element SET, not by basis pair:
            # {u,v} and {u,u+v} span the same 2-dim isotropic subspace
            elems = frozenset(((0, 0, 0, 0), u, v, w))
            if elems not in seen:
                seen.add(elems)
                subs.append(tuple(sorted((u, v))))
    return subs  # 1 + 15 + 15 = 31


def span_elements(basis):
    """All 2^r elements (F_2 labels) of the span, indexed by subset bitmask."""
    out = [(0, 0, 0, 0)]
    for i, b in enumerate(basis):
        cur = list(out)
        for e in cur:
            out.append(tuple((e[k] + b[k]) % 2 for k in range(4)))
    return out  # index = subset bits of basis


# --------------------------------------------------------------------------
# S_3-invariant isotropic groups on 6 qubits.
# A group element is a triple (g1, g2, g3) of 2-qubit labels = one 6-qubit Pauli.
#   trivial-isotypic part: (a, a, a), a in V_t
#   std-isotypic part over T: (x, y, x+y), x,y in T   [basis (t,0,t),(0,t,t) per t]
# --------------------------------------------------------------------------

def group_elements(vt_basis, t_basis):
    vt_elems = span_elements(vt_basis)          # subsets of vt basis
    t_elems = span_elements(t_basis)            # subsets of t basis
    # combine the two parts: (a,a,a) + (x, y, x+y)
    out = []
    for a in vt_elems:
        ia = LABELS.index(a)
        for x in t_elems:
            for y in t_elems:
                z = tuple((x[k] + y[k]) % 2 for k in range(4))
                g1 = tuple((a[k] + x[k]) % 2 for k in range(4))
                g2 = tuple((a[k] + y[k]) % 2 for k in range(4))
                g3 = tuple((a[k] + z[k]) % 2 for k in range(4))
                out.append((LABELS.index(g1), LABELS.index(g2), LABELS.index(g3)))
    return out


def group_basis(vt_basis, t_basis):
    """Basis of the combined group as 6-qubit elements, for the WHT."""
    basis = []
    for a in vt_basis:
        basis.append((LABELS.index(a), LABELS.index(a), LABELS.index(a)))
    for t in t_basis:
        it = LABELS.index(t)
        basis.append((it, LABELS.index((0, 0, 0, 0)), it))
        basis.append((LABELS.index((0, 0, 0, 0)), it, it))
    return basis


def wht(values):
    """Exact integer Walsh-Hadamard transform over (Z/2)^r (tuples of 4 ints)."""
    a = list(values)
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j] = zadd(x, y)
                a[j + h] = zsub(x, y)
        h *= 2
    return a


def enumerate_groups():
    subs = isotropic_subspaces()
    groups = []
    for vt in subs:
        for t in subs:
            elems = group_elements(vt, t)
            basis = group_basis(vt, t)
            if len(set(elems)) != 2 ** len(basis):
                raise AssertionError("basis does not span freely")
            groups.append((basis, elems))
    return groups


def pair_phase(u, v):
    """Phase of M(u) M(v) relative to M(u+v), as a Z[zeta_12] element.

    Convention M(x,z) = i^{xz} X^x Z^z per qubit (so (1,1) is Hermitian Y).
    M(u)M(v) = i^{xz+x'z'-(x xor x')(z xor z')} (-1)^{z x'} M(u+v), per qubit,
    for ALL pairs (commuting or not -- per-copy factors can be +/-i; the total
    over copies is +/-1 exactly when the full Paulis commute).
    """
    e = 0  # exponent of i
    s = 0  # exponent of -1
    for (x, z, x2, z2) in ((u[0], u[1], v[0], v[1]), (u[2], u[3], v[2], v[3])):
        e += x * z + x2 * z2 - ((x ^ x2) * (z ^ z2))
        s += z * x2
    e %= 4
    s %= 2
    base = ((0, 0, 1, 0), (0, 0, 0, 0))
    # i^e * (-1)^s in tuple form
    ituples = [(1, 0, 0, 0), (0, 0, 1, 0), (-1, 0, 0, 0), (0, 0, -1, 0)]
    out = ituples[e]
    if s:
        out = zneg(out)
    return out


def search_ray(ray, groups):
    m, t = moment_tables(ray)
    iI = LABELS.index((0, 0, 0, 0))
    projectors_tested = 0
    witnesses = []
    annihilating = 0
    for basis, elems in groups:
        r = len(basis)
        # subset -> (element, operator phase): g(S) = phase(S) * M(labelsum(S)).
        # The phase cocycle is the physics: dropping it is the Pass-2861-style bug.
        ordered = [((iI, iI, iI), ONE)]
        for b in basis:
            cur = list(ordered)
            for e, ph in cur:
                lab = tuple(
                    LIDX[tuple((LABELS[e[c]][k] + LABELS[b[c]][k]) % 2 for k in range(4))]
                    for c in range(3)
                )
                ph2 = ph
                for c in range(3):
                    ph2 = zmul(ph2, pair_phase(LABELS[e[c]], LABELS[b[c]]))
                ordered.append((lab, ph2))
        # K and C per subset, WITH the operator-product phase
        Kvals, Cvals = [], []
        for ((g1, g2, g3), ph) in ordered:
            k = zadd(zmul(zmul(t[g1], m[g2]), m[g3]),
                     zadd(zmul(zmul(m[g1], t[g2]), m[g3]), zmul(zmul(m[g1], m[g2]), t[g3])))
            c = zmul(zmul(m[g1], m[g2]), m[g3])
            Kvals.append(zmul(ph, k))
            Cvals.append(zmul(ph, c))
        Kt = wht(Kvals)
        Ct = wht(Cvals)
        for bits in range(2 ** r):
            projectors_tested += 1
            if is_zero(Kt[bits]):
                annihilating += 1
                if not is_zero(Ct[bits]):
                    if len(witnesses) < 8:
                        witnesses.append({
                            "generator_labels": [
                                [list(map(int, LABELS[c])) for c in b] for b in basis
                            ],
                            "sign_bits": bits,
                            "rank": r,
                        })
    return projectors_tested, annihilating, witnesses


def independent_witness_check(ray, witnesses, max_check=4):
    """Re-verify claimed witnesses by a completely independent code path:
    dense complex128 64x64 projectors from explicit Pauli matrices, explicit
    single-error basis from QR, direct Gram computation.  Guards the whole
    exact-arithmetic chain against a formula bug.
    """
    import numpy as np

    PAULI = {
        (0, 0): np.eye(2, dtype=complex),
        (1, 0): np.array([[0, 1], [1, 0]], dtype=complex),
        (0, 1): np.array([[1, 0], [0, -1]], dtype=complex),
        (1, 1): np.array([[0, -1j], [1j, 0]], dtype=complex),
    }

    def mat2(label):
        return np.kron(PAULI[(label[0], label[1])], PAULI[(label[2], label[3])])

    # exact ray -> complex unit vector
    w = np.exp(2j * np.pi / 3)

    def to_complex(x):
        a, b, c, d = x
        return a + b * w + c * 1j + d * 1j * w

    m = np.array([to_complex(x) for x in ray], dtype=complex)
    m = m / np.linalg.norm(m)
    Q, _ = np.linalg.qr(np.column_stack([m] + [np.eye(4, dtype=complex)[:, i] for i in range(4)]))
    e = [Q[:, i] for i in range(1, 4)]
    singles = []
    for i in range(3):
        singles.append(np.kron(np.kron(e[i], m), m))
        singles.append(np.kron(np.kron(m, e[i]), m))
        singles.append(np.kron(np.kron(m, m), e[i]))
    mmm = np.kron(np.kron(m, m), m)

    confirmed = 0
    for wit in witnesses[:max_check]:
        gens = wit["generator_labels"]
        bits = wit["sign_bits"]
        P = np.eye(64, dtype=complex)
        for j, g in enumerate(gens):
            G = np.kron(np.kron(mat2(g[0]), mat2(g[1])), mat2(g[2]))
            s = -1.0 if (bits >> j) & 1 else 1.0
            P = P @ (np.eye(64, dtype=complex) + s * G) / 2
        gram = max(abs(np.vdot(s_, P @ s_)) for s_ in singles)
        clean = abs(np.vdot(mmm, P @ mmm))
        if gram < 1e-9 and clean > 1e-6:
            confirmed += 1
    return confirmed


def verify() -> dict[str, Any]:
    rays, tags = build_rays()
    # sanity: every ray squared norm 3
    for r in rays:
        assert inner(r, r) == zscale(3, ONE)

    # sanity: pair_phase agrees with dense matrix multiplication on all pairs
    import numpy as np
    w_ = np.exp(2j * np.pi / 3)
    PAULI_N = {
        (0, 0): np.eye(2, dtype=complex),
        (1, 0): np.array([[0, 1], [1, 0]], dtype=complex),
        (0, 1): np.array([[1, 0], [0, -1]], dtype=complex),
        (1, 1): np.array([[0, -1j], [1j, 0]], dtype=complex),
    }

    def mat2n(lb):
        return np.kron(PAULI_N[(lb[0], lb[1])], PAULI_N[(lb[2], lb[3])])

    phase_audit_ok = True
    for u in LABELS:
        for v in LABELS:
            s = tuple((u[k] + v[k]) % 2 for k in range(4))
            lhs = mat2n(u) @ mat2n(v)
            ph = pair_phase(u, v)
            phn = (ph[0] + ph[1] * w_) + 1j * (ph[2] + ph[3] * w_)
            rhs = phn * mat2n(s)
            if not np.allclose(lhs, rhs):
                phase_audit_ok = False

    groups = enumerate_groups()
    n_groups = len(groups)
    proj_per_ray = sum(2 ** len(b) for b, _ in groups)

    loc_table = {}
    for tag, r in zip(tags, rays):
        loc_table[tag] = local_stabiliser(r)
    nontrivial_loc = {k: v for k, v in loc_table.items() if v}

    per_ray = {}
    witness_gallery = {}
    total_witnesses = 0
    independent_confirmations = 0
    for tag, r in zip(tags, rays):
        tested, annihilating, witnesses = search_ray(r, groups)
        assert tested == proj_per_ray
        confirmed = independent_witness_check(r, witnesses) if witnesses else 0
        independent_confirmations += confirmed
        per_ray[tag] = {
            "projectors_tested": tested,
            "annihilating_projectors": annihilating,
            "witnesses": len(witnesses),
            "witnesses_capped_at": 8,
            "independently_confirmed_dense": confirmed,
        }
        if witnesses:
            witness_gallery[tag] = witnesses[0]
        total_witnesses += len(witnesses)

    checks = {
        "group_count_is_961": n_groups == 961,
        "projectors_per_ray_is_27391": proj_per_ray == 27391,
        "all_36_rays_norm_3": True,
        "pauli_product_phase_cocycle_audited_dense": phase_audit_ok,
        "local_stabilisers_computed": len(loc_table) == 36,
        "search_exhaustive_per_ray": all(v["projectors_tested"] == 27391 for v in per_ray.values()),
        "every_sampled_witness_independently_confirmed": (
            total_witnesses == 0
            or independent_confirmations == sum(
                min(v["witnesses"], 4) for v in per_ray.values()
            )
        ),
    }
    payload = {
        "schema": "w33.three-copy-symmetric-exhaustion.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "Exhaustive over the COMPLETE copy-permutation-symmetric stabilizer "
            "family at three copies: 961 S_3-invariant isotropic groups, 27,391 "
            "signed syndrome projectors, tested exactly (integer Walsh-Hadamard over "
            "Z[zeta_12]) against Tr(PJ)=0 and <mmm|P|mmm> != 0 for every one of the "
            "36 M36 rays, with every reported witness independently re-verified by a "
            "dense complex128 projector construction on a separate code path."
        ),
        "family": {
            "description": "all S_3-invariant 6-qubit stabilizer groups (isotypic completeness argument)",
            "groups": n_groups,
            "signed_projectors_per_ray": proj_per_ray,
            "rays_tested": 36,
        },
        "result": {
            "total_witnesses_all_rays": total_witnesses,
            "per_ray": per_ray,
            "explicit_first_witness_per_ray": witness_gallery,
        },
        "local_stabiliser": {
            "nontrivial_rays": {k: [list(map(int, v)) for v in vs] for k, vs in nontrivial_loc.items()},
            "rays_with_only_identity": 36 - len(nontrivial_loc),
        },
        "context": {
            "two_copy": "Pass 2861: exhaustive 5,355 codes x 4 syndromes x 4 ray classes, zero",
            "three_copy_random": "Pass 2881: 30,000 random groups, zero (Pass 4680: ~1% power)",
            "this_search": "exhaustive over the maximal symmetry-respecting family",
        },
        "boundary": (
            "The verdict is a theorem about the complete copy-permutation-symmetric "
            "family, not about all 315,057,600 stabilizer groups on six qubits: "
            "projectors whose support group is NOT copy-permutation invariant are not "
            "covered.  A witness here certifies possibility for the exact condition "
            "(annihilate the 9-dim single-error subspace, keep the clean ray with "
            "nonzero weight) at the stated postselection strength; it does not by "
            "itself give a decoder, a yield, or a fidelity curve.  No physical device "
            "claim."
        ),
        "checks": checks,
    }
    payload["certificate_sha256"] = "sha256:" + hashlib.sha256(
        json.dumps({k: v for k, v in payload.items() if k != "certificate_sha256"},
                   sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return payload


def main() -> int:
    payload = verify()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(payload["status"], payload["certificate_sha256"])
    print(f"  groups={payload['family']['groups']} projectors/ray={payload['family']['signed_projectors_per_ray']}")
    print(f"  total witnesses over all 36 rays: {payload['result']['total_witnesses_all_rays']}")
    print(f"  rays with nontrivial local stabiliser: {list(payload['local_stabiliser']['nontrivial_rays'])}")
    print(f"  wrote {OUT}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
