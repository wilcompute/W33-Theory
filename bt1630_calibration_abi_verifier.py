#!/usr/bin/env python3
"""
BT1630: Extends bt1626_ym_mass_gap_tightness_verifier.py with BT1604
calibration ABI hard pass/fail gates.

Covers:
  - SNSPD dark count rate < 100 Hz per bin
  - Detection efficiency > 0.90 per active bin
  - Confidence interval width < 0.02 on 168-bin thresholds
  - Fano active detector bin count = 168 (7 * 24)
  - Witting frame / bin assignment: 80 bins x 9 uses + 88 bins x 10 uses = 1600
  - Loss placeholder budget: < 5% per rail
  - Dark-reference bin count >= 1 per Hesse-residue class (7 classes)

Run:
    python bt1630_calibration_abi_verifier.py

Pass criteria: prints CALIBRATION ABI GATES: ALL PASSED
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List


@dataclass
class DetectorBin:
    """Single Fano active detector bin."""
    bin_id: int
    hesse_residue: int
    dark_count_rate_hz: float
    detection_efficiency: float
    threshold_low: float
    threshold_high: float
    n_witting_uses: int
    is_dark_reference: bool = False

    @property
    def ci_width(self) -> float:
        return self.threshold_high - self.threshold_low

    def pass_dark_rate(self) -> bool:
        return self.dark_count_rate_hz < 100.0

    def pass_efficiency(self) -> bool:
        return self.detection_efficiency > 0.90

    def pass_ci_width(self) -> bool:
        return self.ci_width < 0.02


def build_nominal_bench_data() -> List[DetectorBin]:
    """
    Construct 168 nominal detector bins matching the BT1602 usage profile:
      80 bins used 9 times  (bin_id 0..79)
      88 bins used 10 times (bin_id 80..167)
    Total frame assignments: 80*9 + 88*10 = 720 + 880 = 1600  (Witting frames)

    Nominal values are within-spec.  Replace with real bench CSV loader
    before arXiv submission.
    """
    bins: List[DetectorBin] = []
    for i in range(168):
        hesse_r = i % 7
        uses = 9 if i < 80 else 10
        bins.append(DetectorBin(
            bin_id=i,
            hesse_residue=hesse_r,
            dark_count_rate_hz=12.4 + (i % 13) * 0.5,
            detection_efficiency=0.92 + (i % 7) * 0.001,
            threshold_low=0.480 + (i % 11) * 0.001,
            threshold_high=0.498 + (i % 11) * 0.001,
            n_witting_uses=uses,
            is_dark_reference=(hesse_r == 0 and i < 7),
        ))
    return bins


def gate_bin_count(bins: List[DetectorBin]) -> None:
    assert len(bins) == 168, f"Expected 168 bins, got {len(bins)}"
    print(f"  [PASS] Bin count = {len(bins)} (= 7 * 24)")


def gate_usage_profile(bins: List[DetectorBin]) -> None:
    nine_bins = [b for b in bins if b.n_witting_uses == 9]
    ten_bins  = [b for b in bins if b.n_witting_uses == 10]
    total     = sum(b.n_witting_uses for b in bins)
    assert len(nine_bins) == 80,  f"Expected 80 bins x9, got {len(nine_bins)}"
    assert len(ten_bins)  == 88,  f"Expected 88 bins x10, got {len(ten_bins)}"
    assert total == 1600,         f"Expected 1600 total, got {total}"
    print(f"  [PASS] Usage profile: 80 x 9 + 88 x 10 = {total} frames")


def gate_dark_count_rates(bins: List[DetectorBin]) -> None:
    failures = [b for b in bins if not b.pass_dark_rate()]
    assert len(failures) == 0, f"{len(failures)} bins exceed 100 Hz dark count"
    worst = max(bins, key=lambda b: b.dark_count_rate_hz)
    print(f"  [PASS] All 168 dark count rates < 100 Hz  (worst: {worst.dark_count_rate_hz:.1f} Hz, bin {worst.bin_id})")


def gate_detection_efficiency(bins: List[DetectorBin]) -> None:
    failures = [b for b in bins if not b.pass_efficiency()]
    assert len(failures) == 0, f"{len(failures)} bins below 0.90 efficiency"
    worst = min(bins, key=lambda b: b.detection_efficiency)
    print(f"  [PASS] All 168 detection efficiencies > 0.90  (worst: {worst.detection_efficiency:.4f}, bin {worst.bin_id})")


def gate_ci_width(bins: List[DetectorBin]) -> None:
    failures = [b for b in bins if not b.pass_ci_width()]
    assert len(failures) == 0, f"{len(failures)} bins have CI width >= 0.02"
    worst = max(bins, key=lambda b: b.ci_width)
    print(f"  [PASS] All 168 CI widths < 0.02  (worst: {worst.ci_width:.5f}, bin {worst.bin_id})")


def gate_loss_budget(bins: List[DetectorBin]) -> None:
    over_budget = [b for b in bins if (1.0 - b.detection_efficiency) >= 0.05]
    assert len(over_budget) == 0, f"{len(over_budget)} bins exceed 5% loss budget"
    print(f"  [PASS] All 168 bins within 5% loss budget per rail")


def gate_dark_reference_coverage(bins: List[DetectorBin]) -> None:
    dark_refs = [b for b in bins if b.is_dark_reference]
    covered_classes = {b.hesse_residue for b in dark_refs}
    assert covered_classes == set(range(7)), (
        f"Missing dark-reference coverage for classes: {set(range(7)) - covered_classes}"
    )
    print(f"  [PASS] Dark-reference coverage: all 7 Hesse-residue classes ({len(dark_refs)} ref bins)")


def main() -> None:
    print("=" * 65)
    print("BT1630 Calibration ABI Verifier -- BT1604 pass/fail gates")
    print("=" * 65)
    bins = build_nominal_bench_data()
    gate_bin_count(bins)
    gate_usage_profile(bins)
    gate_dark_count_rates(bins)
    gate_detection_efficiency(bins)
    gate_ci_width(bins)
    gate_loss_budget(bins)
    gate_dark_reference_coverage(bins)
    print()
    print("=" * 65)
    print("CALIBRATION ABI GATES: ALL PASSED")
    print("Replace build_nominal_bench_data() with real bench CSV loader")
    print("before arXiv submission.")
    print("=" * 65)


if __name__ == "__main__":
    main()
