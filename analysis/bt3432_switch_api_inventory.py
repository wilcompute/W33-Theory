#!/usr/bin/env python3
"""Inventory the exact Pass-3296 switch implementation after materialization.

This does not guess a switch definition. It records the callable and textual API
that produced the certified 135-species Hamming component, so the full 327-ledger
worker can bind to the same operation in a later executed stage.
"""
from pathlib import Path
import ast
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis/bt3296_3297_cover_hamming_orbifold.py"
OLD_LEDGER = ROOT / "data/PART_BT3296_BT3297_COVER_ORBIT_LEDGER.json"
OUT = ROOT / "data/PART_BT3432_SWITCH_API_INVENTORY.json"


def main():
    if not SOURCE.exists():
        subprocess.run([sys.executable, "bootstrap/pass3296_3307/materialize.py"], cwd=ROOT, check=True)
    text = SOURCE.read_text()
    tree = ast.parse(text)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            if any(token in name.lower() for token in ("switch", "trade", "neighbor", "cover", "orbit")):
                functions.append({
                    "name": name,
                    "arguments": [arg.arg for arg in node.args.args],
                    "line": node.lineno,
                })
    subprocess.run([sys.executable, str(SOURCE.relative_to(ROOT))], cwd=ROOT, check=True)
    ledger = json.loads(OLD_LEDGER.read_text())
    output = {
        "schema": "w33.pass3432.switch_api_inventory.v1",
        "status": "PASS_HISTORICAL_SWITCH_SOURCE_MATERIALIZED",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "candidate_functions": functions,
        "old_ledger_sha256": hashlib.sha256(OLD_LEDGER.read_bytes()).hexdigest(),
        "old_ledger_top_level_keys": sorted(ledger),
        "boundary": "This inventories the exact historical switch implementation. It does not promote a full 327-species component graph until that API is bound to and executed on the canonical ledger.",
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(output["status"], len(functions))


if __name__ == "__main__":
    main()
