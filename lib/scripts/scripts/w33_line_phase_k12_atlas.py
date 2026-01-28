import csv
import json
import math
from collections import defaultdict
from pathlib import Path


def parse_complex(value: str) -> complex:
    return complex(value.strip())


def angle_to_k12(angle: float) -> int:
    two_pi = 2.0 * math.pi
    angle = angle % two_pi
    step = two_pi / 12.0
    k = int(round(angle / step)) % 12
    return k


def counts_to_json(counts):
    return json.dumps({str(k): counts[k] for k in sorted(counts.keys())})


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    out_dir = data_dir / "_workbench" / "02_geometry"
    out_dir.mkdir(parents=True, exist_ok=True)

    point_path = (
        data_dir
        / "toe_W33_orthonormal_phase_solution_20260110"
        / "W33_point_rays_C4_complex.csv"
    )
    line_path = (
        data_dir / "_sources" / "w33" / "W33_lines_tetrads_from_checkpoint_20260109.csv"
    )

    points = {}
    with point_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            point_id = int(row["point_id"])
            coords = [
                parse_complex(row["v0"]),
                parse_complex(row["v1"]),
                parse_complex(row["v2"]),
                parse_complex(row["v3"]),
            ]
            points[point_id] = coords

    lines = []
    with line_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = int(row["line_id"])
            point_ids = [int(p) for p in row["point_ids"].split()]
            lines.append((line_id, point_ids))

    global_counts = defaultdict(int)
    rows = []
    eps = 1e-9
    for line_id, point_ids in lines:
        counts = defaultdict(int)
        coord_counts = [defaultdict(int) for _ in range(4)]
        total_entries = 0
        for pid in point_ids:
            coords = points.get(pid)
            if coords is None:
                continue
            for idx, value in enumerate(coords):
                mag = abs(value)
                if mag <= eps:
                    continue
                angle = math.atan2(value.imag, value.real)
                k = angle_to_k12(angle)
                counts[k] += 1
                coord_counts[idx][k] += 1
                global_counts[k] += 1
                total_entries += 1
        rows.append(
            {
                "line_id": line_id,
                "point_ids": " ".join(str(p) for p in point_ids),
                "total_entries": total_entries,
                "unique_k_mod12": len(counts),
                "coord0_unique_k_mod12": len(coord_counts[0]),
                "coord1_unique_k_mod12": len(coord_counts[1]),
                "coord2_unique_k_mod12": len(coord_counts[2]),
                "coord3_unique_k_mod12": len(coord_counts[3]),
                "k_mod12_counts": counts_to_json(counts),
            }
        )

    out_csv = out_dir / "W33_line_phase_k12_map.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    out_md = out_dir / "W33_line_phase_k12_map.md"
    with out_md.open("w", encoding="utf-8") as handle:
        handle.write("# W33 line phase map (k mod 12)\n\n")
        handle.write("Inputs:\n")
        handle.write(
            "- `data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv`\n"
        )
        handle.write(
            "- `data/_sources/w33/W33_lines_tetrads_from_checkpoint_20260109.csv`\n\n"
        )
        handle.write("Outputs:\n")
        handle.write("- `data/_workbench/02_geometry/W33_line_phase_k12_map.csv`\n\n")
        handle.write("Global k mod 12 counts:\n")
        handle.write(f"- {counts_to_json(global_counts)}\n")


if __name__ == "__main__":
    main()
