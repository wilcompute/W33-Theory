#!/usr/bin/env python3
"""Export the exact Pass-1607 XOR and exact-cardinality resolution cuts."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "analysis" / "w33_pass1606_1610_five_continuations.py"
CERT = ROOT / "data" / "w33_pass1606_1610_five_continuations.json"


def load_verifier():
    spec = importlib.util.spec_from_file_location("p1606", VERIFIER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xor", type=Path, default=ROOT / "data" / "w33_pass1607_resolution_xors.txt")
    ap.add_argument("--exact8", type=Path, default=ROOT / "data" / "w33_pass1607_exact8_equations.txt")
    args = ap.parse_args()
    cert = json.loads(CERT.read_text())
    solver = cert["passes"]["1607_solver_export"]
    mod = load_verifier()
    points, edges, lines, frames0, group, gens, M, H, A, N, d, K, J, octets = mod.build_geometry()
    records = []
    for o in solver["selected_octets"]:
        frames = [int(x) for x in __import__('numpy').flatnonzero(J[:, o])]
        for c in range(8):
            records.append({"octet":o,"color":c,"rhs":0,"variables":[1+9*f+c for f in frames]})
    xor_text = "".join(f"xor rhs={r['rhs']} " + " ".join(map(str, r["variables"])) + "\n" for r in records)
    exact8 = []
    for o in range(45):
        frames = [int(x) for x in __import__('numpy').flatnonzero(J[:, o])]
        for c in range(9):
            variables = [1 + 9*f + c for f in frames]
            exact8.append(f"eq rhs=8 octet={o} color={c} " + " ".join(map(str, variables)))
    exact8_text = "\n".join(exact8) + "\n"
    import hashlib
    expected = solver
    assert hashlib.sha256(xor_text.encode()).hexdigest() == expected["xor_export_sha256"]
    assert hashlib.sha256(exact8_text.encode()).hexdigest() == expected["exact8_export_sha256"]
    args.xor.parent.mkdir(parents=True, exist_ok=True)
    args.xor.write_text(xor_text)
    args.exact8.write_text(exact8_text)
    print(json.dumps({"xors":len(records),"exact8":len(exact8),"xor_sha256":expected["xor_export_sha256"],"exact8_sha256":expected["exact8_export_sha256"]}))

if __name__ == "__main__":
    main()
