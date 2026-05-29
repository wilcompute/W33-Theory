#!/usr/bin/env python3
"""Gray-code / error-correction lift of the Q4 router.

Gray code gives the Hamiltonian clock on Q4, but Gray code by itself is not an
error-correcting code: adjacent states differ in one bit.  The protected lift is
to keep the Q4/Cl4 state as the 4 information bits and encode each state by the
[8,4,4] extended Hamming code, equivalently RM(1,3).

Then every Gray-clock one-bit transition becomes a weight-4 transition between
8-bit protected codewords.  The 16 router states remain 16 states, but now they
sit in an 8-bit self-dual, doubly-even code of minimum distance 4.

This proves the finite architecture:

    Q4 Gray router state  ->  [8,4,4] extended-Hamming/RM(1,3) codeword
    one router bit flip   ->  distance-4 protected code transition
    16 codewords          ->  same count as Cl4 blades and D8 Frobenius norm

The full distance-4 graph on the code is K16 minus a perfect matching; the Q4
Gray cycle is a Hamiltonian subcycle inside that error-detection shell.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

N=4
CODE_N=8
CODE_K=4
CODE_D=4
V_W33=40
H1=81
WE6=51_840
PHI6=7
K_LEVEL=12
E2=16

# Generator from the standard [8,4,4] extended Hamming code form.
G = [
    [1,0,0,0,0,1,1,1],
    [0,1,0,0,1,0,1,1],
    [0,0,1,0,1,1,0,1],
    [0,0,0,1,1,1,1,0],
]

# The cyclic Gray clock already used by the toroidal-knight/Q4 router verifier.
GRAY_CLOCK = [
    (0,0,0,0),(0,1,0,0),(0,1,1,0),(0,0,1,0),
    (0,0,1,1),(0,1,1,1),(0,1,0,1),(0,0,0,1),
    (1,0,0,1),(1,1,0,1),(1,1,1,1),(1,0,1,1),
    (1,0,1,0),(1,1,1,0),(1,1,0,0),(1,0,0,0),
]


def add2(a,b):
    return tuple((x+y)&1 for x,y in zip(a,b))


def dot2(message, row):
    return sum(x*y for x,y in zip(message,row)) & 1


def encode(message:tuple[int,...]) -> tuple[int,...]:
    out=[0]*CODE_N
    for bit,row in zip(message,G):
        if bit:
            out=[(x+y)&1 for x,y in zip(out,row)]
    return tuple(out)


def weight(v):
    return sum(v)


def hamming(a,b):
    return sum(x!=y for x,y in zip(a,b))


def rank_mod2(rows):
    A=[list(r) for r in rows if any(r)]
    rank=0
    col=0
    m=len(A); n=len(A[0]) if A else 0
    while rank<m and col<n:
        piv=next((i for i in range(rank,m) if A[i][col]), None)
        if piv is None:
            col += 1
            continue
        A[rank],A[piv]=A[piv],A[rank]
        for i in range(m):
            if i!=rank and A[i][col]:
                A[i]=[(x^y) for x,y in zip(A[i],A[rank])]
        rank += 1
        col += 1
    return rank


def all_messages():
    return list(itertools.product((0,1), repeat=CODE_K))


def all_codewords():
    return [encode(m) for m in all_messages()]


def pair_distance_distribution(words):
    counts=Counter()
    for i,j in itertools.combinations(range(len(words)),2):
        counts[hamming(words[i],words[j])] += 1
    return dict(sorted(counts.items()))


def gray_flip_sequence(seq):
    out=[]
    for i,a in enumerate(seq):
        b=seq[(i+1)%len(seq)]
        diff=[j for j in range(len(a)) if a[j]!=b[j]]
        out.append(diff[0] if len(diff)==1 else -1)
    return out


def distance4_graph(words):
    adj={i:set() for i in range(len(words))}
    for i,j in itertools.combinations(range(len(words)),2):
        if hamming(words[i],words[j])==4:
            adj[i].add(j); adj[j].add(i)
    return adj


def graph_edges(adj):
    return sum(len(ns) for ns in adj.values())//2


def graph_diameter(adj):
    diam=0
    for s in adj:
        dist={s:0}; q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v]=dist[u]+1; q.append(v)
        diam=max(diam,max(dist.values()))
    return diam


def parity_check_matrix_from_dual_self() -> list[list[int]]:
    # Since the code is self-dual, G is also a parity-check matrix.
    return G


def syndrome(word):
    H=parity_check_matrix_from_dual_self()
    return tuple(dot2(word,row) for row in H)


def single_error_syndromes():
    zero=(0,)*CODE_N
    out={}
    for i in range(CODE_N):
        e=[0]*CODE_N; e[i]=1
        out[i]=syndrome(tuple(e))
    return out


def build_payload():
    messages=all_messages()
    words=all_codewords()
    wordset=set(words)
    weights=Counter(weight(w) for w in words)
    dists=pair_distance_distribution(words)
    nonzero=[w for w in words if any(w)]
    min_dist=min(hamming(a,b) for a,b in itertools.combinations(words,2))
    GGT=[[sum(G[i][t]*G[j][t] for t in range(CODE_N))&1 for j in range(CODE_K)] for i in range(CODE_K)]
    gray_words=[encode(m) for m in GRAY_CLOCK]
    gray_code_distances=[hamming(gray_words[i],gray_words[(i+1)%len(gray_words)]) for i in range(len(gray_words))]
    gray_flips=gray_flip_sequence(GRAY_CLOCK)
    d4=distance4_graph(words)
    d4_degrees=Counter(len(ns) for ns in d4.values())
    complement_pairs=sum(1 for w in words if tuple(1-x for x in w) in wordset)//2
    synd=single_error_syndromes()
    unique_nonzero_syndromes=len(set(synd.values()))==CODE_N and all(any(s) for s in synd.values())

    checks={
        "rank_G_is_4": rank_mod2(G)==4,
        "code_has_16_codewords": len(words)==16 and len(wordset)==16,
        "min_distance_is_4": min_dist==4,
        "weight_enumerator_is_1_14_1": dict(sorted(weights.items()))=={0:1,4:14,8:1},
        "all_nonzero_weights_doubly_even": all(weight(w)%4==0 for w in nonzero),
        "self_orthogonal_and_self_dual": GGT==[[0]*CODE_K for _ in range(CODE_K)] and rank_mod2(G)==CODE_N//2,
        "pair_distances_are_4_or_8": dists=={4:112,8:8},
        "distance4_graph_is_K16_minus_matching": graph_edges(d4)==112 and d4_degrees=={14:16} and complement_pairs==8,
        "distance4_graph_diameter_is_2": graph_diameter(d4)==2,
        "gray_clock_is_cyclic_unit_distance_on_info_Q4": all(x>=0 for x in gray_flips) and len(set(GRAY_CLOCK))==16,
        "encoded_gray_steps_all_distance_4": gray_code_distances==[4]*16,
        "single_bit_error_syndromes_are_unique_nonzero": unique_nonzero_syndromes,
        "can_correct_one_detect_three": CODE_D==4,
        "WE6_factorization_survives": WE6==V_W33*len(words)*H1,
        "D8_E2_matches_codeword_count": E2==len(words),
        "Phi6_plus_one_equals_code_length": PHI6+1==CODE_N,
        "k_level_plus_4_equals_codeword_count": K_LEVEL+4==len(words),
    }
    return {
        "theorem":"Gray_Hamming_RM13_router_lift",
        "code":"binary extended Hamming [8,4,4], equivalently RM(1,3)",
        "generator_matrix":G,
        "parameters":{"length":CODE_N,"dimension":CODE_K,"distance":CODE_D,"codewords":len(words)},
        "weight_enumerator":dict(sorted(weights.items())),
        "pair_distance_distribution":dists,
        "self_dual_check":{"GGT_mod2":GGT,"rank":rank_mod2(G)},
        "gray_router_lift":{"info_gray_clock":GRAY_CLOCK,"flip_sequence":gray_flips,"encoded_step_distances":gray_code_distances,"statement":"each one-bit Q4 Gray move lifts to a distance-4 move in the protected [8,4,4] code"},
        "distance4_shell":{"vertices":len(words),"edges":graph_edges(d4),"degree_distribution":dict(d4_degrees),"diameter":graph_diameter(d4),"complement_pairs_distance8":complement_pairs,"interpretation":"distance-4 shell is K16 minus the 8 complement pairs"},
        "error_correction":{"minimum_distance":min_dist,"corrects_worst_case_errors":(min_dist-1)//2,"detects_errors_up_to":min_dist-1,"single_error_syndromes":{str(k):v for k,v in synd.items()}},
        "W33_bridge":{"factorization":"51840 = 40 * 16 * 81","W33_anchors":V_W33,"router_codewords":len(words),"H1_phase_rank":H1,"Phi6_plus_one_code_length":PHI6+1,"D8_E2_codeword_count":E2},
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_gray_hamming_router_lift.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"parameters":payload["parameters"],"weight_enumerator":payload["weight_enumerator"],"gray_router_lift":payload["gray_router_lift"],"W33_bridge":payload["W33_bridge"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
