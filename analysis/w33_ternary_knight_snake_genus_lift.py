#!/usr/bin/env python3
"""Ternary knight / snake / genus lift for the Q4 router.

The binary Q4 layer is the endpoint skeleton.  A knight jump is not binary inside:
it is a three-unit micro-walk: straight, straight, then perpendicular.  If the
starting square is treated as the previous jump's landing square, each macro jump
contributes exactly three new unit steps, naturally carrying a Z3 phase.

This verifier separates four layers:

1. Q4 Gray clock: 16 macro states, Hamiltonian cycle, one bit flips per jump.
2. Ternary knight lift: every macro jump is a 3-step word (a,a,b) with b
   perpendicular to a; landing parity flips because 3 is odd.
3. Snake/coil correction: the full 16 Gray cycle is not an induced coil in Q4.
   The maximum Q4 coil has length 8; an explicit induced 8-cycle is verified.
4. Genus congruence: triangular complete-graph closure occurs exactly for
   n = 0,3,4,7 mod 12, i.e. the W33 residue packet {0,q,chi,Phi6}.

The ternary microcounts are then:

    full Gray clock: 16 macro jumps * 3 = 48 microticks (Reye incidence count)
    induced Q4 coil: 8 macro jumps * 3 = 24 microticks (m_r / Cl4 square faces)

This keeps the theory ternary/qutrit at the information-flow level while allowing
the binary Q4 graph to act as the endpoint/router skeleton.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

Q=3
CHI=4
PHI6=7
K=12
G2=6
M_R=24
REYE_INCIDENCES=48
V_W33=40
H1=81
WE6=51_840
BOARD=4

KNIGHT_TO_Q4={
    (0,0):(0,0,0,0), (2,3):(0,0,0,1), (3,2):(0,0,1,0), (1,1):(0,0,1,1),
    (1,2):(0,1,0,0), (3,1):(0,1,0,1), (2,0):(0,1,1,0), (0,3):(0,1,1,1),
    (2,1):(1,0,0,0), (0,2):(1,0,0,1), (1,3):(1,0,1,0), (3,0):(1,0,1,1),
    (3,3):(1,1,0,0), (1,0):(1,1,0,1), (0,1):(1,1,1,0), (2,2):(1,1,1,1),
}
GRAY_KNIGHT_TOUR=[(0,0),(1,2),(2,0),(3,2),(1,1),(0,3),(3,1),(2,3),(0,2),(1,0),(2,2),(3,0),(1,3),(0,1),(3,3),(2,1)]
Q4_COIL=[(0,0,0,0),(0,0,0,1),(0,0,1,1),(0,1,1,1),(1,1,1,1),(1,1,1,0),(1,1,0,0),(1,0,0,0)]


def q4_vertices():
    return list(itertools.product((0,1), repeat=4))


def q4_edges():
    edges=set()
    for v in q4_vertices():
        for i in range(4):
            w=list(v); w[i]^=1; w=tuple(w)
            edges.add(tuple(sorted((v,w))))
    return edges


def hamming(a,b):
    return sum(x!=y for x,y in zip(a,b))


def q4_adj():
    adj={v:set() for v in q4_vertices()}
    for a,b in q4_edges():
        adj[a].add(b); adj[b].add(a)
    return adj


def is_cycle(seq, adj):
    return len(set(seq))==len(seq) and all(seq[(i+1)%len(seq)] in adj[seq[i]] for i in range(len(seq)))


def is_induced_cycle(seq, adj):
    if not is_cycle(seq, adj):
        return False
    n=len(seq); pos={v:i for i,v in enumerate(seq)}
    for i,u in enumerate(seq):
        for v in adj[u]:
            if v in pos:
                j=pos[v]
                if (i-j)%n not in (1,n-1):
                    return False
    return True


def max_coil_length_q4_bruteforce():
    # Small exact brute force for Q4 induced cycles through 0000.
    adj=q4_adj(); start=(0,0,0,0); best=[]
    def dfs(path):
        nonlocal best
        u=path[-1]
        if len(path)>2 and start in adj[u] and is_induced_cycle(path,adj):
            if len(path)>len(best):
                best=path[:]
        for v in adj[u]:
            if v==start or v in path:
                continue
            # Prune induced-path chords.
            ok=True
            for old in path[:-1]:
                if v in adj[old]:
                    ok=False; break
            if ok:
                path.append(v); dfs(path); path.pop()
    dfs([start])
    return best


def signed_delta(a,b):
    dr=(b[0]-a[0])%BOARD
    dc=(b[1]-a[1])%BOARD
    def s(x):
        if x==0: return 0
        if x==1: return 1
        if x==3: return -1
        if x==2: return 2  # orientation choice on Z4; +2 and -2 coincide.
        raise ValueError(x)
    return (s(dr),s(dc))


def decompose_knight_move(a,b):
    dr,dc=signed_delta(a,b)
    if abs(dr)==2 and abs(dc)==1:
        long_axis=0; long_sign=1 if dr==2 else -1; short_axis=1; short_sign=dc
    elif abs(dc)==2 and abs(dr)==1:
        long_axis=1; long_sign=1 if dc==2 else -1; short_axis=0; short_sign=dr
    else:
        raise ValueError((a,b,dr,dc))
    step_long=(long_sign,0) if long_axis==0 else (0,long_sign)
    step_short=(short_sign,0) if short_axis==0 else (0,short_sign)
    return [step_long,step_long,step_short]


def add_square(a,step):
    return ((a[0]+step[0])%BOARD,(a[1]+step[1])%BOARD)


def micro_path_for_macro_cycle(cycle):
    records=[]
    for i,a in enumerate(cycle):
        b=cycle[(i+1)%len(cycle)]
        steps=decompose_knight_move(a,b)
        cur=a
        for phase,step in enumerate(steps):
            nxt=add_square(cur,step)
            records.append({"macro_index":i,"phase":phase,"from":cur,"to":nxt,"step":step})
            cur=nxt
        if cur!=b:
            raise AssertionError((a,b,steps,cur))
    return records


def square_parity(sq):
    return (sq[0]+sq[1])%2


def gray_flip_sequence_from_squares(cycle):
    bits=[KNIGHT_TO_Q4[v] for v in cycle]
    seq=[]
    for i,a in enumerate(bits):
        b=bits[(i+1)%len(bits)]
        diff=[j for j in range(4) if a[j]!=b[j]]
        seq.append(diff[0] if len(diff)==1 else -1)
    return seq


def genus_complete(n):
    return ((n-3)*(n-4))//12 if ((n-3)*(n-4))%12==0 else None


def allowed_triangular_residues_mod12():
    return [n for n in range(12) if ((n-3)*(n-4))%12==0]


def build_payload():
    adj=q4_adj()
    full_bits=[KNIGHT_TO_Q4[v] for v in GRAY_KNIGHT_TOUR]
    full_micro=micro_path_for_macro_cycle(GRAY_KNIGHT_TOUR)
    # Map Q4 coil to board squares by inverse labeling.
    inv={v:k for k,v in KNIGHT_TO_Q4.items()}
    coil_squares=[inv[v] for v in Q4_COIL]
    coil_micro=micro_path_for_macro_cycle(coil_squares)
    brute_best=max_coil_length_q4_bruteforce()
    residues=allowed_triangular_residues_mod12()
    key_ns=[3,4,7,12,15,16,19]
    genus_values={n:genus_complete(n) for n in key_ns}
    full_perp=[r["step"] for r in full_micro]
    first_two_equal_all=all(full_micro[3*i]["step"]==full_micro[3*i+1]["step"] for i in range(len(GRAY_KNIGHT_TOUR)))
    last_perp_all=all((full_micro[3*i]["step"][0]*full_micro[3*i+2]["step"][0]+full_micro[3*i]["step"][1]*full_micro[3*i+2]["step"][1])==0 for i in range(len(GRAY_KNIGHT_TOUR)))
    landing_parity_flips=all(square_parity(GRAY_KNIGHT_TOUR[i]) != square_parity(GRAY_KNIGHT_TOUR[(i+1)%16]) for i in range(16))
    micro_phase_counts=Counter(r["phase"] for r in full_micro)

    checks={
        "full_gray_cycle_is_Q4_hamilton_cycle": len(set(full_bits))==16 and all(hamming(full_bits[i], full_bits[(i+1)%16])==1 for i in range(16)),
        "full_gray_cycle_is_not_induced_coil": not is_induced_cycle(full_bits, adj),
        "explicit_Q4_coil_is_induced_length_8": is_induced_cycle(Q4_COIL, adj) and len(Q4_COIL)==8,
        "bruteforce_max_Q4_coil_length_is_8": len(brute_best)==8,
        "each_knight_jump_has_three_microsteps": len(full_micro)==3*len(GRAY_KNIGHT_TOUR)==48,
        "first_two_microsteps_are_parallel_equal": first_two_equal_all,
        "last_microstep_is_perpendicular": last_perp_all,
        "landing_square_parity_flips_each_jump": landing_parity_flips,
        "micro_phases_are_balanced_Z3": dict(micro_phase_counts)=={0:16,1:16,2:16},
        "coil_ternary_lift_has_24_microticks": len(coil_micro)==24==M_R,
        "full_ternary_lift_has_48_microticks": len(full_micro)==48==REYE_INCIDENCES,
        "triangular_embedding_residues_are_0_3_4_7": residues==[0,3,4,7],
        "W33_residue_packet_is_0_q_chi_phi6": [0,Q,CHI,PHI6]==residues,
        "K3_K4_K7_K12_genera": genus_values[3]==0 and genus_values[4]==0 and genus_values[7]==1 and genus_values[12]==6,
        "K12_genus_is_g2": genus_values[12]==G2,
        "WE6_factorization_survives": WE6==V_W33*16*H1,
    }
    return {
        "theorem":"Ternary_Knight_Snake_Genus_Lift",
        "binary_router_layer":{
            "full_gray_cycle_vertices":16,
            "full_gray_flip_sequence":gray_flip_sequence_from_squares(GRAY_KNIGHT_TOUR),
            "is_hamiltonian_gray_cycle":checks["full_gray_cycle_is_Q4_hamilton_cycle"],
            "is_induced_snake_or_coil":False,
            "correction":"full 16-cycle is a router clock, not a snake-in-the-box error-detecting coil"
        },
        "ternary_knight_microgeometry":{
            "rule":"each macro knight edge is subdivided into three unit steps (straight, straight, perpendicular)",
            "include_start_square_count":4,
            "reuse_previous_landing_count":3,
            "full_gray_macro_edges":16,
            "full_gray_microticks":len(full_micro),
            "micro_phase_counts_Z3":dict(micro_phase_counts),
            "first_two_equal":first_two_equal_all,
            "last_perpendicular":last_perp_all,
            "landing_parity_flips":landing_parity_flips,
            "sample_micro_records":full_micro[:9]
        },
        "snake_coil_layer":{
            "explicit_Q4_coil":Q4_COIL,
            "coil_squares_on_toroidal_board":coil_squares,
            "coil_length":len(Q4_COIL),
            "bruteforce_max_Q4_coil_length":len(brute_best),
            "coil_ternary_microticks":len(coil_micro),
            "interpretation":"Q4 coil length 8 is the error-detecting induced cycle; ternary lift gives 24 microticks = m_r"
        },
        "triangular_genus_layer":{
            "formula":"g(K_n)=((n-3)(n-4))/12 when triangular embedding exists",
            "allowed_residues_mod12":residues,
            "W33_residue_packet":"0,q,chi,Phi6 = 0,3,4,7",
            "key_genera":genus_values,
            "interpretation":"triangle is minimal closure q=3; tetrahedron is chi=4 simplex closure; K7 gives torus genus 1; K12 gives genus g2=6"
        },
        "information_geometry_summary":{
            "endpoint_skeleton":"binary Q4 / toroidal knight graph",
            "edge_fiber":"ternary Z3 three-step knight word",
            "protected_subclock":"snake/coil induced Q4 8-cycle, ternary length 24",
            "surface_closure":"complete graph triangular residues 0,3,4,7 mod 12",
            "W33_factorization":"51840 = 40 * 16 * 81 still supplies anchor/router/phase-frame count"
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_ternary_knight_snake_genus_lift.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"binary_router_layer":payload["binary_router_layer"],"ternary_knight_microgeometry":payload["ternary_knight_microgeometry"],"snake_coil_layer":payload["snake_coil_layer"],"triangular_genus_layer":payload["triangular_genus_layer"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
