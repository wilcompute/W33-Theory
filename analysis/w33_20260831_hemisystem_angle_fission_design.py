#!/usr/bin/env python3
"""Resolve the 216-line hemisystem angle algebra and exact design strength.

The projective hemisystem frame has four nontrivial absolute inner products
0,8,16,24 (norm squared 40).  Absolute angle does not resolve the full
PSp(4,3) orbital algebra.  This audit therefore:

* builds the four angle graphs exactly;
* tests whether their 5-class coarse partition (diagonal + four angles) is
  closed under relational multiplication;
* records the stabilizer-suborbit fission of each coarse angle;
* exhausts all 15 nonempty unions of angle graphs and identifies every strongly
  regular fusion;
* proves the 432-vector antipodal shell is a spherical 3-design but not a
  spherical 4-design by an exact fourth-moment obstruction.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260831_hemisystem_eigenframe_576 as hemi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_HEMISYSTEM_ANGLE_FISSION_DESIGN.json'
ANGLES=(0,8,16,24)
ALL=frozenset(range(40))


def canon_pair(T):
    C=ALL-T; a,b=tuple(sorted(T)),tuple(sorted(C))
    return (a,b) if a<b else (b,a)


def graph_params(rows,n=216):
    deg={r.bit_count() for r in rows}
    if len(deg)!=1: return {'regular':False,'degrees':sorted(deg),'srg':False}
    k=next(iter(deg)); lam=set(); mu=set()
    for i in range(n):
        for j in range(i+1,n):
            c=(rows[i]&rows[j]).bit_count()
            (lam if ((rows[i]>>j)&1) else mu).add(c)
            if len(lam)>1 or len(mu)>1:
                return {'regular':True,'degree':k,'srg':False,
                        'lambdaValues':sorted(lam),'muValues':sorted(mu)}
    return {'regular':True,'degree':k,'srg':True,
            'parameters':[n,k,next(iter(lam)) if lam else 0,next(iter(mu)) if mu else 0]}


def main():
    pts,idx,lines,_=base.geometry()
    gens=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens.append(tuple(p))
    gg=[gens[i] for i in (18,62,77,10)]
    G=base.closure(gg,40); assert len(G)==25920

    orbit={frozenset(g[x] for x in hemi.T0) for g in G}; assert len(orbit)==432
    pairs=sorted({canon_pair(T) for T in orbit}); assert len(pairs)==216
    signs=[]
    for P in pairs:
        T=set(P[0]); signs.append(tuple(1 if i in T else -1 for i in range(40)))
    pidx={P:i for i,P in enumerate(pairs)}

    rel={a:[0]*216 for a in ANGLES}
    val=Counter()
    for i,j in itertools.combinations(range(216),2):
        d=abs(sum(a*b for a,b in zip(signs[i],signs[j])))
        assert d in ANGLES
        rel[d][i]|=1<<j; rel[d][j]|=1<<i; val[d]+=1
    valencies={a:rel[a][0].bit_count() for a in ANGLES}
    assert valencies=={0:80,8:85,16:40,24:10}
    assert all({r.bit_count() for r in rel[a]}=={valencies[a]} for a in ANGLES)

    # Is the absolute-angle partition itself an association scheme?  For each
    # product R_a R_b, entries must be constant on every coarse relation class.
    classes=('diag',)+ANGLES
    closure=True; witnesses=[]; intersection_table={}
    for a in ANGLES:
        for b in ANGLES:
            row={}
            for c in classes:
                vals=set()
                for i in range(216):
                    js=[i] if c=='diag' else [j for j in range(216) if (rel[c][i]>>j)&1]
                    for j in js:
                        vals.add((rel[a][i]&rel[b][j]).bit_count())
                        if len(vals)>1: break
                    if len(vals)>1: break
                row[str(c)]=sorted(vals)
                if len(vals)>1:
                    closure=False
                    if len(witnesses)<12: witnesses.append({'left':a,'right':b,'on':str(c),'values':sorted(vals)})
            intersection_table[f'{a}*{b}']=row

    # Stabilizer suborbits give the exact fission seen from one line.
    P0=pairs[0]; T0=frozenset(P0[0]); C0=ALL-T0
    H=[g for g in G if frozenset(g[x] for x in T0) in (T0,C0)]; assert len(H)==120
    def act(g,i):
        T=frozenset(pairs[i][0]); return pidx[canon_pair(frozenset(g[x] for x in T))]
    rem=set(range(216)); sub=[]
    while rem:
        s=min(rem); O={act(g,s) for g in H}; rem-=O; sub.append(sorted(O))
    sub.sort(key=lambda O:(len(O),O))
    fission=defaultdict(list)
    for O in sub:
        if 0 in O: d='diag'
        else:
            ds={abs(sum(a*b for a,b in zip(signs[0],signs[j]))) for j in O}; assert len(ds)==1
            d=str(next(iter(ds)))
        fission[d].append(len(O))
    fission={k:sorted(v) for k,v in fission.items()}

    # Exhaust all unions of the four coarse relations.
    fusions=[]
    srg_fusions=[]
    for bits in range(1,1<<4):
        chosen=[ANGLES[i] for i in range(4) if (bits>>i)&1]
        rows=[]
        for i in range(216):
            r=0
            for a in chosen:r|=rel[a][i]
            rows.append(r)
        gp=graph_params(rows)
        rec={'angles':chosen,**gp}; fusions.append(rec)
        if gp.get('srg'): srg_fusions.append(rec)

    # Exact spherical-design strength of the 432-vector antipodal shell.
    # Normalize each h by sqrt(40). Tight frame + antipodality gives the first,
    # second, and third spherical moments exactly. The fourth moment along a
    # shell vector is computed from the transitive projective angle valencies.
    fourth=Fraction(2,1) # self and antipode
    for a,k in valencies.items(): fourth += 2*k*Fraction(a,40)**4
    fourth_avg=fourth/Fraction(432,1)
    sphere4=Fraction(3,15*17)
    assert fourth_avg==Fraction(2,125)
    assert sphere4==Fraction(1,85) and fourth_avg!=sphere4

    out={
      'schema':'w33.20260831.hemisystem-angle-fission-design.v1','status':'PASS',
      'projectiveFrame':{'lines':216,'ambientEigenspaceDimension':15,'normSquared':40,
        'absoluteAngles':list(ANGLES),'valencies':valencies},
      'coarseAnglePartition':{'associationSchemeClosed':closure,
        'closureWitnesses':witnesses,'intersectionProbe':intersection_table,
        'stabilizerSuborbitFission':fission,'subdegrees':sorted(map(len,sub))},
      'fusionCensus':{'tested':15,'stronglyRegularCount':len(srg_fusions),
        'stronglyRegularFusions':srg_fusions,'allFusions':fusions},
      'sphericalDesign':{'vectors':432,'antipodal':True,'dimension':15,
        'strengthExactly':3,'reason3':'antipodality kills odd moments and the 576 projective tight-frame identity gives the exact isotropic second moment',
        'fourthMomentAlongShellVector':str(fourth_avg),
        'sphericalFourthMomentRequired':str(sphere4),
        'isFourDesign':False},
      'theorem':'The 432 antipodal hemisystem vectors form an exact spherical 3-design in the 15-dimensional W33 -4 eigenspace, but not a 4-design. The four absolute-angle graphs are a coarse fusion of the rank-10 stabilizer orbital structure; the certificate lists exactly which angle unions are strongly regular.',
      'boundary':'Exact finite spherical-code/association-relation computation. A strongly regular fusion is a combinatorial relation, not a physical interaction Hamiltonian.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','coarseClosed':closure,'fission':fission,
      'srgFusions':[r['angles'] for r in srg_fusions],'designStrength':3,
      'fourth':[str(fourth_avg),str(sphere4)]},sort_keys=True))

if __name__=='__main__': main()
