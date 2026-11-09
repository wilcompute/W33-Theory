"""The canonical form of the positive pezzotope and its atlas partner."""

from collections import Counter
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path

import sympy as s
from sympy.matrices.normalforms import smith_normal_decomp

from toe_20261109_real_yoshida_pezzotope_labels import root_reflections
from toe_20261109_yoshida_cone_census import root_system

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "data/toe_20261109_real_yoshida_pezzotope_labels.json"
OUT = ROOT / "data/toe_20261109_pezzotope_canonical_partner.json"
X = s.symbols("x y z w")
Y = s.symbols("a b c d", positive=True)
U_RATIOS = (
    ("C", "126 135 234 456"),
    ("134 156 235 246", "135 146 234 256"),
    ("134 356", "135 346"),
    ("136 145", "135 146"),
    ("125 136 246 345", "126 135 245 346"),
    ("136 235", "135 236"),
    ("123 145 246 356", "124 135 236 456"),
    ("125 356", "135 256"),
    ("125 134", "124 135"),
    ("145 235", "135 245"),
    ("135 234", "134 235"),
    ("135 456", "145 356"),
    ("124 135 256 346", "125 134 246 356"),
    ("126 135", "125 136"),
    ("135 146 236 245", "136 145 235 246"),
)
Y_RATIOS = (
    ((10,), (5, 8, 9, 13, 14)),
    ((9, 11), (4, 7, 12, 15)),
    ((4, 6, 14, 15), (3, 13)),
    ((1, 4, 8, 12, 14), (2,)),
)
PAPER_NORMALS = (
    (0,0,0,1), (0,0,0,-1), (0,0,-1,0), (0,-1,1,1), (-1,0,0,0),
    (0,0,1,0), (0,-1,0,0), (-1,0,0,1), (-1,1,0,0), (1,0,0,0),
    (0,1,0,0), (0,-1,0,1), (-1,0,-1,0), (-1,0,1,1), (0,-1,1,0),
)


def minors(matrix):
    return {"".join(str(i+1) for i in idx): s.factor(matrix[:, idx].det())
            for idx in combinations(range(6), 3)}


def conic(p):
    return s.factor(s.prod(p[k] for k in ("134", "156", "235", "246"))
                    - s.prod(p[k] for k in ("135", "146", "234", "256")))


def chart(x, y, z, w):
    return s.Matrix([[1,0,0,1,1,1], [0,1,0,1,x,z], [0,0,1,1,y,w]])


def normalize(matrix):
    first = matrix[:, :3].inv()*matrix
    unit = s.diag(*(1/v for v in first[:,3]))*first
    return tuple(s.factor(unit[i,j]/unit[0,j]) for j in (4,5) for i in (1,2))


def cremona(matrix, centers):
    first = matrix[:, centers].inv()*matrix
    return s.Matrix.hstack(*(first[:,i] if i in centers else s.Matrix([1/v for v in first[:,i]])
                            for i in range(6)))


def positive_chart():
    a,b,c,d = Y
    g3 = 1+b+a*b
    g8 = 1+b*c+b*d*c+d*c+c+b*d+d
    g10 = g8+a*b*d+a*b*d*c
    g11 = g10+a*b*c
    v = ((a+1)*b/g3, b/(b+1), (a+1)*b*c*g8/((b*c+c+1)*g11), b*c/(b*c+c+1))
    return v, (g3,g8,g10)


def u_functions(p):
    values = {**p,"C":-conic(p)}
    return [s.factor(s.prod(values[k] for k in a.split())/s.prod(values[k] for k in b.split()))
            for a,b in U_RATIOS]


def dlog_parameters(u):
    return [s.factor(s.prod(u[i-1] for i in a)/s.prod(u[i-1] for i in b)) for a,b in Y_RATIOS]


