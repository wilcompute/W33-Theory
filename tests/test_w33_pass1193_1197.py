from analysis.w33_pass1193_a5_intersection_bridge import main as p1193
from analysis.w33_pass1194_residual_wedderburn_idempotents import main as p1194
from analysis.w33_pass1195_ihara_primitive_cycle_census import main as p1195
from analysis.w33_pass1196_equivariant_ihara_orbit_boundary import main as p1196


def test_pass1193_a5_bridge():
    r = p1193()
    assert r["groups"]["intersection_order"] == 60
    assert r["indices"]["PSp43_over_A5"] == 432


def test_pass1194_wedderburn_tower():
    r = p1194()
    assert r["residual"]["commutant_dimension"] == 1109
    assert r["tower"]["kernel_2195"]["commutant_dimension"] == 1118
    assert r["tower"]["carrier_2240"]["commutant_dimension"] == 1193


def test_pass1195_ihara_census():
    r = p1195()
    assert r["short_checks"]["triangles_unoriented"] == 160
    assert r["short_checks"]["length4_unoriented"] == 1740
    assert len(r["census"]) == 40


def test_pass1196_short_orbits():
    r = p1196()
    assert r["point_action"]["generated_order"] == 25920
    assert [x["orbit_size"] for x in r["primitive_cycle_orbits"]["length_4"]] == [120, 1620]
