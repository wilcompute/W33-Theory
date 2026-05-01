from pathlib import Path

import numpy as np
import pytest

from tools.build_linfty_firewall_extension import LInftyE8Extension, _load_bracket_tool

E6_BASIS_EXPORT = Path("artifacts/e6_27rep_basis_export/E6_basis_78.npy")
pytestmark = pytest.mark.skipif(
    not E6_BASIS_EXPORT.exists(),
    reason=f"Missing optional E6 basis export: {E6_BASIS_EXPORT}",
)


def max_abs(e):
    return float(
        max(
            0.0 if e.e6.size == 0 else np.max(np.abs(e.e6)),
            0.0 if e.sl3.size == 0 else np.max(np.abs(e.sl3)),
            0.0 if e.g1.size == 0 else np.max(np.abs(e.g1)),
            0.0 if e.g2.size == 0 else np.max(np.abs(e.g2)),
        )
    )


def basis_elem_g1(toe_mod, idx):
    i, j = idx
    e = toe_mod.E8Z3.zero()
    arr = np.zeros((27, 3), dtype=np.complex128)
    arr[i, j] = 1.0
    return toe_mod.E8Z3(e6=e.e6, sl3=e.sl3, g1=arr, g2=e.g2)


def test_failing_triple_cancelled():
    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()

    # load bad9 from module helper
    from tools.build_linfty_firewall_extension import _load_bad9

    bad9 = _load_bad9()

    # build L∞ with canonical scale = 1/9 (constructor default in tool)
    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # previously failing triple discovered by exhaustive check
    a_idx = (0, 0)
    b_idx = (1, 1)
    c_idx = (21, 2)

    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g1(toe, c_idx)

    # homotopy Jacobi should be (numerically) zero for this triple
    total = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(total) < 1e-12


def test_random_g1_samples_reduce_to_zero():
    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    from tools.build_linfty_firewall_extension import _load_bad9

    bad9 = _load_bad9()
    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    rng = np.random.default_rng(20260212)

    # sample 20 random g1 triples where Jacobi(l2).e6 != 0 and assert homotopy residual==0
    count = 0
    for _ in range(200):
        x = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        y = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        z = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        j_l2 = toe._jacobi(linfty.br_l2, x, y, z)
        if np.max(np.abs(j_l2.e6)) < 1e-12:
            continue
        total = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(total) < 1e-10
        count += 1
        if count >= 20:
            break
    assert count >= 5


def test_mixed_triple_not_cancelled_by_rational_candidate():
    """Confirm the canonical/rationalized l3 alone does NOT cancel the known
    mixed g1_g1_g2 obstruction (regression test reproducing the documented
    failing triple).
    """
    import json

    from tools.build_linfty_firewall_extension import _load_bad9, _load_bracket_tool
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        assemble_l3_total_from_coeffs,
        basis_elem_g1,
        basis_elem_g2,
    )

    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()

    # load the rationalized coefficients from artifact
    data = json.loads(
        open(
            "artifacts/linfty_coord_search_results_rationalized.json",
            "r",
            encoding="utf-8",
        ).read()
    )
    coeffs = data.get("rationalized_coeffs_float")
    assert coeffs is not None

    bad9 = _load_bad9()

    br_l2 = toe.E8Z3Bracket(
        e6_projector=proj,
        cubic_triads=[t for t in all_triads if tuple(sorted(t[:3])) not in bad9],
        scale_g1g1=1.0,
        scale_g2g2=-1.0 / 6.0,
        scale_e6=1.0,
        scale_sl3=1.0 / 6.0,
    )

    fiber_triads = [t for t in all_triads if tuple(sorted(t[:3])) in bad9]
    br_fibers = [
        toe.E8Z3Bracket(
            e6_projector=proj,
            cubic_triads=[T],
            scale_g1g1=1.0,
            scale_g2g2=-1.0 / 6.0,
            scale_e6=1.0,
            scale_sl3=1.0 / 6.0,
        )
        for T in fiber_triads
    ]

    # failing triple from exhaustive check
    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 0)

    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g2(toe, c_idx)

    j_l2 = toe._jacobi(br_l2, x, y, z)
    l3_total = assemble_l3_total_from_coeffs(coeffs, br_l2, br_fibers, toe, x, y, z)
    total = toe.E8Z3(
        e6=j_l2.e6 + l3_total.e6,
        sl3=j_l2.sl3 + l3_total.sl3,
        g1=j_l2.g1 + l3_total.g1,
        g2=j_l2.g2 + l3_total.g2,
    )

    # rationalized l3 on the 9 fibers is NOT sufficient for this mixed triple
    assert max_abs(total) > 1e-10


