#!/usr/bin/env python3
"""Aggregate the five executable Levi-next5-v2 closure tracks."""
from __future__ import annotations
from w33_levi_next5_v2_common import *
from w33_levi_next5_v2_rank import formal_rank_track
from w33_levi_next5_v2_sentinel import SentinelFaultStack
from w33_levi_next5_v2_mod8 import mod8_lift_track
from w33_levi_next5_v2_runtime import native_runtime_track
from w33_levi_next5_v2_photonic import photonic_compiler_track

def analyze() -> dict:
    geometry = base.build_geometry(3)
    tracks = {
        "1_formal_odd_q_rank_certificate": formal_rank_track(),
        "2_sentinel_authenticated_admission": SentinelFaultStack().combined_theorem(),
        "3_mod8_U14_lift": mod8_lift_track(geometry),
        "4_native_51840_action": native_runtime_track(geometry),
        "5_photonic_E8_compiler": photonic_compiler_track(geometry),
    }
    checks = {name: track["all_pass"] for name, track in tracks.items()}
    return {
        "title": "Formal rank, sentinel admission, mod-8 lift, native W(E6) runtime, and photonic E8 compiler",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "all_five_pass": all(checks.values()),
        "tracks": tracks,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="all", choices=["all", "packet-sentinel-stack", "photonic-e8-compile"])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "packet-sentinel-stack":
        output = SentinelFaultStack().combined_theorem()
    elif args.command == "photonic-e8-compile":
        output = photonic_compiler_track(base.build_geometry(3))
    else:
        output = analyze()
    if args.write or args.command == "all":
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output.get("all_pass", output.get("status") in {"PASS", "PROVED"}) else 1


if __name__ == "__main__":
    raise SystemExit(main())
