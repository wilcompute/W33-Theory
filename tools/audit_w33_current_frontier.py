#!/usr/bin/env python3
"""Fail-closed audit of the generated W33 current-frontier publication manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/w33_current_frontier_manifest_v1.json"
INPUT_RE = re.compile(r"\\input\{([^}]+)\}%?")
MANIFEST_INPUT = r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def audit(require_index: bool = True) -> dict:
    config = load_config()
    tex_manifest = ROOT / config["tex_manifest"]
    assert tex_manifest.is_file(), tex_manifest
    manifest_text = tex_manifest.read_text(encoding="utf-8")
    observed_inputs = INPUT_RE.findall(manifest_text)
    required_inputs = config["required_ordered_inputs"]
    assert observed_inputs == required_inputs, (observed_inputs, required_inputs)
    assert len(observed_inputs) == len(set(observed_inputs))
    for item in observed_inputs:
        path = ROOT / f"{item}.tex"
        assert path.is_file(), path

    wrappers = {}
    for wrapper_name, body_name in config["front_doors"].items():
        wrapper = ROOT / wrapper_name
        body = ROOT / body_name
        assert wrapper.is_file() and body.is_file()
        text = wrapper.read_text(encoding="utf-8")
        assert text.count(MANIFEST_INPUT) == 1, wrapper_name
        assert text.count(rf"\input{{{body_name}}}") == 1, wrapper_name
        direct_current = [item for item in required_inputs if rf"\input{{{item}}}" in text]
        assert not direct_current, (wrapper_name, direct_current)
        wrappers[wrapper_name] = {
            "sha256": sha256(wrapper),
            "body": body_name,
            "manifest_references": text.count(MANIFEST_INPUT),
        }

    index_path = ROOT / config["public_index"]
    index_status = {"required": require_index, "path": str(index_path.relative_to(ROOT))}
    if require_index:
        assert index_path.is_file(), index_path
        index_text = index_path.read_text(encoding="utf-8")
        ids = {item: index_text.count(f'id="{item}"') for item in config["required_public_ids"]}
        markers = {item: index_text.count(item) for item in config.get("required_public_markers", [])}
        assert all(count == 1 for count in ids.values()), ids
        assert all(count >= 1 for count in markers.values()), markers
        index_status.update({"sha256": sha256(index_path), "ids": ids, "markers": markers})

    return {
        "schema": "w33.current_frontier_audit.v1",
        "status": "PASS",
        "manifest": {
            "path": config["tex_manifest"],
            "sha256": sha256(tex_manifest),
            "ordered_inputs": observed_inputs,
            "count": len(observed_inputs),
        },
        "wrappers": wrappers,
        "index": index_status,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--allow-unmaterialized-index", action="store_true")
    args = parser.parse_args()
    report = audit(require_index=not args.allow_unmaterialized_index)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print(f"PASS current-frontier audit inputs={report['manifest']['count']}")
    print(payload, end="")


if __name__ == "__main__":
    main()
