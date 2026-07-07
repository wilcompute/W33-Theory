#!/usr/bin/env python3
"""
PASS 75 RUNNER — Execute Tracks P, Q, R in sequence.
"""
import sys, json


def run():
    results = {}

    print("\n" + "="*72)
    print(" PASS 75: TRACK P — WEINBERG ANGLE")
    print("="*72)
    import w33_pass75_trackP_weinberg_angle as tp
    results['P'] = tp.main()

    print("\n" + "="*72)
    print(" PASS 75: TRACK Q — PROTON DECAY")
    print("="*72)
    import w33_pass75_trackQ_proton_decay as tq
    results['Q'] = tq.main()

    print("\n" + "="*72)
    print(" PASS 75: TRACK R — BIJECTION CERTIFICATE")
    print("="*72)
    import w33_pass75_trackR_bijection_certificate as tr
    results['R'] = tr.main()

    print("\n" + "="*72)
    print(" PASS 75 SUMMARY")
    print("="*72)
    for track, r in results.items():
        status = r.get('status', 'UNKNOWN')
        print(f"  Track {track}: {str(r.get('title',''))[:55]:<55} [{status}]")

    all_pass = all(
        r.get('status') in ('COMPLETE', 'VERIFIED', 'CERTIFIED')
        for r in results.values()
    )
    print(f"\n  Overall: {'ALL TRACKS PASS' if all_pass else 'INCOMPLETE'}")

    with open("w33_pass75_results_summary.json", "w") as f:
        json.dump({
            "pass": 75,
            "tracks": ["P", "Q", "R"],
            "all_pass": all_pass,
            "individual": {
                k: {"status": v.get('status'), "title": v.get('title')}
                for k, v in results.items()
            }
        }, f, indent=2)
    print("  Summary -> w33_pass75_results_summary.json")
    return all_pass


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
