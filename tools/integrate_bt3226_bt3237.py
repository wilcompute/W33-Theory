#!/usr/bin/env python3
"""Idempotently wire the Passes 3226-3234 insert into four canonical front doors."""
from __future__ import annotations
import argparse
from pathlib import Path

BEGIN = "% BEGIN PASS3226_3234_PORT_SPIRAL"
END = "% END PASS3226_3234_PORT_SPIRAL"
HBEGIN = "<!-- BEGIN PASS3226_3234_PORT_SPIRAL -->"
HEND = "<!-- END PASS3226_3234_PORT_SPIRAL -->"


def replace_or_insert(text: str, payload: str, begin: str, end: str, anchor: str) -> str:
    if begin in text:
        left = text.index(begin)
        right = text.index(end, left) + len(end)
        return text[:left] + payload.rstrip() + text[right:]
    pos = text.rfind(anchor)
    if pos < 0:
        raise RuntimeError(f"required anchor not found: {anchor!r}")
    return text[:pos] + payload.rstrip() + "\n\n" + text[pos:]


def update(path: Path, payload: str, begin: str, end: str, anchor: str) -> bool:
    old = path.read_text()
    new = replace_or_insert(old, payload, begin, end, anchor)
    if new == old:
        return False
    path.write_text(new)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    root = args.root
    tex = (root / "analysis/BT3235_port_spiral_insert.tex").read_text()
    html = (root / "analysis/BT3235_port_spiral_index_insert.html").read_text()
    changed = []
    for name in ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex"):
        if update(root / name, tex, BEGIN, END, "\\end{document}"):
            changed.append(name)
    if update(root / "docs/index.html", html, HBEGIN, HEND, "</main>"):
        changed.append("docs/index.html")
    print("changed=" + (",".join(changed) if changed else "none"))


if __name__ == "__main__":
    main()
