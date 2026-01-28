import json
import sys
from pathlib import Path

art_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("artifacts/sage-part-jsons")
if not art_dir.exists():
    print(f"Artifact directory {art_dir} not found", file=sys.stderr)
    sys.exit(2)

json_files = sorted(art_dir.glob("PART_*.json"))
if not json_files:
    print(f"No PART_*.json files found in {art_dir}", file=sys.stderr)
    sys.exit(1)

summary = {
    "total_part_json_files": len(json_files),
    "file_list": [p.name for p in json_files],
    "summaries": {},
}
for jf in json_files:
    try:
        data = json.loads(jf.read_text())
        summary["summaries"][jf.name] = data
    except Exception as e:
        summary["summaries"][jf.name] = {"error": str(e)}

out = Path("SUMMARY_RESULTS.json")
out.write_text(json.dumps(summary, indent=2, sort_keys=True))
print(f"Wrote {out} (collected {len(json_files)} PART_*.json files)")

# Run numeric comparisons extractor if available
extractor_candidates = [
    Path("scripts/make_numeric_comparisons_from_summary.py"),
    Path("claude_workspace/scripts/make_numeric_comparisons_from_summary.py"),
]
found_extractor = False
for extractor in extractor_candidates:
    if extractor.exists():
        found_extractor = True
        try:
            import subprocess

            subprocess.check_call([sys.executable, str(extractor)])
            print("Ran numeric comparisons extractor:", extractor)
        except Exception as e:
            print("Numeric extractor failed:", e)
        break
if not found_extractor:
    print("Numeric extractor not found; skipping")
