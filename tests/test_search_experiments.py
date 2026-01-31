from pathlib import Path

from tools.search_experiments import run_sweep

ROOT = Path(__file__).resolve().parents[1]


def test_run_sweep_creates_artifact_and_improves():
    # small sweep to ensure runner executes quickly and produces an artifact
    out = run_sweep(
        triangle_weights=[0, 10], seeds=[0, 1], iterations=500, time_limit=1.0
    )
    assert "runs" in out
    assert len(out["runs"]) == 4
    best = out["best_overall"]
    assert best is not None
    assert best["best_score"] >= out["baseline_score"]

    artfiles = list((ROOT / "artifacts").glob("eq_search_experiments_*.json"))
    assert len(artfiles) >= 1
