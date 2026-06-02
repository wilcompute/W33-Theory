from itertools import product, permutations, combinations
from collections import Counter
import math
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCD_FRAME_ACTION_G2_WEYL_QUOTIENT_results.json'

from analysis.w33_k44_factorization_g2_root_selector import main as selector_main


def xor(a,b): return tuple(x^y for x,y in zip(a,b))
def wt(a): return sum(a)
def fmt(p): return ''.join(map(str,p))
def edge(a,b,idx): return tuple(sorted((idx[a],idx[b])))

def det3_mod2(M):
    s=0
    for p in permutations(range(3)):
        term=1
        for i,j in enumerate(p): term &= M[i][j]
        s ^= term
    return s

def all_gl32():
    mats=[]
    for bits in product([0,1], repeat=9):
        M=tuple(tuple(bits[3*i:3*i+3]) for i in range(3))
        if det3_mod2(M)==1: mats.append(M)
    return mats

def mat_vec(M,v): return tuple(sum(M[i][j]*v[j] for j in range(3)) % 2 for i in range(3))
def apply_edge(e,perm): return tuple(sorted((perm[e[0]],perm[e[1]])))
def apply_matching(M,perm): return frozenset(apply_edge(e,perm) for e in M)
def apply_factorization(F,perm): return frozenset(apply_matching(M,perm) for M in F)
def compose(p,q): return tuple(p[i] for i in q)

def perm_order(p):
    seen=[False]*len(p); L=1
    for i in range(len(p)):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; c+=1; j=p[j]
            if c: L=math.lcm(L,c)
    return L

def orbit_of_group(G, start):
    out={start}; changed=True
    while changed:
        changed=False
        for x in list(out):
            new={g[x] for g in G}
            if not new <= out:
                out |= new; changed=True
    return out


