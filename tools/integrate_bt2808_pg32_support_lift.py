#!/usr/bin/env python3
"""Idempotently integrate the Pass 2808 insert into all three live manuscripts."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSERT = r"\input{analysis/BT2808_pg32_tetrahedral_support_lift_insert}%"

TARGETS = {
    ROOT / "w33_paper.tex": r"\input{analysis/BT2768_metaplectic_sensor_w33_insert}%",
    ROOT / "photonic_holonet.tex": r"\input{analysis/BT2771_hardware_resource_holonet_insert}%",
}


def insert_after(text: str, anchor: str, insertion: str) -> str:
    if insertion in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"anchor not found: {anchor}")
    return text.replace(anchor, anchor + "\n    " + insertion, 1)


def integrate_wrapper(path: Path, anchor: str) -> bool:
    before = path.read_text(encoding="utf-8")
    after = insert_after(before, anchor, INSERT)
    if after == before:
        return False
    path.write_text(after, encoding="utf-8")
    return True


def integrate_blueprint(path: Path) -> bool:
    before = path.read_text(encoding="utf-8")
    if INSERT in before:
        return False
    anchor = "\\tableofcontents\n\\newpage"
    if anchor not in before:
        raise RuntimeError(f"blueprint anchor not found in {path}")
    after = before.replace(
        anchor,
        "\\tableofcontents\n\\newpage\n\n" + INSERT,
        1,
    )
    path.write_text(after, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for path, anchor in TARGETS.items():
        if integrate_wrapper(path, anchor):
            changed.append(str(path.relative_to(ROOT)))
    blueprint = ROOT / "holonet_machine_blueprint.tex"
    if integrate_blueprint(blueprint):
        changed.append(str(blueprint.relative_to(ROOT)))
    print("changed:", ", ".join(changed) if changed else "none (already integrated)")


if __name__ == "__main__":
    main()
