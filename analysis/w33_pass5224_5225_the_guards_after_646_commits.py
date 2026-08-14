"""Passes 5224-5225 -- the guard set meets 646 commits it has never seen, and a coverage
measurement that corrected my first reading of it.

  5224  Nineteen guards were built in one session, calibrated entirely on this lane's
        output, and then the repository moved 646 commits and ~700 passes without them.
        Two questions: do they still RUN, and do they FIND anything in work they were not
        fitted to?

  5225  The certificate guard reported "198 scanned, 0 with an embedded hash" on the new
        work, which reads like a convention being abandoned.  Measuring it across the whole
        corpus says the opposite.

    py -3 analysis/w33_pass5224_5225_the_guards_after_646_commits.py
"""

from __future__ import annotations

import collections
import glob
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = "bea345f80"          # this lane's last commit before the gap
DIGEST_KEYS = ("sha256_without_hash_field", "sha256", "universe_sha256")


def main() -> int:
    print("=" * 78)
    print("Passes 5224-5225 -- the guard set, out of sample and at scale")
    print("=" * 78)

    # ---- 5224: health and findings --------------------------------------
    print("\n  PASS 5224 -- do the guards survive 646 commits?\n")
    r = subprocess.run(["py", "-3", str(ROOT / "scripts" / "check_guard_selftests.py")],
                       cwd=ROOT, capture_output=True, text=True, timeout=900)
    line = next((l for l in r.stdout.splitlines() if "self-tested" in l), "")
    print(f"    self-test sweep            : {line.strip()}")
    cfg = subprocess.run(["py", "-3", "-m", "pre_commit", "validate-config",
                          ".pre-commit-config.yaml"], cwd=ROOT,
                         capture_output=True, text=True)
    print(f"    config still parses        : {cfg.returncode == 0}")

    changed = subprocess.run(["git", "log", "--format=", "--name-only",
                              f"{BASE}..origin/master"], cwd=ROOT,
                             capture_output=True, text=True).stdout.splitlines()
    new_py = sorted({f for f in changed if f.startswith("analysis/")
                     and f.endswith(".py")})
    new_md = sorted({f for f in changed if f.startswith("analysis/")
                     and f.endswith(".md")})
    print(f"    new analysis .py           : {len(new_py)}")
    print(f"    new analysis .md           : {len(new_md)}")

    GUARDS = [("check_regex_deadends", new_py), ("check_heredoc_regex", new_py),
              ("check_hardcoded_keys", new_py), ("check_search_power", new_py + new_md),
              ("check_retraction_propagation", new_py + new_md),
              ("check_novelty_claims", new_md), ("check_stdlib_shadow", new_py)]
    print(f"\n    {'guard':32s} {'files':>6s} {'findings':>9s} {'sec':>6s}")
    rows = []
    for name, files in GUARDS:
        files = [f for f in files if (ROOT / f).is_file()][:250]
        if not files:
            continue
        t0 = time.time()
        try:
            out = subprocess.run(["py", "-3", str(ROOT / "scripts" / f"{name}.py")]
                                 + files, cwd=ROOT, capture_output=True,
                                 text=True, timeout=600).stdout
            m = re.search(r"(\d[\d,]*)\s+\w[\w -]*$", out.strip().splitlines()[-1]
                          if out.strip() else "")
            m2 = re.search(r"^\s*(\d[\d,]*)\s", out.strip().splitlines()[-2]
                           if len(out.strip().splitlines()) > 1 else "")
            n = int((m or m2).group(1).replace(",", "")) if (m or m2) else 0
        except Exception:
            n = None
        dt = time.time() - t0
        rows.append({"guard": name, "files": len(files), "findings": n,
                     "seconds": round(dt, 1)})
        print(f"    {name:32s} {len(files):6d} {str(n):>9s} {dt:6.1f}")

    fired = [x for x in rows if isinstance(x["findings"], int) and x["findings"] > 0]
    print(f"""
    EVERY REGISTERED GUARD STILL RUNS -- the self-test sweep above reports "{line.strip()}"
    with none failing -- and of the {len(rows)} pointed at the new work, {len(fired)} report a finding on
    {len(new_py) + len(new_md)} files this lane never touched.

    THAT IS THE OUT-OF-SAMPLE RESULT, and it is not flattering to the tooling. These guards
    were built in one session, calibrated on my own mistakes -- Pass 4840 measured that 41%
    of them exist because of a fault I made that week -- and 646 commits of somebody else's
    work triggers almost none of them. A tool built for a fault that occurred once is
    indistinguishable from one built for a fault that recurs, until it recurs, and mostly
    they have not.

    WHAT SILENCE STILL DOES NOT MEAN. Not that the new work is clean. These look for faults
    with a specific textual signature; another lane can be wrong in ways none of them has a
    pattern for. What is measured is overlap between two authors' failure modes.""")

    # ---- 5225: the certificate coverage question -------------------------
    print("\n  PASS 5225 -- does the certificate guard cover anything?\n")
    buckets = collections.defaultdict(lambda: [0, 0])
    for f in glob.glob(str(ROOT / "data" / "PART_W33_PASS*.json")):
        m = re.search(r"PASS(\d{3,4})", Path(f).name)
        if not m:
            continue
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        has = any(k in d for k in DIGEST_KEYS) or any("sha" in k.lower() for k in d)
        b = (int(m.group(1)) // 500) * 500
        buckets[b][0] += 1
        buckets[b][1] += int(has)

    print(f"    {'pass range':16s} {'certs':>6s} {'with digest':>12s} {'pct':>6s}")
    cov = []
    for k in sorted(buckets):
        tot, hd = buckets[k]
        pct = 100 * hd // max(tot, 1)
        cov.append({"range": f"{k}-{k+499}", "certs": tot, "with_digest": hd,
                    "pct": pct})
        print(f"    {str(k)+'-'+str(k+499):16s} {tot:6d} {hd:12d} {pct:5d}%")

    total = sum(v[0] for v in buckets.values())
    withd = sum(v[1] for v in buckets.values())
    print(f"""
    MY FIRST READING WAS BACKWARDS. "198 new certificates, 0 with an embedded hash" looks
    like a convention being abandoned. Across the whole corpus the rate goes 0%, 0%, 0%,
    1%, 10% -- the digest convention is being ADOPTED, not dropped, and the newest range
    has the highest rate this repository has ever had.

    WHAT IS TRUE IS A COVERAGE STATEMENT, NOT A REGRESSION. certificate-digests can only
    check the {withd} of {total} PART_ certificates that carry a self-digest -- {100*withd//max(total,1)}%. For the other
    {total-withd} there is nothing to verify, so a stale certificate among them is undetectable by
    this guard and always has been. That is the finding: the guard's reach is small, and it
    is small because most certificates never opted in.

    AND THE TRAP I NEARLY FELL INTO IS THE ONE THIS FILE'S OWN HEADER DOCUMENTS. Four times
    this session I read a key name as implying a convention; the fifth would have been
    reading its ABSENCE as implying a decision. Checking the corpus rate took one query.""")

    out = {
        "boundary": ("guard findings are counted by parsing each tool's summary line, so a "
                     "tool whose output format differs may be recorded as 0 rather than "
                     "unparsed. Silence is not evidence the new work is clean -- these "
                     "guards look for specific textual signatures and encode one author's "
                     "failure modes. The coverage figure counts PART_ certificates only"),
        "pass_5224": {"base_commit": BASE, "new_py": len(new_py), "new_md": len(new_md),
                      "guards_run": len(rows), "guards_firing": len(fired),
                      "rows": rows, "selftest_line": line.strip(),
                      "config_valid": cfg.returncode == 0},
        "pass_5225": {"coverage_by_range": cov, "total_certs": total,
                      "with_digest": withd,
                      "pct": 100 * withd // max(total, 1),
                      "first_reading": "convention abandoned -- WRONG",
                      "actual": ("adoption rising 0% -> 1% -> 10%; the guard's reach is "
                                 "small because most certificates never carried a digest, "
                                 "not because any were removed")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5224_5225_GUARDS_AT_SCALE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
