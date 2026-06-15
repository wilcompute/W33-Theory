#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

out = {
  "theorem": "BT1047 generation-fiber symmetry constraint",
  "matrix_form": "Y = alpha I_3 + beta (J_3 - I_3)",
  "symmetry": "S3 invariant 3 by 3 form",
  "eigenvalues": {"singlet": "alpha + 2 beta", "doublet": "alpha - beta"},
  "traces": {"TrY2": "3 alpha^2 + 6 beta^2", "TrY4": "(alpha+2 beta)^4 + 2 (alpha-beta)^4"},
  "constraint": "sector amplitudes a0,a4,a10,a16 become functions of the singlet and doublet invariants",
  "status": "symbolic constraint; no numerical parameter insertion"
}
Path("data").mkdir(exist_ok=True)
Path("data/bt1047_generation_fiber_symmetry.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
