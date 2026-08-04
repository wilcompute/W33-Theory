#!/usr/bin/env python3
"""Idempotently materialize Passes 3320--3331 into wrapper or monolithic front doors."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "analysis/BT3330_global_cover_quantum_hypercube_insert.tex"
HTML_PATH = ROOT / "analysis/BT3330_global_cover_quantum_hypercube_index_insert.html"
TEX_INPUT = r"\input{analysis/BT3330_global_cover_quantum_hypercube_insert}%"
TEX_LABEL = r"\label{sec:global-cover-quantum-hypercube}"
HTML_ID = 'id="bt3320-3331-global-cover-quantum-hypercube"'
TARGETS = ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex")


def integrate_tex(text: str, insert: str) -> tuple[str, str]:
    """Insert by reference into a lightweight wrapper, or inline into a monolithic paper."""
    if TEX_INPUT in text or TEX_LABEL in text:
        return text, "already_present"

    wrapper_anchor = "  }%\n}\n\\input{"
    if wrapper_anchor in text:
        pos = text.index(wrapper_anchor)
        return text[:pos] + f"    {TEX_INPUT}\n" + text[pos:], "wrapper_input"

    pos = text.rfind(r"\end{document}")
    if pos >= 0:
        return text[:pos] + "\n" + insert.rstrip() + "\n" + text[pos:], "monolithic_insert"

    raise ValueError("neither wrapper anchor nor \\end{document} found")


def integrate_html(text: str, insert: str) -> tuple[str, str]:
    if HTML_ID in text:
        return text, "already_present"
    lower = text.lower()
    pos = lower.rfind("</main>")
    if pos < 0:
        pos = lower.rfind("</body>")
    if pos < 0:
        raise ValueError("missing </main> or </body> insertion point")
    return text[:pos] + insert.rstrip() + "\n" + text[pos:], "html_insert"


def run(root: Path, check: bool = False) -> dict:
    tex = (root / TEX_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    html = (root / HTML_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    report = {
        "schema": "w33.front_door_reachability.v1",
        "check_only": check,
        "targets": {},
    }

    for name in TARGETS:
        path = root / name
        old = path.read_text(encoding="utf-8")
        new, mode = integrate_tex(old, tex)
        changed = new != old
        if changed and not check:
            path.write_text(new, encoding="utf-8")
        report["targets"][name] = {"mode": mode, "changed": changed}

    path = root / "docs/index.html"
    old = path.read_text(encoding="utf-8")
    new, mode = integrate_html(old, html)
    changed = new != old
    if changed and not check:
        path.write_text(new, encoding="utf-8")
    report["targets"]["docs/index.html"] = {"mode": mode, "changed": changed}
    report["all_reachable_after_run"] = True
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    report = run(args.root.resolve(), check=args.check)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
