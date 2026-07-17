import json
from pathlib import Path


def main():
    json_path = Path("data/sheet_intersections.json")
    if not json_path.exists():
        print("Run analysis/export_intersections.py first.")
        return

    with open(json_path) as f:
        mat = json.load(f)

    gap_path = Path("data/sheet_intersections.gap")
    with open(gap_path, "w") as f:
        f.write("mat := [\n")
        for row in mat:
            f.write("  [" + ", ".join(map(str, row)) + "],\n")
        f.write("];\n")
    print(f"Wrote {gap_path}")


if __name__ == "__main__":
    main()
