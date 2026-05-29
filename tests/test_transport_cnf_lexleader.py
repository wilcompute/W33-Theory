"""Unit test for transport CNF exporter lex-leader behavior (synthetic).

This test exercises build_cnf with a tiny synthetic packet and a small group
to ensure lex-leader options run and produce clauses without raising.
"""
from scripts.transport_csp_cnf_export import build_cnf


def make_synthetic_packet(n_cells=2, per_cell=3):
    # total variables
    n = n_cells * per_cell
    # packet_cycles placeholder (list length = n)
    packet_cycles = [tuple([i]) for i in range(n)]
    # build a simple group: identity and rotate-within-cell
    perm_id = tuple(range(n))
    perm_rot = []
    for cell in range(n_cells):
        base = cell * per_cell
        # rotation inside cell: base->base+1, base+1->base+2, base+2->base
        perm_rot.extend([base + 1, base + 2, base + 0])
    perm_rot = tuple(perm_rot)
    packet_image = [perm_id, perm_rot]
    return packet_cycles, packet_image


def test_build_cnf_lexleader_variants():
    packet_cycles, packet_image = make_synthetic_packet()
    # baseline: no lexleader
    clauses0, n0, per0 = build_cnf(packet_cycles, packet_image, per_cell=3, seed_fix=None, lexleader=False, lexleader_strong=False, lexleader_prefix_length=2, commander_size=0)
    assert len(clauses0) > 0
    # prefix lexleader
    clauses1, n1, per1 = build_cnf(packet_cycles, packet_image, per_cell=3, seed_fix=None, lexleader=True, lexleader_strong=True, lexleader_prefix_length=2, commander_size=0)
    assert len(clauses1) > 0
    # full-orbit lexleader (use None => full orbit)
    clauses2, n2, per2 = build_cnf(packet_cycles, packet_image, per_cell=3, seed_fix=None, lexleader=True, lexleader_strong=True, lexleader_prefix_length=None, commander_size=0)
    assert len(clauses2) > 0
    # ensure outputs differ (stronger lexleader should add clauses)
    assert len(clauses2) >= len(clauses1)
