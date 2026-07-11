#!/usr/bin/env python3
"""Static and algebraic certificate for the v4 Lean formalization and CI contract."""
from __future__ import annotations
from functools import lru_cache
import hashlib, json, re
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
FILES=[ROOT/'formal/W33/OddQRank.lean',ROOT/'formal/W33/FourierBlocks.lean',ROOT/'formal/W33/HeisenbergQ3.lean',ROOT/'formal/W33.lean',ROOT/'.github/workflows/lean-formal.yml']
OUT=ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_formal.json'

@lru_cache(maxsize=1)
def analyze():
    content={str(p.relative_to(ROOT)):p.read_text(encoding='utf-8') for p in FILES}
    q=sp.symbols('q')
    identities={
      'point':sp.expand(2*(q**2+1)+(q-1)*q*(q-1)-(q*(q**2+1)+2)),
      'incidence':sp.expand(2*(q**2+q+1)+(q-1)*q*(q+1)-(q*(q+1)**2+2)),
      'line':sp.expand((q+1)+(q-1)*q-(q**2+1)),
      'jordan_rank1':sp.expand((q**3+2*q**2+q-4)+6-(q*(q+1)**2+2)),
      'jordan_dimension':sp.expand(q*(q-1)**2+3*(q**3+2*q**2+q-4)+16-4*(q+1)*(q**2+1)),
    }
    joined='\n'.join(content.values())
    workflow=content['.github/workflows/lean-formal.yml']
    checks={
      'all_symbolic_identities_zero':all(v==0 for v in identities.values()),
      'no_sorry':not re.search(r'(?m)^\s*sorry\b', '\n'.join(v for k,v in content.items() if k.endswith('.lean')), re.I),
      'no_admit':not re.search(r'(?m)^\s*admit\b', '\n'.join(v for k,v in content.items() if k.endswith('.lean')), re.I),
      'imports_root_module':'import W33.FourierBlocks' in content['formal/W33.lean'],
      'lean_action_v1':'leanprover/lean-action@v1' in workflow,
      'kernel_build_required':'lake build --wfail' in workflow or ('build: true' in workflow and '--wfail' in workflow),
      'independent_leanchecker_required':'lake env leanchecker' in workflow,
      'placeholder_rejection_required':"grep -R -n -E" in workflow and '(sorry|admit)' in workflow,
      'branch_and_pr_triggers':'pull_request:' in workflow and '"agent/**"' in workflow,
      'q3_arithmetic_theorems':(
          'theorem q3ArithmeticValues' in joined and 'theorem q3JordanArithmetic' in joined
          and '= 22' in content['formal/W33/FourierBlocks.lean']
          and '22*3 + 6 = 80' in content['formal/W33/FourierBlocks.lean']
      ),
      'no_tautological_block_certificate_structures':(
          'structure TrivialBlock' not in joined
          and 'structure NontrivialBlock' not in joined
          and 'OddQFourierCertificate' not in joined
      ),
      'formal_scope_boundaries_present':(
          'finite-field Fourier transform' in content['formal/W33/FourierBlocks.lean']
          and 'No incidence matrix' in content['formal/W33/OddQRank.lean']
          and 'not a formal proof of the W(3,3) Levi rank theorem' in content['formal/W33/HeisenbergQ3.lean']
      ),
    }
    digest=hashlib.sha256('\n'.join(f'{k}\0{v}' for k,v in sorted(content.items())).encode()).hexdigest()
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'files':list(content),'source_digest':digest,'workflow':{'action':'leanprover/lean-action@v1','lake_directory':'formal','build_wfail':True,'independent_checker':'leanchecker','placeholders_forbidden':True},'honest_boundary':'The Python witness validates source structure and arithmetic locally. Lean kernel and leanchecker validation run in the committed GitHub Actions workflow because Lean is unavailable in this execution container. Neither path supplies the missing finite-field Fourier/incidence construction.','theorem':'Lean checks exact q=3 matrix-space cardinalities plus the arithmetic/divisibility identities used by the proposed odd-q rank and Jordan formulas. It does not prove the geometric incidence-rank theorem; CI requires lake build, placeholder rejection, and a second Lean-kernel replay via leanchecker.'}

def main():
    out=analyze();text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    OUT.write_text(text,encoding='utf-8');print(text,end='')
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
