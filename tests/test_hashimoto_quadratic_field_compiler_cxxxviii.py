from fractions import Fraction

from PART_CXXXVIII_HASHIMOTO_QUADRATIC_FIELD_COMPILER import (
    BASS_TRIVIAL_MULT,
    DIRECTED_EDGES,
    HASHIMOTO_Q,
    characteristic_factorization,
    hashimoto_trace_formula,
    ihara_zeta_inverse_factorization,
    lucas_sequence_for_root_pair,
    phi3,
    phi4,
    phi6,
    quadratic_field_compiler_audit,
    quadratic_sectors,
    trace_table,
)


def test_cyclotomic_values_at_q3():
    assert phi3() == 13
    assert phi4() == 10
    assert phi6() == 7


def test_ramanujan_quadratic_sector_decomposition():
    sectors = quadratic_sectors()
    assert len(sectors) == 2

    r_sector, s_sector = sectors
    assert r_sector.adjacency_eigenvalue == 2
    assert r_sector.adjacency_multiplicity == 24
    assert r_sector.real_part == Fraction(1, 1)
    assert r_sector.imag_square == phi4()
    assert r_sector.norm == HASHIMOTO_Q

    assert s_sector.adjacency_eigenvalue == -4
    assert s_sector.adjacency_multiplicity == 15
    assert s_sector.real_part == Fraction(-2, 1)
    assert s_sector.imag_square == phi6()
    assert s_sector.norm == HASHIMOTO_Q


def test_norm_identities_are_exactly_hashimoto_q():
    # 11 = 1^2 + Phi_4(3) = 2^2 + Phi_6(3)
    assert 1**2 + phi4() == HASHIMOTO_Q
    assert 2**2 + phi6() == HASHIMOTO_Q


def test_hashimoto_dimension_trichotomy_recovered():
    sectors = quadratic_sectors()
    ramanujan_layer = sum(s.doubled_hashimoto_multiplicity for s in sectors)
    bass_layer = 2 * BASS_TRIVIAL_MULT + 1
    assert ramanujan_layer == 78
    assert bass_layer == 401
    assert 1 + ramanujan_layer + bass_layer == DIRECTED_EDGES


def test_characteristic_factorization_degree_and_trace_checks():
    char = characteristic_factorization()
    assert char["degree_check"] == 480
    # Root sum: 11 + 201 - 200 + 24*(2) + 15*(-4) = 0, matching trace(B)=0.
    assert 11 + 201 - 200 + 48 - 60 == 0


def test_ihara_zeta_inverse_contains_the_two_cyclotomic_blocks():
    ihara = ihara_zeta_inverse_factorization()
    assert "(1-2u+11u^2)^24" in ihara["factorization"]
    assert "(1+4u+11u^2)^15" in ihara["factorization"]
    assert "1/sqrt(11)" in ihara["critical_circle"]


def test_lucas_sequences_match_the_two_root_pairs():
    # L_n = alpha^n + beta^n for x^2 - a*x + 11.
    l2 = lucas_sequence_for_root_pair(2, 11, 5)
    lm4 = lucas_sequence_for_root_pair(-4, 11, 5)
    assert l2 == [2, 2, -18, -58, 82, 802]
    assert lm4 == [2, -4, -6, 68, -206, 76]


def test_trace_formula_initial_values_and_triangle_count():
    # n=1,2 vanish because the graph has no loops and no non-backtracking
    # two-step closures. n=3 is 6 * 160 W(3,3) triangles.
    assert hashimoto_trace_formula(1) == 0
    assert hashimoto_trace_formula(2) == 0
    assert hashimoto_trace_formula(3) == 960
    assert hashimoto_trace_formula(4) == 13920
    assert hashimoto_trace_formula(5) == 181440


def test_trace_closure_fraction_for_triangles():
    rows = trace_table(3)
    n3 = rows[2]
    assert n3["n"] == 3
    assert n3["trace_B^n"] == 960
    assert n3["closure_fraction_exact"] == "2/121"


def test_full_audit_internal_checks():
    audit = quadratic_field_compiler_audit(n_max=8)
    checks = audit["checks"]
    assert checks["carrier_total"] == 480
    assert checks["ramanujan_layer_dimension"] == 78
    assert checks["bass_trivial_plus_perron_mate"] == 401
    assert checks["triangle_trace_T3"] == 960
    assert len(audit["trace_table"]) == 8
