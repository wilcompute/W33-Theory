#!/usr/bin/env python3
"""
The control arm, made runnable end-to-end through the existing estimator path. The demonstrator
protocol (holonet_demonstrator_protocol_v1.tex) measures the q=3 Witting fabric and expects contextual
fraction 1/10; the parity-control companion (holonet_parity_control.tex) adds the positive control: the
SAME apparatus on an even-order fabric must read CF=0, because an explicit ovoid (w33_ovoid_construct.py)
gives a noncontextual model satisfying every context. This witness closes the loop by running the
demonstrator's OWN estimators (bt1901 normal-window, bt1904 exact-binomial) on BOTH arms and showing
they return opposite verdicts on the same one-tenth hypothesis:

    positive arm (q=3 fabric)   -> CF ~ 1/10  -> COMPATIBLE with 1/10, INCOMPATIBLE with 0
    control  arm (even-q fabric)-> CF ~ 0      -> INCOMPATIBLE with 1/10, COMPATIBLE with 0

That is the two-arm discriminator: one estimator, two fixtures, geometry-forced opposite answers. A
systematic that faked a 1/10 signal on the odd fabric would have to also fake it on the even fabric to
escape detection, but the even fabric has an explicit ovoid model forbidding any contextual excess.

How the control fixture is built: the even-q ovoid assigns exactly one firing ray to every context, so
the noncontextual prediction has ZERO contextual excess over the classical bound. In the demonstrator's
simplified raw-shot schema (where the estimator reads the dark/loss-corrected signal click rate as the
contextual fraction) that means the signal rows click only at the dark-count baseline. The fixture
therefore encodes the ovoid model directly: signal click rate = dark rate => corrected CF ~ 0. The
fixture is written in the exact BT1900/BT1903 JSONL schema so the unmodified estimators consume it.

Honest scope: this is a synthetic control fixture exercising the estimator path, not physical data; it
demonstrates that the two-arm discriminator runs through the existing pipeline and returns the
geometry-forced verdicts. The positive arm reuses the committed BT1903 synthetic fixture. The even-q
ovoid that justifies CF=0 is the exact object built and verified in w33_ovoid_construct.py.
"""
from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bt1901_contextual_fraction_estimator as bt1901  # noqa: E402
import bt1904_exact_contextual_fraction_estimator as bt1904  # noqa: E402
import w33_ovoid_construct as ov  # noqa: E402

CONTROL_FIXTURE = "data/holonet_control_arm_fixture.jsonl"
POSITIVE_FIXTURE = "data/bt1903_synthetic_demonstrator_fixture.jsonl"
DARK_RATE = 0.01
LOSS_RATE = 0.15


def build_control_fixture(q=2, n_signal=400, n_dark=200, n_loss=200, seed=0):
    """Write a control-arm raw-shot fixture for the even-q fabric (CF=0 ovoid model)."""
    # confirm the even-q ovoid exists (the noncontextual model justifying CF=0)
    ovoid, pts, lines, A, max_sat = ov.find_ovoid(q)
    assert ovoid is not None, f"q={q} must have an ovoid for the control arm"
    n_contexts = len(lines)
    rng = random.Random(seed)
    rows = []
    sid = 0
    # signal rows: no contextual excess -> click only at the dark baseline
    for i in range(n_signal):
        click = "1" if rng.random() < DARK_RATE else "0"
        rows.append(
            {
                "shot_id": sid,
                "context_id": i % n_contexts,
                "ovoid_order_q": q,
                "click_pattern": click,
                "dark_reference": False,
                "loss_probe": False,
                "accepted_flag": True,
                "witness_class": "diagonal_contextual",
            }
        )
        sid += 1
    # dark baseline rows
    for _ in range(n_dark):
        click = "1" if rng.random() < DARK_RATE else "0"
        rows.append(
            {
                "shot_id": sid,
                "click_pattern": click,
                "dark_reference": True,
                "loss_probe": False,
                "accepted_flag": True,
                "witness_class": "dark",
            }
        )
        sid += 1
    # loss probe rows (survival = 1 - LOSS_RATE)
    for _ in range(n_loss):
        click = "1" if rng.random() < (1.0 - LOSS_RATE) else "0"
        rows.append(
            {
                "shot_id": sid,
                "click_pattern": click,
                "dark_reference": False,
                "loss_probe": True,
                "accepted_flag": True,
                "witness_class": "loss",
            }
        )
        sid += 1
    Path(CONTROL_FIXTURE).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return n_contexts, len(ovoid)


def _one_sided_upper95(k, n):
    """Crude one-sided 95% upper bound on a binomial rate (Wald + rule-of-three floor)."""
    import math

    p = k / n if n else 0.0
    wald = p + 1.645 * math.sqrt(max(p * (1 - p), 1e-12) / max(n, 1))
    return max(wald, 3.0 / max(n, 1))  # rule of three when k=0


