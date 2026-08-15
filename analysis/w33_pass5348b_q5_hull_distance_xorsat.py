#!/usr/bin/env python3
"""Pass5348b: symmetry-broken exact distance test for the q5 footprint hull.

Pass5209: the footprint hull H has dimension64, is the image of the even point
module, is doubly even, and has explicit weight40 words (collinear point-row
pairs). Pass5243: every Hoffman-13 shortened word lies in H. Since the full
footprint code has d=25, the only possible nonzero hull weights below40 are
28,32,36.

The PSp4(5) action is transitive on the 325 P-component coordinates and preserves
H. Therefore any nonzero hull word is equivalent to one containing coordinate0.
We construct a 64-row generator for H from F[p]+F[0], force output coordinate0
=1, and ask exact SAT for weight<=36. UNSAT proves d(H)=40 and hence immediately
closes every Hoffman-13 shortening at d=40.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5348B_Q5_HULL_DISTANCE_XORSAT.json'

def basis(rows):
    piv={};B=[]
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(x);break
    return B

def build_hull():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    F=[]
    for p in range(156):
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        F.append(z)
    assert {x.bit_count() for x in F}=={25}
    H=basis([F[0]^F[p] for p in range(1,156)]);assert len(H)==64
    assert all(x.bit_count()%4==0 for x in H)
    return H

def xor_gate(cnf,a,b,c):cnf.extend([[a,b,-c],[-a,-b,-c],[a,-b,c],[-a,b,c]])
def encode_xor(cnf,pool,ins,out):
    if not ins:cnf.append([-out]);return
    if len(ins)==1:
        a=ins[0];cnf.extend([[-a,out],[a,-out]]);return
    cur=ins[0]
    for k,b in enumerate(ins[1:]):
        t=out if k==len(ins)-2 else pool.id(('xor',out,k));xor_gate(cnf,cur,b,t);cur=t

def main():
    from pysat.formula import CNF,IDPool
    from pysat.card import CardEnc,EncType
    from pysat.solvers import Solver
    B=build_hull();r=64;n=325;u=list(range(1,r+1));pool=IDPool(start_from=r+1);cnf=CNF();x=[]
    for j in range(n):
        out=pool.id(('x',j));x.append(out);encode_xor(cnf,pool,[u[i] for i,row in enumerate(B) if row>>j&1],out)
    cnf.append([x[0]])
    cnf.extend(CardEnc.atmost(lits=x,bound=36,vpool=pool,encoding=EncType.seqcounter).clauses)
    solver=used=None
    for name in ('cadical195','cadical153','g4','m22'):
        try:solver=Solver(name=name,bootstrap_with=cnf.clauses);used=name;break
        except Exception:pass
    if solver is None:raise RuntimeError('no PySAT backend')
    sat=solver.solve();model=solver.get_model() if sat else None;solver.delete()
    out={'pass':'5348b','solver':used,'code':'q5 footprint hull [325,64,d_H]_2','query':'support contains coordinate0 and weight<=36','sat':bool(sat)}
    if sat:
        M={v for v in model if v>0};z=0;msg=[]
        for i,v in enumerate(u):
            if v in M:z^=B[i];msg.append(i)
        wt=z.bit_count();assert 0<wt<=36 and z&1 and wt%4==0
        out.update(status='COUNTEREXAMPLE_Q5_HULL_DISTANCE_BELOW40',witness_weight=wt,message_support=msg,
                   coordinate_support=[j for j in range(n) if z>>j&1],
                   conclusion=f'Hull has a verified weight-{wt} word; Hoffman d=40 cannot be inferred from hull containment.')
    else:
        out.update(status='THEOREM_Q5_FOOTPRINT_HULL_325_64_40',minimum_distance=40,
                   conclusion='By coordinate transitivity, UNSAT with coordinate0 fixed excludes every nonzero hull word of weight<=36. Known collinear point-row pairs attain40.',
                   hoffman_consequence='Every Hoffman-13 shortened code lies in this hull and has weight40 witnesses, hence [312,52,40]_2.')
    out['boundary']='The transitivity reduction uses the PSp4(5) coordinate action on all 325 P-components; the Hoffman consequence additionally uses Pass5243 hull containment.'
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
