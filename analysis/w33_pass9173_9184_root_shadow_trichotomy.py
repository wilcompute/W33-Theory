"""Passes 9173–9184 canonical wrapper for the rank-24 W(3,3) root-shadow verifier."""
from pathlib import Path
import w33_rank24_root_shadow_core as _core
from w33_rank24_root_shadow_core import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS9173_9184_ROOT_SHADOW_TRICHOTOMY.json"


def main():
    _core.OUT = OUT
    return _core.main()


if __name__ == "__main__":
    raise SystemExit(main())