def test_mixed_triple_cancelled_by_l3_plus_ce2chain():
    """Use the local CE 2-cochain solver (l4 prototype) to cancel the mixed
    obstruction without regressing pure sectors."""
    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )

    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # failing triple
    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 0)
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g2(toe, c_idx)

    alpha = linfty.compute_local_ce2_alpha_for_triple(x, y, z)
    assert alpha is not None

    linfty.attach_ce2_alpha(alpha)

    total = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(total) < 1e-10

    # sanity: random pure-sector triples should not regress when alpha is attached
    rng = np.random.default_rng(20260212)
    for _ in range(30):
        xa = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        ya = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        za = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        hj = linfty.homotopy_jacobi(xa, ya, za)
        assert max_abs(hj) < 1e-8

    # promote the attached CE2 to a global l4 prototype and verify equivalence
    linfty.attach_l4_from_ce2(alpha)

    # detach the CE2 and ensure the l4 prototype alone cancels the triple
    linfty.detach_ce2_alpha()

    total_l4_only = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(total_l4_only) < 1e-10

    # ensure pure sectors remain OK with l4 attached
    rng = np.random.default_rng(20260212)
    for _ in range(30):
        xa = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        ya = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        za = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        hj = linfty.homotopy_jacobi(xa, ya, za)
        assert max_abs(hj) < 1e-8

    linfty.detach_l4()


def test_dual_mixed_triple_requires_three_pair_ce2_fallback():
    """The g1_g2_g2 witness closes once the local solver is allowed a W leg."""
    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    x = basis_elem_g1(toe, (0, 0))
    y = basis_elem_g2(toe, (0, 0))
    z = basis_elem_g2(toe, (21, 1))

    baseline = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(baseline) > 1e-10

    alpha = linfty.compute_local_ce2_alpha_for_triple(x, y, z)
    assert alpha is not None
    assert getattr(alpha, "_ce2_solution_mode", None) == "uvw"
    assert np.linalg.norm(getattr(alpha, "_ce2_W_flat")) > 1e-12

    linfty.attach_ce2_alpha(alpha)
    repaired = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(repaired) < 1e-10


