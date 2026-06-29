"""Pass 55: the two-arm contextuality discriminator and the scaling divergence plot.

  - holonet_control_arm: the demonstrator's OWN estimators (bt1901/bt1904), unmodified, return opposite
    verdicts on the one-tenth hypothesis -- positive arm (q=3) compatible with 1/10, control arm
    (even-q ovoid model) incompatible with 1/10 and consistent with 0. That is the parity law made a
    runnable two-arm discriminating test.
  - the scaling figure renders without error when matplotlib is present.
"""

import os
import sys

import pytest

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import holonet_bench as bench  # noqa: E402
import holonet_control_arm as ctl  # noqa: E402


def test_two_arm_discriminator():
    report, ok = ctl.run()
    assert ok, report
    assert report["positive_arm"]["compatible_with_one_tenth"] is True
    assert report["control_arm"]["compatible_with_one_tenth"] is False
    assert report["control_arm"]["consistent_with_zero_and_below_one_tenth"] is True


def test_control_fixture_comes_from_ovoid():
    n_contexts, ovoid_size = ctl.build_control_fixture(q=2)
    assert n_contexts == 15 and ovoid_size == 5
    assert os.path.exists(ctl.CONTROL_FIXTURE)


def test_scale_plot_renders(tmp_path):
    pytest.importorskip("matplotlib")
    ledger, ok = bench.run_compare_scale()
    out = tmp_path / "scale.png"
    p = bench.plot_compare_scale(ledger, path=str(out))
    assert os.path.exists(p) and os.path.getsize(p) > 0
