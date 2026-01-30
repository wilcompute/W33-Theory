import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Locate SUMMARY_RESULTS.json (repo-root or inside claude_workspace)
possible = [
    ROOT / "SUMMARY_RESULTS.json",
    ROOT / "claude_workspace" / "SUMMARY_RESULTS.json",
]
if summary_path is None:
    raise FileNotFoundError(
        "SUMMARY_RESULTS.json not found in repo root or claude_workspace"
    )
res = []
# Collect candidate filenames robustly from different summary formats
file_list = []
if isinstance(summary.get("summaries"), dict) and summary.get("summaries"):
    file_list = list(summary.get("summaries").keys())
elif isinstance(summary.get("collected_files"), list) and summary.get(
    "collected_files"
):
    file_list = [
        entry.get("file")
        for entry in summary.get("collected_files")
        if entry.get("file")
    ]
else:
    # fallback to scanning PART_*.json in the repo
    file_list = [p.name for p in ROOT.glob("PART_*.json")]


# write file
out = summary_path.parent / "NUMERIC_COMPARISONS.json"


def main():
    summary_path = next((p for p in possible if p.exists()), None)
    summary = json.load(open(summary_path))
    print("Using SUMMARY_RESULTS at:", summary_path)
    for fname in file_list:
        # DESI
        kr = None
        # try reading original PART file to get numeric values precisely
        partfile = ROOT / fname
        if partfile.exists():
            try:
                data = json.load(open(partfile))
            except Exception:
                data = {}
        else:
            data = {}
        kr = data.get("key_results") or {}
        # Look for DESI dark energy entries with tolerant key matching (allow year suffixes)
        if isinstance(kr, dict):
            for key, val in kr.items():
                k_lower = key.lower()
                if "desi" in k_lower or ("dark" in k_lower and "energy" in k_lower):
                    dd = val if isinstance(val, dict) else {}
                    # Find measured and predicted keys heuristically
                    m_key = None
                    p_key = None
                    for kk in dd.keys():
                        kl = kk.lower()
                        if "w0" in kl and ("measure" in kl or "measured" in kl):
                            m_key = kk
                        if "w33" in kl or "w33_pred" in kl or "pred" in kl:
                            p_key = kk
                    # fallback: any key containing 'w0' and any key containing 'pred' or 'w33'
                    if m_key is None:
                        for kk in dd.keys():
                            if "w0" in kk.lower():
                                m_key = kk
                    if p_key is None:
                        for kk in dd.keys():
                            if "pred" in kk.lower() or "w33" in kk.lower():
                                p_key = kk
                    if m_key and p_key:
                        try:
                            m = float(dd[m_key])
                            p = float(dd[p_key])
                            res.append(
                                {
                                    "file": fname,
                                    "name": "DESI w0",
                                    "measured": m,
                                    "predicted": p,
                                    "diff": p - m,
                                    "pct": (
                                        (abs(p - m) / abs(m)) * 100 if m != 0 else None
                                    ),
                                }
                            )
                        except Exception:
                            pass
                    break  # stop after first DESI-like key found
    print("Found numeric comparisons entries:", len(res))
    print("Writing to:", out)
    with open(out, "w") as f:
        json.dump(res, f, indent=2, default=int)
    print("Wrote", out, "entries:", len(res))


if __name__ == "__main__":
    main()
