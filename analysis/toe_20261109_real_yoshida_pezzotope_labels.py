"""Identify actual real Yoshida sign regions and their pezzotope facet labels."""

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path

from toe_20261109_yoshida_cone_census import root_system, yoshida


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261109_real_yoshida_pezzotope_labels.json'


def canonical(mask, width):
    return mask ^ ((1 << width)-1) if mask >> (width-1) else mask


def root_reflections(roots):
    index = {tuple(v): i for i,v in enumerate(roots)}
    simple = tuple(i for i,v in enumerate(roots)
                   if not any(tuple(v-a) in index for a in roots))
    assert len(simple) == 6
    reflections = []
    for root in roots:
        permutation = []
        negative = 0
        for j,v in enumerate(roots):
            image = v-int(root@v)//4*root
            if next(x for x in image if x) < 0:
                image = -image
                negative |= 1 << j
            permutation.append(index[tuple(image)])
        reflections.append((permutation,negative))
    return simple,reflections


def chamber_regions(inner, subsystems, simple, reflections):
    a2_owners = {pair: i for i,triple in enumerate(subsystems)
                 for factor in triple for pair in combinations(factor,2)}
    row_masks = [sum(1 << i for i in sum(triple,())) for triple in subsystems]
    seen = {0: (simple,0)}
    queue = [0]
    regions = defaultdict(list)
    for source in queue:
        basis, determinant_parity = seen[source]
        signs = canonical(sum(((source & row).bit_count() % 2) << i
                              for i,row in enumerate(row_masks)),40)
        a2_facets = {a2_owners[pair] for pair in combinations(sorted(basis),2)
                     if abs(inner[pair]) == 4}
        regions[signs].append((basis,determinant_parity,a2_facets))
        for permutation,negative in reflections:
            transformed = sum(((source >> j) & 1) << i for i,j in enumerate(permutation))
            image = canonical(transformed ^ negative,36)
            image_basis = tuple(sorted(permutation[j] for j in basis))
            record = (image_basis,1-determinant_parity)
            if image in seen:
                assert seen[image] == record
            else:
                seen[image] = record
                queue.append(image)
    return regions,len(seen)


def paired_regions(rows, subsystems, reflections):
    """Pair sign regions over the same even support and transport signs exactly."""
    members = [set(sum(triple,())) for triple in subsystems]
    incident = [{j for j,b in enumerate(members) if i!=j and not (a&b)}
                for i,a in enumerate(members)]
    points = [(i,j,k,l) for i in range(40) for j in incident[i] if i<j
              for k in incident[i]&incident[j] if j<k
              for l in incident[i]&incident[j]&incident[k] if k<l]
    assert len(points)==40
    fibers = defaultdict(list)
    for row in rows:
        facets = set(row['type_b_cusp_facets'])
        covered = tuple(i for i,point in enumerate(points) if facets.intersection(point))
        assert len(covered)==20
        fibers[covered].append(row)
    assert len(fibers)==216 and set(map(len,fibers.values()))=={2}

    row_of = {frozenset(roots): i for i,roots in enumerate(members)}
    distances = Counter()
    pairs = []
    for fiber in fibers.values():
        first,second = sorted(fiber,key=lambda row:row['determinant_parity'])
        assert [first['determinant_parity'],second['determinant_parity']]==[0,1]
        a,b = int(first['projective_negative_mask'],16),int(second['projective_negative_mask'],16)
        support = set(first['type_b_cusp_facets']) | set(second['type_b_cusp_facets'])
        assert len(support)==10
        root, = set(range(36)) - set().union(*(members[i] for i in support))
        permutation,negative = reflections[root]
        transformed = 0
        for i,roots in enumerate(members):
            j = row_of[frozenset(permutation[r] for r in roots)]
            reflected_sign = sum((negative>>r)&1 for r in roots)%2
            transformed |= (((a>>j)&1)^reflected_sign)<<i
        assert canonical(transformed,40)==b
        distance = (a^b).bit_count()
        distances[min(distance,40-distance)] += 1
        pairs.append([hex(a),hex(b),root])
    return dict(n_pairs=len(pairs),reflection_root_by_pair=sorted(pairs),
                projective_sign_hamming_distance=dict(sorted(distances.items())))


def calculate():
    roots = root_system()
    inner = roots@roots.T
    index = {tuple(v): i for i,v in enumerate(roots)}
    factors = set()
    for i,j in combinations(range(36),2):
        if abs(inner[i,j]) == 4:
            third = roots[i] - int(inner[i,j])//4*roots[j]
            if next(x for x in third if x) < 0:
                third = -third
            factors.add(tuple(sorted((i,j,index[tuple(third)]))))
    subsystems,_ = yoshida(factors,inner)
    simple,reflections = root_reflections(roots)
    regions,source_count = chamber_regions(inner,subsystems,simple,[reflections[i] for i in simple])
    assert source_count==25920 and len(regions)==432
    assert set(map(len,regions.values()))=={60}

    by_cusp_set = {}
    region_rows = []
    for signs,lifts in sorted(regions.items()):
        root_facets = set().union(*(set(basis) for basis,_,_ in lifts))
        cusp_facets = tuple(sorted(set().union(*(cusps for _,_,cusps in lifts))))
        assert len(cusp_facets) == 5, (signs,cusp_facets)
        determinant_parity, = {parity for _,parity,_ in lifts}
        subsystem_roots = [set(sum(subsystems[i],())) for i in cusp_facets]
        triple_roots = set()
        for parts in combinations(subsystem_roots,3):
            common, = set.intersection(*parts)
            triple_roots.add(common)
        assert len(root_facets)==10 and root_facets==triple_roots
        assert all(len(a&b)==3 for a,b in combinations(subsystem_roots,2))
        assert all(any(not (other & part) for part in subsystem_roots)
                   for i,triple in enumerate(subsystems) if i not in cusp_facets
                   for other in (set(sum(triple,())),))
        assert cusp_facets not in by_cusp_set
        by_cusp_set[cusp_facets] = signs
        region_rows.append(dict(projective_negative_mask=hex(signs),determinant_parity=determinant_parity,
                                type_a_root_facets=sorted(root_facets),type_b_cusp_facets=list(cusp_facets)))
    parity = Counter(row['determinant_parity'] for row in region_rows)
    assert parity=={0:216,1:216}
    pairs = paired_regions(region_rows,subsystems,reflections)
    return dict(
        projective_root_chambers=source_count,
        projective_yoshida_sign_regions=len(regions),
        root_chambers_per_region=60,
        determinant_parity_counts=dict(sorted(parity.items())),
        root_labels=roots.tolist(),
        yoshida_row_labels=[[[int(i) for i in a] for a in triple] for triple in subsystems],
        regions=region_rows,
        chiral_pairs=pairs,
        boundary='For a simple-root coordinate of a root chamber, assign valuation one and give the other coordinates valuation zero. For an adjacent pair do this to both coordinates. Positivity prevents cancellation. Their A1 and A2 flats map to the indicated A and B rays.',
    )


if __name__=='__main__':
    result=calculate()
    OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('real regions:',result['projective_yoshida_sign_regions'], 'facets each: 10+5',
          'source chambers each:',result['root_chambers_per_region'],
          'pair sign distances:',result['chiral_pairs']['projective_sign_hamming_distance'])
