#!/usr/bin/env python3
"""Idempotently integrate the Pass 3187-3192 theorem into all front doors."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_INPUT = r"    \input{analysis/BT3191_chromatic_defect_block_filter_insert}%"
BLUEPRINT_INPUT = r"\input{analysis/BT3191_chromatic_defect_block_filter_insert}"
HTML_BEGIN = "<!-- BT3187-BT3192-CHROMATIC-DEFECT-FILTER -->"
HTML_END = "<!-- /BT3187-BT3192-CHROMATIC-DEFECT-FILTER -->"


def integrate_wrapper(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if TEX_INPUT in text:
        return text
    anchor = r"    \input{analysis/BT3124_BT3132_deep_five_front_closure_insert}%"
    if anchor not in text:
        raise RuntimeError(f"missing wrapper anchor in {path}")
    return text.replace(anchor, anchor + "\n" + TEX_INPUT, 1)


def integrate_blueprint(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if BLUEPRINT_INPUT in text:
        return text
    anchor = "\\tableofcontents\n\\newpage"
    if anchor not in text:
        raise RuntimeError("missing blueprint table-of-contents anchor")
    replacement = anchor + "\n\n" + BLUEPRINT_INPUT + "\n\\newpage"
    return text.replace(anchor, replacement, 1)


def integrate_index(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT3191_chromatic_defect_block_filter_index_insert.html").read_text(encoding="utf-8").strip()
    if HTML_BEGIN in text:
        start = text.index(HTML_BEGIN)
        end = text.index(HTML_END, start) + len(HTML_END)
        return text[:start] + insert + text[end:]
    for anchor in ("</main>", "</body>"):
        if anchor in text:
            return text.replace(anchor, insert + "\n" + anchor, 1)
    raise RuntimeError("missing docs/index.html insertion anchor")


def desired():
    return {
        ROOT / "w33_paper.tex": integrate_wrapper(ROOT / "w33_paper.tex"),
        ROOT / "photonic_holonet.tex": integrate_wrapper(ROOT / "photonic_holonet.tex"),
        ROOT / "holonet_machine_blueprint.tex": integrate_blueprint(ROOT / "holonet_machine_blueprint.tex"),
        ROOT / "docs" / "index.html": integrate_index(ROOT / "docs" / "index.html"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = []
    for path, target in desired().items():
        current = path.read_text(encoding="utf-8")
        if current != target:
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(target, encoding="utf-8")
    if args.check and changed:
        raise SystemExit("integration drift: " + ", ".join(changed))
    print("PASS integrated" if not changed else "UPDATED " + ", ".join(changed))


if __name__ == "__main__":
    main()
