import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "analysis" / "w33_s3_completion_admission_controller.py"
    spec = importlib.util.spec_from_file_location(
        "w33_s3_completion_admission_controller", path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_controller() -> dict:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis" / "w33_s3_completion_admission_controller.py"),
        ],
        cwd=ROOT,
        check=True,
    )
    return json.loads(
        (ROOT / "data" / "w33_s3_completion_admission_controller.json").read_text(
            encoding="utf-8"
        )
    )


def test_admission_word_closes_atlas_and_supercycle():
    data = run_controller()
    word = data["admission_word"]

    assert data["verified"] is True
    assert all(data["checks"].values())
    assert word["ordered_paths"] == 4320
    assert word["completions_per_path"] == 3
    assert word["runtime_slots_per_probe"] == 4
    assert word["path_word_ticks"] == 12
    assert word["paths_per_mirror_atlas"] == 180
    assert word["probes_per_mirror_atlas"] == 540
    assert word["mirror_atlases"] == 24
    assert word["identity"] == (
        "4320 paths * 3 completions/path * 4 ticks/completion = 51840"
    )


def test_admission_adjudicator_states_are_conservative():
    module = load_module()

    assert (
        module.adjudicate_branch(
            [None, None, None], minimum_signal=1.0, minimum_margin=0.25
        )["state"]
        == "UNMEASURED"
    )
    assert (
        module.adjudicate_branch(
            [0.1, 0.5, 0.2], minimum_signal=1.0, minimum_margin=0.25
        )["state"]
        == "NO_SIGNAL"
    )
    assert (
        module.adjudicate_branch(
            [2.0, 1.9, 0.1], minimum_signal=1.0, minimum_margin=0.25
        )["state"]
        == "AMBIGUOUS"
    )
    accepted = module.adjudicate_branch(
        [1.0, 1.5, 2.1], minimum_signal=1.0, minimum_margin=0.25
    )
    assert accepted["state"] == "BRANCH_ACCEPTED"
    assert accepted["accepted_completion"] == 2


def test_admission_samples_hit_mirror_boundaries():
    data = run_controller()
    samples = {row["ordered_path_id"]: row for row in data["runtime_samples"]}

    assert samples[0]["path_runtime_slots"][0] == 0
    assert samples[0]["branch_words"][0]["tick_roles"] == [
        "LOAD_PATH_CONTEXT",
        "EMIT_COMPLETION_PROBE",
        "LATCH_BRANCH_EVIDENCE",
        "ADJUDICATE_OR_ESCALATE",
    ]
    assert samples[179]["path_runtime_slots"][-1] == 2159
    assert samples[180]["path_runtime_slots"][0] == 2160
    assert samples[4319]["path_runtime_slots"][-1] == 51839


def test_admission_keeps_no_cover_guardrail():
    data = run_controller()
    boundary = " ".join(data["claim_boundary"])
    policy = data["adjudication_policy"]

    assert "no solution" in policy["guardrail"]
    assert "not measured branch evidence" in boundary
    assert "must be preregistered" in boundary
    assert "unique margin winner" in boundary
    assert "not a canonical quadrangle packet" in boundary


def test_admission_publication_anchor():
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert 'id="holonet-s3-completion-admission-controller"' in docs
    assert "w33_s3_completion_admission_controller.py" in docs
    assert "w33_s3_completion_admission_controller.json" in docs
    assert "4320&times;3&times;4 = 51840" in docs
    assert "180&times;12 = 2160" in docs
