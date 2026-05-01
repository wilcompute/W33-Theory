from fractions import Fraction

from PART_CXLIX_PROJECTION_LAYER import (
    HASHIMOTO_NORM,
    K,
    PHI3,
    PHI4,
    PHI6,
    classify_projection,
    formerly_unclassified_classifications,
    inverse_projection,
    projection,
    projection_dictionary,
    projection_layer_audit,
)


def test_projection_operation_on_structural_atoms():
    assert projection(PHI6) == Fraction(7, 13)
    assert projection(HASHIMOTO_NORM) == Fraction(11, 13)
    assert projection(K) == Fraction(12, 13)
    assert projection(PHI4) == Fraction(10, 13)


def test_inverse_projection_operation():
    assert inverse_projection(PHI6) == Fraction(13, 7)
    assert inverse_projection(HASHIMOTO_NORM) == Fraction(13, 11)


def test_projection_dictionary_tags_formerly_unclassified_values():
    d = projection_dictionary()
    assert d[Fraction(7, 13)].projection_class == "field projection"
    assert d[Fraction(11, 13)].projection_class == "radial projection"
    assert d[Fraction(12, 13)].projection_class == "degree projection"
    assert d[Fraction(13, 7)].projection_class == "inverse projection"


def test_phi4_projection_overlaps_mixer_complement():
    tagged = classify_projection("phi4", Fraction(10, 13))
    assert tagged.matched is True
    assert "mixer overlap" in tagged.projection_class


def test_formerly_unclassified_all_match_projection_layer():
    assert all(c.matched for c in formerly_unclassified_classifications())


def test_projection_layer_boundary_is_distinct_from_mixer():
    # The threshold projection is not the carrier or threshold mixer weight.
    assert projection(PHI6) != Fraction(8, 13)
    assert projection(PHI6) != Fraction(5, 13)


def test_projection_layer_audit_checks():
    audit = projection_layer_audit()
    assert all(audit["checks"].values())
    assert "separate layer" in audit["operation"]["boundary_rule"]
    assert "Projection tokens are not automatically mixer tokens" in audit["operation"]["boundary_rule"]
