"""Focused live-GAP regression for the complete degree-540 species census."""

from __future__ import annotations

from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1139_complete_degree540_species.g"
CERTIFICATE = ROOT / "data" / "w33_pass1139_complete_degree540_species.json"
CLASSIFIER = ROOT / "scripts" / "tag_540_disambiguation.py"
REGISTRY = ROOT / "data" / "ALIAS_REGISTRY.json"

POSITIONS = [77, 78, 79, 80, 81]
RANKS = [25, 28, 27, 21, 32]
JOINT_RANKS = [
    [25, 16, 15, 15, 16],
    [16, 28, 25, 20, 25],
    [15, 25, 27, 20, 25],
    [15, 20, 20, 21, 19],
    [16, 25, 25, 19, 32],
]
TAGS = [
    "{540:point-nonedge}",
    "{540:double-six-nonincident}",
    "{540:gq42-arc}",
    "{540:outer-4c}",
    "{540:line-nonedge}",
]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _certificate() -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 1139"
    result = subprocess.run(
        [gap, "-q", str(SCRIPT.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert (
        "Pass 1139 complete degree-540 species census: PASS (46/46 checks)"
        in result.stdout
    )
    assert "Syntax warning" not in result.stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_gap_proves_the_complete_five_class_census() -> None:
    certificate = _certificate()
    assert certificate["schema"] == (
        "w33.pass1139.complete_degree540_species.gap.v1"
    )
    assert certificate["status"] == "PASS"
    assert certificate["producer"] == "GAP 4.12.1"
    assert certificate["check_count"] == 46
    assert len(certificate["passed_checks"]) == 46
    assert certificate["all_checks_pass"] is True

    census = certificate["order48_tom_census"]
    assert census["positions"] == POSITIONS
    assert census["small_group_ids"] == [
        [48, 33],
        [48, 48],
        [48, 49],
        [48, 30],
        [48, 48],
    ]
    assert census["ranks"] == RANKS
    assert census["joint_rank_matrix"] == JOINT_RANKS
    assert census["normalizer_orders"] == [96, 96, 96, 96, 48]
    assert census["coset_degrees"] == [540] * 5


def test_gap_names_all_five_carriers_and_the_we6_classes() -> None:
    certificate = _certificate()
    species = certificate["species"]
    assert [record["tom_position"] for record in species] == POSITIONS
    assert [record["rank"] for record in species] == RANKS
    assert [record["tag"] for record in species] == TAGS

    bridge = certificate["we6_class_bridge"]
    assert bridge["class_names"] == ["4a", "2d", "4c"]
    assert bridge["class_sizes"] == [540, 540, 540]
    assert bridge["element_orders"] == [4, 2, 4]
    assert bridge["centralizer_orders"] == [96, 96, 96]
    assert bridge["psp_tom_positions"] == [77, 81, 80]


def test_gap_closes_the_double_six_cubic_line_partition() -> None:
    bridge = _certificate()["cubic_incidence_bridge"]
    assert bridge["double_six_tom_position"] == 114
    assert bridge["double_six_count"] == 36
    assert bridge["cubic_line_count"] == 27
    assert bridge["s6_line_orbit_sizes"] == [12, 15]
    assert bridge["incident_flags"] == 432
    assert bridge["incident_stabilizer"] == {
        "order": 60,
        "id": [60, 5],
        "name": "A5",
        "tom_position": 85,
    }
    assert bridge["nonincident_flags"] == 540  # {540:double-six-nonincident}
    assert bridge["nonincident_stabilizer"] == {
        "order": 48,
        "id": [48, 48],
        "name": "C2 x S4",
        "tom_position": 78,
    }
    assert bridge["partition_identity"] == "36*27=36*12+36*15=432+540"


def test_classifier_binds_two_same_line_tags_to_two_occurrences() -> None:
    classifier = _load_module("pass1139_tag540", CLASSIFIER)
    text = (
        "The 540 {540:point-nonedge} noncollinear point pairs differ from "
        "the 540 {540:line-nonedge} skew line pairs."
    )
    matches = classifier._number_matches(text)
    assert len(matches) == 2
    categories = [
        classifier.classify_occurrence(
            text,
            match.start(),
            match.end(),
            "same-line.md",
        )["category"]
        for match in matches
    ]
    assert categories == ["point-nonedge", "line-nonedge"]


def test_classifier_recognizes_all_five_tags_and_mixed_compatibility() -> None:
    classifier = _load_module("pass1139_tag540_all", CLASSIFIER)
    for category in classifier.CANONICAL_SPECIES:
        text = f"The 540 {{540:{category}}} carrier is explicit."  # {540:mixed}
        match = classifier._number_matches(text)[0]
        record = classifier.classify_occurrence(
            text,
            match.start(),
            match.end(),
            f"{category}.md",
        )
        assert record["category"] == category
        assert record["reason"] == "explicit_tag"

    for compatibility in ("both", "mixed"):
        text = f"This one 540 {{540:{compatibility}}} comparison is mixed."  # {540:mixed}
        match = classifier._number_matches(text)[0]
        record = classifier.classify_occurrence(
            text,
            match.start(),
            match.end(),
            "mixed.md",
        )
        assert record["category"] == "both"
        assert record["reason"] == "explicit_mixed_tag"

    text = "The coefficient is 540 {540:unrelated}, not a carrier."
    match = classifier._number_matches(text)[0]
    record = classifier.classify_occurrence(
        text,
        match.start(),
        match.end(),
        "unrelated.md",
    )
    assert record["category"] == "unrelated"
    assert record["reason"] == "explicit_unrelated_tag"


def test_classifier_excludes_pass_number_syntax() -> None:
    classifier = _load_module("pass1139_tag540_passes", CLASSIFIER)
    text = (
        "Pass 540, Pass~540, Passes 528--540, BT540, and PART 540 "
        "are identifiers rather than object cardinalities."
    )
    assert classifier._number_matches(text) == []


def test_classifier_prunes_repository_metadata_and_build_trees(
    tmp_path: Path,
) -> None:
    classifier = _load_module("pass1139_tag540_prune", CLASSIFIER)
    visible = tmp_path / "visible.md"
    visible.write_text(
        "The 540 {540:gq42-arc} Hashimoto arcs are explicit.\n",
        encoding="utf-8",
    )
    hidden_files = [
        tmp_path / ".git" / "hidden.md",
        tmp_path / ".continuity" / "hidden.md",
        tmp_path / "node_modules" / "hidden.md",
        tmp_path / "build" / "hidden.md",
    ]
    for hidden in hidden_files:
        hidden.parent.mkdir(parents=True, exist_ok=True)
        hidden.write_text("An ambiguous " + str(54 * 10, encoding="utf-8") + ".\n",
            encoding="utf-8",
        )

    files = list(classifier.iter_files(tmp_path))
    assert files == [visible]
    audit = classifier.audit(tmp_path)
    assert audit["status"] == "PASS"
    assert audit["files_mentioning_540"] == 1
    assert audit["occurrence_counts"] == {"gq42-arc": 1}


def test_classifier_excludes_generated_meta_indexes(tmp_path: Path) -> None:
    classifier = _load_module("pass1139_tag540_meta", CLASSIFIER)
    data = tmp_path / "data"
    data.mkdir()
    meta = data / "w33_formula_search_universe_v1.json"
    meta.write_text(
        '{"quoted_corpus_text":"an intentionally ambiguous 540"}\n',
        encoding="utf-8",
    )
    assert classifier.audit_file(meta, tmp_path) is None


def test_alias_registry_and_release_surfaces_use_the_five_species() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    records = {
        record.get("psp_tom_position"): record
        for record in registry["objects"]
        if record.get("size") == 540  # {540:mixed}
    }
    assert sorted(records) == POSITIONS
    assert [records[position]["coset_rank"] for position in POSITIONS] == RANKS
    assert [records[position]["tag"] for position in POSITIONS] == TAGS

    release = (
        ROOT / "PASS1132_1136_EXACT_EXECUTION_RELEASE.md"
    ).read_text(encoding="utf-8")
    vocabulary = (ROOT / "RESULTS_VOCABULARY.md").read_text(encoding="utf-8")
    for tag in TAGS:
        assert tag in release
        assert tag in vocabulary
