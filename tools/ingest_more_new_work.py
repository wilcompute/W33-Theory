#!/usr/bin/env python3
"""
Ingest and summarize the 'More New Work' drop folder.

Produces:
  - artifacts/more_new_work_digest.json
  - artifacts/more_new_work_digest.md

This is meant to be deterministic and lightweight: it indexes files, extracts
brief previews, and pulls a few key metrics from known JSON structures.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
DROP_DIR = REPO_ROOT / "More New Work"
EXTRACT_DIR = REPO_ROOT / "artifacts" / "more_new_work_extracted"
OUT_JSON = REPO_ROOT / "artifacts" / "more_new_work_digest.json"
OUT_MD = REPO_ROOT / "artifacts" / "more_new_work_digest.md"


TEXT_EXTS = {".md", ".txt", ".py", ".json", ".yml", ".yaml"}
SKIP_EXTS = {".pyc"}


def sha256_path(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read_text(p: Path, max_bytes: int = 200_000) -> str:
    data = p.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")


def preview_lines(text: str, n: int = 40) -> str:
    lines = text.replace("\r\n", "\n").splitlines()
    return "\n".join(lines[:n])


def try_load_json(p: Path) -> Optional[Any]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def extract_json_metrics(obj: Any) -> Dict[str, Any]:
    """
    Heuristically extract a few high-signal metrics if present.
    """
    if not isinstance(obj, dict):
        return {}
    metrics: Dict[str, Any] = {}
    # Common fields from the unified pipeline reports
    for k in ["checks", "stage1_double_sixes", "stage2_verify_bridge", "stage3_fusion"]:
        if k in obj and isinstance(obj[k], dict):
            metrics[k] = list(obj[k].keys())
    if "checks" in obj and isinstance(obj["checks"], dict):
        chk = obj["checks"]
        if "dynkin_candidate" in chk and isinstance(chk["dynkin_candidate"], dict):
            metrics["dynkin_candidate"] = {
                "score": chk["dynkin_candidate"].get("score"),
                "source": chk["dynkin_candidate"].get("source"),
            }
        if "firewall" in chk and isinstance(chk["firewall"], dict):
            metrics["firewall"] = {
                "good": chk["firewall"].get("good"),
                "bad": chk["firewall"].get("bad"),
                "total": chk["firewall"].get("total"),
            }
    # Dynkin attempt artifacts
    if "best" in obj and isinstance(obj["best"], dict):
        b = obj["best"]
        for k in ["score", "idxs", "C_round", "C_real"]:
            if k in b:
                metrics.setdefault("best", {})[k] = b[k]
    for k in [
        "cartan_rank",
        "root_clusters",
        "stabilizer_count",
        "tol",
        "eps_root",
        "score",
    ]:
        if k in obj:
            metrics[k] = obj[k]
    # PG(3,2) artifacts
    if "summary" in obj and isinstance(obj["summary"], dict):
        metrics["summary"] = obj["summary"]
    for k in ["points", "lines"]:
        if k in obj and isinstance(obj[k], list):
            metrics[f"n_{k}"] = len(obj[k])
    return metrics


def try_extract_pdf_text(
    p: Path, max_pages: int = 2, max_chars: int = 2000
) -> Optional[str]:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    try:
        reader = PdfReader(str(p))
        parts: List[str] = []
        for page in reader.pages[:max_pages]:
            parts.append(page.extract_text() or "")
        text = "\n".join(parts)
        text = "\n".join(line.rstrip() for line in text.splitlines() if line.strip())
        return text[:max_chars]
    except Exception:
        return None


def compare_if_duplicate(p: Path) -> Optional[Dict[str, Any]]:
    """
    If the file also exists in the repo at the same basename under tools/,
    compare contents and report whether identical.
    """
    if p.suffix != ".py":
        return None
    candidate = REPO_ROOT / "tools" / p.name
    if not candidate.exists():
        return None
    try:
        same = p.read_bytes() == candidate.read_bytes()
    except Exception:
        same = False
    return {"repo_candidate": str(candidate), "identical": bool(same)}


def walk_files() -> List[Path]:
    files: List[Path] = []
    for base in [DROP_DIR, EXTRACT_DIR]:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() not in SKIP_EXTS:
                files.append(p)
    # De-dup by path
    return sorted(set(files), key=lambda x: x.as_posix())


def safe_extract_zip(zip_path: Path, dest_dir: Path) -> None:
    """
    Extract a zip into dest_dir with basic path-traversal protection.

    We treat zip member names as relative paths and refuse anything that would
    escape the destination directory.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            name = info.filename
            # Skip macOS metadata and empty names.
            if not name or name.startswith("__MACOSX/") or "/__MACOSX/" in name:
                continue
            out_path = (dest_dir / name).resolve()
            if (
                dest_dir.resolve() not in out_path.parents
                and out_path != dest_dir.resolve()
            ):
                raise RuntimeError(f"Refusing to extract unsafe path: {name}")
            if name.endswith("/"):
                out_path.mkdir(parents=True, exist_ok=True)
                continue
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, "r") as src, out_path.open("wb") as dst:
                shutil.copyfileobj(src, dst)


