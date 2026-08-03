#!/usr/bin/env python3
"""Idempotently promote Passes 2847--2853 into canonical public artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSERT = r"\input{analysis/BT2847_BT2853_protected_observer_noisy_m36_insert}%"


def patch_wrapper(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if INSERT in text:
        return False
    anchor = r"\input{analysis/BT2820_BT2824_blueprint_hardening_insert}%"
    if anchor not in text:
        anchor = r"\input{analysis/BT2808_pg32_tetrahedral_support_lift_insert}%"
    if anchor not in text:
        raise RuntimeError(f"no wrapper anchor in {path}")
    path.write_text(text.replace(anchor, anchor + "\n    " + INSERT, 1), encoding="utf-8")
    return True


def patch_blueprint(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if INSERT in text:
        return False
    text = text.replace("Passes 2700--2802", "Passes 2700--2853", 1)
    marker = r"\end{document}"
    if marker not in text:
        raise RuntimeError("blueprint end marker absent")
    path.write_text(text.replace(marker, INSERT + "\n" + marker, 1), encoding="utf-8")
    return True


def patch_index(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'id="pass-2847-2853-protected-observer"' in text:
        return False
    section = '''
<section id="pass-2847-2853-protected-observer" class="section theorem-section">
  <div class="section-number">Passes 2847--2853</div>
  <h2>Protected and active support telemetry</h2>
  <p>The fixed 52-bit distance-four trajectory has an exact 28-tap puncturing optimum. A changed affine-square measurement schedule needs only 24 samples: twelve support features observed twice.</p>
  <p>The eight shortest observer words carry a distance-four digraph of automorphism order 32, while the 48 minimum fast selectors have automorphism order 6912 and structure S3 x (S4 wreath S2).</p>
  <p>Asymmetric-channel maximum-likelihood decoding cuts modelled word errors by more than 70% in the tested profiles. Active no-reset support feedback identifies every frame in at most four operations.</p>
  <p>The phenomenological noisy M36 recurrence has a golden saddle node at g=(7-3sqrt(5))/4 and p=(3-sqrt(5))/2; this is an analytic operating envelope, not a fault-tolerant threshold.</p>
</section>
'''
    marker = "</body>"
    if marker in text:
        text = text.replace(marker, section + marker, 1)
    else:
        text += section
    path.write_text(text, encoding="utf-8")
    return True


def close_registry(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") == "complete":
        return False
    data["status"] = "complete"
    data["completion"] = {
        "verifier": "analysis/bt2847_2853_protected_observer_noisy_m36.py",
        "certificate": "data/PART_BT2847_BT2853_PROTECTED_OBSERVER_NOISY_M36_results.json",
        "rtl": [
            "rtl/w33_pass2848_affine_square_feature_encoder.sv",
            "rtl/w33_pass2853_affine_square_nn_decoder.sv"
        ],
        "insert": "analysis/BT2847_BT2853_protected_observer_noisy_m36_insert.tex"
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        if patch_wrapper(ROOT / name):
            changed.append(name)
    if patch_blueprint(ROOT / "holonet_machine_blueprint.tex"):
        changed.append("holonet_machine_blueprint.tex")
    if patch_index(ROOT / "docs" / "index.html"):
        changed.append("docs/index.html")
    registry = ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "2847-2853.json"
    if close_registry(registry):
        changed.append(str(registry.relative_to(ROOT)))
    print("changed:", ", ".join(changed) if changed else "none")


if __name__ == "__main__":
    main()
