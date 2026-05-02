from PART_CLXXIII_EISENSTEIN_TORUS_MAP_BRIDGE import (
    Q,
    PHI6,
    eisenstein_norm,
    map_36_counts,
    map_63_counts,
    torus_map_rows,
    eisenstein_torus_map_bridge_audit,
)


def test_eisenstein_norm_sequence_from_pdf_bottom_maps():
    assert [eisenstein_norm(*p) for p in [(1, 0), (2, 0), (1, 1), (2, 1)]] == [1, 4, 3, 7]


def test_phi6_from_q_minus_one_one_norm():
    assert eisenstein_norm(Q - 1, 1) == PHI6 == 7
    assert eisenstein_norm(2, 1) == 7


def test_csaszar_and_szilassi_map_counts():
    assert map_36_counts(2, 1) == (7, 21, 14)
    assert map_63_counts(2, 1) == (14, 21, 7)


def test_dual_swap_and_euler_zero():
    cs = map_36_counts(2, 1)
    sz = map_63_counts(2, 1)
    assert cs[1] == sz[1] == 21
    assert cs[0] == sz[2]
    assert cs[2] == sz[0]
    assert cs[0] - cs[1] + cs[2] == 0
    assert sz[0] - sz[1] + sz[2] == 0


def test_rows_include_all_pdf_bottom_map_rows():
    rows = torus_map_rows()
    assert len(rows) == 8
    assert {(r.symbol, r.b, r.c, r.norm) for r in rows} == {
        ("{3,6}", 1, 0, 1), ("{6,3}", 1, 0, 1),
        ("{3,6}", 2, 0, 4), ("{6,3}", 2, 0, 4),
        ("{3,6}", 1, 1, 3), ("{6,3}", 1, 1, 3),
        ("{3,6}", 2, 1, 7), ("{6,3}", 2, 1, 7),
    }


def test_audit_checks_all_true():
    audit = eisenstein_torus_map_bridge_audit()
    assert all(audit["checks"].values())
    assert audit["csaszar_szilassi_identification"]["shared_edge_count"] == 21
