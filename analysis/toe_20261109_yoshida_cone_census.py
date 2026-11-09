"""Exact nested-set image census for the Yoshida map of marked cubic surfaces."""

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product
from math import gcd
import json
from pathlib import Path

import numpy as np
from sympy import GF, Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261109_yoshida_cone_census.json'
PRIME = 1009  # Larger than the Hadamard bound (sqrt(8))**6 = 512.


def root_system():
    roots = []
    for i, j in combinations(range(8), 2):
        for a, b in product((-2, 2), repeat=2):
            v = [0]*8
            v[i], v[j] = a, b
            roots.append(tuple(v))
    roots.extend(v for v in product((-1, 1), repeat=8) if v.count(-1)%2 == 0)
    roots = np.array(roots, dtype=np.int64)
    a = roots[0]
    b = next(v for v in roots if a@v == -4)
    e6 = roots[(roots@a == 0) & (roots@b == 0)]
    positive = np.array(sorted(tuple(v) for v in e6 if next(x for x in v if x) > 0))
    assert len(positive) == 36
    return positive


def spans(roots):
    """All closed flats via exact row spaces modulo PRIME."""
    full = tuple(range(len(roots)))
    levels = [{(): ()}]
    for _ in range(6):
        level = {}
        for parent, rows in levels[-1].items():
            pivots = [next(j for j, value in enumerate(row) if value) for row in rows]
            table = np.array(rows, dtype=np.int64).reshape(-1, roots.shape[1])
            residuals = (roots - roots[:, pivots] @ table) % PRIME
            for new in set(full) - set(parent):
                v = residuals[new]
                pivot = int(np.flatnonzero(v)[0])
                v = v*pow(int(v[pivot]), -1, PRIME) % PRIME
                closure = tuple(np.flatnonzero(~np.any((residuals-residuals[:, [pivot]]*v)%PRIME, axis=1)))
                if closure not in level:
                    new_rows = (table-table[:, [pivot]]*v)%PRIME
                    level[closure] = sorted([*new_rows.tolist(), v.tolist()], key=lambda row: next(j for j,x in enumerate(row) if x))
        levels.append(level)
    assert list(levels[-1]) == [full]
    return [set(level) for level in levels]


def components(flat, inner):
    todo = set(flat)
    parts = []
    while todo:
        front = [min(todo)]
        todo.remove(front[0])
        part = []
        while front:
            i = front.pop()
            part.append(i)
            neighbors = {j for j in todo if inner[i, j]}
            todo -= neighbors
            front.extend(neighbors)
        parts.append(tuple(sorted(part)))
    return tuple(sorted(parts))


def nested_sets(levels, inner):
    """Maximal nested sets, including the whole connected flat as root."""
    parts = {f: components(f, inner) for level in levels for f in level}
    ranks = {f: rank for rank, level in enumerate(levels) for f in level}
    hyperplanes = defaultdict(list)
    for rank in range(1, len(levels)):
        candidates = [(f, set(f)) for f in levels[rank-1]]
        for flat in levels[rank]:
            if len(parts[flat]) == 1:
                support = set(flat)
                hyperplanes[flat] = [f for f, ids in candidates if ids < support]

    @lru_cache(None)
    def trees(flat):
        result = []
        for h in hyperplanes[flat]:
            for children in product(*(trees(c) for c in parts[h])):
                result.append((flat, *[x for child in children for x in child]))
        assert len(set(result)) == len(result)
        assert all(len(row) == ranks[flat] for row in result)
        return result

    full, = levels[-1]
    connected = [f for f in ranks if len(parts[f]) == 1 and f != full]
    return connected, trees(full)


def yoshida(connected, inner):
    factors = sorted(f for f in connected if len(f) == 3)
    orth = {a: {b for b in factors if not np.any(inner[np.ix_(a,b)])} for a in factors}
    triples = [(a,b,c) for a in factors for b in sorted(orth[a]) if a < b
               for c in sorted(orth[a]&orth[b]) if b < c]
    assert len(triples) == 40
    M = np.zeros((40,36), dtype=np.int64)
    for i, triple in enumerate(triples):
        M[i,list(sum(triple,()))] = 1
    assert np.all(M.sum(axis=1) == 9) and np.all(M.sum(axis=0) == 10)
    return triples, M


def vector_key(v):
    return tuple(map(int, v))


