from __future__ import annotations
import json
import py_compile
import subprocess
import sys
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0,str(ROOT/"analysis"))


def load(name):
    return json.loads((DATA / f"PART_2026_07_11_LEVI_NEXT5_V5_{name}.json").read_text(encoding="utf-8"))


def fresh(name):
    p = subprocess.run([sys.executable, str(ROOT / "analysis" / f"w33_levi_next5_v5_{name}.py")], cwd=ROOT, capture_output=True, text=True, check=True, timeout=240)
    return json.loads(p.stdout)


def test_fourier_geometry():
    d=load("fourier"); assert d["status"]=="PASS"
    assert d["symmetric_matrix_q3"]["symmetric_dimension"]==6
    assert d["symmetric_matrix_q3"]["alternating_dimension"]==3
    assert d["symmetric_matrix_q3"]["diagonal_map_rank"]==3
    assert "No finite Fourier transform" in d["scope_boundary"]
    assert d["full_w33"]["jordan_blocks"] == {"J1":6,"J2":0,"J3":22,"J4":2}


def test_h2_transgression_and_gauge():
    d=load("extension"); assert d["status"]=="PASS"
    assert d["periodic_cohomology"]["H1_dimension"]==3
    assert d["periodic_cohomology"]["H2_dimension"]==3
    assert len(d["H2_extension_classes_prescribed_action"])==8
    assert "not central extensions" in d["scope_boundary"]
    assert d["transgression"]["delta_class"]=="0x0"
    assert d["checks"]["gauged_order8_generator_fixed"]


def test_e8_runtime_lanes():
    d=load("lanes"); assert d["status"]=="PASS"
    assert d["decomposition"]["orbit_sizes"] == [1]*6+[27]*6+[72]
    assert d["routing"]["payload_addresses"]==162
    assert d["routing"]["control_fanout_per_payload"]=={"minus":16,"orthogonal":40,"plus":16}
    assert d["seeded_replay_smoke"]["passed"] and d["seeded_replay_smoke"]["steps"]==50000
    assert d["seeded_replay_smoke"]["proof_strength"].startswith("none")
    assert "complement of the conventional Schlaefli graph" in d["theorem"]


def test_hybrid_hardware_budget():
    d=load("hybrid"); assert d["status"]=="PASS"
    assert d["power_budget"]["total_mw"] < 100
    assert d["synthetic_phase_corners"]["p05"] > .999
    assert d["drift"]["tracked_min"] > .999
    assert d["layout"]["gds_bytes"] > 20000
    assert d["layout"]["kind"]=="record-valid abstract placement sketch"
    assert d["layout"]["validation"]["envelope_ok"]
    assert d["veriloga"]["scope"].startswith("static source contract only")
    assert -32767 <= d["compiler"]["command_word_min"] <= d["compiler"]["command_word_max"] <= 32767


def test_vendor_reference_and_rtl_runtime():
    d=load("hardware"); assert d["status"]=="PASS"
    assert d["reference_reducer"]["execution"].startswith("Python cycle model")
    assert d["reference_reducer"]["input_events"] > 1_000_000
    assert d["reference_reducer"]["frames"]==256
    assert d["runtime_replay"]["w33_points_covered"]==40
    assert d["runtime_replay"]["payload_addresses_covered"]==162
    assert "parallel typed projections" in d["runtime_replay"]["mapping_scope"]
    assert d["rtl"]["execution"].startswith("Icarus compile/smoke")
    assert all(d["checks"].values())


def test_documented_vendor_shapes_and_fail_closed_paths():
    from w33_levi_next5_v5_hardware_vendors import QuTAGAdapter,SwabianAdapter,Tag
    tags=[Tag(10,0),Tag(20,1)]

    class Buffer:
        hasOverflows=False
        def getTimestamps(self):return [10,20]
        def getChannels(self):return [1,2]
        def getEventTypes(self):return [0,0]
        def getMissedEvents(self):return [0,0]
    class Stream:
        def getData(self):return Buffer()
        def stop(self):pass
    class Swabian:
        def createTimeTagger(self):return object()
        def TimeTagStream(self,_tagger,n_max_events,channels):
            assert n_max_events==8 and channels==list(range(1,18));return Stream()
        def freeTimeTagger(self,_tagger):pass
    sw=SwabianAdapter(Swabian(),8);out,missed,fault=sw.read_clean();sw.close()
    assert out==tags and missed==0 and not fault

    class QuTAG:
        def getLastTimestamps(self,reset=True):return [10,20,0],[0,1,0],2
        def getDataLost(self):return True
    q=QuTAGAdapter(QuTAG());assert q.read()[1:]==(1,True)
    with pytest.raises(RuntimeError):q.read_clean()


def test_phase_word_ranges_and_rtl_snapshot_sources():
    from w33_levi_next5_v5_hybrid import decode_phase_words,encode_phase_words
    words=encode_phase_words([-3.0,0.0,3.0],16,signed=True)
    assert words.min()>=-32767 and words.max()<=32767
    for bad,signed in (([32768],True),([-32768],True),([-1],False),([65536],False)):
        with pytest.raises(ValueError):decode_phase_words(bad,16,signed=signed)
    rtl=(ROOT/"hardware/holonet_v5_frame_reducer.sv").read_text(encoding="utf-8")
    tb=(ROOT/"hardware/tb_holonet_v5_frame_reducer.sv").read_text(encoding="utf-8")
    assert all(token in rtl for token in ("frame_counts","accum_overflow","m_axis_frame_id <= frame_counter"))
    assert "c0!==2" in tb and "fid!==0" in tb and "bad second frame snapshot" in tb


def test_all_fresh_witnesses():
    for name in ("fourier","extension","lanes","hybrid","hardware"):
        regenerated=fresh(name)
        assert regenerated["status"]=="PASS"
        assert regenerated==load(name)


def test_sources_compile_and_formal_imported():
    for p in (ROOT/"analysis").glob("w33_levi_next5_v5*.py"):
        py_compile.compile(str(p), doraise=True)
    assert "import W33.HeisenbergQ3" in (ROOT/"formal/W33.lean").read_text(encoding="utf-8")
    blocks=(ROOT/"formal/W33/FourierBlocks.lean").read_text(encoding="utf-8")
    q3=(ROOT/"formal/W33/HeisenbergQ3.lean").read_text(encoding="utf-8")
    assert "structure TrivialBlock" not in blocks
    assert "finite-field Fourier transform" in blocks
    assert "q3_nontrivial_block_ranks" not in q3
    assert "q3_matrix_cardinality_package" in q3


def test_cli_routes_and_aggregate():
    source=(ROOT/"holonet_cmd.py").read_text(encoding="utf-8")
    for cmd in ("fourier-geometry-v5","extension-cohomology-v5","e8-lanes-v5","hybrid-compiler-v5","hardware-runtime-v5","levi-next5-v5"):
        assert cmd in source
    d=load("results"); assert d["status"]=="PASS" and all(d["checks"].values())
    assert all(d["fresh_matches_cached"].values())
    assert d["execution"].startswith("all five witness")
