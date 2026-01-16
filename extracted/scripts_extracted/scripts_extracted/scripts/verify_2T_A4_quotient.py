import csv
from pathlib import Path


def read_table(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        elements = header[1:]
        table = {}
        for row in reader:
            if not row:
                continue
            row_elem = row[0]
            table[row_elem] = dict(zip(elements, row[1:]))
    return elements, table


def base_name(name: str) -> str:
    return name[:-1] if name.endswith("*") else name


def build_quotient(elements, table):
    base_elements = []
    rep_map = {}
    for elem in elements:
        base = base_name(elem)
        if base not in base_elements:
            base_elements.append(base)
        if base not in rep_map or not elem.endswith("*"):
            rep_map[base] = elem

    quotient = {}
    for a in base_elements:
        quotient[a] = {}
        for b in base_elements:
            prod = table[rep_map[a]][rep_map[b]]
            quotient[a][b] = base_name(prod)
    return base_elements, quotient


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    out_dir = data_dir / "_workbench" / "05_symmetry"
    out_dir.mkdir(parents=True, exist_ok=True)

    a4_elements, a4_table = read_table(data_dir / "A4_multiplication_table.csv")
    t2_elements, t2_table = read_table(data_dir / "binary_tetrahedral_2T_multiplication_table.csv")

    base_elements, quotient_table = build_quotient(t2_elements, t2_table)

    base_set = set(base_elements)
    a4_set = set(a4_elements)

    mismatches = []
    for a in a4_elements:
        for b in a4_elements:
            expected = a4_table[a][b]
            actual = quotient_table[a][b]
            if expected != actual:
                mismatches.append((a, b, expected, actual))

    diff_path = out_dir / "2T_to_A4_quotient_diff.csv"
    with diff_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["a", "b", "expected", "actual"])
        writer.writerows(mismatches)

    summary_path = out_dir / "2T_to_A4_quotient_check.md"
    with summary_path.open("w", encoding="utf-8") as handle:
        handle.write("# 2T -> A4 quotient check\n\n")
        handle.write("Inputs:\n")
        handle.write("- `data/_algebra/binary_tetrahedral2T_multiplication_table.csv`\n")
        handle.write("- `data/_algebra/a4multiplication_table.csv`\n\n")
        handle.write("Quotient rule:\n")
        handle.write("- Identify `g ~ g*` by stripping trailing `*`.\n\n")
        handle.write("Element sets:\n")
        handle.write(f"- 2T base elements: {len(base_elements)}\n")
        handle.write(f"- A4 elements: {len(a4_elements)}\n")
        handle.write(f"- base == A4: {base_set == a4_set}\n\n")
        handle.write("Table comparison (A4 vs 2T/center):\n")
        handle.write(f"- mismatches: {len(mismatches)}\n")
        handle.write(f"- diff csv: `{diff_path.relative_to(root).as_posix()}`\n")


if __name__ == "__main__":
    main()

