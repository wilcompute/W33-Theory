#!/usr/bin/env python3
"""Pass 4801 — exact SAT decision of rho(H10)=14 or 15.

Pass4794 proved 14 <= rho(H10) <= 15 and supplied a distance-14 coset.
A distance-15 coset exists iff it has a leader x of weight exactly 15.  For a
codeword c of weight w,

    d(x,c) = 15 + w - 2|supp(x) cap supp(c)| >= 15

is exactly the cardinality constraint |x cap c| <= w/2.  Thus the only remaining
question is feasibility of a 40-variable 0/1 system: wt(x)=15 and one at-most
constraint for each H10 codeword.

The 40 coordinates are transitive under PSp(4,3), so any weight-15 solution can
be moved to one containing coordinate 0.  The weight-12 codeword N(0) then has
intersection a in {1,...,6}; we solve all six cases independently with PySAT.
All codewords are reconstructed from the frozen 10-row generator below and the
known enumerator is rechecked before SAT.  If every case is UNSAT, rho=14; a SAT
case is independently distance-checked and proves rho=15.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4801_H10_COVERING_RADIUS_SAT.json'
G=[
[0,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0],
[1,1,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0],
[1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1],
[1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
[1,0,0,1,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0],
[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0],
[1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0],
[0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
[0,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,0,1,1,0,0,1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0],
]

def mask(row):return sum((int(b)&1)<<i for i,b in enumerate(row))

def span():
    B=[mask(r) for r in G];C=[]
    for a in range(1<<10):
        x=0
        for i,b in enumerate(B):
            if (a>>i)&1:x^=b
        C.append(x)
    assert len(set(C))==1024
    wd=Counter(x.bit_count() for x in C)
    assert wd==Counter({0:1,12:40,16:135,20:672,24:135,28:40,40:1})
    return C,wd

def solve_case(C,a):
    pool=IDPool(start_from=41);cnf=CNF();X=list(range(1,41))
    cnf.extend(CardEnc.equals(X,bound=15,vpool=pool,encoding=EncType.seqcounter).clauses)
    cnf.append([1]) # coordinate 0 is selected
    N0=[i+1 for i,b in enumerate(G[0]) if b]
    cnf.extend(CardEnc.equals(N0,bound=a,vpool=pool,encoding=EncType.seqcounter).clauses)
    # one representative from each complement pair is enough only if both upper
    # and lower bounds are added. Simpler and safer: add all 1022 nontrivial,
    # non-all-one codeword upper bounds.
    for c in C:
        w=c.bit_count()
        if w in (0,40):continue
        supp=[i+1 for i in range(40) if (c>>i)&1]
        cnf.extend(CardEnc.atmost(supp,bound=w//2,vpool=pool,encoding=EncType.seqcounter).clauses)
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as S:
        sat=S.solve();model=S.get_model() if sat else None
        stats=S.accum_stats()
    if not sat:return {'a':a,'sat':False,'solver_stats':stats}
    chosen=[i for i in range(40) if model[i]>0]  # vars 1..40 occupy model positions 0..39
    x=sum(1<<i for i in chosen)
    d=min((x^c).bit_count() for c in C)
    assert len(chosen)==15 and d>=15
    return {'a':a,'sat':True,'chosen_coordinates':chosen,'verified_coset_minimum':d,'solver_stats':stats}

def main()->int:
    C,wd=span();cases=[]
    for a in range(1,7):
        r=solve_case(C,a);cases.append(r)
        if r['sat']:break
    sat=next((r for r in cases if r['sat']),None)
    if sat:
        rho=15;decision='SAT';theorem='A weight-15 coset leader exists. Combined with Pass4794 rho<=15, the exact covering radius is rho(H10)=15.'
    else:
        assert len(cases)==6
        rho=14;decision='UNSAT';theorem='All six symmetry-complete weight-15 leader cases are UNSAT. Combined with the explicit distance-14 witness, the exact covering radius is rho(H10)=14.'
    out={'pass':4801,'code':'H10=[40,10,12]','weight_enumerator':dict(sorted(wd.items())),
      'previous_certified_bracket':[14,15],'symmetry_break':'x_0=1 and |X cap N(0)|=a, a=1..6',
      'cases':cases,'decision':decision,'exact_covering_radius':rho,'theorem':theorem,
      'boundary':'Exact finite SAT certificate. Coordinate transitivity is the only group-theoretic symmetry used; the solver result is independently checked against all 1024 codewords if SAT.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
