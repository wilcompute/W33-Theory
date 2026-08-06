#!/usr/bin/env python3
"""Verify the protected Passes 4121-4128 frontier integration.

This tool never writes docs/index.html.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INSERT="\\input{analysis/BT4121_BT4128_explicit_gauge_dfs_decoder_foundry_attractors_insert}%"
REQUIRED=[
 "data/PART_4121_4128_EXPLICIT_GAUGE_DFS_DECODER_FOUNDRY_ATTRACTORS_BONKERS.json",
 "data/PART_4121_4128_EXPLICIT_GAUGE_DFS_DECODER_FOUNDRY_ATTRACTORS_BONKERS_manifest.json",
 "data/w33_pass4121_explicit_145_gauge_action.json",
 "data/w33_pass4124_cornerstone_floorplan_audit.json",
 "data/w33_pass4125_attractor_orbit_census.json",
 "analysis/w33_pass4121_4128_explicit_gauge_dfs_decoder_foundry_attractors.py",
 "analysis/BT4121_BT4128_explicit_gauge_dfs_decoder_foundry_attractors.md",
 "analysis/BT4121_BT4128_explicit_gauge_dfs_decoder_foundry_attractors_insert.tex",
 "analysis/BT4121_BT4128_explicit_gauge_dfs_decoder_foundry_attractors_index_insert.html",
 "docs/explicit-gauge-dfs-decoder-foundry-attractors-4121-4128.html",
]

def main():
    missing=[p for p in REQUIRED if not (ROOT/p).is_file()]
    if missing: raise SystemExit(f"missing artifacts: {missing}")
    manifest=(ROOT/"analysis/W33_CURRENT_FRONTIER_MANIFEST.tex").read_text()
    assert manifest.count(INSERT)==1
    assert manifest.index("BT4113_BT4120")<manifest.index("BT4121_BT4128")
    cert=json.loads((ROOT/REQUIRED[0]).read_text())
    assert cert["semantic_sha256"]=="a549172701e05bdcb0e629f8cea5282be46db70f223e043b4cb0359b9c3dc4bc"
    ns=json.loads((ROOT/"data/w33_pass_namespace_registry_v2.d/4121-4128.json").read_text())
    assert ns["range"]==[4121,4128] and ns["status"].startswith("source_complete")
    print("Passes 4121-4128 protected frontier is complete; docs/index.html was not modified.")

if __name__=="__main__": main()
