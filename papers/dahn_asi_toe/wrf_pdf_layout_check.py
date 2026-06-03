#!/usr/bin/env python3
"""Layout sanity check for the WRF architecture PDF.

This is intentionally conservative: TeX already catches overfull boxes, while
the MuPDF pass looks for same-baseline text with overlapping horizontal spans.
Math scripts and fractions can look like same-baseline overlaps in structured
text even when the rendered page is correct, so known formula artifacts are
reported separately from unexpected collisions.
"""

from __future__ import annotations

import json
import re
import shutil
import statistics
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


HERE = Path(__file__).resolve().parent
PDF = HERE / "witting_architecture_v2.pdf"
LOG = HERE / "witting_architecture_v2.log"

LOG_PATTERNS = [
    "Overfull",
    "Underfull",
    "LaTeX Warning",
    "Package .*Warning",
    "Undefined",
    "Missing",
    "Error",
    "! ",
]

KNOWN_MATH_ARTIFACTS = [
    ("∈ F4", "3, which is"),
    ("3 Zb1", "3 ⊗ Xa2"),
    ("3 ⊗ Xa2", "3 Zb2"),
    ("3 Zb2", "3 corresponds"),
    ("= 70M · 27", "80 = 2.36"),
]


def parse_bbox(value: str) -> tuple[float, float, float, float]:
    return tuple(map(float, value.split()))  # type: ignore[return-value]


def text_and_baseline(line: ET.Element) -> tuple[str, float | None]:
    chars: list[str] = []
    baselines: list[float] = []
    for char in line.iter("char"):
        value = char.attrib.get("c", "")
        if value:
            chars.append(value)
        if "y" in char.attrib:
            baselines.append(float(char.attrib["y"]))
    if not baselines:
        return "".join(chars).strip(), None
    return "".join(chars).strip(), statistics.median(baselines)


def is_known_artifact(left: str, right: str) -> bool:
    return any(a in left and b in right for a, b in KNOWN_MATH_ARTIFACTS)


def log_hits() -> list[str]:
    if not LOG.exists():
        return [f"missing log file: {LOG}"]
    pattern = re.compile("|".join(f"(?:{item})" for item in LOG_PATTERNS))
    return [line for line in LOG.read_text(errors="ignore").splitlines() if pattern.search(line)]


def render_structured_text(tmpdir: Path) -> list[Path]:
    mutool = shutil.which("mutool")
    if not mutool:
        raise RuntimeError("mutool is required for PDF layout checking")
    subprocess.run(
        [mutool, "draw", "-q", "-F", "stext", "-o", str(tmpdir / "page_%03d.xml"), str(PDF), "1-N"],
        check=True,
    )
    return sorted(tmpdir.glob("page_*.xml"))


def baseline_collisions(xml_paths: list[Path]) -> tuple[list[dict], list[dict]]:
    expected: list[dict] = []
    unexpected: list[dict] = []
    for path in xml_paths:
        page_no = int(path.stem.split("_")[-1])
        tree = ET.parse(path)
        lines = []
        for idx, line in enumerate(tree.findall(".//line")):
            text, baseline = text_and_baseline(line)
            if not text or baseline is None:
                continue
            lines.append((idx, parse_bbox(line.attrib["bbox"]), baseline, text))

        for left_idx, left in enumerate(lines):
            line_a, bbox_a, y_a, text_a = left
            x0_a, _y0_a, x1_a, _y1_a = bbox_a
            for line_b, bbox_b, y_b, text_b in lines[left_idx + 1 :]:
                x0_b, _y0_b, x1_b, _y1_b = bbox_b
                x_overlap = min(x1_a, x1_b) - max(x0_a, x0_b)
                y_delta = abs(y_a - y_b)
                if x_overlap <= 4 or y_delta >= 2.0 or text_a == text_b:
                    continue
                row = {
                    "page": page_no,
                    "lines": [line_a, line_b],
                    "baseline_delta": round(y_delta, 3),
                    "x_overlap": round(x_overlap, 3),
                    "left": text_a[:120],
                    "right": text_b[:120],
                }
                if is_known_artifact(text_a, text_b):
                    expected.append(row)
                else:
                    unexpected.append(row)
    return expected, unexpected


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="wrf-layout-") as raw_tmp:
        xml_paths = render_structured_text(Path(raw_tmp))
        expected, unexpected = baseline_collisions(xml_paths)
    report = {
        "pdf": str(PDF),
        "pages_checked": len(xml_paths),
        "tex_log_hits": log_hits(),
        "expected_math_artifacts": expected,
        "unexpected_same_baseline_overlaps": unexpected,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    assert not report["tex_log_hits"], "TeX log has layout warnings/errors"
    assert not unexpected, "Unexpected same-baseline text overlaps found"


if __name__ == "__main__":
    main()
