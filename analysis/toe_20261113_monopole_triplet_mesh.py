"""Four-point mesh refinement of the finite-cut monopole conversion dip."""

import argparse
import json
from pathlib import Path

import toe_20261113_monopole_triplet_line_shape as line_shape


OUT = line_shape.OUT.with_name("toe_20261113_monopole_triplet_mesh.json")
ENERGIES = (0.0, 0.0018333333333333333, 0.002, 0.004)


def calculate():
    baseline = json.loads(line_shape.OUT.read_text(encoding="utf-8"))["rows"]
    change_in, change_out = line_shape.flavors.flavor_frames()
    refined = next(row for row in line_shape.residues.poles.threshold.prepare(60) if row[0] == "L")
    rows = []
    for energy in ENERGIES:
        previous = min(baseline, key=lambda row: abs(row["energy"]-energy))
        assert abs(previous["energy"]-energy) < 1e-12
        reflection = line_shape.residues.matching(refined, energy)
        conversion = float(line_shape.conversion(change_out.conj().T @ reflection @ change_in))
        rows.append(dict(energy=energy, cells_80=previous["total"], cells_120=conversion,
                         difference=conversion-previous["total"]))
    change = max(abs(row["difference"]) for row in rows)
    assert change < 0.001
    return dict(status="PASS", exterior_cut=5., rows=rows, maximum_absolute_change=change)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