def ensure_zips_extracted() -> None:
    """
    Keep `artifacts/more_new_work_extracted/` in sync with the current drop zips.

    Each zip is extracted into:
      artifacts/more_new_work_extracted/<zip_stem>/
    and tagged with `.source_sha256` so we can skip re-extraction when unchanged.
    """
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    for z in sorted(DROP_DIR.glob("*.zip")):
        dest = EXTRACT_DIR / z.stem
        sha = sha256_path(z)
        tag = dest / ".source_sha256"
        if (
            dest.exists()
            and tag.exists()
            and tag.read_text(encoding="utf-8", errors="replace").strip() == sha
        ):
            continue
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        safe_extract_zip(z, dest)
        tag.write_text(sha + "\n", encoding="utf-8")


def main() -> None:
    if not DROP_DIR.exists():
        # Allow missing drop directory in test environments — proceed with an
        # empty digest. This keeps the tool deterministic and non-fatal when
        # no external drop has been provided.
        print(f"Warning: missing drop directory {DROP_DIR}; proceeding with empty digest")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Ensure extracted view is up-to-date so the digest can see inside zips.
    ensure_zips_extracted()

    digest: Dict[str, Any] = {
        "drop_dir": str(DROP_DIR),
        "extract_dir": str(EXTRACT_DIR),
        "files": [],
    }

    for p in walk_files():
        rel = p.relative_to(REPO_ROOT).as_posix()
        info: Dict[str, Any] = {
            "path": rel,
            "size": p.stat().st_size,
            "sha256": sha256_path(p),
            "suffix": p.suffix.lower(),
        }
        if info["suffix"] in TEXT_EXTS:
            text = safe_read_text(p)
            info["preview"] = preview_lines(text, n=60)
            if info["suffix"] == ".json":
                obj = try_load_json(p)
                if obj is not None:
                    info["json_keys"] = (
                        list(obj.keys()) if isinstance(obj, dict) else None
                    )
                    info["json_metrics"] = extract_json_metrics(obj)
        if info["suffix"] == ".pdf":
            info["pdf_text_preview"] = try_extract_pdf_text(p)

        dup = compare_if_duplicate(p)
        if dup is not None:
            info["duplicate_check"] = dup

        digest["files"].append(info)

    OUT_JSON.write_text(json.dumps(digest, indent=2), encoding="utf-8")

    # Render a lightweight markdown report.
    lines: List[str] = []
    lines.append("# More New Work digest")
    lines.append("")
    lines.append(f"- Drop dir: `{DROP_DIR}`")
    lines.append(f"- Extract dir: `{EXTRACT_DIR}`")
    lines.append(f"- Files indexed: {len(digest['files'])}")
    lines.append("")

    # Highlight a few known “newest” items
    newest_paths = [
        "artifacts/more_new_work_extracted/NewestWork2_2_2026_delta_v3p8/Newest Work 2_2_2026/artifacts_unified_v3/pg32_report.md",
        "artifacts/more_new_work_extracted/NewestWork2_2_2026_delta_v3p8/Newest Work 2_2_2026/artifacts_unified_v3/pg32_points_from_remaining15.json",
        "artifacts/more_new_work_extracted/NewestWork2_2_2026_delta_v3p8/Newest Work 2_2_2026/artifacts_unified_v3/pg32_lines_from_remaining15.json",
        "artifacts/more_new_work_extracted/NewestWork2_2_2026_delta_v3/Newest Work 2_2_2026/artifacts_unified_v3/UNIFIED_REPORT_V3.json",
        "artifacts/more_new_work_extracted/NewestWork2_2_2026_extended_bundle_v3/chat_artifacts/toe_step3_dynkin_lock_attempt_v2.json",
    ]
    lines.append("## Spotlight files")
    for sp in newest_paths:
        lines.append(f"- `{sp}`")
    lines.append("")

    lines.append("## File previews (truncated)")
    for f in digest["files"]:
        path = f["path"]
        lines.append(f"### `{path}`")
        lines.append(f"- size={f['size']} sha256={f['sha256'][:12]}…")
        if "duplicate_check" in f:
            dc = f["duplicate_check"]
            lines.append(
                f"- duplicate_of={dc['repo_candidate']} identical={dc['identical']}"
            )
        if f.get("json_metrics"):
            lines.append(
                f"- json_metrics: `{json.dumps(f['json_metrics'], ensure_ascii=False)[:2000]}`"
            )
        if f.get("pdf_text_preview"):
            lines.append("```")
            lines.append(f.get("pdf_text_preview") or "")
            lines.append("```")
        if f.get("preview"):
            lines.append("```")
            lines.append(f.get("preview") or "")
            lines.append("```")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
