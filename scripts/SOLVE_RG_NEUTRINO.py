#!/usr/bin/env python3
"""Production neutrino solver for the W(3,3) fixed-point packet.

This script keeps the April 2026 legacy NuFIT 5.3 outputs stable for the
existing artifact/tests, while also exposing current official NuFIT 6.0
presets for forward runs.

Function defaults remain legacy-compatible:
  - build_results() uses ``nufit53_legacy``
  - solve_NH()/solve_IH() use ``nufit53_legacy``

CLI default is the current official NuFIT 6.0 fit with SK atmospheric data:
  python scripts/SOLVE_RG_NEUTRINO.py
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import sys
from typing import Dict, Mapping

import numpy as np
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from scripts.w33_spectral_core import W33


@dataclass(frozen=True)
class OscillationPreset:
    name: str
    label: str
    dm2_sol: float
    dm2_atm_nh: float
    dm2_atm_ih: float
    source: str
    release_date: str
    notes: str


LEGACY_PRESET_NAME = "nufit53_legacy"
CURRENT_PRESET_NAME = "nufit60_ic24_with_sk"

OSCILLATION_PRESETS: Dict[str, OscillationPreset] = {
    LEGACY_PRESET_NAME: OscillationPreset(
        name=LEGACY_PRESET_NAME,
        label="NuFIT 5.3 legacy",
        dm2_sol=7.42e-5,
        dm2_atm_nh=2.528e-3,
        dm2_atm_ih=2.510e-3,
        source="https://www.nu-fit.org/?q=node/278",
        release_date="2024-01-31",
        notes="Legacy April 2026 repo baseline preserved for backward compatibility.",
    ),
    CURRENT_PRESET_NAME: OscillationPreset(
        name=CURRENT_PRESET_NAME,
        label="NuFIT 6.0 IC24 with SK atmospheric data",
        dm2_sol=7.49e-5,
        dm2_atm_nh=2.513e-3,
        dm2_atm_ih=2.484e-3,
        source="https://www.nu-fit.org/?q=node/294",
        release_date="2024-12-20",
        notes="Current official NuFIT 6.0 release including tabulated SK and IceCube atmospheric data.",
    ),
    "nufit60_ic19_without_sk": OscillationPreset(
        name="nufit60_ic19_without_sk",
        label="NuFIT 6.0 IC19 without SK atmospheric data",
        dm2_sol=7.49e-5,
        dm2_atm_nh=2.534e-3,
        dm2_atm_ih=2.510e-3,
        source="https://www.nu-fit.org/?q=node/294",
        release_date="2024-12-20",
        notes="Alternate NuFIT 6.0 table without the tabulated SK atmospheric likelihoods.",
    ),
}

# W(3,3) fixed-point targets, kept in the published order.
W33_TARGETS: Dict[str, float] = {
    "1/mu": 1 / W33.mu,
    "1/Phi6": 1 / W33.Phi6,
    "1/Phi3": 1 / W33.Phi3,
    "1/(2k-1)": 1 / W33.two_k_minus_1,
    "1/6": 1 / 6,
}


def get_preset(preset_name: str = LEGACY_PRESET_NAME) -> OscillationPreset:
    try:
        return OSCILLATION_PRESETS[preset_name]
    except KeyError as exc:
        available = ", ".join(sorted(OSCILLATION_PRESETS))
        raise KeyError(f"unknown preset {preset_name!r}; available presets: {available}") from exc


def list_presets() -> tuple[str, ...]:
    return tuple(OSCILLATION_PRESETS)


def masses_NH(m1: float, *, preset_name: str = LEGACY_PRESET_NAME) -> tuple[float, float, float]:
    """Return (m1, m2, m3) for normal ordering given m1 in eV."""
    preset = get_preset(preset_name)
    return (
        m1,
        float(np.sqrt(m1**2 + preset.dm2_sol)),
        float(np.sqrt(m1**2 + preset.dm2_atm_nh)),
    )


def masses_IH(m3: float, *, preset_name: str = LEGACY_PRESET_NAME) -> tuple[float, float, float]:
    """Return (m1, m2, m3) for inverted ordering given lightest m3 in eV."""
    preset = get_preset(preset_name)
    m2 = float(np.sqrt(m3**2 + preset.dm2_atm_ih))
    m1 = float(np.sqrt(m2**2 - preset.dm2_sol))
    return m1, m2, m3


def mu_eff2(masses: tuple[float, float, float]) -> float:
    """Compute mu_eff^2 = -log(s*) / log(Phi4), with s* = geom_mean / max."""
    sorted_masses = np.sort(np.array(masses, dtype=float))
    if np.any(sorted_masses <= 0):
        return float("inf")
    geometric_mean = float(np.exp(np.mean(np.log(sorted_masses))))
    s_star = geometric_mean / float(sorted_masses[-1])
    if s_star <= 0:
        return float("inf")
    return float(-np.log(s_star) / np.log(W33.Phi4))


def solve_NH(
    target: float,
    m1_lo: float = 1e-6,
    m1_hi: float = 0.5,
    *,
    preset_name: str = LEGACY_PRESET_NAME,
) -> dict[str, float] | None:
    """Find NH masses with mu_eff^2 equal to ``target``."""
    try:
        root = brentq(
            lambda m: mu_eff2(masses_NH(m, preset_name=preset_name)) - target,
            m1_lo,
            m1_hi,
            xtol=1e-14,
            maxiter=500,
        )
    except ValueError:
        return None

    masses = masses_NH(root, preset_name=preset_name)
    total = float(sum(masses))
    return {
        "m1_eV": float(root),
        "m1_meV": float(root * 1e3),
        "m2_eV": float(masses[1]),
        "m3_eV": float(masses[2]),
        "sum_eV": total,
        "sum_meV": float(total * 1e3),
        "mu_eff2": float(mu_eff2(masses)),
    }


def solve_IH(
    target: float,
    m3_lo: float = 1e-6,
    m3_hi: float = 0.4,
    *,
    preset_name: str = LEGACY_PRESET_NAME,
) -> dict[str, float] | None:
    """Find IH masses with mu_eff^2 equal to ``target``."""
    try:
        root = brentq(
            lambda m: mu_eff2(masses_IH(m, preset_name=preset_name)) - target,
            m3_lo,
            m3_hi,
            xtol=1e-14,
            maxiter=500,
        )
    except ValueError:
        return None

    masses = masses_IH(root, preset_name=preset_name)
    total = float(sum(masses))
    return {
        "m3_eV": float(root),
        "m3_meV": float(root * 1e3),
        "m1_eV": float(masses[0]),
        "m2_eV": float(masses[1]),
        "sum_eV": total,
        "sum_meV": float(total * 1e3),
        "mu_eff2": float(mu_eff2(masses)),
    }


def build_results(
    preset_name: str = LEGACY_PRESET_NAME,
    *,
    targets: Mapping[str, float] = W33_TARGETS,
) -> dict[str, dict[str, object]]:
    """Return the checked neutrino solutions for a preset, keyed by fixed point."""
    get_preset(preset_name)
    results: dict[str, dict[str, object]] = {}
    for label, target in targets.items():
        entry: dict[str, object] = {"target": float(target), "label": label}
        nh = solve_NH(float(target), preset_name=preset_name)
        ih = solve_IH(float(target), preset_name=preset_name)
        if nh is not None:
            entry["NH"] = nh
        if ih is not None:
            entry["IH"] = ih
        results[label] = entry
    return results


def build_payload(preset_name: str = LEGACY_PRESET_NAME) -> dict[str, object]:
    """Return metadata plus the checked fixed-point solutions for a preset."""
    preset = get_preset(preset_name)
    return {
        "preset": asdict(preset),
        "w33_targets": {label: float(target) for label, target in W33_TARGETS.items()},
        "results": build_results(preset_name=preset_name),
    }


def results_output_path(preset_name: str = LEGACY_PRESET_NAME) -> Path:
    output_dir = ROOT / "artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)
    if preset_name == LEGACY_PRESET_NAME:
        return output_dir / "rg_neutrino_results.json"
    return output_dir / f"rg_neutrino_results_{preset_name}.json"


def write_results(
    results: Mapping[str, object],
    output_path: str | Path | None = None,
    *,
    preset_name: str = LEGACY_PRESET_NAME,
) -> Path:
    path = Path(output_path) if output_path is not None else results_output_path(preset_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return path


def _ordered_labels(results: Mapping[str, Mapping[str, object]], hierarchy: str) -> tuple[str, ...]:
    return tuple(
        label
        for label, _ in sorted(
            (
                (label, float(entry[hierarchy]["sum_meV"]))
                for label, entry in results.items()
                if hierarchy in entry
            ),
            key=lambda item: item[1],
        )
    )


def print_results_table(results: Mapping[str, Mapping[str, object]], *, preset_name: str) -> None:
    preset = get_preset(preset_name)
    print(f"Preset: {preset.label}")
    print(f"Source: {preset.source}")
    print(f"{'Label':12s}  {'Target':10s}  {'NH sum (meV)':12s}  {'IH sum (meV)':12s}")
    print("-" * 58)
    for label, entry in results.items():
        target = float(entry["target"])
        nh = entry.get("NH")
        ih = entry.get("IH")
        nh_sum = f"{nh['sum_meV']:.6f}" if nh else "no solution"
        ih_sum = f"{ih['sum_meV']:.6f}" if ih else "no solution"
        print(f"{label:12s}  {target:.6f}  {nh_sum:12s}  {ih_sum:12s}")
    print()
    print(f"NH ordering: {' < '.join(_ordered_labels(results, 'NH'))}")
    print(f"IH ordering: {' < '.join(_ordered_labels(results, 'IH'))}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preset",
        default=CURRENT_PRESET_NAME,
        choices=sorted(OSCILLATION_PRESETS),
        help="Oscillation-data preset to solve against.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON output path. Defaults to the preset-specific artifact path.",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available oscillation presets and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list_presets:
        for preset_name in list_presets():
            preset = get_preset(preset_name)
            print(f"{preset.name}: {preset.label}")
        return

    payload = build_payload(args.preset)
    results = payload["results"]
    print_results_table(results, preset_name=args.preset)
    output_path = write_results(results, args.output, preset_name=args.preset)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