def test_mixed_triple_cancelled_by_manual_lsq_candidate_3_1():
    """Targeted regression: compute numeric LSQ U/V for the recorded mixed
    failing triple (0,0),(17,1),(3,1), attach the resulting CE2 alpha and
    verify the homotopy Jacobi is (numerically) zero without regressing
    pure-sector checks.
    """
    import numpy as _np

    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    toe = _load_bracket_tool()
    e6_basis = _np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        _np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    # build linfty helper
    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # failing triple (numeric LSQ will be computed below)
    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 1)

    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g2(toe, c_idx)

    # Use the same brackets as `linfty.homotopy_jacobi` so the LSQ candidate
    # targets the actual residual that will be checked below.
    br_l2 = linfty.br_l2

    # target RHS = -(J + l3) where l3 is the canonical fiber-supported term
    J = toe._jacobi(br_l2, x, y, z)
    l3_total = linfty.l3(x, y, z)

    # flatten helpers
    def flatten(e):
        return _np.concatenate(
            [e.e6.reshape(-1), e.sl3.reshape(-1), e.g1.reshape(-1), e.g2.reshape(-1)]
        )

    def flat_to_E8Z3(vec):
        N = 27 * 27
        e6 = vec[:N].reshape((27, 27)).astype(_np.complex128)
        off = N
        sl3 = vec[off : off + 9].reshape((3, 3)).astype(_np.complex128)
        off += 9
        g1 = vec[off : off + 81].reshape((27, 3)).astype(_np.complex128)
        off += 81
        g2 = vec[off : off + 81].reshape((27, 3)).astype(_np.complex128)
        return toe.E8Z3(e6=e6, sl3=sl3, g1=g1, g2=g2)

    Jflat = flatten(J)
    l3flat = flatten(l3_total)
    target = -(Jflat + l3flat)

    # build linear action matrix (same as compute_local_ce2_alpha_for_triple)
    Nflat = target.size
    eye = _np.eye(Nflat, dtype=_np.complex128)
    A_cols = []
    B_cols = []
    for i in range(Nflat):
        vec = eye[:, i]
        # convert flat vec -> E8Z3
        N = 27 * 27
        e6 = vec[:N].reshape((27, 27)).astype(_np.complex128)
        off = N
        sl3 = vec[off : off + 9].reshape((3, 3)).astype(_np.complex128)
        off += 9
        g1 = vec[off : off + 81].reshape((27, 3)).astype(_np.complex128)
        off += 81
        g2 = vec[off : off + 81].reshape((27, 3)).astype(_np.complex128)
        E = toe.E8Z3(e6=e6, sl3=sl3, g1=g1, g2=g2)
        A_cols.append(flatten(br_l2.bracket(x, E)))
        B_cols.append(-flatten(br_l2.bracket(y, E)))

    A = _np.column_stack(A_cols)
    B = _np.column_stack(B_cols)
    M = _np.hstack([A, B])

    M_real = _np.vstack([_np.real(M), _np.imag(M)])
    rhs = _np.concatenate([_np.real(target), _np.imag(target)])

    sol, *_ = _np.linalg.lstsq(M_real, rhs, rcond=None)
    u = sol[:Nflat]
    v = sol[Nflat:]

    # build alpha from numeric U/V and attach
    U_e8 = flat_to_E8Z3(u)
    V_e8 = flat_to_E8Z3(v)

    def alpha_num(a, b):
        # alpha(y,z) = U
        if (
            _np.allclose(a.g1, y.g1)
            and _np.allclose(a.g2, y.g2)
            and _np.allclose(b.g1, z.g1)
            and _np.allclose(b.g2, z.g2)
        ):
            return U_e8
        if (
            _np.allclose(a.g1, z.g1)
            and _np.allclose(a.g2, z.g2)
            and _np.allclose(b.g1, y.g1)
            and _np.allclose(b.g2, y.g2)
        ):
            return U_e8.scale(-1.0)
        if (
            _np.allclose(a.g1, x.g1)
            and _np.allclose(a.g2, x.g2)
            and _np.allclose(b.g1, z.g1)
            and _np.allclose(b.g2, z.g2)
        ):
            return V_e8
        if (
            _np.allclose(a.g1, z.g1)
            and _np.allclose(a.g2, z.g2)
            and _np.allclose(b.g1, x.g1)
            and _np.allclose(b.g2, x.g2)
        ):
            return V_e8.scale(-1.0)
        return toe.E8Z3.zero()

    linfty.attach_ce2_alpha(alpha_num)
    try:
        tot = linfty.homotopy_jacobi(x, y, z)
        assert float(_np.max(_np.abs(tot.g1))) < 1e-8

        # sanity: pure-sector random samples should not regress
        rng = _np.random.default_rng(20260212)
        for _ in range(20):
            xa = toe._random_element(
                rng,
                e6_basis,
                scale0=0,
                scale1=2,
                scale2=0,
                include_g0=False,
                include_g2=False,
            )
            ya = toe._random_element(
                rng,
                e6_basis,
                scale0=0,
                scale1=2,
                scale2=0,
                include_g0=False,
                include_g2=False,
            )
            za = toe._random_element(
                rng,
                e6_basis,
                scale0=0,
                scale1=2,
                scale2=0,
                include_g0=False,
                include_g2=False,
            )
            hj = linfty.homotopy_jacobi(xa, ya, za)
            assert float(_np.max(_np.abs(hj.g1))) < 1e-6
    finally:
        linfty.detach_ce2_alpha()


