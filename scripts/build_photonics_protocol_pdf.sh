#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TEMPLATE="$REPO_ROOT/latex/toe_template.tex"
SRC="$REPO_ROOT/docs/photonics_protocol.md"
OUT_TEX="$REPO_ROOT/docs/photonics_protocol.tex"
OUT_PDF="$REPO_ROOT/docs/photonics_protocol.pdf"
TMP_PDF="$REPO_ROOT/docs/photonics_protocol.build.pdf"
TMP_MD="$REPO_ROOT/.photonics_protocol.build.md"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is required to build the PDF." >&2
  exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Missing template $TEMPLATE" >&2
  exit 1
fi

if [ ! -f "$SRC" ]; then
  echo "ERROR: Missing source $SRC" >&2
  exit 1
fi

# Preprocess unicode math characters into LaTeX-safe forms
SRC_PATH="$SRC" TMP_PATH="$TMP_MD" python3 - <<'PY'
from pathlib import Path
import os
import re

src = Path(os.environ["SRC_PATH"])
tmp = Path(os.environ["TMP_PATH"])
text = src.read_text(encoding="utf-8")

sub_map = {
    "₀":"0","₁":"1","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9",
    "ₐ":"a","ₑ":"e","ₒ":"o","ₓ":"x","ₔ":"e","ₕ":"h","ₖ":"k","ₗ":"l","ₘ":"m","ₙ":"n","ₚ":"p","ₛ":"s","ₜ":"t",
}
sup_map = {
    "⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9",
    "⁺":"+","⁻":"-",
}

def in_code_blocks(lines):
    out = []
    fence = False
    for line in lines:
        if line.strip().startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence:
            line = line.translate(str.maketrans({
                "₀":"_0","₁":"_1","₂":"_2","₃":"_3","₄":"_4","₅":"_5","₆":"_6","₇":"_7","₈":"_8","₉":"_9",
                "⁰":"^0","¹":"^1","²":"^2","³":"^3","⁴":"^4","⁵":"^5","⁶":"^6","⁷":"^7","⁸":"^8","⁹":"^9",
                "⁺":"^+","⁻":"^-",
                "×":"x","→":"->","↔":"<->","≠":"!=","≈":"~=","✓":"OK",
            }))
            out.append(line)
            continue
        def sub_repl(m):
            base = m.group(1)
            subs = "".join(sub_map[c] for c in m.group(2))
            return f"${base}_{{{subs}}}$"
        line = re.sub(r"([\w\)\]]+)([₀-₉ₐₑₒₓₔₕₖₗₘₙₚₛₜ]+)", sub_repl, line)

        def sup_repl(m):
            base = m.group(1)
            sups = "".join(sup_map[c] for c in m.group(2))
            return f"${base}^{{{sups}}}$"
        line = re.sub(r"([A-Za-z0-9]+)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)", sup_repl, line)

        replacements = {
            "→": "\\ensuremath{\\rightarrow}",
            "↔": "\\ensuremath{\\leftrightarrow}",
            "×": "\\ensuremath{\\times}",
            "≠": "\\ensuremath{\\neq}",
            "≈": "\\ensuremath{\\approx}",
            "≅": "\\ensuremath{\\cong}",
            "⊂": "\\ensuremath{\\subset}",
            "⊆": "\\ensuremath{\\subseteq}",
            "⊃": "\\ensuremath{\\supset}",
            "⊇": "\\ensuremath{\\supseteq}",
            "∈": "\\ensuremath{\\in}",
            "∉": "\\ensuremath{\\notin}",
            "≤": "\\ensuremath{\\leq}",
            "≥": "\\ensuremath{\\geq}",
            "±": "\\ensuremath{\\pm}",
            "π": "\\ensuremath{\\pi}",
            "α": "\\ensuremath{\\alpha}",
            "β": "\\ensuremath{\\beta}",
            "γ": "\\ensuremath{\\gamma}",
            "δ": "\\ensuremath{\\delta}",
            "θ": "\\ensuremath{\\theta}",
        }
        for k, v in replacements.items():
            line = line.replace(k, v)
        out.append(line)
    return "".join(out)

lines = text.splitlines(keepends=True)
tmp.write_text(in_code_blocks(lines), encoding="utf-8")
PY

# Generate TEX

docker run --rm -v "$REPO_ROOT:/data" pandoc/latex \
  -s /data/.photonics_protocol.build.md \
  --template=/data/latex/toe_template.tex \
  -V title="Witting/W33 Photonics Protocol" \
  -V subtitle="24‑basis KS + Z₃ Pancharatnam Phase" \
  -V date="January 28, 2026" \
  --toc --number-sections \
  -o /data/docs/photonics_protocol.tex

# Generate PDF

docker run --rm -v "$REPO_ROOT:/data" pandoc/latex \
  -s /data/.photonics_protocol.build.md \
  --template=/data/latex/toe_template.tex \
  -V title="Witting/W33 Photonics Protocol" \
  -V subtitle="24‑basis KS + Z₃ Pancharatnam Phase" \
  -V date="January 28, 2026" \
  --toc --number-sections \
  --pdf-engine=pdflatex \
  -o /data/docs/photonics_protocol.build.pdf

if mv -f "$TMP_PDF" "$OUT_PDF"; then
  echo "Wrote $OUT_PDF"
else
  echo "WARNING: Could not overwrite $OUT_PDF (likely open/locked)." >&2
  echo "Left new PDF at $TMP_PDF" >&2
fi

rm -f "$TMP_MD"

echo "Wrote $OUT_TEX"
