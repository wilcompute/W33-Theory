import glob
import json
from pathlib import Path

import pytest


def test_committed_candidates_have_conjugacy_fields():
    conj_files = sorted(glob.glob("checks/PART_CVII_z3_conjugacy_*.json"))
    if not conj_files:
        pytest.skip("optional z3 conjugacy checks file is absent")
    conj = json.loads(open(conj_files[-1], encoding="utf-8").read())
    conj_map = {int(r["index"]): r for r in conj.get("results", [])}

    cand_files = sorted(glob.glob("committed_artifacts/PART_CVII_z3_candidate_*.json"))
    assert cand_files, "No committed z3 candidate metadata found"

    for cf in cand_files:
        data = json.loads(open(cf, encoding="utf-8").read())
        idx = int(data.get("index", -1))
        if idx in conj_map:
            # If conjugacy info exists for this index, the artifact should include it
            assert "centralizer_size" in data and "conj_class_size" in data
            assert data["centralizer_size"] == conj_map[idx]["centralizer_size"]
            assert data["conj_class_size"] == conj_map[idx]["conj_class_size"]
        else:
            # If conjugacy doesn't contain info for this index, just ensure fields are absent
            assert "centralizer_size" not in data or data["centralizer_size"] is None
            assert "conj_class_size" not in data or data["conj_class_size"] is None