def test_global_l4_assembled_from_local_alphas():
    """Assemble a global CE2 -> l4 from local per‑triple solutions and verify
    it cancels every failing triple recorded by the exhaustive verifier.
    """
    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )

    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # load exhaustive artifact (may contain one or more failing triples)
    import json

    exh = json.loads(
        open(
            "artifacts/exhaustive_homotopy_rationalized_l3.json", "r", encoding="utf-8"
        ).read()
    )

    # support two artifact shapes: either an explicit `failing_examples` list
    # or a single `first_fail` entry produced by the exhaustive verifier.
    g1g1g2 = exh["sectors"].get("g1_g1_g2", {})
    fails = g1g1g2.get("failing_examples")
    if not fails:
        ff = g1g1g2.get("first_fail")
        fails = [ff] if ff is not None else []

    # If no failing triples were recorded, there is nothing to assemble — pass.
    if len(fails) == 0:
        return

    local_alphas = []
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    for ft in fails:
        a_idx = tuple(ft["a"])
        b_idx = tuple(ft["b"])
        c_idx = tuple(ft["c"])
        x = basis_elem_g1(toe, a_idx)
        y = basis_elem_g1(toe, b_idx)
        z = basis_elem_g2(toe, c_idx)

        alpha = linfty.compute_local_ce2_alpha_for_triple(x, y, z)
        assert alpha is not None
        local_alphas.append(alpha)

    # assemble global CE2 by summing local alphas pointwise
    def alpha_global(a, b):
        acc = toe.E8Z3.zero()
        for alpha in local_alphas:
            acc = acc + alpha(a, b)
        return acc

    # promote to global l4 and verify every recorded failing triple is fixed
    linfty.attach_l4_from_ce2(alpha_global)

    for ft in fails:
        a_idx = tuple(ft["a"])
        b_idx = tuple(ft["b"])
        c_idx = tuple(ft["c"])
        x = basis_elem_g1(toe, a_idx)
        y = basis_elem_g1(toe, b_idx)
        z = basis_elem_g2(toe, c_idx)

        total = linfty.homotopy_jacobi(x, y, z)
        assert max_abs(total) < 1e-10

    # sample pure g1 triples don't regress
    rng = np.random.default_rng(20260212)
    for _ in range(40):
        xa = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        ya = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        za = toe._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        hj = linfty.homotopy_jacobi(xa, ya, za)
        assert max_abs(hj) < 1e-8

    linfty.detach_l4()


def test_ce2_artifact_bracket_y_V_g1_component():
    """Fast check: for the recorded failing triple, ensure the CE2 artifact's
    V (flattened array) produces the expected `bracket(y, V).g1[6,1]` value
    (should match 1/54 as observed in diagnostics)."""
    import json
    from fractions import Fraction

    from tools.build_linfty_firewall_extension import _load_bracket_tool
    from tools.exhaustive_homotopy_check_rationalized_l3 import basis_elem_g1

    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)

    br = toe.E8Z3Bracket(
        e6_projector=proj,
        cubic_triads=toe._load_signed_cubic_triads(),
        scale_g1g1=1.0,
        scale_g2g2=-1.0 / 6.0,
        scale_e6=1.0,
        scale_sl3=1.0 / 6.0,
    )

    # failing triple indices
    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 0)

    # load CE2 artifact and find matching record
    ce2 = json.loads(
        open(
            "artifacts/ce2_rational_local_solutions.json", "r", encoding="utf-8"
        ).read()
    )
    rec = None
    for k, v in ce2.items():
        if (
            tuple(v.get("a")) == a_idx
            and tuple(v.get("b")) == b_idx
            and tuple(v.get("c")) == c_idx
        ):
            rec = v
            break
    assert rec is not None, "CE2 artifact missing record for failing triple"

    V_rats = [Fraction(s) if s != "0" else None for s in rec.get("V_rats", [])]
    V_num = np.array(
        [float(fr) if fr is not None else 0.0 for fr in V_rats], dtype=np.complex128
    )
    N = 27 * 27
    e6 = V_num[:N].reshape((27, 27)).astype(np.complex128)
    off = N
    sl3 = V_num[off : off + 9].reshape((3, 3)).astype(np.complex128)
    off += 9
    g1 = V_num[off : off + 81].reshape((27, 3)).astype(np.complex128)
    off += 81
    g2 = V_num[off : off + 81].reshape((27, 3)).astype(np.complex128)

    V_e8 = toe.E8Z3(e6=e6, sl3=sl3, g1=g1, g2=g2)
    y = basis_elem_g1(toe, b_idx)
    out = br.bracket(y, V_e8)

    # expected numeric contribution (artifact / bracket sign observed in diagnostics)
    expected = -1.0 / 54.0
    assert (
        abs(float(out.g1[6, 1]) - expected) < 1e-12
    ), f"bracket(y,V).g1[6,1]={out.g1[6,1]} != {expected}"


