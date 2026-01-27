#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TEMPLATE="$REPO_ROOT/latex/toe_template.tex"
SRC="$REPO_ROOT/FINAL_TOE_PROOF.md"
OUT_TEX="$REPO_ROOT/FINAL_TOE_PROOF.tex"
OUT_PDF="$REPO_ROOT/FINAL_TOE_PROOF.pdf"
TMP_MD="$REPO_ROOT/.final_toe_proof.build.md"

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
            # Replace unicode inside code fences with ASCII-safe equivalents
            line = line.translate(str.maketrans({
                "₀":"_0","₁":"_1","₂":"_2","₃":"_3","₄":"_4","₅":"_5","₆":"_6","₇":"_7","₈":"_8","₉":"_9",
                "⁰":"^0","¹":"^1","²":"^2","³":"^3","⁴":"^4","⁵":"^5","⁶":"^6","⁷":"^7","⁸":"^8","⁹":"^9",
                "⁺":"^+","⁻":"^-",
                "×":"x","→":"->","↔":"<->","≠":"!=","≈":"~=","✓":"OK",
            }))
            out.append(line)
            continue
        # subscript digits: Z₁₂ -> $Z_{12}$
        def sub_repl(m):
            base = m.group(1)
            subs = "".join(sub_map[c] for c in m.group(2))
            return f"${base}_{{{subs}}}$"
        line = re.sub(r"([\w\)\]]+)([₀-₉ₐₑₒₓₔₕₖₗₘₙₚₛₜ]+)", sub_repl, line)

        # superscript digits: 10⁻⁹⁰ -> $10^{-90}$
        def sup_repl(m):
            base = m.group(1)
            sups = "".join(sup_map[c] for c in m.group(2))
            return f"${base}^{{{sups}}}$"
        line = re.sub(r"([A-Za-z0-9]+)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)", sup_repl, line)

        # remaining symbols
        replacements = {
            "→": "\\ensuremath{\\rightarrow}",
            "↔": "\\ensuremath{\\leftrightarrow}",
            "×": "\\ensuremath{\\times}",
            "≠": "\\ensuremath{\\neq}",
            "≈": "\\ensuremath{\\approx}",
            "✓": "\\ensuremath{\\checkmark}",
            "α": "\\ensuremath{\\alpha}",
            "β": "\\ensuremath{\\beta}",
            "γ": "\\ensuremath{\\gamma}",
            "δ": "\\ensuremath{\\delta}",
            "ε": "\\ensuremath{\\epsilon}",
            "ζ": "\\ensuremath{\\zeta}",
            "η": "\\ensuremath{\\eta}",
            "θ": "\\ensuremath{\\theta}",
            "λ": "\\ensuremath{\\lambda}",
            "μ": "\\ensuremath{\\mu}",
            "ν": "\\ensuremath{\\nu}",
            "ξ": "\\ensuremath{\\xi}",
            "π": "\\ensuremath{\\pi}",
            "ρ": "\\ensuremath{\\rho}",
            "σ": "\\ensuremath{\\sigma}",
            "τ": "\\ensuremath{\\tau}",
            "φ": "\\ensuremath{\\phi}",
            "χ": "\\ensuremath{\\chi}",
            "ψ": "\\ensuremath{\\psi}",
            "ω": "\\ensuremath{\\omega}",
            "Δ": "\\ensuremath{\\Delta}",
            "Θ": "\\ensuremath{\\Theta}",
            "Λ": "\\ensuremath{\\Lambda}",
            "Π": "\\ensuremath{\\Pi}",
            "Σ": "\\ensuremath{\\Sigma}",
            "Φ": "\\ensuremath{\\Phi}",
            "Ψ": "\\ensuremath{\\Psi}",
            "Ω": "\\ensuremath{\\Omega}",
        }
        for k, v in replacements.items():
            line = line.replace(k, v)

        # Merge math segments followed by unicode subscripts/superscripts
        def merge_math_sub(m):
            body = m.group(1)
            subs = "".join(sub_map[c] for c in m.group(2))
            return f"${body}_{{{subs}}}$"
        line = re.sub(r"\$([^$]+)\$([₀-₉ₐₑₒₓₔₕₖₗₘₙₚₛₜ]+)", merge_math_sub, line)

        def merge_math_sup(m):
            body = m.group(1)
            sups = "".join(sup_map[c] for c in m.group(2))
            return f"${body}^{{{sups}}}$"
        line = re.sub(r"\$([^$]+)\$([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)", merge_math_sup, line)

        # Merge \( ... \) followed by unicode subscripts/superscripts
        line = re.sub(r"\\\(([^)]+)\\\)([₀-₉ₐₑₒₓₔₕₖₗₘₙₚₛₜ]+)", merge_math_sub, line)
        line = re.sub(r"\\\(([^)]+)\\\)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)", merge_math_sup, line)

        out.append(line)
    return "".join(out)

lines = text.splitlines(keepends=True)
tmp.write_text(in_code_blocks(lines), encoding="utf-8")
PY

# Generate TEX

docker run --rm -v "$REPO_ROOT:/data" pandoc/latex \
  -s /data/.final_toe_proof.build.md \
  --template=/data/latex/toe_template.tex \
  -V title="W33 Theory of Everything — Final Proof" \
  -V subtitle="E8 → W33 via Coxeter 6-cycles" \
  -V date="January 27, 2026" \
  --toc --number-sections \
  -o /data/FINAL_TOE_PROOF.tex

# Generate PDF

docker run --rm -v "$REPO_ROOT:/data" pandoc/latex \
  -s /data/.final_toe_proof.build.md \
  --template=/data/latex/toe_template.tex \
  -V title="W33 Theory of Everything — Final Proof" \
  -V subtitle="E8 → W33 via Coxeter 6-cycles" \
  -V date="January 27, 2026" \
  --toc --number-sections \
  --pdf-engine=pdflatex \
  -o /data/FINAL_TOE_PROOF.pdf

rm -f "$TMP_MD"

echo "Wrote $OUT_TEX"
echo "Wrote $OUT_PDF"
