#!/usr/bin/env python3
"""
PASS 77 RUNNER — Execute Tracks V, W, X in sequence.
"""
import sys, json


def run():
    results = {}

    print("\n" + "="*72)
    print(" PASS 77: TRACK V — RELIC DENSITY FIX")
    print("="*72)
    import w33_pass77_trackV_relic_density as tv
    results['V'] = tv.main()

    print("\n" + "="*72)
    print(" PASS 77: TRACK W — COSMOLOGICAL CONSTANT")
    print("="*72)
    import w33_pass77_trackW_cosmological_constant as tw
    results['W'] = tw.main()

    print("\n" + "="*72)
    print(" PASS 77: TRACK X — GAUGE UNIFICATION")
    print("="*72)
    import w33_pass77_trackX_gauge_unification as tx
    results['X'] = tx.main()

    print("\n" + "="*72)
    print(" PASS 77 SUMMARY")
    print("="*72)
    for track, r in results.items():
        status = r.get('status', 'UNKNOWN')
        print(f"  Track {track}: {str(r.get('title',''))[:55]:<55} [{status}]")

    all_pass = all(
        r.get('status') in ('COMPLETE', 'VERIFIED', 'CERTIFIED')
        for r in results.values()
    )
    print(f"\n  Overall: {'ALL TRACKS PASS' if all_pass else 'INCOMPLETE'}")

    with open("w33_pass77_results_summary.json", "w") as f:
        json.dump({
            "pass": 77,
            "tracks": ["V", "W", "X"],
            "all_pass": all_pass,
            "individual": {
                k: {"status": v.get('status'), "title": v.get('title')}
                for k, v in results.items()
            }
        }, f, indent=2)
    print("  Summary -> w33_pass77_results_summary.json")
    return all_pass


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
