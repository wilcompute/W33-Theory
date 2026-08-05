from __future__ import annotations

import importlib.util
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass3751_3758_monster_lattice_multiport_cover.py"
FROZEN = ROOT / "data" / "PART_3751_3758_MONSTER_LATTICE_MULTIPORT_COVER_results.json"

spec = importlib.util.spec_from_file_location("pass3751_3758", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    return module.build_certificate()


def test_frozen_certificate_reproduces_exactly() -> None:
    expected = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert certificate() == expected
    assert expected["semantic_sha256"] == "6271dafcc58467d6e758cdbcc9a1b220fe21693b3ace3c727fb5b5499be60ce6"
    assert all(expected["checks"].values())


def test_eight_front_exact_invariants() -> None:
    got = certificate()
    lattice = got["construction_a_lattice"]
    assert lattice["gram_smith_normal_form"] == {"1": 12, "2": 24}
    assert lattice["root_system"] == "A1^36"
    assert lattice["root_count"] == 72

    factor = got["hadamard_multiport_factorization"]
    assert len(factor["primitive_integer_reflection_vectors"]) == 21
    assert got["checks"]["twenty_one_commuting_householders_exact"] is True

    cover = got["cover_classification"]
    assert cover["distance_regular"] is False
    assert cover["terwilliger_dimension_mod_primes"] == {
        "1000003": 55,
        "1000033": 55,
        "1000037": 55,
    }

    walsh = got["quadratic_walsh_parent"]
    assert walsh["difference_set_parameters"] == [64, 36, 20]
    assert walsh["principal_minor_identity"].startswith("K=W_N-2I")

    smith = got["triple_incidence_integral_cokernel"]
    assert smith["smith_normal_form"] == {"1": 30, "2": 5, "6": 1}
    assert smith["cokernel_order"] == 192

    frame = got["twisted_holonomy_frame"]
    assert frame["rank"] == 20
    assert frame["tight_frame_bound"] == 6
