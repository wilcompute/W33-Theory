"""TOE85: exact H27 action and radical filtration of TOE83's H2 face relations.

Works over F2 and F3. All results arise from the native oriented 99x135
boundary matrix and all 27 signed H27 face-chain automorphisms.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/w33_20261015_toe83_h27_square_css_surgery.json"


def rank_and_basis(vectors, p):
    """Independent row basis over a prime field, deterministic pivots."""
    pivots = {}
    for vector in vectors:
        w = [int(a) % p for a in vector]
        while True:
            j = next((i for i, x in enumerate(w) if x), None)
            if j is None:
                break
            if j in pivots:
                scale = w[j]
                w = [(a - scale * b) % p for a, b in zip(w, pivots[j])]
            else:
                inv = pow(w[j], -1, p)
                pivots[j] = [(inv * a) % p for a in w]
                break
    return [pivots[k] for k in sorted(pivots)]


def nullspace(matrix, p):
    """RREF-based nullspace of an m-by-n matrix, columns = 2-cells."""
    m, n = len(matrix), len(matrix[0])
    a = [[x % p for x in row] for row in matrix]
    pivots = []
    r = 0
    for c in range(n):
        t = next((i for i in range(r, m) if a[i][c]), None)
        if t is None:
            continue
        a[r], a[t] = a[t], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(inv * v) % p for v in a[r]]
        for i in range(m):
            if i == r or not a[i][c]:
                continue
            scale = a[i][c]
            a[i] = [(x - scale * y) % p for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    free = [j for j in range(n) if j not in set(pivots)]
    basis = []
    for f in free:
        v = [0] * n
        v[f] = 1
        for i, c in enumerate(pivots):
            v[c] = (-a[i][f]) % p
        assert all(sum(t * x for t, x in zip(row, v)) % p == 0 for row in matrix)
        basis.append(v)
    return basis, free, len(pivots)


def geometry():
    D = json.loads(SOURCE.read_text(encoding="utf-8"))
    reps = D["orbit_metadata"]["selected_orbit_representatives"]
    H = list(product(range(3), repeat=3))
    idx = {h:i for i,h in enumerate(H)}

    def mul(x, y):
        a,b,c=x; A,B,C=y
        return ((a+A)%3, (b+B)%3, (c+C-b*A)%3)

    directions = ((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    triangles = sorted({tuple(sorted(idx[mul(g,t)] for t in ((0,0,0), d, mul(d,d))))
                        for g in H for d in directions})
    edges = sorted({tuple(sorted(e)) for f in triangles for e in combinations(f,2)})
    assert (len(triangles), len(edges)) == (45, 135)
    edge_index = {e:i for i,e in enumerate(edges)}
    perms = [[idx[mul(g,h)] for h in H] for g in H]
    square_orbits = []
    for rep in reps:
        edge_set = [tuple(e) for e in rep]
        orbit = {tuple(sorted(tuple(sorted((perm[u], perm[v]))) for u,v in edge_set))
                 for perm in perms}
        assert len(orbit) == 27
        square_orbits.append(orbit)
    squares = sorted(square_orbits[0] | square_orbits[1])
    assert len(squares) == 54

    def walk_from_edges(es):
        ns = defaultdict(set)
        for u,v in es:
            ns[u].add(v); ns[v].add(u)
        assert len(ns) == 4 and all(len(x)==2 for x in ns.values())
        v = min(ns); u = min(ns[v]); walk = [v,u]
        while len(walk) < 4:
            walk.append(next(x for x in ns[walk[-1]] if x != walk[-2]))
        return walk + [v]

    def boundary(walk):
        row = [0] * len(edges)
        for u,v in zip(walk,walk[1:]):
            row[edge_index[tuple(sorted((u,v)))]] += 1 if u<v else -1
        return row

    rows = [boundary([a,b,c,a]) for a,b,c in triangles] + [
        boundary(walk_from_edges(s)) for s in squares
    ]
    face_index = {tuple(f):i for i,f in enumerate(triangles)}
    sq_index = {tuple(s):45+i for i,s in enumerate(squares)}
    actions = {}
    for g,perm in zip(H,perms):
        edge_dest = [edge_index[tuple(sorted((perm[u],perm[v])))] for u,v in edges]
        edge_sign = [1 if perm[u]<perm[v] else -1 for u,v in edges]
        dst,sgn = [],[]
        for i,row in enumerate(rows):
            if i < 45:
                j = face_index[tuple(sorted(perm[v] for v in triangles[i]))]
            else:
                j = sq_index[tuple(sorted(tuple(sorted((perm[u],perm[v]))) for u,v in squares[i-45]))]
            mapped = [0]*135
            for e,v in enumerate(row):
                if v:
                    mapped[edge_dest[e]] = v*edge_sign[e]
            target = rows[j]
            sign = 1 if mapped == target else -1
            assert mapped == [sign*t for t in target], (g,i,j)
            dst.append(j);sgn.append(sign)
        assert sorted(dst) == list(range(99))
        actions[g]=(dst,sgn)
    return H,rows,actions


def act(vector,action,p):
    dest,sign = action
    w = [0]*len(vector)
    for i,v in enumerate(vector):
        w[dest[i]] = v * sign[i] % p
    return w


def action_on_kernel(kernel, free, action, p):
    matrix = []
    for basis in kernel:
        image = act(basis, action, p)
        coeff = [image[j] for j in free]
        restored = [sum(coeff[k]*kernel[k][j] for k in range(len(coeff)))%p
                    for j in range(len(basis))]
        assert restored == image, "H27 must preserve H2 kernel"
        matrix.append(coeff)
    return matrix  # column-action; list of images of basis vectors


def apply(matrix, coeff, p):
    d=len(matrix)
    return [sum(coeff[i]*matrix[i][j] for i in range(d))%p for j in range(d)]


def certificate():
    H, faces, actions=geometry()
    boundary_matrix=[[faces[j][i] for j in range(99)] for i in range(135)]
    out = {"source":"TOE83 selected two H27 square-face orbits",
           "chain_dimensions":{"C2":99,"C1":135,"H2":16},
           "verified_signed_face_automorphisms":len(actions)}
    for p in (2,3):
        basis,free,rank=nullspace(boundary_matrix,p)
        assert rank==83 and len(basis)==16
        matrices={g:action_on_kernel(basis,free,action,p) for g,action in actions.items()}
        eye=[[int(i==j) for j in range(16)] for i in range(16)]
        assert matrices[(0,0,0)]==eye
        shifts={}
        for g,M in matrices.items():
            diff=[[(a-b)%p for a,b in zip(image, unit)]
                  for image,unit in zip(M,eye)]
            shifts[g]=len(rank_and_basis(diff,p))
        stats=Counter(str(rank) for rank in shifts.values())
        gens=((1,0,0),(0,1,0))
        combined=[]
        for i in range(16):
            combined.append([x for g in gens for x in
                             [(matrices[g][i][j]-int(i==j))%p for j in range(16)]])
        fixed=16-len(rank_and_basis(combined,p))
        # Verify the noncommutative representation law for all 729 pairs.
        for g in H:
            for h in H:
                a,b,c=g; A,B,C=h
                gh=((a+A)%3,(b+B)%3,(c+C-b*A)%3)
                assert all(apply(matrices[g], matrices[h][i],p)==matrices[gh][i]
                           for i in range(16))
        report={"boundary_rank":rank,"dimension":len(basis),
                "rank_g_minus_identity_distribution":dict(sorted(stats.items())),
                "H27_fixed_dimension":fixed,
                "center_generator_rank":shifts[(0,0,1)],
                "generators":[list(g) for g in gens],
                "elements":[{"h":list(g),"rank_g_minus_identity":shifts[g]} for g in H]}
        if p == 2:
            # Maschke projectors: 3 = 9 = 27 = 1 in F2, so subgroup
            # sums are exact idempotents, without division factors.
            def projector(subgroup):
                return [[sum(matrices[g][i][j] for g in subgroup) % 2
                         for j in range(16)] for i in range(16)]
            z = [(0,0,c) for c in range(3)]
            Pz = projector(z)
            Pall = projector(H)
            assert len(rank_and_basis(Pz,2)) == 10
            assert len(rank_and_basis(Pall,2)) == fixed == 2
            def projection_apply(M,v):
                return apply(M,v,2)
            for P in (Pz,Pall):
                assert all(projection_apply(P, P[i]) == P[i]
                           for i in range(16))
            directions = [(1,0),(0,1),(1,1),(1,2)]
            line_dims = {}
            two_dim_isotypic = []
            for a,b in directions:
                line = [((t*a)%3,(t*b)%3,c)
                        for t in range(3) for c in range(3)]
                Pl = projector(line)
                assert len(rank_and_basis(Pl,2)) == 4
                piece = [[(u-v)%2 for u,v in zip(x,y)]
                         for x,y in zip(Pl,Pall)]
                assert len(rank_and_basis(piece,2)) == 2
                line_dims[f"{a},{b}"] = 2
                two_dim_isotypic.append(piece)
            # The four 2D projectors have disjoint images modulo the
            # common 2D invariant projector.
            assert len(rank_and_basis([v for M in two_dim_isotypic for v in M],2)) == 8
            faithful_projection = [[(u-v)%2 for u,v in zip(x,y)]
                                  for x,y in zip(eye,Pz)]
            faithful_basis = rank_and_basis(faithful_projection,2)
            assert len(faithful_basis) == 6
            # Brute-force irreducibility certificate: each of the 63
            # nonzero vectors in the 6D faithful sector generates it.
            checked = 0
            for bits in range(1,1<<6):
                v = [sum(faithful_basis[k][j] for k in range(6)
                         if (bits >> k)&1)%2 for j in range(16)]
                orbit = [apply(matrices[g],v,2) for g in H]
                assert len(rank_and_basis(orbit,2)) == 6
                checked += 1
            assert checked == 63
            report["semisimple_decomposition"] = {
                "trivial_dimension":2,
                "four_nontrivial_F3xF3_character_pairs":line_dims,
                "faithful_irreducible_dimension":6,
                "faithful_nonzero_cyclic_vectors_verified":checked,
                "center_invariant_dimension":10,
                "order9_subgroup_fixed_dimensions":[4]*4
            }
        if p == 3:
            # The H2 low-rank six-element direction is independently
            # the exact TOE84 logical H1 rank-16 clock polarization.
            A={(0,b,c) for b in range(3) for c in range(3)}
            center={(0,0,c) for c in range(3)}
            rank8={g for g,r in shifts.items() if r==8}
            assert rank8==A-center
            logical=json.loads((ROOT/'data/w33_20261015_toe84_h27_logical_clifford.json').read_text(encoding='utf-8'))
            assert {tuple(g) for g in logical['ternary_rank16_polarization']}==A
            report['H2_rank8_polarization']=[list(g) for g in sorted(A)]
            report['same_polarization_as_TOE84_H1']=True
            subspace=eye
            filtration=[len(subspace)]
            while subspace:
                new=[]
                for v in subspace:
                    for g in gens:
                        image=apply(matrices[g],v,p)
                        new.append([(a-b)%p for a,b in zip(image,v)])
                subspace=rank_and_basis(new,p)
                assert len(subspace)<filtration[-1], "augmentation radical must descend"
                filtration.append(len(subspace))
                assert len(filtration)<20
            report["augmentation_radical_filtration_dimensions"]=filtration
            report["Loewy_layer_dimensions"]=[a-b for a,b in zip(filtration,filtration[1:])]
            # Multiplicity of the trivial F3 simple in H2 equals dim of head.
            report["F3_trivial_head_dimension"]=filtration[0]-filtration[1]
        out[f"F{p}"]=report
    assert out["F2"]["dimension"]==out["F3"]["dimension"]==16
    return out


if __name__ == "__main__":
    data=certificate()
    output=ROOT/"data/w33_20261015_toe85_h2_relation_module.json"
    output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:{q:v for q,v in info.items() if q!="elements"}
                      for k,info in data.items() if k in ("F2","F3")},indent=2))
    print("Certificate written:",output)
