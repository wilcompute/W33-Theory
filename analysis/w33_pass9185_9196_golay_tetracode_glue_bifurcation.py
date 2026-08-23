"""Passes 9185–9196 canonical wrapper for the Golay/tetracode glue bifurcation verifier."""
from pathlib import Path
import w33_rank24_glue_bifurcation_core as _core
from w33_rank24_glue_bifurcation_core import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json"


def main():
    _core.OUT = OUT
    return _core.main()


if __name__ == "__main__":
    raise SystemExit(main())
