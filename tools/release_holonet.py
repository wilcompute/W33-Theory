#!/usr/bin/env python3
"""BT909 human-facing Photonic Holonet release wrapper."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    print("[BT909] Running Photonic Holonet guarded release...")
    subprocess.run([sys.executable, "tools/release_bt908_photonic_holonet_pdf.py"], cwd=ROOT, check=True)
    print("\n[BT909] Release complete. Artifacts:")
    print("  - photonic_holonet.pdf")
    print("  - dist/photonic_holonet_release_manifest.json")


if __name__ == "__main__":
    main()
