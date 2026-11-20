#!/usr/bin/env python3
"""Read *each* Nov 13--20 master commit's complete textual patch and summarize coverage.

Patch digests certify exhaustive I/O; the summary is triage, not a claim
that a hash or keyword search proves every mathematical theorem in the diff.
Usage: python analysis/toe_20261120_weekly_commit_patch_intake.py
"""
from __future__ import annotations
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
START = "2026-11-13T00:00:00Z"
STOP = "2026-11-21T00:00:00Z"
TOPICS = {
    "quantum_info": r"qutrit|qubit|SIC|MUB|quantum|Clifford|Pauli|Knill|Laflamme|CSS",
    "exceptional": r"\bE8\b|\bE6\b|\bG2\b|\bF4\b|Albert|H27|octonion",
    "gauge_and_matter": r"Yang.Mills|SU3|SU5|Spin10|Higgs|Yukawa|fermion|anomal|chirali",
    "geometry_topology": r"topolog|homolog|holonom|manifold|hexagon|torus|quadric|polyhed|GQ|Witting",
    "causal_gravity": r"causal|gravity|Lorentz|metric|Einstein|AdS|cosmolog|BF bound",
    "photonic_hardware": r"photon|detector|optical|readout|noise|loss|memory|calibrat",
}
def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)
def main() -> None:
    revs = git("rev-list", "--since="+START, "--until="+STOP, "master").decode().splitlines()
    rows = []
    counts = collections.Counter()
    changes = collections.Counter()
    total_bytes = 0
    for i, sha in enumerate(revs, 1):
        full = git("show", "--format=fuller", "--no-ext-diff", "--no-renames", "--no-color", sha)
        text = full.decode("utf-8", "replace")
        metadata = git("show", "-s", "--format=%cI%n%s", sha).decode().splitlines()
        files = re.findall(r"(?m)^diff --git a/(.*?) b/(.*?)$", text)
        touched = [b for a, b in files]
        categories = [label for label, expr in TOPICS.items() if re.search(expr, text[:150000], re.I)]
        for c in categories:
            counts[c] += 1
        for p in touched:
            ext = Path(p).suffix.lower() or "<none>"
            changes[ext] += 1
        rows.append({
            "sha": sha,
            "date": metadata[0],
            "subject": metadata[1][:220],
            "patch_sha256": hashlib.sha256(full).hexdigest(),
            "patch_bytes": len(full),
            "changed_files": len(touched),
            "paths": touched[:35],
            "topics": categories,
        })
        total_bytes += len(full)
        if i % 50 == 0:
            print(f"FULL_PATCH_REVIEW {i}/{len(revs)} bytes={total_bytes}", flush=True)
    result = {
        "date_window_inclusive_utc": [START, STOP],
        "baseline_head": git("rev-parse", "master").decode().strip(),
        "commits_read_full_patch": len(rows),
        "patch_bytes_read": total_bytes,
        "patch_sha256_manifest": hashlib.sha256("\n".join(x["patch_sha256"] for x in rows).encode()).hexdigest(),
        "categories_documentary_not_proofs": dict(counts),
        "changed_path_extensions": dict(changes),
        "top_patch_sizes": sorted(rows,key=lambda x:x["patch_bytes"],reverse=True)[:20],
        "commit_manifest": rows,
        "disclaimer": "Exhaustive git patch-byte intake and metadata triage; only independently rederived claims qualify as verified."
    }
    dest = ROOT/"data"/"toe_20261120_week_commit_patch_intake.json"
    dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("RESULT",str(dest),flush=True)
    print(json.dumps({k:result[k] for k in ("commits_read_full_patch","patch_bytes_read","patch_sha256_manifest","categories_documentary_not_proofs","changed_path_extensions")},indent=2),flush=True)

if __name__=="__main__":
    main()
