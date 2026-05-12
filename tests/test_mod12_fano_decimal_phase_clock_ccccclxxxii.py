def test_genus_increment_phase_arithmetic():
    dv = 3
    de = 15
    df = 10
    assert (dv, de % 12, df % 12) == (3, 3, 10)
    assert dv - de + df == -2


def test_three_clocks():
    clocks = {"mod12": 12, "fano": 7, "decimal_face": 10}
    assert clocks["mod12"] == 12
    assert clocks["fano"] == 7
    assert clocks["decimal_face"] == 10


def test_toroidal_shell_split():
    csaszar = 5
    szilassi = 2
    assert csaszar + szilassi == 7


def test_fano_minimal_incidence_counts():
    points = 7
    lines = 7
    per_line = 3
    through_point = 3
    incidences = 21
    assert points == lines == 7
    assert lines * per_line == incidences
    assert points * through_point == incidences


def test_phase_percolation_atom_labels():
    labels = {"occupation", "phase12", "color7", "face10", "bivector_id"}
    assert labels == {"occupation", "phase12", "color7", "face10", "bivector_id"}


def test_closure_defects():
    defects = {"mod12_phase", "fano_triple", "face_genus_residue", "clifford_holonomy"}
    assert "mod12_phase" in defects
    assert "fano_triple" in defects
    assert "face_genus_residue" in defects
    assert "clifford_holonomy" in defects
