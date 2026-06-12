#!/usr/bin/env python3
"""BT789: audit the BT777 suite manifest against landed verifier files."""
from __future__ import annotations
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/"analysis"/"bt777_run_bt766_bt776_suite.py"
OUT=ROOT/"data"/"PART_BT789_SUITE_MANIFEST_AUDIT_summary.json"
SHOULD_INCLUDE=["bt787_q43_one_block"]
SHOULD_NOT_INCLUDE=["bt784_pg_gauge_action_bridge","bt788_h15_one_move_bridge"]

def lists_from_runner():
    tree=ast.parse(RUNNER.read_text())
    vals={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for t in node.targets:
                if isinstance(t,ast.Name) and t.id in {"MODULES","EXPECTED_OUTPUTS"}:
                    vals[t.id]=ast.literal_eval(node.value)
    return vals.get("MODULES",[]), vals.get("EXPECTED_OUTPUTS",[])

def main():
    mods,outs=lists_from_runner()
    module_files={m:(ROOT/"analysis"/(m+".py")).exists() for m in mods}
    output_shape={p:p.startswith("data/PART_BT") and p.endswith((".json",".md")) for p in outs}
    missing_should=[m for m in SHOULD_INCLUDE if m not in mods]
    bad_should=[m for m in SHOULD_NOT_INCLUDE if m in mods]
    checks={
        "runner_exists":RUNNER.exists(),
        "all_listed_modules_exist":all(module_files.values()),
        "all_output_paths_have_expected_shape":all(output_shape.values()),
        "bt787_landed_but_not_yet_in_runner":missing_should==["bt787_q43_one_block"],
        "blocked_bridge_modules_not_in_runner":not bad_should,
    }
    result={"theorem":"BT789 suite manifest audit","summary":{"module_count":len(mods),"output_count":len(outs),"missing_recommended_modules":missing_should,"blocked_modules_present":bad_should},"module_files":module_files,"checks":checks,"all_checks_pass":all(checks.values()),"boundary":"Audit only. It records that BT787 should be added to BT777 when a runner patch is allowed; blocked BT784/BT788 verifier names are intentionally absent."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["all_checks_pass"]: raise SystemExit(1)
if __name__=="__main__": main()
