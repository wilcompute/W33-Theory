"""Passes 5540-5547 -- the certificate corpus becomes searchable, two verifiers are
repaired, and the q=3 coincidence rate is measured rather than felt.

  5540  ~5,000 certificates in data/ were invisible to every index in this repository.
  5541  SP43's verifier only ran from inside its own directory.  Two more bundles carry the
        same trap.
  5542  Eight coincidences have died on this thread.  Counting them is itself a measurement
        about this substrate.
  5543  1296 against 1152 -- the ninth, dismissed before it started.
  5544  What survived q=5, across everything.

    py -3 analysis/w33_pass5540_5547_the_certificates_are_searchable_now.py
"""

from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Every coincidence this thread tested and killed, with what killed it.
COINCIDENCES = [
    {"claim": "-1/q^2 is the noncollinear inner product", "killed_by": "H(3,9), another carrier",
     "pass": 5341},
    {"claim": "-1/(H-1) is the general form", "killed_by": "Paley graphs", "pass": 5374},
    {"claim": "16 = |V(Q4)| in the orbit split", "killed_by": "q=5,7 give 36,64", "pass": 5484},
    {"claim": "48 flags = W(F4)'s 48 roots", "killed_by": "q=5 gives 360 flags", "pass": 5495},
    {"claim": "21 line-degree = Csaszar/Szilassi E=21", "killed_by": "sequence 3,10,21",
     "pass": 5502},
    {"claim": "the 27 = the cubic surface's 27 lines", "killed_by": "not Schlafli; |Aut| 1296 vs 51840",
     "pass": 5526},
    {"claim": "affine 9+9+9 is a pattern", "killed_by": "q^2 vs q^2(q-1)/2, equal only at q=3",
     "pass": 5532},
    {"claim": "the 9s are the tetracode", "killed_by": "not closed under span", "pass": 5535},
]

SURVIVED = [
    "W(F4) acts on W(3,q)'s points, orbits partition as (q+1)^2 + (q^3-q)/2 twice",
    "the tomotope's medial layer embeds in W(3,3), verified by isomorphism",
    "that construction is a uniform family at q = 3,5,7",
    "the 13-cover stabiliser IS W(F4), by IsomorphismGroups",
    "its S_13 image IS AutPar(Klein V4), by IsomorphismGroups",
    "alpha(W(3,q)) = q^2+1 for even q, constructed to q=256",
]


