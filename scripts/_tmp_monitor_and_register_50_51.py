#!/usr/bin/env python3
"""Monitor for the targeted dd_shrink sweep for pair (50,51).
Polls the `checks` directory for new `PART_CVII_dd_shrink_result_*.json` files and runs
`scripts/register_dd_obstructions.py --commit` (no push) when new results appear.
Also watches for `dd_repro_targeted_50_51_summary_*.json` and copies the latest
summary to `checks/dd_repro_targeted_50_51_summary_latest.json` for easy inspection.
Logs activity to `checks/PART_CVII_dd_monitor_log_<ts>.txt`.

Runs for up to `timeout` seconds (default 30 minutes) and exits.
"""
import glob
import json
import os
import subprocess
import time
from pathlib import Path

CHECKS = Path("checks")
LOG = CHECKS / f"PART_CVII_dd_monitor_log_{int(time.time())}.txt"
SEEN_FILE = CHECKS / "_tmp_dd_monitor_seen.json"

# Load seen state if present
seen = set()
if SEEN_FILE.exists():
    try:
        seen = set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))
    except Exception:
        seen = set()

# Parameters
interval = 30
timeout = 60 * 30  # 30 minutes
start = time.time()

with open(LOG, "a", encoding="utf-8") as f:
    f.write(f"START {time.time()}\n")

try:
    while time.time() - start < timeout:
        # Discover dd_shrink_result files
        results = sorted(glob.glob(str(CHECKS / "PART_CVII_dd_shrink_result_*.json")))
        new = [r for r in results if r not in seen]
        if new:
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(f"{time.time()}: found {len(new)} new result(s) -> {new}\n")
            # Persist seen
            seen.update(new)
            SEEN_FILE.write_text(json.dumps(sorted(list(seen, encoding="utf-8")), indent=2), encoding="utf-8"
            )
            # Run register (commit-only)
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(
                    f"{time.time()}: running register_dd_obstructions.py --commit\n"
                )
            proc = subprocess.run(
                ["py", "-3", "scripts/register_dd_obstructions.py", "--commit"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            with open(LOG, "a", encoding="utf-8") as f:
                f.write("register stdout:\n")
                f.write(proc.stdout[:10000])
                f.write("\nregister stderr:\n")
                f.write(proc.stderr[:10000])
                f.write("\n")

        # Look for summary file
        summaries = sorted(
            glob.glob(str(CHECKS / "dd_repro_targeted_50_51_summary_*.json")),
            key=os.path.getmtime,
        )
        if summaries:
            latest = summaries[-1]
            dest = CHECKS / "dd_repro_targeted_50_51_summary_latest.json"
            try:
                with open(latest, "r", encoding="utf-8") as s, open(
                    dest, "w", encoding="utf-8"
                ) as d:
                    d.write(s.read())
                with open(LOG, "a", encoding="utf-8") as f:
                    f.write(
                        f"{time.time()}: found summary {latest} and copied to {dest}\n"
                    )
            except Exception as e:
                with open(LOG, "a", encoding="utf-8") as f:
                    f.write(f"{time.time()}: failed copying summary: {e}\n")
            # summary indicates sweep completion; break after processing
            break

        time.sleep(interval)
finally:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"END {time.time()} (elapsed {time.time()-start} s)\n")

print("Monitor finished")
