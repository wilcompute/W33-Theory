"""Parse key TeX files for theorem/lemma environments, labels, numeric claims, and TODOs.
Writes JSON report to bundles/v23_toe_finish/v23/tex_claims_summary.json
"""

import json
import re
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
out = repo / "bundles" / "v23_toe_finish" / "v23" / "tex_claims_summary.json"

# files of interest (explicit)
files = [
    repo / "W33_FORMAL_THEORY.tex",
    repo / "W33_TOE_COMPLETE_v31_EXECUTEDPATCH.tex",
]
# include the bundle v50 folder if present
bundle_v50 = repo / "W33_TEX_AND_PDF_COMPLETE_BUNDLE_v50"
if bundle_v50.exists():
    files += list(bundle_v50.rglob("*.tex"))

claims = []
for f in files:
    if not f.exists():
        continue
    txt = f.read_text(encoding="utf-8", errors="ignore")
    # extract theorem/lemma environments
    for m in re.finditer(
        r"\\begin\{(theorem|lemma|proposition|claim)\}(.{0,500}?)(?:\\end\{\1\})",
        txt,
        re.S,
    ):
        env, body = m.group(1), m.group(2)
        labels = re.findall(r"\\label\{([^}]+)\}", body)
        nums = re.findall(r"\b(\d{1,6}[,\d{0,3}]*)\b", body)
        claims.append(
            {
                "file": str(f.relative_to(repo)),
                "env": env,
                "labels": labels,
                "numbers": nums,
                "excerpt": body.strip()[:200],
            }
        )
    # TODO/NB comments
    for m in re.finditer(r"%+\s*(TODO|NOTE|HINT|FIXME)[:\-]?\s*(.*)", txt):
        claims.append(
            {
                "file": str(f.relative_to(repo)),
                "todo_type": m.group(1),
                "message": m.group(2).strip(),
            }
        )

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(claims, indent=2))
print("Wrote", out)