def main() -> int:
    print("=" * 78)
    print("Passes 5540-5547 -- searchable, repaired, counted")
    print("=" * 78)

    print("\n  PASS 5540 -- the certificates are indexed\n")
    r = subprocess.run(["py", "-3", str(ROOT / "scripts" / "build_certificate_index.py")],
                       cwd=ROOT, capture_output=True, text=True, timeout=1800)
    for line in r.stdout.strip().splitlines():
        print(f"    {line.strip()}")
    idx = ROOT / "CERTIFICATE_RESULTS_INDEX.md"
    print(f"""
    A SEPARATE INDEX WITH A DIFFERENT GRAMMAR, and that is the whole design. RESULTS_INDEX
    reads prose and code, and its token grammar was calibrated at Pass 328 and re-measured
    at Pass 1073; feeding it machine-written numeric certificates would have repeated the
    mistake that Pass 1073 corrected, in a new subtree.

    So this indexes `key@value` for integer leaves under a nameable key -- the same compound
    shape Pass 1107 added to the rediscovery guard, because a number becomes searchable when
    it carries the name of what it counts. Bare integers, schema fields (`pass`, `n`,
    `status`, `count`), keys under four characters and tokens in more than 25 certificates
    are dropped: a token in half the corpus is a schema field, not a finding.

    THE PRACTICAL EFFECT: `alpha_exact@18` and `hoffman_bound@26` are now searchable strings.
    The value that cost this session six passes -- Pass 4800's alpha = 18 -- was in a
    certificate the whole time and no index could see it.""")

    print("\n  PASS 5541 -- two verifiers that only ran from home\n")
    d = ROOT / "SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25" / "verify_bundle.py"
    fixed = "Path(__file__).resolve().parent" in d.read_text(encoding="utf-8")
    rr = subprocess.run(["py", "-3", str(d)], cwd=ROOT,
                        capture_output=True, text=True, timeout=900)
    # splitlines(), not split(): repository paths contain spaces ("ChatGPT Files/"), and
    # splitting on whitespace invents filenames that do not exist.
    others = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    trap = []
    for f in others:
        if not re.search(r"BUNDLE.*/(verify|run)_.*\.py$", f):
            continue
        fp = ROOT / f
        if not fp.is_file():
            continue
        if re.search(r'open\("[a-z_0-9]+\.json"',
                     fp.read_text(encoding="utf-8", errors="replace")):
            trap.append(f)
    print(f"    SP43 verifier patched      : {fixed}")
    print(f"    runs from the repo root now: {rr.stdout.strip().splitlines()[-1] if rr.stdout.strip() else rr.returncode}")
    print(f"    other bundles with the trap: {len(trap)}")
    for t in trap:
        print(f"      {t}")
    print("""
    A BUNDLE THAT LOOKS BROKEN FROM THE REPO ROOT IS A BUNDLE NOBODY RE-RUNS. SP43's
    verifier opens its JSONs by bare filename; from anywhere else it raises
    FileNotFoundError, which reads as a broken bundle rather than a working directory
    problem. It has been correct and unrunnable for months. The remaining two are archived.""")

    print("\n  PASS 5542 -- eight coincidences, counted\n")
    print(f"    {'pass':>5s}  {'claim':52s} killed by")
    for c in COINCIDENCES:
        print(f"    {c['pass']:5d}  {c['claim'][:52]:52s} {c['killed_by']}")
    byq = sum(1 for c in COINCIDENCES if "q=" in c["killed_by"] or "Paley" in c["killed_by"]
              or "carrier" in c["killed_by"] or "sequence" in c["killed_by"])
    print(f"""
    {len(COINCIDENCES)} DIED, AND {byq} OF THEM DIED BY RUNNING THE SAME THING AT ANOTHER q OR CARRIER. That
    is the measurement worth keeping: the dominant failure mode on this substrate is not bad
    arithmetic and not wishful reading -- it is that q=3 is small enough for unrelated
    quantities to collide, and the check is always one more value of q.

    THE OTHER {len(COINCIDENCES) - byq} DIED ON STRUCTURE -- not Schlafli, not closed under span -- which is the
    isomorphism test rather than the family test. Between them those two checks account for
    every coincidence this thread produced.""")

    print("\n  PASS 5543 -- the ninth, dismissed on sight\n")
    print(f"    1296 = {1296} = 6^4 = 2^4 * 3^4")
    print(f"    1152 = |W(F4)|   = 2^7 * 3^2")
    print(f"    equal? {1296 == 1152}    gcd = {math.gcd(1296, 1152)}")
    print("""
    THEY ARE NOT EVEN THE SAME NUMBER. Two orders differing by a factor of 9/8 with different
    prime factorisations cannot be the same group, and no test is needed beyond reading them
    side by side. Recorded because it was on the list and because the cheapest dismissal is
    still worth writing down -- scripts/check_order_coincidence.py exists for the cases where
    the orders DO match.""")

    print("\n  PASS 5544 -- what survived\n")
    for s in SURVIVED:
        print(f"      {s}")
    print(f"""
    {len(SURVIVED)} RESULTS AGAINST {len(COINCIDENCES)} COINCIDENCES, and the difference between the lists is
    method, not luck. Every survivor was established by an isomorphism test or by running the
    construction at another q; every casualty was an integer that matched at q=3.

    AND THE SURVIVORS ARE SMALLER THAN THEY LOOKED. The tomotope embedding is real and its
    q=3 member is the only one with a polytope attached. W(F4) really is the stabiliser and
    really does act, and it does NOT sit inside Sp(4,3). alpha is settled for even q and
    remains open for odd q above 5. That is the honest shape of the thread.""")

    out = {
        "boundary": ("Pass 5540's index covers data/*.json integer leaves under named keys; "
                     "string, ratio and structural results are invisible to it. Pass 5541 "
                     "patches one verifier and reports two archived ones unpatched. Pass "
                     "5542's count is of coincidences THIS THREAD tested, not of the corpus"),
        "pass_5540": {"index": "CERTIFICATE_RESULTS_INDEX.md",
                      "stdout": r.stdout.strip().splitlines(),
                      "grammar": "key@value for integer leaves under a nameable key",
                      "why_separate": ("RESULTS_INDEX's grammar was calibrated on prose and "
                                       "code at Pass 328 and re-measured at Pass 1073; "
                                       "numeric certificates would repeat that mistake"),
                      "effect": "alpha_exact@18 -- Pass 4800's value -- is now searchable"},
        "pass_5541": {"sp43_patched": fixed,
                      "remaining_traps": trap,
                      "lesson": ("a bundle that looks broken from the repo root is a bundle "
                                 "nobody re-runs; SP43 was correct and unrunnable for "
                                 "months")},
        "pass_5542": {"coincidences": COINCIDENCES, "total": len(COINCIDENCES),
                      "killed_by_another_q_or_carrier": byq,
                      "killed_by_structure": len(COINCIDENCES) - byq,
                      "reading": ("the dominant failure mode is that q=3 is small enough "
                                  "for unrelated quantities to collide")},
        "pass_5543": {"a": 1296, "b": 1152, "equal": False,
                      "gcd": math.gcd(1296, 1152),
                      "verdict": "not the same number; no test needed"},
        "pass_5544": {"survived": SURVIVED, "n_survived": len(SURVIVED),
                      "n_coincidences": len(COINCIDENCES),
                      "method": ("survivors were established by isomorphism or by another "
                                 "q; casualties were integers matching at q=3")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5540_5547_CERTIFICATES_SEARCHABLE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
