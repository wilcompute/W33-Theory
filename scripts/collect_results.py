import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.json_safe import dump_json

SUMMARY_KEYS = [
    "key_finding",
    "key_insight",
    "key_result",
    "key_results",
    "title",
    "summary",
]
PART_DIRS = [
    ROOT,
    ROOT / "archive" / "json",
]


def roman_to_int(text: str) -> int:
    text = text.upper()
    if text.startswith("DCM"):
        suffix = text[3:]
        return 900 + (roman_to_int(suffix) if suffix else 0)

    roman_map = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    total = 0
    index = 0
    while index < len(text):
        current = roman_map.get(text[index], 0)
        nxt = roman_map.get(text[index + 1], 0) if index + 1 < len(text) else 0
        if current == 0:
            raise ValueError(f"invalid roman numeral: {text}")
        if current < nxt:
            total += nxt - current
            index += 2
        else:
            total += current
            index += 1
    return total


def normalize_part_number(data: dict) -> int | None:
    part_number = data.get("part_number")
    if isinstance(part_number, int):
        return part_number
    for key in ("part", "part_name"):
        value = data.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                try:
                    return roman_to_int(value)
                except ValueError:
                    continue
    return None


def short_summary(data: dict) -> str | None:
    for key in SUMMARY_KEYS:
        if key not in data:
            continue
        value = data[key]
        if isinstance(value, dict):
            if not value:
                return "{}"
            first_value = next(iter(value.values()))
            return str(first_value)
        return str(value)
    for value in data.values():
        if isinstance(value, str) and len(value) < 200:
            return value
    return None


def summarize_part_file(path: Path) -> tuple[object, dict]:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    data = raw if isinstance(raw, dict) else {"results": raw, "part": path.stem}
    entry = {
        "file": path.name,
        "ok": True,
        "part": data.get("part") or data.get("part_name") or data.get("part_number"),
        "part_number": normalize_part_number(data),
        "timestamp": data.get("timestamp") or data.get("date"),
        "short": short_summary(data),
    }
    return raw, entry


def iter_part_files() -> list[Path]:
    seen: set[str] = set()
    part_files: list[Path] = []
    for directory in PART_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("PART_*.json")):
            if path.name in seen:
                continue
            seen.add(path.name)
            part_files.append(path)
    return part_files


def main() -> None:
    json_files = iter_part_files()
    summaries: dict[str, object] = {}
    collected_files: list[dict] = []
    summary_by_part: dict[str, dict] = {}

    for path in json_files:
        entry = {"file": path.name, "ok": False}
        try:
            raw, entry = summarize_part_file(path)
            summaries[path.name] = raw
        except Exception as exc:
            entry["error"] = str(exc)
        collected_files.append(entry)
        summary_by_part[path.name] = {
            "part": entry.get("part"),
            "part_number": entry.get("part_number"),
            "timestamp": entry.get("timestamp"),
            "short": entry.get("short"),
            "file": path.name,
        }

    summary = {
        "count": len(json_files),
        "total_part_json_files": len(json_files),
        "file_list": [path.name for path in json_files],
        "summaries": summaries,
        "collected_files": collected_files,
        "summary_by_part": summary_by_part,
    }

    out = ROOT / "SUMMARY_RESULTS.json"
    dump_json(summary, out, indent=2, sort_keys=True)
    print(f"Collected {len(json_files)} PART_*.json files into {out}")


if __name__ == "__main__":
    main()