def root_labels():
    """Match the article's difference/triple/conic forms to the repo's roots."""
    roots = root_system()
    simple, _ = root_reflections(roots)
    eye = s.eye(6)
    standard = {"".join(str(i+1) for i in ij): eye[ij[0],:]-eye[ij[1],:]
                for ij in combinations(range(6),2)}
    standard.update({"".join(str(i+1) for i in ijk):
                     sum((eye[i,:] for i in ijk),s.zeros(1,6))
                     for ijk in combinations(range(6),3)})
    standard["C"] = s.ones(1,6)
    basis = s.Matrix.vstack(*(standard[f"{i}{i+1}"] for i in range(1,6)), standard["456"])
    metric = eye-s.ones(6)/9
    for order in permutations(simple):
        native = s.Matrix(roots[list(order)].tolist())
        if native*native.T == 4*basis*metric*basis.T:
            break
    else:
        raise AssertionError("Root Cartan labels do not match")
    transport = basis.inv()*native
    assert transport*transport.T == 4*metric
    lookup = {tuple(v): i for i,v in enumerate(roots)}
    labels, signs = {}, {}
    for key,v in standard.items():
        image = tuple(v*transport)
        sign = int(s.sign(next(x for x in image if x)))
        labels[key] = lookup[tuple(sign*x for x in image)]
        signs[key] = sign
    assert len(set(labels.values())) == 36
    return standard, labels, signs


def yoshida_signs(atlas, standard, labels, signs, matrix):
    """Calibrate products of minors against oriented linear root products."""
    d = s.Matrix([1,2,3,5,7,11])
    calibration = minors(s.Matrix([[1]*6,list(d),[x**3 for x in d]]))
    sample = minors(matrix)
    calibration["C"], sample["C"] = conic(calibration), conic(sample)
    root_sign = {k: signs[k]*s.sign((v*d)[0]) for k,v in standard.items()}
    inverse = {i:k for k,i in labels.items()}
    result = []
    for factors in atlas["yoshida_row_labels"]:
        keys = [inverse[i] for factor in factors for i in factor]
        products = [k for k in keys if len(k)==3 or k=="C"]
        assert (len(products), "C" in products) in {(6,False),(3,True)}
        # Both polynomials have the same omitted full Vandermonde factor.
        value = s.prod(s.sign(sample[k]*calibration[k]) for k in products)
        value *= s.prod(root_sign[k] for k in keys)
        assert abs(value) == 1
        result.append(value)
    return hex(sum((sign!=result[-1]) << i for i,sign in enumerate(result)))


def root_exponents(labels, key):
    row = s.zeros(1,36)
    if key=="C":
        parts = [k for k in labels if len(k)==2]+[key]
    else:
        parts = ["".join(p) for p in combinations(key,2)]+[key]
    for k in parts:
        row[labels[k]] += 1
    return row


def u_and_y_exponents(labels):
    def exponents(keys):
        return sum((root_exponents(labels,k) for k in keys.split()),s.zeros(1,36))
    u = s.Matrix.vstack(*(exponents(a)-exponents(b) for a,b in U_RATIOS))
    y = s.Matrix.vstack(*(sum((u[i-1,:] for i in a),s.zeros(1,36))
                          -sum((u[i-1,:] for i in b),s.zeros(1,36)) for a,b in Y_RATIOS))
    return u,y


def facet_certificate(atlas, seed, labels, reflection):
    """Identify ordered facets by their primitive valuation vectors."""
    u,y = u_and_y_exponents(labels)
    facet_map, valuations = {}, {}
    for i in seed["type_a_root_facets"]:
        valuations[("a",i)] = (tuple([i]),)
    for i in seed["type_b_cusp_facets"]:
        valuations[("b",i)] = tuple(map(tuple,atlas["yoshida_row_labels"][i]))
    for label,choices in valuations.items():
        for chosen in choices:
            orders = u[:,chosen]*s.ones(len(chosen),1)
            if tuple(orders) in {tuple(s.eye(15)[:,i]) for i in range(15)}:
                i, = [i for i,n in enumerate(orders) if n]
                assert i not in facet_map or facet_map[i]==label
                facet_map[i] = label
                break
    assert len(facet_map) == 15, facet_map
    ordered = [facet_map[i] for i in range(15)]
    assert len(set(ordered)) == 15
    normals = []
    for label in ordered:
        candidates = valuations[label]
        for chosen in candidates:
            orders = u[:,chosen]*s.ones(len(chosen),1)
            if orders == s.eye(15)[:,len(normals)]:
                normal = y[:,chosen]*s.ones(len(chosen),1)
                assert tuple(normal)==PAPER_NORMALS[len(normals)]
                opposite_y = y[:,reflection]
                reflected = [reflection[i] for i in chosen]
                assert opposite_y[:,reflected]*s.ones(len(reflected),1)==normal
                normals.append(normal)
                break
    assert len(normals)==15
    inverse = {i:k for k,i in labels.items()}
    return ordered,normals,[(inverse[i] if kind=="a" else i) for kind,i in ordered]