def run():
    """Run both estimators on both arms; return (report, ok)."""
    n_contexts, ovoid_size = build_control_fixture(q=2)

    pos_rows = bt1901.load_rows(POSITIVE_FIXTURE)
    ctl_rows = bt1901.load_rows(CONTROL_FIXTURE)

    pos = bt1901.estimate(pos_rows)
    ctl = bt1901.estimate(ctl_rows)
    pos_exact = bt1904.estimate(pos_rows)
    ctl_exact = bt1904.estimate(ctl_rows)

    # control-arm one-sided upper bound: CF consistent with 0 and well below the positive 1/10
    ctl_signal = [
        r for r in ctl_rows if r.get("witness_class") == "diagonal_contextual"
    ]
    k = sum(bt1901.is_click(r) for r in ctl_signal)
    ub95 = _one_sided_upper95(k, len(ctl_signal))

    report = {
        "positive_arm": {
            "fabric": "W(3) odd",
            "corrected_CF": pos["corrected_contextual_fraction"],
            "compatible_with_one_tenth": pos["compatible_with_one_tenth"],
            "exact_pvalue_under_1/10": pos_exact[
                "exact_two_sided_binomial_pvalue_under_target"
            ],
        },
        "control_arm": {
            "fabric": "W(2) even",
            "n_contexts": n_contexts,
            "ovoid_size": ovoid_size,
            "corrected_CF": ctl["corrected_contextual_fraction"],
            "compatible_with_one_tenth": ctl["compatible_with_one_tenth"],
            "one_sided_95_upper_bound_CF": ub95,
            "consistent_with_zero_and_below_one_tenth": ub95 < 0.1,
        },
        "discriminator_ok": (
            pos["compatible_with_one_tenth"]
            and not ctl["compatible_with_one_tenth"]
            and ub95 < 0.1
        ),
    }
    ok = report["discriminator_ok"]
    return report, ok


def main():
    print(
        "== the demonstrator's two-arm discriminator, through the existing estimator path ==\n"
    )
    report, ok = run()
    p, c = report["positive_arm"], report["control_arm"]
    print(
        f"positive arm  {p['fabric']:>10}:  CF_hat = {p['corrected_CF']:.4f}  "
        f"-> compatible with 1/10: {p['compatible_with_one_tenth']}  (exact p under 1/10 = {p['exact_pvalue_under_1/10']:.3f})"
    )
    print(
        f"control  arm  {c['fabric']:>10}:  CF_hat = {c['corrected_CF']:.4f}  "
        f"-> compatible with 1/10: {c['compatible_with_one_tenth']}  (95% upper bound {c['one_sided_95_upper_bound_CF']:.4f} < 1/10: {c['consistent_with_zero_and_below_one_tenth']})"
    )
    print(
        f"   [W(2) control uses the explicit ovoid of {c['ovoid_size']} rays over {c['n_contexts']} contexts as its noncontextual model]"
    )
    print(
        f"\n{'DISCRIMINATOR OK -- same estimator, opposite verdicts: positive=1/10, control=0.' if ok else 'FAILURE: arms did not separate.'}"
    )

    out = {
        **report,
        "summary": (
            "the demonstrator's two-arm discriminator, runnable end-to-end through the EXISTING estimators "
            "(bt1901 normal-window, bt1904 exact-binomial), unmodified. A synthetic control fixture for the "
            "even-order W(2) fabric is generated from the explicit ovoid model (signal click rate = dark "
            "baseline, i.e. zero contextual excess, in the demonstrator's raw-shot schema) and run beside "
            "the committed BT1903 positive fixture. The SAME estimator returns opposite verdicts on the "
            "one-tenth hypothesis: positive arm CF~1/10 (compatible with 1/10), control arm CF~0 "
            "(incompatible with 1/10, one-sided 95% upper bound below 1/10). That is the parity law made a "
            "runnable discriminating test: a faked 1/10 on the odd fabric would have to be faked on the "
            "even fabric too, where the ovoid forbids any contextual excess. HONEST: synthetic control "
            "fixture exercising the estimator path, not physical data; the positive arm reuses the "
            "committed BT1903 fixture; the ovoid is the exact object from w33_ovoid_construct.py."
        ),
        "sources": [
            "bt1901_contextual_fraction_estimator / bt1904_exact_contextual_fraction_estimator (unmodified)",
            "w33_ovoid_construct (even-q ovoid = noncontextual model)",
            "holonet_demonstrator_protocol_v1.tex / holonet_parity_control.tex",
        ],
    }
    with open("data/holonet_control_arm.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/holonet_control_arm.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
