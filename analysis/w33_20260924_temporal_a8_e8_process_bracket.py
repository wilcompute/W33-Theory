#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_a8_e8_process_bracket.json"

from analysis.w33_20260924_temporal_hesse_4a2_a8_bridge import (
    CELLS, collinear,
)

N=9
ALL=set(range(N))
TRIPLES=[tuple(x) for x in itertools.combinations(range(N),3)]
TSET=set(TRIPLES)
A8=[(i,j) for i in range(N) for j in range(N) if i!=j]

def act_a8_on_lam3(root,S):
    i,j=root
    S=set(S)
    if j in S and i not in S:
        return tuple(sorted((S-{j})|{i}))
    return None

def act_a8_on_lam6_index(root,T):
    # Lambda6 root indexed as -w_T, T is the complementary 3-subset.
    i,j=root
    T=set(T)
    if i in T and j not in T:
        return tuple(sorted((T-{i})|{j}))
    return None
def bracket_lam3_lam3(S,T):
    S=set(S); T=set(T)
    if S&T:
        return None
    U=tuple(sorted(ALL-(S|T)))
    return ("lam6",U)

def bracket_lam6_lam6(S,T):
    S=set(S); T=set(T)
    if S&T:
        return None
    U=tuple(sorted(ALL-(S|T)))
    return ("lam3",U)

def bracket_lam3_lam6(S,T):
    S=set(S); T=set(T)
    if S==T:
        return ("cartan",tuple(sorted(S)))
    if len(S&T)==2:
        i=next(iter(S-T))
        j=next(iter(T-S))
        return ("a8",(i,j))
    return None

def main():
    # Natural sl9 action on both exterior sectors is surjective.
    a3=Counter()
    a6=Counter()
    for r in A8:
        for S in TRIPLES:
            T=act_a8_on_lam3(r,S)
            if T is not None:
                assert T in TSET
                a3[T]+=1
            T=act_a8_on_lam6_index(r,S)
            if T is not None:
                assert T in TSET
                a6[T]+=1
    assert sum(a3.values())==sum(a6.values())==1512
    assert set(a3.values())==set(a6.values())=={18}
    # Exterior wedge rules.
    out36=Counter()
    pairs36=0
    for S,T in itertools.combinations(TRIPLES,2):
        z=bracket_lam3_lam3(S,T)
        if z:
            pairs36+=1
            out36[z[1]]+=1
    assert pairs36==840
    assert len(out36)==84 and set(out36.values())=={10}

    out63=Counter()
    pairs63=0
    for S,T in itertools.combinations(TRIPLES,2):
        z=bracket_lam6_lam6(S,T)
        if z:
            pairs63+=1
            out63[z[1]]+=1
    assert pairs63==840
    assert out63==out36

    contraction=Counter()
    opposite=0
    zero=0
    for S in TRIPLES:
        for T in TRIPLES:
            z=bracket_lam3_lam6(S,T)
            if z is None:
                zero+=1
            elif z[0]=="cartan":
                opposite+=1
            else:
                contraction[z[1]]+=1
    assert opposite==84
    assert sum(contraction.values())==1512
    assert len(contraction)==72 and set(contraction.values())=={21}
    # Hesse-specific root-support closure.
    hesse=[t for t in TRIPLES if collinear(t)]
    noncol=[t for t in TRIPLES if not collinear(t)]
    assert (len(hesse),len(noncol))==(12,72)

    hesse_rows=[]
    same_direction_nonzero=0
    cross_direction_zero=0
    for S,T in itertools.combinations(hesse,2):
        z=bracket_lam3_lam3(S,T)
        inter=len(set(S)&set(T))
        if inter==0:
            assert z is not None
            U=z[1]
            assert U in hesse
            assert set(S)|set(T)|set(U)==ALL
            same_direction_nonzero+=1
            hesse_rows.append({
              "line1":list(S),"line2":list(T),
              "bracket":"-w_"+str(U),"third_parallel_line":list(U),
            })
        else:
            assert inter==1 and z is None
            cross_direction_zero+=1
    assert same_direction_nonzero==12
    assert cross_direction_zero==54

    # Complete 240-root support inventory.
    assert 72+84+84==240
    out={
      "schema":"w33.20260924.temporal_a8_e8_process_bracket.v1",
      "status":"PASS_NINE_HISTORY_CELLS_COMPILE_THE_A8_E8_ROOT_SUPPORT_BRACKETS",
      "basis":{
        "history_cells":9,
        "sl9_roots":72,
        "Lambda3_packets":84,
        "Lambda6_dual_packets":84,
        "root_total":240,
        "Cartan_dimension":8,
        "Lie_dimension":248,
      },
      "support_rules":{
        "sl9_on_Lambda3":"E_ij replaces j by i when j in S and i not in S",
        "sl9_on_Lambda6":"dual replacement on the complementary 3-subset index",
        "Lambda3_Lambda3":"disjoint S,T -> -w_complement(S union T)",
        "Lambda6_Lambda6":"disjoint S,T -> +w_complement(S union T)",
        "Lambda3_Lambda6":"|S intersect T|=2 -> E_(S\\T),(T\\S); S=T -> Cartan",
      },
      "exact_counts":{
        "sl9_Lambda3_nonzero":sum(a3.values()),
        "sl9_Lambda3_preimages_per_output":18,
        "sl9_Lambda6_nonzero":sum(a6.values()),
        "Lambda3_Lambda3_nonzero_unordered_pairs":pairs36,
        "Lambda3_Lambda3_preimages_per_output":10,
        "Lambda3_Lambda6_root_contractions":sum(contraction.values()),
        "Lambda3_Lambda6_preimages_per_A8_root":21,
        "Lambda3_Lambda6_opposite_Cartan_pairs":opposite,
      },
      "Hesse_process":{
        "Hesse_lines":len(hesse),
        "noncollinear_triangles":len(noncol),
        "same_parallel_class_nonzero_pairs":same_direction_nonzero,
        "different_direction_zero_pairs":cross_direction_zero,
        "law":"two parallel Hesse lines bracket to the negative root of the third line; different striations have zero root-sum bracket",
        "rows":hesse_rows,
      },
      "theorem":(
        "The standard A8 root support of E8 is a literal process compiler on "
        "nine history cells. sl9 roots perform one-cell substitutions on three-"
        "history packets; disjoint packets wedge to the complementary dual "
        "packet; Lambda3/Lambda6 packets differing in one cell contract to the "
        "corresponding sl9 transition; opposite packets return a Cartan update. "
        "All output root supports are reached with uniform exact multiplicities. "
        "On the Hesse 12, this specializes to four independent A2 bracket "
        "triangles, one per temporal/null striation."
      ),
      "boundary":(
        "This packet certifies Chevalley root-support incidence, not the signs "
        "of every structure constant. Signed Jacobi-normalized brackets remain "
        "owned by the repository's frozen E8 structure-constant artifact."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "counts":out["exact_counts"],
      "Hesse":{k:v for k,v in out["Hesse_process"].items() if k!="rows"},
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