def residue_certificate(atlas, ordered, normals):
    roots = s.Matrix(atlas["root_labels"])
    factors = atlas["yoshida_row_labels"]

    def meet(a,b):
        kind,i = a
        other,j = b
        if kind==other=="a":
            return (roots[i,:]*roots[j,:].T)[0]==0
        if kind==other=="b":
            return False
        if kind=="b":
            i,j = j,i
        return any(i in f for f in factors[j])

    vertices = [ids for ids in combinations(range(15),4)
                if all(meet(ordered[i],ordered[j]) for i,j in combinations(ids,2))]
    assert len(vertices)==45
    records = []
    for ids in vertices:
        determinant = int(s.Matrix.hstack(*(normals[i] for i in ids)).det())
        assert abs(determinant)==1
        records.append([list(i+1 for i in ids),determinant])
    facet_residues = [[(-1)**i*int(v) for i,v in enumerate(normal)] for normal in normals]
    # These are contractions in the basis omitting the ith dlog coordinate.
    return facet_residues,records


def kummer_certificate(atlas, labels, reflection):
    """Find integral Yoshida characters in the rank-15 projective lattice."""
    rows = [sum(factors,[]) for factors in atlas["yoshida_row_labels"]]
    M = s.Matrix([[int(i in row) for i in range(36)] for row in rows])
    Q = (M[:-1,:]-s.ones(39,1)*M[-1,:]).T
    diagonal, left, right = smith_normal_decomp(Q,domain=s.ZZ)
    assert diagonal == left*Q*right
    assert [abs(diagonal[i,i]) for i in range(15)] == [1]*14+[3]
    assert diagonal[15:,:] == s.zeros(21,39)
    u,y = u_and_y_exponents(labels)

    def vector(row):
        transformed = left*row.T
        assert not any(transformed[15:])
        result = s.zeros(39,1)
        for i in range(15):
            result[i] = transformed[i]/diagonal[i,i]
        result = right*result
        assert Q*result == row.T
        return result

    def integral(row):
        coeff = vector(row)
        assert all(x.q == 1 for x in coeff)
        return [[i,int(x)] for i,x in enumerate(coeff) if x]

    def quotient_class(row):
        hits = [k for k in range(3) if all(x.q == 1 for x in vector(row-k*u[0,:]))]
        result, = hits
        return result

    assert any(x.q != 1 for x in vector(u[0,:]))
    u_classes = [quotient_class(u[i,:]) for i in range(15)]
    y_classes = [quotient_class(y[i,:]) for i in range(4)]
    assert u_classes == [1]*15
    assert y_classes == [2,1,2,1]
    ratio_row = s.Matrix([[1]*10+[2]*5])*u
    reflected = u[0,reflection]
    assert quotient_class(ratio_row)==2 and quotient_class(reflected)==2
    return dict(
        nonzero_smith_diagonal=[1]*14+[3],
        class_generator="the exponent vector of u1",
        u_classes=u_classes,y_classes=y_classes,form_ratio_absolute_class=2,
        reflected_u1_class=2,
        monomials_up_to_constant_sign=dict(
            cube_of_u1=integral(3*u[0,:]),
            u_i_over_u1=[integral(u[i,:]-u[0,:]) for i in range(15)],
            u1_times_reflected_u1=integral(reflected+u[0,:]),
            absolute_form_ratio_over_u1_squared=integral(ratio_row-2*u[0,:]),
        ),
    )


