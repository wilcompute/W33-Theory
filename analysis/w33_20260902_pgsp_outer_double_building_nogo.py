#!/usr/bin/env python3
"""Global PGSp outer involution cannot exchange the 64/81 building Steinbergs.

The common-spread analysis suggests a local S6 outer twist between the two
six-state fibres of the circuit-216 and hemisystem-216 actions.  This script
asks whether that local twist is the restriction of the actual global
PGSp(4,3)/PSp(4,3) outer automorphism.

It cannot exchange St_81 and St_64 on abstract grounds: automorphisms preserve
irreducible character degree.  Here we verify the stronger carrier-level fact
against the explicit multiplier-minus-one similitude used elsewhere in the
repo,

    s = diag(1,2,1,2) mod 3.

Conjugation by s normalizes the exact PSp action on 40 projective points.  We
materialize the induced involution alpha on all 25,920 group elements, compute
both building-homology characters elementwise, and compute the two degree-216
permutation characters.  The certificate records whether each character is
fixed or exchanged under alpha and its exact 64/81 multiplicities.

If the local spread-S6 audit proves two nonconjugate S5 fibre types, combining
that result with this certificate means the S6 outer twist is a local
nonextendable fibre phenomenon, not the global PGSp outer automorphism.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260901_packet48_bt796_crossid as shell

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_20260902_PGSP_OUTER_DOUBLE_BUILDING_NOGO.json'
T0 = frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL = frozenset(range(40))


def norm(v):
    i = next(k for k, x in enumerate(v) if x % 3)
    z = pow(v[i] % 3, -1, 3)
    return tuple((z * x) % 3 for x in v)


def comp(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def ip(a, b):
    z = sum(x*y for x, y in zip(a, b))
    assert z % len(a) == 0
    return z // len(a)


def canon_pair(T):
    C = ALL - T
    a, b = tuple(sorted(T)), tuple(sorted(C))
    return (a, b) if a < b else (b, a)


def main():
    D = shell.build()
    pts, wlines, supports, charts, G = D['pts'], D['wlines'], D['supports'], D['charts'], D['G']
    assert (len(pts),len(wlines),len(supports),len(charts),len(G)) == (40,40,45,27,25920)
    idx = {v:i for i,v in enumerate(pts)}

    # Explicit multiplier -1 symplectic similitude s=diag(1,2,1,2).
    def outer_vec(v):
        return norm((v[0], 2*v[1], v[2], 2*v[3]))
    outer = tuple(idx[outer_vec(v)] for v in pts)
    assert comp(outer, outer) == tuple(range(40))

    gindex = {p40:i for i,(p40,_p45,_p27) in enumerate(G)}
    assert outer not in gindex
    alpha = []
    for p40,_p45,_p27 in G:
        c = comp(outer, comp(p40, outer))
        assert c in gindex
        alpha.append(gindex[c])
    assert len(set(alpha)) == 25920
    assert all(alpha[alpha[i]] == i for i in range(25920))
    outer_nontrivial = any(alpha[i] != i for i in range(25920))
    assert outer_nontrivial

    li = {frozenset(L):i for i,L in enumerate(wlines)}
    def line_perm(p40):
        return tuple(li[frozenset(p40[x] for x in L)] for L in wlines)

    wch = [(p,ell) for ell,L in enumerate(wlines) for p in L]
    fch = [(packet,c) for c,C in enumerate(charts) for packet in C]
    assert len(wch)==160 and len(fch)==135

    # Circuit 216 and hemisystem 216 carriers.
    _pts2,_idx2,_lines2,N = base.geometry()
    supports2,masks = base.supports_from_N(N)
    assert supports2 == supports
    circuits=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C:w ^= masks[i]
        if w==0:circuits.append(tuple(C))
    assert len(circuits)==216

    orbit432={frozenset(p40[x] for x in T0) for p40,_p45,_p27 in G}
    assert len(orbit432)==432
    hpairs=sorted({canon_pair(T) for T in orbit432})
    assert len(hpairs)==216

    chi81=[];chi64=[];pcirc=[];phemi=[]
    for p40,p45,p27 in G:
        lp=line_perm(p40)
        fp=sum(p40[i]==i for i in range(40))
        fl=sum(lp[i]==i for i in range(40))
        fc=sum(p40[p]==p and lp[ell]==ell for p,ell in wch)
        chi81.append(fc-fp-fl+1)

        f45=sum(p45[i]==i for i in range(45))
        f27=sum(p27[i]==i for i in range(27))
        f135=sum(p45[p]==p and p27[c]==c for p,c in fch)
        chi64.append(f135-f45-f27+1)

        pcirc.append(sum(tuple(sorted(p45[x] for x in C))==C for C in circuits))
        fixed_h=0
        for P in hpairs:
            T=frozenset(P[0])
            fixed_h += canon_pair(frozenset(p40[x] for x in T)) == P
        phemi.append(fixed_h)

    assert ip(chi81,chi81)==1 and ip(chi64,chi64)==1 and ip(chi81,chi64)==0
    assert ip(pcirc,chi81)==1 and ip(pcirc,chi64)==0
    assert ip(phemi,chi81)==0 and ip(phemi,chi64)==1

    twist = lambda ch: [ch[alpha[i]] for i in range(25920)]
    t81,t64,tc,th = map(twist,(chi81,chi64,pcirc,phemi))
    char81_fixed=(t81==chi81);char64_fixed=(t64==chi64)
    circuit_fixed=(tc==pcirc);hemi_fixed=(th==phemi)
    circuit_to_hemi=(tc==phemi);hemi_to_circuit=(th==pcirc)

    # Degree alone already forbids 64<->81. The elementwise test records the
    # stronger behavior of this concrete PGSp outer automorphism.
    assert not circuit_to_hemi and not hemi_to_circuit
    assert ip(tc,chi81)==1 and ip(tc,chi64)==0
    assert ip(th,chi81)==0 and ip(th,chi64)==1

    out={
      'schema':'w33.20260902.pgsp-outer-double-building-nogo.v1','status':'PASS',
      'groupOrder':25920,
      'outerSimilitude':{'matrixMod3':'diag(1,2,1,2)','multiplier':-1,'involutionOnGroup':True,'nontrivial':outer_nontrivial},
      'buildingCharacters':{
        'St81':{'degree':81,'norm':1,'fixedByExplicitOuter':char81_fixed},
        'St64':{'degree':64,'norm':1,'fixedByExplicitOuter':char64_fixed},
        'crossInnerProduct':0,
        'degreePreservationNoGo':'Any automorphism preserves character degree, so no automorphism of PSp4(3) can exchange degree 81 with degree 64.'},
      'selectors':{
        'circuit216':{'multiplicity81':1,'multiplicity64':0,'fixedByExplicitOuter':circuit_fixed},
        'hemisystem216':{'multiplicity81':0,'multiplicity64':1,'fixedByExplicitOuter':hemi_fixed},
        'outerTwistedCircuitEqualsHemisystem':circuit_to_hemi,
        'outerTwistedHemisystemEqualsCircuit':hemi_to_circuit,
        'twistedCircuitMultiplicities':[ip(tc,chi64),ip(tc,chi81)],
        'twistedHemisystemMultiplicities':[ip(th,chi64),ip(th,chi81)],
      },
      'theorem':(
        'The actual PGSp(4,3)/PSp(4,3) outer involution does not exchange the two building Steinbergs or the circuit/hemisystem selector characters. Character degree already forbids St81<->St64 under any automorphism; the explicit multiplier-minus-one similitude is checked elementwise on all 25,920 group elements and preserves the 64/81 selector pattern under twisting.'),
      'consequence':(
        'If the common-spread S6 fibres are related by the exceptional outer automorphism of S6, that fibre twist does not extend to the global PGSp outer automorphism of PSp4(3). It is a local nonextendable outer twist inside the spread stabilizer.'),
      'boundary':(
        'This is finite character/permutation-group structure. Nonextendability of this local S6 twist does not exclude other correspondences between the two 216 carriers that are not induced by group automorphisms.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','fixed':[char81_fixed,char64_fixed,circuit_fixed,hemi_fixed],
                      'swap':[circuit_to_hemi,hemi_to_circuit],
                      'twistedMults':[out['selectors']['twistedCircuitMultiplicities'],out['selectors']['twistedHemisystemMultiplicities']]},sort_keys=True))


if __name__=='__main__':main()
