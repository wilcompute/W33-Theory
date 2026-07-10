#!/usr/bin/env python3
"""Mirror-check and provenance certificate for the Lean odd-q rank module."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'formal/W33/OddQRank.lean'
TOOLCHAIN=ROOT/'formal/lean-toolchain'

def analyze():
    text=LEAN.read_text();q=sp.symbols('q')
    identities={
      'point':2*(q**2+1)+(q-1)*q*(q-1)-(q*(q**2+1)+2),
      'incidence':2*(q**2+q+1)+(q-1)*q*(q+1)-(q*(q+1)**2+2),
      'line':(q+1)+(q-1)*q-(q**2+1),
      'rank1':q**3+2*q**2+q-4+6-(q*(q+1)**2+2),
      'rank2':q**3+2*q**2+q-4+8-(q*(q**2+1)+2*q**2+4),
      'dimension':q*(q-1)**2+3*(q**3+2*q**2+q-4)+16-4*(q+1)*(q**2+1),
    }
    theorems=re.findall(r'\btheorem\s+([A-Za-z0-9_]+)',text)
    checks={
      'all_symbolic_identities_zero':all(sp.expand(v)==0 for v in identities.values()),
      'no_sorry': 'sorry' not in text,
      'no_axiom': not re.search(r'^\s*axiom\b',text,re.M),
      'expected_theorem_count':len(theorems)==11,
      'mathlib_import':text.startswith('import Mathlib.Tactic'),
      'toolchain_pinned':TOOLCHAIN.read_text().strip()=='leanprover/lean4:v4.32.0-rc1',
    }
    return {
      'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'lean_file':str(LEAN.relative_to(ROOT)),'toolchain':TOOLCHAIN.read_text().strip(),
      'theorems':theorems,'sha256':hashlib.sha256(text.encode()).hexdigest(),
      'kernel_check':{'ran':False,'reason':'Lean/lake are not installed in the execution container and outbound package installation is unavailable.'},
      'scope':'The Lean module formalizes the arithmetic assembly, odd-q parity/integrality, and Jordan rank ladder. The finite-geometry Fourier block decomposition remains an explicit hypothesis supplied by the executable mathematical certificate.'
    }
def main():
    out=analyze();print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
