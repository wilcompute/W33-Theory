"""Passes 5250-5253 -- closing the guard set's own gaps, and measuring it against the
other lane's guard rather than assuming the two are complementary.

  5250  Six guards had no self-test for eleven turns.  A zero from an untested checker is
        the absence of evidence formatted to look like the presence of it (Pass 5224), so
        those six were the part of the dashboard that meant nothing.  All six now have one.

  5251  The other lane built its own guard at Pass4996 and neither lane knew.  Are they
        redundant?  Measured, not assumed.

  5252  Seven cross-lane comparisons have now been run from this side.  What is the record
        when the two lanes DISAGREE?

  5253  Passes 5228-5229 produced a counterexample worth keeping executable: two graphs,
        one spectrum, two independence numbers.  That is now a guard.

    py -3 analysis/w33_pass5250_5253_the_guard_set_reconciled_across_lanes.py
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

NEWLY_TESTED = ["stale-boundaries", "shifted-adjacency-descendants", "tag-540-check",
                "pass-namespace-collision-guard", "topical-aliases", "rtl-folds"]

# The cross-lane comparisons run from THIS side, with what happened. Kept as data rather
# than prose so the count cannot drift from the claim (Pass 4923).
COMPARISONS = [
    {"pass": "4930s", "topic": "eight-cycle count", "mine": 540, "theirs": 1080,
     "agreed": False, "who_was_right": "theirs",
     "cause": "I divided by 2 twice"},
    {"pass": "4930s", "topic": "E6 root count as projective pairs", "mine": 52,
     "theirs": 36, "agreed": False, "who_was_right": "theirs",
     "cause": "root system not closed under negation in my construction"},
    {"pass": "4940s", "topic": "order-1440 firewall", "mine": None, "theirs": None,
     "agreed": True, "who_was_right": "both", "cause": ""},
    {"pass": "4940s", "topic": "Steiner quotient carrier", "mine": None, "theirs": None,
     "agreed": True, "who_was_right": "both", "cause": ""},
    {"pass": "5222", "topic": "H(3,9) independence number = 28", "mine": 28,
     "theirs": 28, "agreed": True, "who_was_right": "both", "cause": ""},
    {"pass": "5228", "topic": "Q(4,3) maximum coclique = 10", "mine": 10, "theirs": 10,
     "agreed": True, "who_was_right": "both", "cause": ""},
    {"pass": "5248", "topic": "Hoffman bound 28 on H(3,9)", "mine": 28, "theirs": 28,
     "agreed": True, "who_was_right": "both", "cause": ""},
]


def main() -> int:
    print("=" * 78)
    print("Passes 5250-5253 -- the guard set, reconciled")
    print("=" * 78)

    # ---- 5250 --------------------------------------------------------------
    print("\n  PASS 5250 -- the six untested guards\n")
    r = subprocess.run(["py", "-3", str(ROOT / "scripts" / "check_guard_selftests.py")],
                       cwd=ROOT, capture_output=True, text=True, timeout=1800)
    line = next((x.strip() for x in r.stdout.splitlines() if "self-tested" in x), "")
    print(f"    inventory now reports: {line}")
    print(f"    newly given a self-test: {', '.join(NEWLY_TESTED)}")
    print("""
    ONE OF THE SIX WAS NEVER UNTESTED. check_stale_boundaries.py had a working self-test the
    whole time, spelled --self-test, while the inventory runner probes for --selftest. A
    hyphen. The tool was green, the dashboard said unknown, and nothing anywhere disagreed
    because no third thing compared them. That is the same shape as the pre-commit config
    that did not parse for fourteen days: a monitoring layer reporting on itself.

    AND ONE SELF-TEST CANNOT TEST THE THING THAT MATTERS. rtl-folds needs yosys, which is
    absent here, so its self-test covers the module extractor and explicitly says the fold
    detection is NOT exercised. A green there means the guard will look at the right
    modules, not that it can still detect a fold. Written into the output so nobody reads
    the green as more than it is.""")

    # ---- 5251 --------------------------------------------------------------
    print("\n  PASS 5251 -- my guards versus the other lane's Pass4996 firewall\n")
    spec = importlib.util.spec_from_file_location(
        "fw", ROOT / "tools" / "w33_stale_claim_firewall.py")
    fw = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(fw)
    except SystemExit:
        pass
    theirs = set(fw.live_paths())
    cfg = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    pats = [(h["id"], re.compile(h["files"]))
            for rp in cfg["repos"] for h in rp.get("hooks", []) if h.get("files")]
    covered = {p for p in theirs if any(rx.search(p) for _, rx in pats)}
    mypy_files = list((ROOT / "analysis").glob("*.py"))
    theirs_reads_py = len([p for p in mypy_files if p.as_posix() in theirs])
    fwrun = subprocess.run(["py", "-3", str(ROOT / "tools" / "w33_stale_claim_firewall.py")],
                           cwd=ROOT, capture_output=True, text=True)

    print(f"    their rules                          : {len(fw.RULES)} (claim-specific regexes)")
    print(f"    their live surfaces                  : {len(theirs)}")
    print(f"      within my guards' file patterns    : {len(covered)}")
    print(f"    my analysis/*.py corpus              : {len(mypy_files):,}")
    print(f"      their firewall reads               : {theirs_reads_py}")
    print(f"    their firewall exit code right now   : {fwrun.returncode}")

    print(f"""
    NOT REDUNDANT, AND NOT COMPLEMENTARY IN THE WAY I EXPECTED. Their firewall is PRECISION
    tooling: {len(fw.RULES)} regexes naming {len(fw.RULES)} specific retracted claims, aimed at {len(theirs)} curated live
    surfaces -- the published manuscripts and theorem pages -- and fail-closed. Mine are
    RECALL tooling: generic patterns over the whole working corpus. Their firewall reads
    {theirs_reads_py} of my {len(mypy_files):,} analysis scripts. So a stale claim that never reaches a published
    surface is invisible to them, and a specific retracted claim phrased in wording my
    generic patterns miss is invisible to me. Two different failure modes, neither
    subsumed.

    AND THEIR FIREWALL IS CURRENTLY RED. Exit code {fwrun.returncode}, two violations, both on the same rule
    (tritangent_support8_minimum) and both on Pass5000-5007 surfaces. Reported here rather
    than acted on -- it is their rule and their claim, and per the ownership protocol the
    lane that owns a result owns its corrections. Flagging it across the boundary IS the
    protocol.

    WHAT I ALSO FOUND: their firewall has no self-test. By the argument in Pass 5224 that
    makes its zero uninterpretable -- except it is not currently returning zero, so this is
    a latent problem rather than an active one.""")

    # ---- 5252 --------------------------------------------------------------
    print("\n  PASS 5252 -- the record when the lanes disagree\n")
    dis = [c for c in COMPARISONS if not c["agreed"]]
    agr = [c for c in COMPARISONS if c["agreed"]]
    mine_right = [c for c in dis if c["who_was_right"] == "mine"]
    print(f"    {'pass':>6s} {'topic':38s} {'agreed':>7s} {'right':>7s}")
    for c in COMPARISONS:
        print(f"    {c['pass']:>6s} {c['topic']:38s} "
              f"{('yes' if c['agreed'] else 'NO'):>7s} {c['who_was_right']:>7s}")
    print(f"""
    {len(COMPARISONS)} comparisons, {len(agr)} agreeing, {len(dis)} disagreeing -- and in {len(dis)} of {len(dis)} disagreements the
    other lane was right and the error was mine. Both were arithmetic in my own
    construction, not a difference of interpretation: a factor of two applied twice, and a
    root system I built without closing it under negation.

    THE RULE THAT FOLLOWS, stated as a prior rather than a policy: when a cross-lane number
    disagrees, the base rate says re-derive MINE first. {len(mine_right)} of {len(dis)} disagreements have gone the
    other way. That is a small sample and it is the entire sample, and a prior built on two
    events is weak -- but it is stronger than the instinct it replaces, which was to assume
    the other lane had mis-stated something.

    THE HONEST LIMIT: this counts comparisons I RAN, so it cannot see disagreements neither
    lane noticed. The 21 percent uncited-collision rate Pass 328 measured is the real
    denominator, and it is not this one.""")

    # ---- 5253 --------------------------------------------------------------
    print("\n  PASS 5253 -- the counterexample is now executable\n")
    st = subprocess.run(["py", "-3", str(ROOT / "scripts" / "check_spectral_overreach.py"),
                         "--selftest"], cwd=ROOT, capture_output=True, text=True)
    sweep = subprocess.run(
        ["py", "-3", str(ROOT / "scripts" / "check_spectral_overreach.py")]
        + [str(p) for p in sorted((ROOT / "analysis").glob("w33_pass5*.py"))[:400]],
        cwd=ROOT, capture_output=True, text=True)
    nfind = next((x for x in sweep.stdout.splitlines() if "candidate" in x), "").strip()
    print(f"    check_spectral_overreach --selftest  : "
          f"{'green (7/7)' if st.returncode == 0 else 'FAILING'}")
    print(f"    swept over recent passes             : {nfind}")
    print("""
    IT FLAGS A VERB, NOT A TOPIC. "Hoffman gives alpha <= 10" is the correct statement of
    the ratio bound and appears throughout this corpus; flagging it would fire on every
    legitimate use and the guard would be switched off inside a day. What is flagged is
    determines / equals / is fixed by. Two of the seven self-test cases are correct bound
    statements that must NOT flag, and they are the cases that make it usable.

    WHAT IT CANNOT DO, said plainly: it reads sentences, not mathematics. The counterexample
    behind it -- W(3,3) and Q(4,3) both SRG(40,12,2,4) with alpha 7 and 10 -- took two lanes
    and four passes to assemble, and no regex was ever going to find that. The guard catches
    the RESTATEMENT of an error, never the error.""")

    out = {
        "boundary": ("Pass 5250: rtl-folds' self-test covers the module extractor only -- "
                     "yosys is absent and fold detection is NOT exercised. Pass 5251 "
                     "compares FILE COVERAGE, not detection power; 'within my file "
                     "patterns' means a guard would scan the file if staged, not that it "
                     "would catch what their rules catch. Pass 5252 counts only "
                     "comparisons this lane RAN, so it cannot see disagreements neither "
                     "lane noticed, and a prior built on 2 disagreements is weak. Pass "
                     "5253's guard catches restatements of the error, never the error"),
        "pass_5250": {"newly_self_tested": NEWLY_TESTED, "inventory": line,
                      "finding": ("check_stale_boundaries had a working self-test all "
                                  "along, spelled --self-test while the runner probes "
                                  "--selftest; both spellings now accepted"),
                      "untestable_here": "rtl-folds fold detection (needs yosys)"},
        "pass_5251": {"their_rules": len(fw.RULES), "their_surfaces": len(theirs),
                      "their_surfaces_in_my_patterns": len(covered),
                      "my_analysis_py": len(mypy_files),
                      "their_firewall_reads_my_py": theirs_reads_py,
                      "their_exit_code": fwrun.returncode,
                      "verdict": ("not redundant: theirs is precision tooling on published "
                                  "surfaces, mine is recall tooling on the working corpus; "
                                  "neither subsumes the other"),
                      "flagged_across_boundary": ("their firewall is currently RED with 2 "
                                                  "violations of tritangent_support8_"
                                                  "minimum on Pass5000-5007 surfaces; "
                                                  "their rule, their claim, their call"),
                      "also": "their firewall has no self-test"},
        "pass_5252": {"comparisons": COMPARISONS, "total": len(COMPARISONS),
                      "agreed": len(agr), "disagreed": len(dis),
                      "mine_right_in_disagreements": len(mine_right),
                      "prior": ("when a cross-lane number disagrees, re-derive MINE first "
                               "-- 0 of 2 disagreements went my way")},
        "pass_5253": {"guard": "scripts/check_spectral_overreach.py",
                      "selftest_green": st.returncode == 0,
                      "counterexample": ("W(3,3) and Q(4,3) are both SRG(40,12,2,4); "
                                         "alpha is 7 and 10"),
                      "flags": "determination verbs, never bounding language",
                      "sweep": nfind},
    }
    fp = ROOT / "data" / "PART_W33_PASS5250_5253_GUARDS_RECONCILED.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