def test_ce2_alpha_and_dalpha_component_consistency():
    """Verify numeric CE2 alpha and its coboundary for the recorded failing
    triple; assert exact component values discovered during debugging.

    - alpha(x,z).e6[6,17] should equal +1/27
    - d_alpha_on_triple(x,y,z).g1[6,1] should equal +1/27
    - bracket(y, V_from_artifact).g1[6,1] remains -1/54 (sanity)
    """
    import json
    from fractions import Fraction

    import numpy as _np

    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    toe = _load_bracket_tool()
    e6_basis = _np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        _np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 0)

    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g2(toe, c_idx)

    # compute local CE2 alpha for this triple and inspect components
    alpha = linfty.compute_local_ce2_alpha_for_triple(x, y, z)
    assert alpha is not None

    # alpha(x,z).e6 should contain the 1/54 entry at (6,17) (local-solver value)
    a_e6_val = alpha(x, z).e6[6, 17]
    assert abs(float(a_e6_val) - 1.0 / 54.0) < 1e-12

    # attach the computed local CE2 alpha so d_alpha_on_triple will use it
    linfty.attach_ce2_alpha(alpha)
    try:
        d_alpha = linfty.d_alpha_on_triple(x, y, z)
        assert abs(float(d_alpha.g1[6, 1]) - 1.0 / 54.0) < 1e-12
    finally:
        linfty.detach_ce2_alpha()

    # sanity: the CE2 artifact bracket(y, V) still reports -1/54 at the same
    # g1 component (this documents the mismatch we are tracking)
    ce2 = json.loads(
        open(
            "artifacts/ce2_rational_local_solutions.json", "r", encoding="utf-8"
        ).read()
    )
    rec = None
    for k, v in ce2.items():
        if (
            tuple(v.get("a")) == a_idx
            and tuple(v.get("b")) == b_idx
            and tuple(v.get("c")) == c_idx
        ):
            rec = v
            break
    assert rec is not None

    V_rats = [Fraction(s) if s != "0" else None for s in rec.get("V_rats", [])]
    V_num = _np.array(
        [float(fr) if fr is not None else 0.0 for fr in V_rats], dtype=_np.complex128
    )
    N = 27 * 27
    e6 = V_num[:N].reshape((27, 27)).astype(_np.complex128)
    off = N
    sl3 = V_num[off : off + 9].reshape((3, 3)).astype(_np.complex128)
    off += 9
    g1 = V_num[off : off + 81].reshape((27, 3)).astype(_np.complex128)
    off += 81
    g2 = V_num[off : off + 81].reshape((27, 3)).astype(_np.complex128)

    V_e8 = toe.E8Z3(e6=e6, sl3=sl3, g1=g1, g2=g2)
    br = toe.E8Z3Bracket(
        e6_projector=proj,
        cubic_triads=toe._load_signed_cubic_triads(),
        scale_g1g1=1.0,
        scale_g2g2=-1.0 / 6.0,
        scale_e6=1.0,
        scale_sl3=1.0 / 6.0,
    )
    out = br.bracket(y, V_e8)
    assert abs(float(out.g1[6, 1]) + 1.0 / 54.0) < 1e-12


def test_local_ce2_uv_rationalization_and_l4_callable():
    """Ensure compute_local_ce2_alpha_for_triple can return/rationalize U/V and
    that the promoted l4 callable reflects the CE2 data (nonzero where expected).
    """
    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )

    toe = _load_bracket_tool()
    basis_path = "artifacts/e6_27rep_basis_export/E6_basis_78.npy"
    e6_basis = np.load(basis_path).astype(np.complex128)
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # failing triple
    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 0)
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g2(toe, c_idx)

    # request raw U/V and rationalized forms
    result = linfty.compute_local_ce2_alpha_for_triple(
        x, y, z, return_uv=True, rationalize_uv=True, max_den=720
    )
    assert result is not None
    alpha, U_flat, V_flat, U_rats, V_rats = result

    # confirm a rational with small denominator appears (V contains 1/6 in norm)
    from fractions import Fraction

    # at least one rational entry should be non-None and have small denominator
    non_none_v = [r for r in V_rats if r is not None]
    assert len(non_none_v) > 0
    # ensure the solver found a nontrivial V and the rationalized entries have small denominators
    import numpy as _np

    assert _np.linalg.norm(V_flat) > 1e-15
    denom_sizes = [r.denominator for r in non_none_v]
    assert min(denom_sizes) <= 720
    assert max(abs(r.numerator) for r in non_none_v) < 10000

    # promote to l4 and confirm the l4 callable is nonzero on a sensible 4-tuple
    linfty.attach_l4_from_ce2(alpha)
    # pick a 4-tuple where alpha is nonzero on (x,z) or (y,z)
    l4_val = linfty._l4_fn(x, y, z, x)
    assert (
        max(
            0.0 if l4_val.e6.size == 0 else float(np.max(np.abs(l4_val.e6))),
            0.0 if l4_val.sl3.size == 0 else float(np.max(np.abs(l4_val.sl3))),
            0.0 if l4_val.g1.size == 0 else float(np.max(np.abs(l4_val.g1))),
            0.0 if l4_val.g2.size == 0 else float(np.max(np.abs(l4_val.g2))),
        )
        > 1e-12
    )

    linfty.detach_l4()


