import importlib.util
import random

spec = importlib.util.spec_from_file_location(
    "the_exact_map", "exploration/THE_EXACT_MAP.py"
)
exact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact)


def _evaluate_line_rep(line_rep, sample):
    """Evaluate the cocycle sample against an explicit line representative list."""
    line_symp = [
        [(p1[0] * p2[1] - p2[0] * p1[1]) % 3 for p2 in line_rep] for p1 in line_rep
    ]
    pos_symp = [
        [
            line_symp[exact.pos_to_line_mog[i]][exact.pos_to_line_mog[j]]
            for j in range(12)
        ]
        for i in range(12)
    ]

    def symplectic_sign(c1, c2):
        total = 0
        for i in exact.support(c1):
            for j in exact.support(c2):
                total = (total + pos_symp[i][j]) % 3
        return 1 if total == 0 else (-1 if total == 1 else 1)

    cocycle_pass = 0
    cocycle_fail = 0
    zero = tuple([0] * 12)

    for a in sample[:15]:
        for b in sample[:15]:
            for c in sample[:15]:
                if a != b and b != c and a != c:
                    bc = tuple((b[i] + c[i]) % 3 for i in range(12))
                    ca = tuple((c[i] + a[i]) % 3 for i in range(12))
                    ab = tuple((a[i] + b[i]) % 3 for i in range(12))

                    if bc != zero and ca != zero and ab != zero:
                        s1 = symplectic_sign(a, bc) * symplectic_sign(b, c)
                        s2 = symplectic_sign(b, ca) * symplectic_sign(c, a)
                        s3 = symplectic_sign(c, ab) * symplectic_sign(a, b)

                        if s1 == s2 == s3:
                            cocycle_pass += 1
                        else:
                            cocycle_fail += 1

    return cocycle_pass, cocycle_fail


def test_line_rep_is_tuned_and_sample_cocycle_matches_expected():
    """Pin the canonical `line_rep` and verify the sampled cocycle pass/fail counts.

    This test is intentionally lightweight (uses the same 50→15 sampling THE_EXACT_MAP.py uses)
    and prevents accidental regressions to the tuned representatives.
    """
    expected = [
        (0, 2),
        (0, 0),
        (1, 1),
        (0, 0),
        (2, 2),
        (0, 1),
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 0),
        (2, 2),
    ]

    assert exact.line_rep == expected

    random.seed(42)
    sample = random.sample(exact.weight_6, 50)

    cocycle_pass, cocycle_fail = _evaluate_line_rep(exact.line_rep, sample)

    # Preserve determinism: ensure the total tested triples remains the same
    assert cocycle_pass + cocycle_fail == 2652
    assert (cocycle_pass, cocycle_fail) == (1743, 909)

    # Require sampled-cocycle does not regress: compare against the canonical baseline
    canon = [exact.canonical_point(l) for l in exact.F3_lines]
    base_pc, base_fc = _evaluate_line_rep(canon, sample)
    assert (base_pc, base_fc) == (843, 1809)
    assert cocycle_pass >= base_pc