def transport_words(atlas, seed, seed_root, labels, reflections):
    """Check the full atlas and supply Weyl words from the positive chamber."""
    simple,_ = root_reflections(root_system())
    rows = [frozenset(sum(row,[])) for row in atlas["yoshida_row_labels"]]
    row_index = {row:i for i,row in enumerate(rows)}
    regions = {tuple(r["type_b_cusp_facets"]):r["projective_negative_mask"] for r in atlas["regions"]}
    partner_roots = {mask:r for a,b,r in atlas["chiral_pairs"]["reflection_root_by_pair"] for mask in (a,b)}
    root_name = {i:k for k,i in labels.items()}
    maps = {}
    for i in simple:
        root_perm = reflections[i][0]
        cusp_perm = [row_index[frozenset(root_perm[j] for j in row)] for row in rows]
        maps[i] = (root_perm,cusp_perm)
    start = tuple(seed["type_b_cusp_facets"])
    reached, queue = {start:((),seed_root)}, [start]
    for source in queue:
        word,partner_root = reached[source]
        for i,(root_perm,cusp_perm) in maps.items():
            target = tuple(sorted(cusp_perm[j] for j in source))
            assert partner_roots[regions[target]] == root_perm[partner_root]
            if target not in reached:
                reached[target] = ((*word,root_name[i]),root_perm[partner_root])
                queue.append(target)
    assert len(reached)==432
    return {regions[key]:list(reached[key][0]) for key in sorted(reached)}


def scattering_certificate(factors, normals, vertex_residues, orders):
    """The form ratio selects a point of the positive kinematic cone."""
    exponents = {tuple(sum(v) for v in zip(*choice))
                 for choice in product(*(s.Poly(f,*Y).monoms() for f in factors))}
    normal_tuples = [tuple(map(int,v)) for v in normals]
    minimums, faces = [], []
    for normal in normal_tuples:
        dots = {e:sum(x*y for x,y in zip(normal,e)) for e in exponents}
        lower = min(dots.values())
        minimums.append(lower)
        faces.append({e for e,value in dots.items() if value==lower})

    points = Counter()
    amplitude = 0
    root_only = 0
    for facets,determinant in vertex_residues:
        point, = set.intersection(*(faces[i-1] for i in facets))
        points[point] += 1
        assert set(facets) <= {i+1 for i,face in enumerate(faces) if point in face}
        amplitude += s.Rational(abs(determinant),s.prod(orders[i-1] for i in facets))
        root_only += all(i<=10 for i in facets)
    assert root_only==5 and amplitude==25
    print("scattering amplitude",amplitude,"Newton vertices",len(points),"cone multiplicities",dict(Counter(points.values())),flush=True)
    return dict(
        selected_facet_weights=orders,
        newton_polynomial_support_size=len(exponents),
        newton_vertices=[list(e) for e in sorted(points)],
        cone_count_by_newton_vertex={str(k):v for k,v in sorted(Counter(points.values()).items())},
        newton_facet_minimums=minimums,
        root_only_vertex_cones=root_only,cusp_vertex_cones=len(vertex_residues)-root_only,
        unit_weighted_schwinger_integral=int(amplitude),
        polar_lattice_coordinate_volume=str(amplitude/s.factorial(4)),
        scope="The mathematical positive-geometry amplitude at the weights from the form ratio.",
    )


