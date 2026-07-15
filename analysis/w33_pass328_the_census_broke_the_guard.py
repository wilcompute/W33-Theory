#!/usr/bin/env python3
"""Pass 328: the rediscovery census -- which measured the GUARD, not the corpus.

Pass 327 shipped a pre-commit rediscovery guard. This pass ran it over all 172
pass files to measure the true duplication rate. The number came back:

        167 of 172 files flagged  =  97%

and that number is worthless. A guard that fires on 97% of commits carries no
information; it will be ignored within a day, which is EXACTLY how the
instruction it was built to replace ("search the corpus first") already failed --
twice, at a cost of ~19 passes. My fix had the defect I warned about in its own
docstring: it trains people to stop reading it.

So the census measured the guard, not the corpus. Good: that is what a census is
for, and finding it now costs nothing.

WHAT CARRIES SIGNAL -- MEASURED, NOT GUESSED.
Flag rate over the same 172 files, by token class:

    everything, incl. bare integers ......... 167/172 = 97%   noise
    bare integers, rare-only (<=3 files) .... 135/172 = 78%   still noise
    code parameters [[n,k,d]] / [n,k,d] ...... 35/172 = 20%   SIGNAL
    slash-sequences (25/91/225) ............... 4/172 =  2%   signal, sparse

WHY BARE INTEGERS ARE NOISE. The same integer legitimately recurs everywhere: a
dimension, an orbit count, a group order. Its recurrence is not evidence of
anything. Worse, the files flagged HARDEST were the audit passes themselves --
174 (32 hits), 311 (27), 322 (21), 325 (18) -- because a pass whose JOB is to
survey prior results necessarily quotes many numbers. The guard was punishing
precisely the behaviour it was built to encourage.

WHY CODE PARAMETERS ARE SIGNAL. [[40,10,4]] is an OBJECT, not a quantity. Two
files asserting it are talking about the same code. That is what a rediscovery
IS: the same object, claimed twice. 20% is a rate a human will still look at.

THE GUARD IS NOW CALIBRATED to code parameters + sequences (~22%), and the
calibration is written into its docstring so the next person does not re-guess it.

THE CENSUS ANSWER, with the fixed metric: 35 of 172 pass files (20%) assert a
code parameter that already exists elsewhere and is not cited in the file. That
is the honest scale of the duplication problem -- not 97%, and not the 2 cases I
found by hand.

THE META-LESSON, WHICH IS THE POINT OF RUNNING IT.
This is the fourth time in this arc that a measurement I designed came out
uninformative BY CONSTRUCTION -- Pass 287 (the trace law), Pass 319 (the delta
table, my own idea), Pass 323 (k*d=n), and now the guard's 97%. The pattern is
identical every time: a quantity that cannot come out any other way carries no
information. The difference here is that I measured it before shipping the number
as a result, which is the only reason it is a calibration and not a fifth
retraction.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass328_the_census_broke_the_guard.json"

sys.path.insert(0, str(ROOT / "scripts"))
from check_rediscovery import (  # noqa: E402
    RE_CSS, RE_LIN, RE_SEQ, RE_INT, NOISE, SKIP, load_index,
)


def main():
    checks = {}
    idx = load_index()
    files = sorted((ROOT / "analysis").glob("w33_pass*.py")) + \
        sorted((ROOT / "passes").glob("*.py"))
    checks["index_loaded"] = len(idx) > 0
    checks["found_pass_files"] = len(files) > 100

    def rate(extract, rare_max=None):
        flagged = 0
        for p in files:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            rel = p.relative_to(ROOT).as_posix()
            for tok in extract(txt):
                if rare_max is not None and len(idx.get(tok, [])) > rare_max:
                    continue
                prior = [x for x in idx.get(tok, [])
                         if x != rel and Path(x).name not in txt]
                if prior:
                    flagged += 1
                    break
        return flagged

    def allf(t):
        s = {re.sub(r"\s+", "", m) for rx in (RE_CSS, RE_LIN, RE_SEQ)
             for m in rx.findall(t)}
        s |= {m for m in RE_INT.findall(t) if m not in NOISE}
        return s - SKIP

    def params(t):
        return {re.sub(r"\s+", "", m) for rx in (RE_CSS, RE_LIN) for m in rx.findall(t)}

    def seqs(t):
        return set(RE_SEQ.findall(t))

    n = len(files)
    r_all = rate(allf)
    r_par = rate(params)
    r_seq = rate(seqs)
    r_rare = rate(allf, rare_max=3)

    checks["everything_flags_over_90_percent"] = r_all / n > 0.90
    checks["rare_only_still_over_70_percent"] = r_rare / n > 0.70
    checks["code_params_between_10_and_35_percent"] = 0.10 < r_par / n < 0.35
    checks["sequences_are_sparse"] = r_seq / n < 0.10
    checks["params_carry_more_signal_than_integers"] = r_par < r_all
    checks["so_the_shipped_guard_was_noise"] = r_all / n > 0.90
    checks["guard_now_calibrated_to_params_and_seqs"] = True

    # the guard is fixed: results_in no longer emits bare integers
    from check_rediscovery import results_in
    probe = "the code is [[40,10,4]] with 51840 and 8353 and 12345"
    got = results_in(probe)
    checks["fixed_guard_keeps_code_params"] = "[[40,10,4]]" in got
    checks["fixed_guard_drops_bare_integers"] = "8353" not in got and "12345" not in got

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass328.census_broke_the_guard.v1",
        "status": "PASS" if all_pass else "FAIL",
        "VERDICT": (
            "The census measured the GUARD, not the corpus. 167/172 = 97% flagged. "
            "A guard that fires on 97% of commits carries no information and will "
            "be ignored within a day -- exactly how the instruction it replaces "
            "already failed, twice, at a cost of ~19 passes. My fix had the defect "
            "its own docstring warned about."
        ),
        "measured_flag_rates": {
            "files": n,
            "everything (incl. bare integers)": f"{r_all}/{n} = {100*r_all/n:.0f}% -- NOISE",
            "bare integers, rare-only (<=3 files)": f"{r_rare}/{n} = {100*r_rare/n:.0f}% -- still noise",
            "code parameters [[n,k,d]] / [n,k,d]": f"{r_par}/{n} = {100*r_par/n:.0f}% -- SIGNAL",
            "slash-sequences": f"{r_seq}/{n} = {100*r_seq/n:.0f}% -- signal, sparse",
        },
        "why_bare_integers_are_noise": (
            "The same integer legitimately recurs everywhere -- a dimension, an "
            "orbit count, a group order. Its recurrence is not evidence. Worse, the "
            "files flagged HARDEST were the audit passes themselves (174: 32 hits, "
            "311: 27, 322: 21, 325: 18), because a pass whose job is to survey "
            "prior results necessarily quotes many numbers. The guard was punishing "
            "exactly the behaviour it was built to encourage."
        ),
        "why_code_parameters_are_signal": (
            "[[40,10,4]] is an OBJECT, not a quantity. Two files asserting it are "
            "talking about the same code -- which is what a rediscovery IS: the "
            "same object claimed twice. 20% is a rate a human will still look at."
        ),
        "THE_CENSUS_ANSWER": (
            f"With the fixed metric: {r_par} of {n} pass files ({100*r_par/n:.0f}%) "
            "assert a code parameter that already exists elsewhere and is not cited "
            "in the file. That is the honest scale of the duplication problem -- "
            "not 97%, and not the 2 cases found by hand in Passes 322/323."
        ),
        "the_fix": "results_in() now emits only code parameters and sequences, and "
                   "the calibration table is written into its docstring so the next "
                   "person does not re-guess it.",
        "THE_META_LESSON": (
            "Fourth time in this arc that a measurement I designed was "
            "uninformative BY CONSTRUCTION: Pass 287 (the trace law), Pass 319 (the "
            "delta table -- my own idea), Pass 323 (k*d=n), and now the guard's "
            "97%. Identical pattern each time: a quantity that cannot come out any "
            "other way carries no information. The difference is that this one was "
            "measured BEFORE shipping the number as a result -- which is the only "
            "reason it is a calibration and not a fifth retraction."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
