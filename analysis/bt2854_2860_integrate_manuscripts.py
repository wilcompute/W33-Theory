#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSERT = r"    \input{analysis/BT2854_BT2860_seven_frontiers_insert}%"
ANCHORS = {
    "w33_paper.tex": r"    \input{analysis/BT2809_BT2815_seven_frontiers_insert}%",
    "photonic_holonet.tex": r"    \input{analysis/BT2809_BT2815_seven_frontiers_insert}%",
}


def integrate_wrapper(path: Path, anchor: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if INSERT in text:
        return False
    if anchor not in text:
        raise SystemExit(f"anchor missing in {path}: {anchor}")
    path.write_text(text.replace(anchor, anchor + "\n" + INSERT, 1), encoding="utf-8")
    return True


def integrate_blueprint(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    marker = r"\input{analysis/BT2854_BT2860_seven_frontiers_insert}"
    if marker in text:
        return False
    end = text.rfind(r"\end{document}")
    if end < 0:
        raise SystemExit(f"no end document in {path}")
    block = "\n% Passes 2854--2860 exact support closure.\n" + marker + "\n"
    path.write_text(text[:end] + block + text[end:], encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for name, anchor in ANCHORS.items():
        path = ROOT / name
        if path.exists() and integrate_wrapper(path, anchor):
            changed.append(name)
    blueprint = ROOT / "holonet_machine_blueprint.tex"
    if blueprint.exists() and integrate_blueprint(blueprint):
        changed.append(blueprint.name)
    print("changed=" + ",".join(changed) if changed else "already integrated")


if __name__ == "__main__":
    main()
