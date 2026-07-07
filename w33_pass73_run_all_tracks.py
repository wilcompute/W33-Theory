#!/usr/bin/env python3
"""
PASS 73 RUNNER — Execute Tracks J, K, L in sequence.
"""
import sys, json

def run():
    results = {}

    print("\n" + "="*72)
    print(" PASS 73: TRACK J — EQUIVARIANT BIJECTION V4")
    print("="*72)
    import w33_pass73_trackJ_bijection_v4 as tj
    results['J'] = tj.main()

    print("\n" + "="*72)
    print(" PASS 73: TRACK K — AFFINE E8 CHARACTER")
    print("="*72)
    import w33_pass73_trackK_affine_e8_character as tk
    results['K'] = tk.main()

    print("\n" + "="*72)
    print(" PASS 73: TRACK L — PMNS CP PHASE")
    print("="*72)
    import w33_pass73_trackL_pmns_cp_phase as tl
    results['L'] = tl.main()

    print("\n" + "="*72)
    print(" PASS 73 SUMMARY")
    print("="*72)
    for track, r in results.items():
        status = r.get('status', 'UNKNOWN')
        print(f"  Track {track}: {r.get('title','')[:55]:<55} [{status}]")

    all_pass = all(r.get('status') in ('COMPLETE', 'VERIFIED') for r in results.values())
    print(f"\n  Overall: {'ALL TRACKS PASS' if all_pass else 'SOME TRACKS INCOMPLETE'}")

    with open("w33_pass73_results_summary.json", "w") as f:
        json.dump({
            "pass": 73,
            "tracks": ["J", "K", "L"],
            "all_pass": all_pass,
            "individual": {
                k: {"status": v.get('status'), "title": v.get('title')}
                for k, v in results.items()
            }
        }, f, indent=2)
    print("  Summary -> w33_pass73_results_summary.json")
    return all_pass

if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
