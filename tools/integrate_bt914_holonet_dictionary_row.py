#!/usr/bin/env python3
"""BT914 - integrate the profile row into the Holonet physics-to-architecture dictionary.

Idempotent patcher for photonic_holonet.tex.  It inserts a table row after the
magic-strata row in Section 14.4, plus a short paragraph explaining the
C^9=(2+2+2+2)+1 profile layer and sentinel coordinate.
"""
from __future__ import annotations
from pathlib import Path

TARGET = Path("photonic_holonet.tex")
ANCHOR = "magic strata $8+24+4$ & fermion shell grading & fuel octanes\\\\"
ROW = "profile multiplicity $9\\cdot\\mathbf2$ & CKM/PMNS/Koide coordinate layer & four profile planes plus sentinel\\\\"
PARA_ANCHOR = "The first row carries the deepest identification, drawn from the companion paper"
PARA = """The new profile row is a guardrail rather than a new particle claim.  BT897--BT914 place the numerical Cabibbo/PMNS/Koide scaffold inside the multiplicity factor
\\[
\\mathbb C^9=(2+2+2+2)+1,
\\]
where the four two-planes carry the searched substrate fractions $9/178$, $4/13$, $2/91$, and $7/13$, while the final $+1$ is a sentinel/provenance coordinate.  It is not a sterile generation: it monitors profile drift, stale release artifacts, and $g=15$ fault energy.\n\n"""

def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if ROW not in text:
        if ANCHOR not in text:
            raise SystemExit("BT914 missing dictionary anchor")
        text = text.replace(ANCHOR, ANCHOR + "\n" + ROW, 1)
    if PARA not in text:
        if PARA_ANCHOR not in text:
            raise SystemExit("BT914 missing paragraph anchor")
        text = text.replace(PARA_ANCHOR, PARA + PARA_ANCHOR, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("BT914 Holonet dictionary row patch applied/idempotent")

if __name__ == "__main__":
    main()