def images(connected, M, triples, inner):
    # Project by subtracting the last Yoshida coordinate.
    Q = M[:-1] - M[-1]
    a_rays = [Q[:,j] for j in range(36)]
    b_rays = []
    b_scales = []
    for triple in triples:
        cols = [Q[:,f].sum(axis=1) for f in triple]
        assert all(np.array_equal(v, cols[0]) for v in cols)
        scale = gcd(*map(int, cols[0]))
        b_rays.append(cols[0]//scale)
        b_scales.append(scale)
    rays = a_rays+b_rays
    lookup = {vector_key(v): i for i,v in enumerate(rays)}
    assert len(lookup) == 76
    pairs = [(i,j) for i,j in combinations(range(36),2) if inner[i,j] == 0]
    pair_sums = {vector_key(rays[i]+rays[j]): (i,j) for i,j in pairs}
    assert len(pair_sums) == 270
    lifts = {}
    for flat in connected:
        value = Q[:,flat].sum(axis=1)
        scale = gcd(*map(int,value))
        if not scale:
            lifts[flat] = ()
            continue
        key = vector_key(value//scale)
        if key in lookup:
            lifts[flat] = ((lookup[key], scale),)
        else:
            i,j = pair_sums[key]
            lifts[flat] = ((i,scale),(j,scale))
    assert sum(len(f)==6 for f in lifts if len(lifts[f])==2) == 270
    return rays, b_scales, lifts


def maximal_cones(triples, inner):
    result = {}
    for inds in combinations(range(36),4):
        if all(inner[i,j] == 0 for i,j in combinations(inds,2)):
            result[inds] = 'aaaa'
    assert len(result) == 135
    for t, factors in enumerate(triples):
        for inds in product(*factors):
            result[tuple(sorted(inds))+(36+t,)] = 'aaab'
    assert len(result) == 1215
    return result


def lattice_invariants(rays, cone):
    """Index of the ray generators in their ambient saturated span."""
    form = smith_normal_form(Matrix(np.array([rays[i] for i in cone]).T), domain=ZZ)
    return [abs(int(form[i,i])) for i in range(len(cone))]


def cone_images(cones, trees, lifts):
    """Classify all nested-set image cones by support and primitive columns."""
    faces = {f for cone in cones for k in range(5) for f in combinations(cone,k)}
    charts = defaultdict(Counter)
    support_dims = Counter()
    for _, *nested in trees:
        columns = tuple(sorted({lifts[f] for f in nested if lifts[f]}))
        support = tuple(sorted({i for col in columns for i,_ in col}))
        assert support in faces, (nested, columns)
        support_dims[len(support)] += 1
        if len(support) == 4:
            charts[support][columns] += 1
    return charts, dict(sorted(support_dims.items()))


def verify_cover(charts, cones):
    # The 24 chambers of the coordinate ordering subdivision cover the positive orthant.
    # Each chamber is generated by the four indicators of the nested suffixes.
    chain_rays = [Matrix([[int(i in order[j:]) for j in range(4)] for i in range(4)])
                  for order in permutations(range(4))]
    by_type = defaultdict(Counter)
    profiles = {}
    for cone, label in cones.items():
        local = defaultdict(int)
        for cols, multiplicity in charts[cone].items():
            signature = tuple(sorted(tuple((cone.index(i),w) for i,w in col) for col in cols))
            local[signature] += multiplicity
        profile = tuple(sorted(local.items()))
        if profile not in profiles:
            real_cover = set()
            integral_cover = set()
            full = set()
            for cols in local:
                A = Matrix([[dict(col).get(i,0) for col in cols] for i in range(4)])
                if A.rank() != 4:
                    assert any(not any(A.row(i)) for i in range(4)) or any(
                        A.row(i) == A.row(j) for i,j in combinations(range(4),2))
                    continue
                full.add(tuple(sorted({tuple(i for i,_ in col) for col in cols})))
                for triple in combinations(range(A.cols),3):
                    normals = A[:,triple].T.nullspace()
                    if len(normals) == 1:
                        normal, = normals
                        # A mixed-sign image wall inside the orthant is a
                        # coordinate equality. One-sign walls are outside.
                        if min(normal)<0<max(normal):
                            assert sum(bool(v) for v in normal) == 2 and sum(normal) == 0
                # All suffixes have 0/1 coefficients. Nonnegative integral
                # combinations can only use disjoint unit-scale columns.
                unit_cols = [sum(1<<i for i,_ in col) for col in cols
                             if all(w==1 for _,w in col)]
                reachable = {0}
                for u in unit_cols:
                    reachable |= {v | u for v in reachable if not (v & u)}
                inverses = [basis.inv() for selected in combinations(range(A.cols),4)
                            if (basis := A[:,selected]).det()]
                for j, chamber in enumerate(chain_rays):
                    if all(any(all(x >= 0 for x in inv*ray) for inv in inverses)
                           for ray in chamber.columnspace()):
                        real_cover.add(j)
                    if all(sum(1<<i for i,value in enumerate(ray) if value) in reachable
                           for ray in chamber.columnspace()):
                        integral_cover.add(j)
            profiles[profile] = (len(real_cover),len(integral_cover),len(full))
        covered, integral, full = profiles[profile]
        assert covered == integral == 24, (cone,covered,integral)
        by_type[label][(covered,integral,full,sum(local.values()))] += 1
    return {label: {str(k):v for k,v in counts.items()} for label,counts in by_type.items()}


def weyl_reflections(roots, triples):
    """Reflection permutations on root rays and Yoshida rows."""
    lookup = {tuple(v): i for i,v in enumerate(roots)}
    subsystems = [frozenset(sum(triple,())) for triple in triples]
    by_roots = {sub: i for i,sub in enumerate(subsystems)}
    reflections = []
    for root in roots:
        mapping = []
        for v in roots:
            image = v - (int(v@root)//4)*root
            if next(x for x in image if x) < 0:
                image = -image
            mapping.append(lookup[tuple(image)])
        mapping += [36+by_roots[frozenset(mapping[i] for i in sub)] for sub in subsystems]
        assert sorted(mapping) == list(range(76))
        reflections.append(mapping)
    return reflections


def cone_orbits(reflections, cones):
    """The Weyl root reflections are transitive on each named cone type."""
    reps = {}
    for label in sorted(set(cones.values())):
        representative = min(c for c,l in cones.items() if l==label)
        seen, todo = {representative}, [representative]
        while todo:
            cone = todo.pop()
            for g in reflections:
                image = tuple(sorted(g[i] for i in cone))
                if image not in seen:
                    seen.add(image)
                    todo.append(image)
        assert seen == {c for c,l in cones.items() if l==label}
        reps[label] = representative
    return reps


def fiber_graph(nestings, target):
    """Slice source cones, then identify endpoints by their common nested face."""
    vertices, edges, legs = set(), set(), set()
    for nested,basis,inv,direction in nestings:
        offset = Matrix([0]*5)
        for j,v in zip(basis,inv*Matrix(target)):
            offset[j] = v
        if any(a<0 and b==0 for a,b in zip(offset,direction)):
            continue
        lower = max(-a/b for a,b in zip(offset,direction) if b>0)
        upper = min((-a/b for a,b in zip(offset,direction) if b<0),default=None)
        if upper is not None and upper < lower:
            continue

        def endpoint(t):
            return tuple(sorted((f,v) for f,v in zip(nested,offset+t*direction) if v))

        lo = endpoint(lower)
        vertices.add(lo)
        if upper is None:
            legs.add((lo,tuple(sorted((f,v) for f,v in zip(nested,direction) if v))))
        elif lower < upper:
            hi = endpoint(upper)
            vertices.add(hi)
            edges.add(tuple(sorted((lo,hi))))
    neighbors = {v:set() for v in vertices}
    for a,b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    todo, components = set(vertices), 0
    while todo:
        components += 1
        front = [todo.pop()]
        while front:
            new = neighbors[front.pop()] & todo
            todo -= new
            front.extend(new)
    leg_degrees = Counter(v for v,_ in legs)
    valences = Counter(len(neighbors[v])+leg_degrees[v] for v in vertices)
    leg_flat_sizes = Counter(tuple(len(f) for f,_ in ray) for _,ray in legs)
    return (len(vertices),len(edges),len(legs),components,
            len(edges)-len(vertices)+components,tuple(sorted(valences.items())),
            tuple(sorted(leg_flat_sizes.items())))


def fiber_census(reps, trees, lifts):
    """Exact generic fibers for all open coordinate-order chambers of both types."""
    result = {}
    for label,cone in reps.items():
        nestings = []
        for _,*nested in trees:
            if set(cone) != {i for f in nested for i,_ in lifts[f]}:
                continue
            A = Matrix([[dict(lifts[f]).get(i,0) for f in nested] for i in cone])
            basis = A.rref()[1]
            if len(basis) < 4:
                continue
            free, = set(range(5))-set(basis)
            inv = A[:,basis].inv()
            direction = Matrix([0]*5)
            direction[free] = 1
            for j,v in zip(basis,-inv*A[:,free]):
                direction[j] = v
            nestings.append((nested,basis,inv,direction))
        profiles = Counter(fiber_graph(nestings,target) for target in permutations((1,9,81,729)))
        assert len(profiles) == 1
        profile, = profiles
        v,e,l,c,b1,valences,leg_flats = profile
        assert (v,e,l,c,b1) == ((28,36,30,1,9) if label=='aaaa' else (27,36,30,1,10))
        result[label] = dict(representative=list(map(int,cone)), strict_order_chambers=24,
                             vertices=v, bounded_edges=e, unbounded_edges=l,
                             components=c, first_betti=b1, valences=dict(valences),
                             unbounded_source_flat_sizes={str(k):n for k,n in leg_flats})
    return result


def balance(rays,cones):
    """Check unit-weight balancing on all ridges with primitive quotient normals."""
    adjacent = defaultdict(list)
    for cone in cones:
        for i in cone:
            adjacent[tuple(j for j in cone if j!=i)].append(i)
    for ridge,extensions in adjacent.items():
        tangent = Matrix(np.array([rays[i] for i in ridge]).T)
        normal = Matrix(np.array([rays[i] for i in extensions]).sum(axis=0))
        coeff = tangent.gauss_jordan_solve(normal)[0]
        assert all(v.q==1 for v in coeff)
    return dict(ridges=len(adjacent),valences=dict(sorted(Counter(map(len,adjacent.values())).items())))


def torsion_character(M, reflections):
    """A nonzero class of order three and the action on its generator."""
    Q = Matrix(M[:-1]-M[-1])
    reduce_mod_three = lambda A: DomainMatrix.from_Matrix(A).convert_to(GF(3))
    qm = reduce_mod_three(Q)
    assert qm.rank() == 14

    def in_image_mod_three(v):
        return reduce_mod_three(Q.row_join(v)).rank() == 14

    for k in qm.nullspace().to_Matrix().tolist():
        preimage = Matrix(k)
        v = Q*preimage/3
        assert all(x.q==1 for x in v)
        if not in_image_mod_three(v):
            break
    else:
        raise AssertionError('No projective order-three obstruction')

    extended = list(v)+[0]
    for reflection in reflections:
        transformed = [extended[reflection[36+i]-36] for i in range(40)]
        projective = Matrix([x-transformed[-1] for x in transformed[:-1]])
        assert in_image_mod_three(projective+v)
        assert not in_image_mod_three(projective-v)
    return dict(
        witness=list(map(int,v)),
        integral_preimage_of_three_times_witness=list(map(int,preimage)),
        modulo_three_image_rank=14,
        reflection_character={'-1':len(reflections)},
        root_order=M.shape[1],
        projective_chart='Subtract Yoshida coordinate 39',
    )


def calculate():
    roots = root_system()
    inner = roots@roots.T
    levels = spans(roots)
    connected, trees = nested_sets(levels,inner)
    print('flat counts',list(map(len,levels)), 'connected', len(connected),'trees',len(trees),flush=True)
    assert list(map(len,levels)) == [1,36,390,1530,2001,639,1]
    assert len(connected)==750 and len(trees)==142560
    triples,M = yoshida(connected,inner)
    rays,b_scales,lifts = images(connected,M,triples,inner)
    cones = maximal_cones(triples,inner)
    charts,dims = cone_images(cones,trees,lifts)
    print('image support dimensions',dims,flush=True)
    cover = verify_cover(charts,cones)
    print('cover',cover,flush=True)
    lattice = {}
    for label in sorted(set(cones.values())):
        lattice[label] = Counter(tuple(lattice_invariants(rays, c)) for c in cones if cones[c]==label)
    assert all(form==(1,1,1,1) for values in lattice.values() for form in values)
    balancing = balance(rays,cones)
    reflections = weyl_reflections(roots,triples)
    fibers = fiber_census(cone_orbits(reflections,cones),trees,lifts)
    torsion = torsion_character(M,reflections)
    print('balanced and fibers',balancing,fibers,flush=True)
    global_smith = smith_normal_form(Matrix(M), domain=ZZ)
    quotient_smith = smith_normal_form(Matrix(M[:-1]-M[-1]), domain=ZZ)
    affine_diagonal = [abs(int(global_smith[i,i])) for i in range(36) if global_smith[i,i]]
    projective_diagonal = [abs(int(quotient_smith[i,i])) for i in range(36) if quotient_smith[i,i]]
    assert affine_diagonal == [1]*15+[3] and projective_diagonal == [1]*14+[3]
    assert balancing['ridges'] == 1620
    return {
        'root_labels': roots.tolist(),
        'yoshida_row_labels': [[[int(i) for i in a] for a in triple] for triple in triples],
        'flat_counts_by_rank': list(map(len,levels)),
        'connected_flat_sizes': dict(Counter(map(len,connected))),
        'nested_maximal_cones': len(trees),
        'projected_support_dimensions': dims,
        'primitive_b_ray_scales': dict(Counter(b_scales)),
        'coverage_key': 'braid chambers covered over R, braid chambers lifting integrally in a single source cone, distinct full-rank column-support lists, nested maximal sets of full support',
        'coverage': cover,
        'unit_weight_balancing': balancing,
        'generic_set_theoretic_tropical_fibers': fibers,
        'ambient_integral_smith_by_cone_type': {k:{str(a):b for a,b in v.items()} for k,v in lattice.items()},
        'yoshida_smith_nonzero': affine_diagonal,
        'projectivized_yoshida_smith_nonzero': projective_diagonal,
        'projective_torsion_character': torsion,
    }


if __name__ == '__main__':
    result = calculate()
    print(result)
    OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