def calculate():
    atlas = json.loads(ATLAS.read_text(encoding="utf-8"))
    standard, labels, signs = root_labels()
    positive, factors = positive_chart()
    sample = chart(*(x.subs(dict.fromkeys(Y,1)) for x in positive))
    mask = yoshida_signs(atlas,standard,labels,signs,sample)
    regions = {r["projective_negative_mask"]:r for r in atlas["regions"]}
    pair = next(p for p in atlas["chiral_pairs"]["reflection_root_by_pair"] if mask in p[:2])
    assert pair[2]==labels["135"]
    partner, = set(pair[:2])-{mask}
    _, reflections = root_reflections(root_system())
    reflection = reflections[pair[2]][0]
    words = transport_words(atlas,regions[mask],pair[2],labels,reflections)
    assert yoshida_signs(atlas,standard,labels,signs,cremona(sample,[0,2,4]))==partner
    gale = (-sample[:,3:].T).row_join(s.eye(3))
    gale_mask = yoshida_signs(atlas,standard,labels,signs,gale)
    assert gale_mask not in (mask,partner)
    assert all(0 < u < 1 for u in u_functions(minors(sample)))
    assert all(not (set(regions[a][key]) & set(regions[b][key]))
               for a,b,_ in atlas["chiral_pairs"]["reflection_root_by_pair"]
               for key in ("type_a_root_facets","type_b_cusp_facets"))
    print("identified partner",mask,partner,"root 135",flush=True)

    ordered,normals,names = facet_certificate(atlas,regions[mask],labels,reflection)
    facet_residues,vertex_residues = residue_certificate(atlas,ordered,normals)

    p = minors(chart(*X))
    q = conic(p)
    coeff = s.factor(p["135"]/(p["123"]*p["345"]*p["156"]*q))
    u = u_functions(p)
    dlog = dlog_parameters(u)
    assert s.factor(s.Matrix(dlog).jacobian(X).det(method="domain-ge")/s.prod(dlog)/coeff)==1
    g = normalize(cremona(chart(*X),[0,2,4]))
    dg = s.factor(s.Matrix(g).jacobian(X).det(method="domain-ge"))
    substitutions = dict(zip(X,g))
    assert tuple(s.factor(x.subs(substitutions,simultaneous=True)) for x in g)==X
    reflected = s.factor(coeff.subs(substitutions,simultaneous=True)*dg)
    ratio = s.factor(reflected/coeff)
    assert s.factor(ratio*ratio.subs(substitutions,simultaneous=True))==1
    assert s.factor(ratio/s.prod(u[i]**(1+(i>=10)) for i in range(15)))==-1
    a,b,c,d = Y
    product = s.prod(factors)
    ratio_positive = -a*b**2*c*d/product
    assert s.factor(ratio.subs(dict(zip(X,positive)),simultaneous=True)/ratio_positive)==1
    # The denominator strictly exceeds the numerator on the positive orthant.
    assert all(k>0 for k in s.Poly(product-a*b**2*c*d,*Y).coeffs())
    orders = []
    for ray in normals:
        order = sum(i*j for i,j in zip((1,2,1,1),ray))
        order -= sum(min(sum(i*j for i,j in zip(m,ray))
                         for m in s.Poly(f,*Y).monoms()) for f in factors)
        orders.append(int(order))
    assert orders == [1]*10+[2]*5
    print("ratio valuations",orders,flush=True)
    kummer = kummer_certificate(atlas,labels,reflection)
    scattering = scattering_certificate(factors,normals,vertex_residues,orders)
    print("Kummer exponent classes",kummer["u_classes"],kummer["y_classes"],flush=True)
    return dict(
        seed_mask=mask,partner_mask=partner,partner_root="135",gale_negative_control_mask=gale_mask,
        canonical_chart_coefficient=str(coeff), partner_chart_coefficient=str(reflected),
        reflection_chart=[str(x) for x in g],reflection_jacobian=str(dg),
        ratio=str(ratio),ratio_in_positive_chart=str(ratio_positive),
        positive_chamber_bound="-1 < ratio < 0",partner_chamber_bound="ratio < -1",
        ordered_facet_labels=[[k,i,n] for (k,i),n in zip(ordered,names)],
        facet_residue_contractions=facet_residues,ordered_vertex_residues=vertex_residues,
        seed_facet_orders_of_ratio=orders,disjoint_facet_support_pairs=216,
        kummer_character_lattice=kummer,
        ratio_selected_scattering_potential=scattering,
        seed_to_region_weyl_words_in_application_order=words,
        orientation_convention="The 432 canonical forms are the Weyl translates of the published seed form.",
        residues_scope="Primitive logarithmic charts. Partner residues are compared after relabeling and transport.",

        atlas_sha256=hashlib.sha256(ATLAS.read_bytes()).hexdigest(),
    )


if __name__=="__main__":
    result = calculate()
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("verified canonical-form partner and",len(result["ordered_vertex_residues"]),"vertex residues")