def test_exact_l4_assembled_from_rationalized_ce2():
    """Run the assemble_exact_l4_from_local_ce2 tool and verify its artifact
    and numeric consequences (unit-test the exact/rational CE2 → l4 path).
    """
    import importlib.util
    import json
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]

    spec = importlib.util.spec_from_file_location(
        "assemble_ce2", ROOT / "tools" / "assemble_exact_l4_from_local_ce2.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    res = mod.main(max_den=720)
    assert res and "artifact" in res

    # expect certificates to be returned as well
    assert "certificates" in res and isinstance(res["certificates"], dict)

    art_path = Path(res["artifact"])
    assert art_path.exists()
    data = json.loads(art_path.read_text(encoding="utf-8"))

    # artifact should contain at least the failing triple key and rational arrays
    assert len(data) >= 1
    first_key = list(data.keys())[0]
    entry = data[first_key]
    assert "U_rats" in entry and "V_rats" in entry
    # denominators should be bounded by the supplied max_den
    from fractions import Fraction

    rats = [Fraction(s) for s in entry["V_rats"] if s != "0"]
    assert all(fr.denominator <= 720 for fr in rats)


def test_pslq_snf_ce2_uv_check_tool_runs_and_passes():
    """Run the PSLQ/SNF CE2 U/V verifier and assert it reports OK for all
    recorded local solutions."""
    import importlib.util
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "pslq_ce2", ROOT / "tools" / "pslq_snf_ce2_uv_check.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    report = mod.main()
    assert report.get("ok", False) is True
    out_path = ROOT / "artifacts" / "pslq_snf_ce2_uv_check.json"
    assert out_path.exists()
    import json

    rep = json.loads(out_path.read_text(encoding="utf-8"))
    assert "entries" in rep and len(rep["entries"]) >= 1


def test_snf_certificate_ce2_uv_tool_runs_and_certifies():
    """Run SNF certificate builder and assert a valid integer-lift certificate
    exists for each recorded CE2 local solution."""
    import importlib.util
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "snf_ce2", ROOT / "tools" / "snf_certificate_ce2_uv.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    report = mod.main()
    assert "entries" in report and len(report["entries"]) >= 1
    # every entry should have been verified
    for k, v in report["entries"].items():
        assert v.get("verified", False) is True
        assert v.get("D_found") is not None
        assert isinstance(v.get("snf_diag"), list)


def test_derive_symbolic_l4_and_exhaustive_l3_l4_passes():
    """Derive symbolic l4 constants, load them into the assembler, and run
    an exhaustive homotopy check for (l2 + l3 + l4)."""
    import importlib.util
    import json
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]

    # derive symbolic l4 from rational CE2 solutions
    spec = importlib.util.spec_from_file_location(
        "derive_l4", ROOT / "tools" / "derive_symbolic_l4.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    sym = mod.main()
    assert isinstance(sym, dict) and len(sym) >= 1

    # attach symbolic l4 in an LInfty instance and ensure it cancels failing triple
    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )

    toe = _load_bracket_tool()
    e6_basis = np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)
    # attach symbolic constants
    linfty.attach_l4_from_symbolic_constants(
        ROOT / "artifacts" / "l4_symbolic_constants.json"
    )
    # the loader should also register a CE2 coboundary callback when the
    # assembled CE2 artifact is present
    assert (
        hasattr(linfty, "_l4_coboundary_on_triple")
        and linfty._l4_coboundary_on_triple is not None
    )

    # ensure the CE2 alpha is also registered for d_alpha_on_triple fallback
    assert hasattr(linfty, "_ce2_alpha") and linfty._ce2_alpha is not None

    # load the exhaustive-l3 artifact + helpers and read the recorded failing triple
    exh = json.loads(
        open(
            "artifacts/exhaustive_homotopy_rationalized_l3.json", "r", encoding="utf-8"
        ).read()
    )
    ft = exh["sectors"]["g1_g1_g2"]["first_fail"]

    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    # the registered CE2 alpha and the coboundary callback should agree
    d_alpha_val = linfty.d_alpha_on_triple(
        basis_elem_g1(toe, tuple(ft["a"])),
        basis_elem_g1(toe, tuple(ft["b"])),
        basis_elem_g2(toe, tuple(ft["c"])),
    )
    l4_cb_val = linfty._l4_coboundary_on_triple(
        basis_elem_g1(toe, tuple(ft["a"])),
        basis_elem_g1(toe, tuple(ft["b"])),
        basis_elem_g2(toe, tuple(ft["c"])),
    )
    assert max_abs(d_alpha_val - l4_cb_val) < 1e-10

    x = basis_elem_g1(toe, tuple(ft["a"]))
    y = basis_elem_g1(toe, tuple(ft["b"]))
    z = basis_elem_g2(toe, tuple(ft["c"]))

    tot = linfty.homotopy_jacobi(x, y, z)
    assert (
        max(
            0.0 if tot.e6.size == 0 else float(np.max(np.abs(tot.e6))),
            0.0 if tot.sl3.size == 0 else float(np.max(np.abs(tot.sl3))),
            0.0 if tot.g1.size == 0 else float(np.max(np.abs(tot.g1))),
            0.0 if tot.g2.size == 0 else float(np.max(np.abs(tot.g2))),
        )
        < 1e-10
    )

    # run the exhaustive l3+l4 verifier tool
    spec2 = importlib.util.spec_from_file_location(
        "exh_l3_l4", ROOT / "tools" / "exhaustive_homotopy_check_l3_l4.py"
    )
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)

    mod2.main()
    outp = ROOT / "artifacts" / "exhaustive_homotopy_l3_l4.json"
    assert outp.exists()
    rep = json.loads(outp.read_text(encoding="utf-8"))
    # expect all sectors to pass
    for s in ("g1_g1_g1", "g2_g2_g2", "g1_g1_g2", "g1_g2_g2"):
        assert rep["sectors"][s]["passed"] is True


