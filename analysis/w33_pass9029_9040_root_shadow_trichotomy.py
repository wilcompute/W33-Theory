"""Passes 9029-9040 -- rank-24 W(3,3) root-shadow trichotomy.

This verifier starts from the three exact rank-24 carriers classified in Pass 8989-9012
and asks a new question: what do the *roots* of each Niemeier lattice look like after
projection to L/(I-X)L ~= F_3^4?

It independently reconstructs N(A2^12) from the extended ternary Golay code and checks
an explicit signed 3^4 monomial automorphism.  The E6^4 and E8^3 carriers are rebuilt
from their already-frozen repo witnesses.

The output is intentionally finite and exact.  It makes no physics claim.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
from sympy import Matrix, eye, zeros
from sympy.matrices.normalforms import hermite_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS9029_9040_ROOT_SHADOW_TRICHOTOMY.json"

A2 = Matrix([[2, -1], [-1, 2]])
E6 = Matrix([
    [2, 0, -1, 0, 0, 0],
    [0, 2, 0, -1, 0, 0],
    [-1, 0, 2, -1, 0, 0],
    [0, -1, -1, 2, -1, 0],
    [0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, -1, 2],
])
E8 = np.array([
    [2, 0, -1, 0, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0, 0],
    [0, 0, 0, -1, 2, -1, 0, 0],
    [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, 0, -1, 2],
], dtype=np.int64)

# Standard extended ternary Golay [12,6,6] generator (I6 | B).
GOLAY12 = np.array([
    [1,0,0,0,0,0, 1,1,1,1,1,0],
    [0,1,0,0,0,0, 1,1,2,2,0,2],
    [0,0,1,0,0,0, 1,2,1,0,2,2],
    [0,0,0,1,0,0, 2,1,0,1,2,2],
    [0,0,0,0,1,0, 2,0,1,2,1,2],
    [0,0,0,0,0,1, 0,2,2,1,1,2],
], dtype=np.int64)

# Explicit signed monomial Golay automorphism found in the Pass 8989-9012 search.
# Convention: source coordinate j maps to target PERM[j], multiplied by SIGN[j].
PERM = [5, 2, 4, 11, 1, 7, 3, 0, 9, 10, 8, 6]
SIGNS_MOD3 = [2,2,2,1,1,2,1,1,1,2,2,1]  # 2 = -1
CYCLES = [(7,0,5), (4,1,2), (8,9,10), (11,6,3)]


def rank_modp(a: np.ndarray, p: int = 3) -> int:
    a = np.array(a, dtype=np.int64) % p
    m, n = a.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if int(a[i,c]) % p), None)
        if piv is None:
            continue
        a[[r,piv]] = a[[piv,r]]
        a[r] = (a[r] * pow(int(a[r,c]), -1, p)) % p
        for i in range(m):
            if i != r and a[i,c] % p:
                a[i] = (a[i] - a[i,c] * a[r]) % p
        r += 1
        if r == m:
            break
    return r


def nullspace_modp(a: np.ndarray, p: int = 3) -> np.ndarray:
    a = np.array(a, dtype=np.int64) % p
    m, n = a.shape
    r = 0
    pivots = []
    for c in range(n):
        piv = next((i for i in range(r, m) if int(a[i,c]) % p), None)
        if piv is None:
            continue
        a[[r,piv]] = a[[piv,r]]
        a[r] = (a[r] * pow(int(a[r,c]), -1, p)) % p
        for i in range(m):
            if i != r and a[i,c] % p:
                a[i] = (a[i] - a[i,c] * a[r]) % p
        pivots.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in pivots]
    out = []
    for f in free:
        x = np.zeros(n, dtype=np.int64)
        x[f] = 1
        for rr, pc in enumerate(pivots):
            x[pc] = (-a[rr,f]) % p
        out.append(x)
    return np.array(out, dtype=np.int64)


def inv_mod(a: np.ndarray, p: int = 3) -> np.ndarray:
    a = np.array(a, dtype=np.int64) % p
    n = a.shape[0]
    aug = np.concatenate([a, np.eye(n, dtype=np.int64)], axis=1) % p
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if int(aug[i,c]) % p), None)
        if piv is None:
            raise ValueError("singular")
        aug[[r,piv]] = aug[[piv,r]]
        aug[r] = (aug[r] * pow(int(aug[r,c]), -1, p)) % p
        for i in range(n):
            if i != r and aug[i,c] % p:
                aug[i] = (aug[i] - aug[i,c] * aug[r]) % p
        r += 1
    return aug[:,n:] % p


def quotient_form(x: Matrix, gram: Matrix):
    """Return H: L -> F3^4 and the alternating form J in H-coordinates."""
    a = eye(x.rows) - x
    h = nullspace_modp(np.array(a.T.tolist(), dtype=np.int64), 3)
    assert h.shape == (4, x.rows)
    pmat = 3 * a.inv()
    assert all(v.q == 1 for v in pmat)
    f = pmat.T * gram
    assert f + f.T == 3 * gram
    fmod = np.array(f.tolist(), dtype=np.int64) % 3
    pivcols = None
    rinv = None
    for cols in itertools.combinations(range(x.rows), 4):
        try:
            rinv = inv_mod(h[:,cols], 3)
            pivcols = cols
            break
        except ValueError:
            pass
    assert pivcols is not None
    u = np.zeros((x.rows,4), dtype=np.int64)
    u[list(pivcols),:] = rinv
    assert np.array_equal((h @ u) % 3, np.eye(4, dtype=np.int64))
    j = (u.T @ fmod @ u) % 3
    assert rank_modp(j,3) == 4
    assert not ((j + j.T) % 3).any()
    assert all(int(j[i,i]) % 3 == 0 for i in range(4))
    return h, j


def projective(v):
    v = tuple(int(x) % 3 for x in v)
    if not any(v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % 3 for y in v)
    raise AssertionError


def projective_points_4():
    pts = set()
    for v in itertools.product(range(3), repeat=4):
        q = projective(v)
        if q is not None:
            pts.add(q)
    return sorted(pts)


def is_line(points, j):
    pts = [tuple(p) for p in points]
    if len(set(pts)) != 4:
        return False
    if rank_modp(np.array(pts, dtype=np.int64), 3) != 2:
        return False
    for a,b in itertools.combinations(pts,2):
        if int(np.array(a) @ j @ np.array(b)) % 3:
            return False
    return True


def root_shadow(root_vectors, h):
    ctr = Counter()
    for z in root_vectors:
        q = tuple(int(x) for x in (h @ (np.array(z,dtype=np.int64) % 3)) % 3)
        ctr[projective(q)] += 1
    return ctr


def e8_roots():
    found = {tuple(np.eye(8,dtype=np.int64)[i]) for i in range(8)}
    frontier = list(found)
    while frontier:
        nxt = []
        for vt in frontier:
            v = np.array(vt,dtype=np.int64)
            for i in range(8):
                w = v.copy()
                w[i] -= int(E8[i] @ v)
                tw = tuple(int(x) for x in w)
                if tw not in found:
                    found.add(tw)
                    nxt.append(tw)
        frontier = nxt
    roots = sorted(found | {tuple(-np.array(v)) for v in found})
    assert len(roots) == 240
    return roots


def e6_roots():
    roots = []
    g = np.array(E6.tolist(), dtype=np.int64)
    for v in itertools.product(range(-3,4), repeat=6):
        a = np.array(v,dtype=np.int64)
        if int(a @ g @ a) == 2:
            roots.append(v)
    assert len(roots) == 72
    return roots


def golay_codewords():
    words = set()
    for c in itertools.product(range(3), repeat=6):
        words.add(tuple((np.array(c,dtype=np.int64) @ GOLAY12) % 3))
    assert len(words) == 729
    return words


def build_a2_12():
    words = golay_codewords()
    weights = Counter(sum(x != 0 for x in w) for w in words)
    assert weights == Counter({9:440, 6:264, 12:24, 0:1})
    assert not ((GOLAY12 @ GOLAY12.T) % 3).any()

    t = np.zeros((12,12), dtype=np.int64)
    for src, dst in enumerate(PERM):
        t[dst,src] = SIGNS_MOD3[src] % 3
    assert all(tuple((t @ np.array(w,dtype=np.int64)) % 3) in words for w in words)
    assert np.array_equal(np.linalg.matrix_power(t,3) % 3, np.eye(12,dtype=np.int64))

    # N(A2^12) from A2^12 plus six Golay glue generators.
    omega1 = Matrix([Matrix([[2], [1]])[0]/3, Matrix([[2], [1]])[1]/3])
    gens = []
    for i in range(24):
        e = zeros(24,1); e[i] = 1; gens.append(e)
    for row in GOLAY12:
        v = zeros(24,1)
        for c in range(12):
            v[2*c:2*c+2,0] = int(row[c]) * omega1
        gens.append(v)
    m = Matrix.hstack(*gens)
    m3 = Matrix([[int(3*x) for x in m.row(i)] for i in range(24)])
    basis = hermite_normal_form(m3) / 3  # columns are a basis of N
    assert basis.det() == Matrix([[1]]).det()/729

    gamb = Matrix.diag(*([A2]*12))
    gram = basis.T * gamb * basis
    assert gram.det() == 1
    assert all(v.q == 1 for v in gram)
    assert all(int(gram[i,i]) % 2 == 0 for i in range(24))

    # Signed 3^4 permutation; one A2 Coxeter twist per component 3-cycle.
    r = Matrix([[0,-1],[1,-1]])
    assert r.T*A2*r == A2 and r**3 == eye(2)
    xamb = zeros(24)
    twist = {cyc[0] for cyc in CYCLES}
    for src, dst in enumerate(PERM):
        s = -1 if SIGNS_MOD3[src] == 2 else 1
        block = s * (r if src in twist else eye(2))
        xamb[2*dst:2*dst+2, 2*src:2*src+2] = block
    assert xamb.T*gamb*xamb == gamb
    assert xamb**9 == eye(24) and xamb**3 != eye(24)
    x = basis.inv()*xamb*basis
    assert all(v.q == 1 for v in x)
    assert x.T*gram*x == gram
    assert (eye(24)-x).det() == 81
    assert x**6 + x**3 + eye(24) == zeros(24)

    h,j = quotient_form(x,gram)
    roots = []
    per_component = {}
    binv = basis.inv()
    a2roots = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]
    for comp in range(12):
        local = []
        for pair in a2roots:
            amb = zeros(24,1)
            amb[2*comp] = pair[0]; amb[2*comp+1] = pair[1]
            z = binv*amb
            assert all(v.q == 1 for v in z)
            zv = [int(v) for v in z]
            roots.append(zv)
            q = projective((h @ (np.array(zv,dtype=np.int64)%3))%3)
            local.append(q)
        assert len(set(local)) == 1
        per_component[str(comp)] = local[0]
    shadow = root_shadow(roots,h)
    visible = sorted(q for q in shadow if q is not None)
    assert shadow.get(None,0) == 0
    assert Counter(shadow[q] for q in visible) == Counter({18:4})
    assert is_line(visible,j)
    cycle_points = []
    for cyc in CYCLES:
        qset = {per_component[str(c)] for c in cyc}
        assert len(qset) == 1
        cycle_points.append(next(iter(qset)))
    assert set(cycle_points) == set(visible)

    return {
        "golay": {"size":729, "dimension":6, "minimum_weight":6,
                  "weight_enumerator":{str(k):int(v) for k,v in sorted(weights.items())},
                  "self_dual_check":True},
        "monomial_witness":{"perm":PERM, "signs_mod3":SIGNS_MOD3,
                            "cycles":[list(c) for c in CYCLES],
                            "order_mod3":3, "preserves_golay":True},
        "lattice":{"det":1, "even":True, "root_count":72},
        "carrier":{"order":9, "det_I_minus_X":81, "phi9":True, "quotient_rank":4},
        "root_shadow":{"zero_roots":0, "visible_projective_points":4,
                       "multiplicity_per_point":18, "is_W33_line":True,
                       "component_cycles_are_line_points":True},
    }


def build_e6_4():
    w = Matrix(np.loadtxt(ROOT/"analysis"/"_e6_ord9.txt",dtype=np.int64).tolist())
    b = Matrix(np.loadtxt(ROOT/"analysis"/"_niemeier_e6_4_basis.txt",dtype=np.int64).tolist())
    gram = Matrix(np.loadtxt(ROOT/"analysis"/"_niemeier_e6_4_gram.txt",dtype=np.int64).tolist())
    mz = E6*w*E6.inv()
    a = zeros(24)
    for k in range(4):
        a[6*k:6*k+6,6*k:6*k+6] = mz
    x = b.T.inv()*a*b.T
    assert all(v.q == 1 for v in x)
    assert x.T*gram*x == gram
    assert (eye(24)-x).det() == 81
    assert x**6+x**3+eye(24)==zeros(24)
    h,j = quotient_form(x,gram)

    roots6 = e6_roots()
    binv = b.T.inv()
    roots = []
    zero_local_roots = []
    for comp in range(4):
        local_shadow = Counter()
        local_zero_simple = []
        for rv in roots6:
            amb = zeros(24,1)
            amb[6*comp:6*comp+6,0] = E6*Matrix(rv)
            z = binv*amb
            assert all(v.q == 1 for v in z)
            zv = [int(v) for v in z]
            roots.append(zv)
            q = projective((h @ (np.array(zv,dtype=np.int64)%3))%3)
            local_shadow[q] += 1
            if q is None:
                local_zero_simple.append(np.array(rv,dtype=np.int64))
        assert sorted(local_shadow.values()) == [18,54]
        zero_local_roots.append(local_zero_simple)

    shadow = root_shadow(roots,h)
    visible = sorted(q for q in shadow if q is not None)
    assert shadow[None] == 72
    assert Counter(shadow[q] for q in visible) == Counter({54:4})
    assert is_line(visible,j)

    # In each E6 component, the 18 quotient-zero roots form A2^3 exactly.
    e6g = np.array(E6.tolist(),dtype=np.int64)
    for zr in zero_local_roots:
        zset = {tuple(v) for v in zr}
        assert len(zset) == 18
        for aa in zr:
            for bb in zr:
                ip = int(aa @ e6g @ bb)
                assert tuple(bb - ip*aa) in zset
        adj = {i:set() for i in range(18)}
        for i,aa in enumerate(zr):
            for k,bb in enumerate(zr[i+1:], i+1):
                if int(aa @ e6g @ bb) != 0:
                    adj[i].add(k); adj[k].add(i)
        seen=set(); sizes=[]
        for i in range(18):
            if i in seen:
                continue
            todo=[i]; seen.add(i); n=0
            while todo:
                u=todo.pop(); n+=1
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v); todo.append(v)
            sizes.append(n)
        assert sorted(sizes) == [6,6,6]

    return {
        "lattice":{"det":1, "even":True, "root_count":288},
        "carrier":{"order":9, "det_I_minus_X":81, "phi9":True, "quotient_rank":4,
                   "mechanism":"diagonal W(E6)^4"},
        "root_shadow":{"zero_roots":72, "visible_projective_points":4,
                       "multiplicity_per_point":54, "is_W33_line":True,
                       "per_E6_component":"18 zero + 54 on one line point",
                       "zero_root_subsystem_per_component":"A2^3",
                       "total_zero_root_system":"A2^12"},
    }


def build_e8_3():
    roots8 = e8_roots()
    def refl(i):
        m = np.eye(8,dtype=np.int64)
        m[i,:] -= E8[i]
        return m
    cox = np.eye(8,dtype=np.int64)
    for i in range(8):
        cox = cox @ refl(i)
    j3 = np.linalg.matrix_power(cox,10)
    assert np.array_equal(np.linalg.matrix_power(j3,3),np.eye(8,dtype=np.int64))
    tau = np.zeros((24,24),dtype=np.int64)
    for i in range(3):
        tau[8*((i+1)%3):8*((i+1)%3)+8,8*i:8*i+8] = np.eye(8,dtype=np.int64)
    d = np.zeros((24,24),dtype=np.int64)
    d[:8,:8]=j3; d[8:16,8:16]=np.eye(8,dtype=np.int64); d[16:,16:]=np.eye(8,dtype=np.int64)
    g = tau @ d
    x = Matrix(g.tolist())
    gram = Matrix.diag(*([Matrix(E8.tolist())]*3))
    assert x.T*gram*x == gram
    assert x**9 == eye(24) and x**3 != eye(24)
    assert x**6+x**3+eye(24)==zeros(24)
    assert (eye(24)-x).det()==81
    h,j = quotient_form(x,gram)

    roots=[]
    for comp in range(3):
        local=[]
        for rv in roots8:
            z=np.zeros(24,dtype=np.int64)
            z[8*comp:8*comp+8]=np.array(rv,dtype=np.int64)
            roots.append(z)
            local.append(projective((h @ (z%3))%3))
        c=Counter(local)
        assert None not in c and len(c)==40 and set(c.values())=={6}
    shadow=root_shadow(roots,h)
    assert None not in shadow
    assert len(shadow)==40 and set(shadow.values())=={18}
    assert set(shadow) == set(projective_points_4())

    pts=projective_points_4()
    adj=np.zeros((40,40),dtype=np.int64)
    for i,a in enumerate(pts):
        for k,b in enumerate(pts):
            if i!=k and int(np.array(a)@j@np.array(b))%3==0:
                adj[i,k]=1
    assert set(adj.sum(axis=1).tolist())=={12}
    for i in range(40):
        for k in range(i+1,40):
            assert int((adj[i]&adj[k]).sum()) == (2 if adj[i,k] else 4)

    return {
        "lattice":{"det":1, "even":True, "root_count":720},
        "carrier":{"order":9, "det_I_minus_X":81, "phi9":True, "quotient_rank":4,
                   "mechanism":"3-cycle of E8 factors with one order-3 Coxeter twist"},
        "root_shadow":{"zero_roots":0, "visible_projective_points":40,
                       "multiplicity_per_point":18, "covers_all_W33_points":True,
                       "per_E8_factor":"all 40 points, 6 roots per point",
                       "graph_check":"SRG(40,12,2,4)"},
    }


def main():
    a2 = build_a2_12()
    e6 = build_e6_4()
    e8 = build_e8_3()
    out = {
        "theorem":"Rank-24 W(3,3) Root-Shadow Trichotomy",
        "boundary":(
            "VERIFIED for the three and only three rank-24 Niemeier carriers classified in "
            "Pass 8989-9012. E8^3 projects its 720 roots uniformly onto all 40 W33 points "
            "(18 roots/point). E6^4 has 72 quotient-zero roots forming A2^12 and projects "
            "the remaining 216 roots onto one W33 line (54 roots/point). A2^12 projects all "
            "72 roots onto one W33 line (18 roots/point). No physics inference is made."
        ),
        "E8^3":e8,
        "E6^4":e6,
        "A2^12":a2,
        "cross_carrier_bridge":{
            "E6_kernel_root_system_equals_third_carrier_root_system":"A2^12",
            "caution":(
                "This is an equality of root-system type inside N(E6^4), not an identification "
                "of the full Niemeier lattice N(A2^12) with a sublattice of N(E6^4)."
            ),
        },
        "visible_root_pairs_per_point":{"E8^3":9,"E6^4":27,"A2^12":9},
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
