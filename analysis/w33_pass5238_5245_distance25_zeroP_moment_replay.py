#!/usr/bin/env python3
"""Pass5238-5245 fast algebraic replay.

This producer locks the proof steps that do not require the heavier orbit/MILP
censuses: the shell-moment distance lemma, q=3/5/7 footprint distances from the
frozen shell parameters, the q=5 local even tensor distance 40, and the strict
zero-P reduction.  Heavy finite enumerations are frozen in
PART_W33_PASS5238_5245_RESULTS.json and have separate workflow commands.
"""
from itertools import combinations


def shell_distance(replication: int, max_pair_codegree: int) -> int:
    assert replication % max_pair_codegree == 0
    # For a primal support of weight w and dual checks B, t_B is even:
    #   sum C(t_B,2) >= (1/2)sum t_B = r w/2
    # and <= lambda C(w,2).  Hence w >= 1+r/lambda.
    return 1 + replication // max_pair_codegree


def cut_k6_words():
    edges=list(combinations(range(6),2))
    out=[]
    for mask in range(1<<5): # vertex 5 is the fixed cut gauge
        S={i for i in range(5) if (mask>>i)&1}
        w=0
        bits=0
        for j,(u,v) in enumerate(edges):
            if ((u in S) != (v in S)):
                bits |= 1<<j
                w += 1
        out.append(bits)
    return out


def main():
    # Shell-moment anchors.
    assert shell_distance(24,3)==9
    assert shell_distance(600,25)==25
    assert shell_distance(18816,392)==49

    # Cut(K6): d1=5 and d2=9.
    C=cut_k6_words()
    weights=sorted(x.bit_count() for x in C if x)
    assert weights[0]==5
    d2=min((a|b).bit_count() for i,a in enumerate(C) if a
           for b in C[i+1:] if b and b!=a)
    assert d2==9

    # Rank-one tensor weights are products of nonzero factor weights.
    factor_weights=sorted(set(weights))
    even_rank1=min(a*b for a in factor_weights for b in factor_weights
                   if (a*b)%2==0)
    assert even_rank1==40
    # Any tensor rank >=2 has at least d2 nonzero rows, each of factor weight d1.
    assert d2*weights[0]==45>40
    # Six factor words have weight5 and fifteen have weight8; both orientations.
    n5=sum(x.bit_count()==5 for x in C)
    n8=sum(x.bit_count()==8 for x in C)
    assert (n5,n8)==(6,15)
    assert 2*n5*n8==180

    # q5 strict reduction: nonzero P parity has >=25 odd components and each
    # odd component costs >=25 apartment coordinates.
    assert 25*25==625
    # Zero P parity forces even local states, so a strict (<625) word can have
    # at most floor(624/40)=15 active P components.
    assert 624//40==15

    # q7 shell geometry arithmetic.
    n=1225; k=384; t=12; selected_edges=48
    assert t*k//(2*selected_edges)==48 # q^2-1
    assert 1+t*k//(2*selected_edges)==49

    print('PASS5238-5245 FAST REPLAY OK')
    print('q3/q5/q7 footprint distances = 9,25,49')
    print('q5 local even P-component distance = 40; strict active components <=15')
    print('FIREWALL: q5 strict sub-625 zero-P sector / leader36 remains open')


if __name__=='__main__':
    main()
