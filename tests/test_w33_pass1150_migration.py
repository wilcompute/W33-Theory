from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_pass1150_finalize_shifted_adjacency_migration.py"; s=importlib.util.spec_from_file_location("pass1150",p); m=importlib.util.module_from_spec(s); assert s and s.loader; s.loader.exec_module(m); return m
def test_pass1150_synthetic(tmp_path:Path):
    m=load()
    for d in ["data","analysis","tests","docs"]: (tmp_path/d).mkdir()
    (tmp_path/"analysis/legacy.py").write_text('"""doc"""\nfrom __future__ import annotations\nprint("old", encoding="utf-8")\n')
    (tmp_path/"tests/test_old.py").write_text('from __future__ import annotations\ndef test_old(, encoding="utf-8"): assert True\n')
    (tmp_path/"docs/old.md").write_text('# Old\n', encoding="utf-8")
    ledger={"schema":"v3","known_descendants":{"analysis/legacy.py":"legacy_derivation_pending_patch","tests/test_old.py":"legacy_test_quarantined_pending_marker","docs/old.md":"historical_summary_pending_patch"}}
    (tmp_path/"data/w33_shifted_adjacency_retraction_ledger.json").write_text(json.dumps(ledger, encoding="utf-8"))
    r=m.run(tmp_path,apply=True); assert r["status"]=="PASS" and r["pending_before"]==3
    new=json.loads((tmp_path/"data/w33_shifted_adjacency_retraction_ledger.json").read_text(encoding="utf-8")); assert new["schema"].endswith("v4") and all("pending" not in s.lower() for s in new["known_descendants"].values())
