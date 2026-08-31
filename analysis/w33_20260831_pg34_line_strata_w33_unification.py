#!/usr/bin/env python3
"""Unify the 357 PG(3,4) lines with W33/GQ(4,2)/trade-lattice objects.

Starting from the repository's independently reconstructed 85x85 Hermitian
polarity design matrix H, this audit recovers every projective line as the
intersection of two polar planes.  It then proves that the classical Hermitian
line-type split 357 = 27 + 240 + 90 is exactly the repo's existing finite
geometry:

  27 generators (5 absolute + 0 nonabsolute)
      = the 27 GQ(4,2) lines on the 45 minimum-vector labels;

  240 secants (3 absolute + 2 nonabsolute)
      = the 240 W33 edges on the 40 nonabsolute labels;
      polarity pairs them into 120 pairs, whose four nonabsolute endpoints are
      exactly one W33 line, with three complementary-edge pairings per line;

  90 tangents (1 absolute + 4 nonabsolute)
      = the 90 historical flat tetrads / tangent four-cocliques;
      polarity pairs them into 45 pairs, and each 4+4 union is exactly one of
      the 45 sentinel weight-8 supports / projective norm-8 lattice minima.

Thus the 27 Schlaefli-complement base, 240 edge carrier, 90 flat tetrads,
45 sentinel minima and 40 W33 lines are all line-polarity strata of one
PG(3,4) geometry rather than unrelated equal-count phenomena.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import w33_20260829_pg34_polarity_sentinel as pg
import w33_20260828_trade_lattice_minimum_gq45 as trade

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_PG34_LINE_STRATA_W33_UNIFICATION.json'


def srg(G):
    deg={len(x) for x in G}; la=set(); mu=set()
    for i,j in itertools.combinations(range(len(G)),2):
        c=len(G[i]&G[j]); (la if j in G[i] else mu).add(c)
    return [len(G),sorted(deg),sorted(la),sorted(mu)]


def main():
    N,A=pg.geometry(); B,G=pg.trade_incidence(N)
    H=[]
    for i in range(40): H.append(A[i]+B[i])
    for j in range(45):
        H.append([B[i][j] for i in range(40)] + [G[j][k]+(1 if j==k else 0) for k in range(45)])
    assert len(H)==85 and all(sum(r)==21 for r in H)

    # For Hermitian polarity, intersection of two polar planes is the polar
    # projective line.  Across all unordered point pairs these are exactly the
    # 357 lines of PG(3,4), each with five points.
    lines85=set()
    for i,j in itertools.combinations(range(85),2):
        L=tuple(k for k in range(85) if H[i][k] and H[j][k])
        assert len(L)==5
        lines85.add(L)
    lines85=sorted(lines85); assert len(lines85)==357

    strata=defaultdict(list)
    for L in lines85:
        non=tuple(x for x in L if x<40)
        ab=tuple(x-40 for x in L if x>=40)
        strata[(len(ab),len(non))].append((L,ab,non))
    counts={str(k):len(v) for k,v in sorted(strata.items())}
    assert {k:len(v) for k,v in strata.items()}=={(5,0):27,(3,2):240,(1,4):90}

    # The 45-point absolute block G is GQ(4,2) adjacency: generators are its
    # five-point maximal cliques / lines.  Check directly from the 27 sets.
    gen_abs={tuple(sorted(ab)) for _,ab,_ in strata[(5,0)]}
    assert len(gen_abs)==27
    assert all(all(G[a][b] for a,b in itertools.combinations(L,2)) for L in gen_abs)
    abs_line_degree=Counter(x for L in gen_abs for x in L)
    assert set(abs_line_degree.values())=={3}

    # 240 secants -> exactly all W33 edges.
    secant_edges={tuple(sorted(non)) for _,_,non in strata[(3,2)]}
    w33_edges={tuple((i,j)) for i,j in itertools.combinations(range(40),2) if A[i][j]}
    assert len(secant_edges)==240 and secant_edges==w33_edges

    # 90 tangents -> 4-cocliques.
    tangent_tetrads={tuple(sorted(non)) for _,_,non in strata[(1,4)]}
    assert len(tangent_tetrads)==90
    assert all(not any(A[a][b] for a,b in itertools.combinations(T,2)) for T in tangent_tetrads)

    # Reconstruct the historical 90 flat tetrads independently, using the same
    # tricentric-center rule as the lattice minimum theorem.
    centers={}
    for t in itertools.combinations(range(40),3):
        if all(not A[a][b] for a,b in itertools.combinations(t,2)):
            centers[t]=tuple(x for x in range(40) if all(A[x][a] for a in t))
    flat=[t for t,c in centers.items() if len(c)==4]
    historical={tuple(sorted(centers[t])) for t in flat}
    assert len(historical)==90 and tangent_tetrads==historical

    # Line polarity: L^perp = intersection of polar planes of any two points
    # on L.  This is an involution on the 357 lines.
    line_index={L:i for i,L in enumerate(lines85)}
    pol=[]
    for L in lines85:
        i,j=L[:2]
        P=tuple(k for k in range(85) if H[i][k] and H[j][k])
        # P computed this way is L^perp only if L here is span(i,j); our lines85
        # themselves arose as polar lines.  In a nondegenerate polarity the same
        # set construction is involutive, and direct closure below verifies it.
        assert P in line_index
        pol.append(line_index[P])
    assert all(pol[pol[i]]==i for i in range(357))

    type_index={i:(sum(x>=40 for x in L),sum(x<40 for x in L)) for i,L in enumerate(lines85)}
    assert all(type_index[i]==type_index[pol[i]] for i in range(357))
    fixed=Counter(type_index[i] for i in range(357) if pol[i]==i)
    pair_counts=Counter()
    seen=set()
    for i in range(357):
        if i in seen: continue
        j=pol[i]; seen.add(i); seen.add(j)
        pair_counts[type_index[i]]+=1

    # WARNING: because lines85 were constructed as intersections of polar
    # planes, the direct row-intersection operation on two points of L returns
    # L^perp. This distinguishes fixed generators from paired secants/tangents.
    assert fixed==Counter({(5,0):27})
    assert pair_counts==Counter({(5,0):27,(3,2):120,(1,4):45})

    # Secant polar pairs -> complementary edges of a unique W33 line (4-clique).
    secant_pair_unions=[]
    for i,L in enumerate(lines85):
        if type_index[i]!=(3,2) or i>pol[i]: continue
        e1=tuple(x for x in L if x<40)
        e2=tuple(x for x in lines85[pol[i]] if x<40)
        assert set(e1).isdisjoint(e2)
        U=tuple(sorted(set(e1)|set(e2))); assert len(U)==4
        assert all(A[a][b] for a,b in itertools.combinations(U,2))
        secant_pair_unions.append(U)
    assert len(secant_pair_unions)==120
    # The maximal 4-cliques of W33 are exactly its 40 GQ lines, each receiving
    # the three complementary-edge partitions.
    w33_lines=set()
    for U in itertools.combinations(range(40),4):
        if all(A[a][b] for a,b in itertools.combinations(U,2)): w33_lines.add(tuple(U))
    assert len(w33_lines)==40
    assert set(secant_pair_unions)==w33_lines
    assert Counter(secant_pair_unions)==Counter({L:3 for L in w33_lines})

    # Tangent polar pairs -> the 45 disjoint flat-tetrad pairs / sentinel minima.
    tangent_pair_unions=[]; tangent_abs=[]
    for i,L in enumerate(lines85):
        if type_index[i]!=(1,4) or i>pol[i]: continue
        P=lines85[pol[i]]
        T1=tuple(x for x in L if x<40); T2=tuple(x for x in P if x<40)
        a1=tuple(x-40 for x in L if x>=40); a2=tuple(x-40 for x in P if x>=40)
        assert len(a1)==len(a2)==1 and a1==a2
        assert set(T1).isdisjoint(T2)
        U=frozenset(T1)|frozenset(T2); assert len(U)==8
        tangent_pair_unions.append(tuple(sorted(U))); tangent_abs.append(a1[0])
    assert len(tangent_pair_unions)==45 and len(set(tangent_abs))==45
    supports={tuple(sorted(c for c in range(40) if B[c][m])) for m in range(45)}
    assert set(tangent_pair_unions)==supports
    # In fact the common absolute point labels the same B-column support.
    for U,m in zip(tangent_pair_unions,tangent_abs):
        assert U==tuple(sorted(c for c in range(40) if B[c][m]))

    # Incidence summary: tangent tetrad through each nonabsolute point and
    # generator/secant incidences recover the expected projective line counts.
    tangent_point_degree=Counter(x for T in tangent_tetrads for x in T)
    secant_point_degree=Counter(x for e in secant_edges for x in e)
    assert set(tangent_point_degree.values())=={9}
    assert set(secant_point_degree.values())=={12}

    out={
      'schema':'w33.20260831.pg34-line-strata-w33-unification.v1','status':'PASS',
      'PG34':{'points':85,'lines':357,'lineSize':5,'lineTypeCounts':counts,
              'polarityFixedLineCounts':{str(k):v for k,v in sorted(fixed.items())},
              'polarityOrbitCounts':{str(k):v for k,v in sorted(pair_counts.items())}},
      'generator27':{'count':27,'absolutePerLine':5,'GQ42LinesExactly':True,
                     'eachAbsolutePointOn':3,'dualCarrier':'GQ(2,4) / Schlaefli-complement 27-point graph'},
      'secant240':{'count':240,'absolutePerLine':3,'nonabsolutePerLine':2,
                   'nonabsolutePairsExactlyW33Edges':True,'W33EdgeCount':240,
                   'polarityPairs':120,'polarPairUnionExactlyW33Line':True,
                   'W33Lines':40,'polarEdgePairsPerW33Line':3},
      'tangent90':{'count':90,'absolutePerLine':1,'nonabsolutePerLine':4,
                   'nonabsoluteTetradsExactlyHistoricalFlatTetrads':True,
                   'tetradsAreW33Cocliques':True,'polarityPairs':45,
                   'polarTangentPairUnionExactlySentinelSupport':True,
                   'sentinelSupports':45,'commonAbsolutePointLabelsSupport':True},
      'masterIdentity':'357 = 27 generators + 240 secants + 90 tangents; Hermitian polarity refines this as 27 fixed generators + 120 secant pairs + 45 tangent pairs.',
      'theorem':'The 27 Schlaefli/GQ base lines, 240 W33 edges, 90 flat tetrads, 45 sentinel minimum supports and 40 W33 lines are exact strata or polarity quotients of the single 357-line PG(3,4) geometry reconstructed from H.',
      'boundary':'Exact finite geometry. The Veldkamp terminology is a classical reinterpretation of the already reconstructed PG(3,4) point/plane polarity design; no physical identification is asserted.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','strata':counts,'fixed':dict(fixed),'polarityPairs':dict(pair_counts),
                      'edges':len(secant_edges),'tetrads':len(tangent_tetrads),'supports':len(supports)},sort_keys=True))

if __name__=='__main__': main()
