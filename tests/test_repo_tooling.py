"""Regression tests for the 2026-10-30 repository tooling: formula-freeze digest, find.py, bootstrap payload checker."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from formula_universe_digest import digest  # noqa: E402


def _universe(frozen_at, head, formulas):
    fam = [dict(formula_id=f"id{i}", normalized_formula=f, occurrence_count=1, file_count=1, source_files=["a.md"],
                source_locations=[dict(path="a.md", line=10 + i)]) for i, f in enumerate(formulas)]
    return json.dumps(dict(frozen_at=frozen_at, repository_head=head, summary=dict(files_scanned=5), exact_families=fam,
                           structural_families=[dict(structural_family_id="s", exact_formula_ids=[x["formula_id"] for x in fam])]))


def test_digest_ignores_bookkeeping_but_sees_formulas():
    a = _universe("2026-10-29", "aaa", ["x=1", "y=2"])
    b = _universe("2026-10-30", "bbb", ["x=1", "y=2"])          # only timestamps / HEAD moved: no commit wanted
    c = _universe("2026-10-30", "bbb", ["x=1", "y=2", "z=3"])   # a new formula: commit wanted
    assert digest(a) == digest(b)
    assert digest(a) != digest(c)


def test_find_reads_the_live_tree():
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "find.py"), "k(q+2-k)", "--limit", "3"], cwd=ROOT,
                         capture_output=True, text=True, timeout=600).stdout
    assert "tracked files:" in out and "analysis/" in out


def test_bootstrap_checker_reports_the_truncated_packet():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_bootstrap_payloads.py"), "--json"], cwd=ROOT,
                       capture_output=True, text=True, timeout=300)
    rows = json.loads(r.stdout)
    bad = {x["target"] for x in rows if x["status"] != "OK"}
    assert "analysis/bt3388_3399_engine.py" in bad          # known-broken since the 2026-08-04 upload: the checker must see it
