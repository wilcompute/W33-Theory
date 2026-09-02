#!/usr/bin/env python3
"""Construct both exceptional Steinberg modules as building homology.

The exceptional isomorphism PSp4(3) ~= U4(2) gives the same abstract group two
rank-two building actions visible in this repo:

  * W(3,3)=GQ(3,3): 40 points, 40 lines, 160 chambers;
  * GQ(4,2) (dual GQ(2,4)): 45 packet/octets, 27 factor charts, 135 chambers.

For a connected type-preserving Levi graph X and any automorphism g,

    chi_H1(g) = chi_C1(g) - chi_C0(g) + chi_H0(g)
              = #fixed chambers - #fixed vertices + 1.

Hence the two first-homology dimensions are

    160 - 80 + 1 = 81,
    135 - 72 + 1 = 64.

Solomon--Tits identifies top building homology with the Steinberg module.  The
finite computations below are independent of that naming: over every element
of the exact order-25920 PSp action we compute both homology characters, prove
that each has character norm one and that they are orthogonal, and then recover
multiplicities in the circuit-216, hemisystem-216, obstruction-1080 and
BT796/packet48-2160 permutation carriers by exact character inner products.

External interpretation only:
  https://encyclopediaofmath.org/wiki/Steinberg_module
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260901_packet48_bt796_crossid as shell

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260901_DOUBLE_BUILDING_STEINBERG_HOMOLOGY.json"
T0 = frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL = frozenset(range(40))


def canon_pair(T):
    C = ALL - T
    a, b = tuple(sorted(T)), tuple(sorted(C))
    return (a, b) if a < b else (b, a)


def ip(a, b):
    s = sum(x*y for x, y in zip(a, b))
    assert s % len(a) == 0
    return s // len(a)


def main():
    D = shell.build()
    pts, wlines, supports, charts, G = D['pts'], D['wlines'], D['supports'], D['charts'], D['G']
    assert len(pts) == len(wlines) == 40
    assert len(supports) == 45 and len(charts) == 27 and len(G) == 25920

    li = {frozenset(L): i for i, L in enumerate(wlines)}
    line_sets = [set(L) for L in wlines]
    def line_perm(p40):
        return tuple(li[frozenset(p40[x] for x in L)] for L in wlines)

    # W33 Levi chambers and GQ(4,2) factor chambers.
    wch = [(p, ell) for ell, L in enumerate(wlines) for p in L]
    fch = [(packet, c) for c, C in enumerate(charts) for packet in C]
    assert len(wch) == 160 and len(fch) == 135

    # The two 216 carriers.
    _pts2, _idx2, _lines2, N = base.geometry()
    supports2, masks = base.supports_from_N(N)
    assert supports2 == supports
    circuits = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            circuits.append(tuple(C))
    assert len(circuits) == 216

    orbit432 = {frozenset(p40[x] for x in T0) for p40, _p45, _p27 in G}
    assert len(orbit432) == 432
    hpairs = sorted({canon_pair(T) for T in orbit432})
    assert len(hpairs) == 216
    hset = set(hpairs)

    # BT796 slots = skew W33-line pair plus one of four common transversals.
    skew = [(i,j) for i,j in itertools.combinations(range(40),2) if not (line_sets[i] & line_sets[j])]
    trans = []
    for a,b in skew:
        tv = tuple(k for k in range(40) if k not in (a,b) and line_sets[k] & line_sets[a] and line_sets[k] & line_sets[b])
        assert len(tv) == 4
        trans.append(tv)
    assert len(skew) == 540

    chi81=[]; chi64=[]
    pcirc=[]; phemi=[]; pobs=[]; p2160=[]
    order_profiles = Counter()

    for p40,p45,p27 in G:
        lp = line_perm(p40)

        # H1 character = fixed chambers - fixed vertices + 1.
        fp = sum(p40[i] == i for i in range(40))
        fl = sum(lp[i] == i for i in range(40))
        fc = sum(p40[p] == p and lp[ell] == ell for p,ell in wch)
        chi81.append(fc - fp - fl + 1)

        f45 = sum(p45[i] == i for i in range(45))
        f27 = sum(p27[i] == i for i in range(27))
        f135 = sum(p45[p] == p and p27[c] == c for p,c in fch)
        chi64.append(f135 - f45 - f27 + 1)

        # Circuit permutation character.
        pcirc.append(sum(tuple(sorted(p45[x] for x in C)) == C for C in circuits))

        # Hemisystem projective-line permutation character.
        fixed_h=0
        for P in hpairs:
            T = frozenset(P[0])
            image = canon_pair(frozenset(p40[x] for x in T))
            fixed_h += (image == P)
        phemi.append(fixed_h)

        # Obstruction = 27 completion charts x 40 W33 lines.
        pobs.append(f27 * fl)

        # BT796/packet48 2160 character.  A slot is fixed iff its unordered
        # skew pair is fixed and its chosen transversal line is fixed.
        fixed_slots=0
        for s,(a,b) in enumerate(skew):
            if frozenset((lp[a],lp[b])) != frozenset((a,b)):
                continue
            fixed_slots += sum(lp[t] == t for t in trans[s])
        p2160.append(fixed_slots)

    n=len(G)
    assert chi81[0] in range(-1000,1000)  # closure order is not identity-sorted
    # Locate the identity by simultaneous full fixed-point counts.
    ids=[i for i,(a,b,c,d) in enumerate(zip(pcirc,phemi,pobs,p2160)) if a==216 and b==216 and c==1080 and d==2160]
    assert len(ids)==1
    e=ids[0]
    assert chi81[e] == 81 and chi64[e] == 64

    norm81=ip(chi81,chi81); norm64=ip(chi64,chi64); cross=ip(chi81,chi64)
    assert norm81 == norm64 == 1 and cross == 0

    mult = {
      'circuit216': {'H1_W33_81': ip(pcirc,chi81), 'H1_GQ42_64': ip(pcirc,chi64)},
      'hemisystem216': {'H1_W33_81': ip(phemi,chi81), 'H1_GQ42_64': ip(phemi,chi64)},
      'obstruction1080': {'H1_W33_81': ip(pobs,chi81), 'H1_GQ42_64': ip(pobs,chi64)},
      'packet48_BT796_2160': {'H1_W33_81': ip(p2160,chi81), 'H1_GQ42_64': ip(p2160,chi64)},
    }
    assert mult['circuit216'] == {'H1_W33_81':1,'H1_GQ42_64':0}
    assert mult['hemisystem216'] == {'H1_W33_81':0,'H1_GQ42_64':1}
    assert mult['obstruction1080'] == {'H1_W33_81':3,'H1_GQ42_64':3}

    out={
      'schema':'w33.20260901.double-building-steinberg-homology.v1',
      'status':'PASS',
      'groupOrder':n,
      'buildings':{
        'W33_GQ33':{'points':40,'lines':40,'chambers':160,'leviVertices':80,'cycleRank':81},
        'GQ42_factor_geometry':{'points_packets':45,'lines_factorCharts':27,'chambers':135,'leviVertices':72,'cycleRank':64},
      },
      'characterCertificate':{
        'H1_W33_degree':chi81[e], 'H1_W33_norm':norm81,
        'H1_GQ42_degree':chi64[e], 'H1_GQ42_norm':norm64,
        'crossInnerProduct':cross,
        'irreducibleAndNonisomorphicOverCharacteristicZero':True,
      },
      'permutationCarrierMultiplicities':mult,
      'solomonTitsInterpretation':(
        'For a finite group with BN-pair, the Steinberg representation is the top homology of its Tits building. '
        'Thus the two explicitly computed irreducible H1 characters are the degree-81 PSp4(3) Steinberg and degree-64 U4(2) Steinberg under the exceptional isomorphism.'
      ),
      'externalReference':'https://encyclopediaofmath.org/wiki/Steinberg_module',
      'theorem':(
        'The recurring 81 and 64 sectors have an intrinsic geometric origin: they are exactly the first homology modules of the two rank-two Levi graphs carried by the same order-25920 group. '
        'The circuit and hemisystem 216 shells select these two building-homology irreducibles complementarily, while the 1080 obstruction carrier contains three copies of each. '
        'The recorded 2160 multiplicities decide whether the BT796/packet48 shell contains enough copies to route both multiplicity-three blocks.'
      ),
      'boundary':(
        'This is finite building homology and characteristic-zero representation theory. It gives no particle, field, energy, spacetime, or experimental identification by itself.'
      )
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','norm81':norm81,'norm64':norm64,'cross':cross,'multiplicities':mult},sort_keys=True))

if __name__=='__main__':
    main()
