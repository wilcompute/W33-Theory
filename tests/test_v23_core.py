import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd


def load_expected(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_v23_counts_match_toe_core():
    base = Path(__file__).parent.parent / "bundles" / "v23_toe_finish" / "v23"
    csv_path = base / "Q_triangles_with_centers_Z2_S3_fiber6.csv"
    json_path = base / "toe_core_theorem.json"

    assert csv_path.exists(), f"Missing CSV: {csv_path}"
    assert json_path.exists(), f"Missing JSON: {json_path}"

    df = pd.read_csv(csv_path)
    expected = load_expected(json_path)

    # centers counts
    centers_counts = dict(Counter(df["centers"].astype(int).tolist()))
    assert centers_counts == {
        int(k): int(v) for k, v in expected["triangle_counts_by_centers"].items()
    }

    # parity + cycle type counts (z2_parity, fiber6_cycle_type)
    def parse_cycle(s: str):
        nums = re.findall(r"\\d+", str(s))
        return tuple(int(x) for x in nums)

    # debug sample values
    sample = [r.fiber6_cycle_type for r in df.itertuples(index=False)][:10]
    print("DEBUG sample fiber6_cycle_type first10:", sample)
    print("DEBUG parsed sample:", [parse_cycle(s) for s in sample])
    print("DEBUG re module:", repr(re))
    print("DEBUG re.findall on example:", re.findall(r"\d+", sample[0]))
    # robust direct comparison using dataframe filtering to avoid parsing issues
    import ast

    for k_str, v in expected["triangle_counts_by_parity_and_cycle_type"].items():
        parsed = ast.literal_eval(k_str)
        parity = int(parsed[0])
        cycle = tuple(int(x) for x in parsed[1])
        cycle_str = str(tuple(cycle))
        actual_count = int(
            df[(df.z2_parity == parity) & (df.fiber6_cycle_type == cycle_str)].shape[0]
        )
        assert actual_count == int(
            v
        ), f"Mismatch for {(parity, cycle)}: expected {v}, got {actual_count}"

    # exact law entries are present and match counts (centers, z2_parity, fiber6_cycle_type)
    combo = Counter(
        (int(r.centers), int(r.z2_parity), r.fiber6_cycle_type)
        for r in df.itertuples(index=False)
    )
    for e in expected["exact_law"]:
        key = (int(e["centers"]), int(e["z2_parity"]), e["fiber6_cycle_type"])
        assert combo.get(key, 0) == int(
            e["count"]
        ), f"Mismatch for {key}: expected {e['count']}, got {combo.get(key,0)}"
