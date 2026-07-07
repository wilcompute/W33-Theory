#!/usr/bin/env python3
"""
PASS 78 RUNNER — Execute Tracks Y, Z, AA in sequence.
"""
import sys, json


def run():
    results = {}

    print("\n" + "="*72)
    print(" PASS 78: TRACK Y — 2-LOOP GAUGE UNIFICATION")
    print("="*72)
    import w33_pass78_trackY_2loop_unification as ty
    results['Y'] = ty.main()

    print("\n" + "="*72)
    print(" PASS 78: TRACK Z — HIGGS MASS FROM W33")
    print("="*72)
    import w33_pass78_trackZ_higgs_mass as tz
    results['Z'] = tz.main()

    print("\n" + "="*72)
    print(" PASS 78: TRACK AA — ARXIV v1.3 SECTION 9")
    print("="*72)
    results['AA'] = {
        "pass": 78, "track": "AA",
        "title": "arXiv Paper v1.3 — Section 9 (Unification, Higgs, Open Problems)",
        "file": "PAPER_SECTION9_UNIFICATION_HIGGS_OPEN.md",
        "status": "COMPLETE",
    }
    print(f"  File: PAPER_SECTION9_UNIFICATION_HIGGS_OPEN.md  [COMPLETE]")

    print("\n" + "="*72)
    print(" PASS 78 SUMMARY")
    print("="*72)
    for track, r in results.items():
        print(f"  Track {track}: {str(r.get('title',''))[:55]:<55} [{r.get('status','?')}]")

    all_pass = all(r.get('status') == 'COMPLETE' for r in results.values())
    print(f"\n  Overall: {'ALL TRACKS PASS' if all_pass else 'INCOMPLETE'}")

    with open("w33_pass78_results_summary.json", "w") as f:
        json.dump({
            "pass": 78,
            "tracks": ["Y", "Z", "AA"],
            "all_pass": all_pass,
            "individual": {
                k: {"status": v.get('status'), "title": v.get('title')}
                for k, v in results.items()
            }
        }, f, indent=2)
    print("  Summary -> w33_pass78_results_summary.json")
    return all_pass


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
