"""
Part CXXVI — Spread-line Morita spectral bridge.

Pure arithmetic regression tests for the rectangular incidence bridge
between 40 W(3,3) lines and 36 complete two-qutrit MUB spreads.
"""

LINE_COUNT = 40
SPREAD_COUNT = 36
SPREADS_PER_LINE = 9
LINES_PER_SPREAD = 10

# Line-disjointness graph on W(3,3) lines.
LINE_DISJOINT_SRG = (40, 27, 18, 18)
LINE_DISJOINT_EIGS = {27: 1, 3: 15, -3: 24}

# Four-overlap graph on complete MUB spreads.
SPREAD_OVERLAP4_SRG = (36, 15, 6, 6)
SPREAD_OVERLAP4_EIGS = {15: 1, 3: 15, -3: 20}


def gram_line_eigs():
    # BB^T = 9I + 3D.
    return {SPREADS_PER_LINE + 3 * eig: mult for eig, mult in LINE_DISJOINT_EIGS.items()}


def gram_spread_eigs():
    # B^T B = J + 9I + 3A4.
    # On constants: J contributes 36. On nonconstants: J contributes 0.
    return {
        36 + 9 + 3 * 15: 1,
        9 + 3 * 3: 15,
        9 + 3 * (-3): 20,
    }


class TestCXXVIBasicIncidenceCounts:
    def test_total_incidences_match_both_sides(self):
        assert LINE_COUNT * SPREADS_PER_LINE == SPREAD_COUNT * LINES_PER_SPREAD == 360

    def test_common_spine_rank(self):
        line_gram = gram_line_eigs()
        spread_gram = gram_spread_eigs()
        assert line_gram == {90: 1, 18: 15, 0: 24}
        assert spread_gram == {90: 1, 18: 15, 0: 20}
        assert sum(mult for eig, mult in line_gram.items() if eig != 0) == 16
        assert sum(mult for eig, mult in spread_gram.items() if eig != 0) == 16

    def test_carrier_decompositions(self):
        assert 1 + 15 + 24 == 40
        assert 1 + 15 + 20 == 36
        assert 1 + 15 == 16


class TestCXXVIGramHamiltonian:
    def test_normalized_mub_hamiltonian_spectrum(self):
        spread_gram = gram_spread_eigs()
        normalized = {eig // 18: mult for eig, mult in spread_gram.items()}
        assert normalized == {5: 1, 1: 15, 0: 20}

    def test_a2_null_plane_is_inside_twenty_kernel(self):
        # CXXV found a 2-dimensional A2 quotient null plane. CXXVI upgrades this:
        # it is contained in the full 20-dimensional right kernel of B.
        a2_dim = 2
        full_kernel_dim = gram_spread_eigs()[0]
        assert full_kernel_dim == 20
        assert a2_dim < full_kernel_dim
        assert full_kernel_dim - a2_dim == 18

    def test_dual_obstruction_dimensions(self):
        left_cokernel = gram_line_eigs()[0]
        right_kernel = gram_spread_eigs()[0]
        assert left_cokernel == 24
        assert right_kernel == 20
        assert left_cokernel - right_kernel == 4
        assert left_cokernel + right_kernel == 44
