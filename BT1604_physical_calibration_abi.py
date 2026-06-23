#!/usr/bin/env python3
"""
BT1604 — Physical Calibration ABI
====================================
Converts the BT1601 loss/dark placeholders into a bench-data schema
with thresholds, confidence intervals, and pass/fail gates.

Architecture:
  CalibrationRecord   — one per detector bin, one per rail, one per run
  CalibrationABI      — aggregates records, emits pass/fail verdict
  ThresholdBank       — holds all tunable thresholds with CI bounds

Context in the BT stack:
  BT1601 introduced loss_placeholder and dark_placeholder fields.
  BT1602 welded 168 Fano detector bins to the Witting transaction body.
  BT1603 closed the finite universal-computation ABI.
  BT1604 (this file) turns those placeholders into live, testable calibration
  gates that a physical bench run can populate and validate.
"""

from __future__ import annotations

import json
import math
import statistics
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple

# ---------------------------------------------------------------------------
# Constants — default threshold bank (override per bench run)
# ---------------------------------------------------------------------------

DEFAULT_THRESHOLDS: Dict[str, Dict] = {
    "loss": {
        "warn_frac": 0.05,   # 5 % single-photon loss → warning
        "fail_frac": 0.15,   # 15 % → hard fail
        "ci_z": 1.96,        # 95 % confidence interval z-score
    },
    "dark": {
        "warn_rate_hz": 100,   # dark count rate warning
        "fail_rate_hz": 500,   # dark count rate hard fail
        "ci_z": 1.96,
    },
    "efficiency": {
        "warn_frac": 0.80,   # detector efficiency below this → warning
        "fail_frac": 0.60,   # below this → hard fail
        "ci_z": 1.96,
    },
    "timing_jitter_ps": {
        "warn": 50.0,
        "fail": 150.0,
        "ci_z": 1.96,
    },
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CalibrationSample:
    """One raw measurement sample from a detector bin."""
    bin_id: int                  # Fano bin index 0..167
    rail: str                    # 'H', 'V', or orbital label
    loss_observed: float         # measured photon loss fraction [0,1]
    dark_count_hz: float         # dark count rate in Hz
    efficiency: float            # detector efficiency [0,1]
    timing_jitter_ps: float      # timing jitter in picoseconds
    run_id: str = "run_0"        # bench run identifier


@dataclass
class ConfidenceInterval:
    mean: float
    lower: float
    upper: float
    n_samples: int

    def contains(self, threshold: float) -> bool:
        return self.lower <= threshold <= self.upper

    def below(self, threshold: float) -> bool:
        return self.upper < threshold

    def above(self, threshold: float) -> bool:
        return self.lower > threshold


@dataclass
class CalibrationRecord:
    """Aggregated calibration state for one (bin_id, rail) pair."""
    bin_id: int
    rail: str
    run_id: str
    n_samples: int

    loss_ci: ConfidenceInterval = field(default=None)
    dark_ci: ConfidenceInterval = field(default=None)
    efficiency_ci: ConfidenceInterval = field(default=None)
    jitter_ci: ConfidenceInterval = field(default=None)

    loss_gate: str = "UNKNOWN"        # PASS / WARN / FAIL
    dark_gate: str = "UNKNOWN"
    efficiency_gate: str = "UNKNOWN"
    jitter_gate: str = "UNKNOWN"
    overall_gate: str = "UNKNOWN"


# ---------------------------------------------------------------------------
# Helper: confidence interval from list of floats
# ---------------------------------------------------------------------------

def _ci(values: List[float], z: float = 1.96) -> ConfidenceInterval:
    n = len(values)
    if n == 0:
        return ConfidenceInterval(float("nan"), float("nan"), float("nan"), 0)
    mu = statistics.mean(values)
    if n == 1:
        return ConfidenceInterval(mu, mu, mu, 1)
    se = statistics.stdev(values) / math.sqrt(n)
    return ConfidenceInterval(mu, mu - z * se, mu + z * se, n)


# ---------------------------------------------------------------------------
# Threshold bank
# ---------------------------------------------------------------------------

class ThresholdBank:
    def __init__(self, overrides: Optional[Dict] = None):
        import copy
        self._bank = copy.deepcopy(DEFAULT_THRESHOLDS)
        if overrides:
            for key, vals in overrides.items():
                if key in self._bank:
                    self._bank[key].update(vals)
                else:
                    self._bank[key] = vals

    def loss(self) -> Tuple[float, float, float]:
        t = self._bank["loss"]
        return t["warn_frac"], t["fail_frac"], t["ci_z"]

    def dark(self) -> Tuple[float, float, float]:
        t = self._bank["dark"]
        return t["warn_rate_hz"], t["fail_rate_hz"], t["ci_z"]

    def efficiency(self) -> Tuple[float, float, float]:
        t = self._bank["efficiency"]
        return t["warn_frac"], t["fail_frac"], t["ci_z"]

    def jitter(self) -> Tuple[float, float, float]:
        t = self._bank["timing_jitter_ps"]
        return t["warn"], t["fail"], t["ci_z"]

    def to_dict(self) -> Dict:
        return dict(self._bank)


# ---------------------------------------------------------------------------
# Gate logic (lower-is-better for loss/dark/jitter; higher-is-better for eff)
# ---------------------------------------------------------------------------

def _gate_lower_is_better(ci: ConfidenceInterval, warn: float, fail: float) -> str:
    """FAIL if CI mean >= fail threshold; WARN if mean >= warn; else PASS."""
    if ci.mean >= fail:
        return "FAIL"
    if ci.mean >= warn:
        return "WARN"
    return "PASS"


def _gate_higher_is_better(ci: ConfidenceInterval, warn: float, fail: float) -> str:
    """FAIL if CI mean <= fail threshold; WARN if mean <= warn; else PASS."""
    if ci.mean <= fail:
        return "FAIL"
    if ci.mean <= warn:
        return "WARN"
    return "PASS"


# ---------------------------------------------------------------------------
# Calibration ABI
# ---------------------------------------------------------------------------

class CalibrationABI:
    """
    Top-level calibration authority.  Feed it raw CalibrationSamples;
    it groups them by (bin_id, rail), computes CIs, and emits records
    with pass/fail gates.
    """

    def __init__(self, threshold_overrides: Optional[Dict] = None):
        self.bank = ThresholdBank(threshold_overrides)
        self._samples: List[CalibrationSample] = []

    def ingest(self, samples: List[CalibrationSample]) -> None:
        self._samples.extend(samples)

    def evaluate(self) -> List[CalibrationRecord]:
        """Process all ingested samples and return CalibrationRecords."""
        grouped: Dict[Tuple[int, str], List[CalibrationSample]] = {}
        for s in self._samples:
            key = (s.bin_id, s.rail)
            grouped.setdefault(key, []).append(s)

        records: List[CalibrationRecord] = []
        for (bin_id, rail), group in sorted(grouped.items()):
            run_id = group[0].run_id
            n = len(group)

            loss_ci    = _ci([s.loss_observed    for s in group], self.bank.loss()[2])
            dark_ci    = _ci([s.dark_count_hz    for s in group], self.bank.dark()[2])
            eff_ci     = _ci([s.efficiency       for s in group], self.bank.efficiency()[2])
            jitter_ci  = _ci([s.timing_jitter_ps for s in group], self.bank.jitter()[2])

            l_warn, l_fail, _  = self.bank.loss()
            d_warn, d_fail, _  = self.bank.dark()
            e_warn, e_fail, _  = self.bank.efficiency()
            j_warn, j_fail, _  = self.bank.jitter()

            loss_g = _gate_lower_is_better(loss_ci, l_warn, l_fail)
            dark_g = _gate_lower_is_better(dark_ci, d_warn, d_fail)
            eff_g  = _gate_higher_is_better(eff_ci, e_warn, e_fail)
            jit_g  = _gate_lower_is_better(jitter_ci, j_warn, j_fail)

            gates = [loss_g, dark_g, eff_g, jit_g]
            if "FAIL" in gates:
                overall = "FAIL"
            elif "WARN" in gates:
                overall = "WARN"
            else:
                overall = "PASS"

            rec = CalibrationRecord(
                bin_id=bin_id, rail=rail, run_id=run_id, n_samples=n,
                loss_ci=loss_ci, dark_ci=dark_ci, efficiency_ci=eff_ci, jitter_ci=jitter_ci,
                loss_gate=loss_g, dark_gate=dark_g, efficiency_gate=eff_g,
                jitter_gate=jit_g, overall_gate=overall,
            )
            records.append(rec)
        return records

    def summary(self) -> Dict:
        """Return a top-level pass/fail/warn count across all records."""
        records = self.evaluate()
        counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "UNKNOWN": 0}
        for r in records:
            counts[r.overall_gate] = counts.get(r.overall_gate, 0) + 1
        counts["total"] = len(records)
        counts["verdict"] = "FAIL" if counts["FAIL"] > 0 else ("WARN" if counts["WARN"] > 0 else "PASS")
        return counts

    def to_json(self, indent: int = 2) -> str:
        """Serialise all evaluated records to JSON."""
        records = self.evaluate()
        output = []
        for r in records:
            d = asdict(r)
            output.append(d)
        return json.dumps(output, indent=indent, default=str)


