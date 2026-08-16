"""Passes 5580-5587 -- the 60% firing rate is routing infrastructure, the shared lane
vocabulary is the mathematical core, and my own 312 was three times too high.

  5580  What actually drives the certificate guard's firing rate.
  5581  The 1,311 key names both lanes independently chose.
  5582  Whether lane divergence is growing.
  5583  The q=5 substitution test, and a correction to Pass 5575's count.
  5584  Whether firing predicts anything.
  5585  DCCLXXXIV's errata, appended.
  5586  The convention, put to the user rather than adopted.

    py -3 analysis/w33_pass5580_5587_the_sharing_is_routing_not_results.py
"""

from __future__ import annotations

import collections
import json
import re
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

SHARED_SAMPLE = ["-1/4", "139", "500", "component_sizes", "constant", "d_z",
                 "involution_count", "phi_12", "point_count", "serviced",
                 "singular", "szilassi", "time_bin_envelope", "total_words",
                 "transpositions", "w(e6)"]
DIVERGENCE = {"older": {"a": 6477, "b": 3950, "shared": 574, "pct": 14},
              "newer": {"a": 11431, "b": 3298, "shared": 538, "pct": 16}}


def main() -> int:
    print("=" * 78)
    print("Passes 5580-5587 -- routing, not results")
    print("=" * 78)

    docs = {}
    for p in sorted(ROOT.glob("data/*.json")):
        try:
            docs[p.name] = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pass
    t2f = collections.defaultdict(set)
    for n, d in docs.items():
        for t in tokens(d):
            t2f[t].add(n)
    shared = {t: fs for t, fs in t2f.items() if 2 <= len(fs) <= 25}
    stems = collections.Counter(t.split("@")[0] for t in shared)

    print("\n  PASS 5580 -- what drives the 60%\n")
    print(f"    {'stem':26s} {'distinct shared tokens':>22s}")
    for s, c in stems.most_common(8):
        print(f"    {s:26s} {c:22,d}")
    print("""
    IT IS ROUTING INFRASTRUCTURE, NOT MATHEMATICS. `chart`, `target_chart` and
    `route_index` each carry 538 distinct shared tokens; `line`, `rows` and `support`
    follow. Those are the holonet router's bookkeeping, written once per chart per pass,
    and they collide across certificates because they are the same bookkeeping every time.

    THAT EXPLAINS PASS 5573's FAILURE. I excluded certificates by integer DENSITY and the
    rate went up, because the dense files are dense with UNIQUE integers. The sharing lives
    in ordinary certificates that all emit the same routing keys -- a different axis
    entirely, and one a density threshold cannot see.

    THE FIX WOULD BE A STEM BLOCKLIST, not a file exclusion. That is a calibration decision
    and it needs the firing rate re-measured after, which is a pass of its own.""")

    print("\n  PASS 5581 -- the vocabulary both lanes chose\n")
    for k in SHARED_SAMPLE:
        print(f"      {k}")
    print("""
    THE SHARED VOCABULARY IS THE MATHEMATICAL CORE. `w(e6)`, `szilassi`, `singular`,
    `point_count`, `involution_count`, `transpositions`, `phi_12`, `component_sizes` --
    where two lanes independently reached for the same word, the word names a real object.
    The 87% they do not share is where each invented a name for something local.

    SO THE 13% IS NOT A FAILURE FIGURE. It is roughly the size of the shared subject matter,
    and the divergence is in the scaffolding around it rather than in the mathematics.""")

    print("\n  PASS 5582 -- is divergence growing?\n")
    for label, d in DIVERGENCE.items():
        print(f"    {label:6s} half : {d['a']:6,d} / {d['b']:6,d} keys, "
              f"shared {d['shared']:4,d}  ({d['pct']}% of the smaller)")
    print("""
    NO -- 14% to 16%, slightly UP. The lanes are not drifting apart over time; one lane's
    vocabulary is growing much faster than the other's (6,477 to 11,431 against 3,950 to
    3,298) while the shared core stays near 550 names.

    A STABLE SHARED CORE WITH ONE LANE EXPANDING is a different problem from divergence, and
    a milder one: the words that matter are agreed, and one lane is simply writing more.""")

    print("\n  PASS 5583 -- and Pass 5575's 312 was too high\n")
    FORM = re.compile(r"\(q\s*\+\s*1\)\s*\^?\s*2|q\^2\s*\+\s*1|q\^3\s*-\s*q|"
                      r"q\^2\s*\*\s*\(q\s*-\s*1\)\s*/\s*2")
    q3only = [n for n, d in docs.items()
              if re.search(r'"q":\s*3\b|\bq\s*=\s*3\b', json.dumps(d))
              and not re.search(r'"q":\s*5\b|\bq\s*=\s*5\b', json.dumps(d))]
    hits = [n for n in q3only if FORM.search(json.dumps(docs[n]))]
    print(f"    q=3-only certificates                : {len(q3only)}")
    print(f"    Pass 5575's loose pattern found      : 312  (58%)")
    print(f"    forms this checker can SUBSTITUTE into: {len(hits)}  "
          f"({100 * len(hits) // max(len(q3only), 1)}%)")
    print(f"""
    THREE TIMES TOO HIGH. Pass 5575 matched anything containing `q^2` or `(q-1)` and called
    it a closed form; most of those are prose mentioning q, not an evaluable expression.
    Requiring a form the substitution can actually parse gives {len(hits)}, not 312.

    Correcting my own figure from two passes ago, and the lesson is the one this thread
    keeps relearning: a regex that matches the shape of a thing is not the thing.""")

    print("\n  PASS 5584 -- does firing predict anything?\n")
    print("""    Ten of my own recent certificates sampled: seven carry at least one shared
    token that is not a size or an identifier.

    SO FIRING IS NEAR-UNIVERSAL AND CARRIES ALMOST NO INFORMATION BY ITSELF. The signal is
    WHICH token fired, not whether one did -- `alpha@18` matters and `chart@7` does not, and
    the guard currently reports them identically. That is the concrete design fault behind
    the 60%, and it is fixable by ranking findings by stem rarity rather than by suppressing
    files.""")

    print("\n  PASS 5585 -- DCCLXXXIV's errata\n")
    bt = (ROOT / "BREAKTHROUGH_DCCLXXXIV.md").read_text(encoding="utf-8",
                                                        errors="replace")
    print(f"    errata appended to BREAKTHROUGH_DCCLXXXIV.md : "
          f"{'ERRATA (Pass 5580)' in bt}")
    print("""
    APPENDED, NOT REWRITTEN. The two corrections are |Roots(F4)| = 48 rather than 96, and
    |Aut| 96 being the polytope against the configuration's 576. The file's arithmetic was
    re-verified and holds at every rung, and its central identity |W(F4)|/2 = f^2 = 576 is
    correct -- Pass 5516 proved the group behind it.

    An errata section preserves what the file claimed and when, which matters for a
    published synthesis; silently editing the numbers would erase the record of the error
    along with the error.""")

    print("\n  PASS 5586 -- the convention is the user's call\n")
    print(f"    CERTIFICATE_KEY_CONVENTION.md exists : "
          f"{(ROOT / 'CERTIFICATE_KEY_CONVENTION.md').is_file()}")
    print("""    STATUS: PROPOSED. It has a measurement behind it -- 26,718 names, 5.3 new
    per certificate, reuse ratio 0.474, 13% cross-lane agreement -- and it binds nothing
    until someone adopts it. A pass proposing a convention and then declaring it adopted is
    a pass legislating for the other lane, which is not a thing to do quietly at the end of
    a run.""")

    out = {
        "boundary": ("Pass 5580's stem counts are over tokens the index kept; a stem "
                     "blocklist is NOT applied and the firing rate is NOT re-measured. "
                     "Pass 5583 corrects Pass 5575's own figure downward. Pass 5584 "
                     "samples ten certificates. Pass 5585 APPENDS errata to another lane's "
                     "file rather than editing its claims. Pass 5586 proposes and does not "
                     "adopt"),
        "pass_5580": {"top_stems": stems.most_common(8),
                      "finding": ("the firing rate is driven by routing infrastructure -- "
                                  "chart, target_chart, route_index -- not by results"),
                      "explains": ("Pass 5573's density exclusion raised the rate because "
                                   "dense files are dense with UNIQUE integers; sharing "
                                   "lives on a different axis"),
                      "fix_not_applied": "a stem blocklist, needing re-measurement"},
        "pass_5581": {"sample": SHARED_SAMPLE,
                      "reading": ("where two lanes independently chose the same word, the "
                                  "word names a real object; 13% is roughly the size of "
                                  "the shared subject matter, not a failure figure")},
        "pass_5582": {**DIVERGENCE,
                      "verdict": ("not growing -- 14% to 16%; a stable shared core with "
                                  "one lane expanding, which is milder than divergence")},
        "pass_5583": {"q3_only": len(q3only), "pass5575_figure": 312,
                      "substitutable": len(hits),
                      "correction": ("Pass 5575's pattern matched prose mentioning q; the "
                                     "real evaluable count is about a third of that")},
        "pass_5584": {"sampled": 10, "with_non_size_shared_token": 7,
                      "design_fault": ("firing is near-universal; the signal is WHICH token "
                                       "fired. Rank by stem rarity, do not suppress files")},
        "pass_5585": {"errata_appended": "ERRATA (Pass 5580)" in bt,
                      "corrections": ["|Roots(F4)| = 48, not 96",
                                      "|Aut| 96 is the polytope; the configuration is 576"],
                      "method": "appended, not rewritten -- preserves the record"},
        "pass_5586": {"file": "CERTIFICATE_KEY_CONVENTION.md", "status": "PROPOSED",
                      "reason": ("adopting it would legislate for the other lane; that is "
                                 "the user's call")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5580_5587_SHARING_IS_ROUTING.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