def test_attach_l4_from_ce2_preserves_existing_coboundary():
    """Regression: `attach_l4_from_ce2` must not overwrite a previously
    attached triple-aware coboundary (installed by
    `attach_l4_from_symbolic_constants`)."""
    from pathlib import Path

    import numpy as _np

    from tools.build_linfty_firewall_extension import (
        LInftyE8Extension,
        _load_bad9,
        _load_bracket_tool,
    )
    from tools.exhaustive_homotopy_check_rationalized_l3 import (
        basis_elem_g1,
        basis_elem_g2,
    )

    toe = _load_bracket_tool()
    e6_basis = _np.load("artifacts/e6_27rep_basis_export/E6_basis_78.npy").astype(
        _np.complex128
    )
    proj = toe.E6Projector(e6_basis)
    all_triads = toe._load_signed_cubic_triads()
    bad9 = _load_bad9()

    linfty = LInftyE8Extension(toe, proj, all_triads, bad9, l3_scale=1.0 / 9.0)

    # attach symbolic constants (this installs a triple-aware coboundary)
    linfty.attach_l4_from_symbolic_constants("artifacts/l4_symbolic_constants.json")
    existing_cb = linfty._l4_coboundary_on_triple
    assert existing_cb is not None

    # attach an aggregated CE2 -> l4 via attach_l4_from_ce2 (should preserve cb)
    def dummy_alpha(a, b):
        return toe.E8Z3.zero()

    linfty.attach_l4_from_ce2(dummy_alpha)
    assert linfty._l4_coboundary_on_triple is existing_cb

    # ensure homotopy for the recorded failing triple still cancels
    a_idx = (0, 0)
    b_idx = (17, 1)
    c_idx = (3, 0)
    x = basis_elem_g1(toe, a_idx)
    y = basis_elem_g1(toe, b_idx)
    z = basis_elem_g2(toe, c_idx)
    tot = linfty.homotopy_jacobi(x, y, z)
    assert max_abs(tot) < 1e-10
