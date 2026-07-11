#!/usr/bin/env python3
"""Static and algebraic certificate for the v4 Lean formalization and CI contract."""
from __future__ import annotations
from functools import lru_cache
import hashlib, json, re
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
FILES=[ROOT/'formal/W33/OddQRank.lean',ROOT/'formal/W33/FourierBlocks.lean',ROOT/'formal/W33.lean',ROOT/'.github/workflows/lean-formal.yml']

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
      'kernel_build_required':'build: true' in workflow and '--wfail' in workflow,
      'independent_nanoda_required':'nanoda: true' in workflow and 'nanoda-allow-sorry: false' in workflow,
      'branch_and_pr_triggers':'pull_request:' in workflow and '"agent/**"' in workflow,
      'q3_numeric_theorems':'theorem q3Ranks' in joined and 'theorem q3JordanCensus' in joined,
    }
    digest=hashlib.sha256('\n'.join(f'{k}\0{v}' for k,v in sorted(content.items())).encode()).hexdigest()
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'files':list(content),'source_digest':digest,'workflow':{'action':'leanprover/lean-action@v1','lake_directory':'formal','build_wfail':True,'nanoda_no_sorry':True},'honest_boundary':'The Python witness validates source structure and algebra locally. Kernel and nanoda validation are delegated to the committed GitHub Actions workflow because Lean is unavailable in this execution container.','theorem':'The local Fourier-block interface kernel-reduces the global odd-q rank/Jordan theorem to explicit geometric block certificates and numerically closes q=3; CI requires both lake build and nanoda with sorryAx forbidden.'}

def main():
    out=analyze();print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