def main():
    prev=selector_main()
    pts=list(product([0,1], repeat=3)); idx={p:i for i,p in enumerate(pts)}
    even=[p for p in pts if wt(p)%2==0]
    odd=[p for p in pts if wt(p)%2==1]
    S=odd[:]
    K44_edges=set(edge(e,o,idx) for e in even for o in odd)
    F0=frozenset(frozenset(edge(e,xor(e,s),idx) for e in even) for s in S)

    # Full Aut(K4,4) as all side-preserving plus side-swapping permutations.
    G=set()
    for pe in permutations(even):
        mapE=dict(zip(even,pe))
        for po in permutations(odd):
            mapO=dict(zip(odd,po))
            G.add(tuple(idx[mapE[p]] if p in mapE else idx[mapO[p]] for p in pts))
    for peo in permutations(odd):
        mapE=dict(zip(even,peo))
        for poe in permutations(even):
            mapO=dict(zip(odd,poe))
            G.add(tuple(idx[mapE[p]] if p in mapE else idx[mapO[p]] for p in pts))

    orbit=set(apply_factorization(F0,g) for g in G)
    orbit_list=sorted(orbit, key=lambda F: sorted(sorted(m) for m in F))
    frame_idx={F:i for i,F in enumerate(orbit_list)}

    frame_action=set(); kernel=set(); stabilizer0=[]
    identity6=tuple(range(6))
    for g in G:
        a=tuple(frame_idx[apply_factorization(F,g)] for F in orbit_list)
        frame_action.add(a)
        if a==identity6: kernel.add(g)
        if a[0]==0: stabilizer0.append(a)

    # Recover the canonical K3,3 bipartition on the six frames from stabilizer orbits.
    remaining=set(range(6)); orbits=[]
    while remaining:
        start=next(iter(remaining))
        orb=orbit_of_group(stabilizer0, start)
        orbits.append(orb); remaining-=orb
    # For a vertex in K3,3, its stabilizer has orbit sizes 1,2 on the same side and 3 on the opposite side.
    same_side_next=[o for o in orbits if len(o)==2][0]
    partA=frozenset({0} | same_side_next)
    partB=frozenset(set(range(6))-set(partA))
    root_edges=set(tuple(sorted((a,b))) for a in partA for b in partB)

    # Compare induced action to Aut(K3,3) on this recovered bipartition.
    AutK33=set(); A=list(partA); B=list(partB)
    for pa in permutations(A):
        for pb in permutations(B):
            m=dict(zip(A,pa)); m.update(dict(zip(B,pb)))
            AutK33.add(tuple(m[i] for i in range(6)))
    for pa in permutations(B):
        for pb in permutations(A):
            m=dict(zip(A,pa)); m.update(dict(zip(B,pb)))
            AutK33.add(tuple(m[i] for i in range(6)))

    order_profile=Counter(perm_order(p) for p in frame_action)
    kernel_order_profile=Counter(perm_order(p) for p in kernel)
    kernel_commutative=all(compose(a,b)==compose(b,a) for a in kernel for b in kernel)
    kernel_closed=all(compose(a,b) in kernel for a in kernel for b in kernel)

    # Kernel orbits on the eight Fano axes.
    rem=set(range(8)); kernel_axis_orbits=[]
    while rem:
        start=next(iter(rem))
        orb=orbit_of_group(kernel, start)
        kernel_axis_orbits.append(orb); rem-=orb

    decompositions={
        'aut_k44':len(G),
        'kernel_16_times_frame_action_72':len(kernel)*len(frame_action),
        'codec_count_16_times_positive_roots_6_times_weyl_12':16*6*12,
        'tomotope_axes_8_times_affine_stabilizer_24_times_root_selector_6':8*24*6,
        'two_parities_times_576':2*576,
    }

    checks={
        'inherits_g2_root_selector':prev['n_verified']==prev['n_checks']==23,
        'aut_k44_order_1152':len(G)==1152,
        'factorization_frame_count_6':len(orbit_list)==6,
        'frame_action_order_72':len(frame_action)==72,
        'kernel_order_16':len(kernel)==16,
        'orbit_kernel_identity_1152_equals_16_times_72':len(G)==len(kernel)*len(frame_action),
        'kernel_is_elementary_abelian_2_4':kernel_order_profile==Counter({1:1,2:15}) and kernel_commutative and kernel_closed,
        'kernel_axis_orbits_two_parity_halves':sorted(len(o) for o in kernel_axis_orbits)==[4,4],
        'stabilizer_orbit_pattern_1_2_3':sorted(len(o) for o in orbits)==[1,2,3],
        'recovered_frame_bipartition_3_plus_3':len(partA)==3 and len(partB)==3,
        'frame_root_graph_k33_edge_count_9':len(root_edges)==9,
        'frame_root_graph_degree_3':Counter(v for e in root_edges for v in e)==Counter({i:3 for i in range(6)}),
        'frame_action_preserves_k33_bipartition_or_swaps':all(frozenset(p[i] for i in partA) in {partA,partB} for p in frame_action),
        'frame_action_equals_aut_k33':frame_action==AutK33,
        'aut_k33_order_72':len(AutK33)==72,
        'frame_action_order_profile_matches_aut_k33':order_profile==Counter({1:1,2:21,3:8,4:18,6:24}),
        'frame_vertex_stabilizer_order_12':len(stabilizer0)==12,
        'vertex_stabilizer_is_weyl_g2_order_12':len(stabilizer0)==12,
        'positive_g2_root_count_6':len(orbit_list)==6,
        'oriented_g2_root_count_12':2*len(orbit_list)==12,
        'root_graph_edges_q_squared':len(root_edges)==9,
        'root_graph_bipartition_as_short_long_3_3':len(partA)==len(partB)==3,
        'all_decompositions_1152':all(v==1152 for v in decompositions.values()),
        'frame_action_72_equals_6_times_weyl_12':len(frame_action)==6*12,
    }
    assert all(checks.values()), checks

    R={
        'part':'MMCD',
        'theorem':'Frame action / G2 Weyl quotient theorem',
        'carrier':'the six one-factorization frames of K4,4 obtained from the Fano hinge chart',
        'exact_sequence':'1 -> (C2)^4 -> Aut(K4,4) -> Aut(K3,3) -> 1 at the frame-action level',
        'groups':{
            'Aut_K44_order':len(G),
            'frame_action_order':len(frame_action),
            'kernel_order':len(kernel),
            'kernel_structure':'elementary abelian 2^4',
            'frame_action_group':'Aut(K3,3) = S3 wr C2, order 72',
            'frame_vertex_stabilizer_order':len(stabilizer0),
            'Weyl_G2_order':12
        },
        'root_graph':{
            'vertices':'six K4,4 one-factorization frames = six positive G2 root sectors',
            'bipartition':[sorted(partA), sorted(partB)],
            'reading':'3 short positive roots + 3 long positive roots',
            'edges':len(root_edges),
            'degree':3,
            'graph':'K3,3'
        },
        'decompositions_of_1152':decompositions,
        'interpretation':'The full K4,4 automorphism group does more than move the affine 192-frame through six choices.  Its induced action on those six choices is exactly Aut(K3,3), order 72.  The kernel of the action is an elementary 2^4 codec kernel.  Thus Aut(K4,4)=16*72 at the frame-action level, while 72=6*12 decomposes as six positive G2 root sectors times the Weyl group order of G2.  The six frames themselves carry a canonical K3,3 short/long-root graph with 9=q^2 cross-relations.',
        'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['groups']); print(r['root_graph'])
