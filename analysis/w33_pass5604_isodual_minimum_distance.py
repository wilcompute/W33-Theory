#!/usr/bin/env python3
"""Pass5604: exact all-q minimum distance of the determinant-coset isodual code.

Pass5601 proved C_- = C_+^perp, where C_+ is the binary span of PSL2(q)
projectivity graphs on P1(q)xP1(q), and C_- is the opposite PGL2 determinant
coset span.  Every generator has weight q+1.

Lower bound: fix c in a nonzero support S of C_+.  Opposite-coset projectivity
graphs through c number r=q(q-1)/2.  Any second compatible cell lies with c
on exactly lambda=(q-1)/2 such graphs; an incompatible cell lies on none.
If |S|=s<=q, at most (s-1)lambda graphs through c can hit another support
cell, so at least

  r-(s-1)lambda=(q-1)(q-s+1)/2 > 0

opposite graphs meet S exactly once.  That contradicts S orthogonal to every
C_- generator. Hence d(C_+)>=q+1, while a projectivity row gives equality.
The same holds for C_- by isoduality.

The optional MILP replay independently certifies q=7 and q=9. Coordinate
transitivity permits fixing one support bit to 1, eliminating the zero word.
"""
from __future__ import annotations
import argparse, importlib, json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
prev=importlib.import_module('w33_pass5595_5602_projectivity_closure_toe_probes')
OUT=ROOT/'data/PART_W33_PASS5604_ISODUAL_MINIMUM_DISTANCE.json'


def theory(q:int)->dict:
    assert q>=3 and q%2==1
    r=q*(q-1)//2
    lam=(q-1)//2
    return {
      'q':q,
      'length':(q+1)**2,
      'dimension':(q+1)**2//2,
      'row_weight':q+1,
      'opposite_graphs_through_cell':r,
      'opposite_graphs_through_compatible_pair':lam,
      'distance':q+1,
      'lower_bound_at_s_eq_q':r-(q-1)*lam,
    }


def independent_rows(bitrows:list[int], n:int)->np.ndarray:
    _,bd=prev.rank_bits(bitrows)
    vals=list(bd.values())
    return np.array([[(x>>j)&1 for j in range(n)] for x in vals],dtype=np.int8)


def milp_distance(dual_perms, q:int)->dict:
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import csc_matrix, lil_matrix
    n=(q+1)**2
    dual_bits=[prev.row_bits_from_perm(g) for g in dual_perms]
    H=independent_rows(dual_bits,n)
    r=H.shape[0]
    # H x = 2 y, x binary.  Fix x_0=1 by coordinate transitivity.
    A=lil_matrix((r+1,n+r),dtype=float)
    A[:r,:n]=H
    for i in range(r): A[i,n+i]=-2.0
    A[r,0]=1.0
    lb=np.zeros(r+1); ub=np.zeros(r+1); lb[-1]=ub[-1]=1.0
    c=np.r_[np.ones(n),np.zeros(r)]
    lo=np.zeros(n+r); hi=np.r_[np.ones(n),np.full(r,n//2)]
    res=milp(c,integrality=np.ones(n+r,dtype=int),bounds=Bounds(lo,hi),
             constraints=LinearConstraint(csc_matrix(A),lb,ub),
             options={'time_limit':120})
    if not res.success:
        raise RuntimeError(f'MILP did not prove optimality for q={q}: {res.message}')
    d=int(round(float(res.fun)))
    assert d==q+1
    return {'q':q,'MILP_optimal':True,'minimum_weight':d,'dual_check_rank':int(r),'solver_message':res.message}


def prime_cosets(q:int):
    PGL,G=prev.pgl_psl_perms_prime(q); Gs=set(G)
    h=next(x for x in PGL if x not in Gs)
    opp=[prev.compose(h,g) for g in G]
    return G,opp


def extension_cosets(F):
    PGL,G=prev.pgl_psl_perms_F(F); Gs=set(G)
    h=next(x for x in PGL if x not in Gs)
    opp=[prev.compose(h,g) for g in G]
    return G,opp


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--skip-milp',action='store_true')
    args=ap.parse_args()
    anchors=[]
    if not args.skip_milp:
        _,opp7=prime_cosets(7); anchors.append(milp_distance(opp7,7))
        _,opp9=extension_cosets(prev.GFp2(3,2)); anchors.append(milp_distance(opp9,9))
    out={
      'status':'THEOREM_ALLODD_MINIMUM_DISTANCE',
      'theorem':'For every odd prime power q, d(C_+)=d(C_-)=q+1.',
      'parameters':'[(q+1)^2,(q+1)^2/2,q+1]_2 for both determinant sectors',
      'proof':[
        'C_-=C_+^perp (Pass5601).',
        'Through one cell there are r=q(q-1)/2 opposite-coset projectivity graphs.',
        'Through a compatible pair there are lambda=(q-1)/2; through an incompatible pair there are zero.',
        'If a nonzero support S has s<=q and c in S, at least r-(s-1)lambda=(q-1)(q-s+1)/2>0 dual generators meet S exactly once, contradicting orthogonality.',
        'A projectivity generator has weight q+1, so the lower bound is sharp.',
      ],
      'sample_formulas':[theory(q) for q in (3,5,7,9,11,13,25)],
      'independent_exact_MILP_anchors':anchors,
      'equality_note':'At weight q+1 the union-bound equality forces all support cells to have distinct first and second coordinates, hence every minimum support is a permutation graph. Classifying which permutation graphs occur as codewords remains separate.',
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