# ---------------------------------------------------------------------------
# Synthetic test harness (168 Fano bins × 2 rails)
# ---------------------------------------------------------------------------

def _generate_synthetic_samples(
    n_bins: int = 168,
    rails: List[str] = None,
    samples_per_bin: int = 10,
    seed: int = 42,
) -> List[CalibrationSample]:
    """Generate deterministic synthetic calibration samples for 168 Fano bins."""
    import random
    rng = random.Random(seed)
    if rails is None:
        rails = ["H", "V"]
    out: List[CalibrationSample] = []
    for bin_id in range(n_bins):
        for rail in rails:
            for k in range(samples_per_bin):
                # BT1602 usage profile: 80 bins used 9×, 88 bins used 10×
                usage = 9 if bin_id < 80 else 10
                # Slightly elevate loss for bins that are heavily used
                base_loss = 0.02 + (usage - 9) * 0.005
                out.append(CalibrationSample(
                    bin_id=bin_id,
                    rail=rail,
                    loss_observed=max(0.0, rng.gauss(base_loss, 0.005)),
                    dark_count_hz=max(0.0, rng.gauss(80.0, 20.0)),
                    efficiency=min(1.0, rng.gauss(0.88, 0.03)),
                    timing_jitter_ps=max(0.0, rng.gauss(30.0, 8.0)),
                    run_id="synthetic_bt1604",
                ))
    return out


if __name__ == "__main__":
    print("BT1604 — Physical Calibration ABI")
    print("===================================\n")

    abi = CalibrationABI()
    samples = _generate_synthetic_samples()
    abi.ingest(samples)

    summary = abi.summary()
    print("Calibration summary:")
    for k, v in summary.items():
        print(f"  {k:12s}: {v}")

    records = abi.evaluate()
    fail_list = [r for r in records if r.overall_gate == "FAIL"]
    warn_list = [r for r in records if r.overall_gate == "WARN"]
    print(f"\nFailed bins : {len(fail_list)}")
    print(f"Warned bins : {len(warn_list)}")
    print(f"Total bins  : {len(records)}")
    print("\nBT1604 calibration ABI: OK")
