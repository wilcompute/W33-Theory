#!/usr/bin/env python3
"""Idempotently integrate Passes 3205-3213 into all four canonical front doors."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_INPUT = r"    \input{analysis/BT3212_chromatic_closure_insert}%"
TEX_ANCHOR = r"    \input{analysis/BT3191_chromatic_defect_block_filter_insert}%"
HTML_BEGIN = "<!-- BT3205-BT3213-CHROMATIC-CLOSURE -->"
HTML_END = "<!-- /BT3205-BT3213-CHROMATIC-CLOSURE -->"


def integrate_tex(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if TEX_INPUT in text:
        return text
    if TEX_ANCHOR not in text:
        raise RuntimeError(f"missing Pass 3191 anchor in {path}")
    return text.replace(TEX_ANCHOR, TEX_ANCHOR + "\n" + TEX_INPUT, 1)


def integrate_index(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    insert = (ROOT / "analysis" / "BT3212_chromatic_closure_index_insert.html").read_text(encoding="utf-8").strip()
    if HTML_BEGIN in text:
        start = text.index(HTML_BEGIN)
        end = text.index(HTML_END, start) + len(HTML_END)
        return text[:start] + insert + text[end:]
    anchor = "    <h2>Passes 3187–3192: the last chromatic bit gets a proof filter</h2>"
    if anchor not in text:
        raise RuntimeError("missing public-index chromatic anchor")
    return text.replace(anchor, insert + "\n\n" + anchor, 1)


def desired() -> dict[Path, str]:
    return {
        ROOT / "w33_paper.tex": integrate_tex(ROOT / "w33_paper.tex"),
        ROOT / "photonic_holonet.tex": integrate_tex(ROOT / "photonic_holonet.tex"),
        ROOT / "holonet_machine_blueprint.tex": integrate_tex(ROOT / "holonet_machine_blueprint.tex"),
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
