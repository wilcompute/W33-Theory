from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/bt3549_3555_borel_pentad_quantum_walk.py"
spec=spec_from_file_location("bt3549_3555",SRC)
mod=module_from_spec(spec);spec.loader.exec_module(mod)

def test_semantic_digest():
    result=mod.build()
    assert result["semantic_sha256"]=="251725b948b166f475cf0a44b9d6662280c2dd7a7e12c47fb5ece3d110cc1f6b"

def test_borel_models():
    x=mod.borel_signature_models()
    assert x["signature_count"]==24
    assert x["profiles"]["P19"]["edge_orbit_variables"]==30915
    assert x["profiles"]["P57"]["ordered_pair_orbits"]==61792

def test_commutant_and_hermitian_split():
    x=mod.perkel_commutant_table()
    assert x["orbital_rank"]==21
    assert x["center_dimension"]==5
    assert (x["transpose_fixed_dimension"],x["transpose_skew_dimension"])==(11,10)
    assert x["nonzero_structure_constants"]==1035

def test_pentad_octad_falsifier():
    x=mod.factorization_search()
    assert x["factorization_counts"]["K8"]["one_factorizations"]==6240
    assert x["K8_setwise_S8_stabilizer"]==1
    g=x["K8_compiled_graph"]
    assert (g["vertices"],g["edges"],g["diameter"])==(82,369,3)
    assert (g["triangles"],g["four_cycles"])==(60,422)

def test_archive_and_quantum_walk():
    a=mod.proof_archive_contract()
    assert (a["instances"],a["shards"])==(3720,64)
    assert a["shard_size_census"]=={"58":56,"59":8}
    q=mod.quantum_walk_compiler()
    assert q["W33"]["distinct_vertex_amplitude_bounds"]=={"adjacent":"1/4","nonadjacent":"2/15"}
    assert q["Gewirtz"]["distinct_vertex_amplitude_bounds"]=={"adjacent":"2/7","nonadjacent":"1/12"}
