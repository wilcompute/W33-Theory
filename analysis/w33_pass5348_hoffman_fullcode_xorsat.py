#!/usr/bin/env python3
"""Pass5348: attack the FULL Hoffman-shortened [312,52,d] code by XOR-SAT.

Earlier passes proved d in {28,32,36,40} and closed every <=3-cell span at 40.
This pass does not stop at the four-cell layer: it constructs a 52-element basis
for the entire shortened code from the 13 ten-dimensional Hoffman cell codes and
asks a SAT solver whether a nonzero codeword of weight <=39 exists.

The model is exact. Message bits generate each output coordinate by XOR gates;
a cardinality constraint bounds the Hamming weight, and a single clause excludes
the zero message. UNSAT therefore proves d>=40. Since every cell already contains
weight-40 words, UNSAT closes d=40. SAT returns and verifies an explicit witness.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5348_HOFFMAN_FULLCODE_XORSAT.json'
COVER=(6,30,73,111,128,140,157,189,193,226,254,277,320)

def basis(rows):
    piv={};B=[]
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(x);break
    return B

def build_code():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    F=[]
    for p in range(156):
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        F.append(z)
    cells=[]
    for c in COVER:
        P=sorted(blocks[c]);a=F[P[0]]
        C=basis([a^F[p] for p in P[1:]])
        assert len(C)==10
        cells.append(C)
    B=basis(sum(cells,[]));assert len(B)==52
    coords=[j for j in range(325) if j not in set(COVER)];assert len(coords)==312
    assert all(((x>>c)&1)==0 for x in B for c in COVER)
    return B,coords

def xor_gate(cnf,a,b,c):
    # c <-> a XOR b
    cnf.extend([[a,b,-c],[-a,-b,-c],[a,-b,c],[-a,b,c]])

def encode_xor(cnf,vpool,inputs,out):
    if not inputs:
        cnf.append([-out]);return
    if len(inputs)==1:
        a=inputs[0];cnf.extend([[-a,out],[a,-out]]);return
    cur=inputs[0]
    for k,b in enumerate(inputs[1:]):
        last=(k==len(inputs)-2)
        t=out if last else vpool.id(('xor',out,k))
        xor_gate(cnf,cur,b,t);cur=t

def main():
    from pysat.formula import CNF,IDPool
    from pysat.card import CardEnc,EncType
    from pysat.solvers import Solver
    B,coords=build_code();r=len(B)
    pool=IDPool(start_from=r+1);u=list(range(1,r+1));x=[];cnf=CNF()
    for j in coords:
        out=pool.id(('x',j));x.append(out)
        ins=[u[i] for i,row in enumerate(B) if (row>>j)&1]
        encode_xor(cnf,pool,ins,out)
    cnf.append(u[:]) # nonzero message
    cnf.extend(CardEnc.atmost(lits=x,bound=39,vpool=pool,encoding=EncType.seqcounter).clauses)
    names=['cadical195','cadical153','g4','m22']
    solver=None;used=None
    for name in names:
        try:
            solver=Solver(name=name,bootstrap_with=cnf.clauses);used=name;break
        except Exception:
            pass
    if solver is None:raise RuntimeError('no PySAT backend available')
    sat=solver.solve();model=solver.get_model() if sat else None;solver.delete()
    rec={'pass':5348,'solver':used,'rank':52,'length':312,'query':'exists nonzero codeword of weight <=39','sat':bool(sat)}
    if sat:
        M=set(v for v in model if v>0);msg=[i for i,v in enumerate(u) if v in M]
        z=0
        for i in msg:z^=B[i]
        wt=sum((z>>j)&1 for j in coords)
        assert 0<wt<=39
        rec.update(status='COUNTEREXAMPLE_HOFFMAN_DISTANCE_BELOW40',witness_weight=wt,message_support=msg,
                   coordinate_support=[j for j in coords if (z>>j)&1],
                   conclusion=f'shortened distance is at most {wt}; previous lower bound must be refined against this witness.')
    else:
        rec.update(status='THEOREM_HOFFMAN_SHORTENED_CODE_312_52_40',minimum_distance=40,
                   code='[312,52,40]_2',
                   conclusion='Exact XOR-SAT proves no nonzero word has weight <=39; known cell words attain weight40.')
    rec['certificate']='CNF encodes an injective 52-bit generator, 312 coordinate XOR equations, nonzero message, and Hamming weight <=39.'
    OUT.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
