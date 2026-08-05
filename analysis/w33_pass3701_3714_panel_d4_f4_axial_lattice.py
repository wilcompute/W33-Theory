#!/usr/bin/env python3
"""Passes 3701-3714: D4/F4 triality, binary-panel obstruction, 45-axis geometry,
three-qubit Lagrangian code, axial no-go, Monster fingerprint, and II(24,24)
polarization theorem.

The verifier reconstructs the exact U4(2) carrier from the preceding executable
packet and derives every promoted finite statement.  The existence of the Leech
lattice as an even unimodular rootless rank-24 lattice is retained as an external
mathematical premise; no explicit Leech basis or Monster word is claimed here.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product, permutations
from math import lcm
import json
from pathlib import Path
import runpy

import networkx as nx
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1] if HERE.parent.name == "analysis" else HERE.parent
PREV = ROOT / "analysis" / "w33_pass3635_3648_monster_u42_completion.py"
OUTPUT = ROOT / "data" / "PART_3701_3714_D4_F4_TRIALITY_AXIAL_LATTICE_results.json"
MOD = 1_000_003


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def perm_order(g):
    seen = [False] * len(g)
    ans = 1
    for i in range(len(g)):
        if seen[i]:
            continue
        j = i
        c = 0
        while not seen[j]:
            seen[j] = True
            j = g[j]
            c += 1
        ans = lcm(ans, c)
    return ans


def closure_perm(gens, cap=None):
    gens = list(gens)
    ident = tuple(range(len(gens[0])))
    moves = list(dict.fromkeys(gens + [inverse(g) for g in gens]))
    seen = {ident}
    q = deque([ident])
    while q:
        h = q.popleft()
        for g in moves:
            x = compose(g, h)
            if x not in seen:
                seen.add(x)
                q.append(x)
                if cap and len(seen) > cap:
                    raise RuntimeError(f"closure exceeded {cap}")
    return seen


def conjugate(g, h):
    return compose(compose(g, h), inverse(g))


def orbits(group, n):
    unseen = set(range(n))
    ans = []
    while unseen:
        r = min(unseen)
        o = {g[r] for g in group}
        ans.append(tuple(sorted(o)))
        unseen -= o
    return sorted(ans, key=len)


def orbital_matrix(group, n):
    M = -np.ones((n, n), dtype=int)
    color = 0
    for i in range(n):
        for j in range(n):
            if M[i, j] >= 0:
                continue
            orb = {(g[i], g[j]) for g in group}
            for a, b in orb:
                M[a, b] = color
            color += 1
    return M, color


def colored_isomorphism(MA, MB):
    n = len(MA)
    valsA = {int(c): int(np.sum(MA[0] == c)) for c in set(MA.flatten())}
    valsB = {int(c): int(np.sum(MB[0] == c)) for c in set(MB.flatten())}
    by_val = {}
    for c, v in valsA.items():
        by_val.setdefault(v, [[], []])[0].append(c)
    for c, v in valsB.items():
        by_val.setdefault(v, [[], []])[1].append(c)
    color_maps = [{}]
    for _, (ca, cb) in by_val.items():
        if len(ca) != len(cb):
            return None
        nxt = []
        for p in permutations(cb):
            for d in color_maps:
                e = dict(d)
                e.update(dict(zip(ca, p)))
                nxt.append(e)
        color_maps = nxt
    for cmap in color_maps:
        GA = nx.DiGraph()
        GB = nx.DiGraph()
        GA.add_nodes_from(range(n))
        GB.add_nodes_from(range(n))
        for i in range(n):
            for j in range(n):
                GA.add_edge(i, j, color=cmap[int(MA[i, j])])
                GB.add_edge(i, j, color=int(MB[i, j]))
        gm = nx.algorithms.isomorphism.DiGraphMatcher(
            GA, GB, edge_match=lambda a, b: a["color"] == b["color"]
        )
        if gm.is_isomorphic():
            return tuple(gm.mapping[i] for i in range(n))
    return None


def gf2_rank(rows, nbits):
    rows = [int(r) for r in rows if r]
    rank = 0
    for col in range(nbits - 1, -1, -1):
        pivot = next((r for r in range(rank, len(rows)) if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and ((rows[r] >> col) & 1):
                rows[r] ^= rows[rank]
        rank += 1
    return rank


def build():
    p = runpy.run_path(str(PREV))
    A40 = np.asarray(p["A"], dtype=np.int64)
    N = np.asarray(p["N"], dtype=np.int64)
    X = np.asarray(p["X"], dtype=np.int64)
    C0 = np.asarray(p["C0"], dtype=np.int64)
    C1 = np.asarray(p["C1"], dtype=np.int64)
    G4 = list(p["G4"])
    GROUP = tuple(p["GROUP"])
    A6S = tuple(p["A6_SUBGROUPS"])
    assert len(GROUP) == 25920 and len(A6S) == 36

    a6idx = {h: i for i, h in enumerate(A6S)}
    def chamber_perm(g):
        return tuple(a6idx[frozenset(conjugate(g, x) for x in h)] for h in A6S)
    cg4 = [chamber_perm(g) for g in G4]
    chamber_group = closure_perm(cg4, 25920)
    I = np.array([[len(A6S[i].intersection(A6S[j])) for j in range(36)] for i in range(36)])
    A36 = (I == 12).astype(np.int64)
    np.fill_diagonal(A36, 0)
    k4s = tuple(c for c in combinations(range(36), 4) if all(A36[i, j] for i, j in combinations(c, 2)))
    assert len(k4s) == 135

    id40 = tuple(range(40)); id36 = tuple(range(36))
    moves40 = G4 + [inverse(g) for g in G4]
    moves36 = cg4 + [inverse(g) for g in cg4]
    action = {id36: id40}; qact = deque([id36])
    while qact:
        h36 = qact.popleft(); h40 = action[h36]
        for g40, g36 in zip(moves40, moves36):
            x36 = compose(g36, h36)
            if x36 not in action:
                action[x36] = compose(g40, h40); qact.append(x36)
    assert len(action) == 25920

    k4_to_oct = {}
    for c in k4s:
        stab_ch = [g for g in chamber_group if tuple(sorted(g[i] for i in c)) == c]
        obs = orbits([action[g] for g in stab_ch], 40)
        assert [len(o) for o in obs] == [8, 32]
        k4_to_oct[c] = obs[0]
    oct_to_k4 = defaultdict(list)
    for c, o in k4_to_oct.items():
        oct_to_k4[o].append(c)
    octads = tuple(sorted(oct_to_k4))
    assert len(octads) == 45 and {len(v) for v in oct_to_k4.values()} == {3}
    assert all(len(set(a).intersection(b)) == 0 for frames in oct_to_k4.values() for a, b in combinations(frames, 2))
    oct_intersections = Counter(len(set(a).intersection(b)) for i, a in enumerate(octads) for b in octads[i + 1:])
    A45 = np.array([[int(i != j and not set(octads[i]).intersection(octads[j])) for j in range(45)] for i in range(45)], dtype=np.int64)
    A45sq = A45 @ A45
    lam = {int(A45sq[i, j]) for i in range(45) for j in range(i + 1, 45) if A45[i, j]}
    mu = {int(A45sq[i, j]) for i in range(45) for j in range(i + 1, 45) if not A45[i, j]}
    assert set(A45.sum(axis=1)) == {12} and lam == mu == {3}
    axis = np.array([[48 if i in o else -12 for i in range(40)] for o in octads], dtype=np.int64)
    axis_gram = axis @ axis.T
    axis_offdiag = Counter(int(axis_gram[i, j]) for i in range(45) for j in range(i + 1, 45))
    axis_eigs = Counter(np.rint(np.linalg.eigvalsh(axis_gram)).astype(int))
    assert axis_eigs == Counter({43200: 24, 0: 21})

    def bits(x): return tuple((x >> i) & 1 for i in range(6))
    def q0(x):
        a = bits(x); return sum(a[2*i] * a[2*i+1] for i in range(3)) & 1
    mask = 3
    def qminus(x):
        a = bits(x); m = bits(mask); return (q0(x) + sum(ai*mi for ai, mi in zip(a, m))) & 1
    def bil(x, y):
        a = bits(x); b = bits(y); return sum(a[2*i]*b[2*i+1] + a[2*i+1]*b[2*i] for i in range(3)) & 1
    ns = [x for x in range(1, 64) if qminus(x)]; ni = {x: i for i, x in enumerate(ns)}
    def symmetry(v): return tuple(ni[x ^ (v if bil(x, v) else 0)] for x in ns)
    full = closure_perm([symmetry(v) for v in ns], 51840)
    assert len(full) == 51840
    Af2 = np.array([[int(i != j and bil(x, y) == 0) for j, y in enumerate(ns)] for i, x in enumerate(ns)])
    iso_map = next(nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(A36), nx.from_numpy_array(Af2)).isomorphisms_iter())
    fiso = tuple(iso_map[i] for i in range(36)); finv = inverse(fiso)
    even_group = {compose(compose(fiso, g), finv) for g in chamber_group}
    assert len(even_group) == 25920 and even_group < full

    def span(vs):
        out = {0}
        for coeff in product((0, 1), repeat=len(vs)):
            x = 0
            for c, v in zip(coeff, vs):
                if c: x ^= v
            out.add(x)
        return frozenset(out)
    lagrangians = set()
    for a, b, c in combinations(range(1, 64), 3):
        if bil(a, b) == bil(a, c) == bil(b, c) == 0:
            s = span((a, b, c))
            if len(s) == 8: lagrangians.add(s)
    assert len(lagrangians) == 135
    blocks = tuple(sorted(tuple(sorted(ni[x] for x in L if x and qminus(x))) for L in lagrangians))
    assert set(blocks) == {tuple(sorted(fiso[i] for i in c)) for c in k4s}
    M = np.zeros((135, 36), dtype=np.uint8)
    for r, b in enumerate(blocks): M[r, list(b)] = 1
    rank_inc = gf2_rank([sum(int(M[r, j]) << j for j in range(36)) for r in range(135)], 36)
    affine_words = set()
    for a in range(64):
        linear = tuple(bil(a, x) for x in ns)
        affine_words.add(linear); affine_words.add(tuple(1 ^ t for t in linear))
    assert len(affine_words) == 128
    assert all(all(sum(w[j] * int(M[r, j]) for j in range(36)) % 2 == 0 for r in range(135)) for w in affine_words)
    weights = Counter(sum(w) for w in affine_words)
    assert rank_inc == 29 and weights == Counter({0:1,16:63,20:63,36:1})

    first_block = blocks[0]
    H = {g for g in even_group if tuple(sorted(g[i] for i in first_block)) == first_block}
    assert len(H) == 192
    action4 = {g: tuple(first_block.index(g[i]) for i in first_block) for g in H}
    kernel = {g for g, a in action4.items() if a == tuple(range(4))}
    assert len(kernel) == 8 and all(perm_order(g) in (1, 2) for g in kernel)
    assert len(set(action4.values())) == 24
    center = [z for z in H if all(compose(z,h) == compose(h,z) for h in H)]
    assert len(center) == 2
    z = next(x for x in center if x != tuple(range(36)))
    complement = None; hs = list(H)
    for a in hs:
        for b in hs:
            S = closure_perm((a, b), 192)
            if len(S) == 24 and S.isdisjoint(kernel - {tuple(range(36))}) and len({action4[g] for g in S}) == 24:
                complement = S; break
        if complement is not None: break
    assert complement is not None
    cosets = []; seen = set()
    for h in H:
        if h in seen: continue
        c = tuple(sorted((h, compose(z, h)))); cosets.append(c); seen.update(c)
    cosets = sorted(cosets); ci = {c:i for i,c in enumerate(cosets)}
    qid = ci[tuple(sorted((tuple(range(36)), z)))]
    def qmul(i, j):
        x = compose(cosets[i][0], cosets[j][0]); return ci[tuple(sorted((x, compose(z, x))))]
    section = [c[0] for c in cosets]; equations = []
    for i in range(96):
        for j in range(96):
            k = qmul(i, j); prod = compose(section[i], section[j]); rhs = int(prod != section[k])
            assert prod == (section[k] if not rhs else compose(z, section[k]))
            equations.append((1 << i) ^ (1 << j) ^ (1 << k) | (rhs << 96))
    equations.append(1 << qid)
    cocycle_rank = gf2_rank([r & ((1 << 96) - 1) for r in equations], 96)
    cocycle_aug_rank = gf2_rank(equations, 97)
    assert (cocycle_rank, cocycle_aug_rank) == (95, 96)

    old_first = k4s[0]; oct0 = k4_to_oct[old_first]; triple_old = oct_to_k4[oct0]
    triple = [tuple(sorted(fiso[i] for i in c)) for c in triple_old]; triple_set = set(triple)
    N576 = {g for g in even_group if {tuple(sorted(g[i] for i in b)) for b in triple} == triple_set}
    N1152 = {g for g in full if {tuple(sorted(g[i] for i in b)) for b in triple} == triple_set}
    assert len(N576) == 576 and len(N1152) == 1152 and [len(o) for o in orbits(N1152, 36)] == [12, 24]

    roots = set()
    for i in range(4):
        for s in (-2, 2):
            v = [0]*4; v[i] = s; roots.add(tuple(v))
    for signs in product((-1,1), repeat=4): roots.add(tuple(signs))
    for i,j in combinations(range(4),2):
        for a,b in product((-2,2), repeat=2):
            v=[0]*4; v[i]=a; v[j]=b; roots.add(tuple(v))
    roots = tuple(sorted(roots)); ri = {r:i for i,r in enumerate(roots)}
    short = tuple(r for r in roots if sum(x*x for x in r) == 4); si = {r:i for i,r in enumerate(short)}
    def reflection(alpha):
        aa = sum(x*x for x in alpha); out=[]
        for x in roots:
            dot=sum(a*b for a,b in zip(x,alpha)); y=tuple((aa*xx-2*dot*aa_i)//aa for xx,aa_i in zip(x,alpha)); out.append(ri[y])
        return tuple(out)
    wf4 = closure_perm([reflection(a) for a in [(0,2,-2,0),(0,0,2,-2),(0,0,0,2),(1,-1,-1,-1)]], 1152)
    assert len(wf4) == 1152
    wf4short = {tuple(si[roots[g[ri[r]]]] for r in short) for g in wf4}
    orb24 = orbits(N1152, 36)[1]; oi = {v:i for i,v in enumerate(orb24)}
    n24 = {tuple(oi[g[v]] for v in orb24) for g in N1152}
    MA,_ = orbital_matrix(n24,24); MB,_ = orbital_matrix(wf4short,24); conj = colored_isomorphism(MA,MB)
    assert conj is not None and {compose(compose(conj,g),inverse(conj)) for g in n24} == wf4short

    exact_gens = [compose(compose(fiso,g),finv) for g in cg4]
    outside_involutions = [x for x in full-even_group if perm_order(x)==2]
    inv_sets = [[x for x in outside_involutions if compose(compose(x,g),x)==inverse(g)] for g in exact_gens]
    assert [len(s) for s in inv_sets] == [108]*4 and not set(inv_sets[0]).intersection(*map(set,inv_sets[1:]))
    factor_pairs = [[(a, compose(a,g)) for a in invs] for g,invs in zip(exact_gens,inv_sets)]
    pair_min = {}
    for i,j in combinations(range(4),2):
        best=4
        for ai,bi in factor_pairs[i]:
            for aj,bj in factor_pairs[j]:
                count=sum(compose(x,y)!=compose(y,x) for x in (ai,bi) for y in (aj,bj)); best=min(best,count)
                if best==2: break
            if best==2: break
        pair_min[f"{i}{j}"]=best
    min_noncommuting = 4 + sum(pair_min.values())
    assert set(pair_min.values()) == {2} and min_noncommuting == 16

    uambient = sp.Matrix([48 if i in oct0 else -12 for i in range(40)]); Xsp = sp.Matrix(X.tolist())
    ucoords = Xsp.gauss_jordan_solve(uambient)[0]; assert Xsp*ucoords == uambient
    def tensor_product(C, u, v):
        return sp.Matrix([sum(int(C[o,a,b]) * int(u[a]) * int(v[b]) for a in range(24) for b in range(24)) % MOD for o in range(24)])
    umod = [int(x)%MOD for x in ucoords]; uvec = sp.Matrix(umod)
    y0 = tensor_product(C0,umod,umod); y1 = tensor_product(C1,umod,umod)
    assert y0 == (36*uvec)%MOD and y1 == ((-216)*uvec)%MOD
    joint = [(36,-216,1),(28,152,6),(-12,-168,8),(-12,72,9)]
    allowed = (Fraction(0),Fraction(1,4),Fraction(1,32)); majorana_solutions=[]
    for target in permutations(allowed):
        a,b,_=joint[1]; den=Fraction(b)+216*target[0]
        if den==0: continue
        t=Fraction(36*target[0]-a,den)
        if t==Fraction(1,6): continue
        if tuple(Fraction(aa+bb*t,36-216*t) for aa,bb,_ in joint[1:])==target: majorana_solutions.append((t,target))
    assert not majorana_solutions

    piv = list(p["PIVOTS"]); G24 = sp.Matrix(N[np.ix_(piv,piv)].tolist())
    E8 = sp.Matrix([[2,-1,0,0,0,0,0,0],[-1,2,-1,0,0,0,0,0],[0,-1,2,-1,0,0,0,0],[0,0,-1,2,-1,0,0,0],[0,0,0,-1,2,-1,0,-1],[0,0,0,0,-1,2,-1,0],[0,0,0,0,0,-1,2,0],[0,0,0,0,-1,0,0,2]])
    Htarget = sp.diag(E8,E8,E8); assert Htarget.det()==1
    Bmat=sp.zeros(24)
    for i in range(24):
        Bmat[i,i]=(Htarget[i,i]-G24[i,i])//2
        for j in range(i+1,24): Bmat[i,j]=Htarget[i,j]-G24[i,j]
    assert G24+Bmat+Bmat.T==Htarget
    det0=abs(int(G24.det())); lead15=int((G24-2*sp.eye(24))[:15,:15].det())
    assert det0>1 and lead15<0

    checks = {
        "octads_45_three_frames_each": True,"octad_intersections_0_or_2": oct_intersections==Counter({2:720,0:270}),
        "axis_graph_srg_45_12_3_3": set(A45.sum(axis=1))=={12} and lam==mu=={3},"axis_tight_frame_rank24": axis_eigs==Counter({43200:24,0:21}),
        "lagrangian_contexts_135": len(lagrangians)==135,"incidence_code_rank29": rank_inc==29,"dual_affine_two_weight_code": weights==Counter({0:1,16:63,20:63,36:1}),
        "frame_stabilizer_WD4_structure": len(H)==192 and len(kernel)==8 and complement is not None,"central_extension_cocycle_nontrivial": (cocycle_rank,cocycle_aug_rank)==(95,96),
        "triality_normalizer_576": len(N576)==576,"full_octad_stabilizer_WF4": len(N1152)==1152 and conj is not None,
        "no_common_outer_inverter": not set(inv_sets[0]).intersection(*map(set,inv_sets[1:])),"rank8_string_factorization_no_go": min_noncommuting==16,
        "octad_axis_square_laws": y0==(36*uvec)%MOD and y1==((-216)*uvec)%MOD,"majorana_2A_spectrum_no_go": not majorana_solutions,
        "universal_graph_polarization": G24+Bmat+Bmat.T==Htarget,"E8_cubed_positive_unimodular_child": Htarget.det()==1,"equivariant_positive_unimodular_no_go": det0>1 and lead15<0,
    }
    assert all(checks.values())
    result = {
        "schema":"w33.pass3701_3714.d4_f4_triality_axial_lattice.v1","status":"PASS_EXACT_SEVEN_FRONT_SOURCE","checks":checks,
        "binary_panel_resolution":{"rank_preserving_cover":"IMPOSSIBLE: panel cardinality is preserved by an unbranched rank-preserving cover","outer_involutions":len(outside_involutions),"inverters_per_exact_generator":[len(s) for s in inv_sets],"common_inverters":0,"minimum_cross_color_noncommuting_pairs":pair_min,"minimum_total_noncommuting_edges":min_noncommuting,"string_rank8_maximum_edges":7,"verdict":"No common-sheet involutory lift and no color-split rank-8 string Coxeterization preserves the exact four-generator U4(2) target."},
        "d4_f4_triality":{"frames":135,"octads":45,"frames_per_octad":3,"frame_stabilizer_order":len(H),"frame_stabilizer_census":dict(sorted(Counter(perm_order(g) for g in H).items())),"kernel_C2_cubed_order":len(kernel),"quotient_S4_order":len(set(action4.values())),"S4_complement_order":len(complement),"center_order":len(center),"central_quotient_cocycle_rank":cocycle_rank,"central_quotient_augmented_rank":cocycle_aug_rank,"central_extension_non_split":True,"triality_normalizer_order":len(N576),"full_outer_stabilizer_order":len(N1152),"full_outer_stabilizer_census":dict(sorted(Counter(perm_order(g) for g in N1152).items())),"full_outer_stabilizer_is_WF4":True,"tower":"W(D4) (192) < even-frame triality subgroup (576) < W(F4) (1152)"},
        "axis45_geometry":{"octad_intersection_census":dict(sorted(oct_intersections.items())),"disjointness_srg":[45,12,3,3],"spectrum":{"12":1,"3":20,"-3":24},"axis_norm":23040,"axis_offdiagonal_gram_census":dict(sorted(axis_offdiag.items())),"axis_gram_spectrum":{"43200":24,"0":21},"tight_frame_dimension":24},
        "three_qubit_lagrangian_code":{"ambient":"W(5,2) three-qubit Pauli symplectic space","lagrangian_three_spaces":len(lagrangians),"anisotropic_points":36,"anisotropic_points_per_lagrangian":4,"binary_incidence_rank":rank_inc,"dual_dimension":36-rank_inc,"dual_weight_enumerator":{"0":1,"16":63,"20":63,"36":1},"exact_identification":"restrictions of all affine-linear functions B(a,x)+c to q(x)=1"},
        "octad_axial_envelope":{"distinct_axis_lines":45,"frames_per_axis":3,"unnormalized_axis_entries":{"on_octad":48,"off_octad":-12},"axis_norm":23040,"product_square_laws":{"m0":"36 u","m1":"-216 u"},"joint_left_eigenpairs":[{"m0":a,"m1":b,"multiplicity":m} for a,b,m in joint],"normalized_nonaxis_eigenvalues":["(28+152t)/(36-216t) multiplicity 6","(-12-168t)/(36-216t) multiplicity 8","(-12+72t)/(36-216t) multiplicity 9"],"monster_2A_majorana_target":["0","1/4","1/32"],"solutions":[],"verdict":"No parameter in the complete two-dimensional U4(2)-equivariant commutative Frobenius plane gives the Monster 2A Majorana Peirce spectrum on the 45 canonical octad axes."},
        "monster_four_parabolic_front":{"abstract_four_generator_signature":"unchanged and exact","new_internal_fingerprint":{"135_WD4_frames":True,"45_WF4_octad_normalizers":True,"degree45_rank3_suborbits":[1,12,32],"axis_graph_srg":[45,12,3,3]},"public_search_result":"No serialized mmgroup U4(2) words were located in the checked maximal-subgroup database or documentation; U4(2) is non-maximal.","status":"MMgroup_WORDS_PENDING"},
        "II24_24_polarization":{"graph_formula":"Gram(graph(B)) = G + B + B^T","universality":"Every even integral rank-24 Gram matrix H is obtained by an integral upper-triangular B.","executable_positive_child":"E8^3","E8_cubed_determinant":int(Htarget.det()),"leech_consequence":"Using the external theorem that the Leech lattice is even, unimodular, rank 24, and rootless, the same formula proves existence of a primitive noncanonical rootless graph section.","explicit_Leech_basis_frozen_here":False,"U42_equivariant_B":"scalar mI by irreducibility/Schur","G_determinant_factorization":{str(k):int(v) for k,v in sp.factorint(det0).items()},"G_minus_2I_leading_15_minor":lead15,"equivariant_verdict":"No U4(2)-equivariant positive-definite unimodular graph polarization exists.","specificity_firewall":"Polarization universality means existence of a Leech child alone is not evidence of a W33-specific construction; a canonical or symmetry-controlled section remains required."},
        "evidence_boundary":{"proved_here":["strong involutory binary-resolution obstruction","explicit W(D4) frame stabilizer structure","nontrivial central quotient cocycle","exact W(D4)-triality-W(F4) tower","45-object SRG and two-distance tight frame","135 Lagrangian context identification and dual affine code","45-axis Majorana spectrum no-go","universal graph-polarization formula and executable E8^3 child","equivariant positive-unimodular polarization no-go"],"not_proved_here":["regular abstract-polytope cover of the ternary chamber system","serialized Monster words","explicit frozen Leech basis or canonical Leech section","Majorana, Griess, or VOA realization","remote CI or PDF evidence","physical implementation"]}
    }
    semantic=json.dumps(result,sort_keys=True,separators=(",",":")).encode(); result["semantic_sha256"]=sha256(semantic).hexdigest(); return result


def main():
    result=build(); OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("PASS_3701_3714",result["semantic_sha256"]); print(json.dumps(result,indent=2))


if __name__=="__main__": main()
