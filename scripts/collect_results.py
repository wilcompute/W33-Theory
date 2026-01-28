import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

summary = {"collected_files": [], "count": len(json_files), "summary_by_part": {}}

# keys to try for a short description
summary_keys = [
    "key_finding",
    "key_insight",
    "key_finding",
    "key_result",
    "key_results",
    "title",
    "summary",
]

for jf in json_files:
    entry = {"file": jf.name}
    try:
        with open(jf, "r") as f:
            data = json.load(f)
        entry["ok"] = True

        # Handle array-valued PART files (wrap in an object)
        if isinstance(data, list):
            data = {"results": data, "part": jf.stem}

        # grab canonical metadata if present
        part = data.get("part") or data.get("part_name") or data.get("part_number")
        # Normalize part_number to an integer when possible. Some PART files use roman numerals in 'part'.
        part_number = (
            data.get("part_number") if data.get("part_number") is not None else None
        )
        if part_number is None:
            p = data.get("part") or data.get("part_name") or None
            if isinstance(p, int):
                part_number = p
            elif isinstance(p, str):
                # try decimal integer
                try:
                    part_number = int(p)
                except Exception:
                    # try basic Roman numeral parsing (supports up to a few hundred)
                    def roman_to_int(s: str) -> int:
                        roman_map = {
                            "I": 1,
                            "V": 5,
                            "X": 10,
                            "L": 50,
                            "C": 100,
                            "D": 500,
                            "M": 1000,
                        }
                        s = s.upper()
                        i = 0
                        total = 0
                        while i < len(s):
                            if i + 1 < len(s) and roman_map.get(s[i]) < roman_map.get(
                                s[i + 1], 0
                            ):
                                total += roman_map[s[i + 1]] - roman_map[s[i]]
                                i += 2
                            else:
                                total += roman_map.get(s[i], 0)
                                i += 1
                        if total == 0:
                            raise ValueError("Not a Roman numeral")
                        return total

                    try:
                        part_number = roman_to_int(p)
                    except Exception:
                        part_number = None
        timestamp = data.get("timestamp") or data.get("date") or None
        short = None
        for k in summary_keys:
            if k in data:
                # convert dicts to brief string if necessary
                v = data[k]
                if isinstance(v, dict):
                    short = next(iter(v.values())) if v else str(v)
                else:
                    short = str(v)
                break
        if not short:
            # fallback to the first top-level string field
            for k, v in data.items():
                if isinstance(v, str) and len(v) < 200:
                    short = v
                    break
        entry["part"] = part
        entry["part_number"] = part_number
        entry["timestamp"] = timestamp
        entry["short"] = short

        # numeric comparisons: search for measured/predicted pairs
        comparisons = []

        def scan_for_pairs(d):
            # recursively scan dicts for measured and predicted keys
            if not isinstance(d, dict):
                return
            for k, v in d.items():
                if isinstance(v, dict):
                    scan_for_pairs(v)
                else:
                    pass
            # check keys in this dict
            keys = set(d.keys())
            measured_keys = [
                k
                for k in keys
                if "meas" in k.lower()
                or "observ" in k.lower()
                or "experimental" in k.lower()
            ]
            pred_keys = [
                k
                for k in keys
                if "pred" in k.lower()
                or "w33" in k.lower()
                or "predicted" in k.lower()
                or "value" in k.lower()
            ]
            for mk in measured_keys:
                for pk in pred_keys:
                    try:
                        m = float(d[mk])
                        p = float(d[pk])
                        diff = p - m
                        pct = (abs(diff) / abs(m)) * 100 if m != 0 else None
                        comparisons.append(
                            {
                                "measured_key": mk,
                                "predicted_key": pk,
                                "measured": m,
                                "predicted": p,
                                "difference": diff,
                                "percent_diff": pct,
                            }
                        )
                    except Exception:
                        continue

        scan_for_pairs(data)
        if comparisons:
            entry["comparisons"] = comparisons

        # Special-case known experiment structures (e.g., DESI dark energy)
        # DESI: data['key_results']['desi_dark_energy'] with 'w0_measured' and 'w0_w33_predicted'
        try:
            kr = data.get("key_results") or {}
            if isinstance(kr, dict) and "desi_dark_energy" in kr:
                dd = kr["desi_dark_energy"]
                if "w0_measured" in dd and "w0_w33_predicted" in dd:
                    m = float(dd["w0_measured"])
                    p = float(dd["w0_w33_predicted"])
                    diff = p - m
                    pct = (abs(diff) / abs(m)) * 100 if m != 0 else None
                    entry.setdefault("comparisons", []).append(
                        {
                            "name": "DESI w0",
                            "measured": m,
                            "predicted": p,
                            "difference": diff,
                            "percent_diff": pct,
                        }
                    )
        except Exception:
            pass

        summary["collected_files"].append(entry)

        # add to summary_by_part keyed by filename
        summary["summary_by_part"][jf.name] = {
            "part": part,
            "part_number": part_number,
            "timestamp": timestamp,
            "short": short,
            "file": jf.name,
            "comparisons": comparisons if comparisons else None,
        }
    except Exception as e:
        entry["ok"] = False
        entry["error"] = str(e)
        summary["collected_files"].append(entry)

# Compatibility: add a couple of keys expected by downstream scripts/tests
# Build a simple mapping `summaries` filename -> metadata for backward compatibility
summaries_map = {}
summary["summaries"] = summaries_map

from utils.json_safe import dump_json

out = ROOT / "SUMMARY_RESULTS.json"


def main():
    sys.path.insert(0, str(ROOT))
    json_files = sorted(ROOT.glob("PART_*.json"))
    summary["total_part_json_files"] = len(json_files)
    for entry in summary["collected_files"]:
        fname = entry.get("file")
        if not fname:
            continue
        sm = {}
        # Include 'part' only if present and a string
        if entry.get("part"):
            sm["part"] = entry.get("part")
        # Only include integer part_number if available
        if entry.get("part_number") is not None:
            sm["part_number"] = entry.get("part_number")
        # Keep a short text field if present
        if entry.get("short"):
            sm["short"] = entry.get("short")
        # Only include timestamp if present and non-null (schema expects a string)
        if entry.get("timestamp"):
            sm["timestamp"] = entry.get("timestamp")
        summaries_map[fname] = sm
    dump_json(summary, out, indent=2, sort_keys=True)
    print(f"Collected {len(json_files)} PART_*.json files into {out}")


if __name__ == "__main__":
    main()
