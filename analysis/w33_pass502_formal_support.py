#!/usr/bin/env python3
"""Pass 502: executable support for the two Lean formalizations."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass502_formal_support.json'

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A):return [list(x) for x in zip(*A)]
def incidence(p,nbase):
    return [[1 if b==i else 0 for s in range(p) for b in range(nbase)] for i in range(nbase)]
def gram_check(p,nbase):
    A=incidence(p,nbase);G=matmul(A,transpose(A))
    target=[[p if i==j else 0 for j in range(nbase)] for i in range(nbase)]
    return {'p':p,'base_points':nbase,'columns':p*nbase,'gram_ok':G==target,'trace':sum(G[i][i] for i in range(nbase)),'expected_trace':p*nbase}
def paired_product(values):
    half=1;full=1
    for x in values:half*=x;full*=x*x
    return {'values':values,'half_product':half,'full_product':full,'square':half*half,'identity':full==half*half}
def main_payload():
    grams=[gram_check(3,4),gram_check(3,12),gram_check(5,6),gram_check(7,8)]
    pairs=[paired_product([2,3,5]),paired_product([-7,11,13]),paired_product([3**4,3**6,5])]
    lean1=ROOT/'formal'/'W33'/'Pass502HjelmslevGram.lean';lean2=ROOT/'formal'/'W33'/'Pass502RelativeNormSquare.lean'
    sources=[lean1.read_text(),lean2.read_text()]
    checks={
      'all_gram_examples':all(x['gram_ok'] and x['trace']==x['expected_trace'] for x in grams),
      'all_paired_products_square':all(x['identity'] for x in pairs),
      'lean_files_present':lean1.exists() and lean2.exists(),
      'no_sorry':all('sorry' not in s.lower() for s in sources),
      'hjelmslev_theorem_named':'theorem uniformCover_gram' in sources[0],
      'relative_norm_theorem_named':'theorem pairedStarProduct_eq_sq' in sources[1],
    }
    return {'schema':'w33.pass502.formal_support.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'formal_files':['formal/W33/Pass502HjelmslevGram.lean','formal/W33/Pass502RelativeNormSquare.lean'],
      'gram_examples':grams,'paired_product_examples':pairs,
      'boundary':'Python certifies finite instances and source custody. The GitHub Lean workflow is the authoritative compile check.',
      'checks':checks}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();pl=main_payload();text=json.dumps(pl,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 502 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':pl['status'],'checks':sum(pl['checks'].values()),'total':len(pl['checks'])},indent=2));return 0 if pl['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
