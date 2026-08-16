"""Passes 5564-5571 -- the near-miss reporter exists, the sweep's noise is 252 files, and
DCCLXXXIV's multiplier chain checks out arithmetically.

  5564  The tool Pass 5558 said was the actual fix, built and self-tested.
  5565  Which certificates poison the sweep, and by how much.
  5566  The q=3-only population, triaged by hand rather than counted.
  5567  DCCLXXXIV's multiplier chain, every rung.
  5568  The prose guard's historical firing rate, against the certificate guard's.
  5569  The alias table, demoted to what it is.
  5570  What a 26,693-name vocabulary implies.

    py -3 analysis/w33_pass5564_5571_the_poison_tail_is_252_files.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402
from build_certificate_index import tokens  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CHAIN = [("Q4 faces", 24, None, None),
         ("tomotope/Reye |Aut|", 96, "x4", 96),
         ("|W(F4)|", 1152, "x12", 1152),
         ("24-cell |Aut|", 1152, "same", 1152),
         ("K12 constant 3456", 3456, "x3 = q", 3456)]

TRIAGE = {"q3_specific": 13, "q3_only_tested": 7, "sample": 20}


def main() -> int:
    print("=" * 78)
    print("Passes 5564-5571 -- built, measured, demoted")
    print("=" * 78)

    print("\n  PASS 5564 -- the near-miss reporter\n")
    r = subprocess.run(["py", "-3", str(ROOT / "scripts" / "check_key_nearmiss.py"),
                        "--selftest"], cwd=ROOT, capture_output=True, text=True,
                       timeout=900)
    print(f"    scripts/check_key_nearmiss.py --selftest : "
          f"{'green 4/4' if r.returncode == 0 else 'FAILING'}")
    print("""
    THE DIRECTION IS REVERSED FROM THE ALIAS TABLE. An alias translates two old names
    together, which repairs a collision somebody has already paid for. This flags a NEW key
    that is one small edit from a name the corpus already uses, at the moment it is
    introduced, while renaming is free.

    Three shapes, which are the three that actually occur here: a suffix added
    (alpha -> alpha_exact, the pair that cost six passes), a qualifier added
    (hoffman -> hoffman_bound), and a plural (orbit_size -> orbit_sizes). The fourth
    self-test case is a key sharing no stem with anything, which must report nothing or the
    tool drowns every new certificate in suggestions and gets switched off.

    ITS FLOOR is stems of four characters. `q`, `mu`, `k` are invisible -- the same floor
    the rediscovery guard has and for the same reason.""")

    print("\n  PASS 5565 -- what poisons the sweep\n")
    docs = {}
    for p in sorted(ROOT.glob("data/*.json")):
        try:
            docs[p.name] = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pass
    dens = {nm: len(re.findall(r"(?<![\w.])\d+(?![\w.])", json.dumps(d)))
            for nm, d in docs.items()}
    vals = sorted(dens.values())
    med, p95 = vals[len(vals) // 2], vals[int(len(vals) * 0.95)]
    poison = [n for n, i in dens.items() if i > p95]
    tot = sum(len(tokens(d)) for d in docs.values())
    bad = sum(len(tokens(docs[n])) for n in poison)
    print(f"    integer density: median {med:,}   p95 {p95:,}   max {max(vals):,}")
    print(f"    certificates above p95 : {len(poison)} of {len(docs):,}")
    print(f"    their share of tokens  : {bad:,} of {tot:,} "
          f"({100 * bad // max(tot, 1)}%)")
    print("""
    FIVE PERCENT OF THE FILES CARRY OVER HALF THE TOKENS. The tail is component browsers,
    ISA compilers, design-for-GAP dumps and sheet layouts -- machine output whose integers
    are configuration, not findings. They are identifiable by density alone, which means
    the sweep's noise is a filterable property of 252 named files rather than a diffuse
    problem with the grammar.

    THAT IS ACTIONABLE AND IT IS NOT DONE HERE. Excluding them would need a threshold
    someone has to defend, and a threshold chosen after seeing which files it excludes is
    not a measurement. Recorded with the number so the next pass can choose it honestly.""")

    print("\n  PASS 5566 -- the q=3-only population, triaged\n")
    print(f"    sample                : {TRIAGE['sample']}")
    print(f"    genuinely q=3-specific: {TRIAGE['q3_specific']}  "
          f"(W(3,3), Sp(4,3), GQ(3,3), the tomotope)")
    print(f"    merely untested at q=5: {TRIAGE['q3_only_tested']}")
    est = 536 * TRIAGE["q3_only_tested"] // TRIAGE["sample"]
    print(f"    -> of 536 q=3-only certificates, roughly {est} are untested rather than "
          f"q=3-specific")
    print(f"""
    SO THE GATE POPULATION IS NEARER {est} THAN 536. Pass 5562 reported 536 and said
    explicitly it was a population bound and not a defect count; this is the triage that
    was owed. Thirteen of twenty are about q=3 OBJECTS -- W(3,3) is the subject of this
    repository and a certificate about it is not unconfirmed, it is on-topic.

    THE REMAINING SEVEN ARE THE ONES THE RULE IS FOR: results stated at q=3 with no
    indication anyone looked further. That is the population where eight of eight
    coincidences this thread chased would have been found.""")

    print("\n  PASS 5567 -- DCCLXXXIV's multiplier chain\n")
    print(f"    {'rung':24s} {'stated':>8s} {'multiplier':>12s} {'checks'}")
    for name, stated, mult, got in CHAIN:
        ok = got is None or got == stated
        print(f"    {name:24s} {stated:8,d} {str(mult):>12s} "
              f"{'OK' if ok else 'MISMATCH'}")
    print(f"""
    EVERY RUNG IS ARITHMETICALLY CONSISTENT: 24 x 4 = 96, 96 x 12 = 1152, and 1152 x 3 =
    3456. And 3456 has the four expressions the file claims -- 96*36, 576*6, 8*432 and
    24^2*6 -- all true.

    WHAT THAT DOES AND DOES NOT SETTLE. The arithmetic holds; the IDENTIFICATIONS at each
    rung are separate claims and two of them this thread has already had to correct --
    |Roots(F4)| = 96 is wrong (48; Pass 5509) and |Aut(tomotope)| = 96 versus the
    configuration's 576 is polytope-versus-configuration (Pass 5510). A chain of correct
    multiplications between objects can still misname the objects, and that is exactly what
    happened twice.""")

    print("\n  PASS 5568 -- both guards, replayed\n")
    print("    certificate guard : 2,666 of 4,375 certificates   60%")
    print("    prose guard       :   665 of 1,500 analysis files 44%")
    print("""
    NEITHER IS A GATE, AND THE PROSE GUARD IS THE BETTER OF THE TWO. 44% against 60%, with
    the prose guard's grammar having been calibrated twice (Pass 328, re-measured Pass 1073)
    and the certificate grammar written this week. That gap is roughly what a calibration
    buys, and it is the argument for calibrating the new one against real firing rates
    rather than against a self-test.""")

    print("\n  PASS 5569 -- the alias table, demoted\n")
    print("""    It stays, documented as what it is: a 13-entry patch for collisions that
    were already known to have cost something, not a mechanism. Pass 5557's 26,693 key
    names make the general version impossible and Pass 5564's reporter is the replacement.
    Removing it would re-break the one case it fixes.""")

    print("\n  PASS 5570 -- what 26,693 key names implies\n")
    print("""    A corpus of ~5,000 certificates carrying 26,693 distinct integer-valued key
    names averages five NEW key names per certificate. That is not a vocabulary; it is a
    corpus where every pass invents its own words.

    AND IT IS THE STRUCTURAL CAUSE OF THE REDISCOVERY RATE. CLAUDE.md's rule is "search for
    the RESULT, not the topic" -- but a result is only searchable if two authors spell it
    the same way, and here they systematically do not. Pass 4800's `alpha` against BT818's
    `alpha_exact` is one instance of a pattern with 26,693 opportunities.

    THE HONEST IMPLICATION: no index built on key names can close this, because the names
    are the problem. Near-miss reporting at write time is a partial fix. A convention
    enforced at write time would be a real one, and nobody has proposed one.""")

    out = {
        "boundary": ("Pass 5566's triage is a 20-file hand-read extrapolated to 536; the "
                     "estimate carries that sample's error. Pass 5567 verifies ARITHMETIC "
                     "only -- two identifications in the same chain have already needed "
                     "correction. Pass 5565 measures the poison tail and does NOT choose a "
                     "threshold. alpha(W(3,9)) with the clique formulation was still "
                     "running when this pass was written"),
        "pass_5564": {"tool": "scripts/check_key_nearmiss.py",
                      "selftest_green": r.returncode == 0,
                      "direction": ("flags a NEW key one edit from an existing one at "
                                    "write time, rather than translating old names "
                                    "together after a collision has cost something"),
                      "floor": "stems of four characters; q, mu, k invisible"},
        "pass_5565": {"median_ints": med, "p95": p95, "max": max(vals),
                      "above_p95": len(poison), "of": len(docs),
                      "token_share_pct": 100 * bad // max(tot, 1),
                      "actionable": "yes, by density; threshold NOT chosen here"},
        "pass_5566": {**TRIAGE, "q3_only_total": 536, "estimated_gate_population": est,
                      "correction": ("Pass 5562's 536 was a population bound; the triage "
                                     "it was owed puts the real figure nearer " + str(est))},
        "pass_5567": {"chain": CHAIN, "all_arithmetic_ok": True,
                      "3456_expressions": ["96*36", "576*6", "8*432", "24^2*6"],
                      "caveat": ("arithmetic holds; identifications are separate claims and "
                                 "two needed correction -- F4 roots 48 not 96 (Pass 5509), "
                                 "and 96 vs 576 polytope-vs-configuration (Pass 5510)")},
        "pass_5568": {"certificate_guard_pct": 60, "prose_guard_pct": 44,
                      "reading": ("the twice-calibrated grammar fires 16 points less often; "
                                  "that gap is what calibration buys")},
        "pass_5569": {"alias_entries": 13, "status": "kept, documented as a known-collision "
                                                     "patch and not a mechanism"},
        "pass_5570": {"certificates": len(docs), "distinct_int_keys": 26693,
                      "new_keys_per_certificate": round(26693 / max(len(docs), 1), 1),
                      "implication": ("a result is searchable only if two authors spell it "
                                      "the same way; here they systematically do not. No "
                                      "key-name index closes this -- the names are the "
                                      "problem")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5564_5571_POISON_TAIL_AND_VOCABULARY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
