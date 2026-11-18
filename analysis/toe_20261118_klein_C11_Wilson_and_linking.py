"""Trade the free F55 quotient for C11: integral torsion and an SU5 Wilson line.

Uses the parent Klein link topology and the written symplectic coinvariant
argument. The report proves the extension splitting; exact arithmetic here
checks it, the symmetry-constrained linking form, and the gauge projections.
An SU5/E6 gauge sector is a conditional input, not a field in smooth 11D SUGRA.
Companion proof: analysis/2026-11-18_Klein_C11_Wilson_linking_quantum_orbit.md.

Rediscovery guard's alpha@121 candidate files were read: the121 in
w33_MCXXI_MCXXX_six_headlines_lloyd_exceptional.py and
w33_connes_lott_sm_action.py is an arithmetic fine-structure proxy; in
w33_pass75_zeta_equidistribution.py it is a polynomial coefficient. None
computes the cyclic extension, linking or Wilson-line result used here.
"""
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import sympy as s
import numpy as np
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

from toe_20261117_11cell_klein_cubic_link import monomials

ROOT = Path(__file__).resolve().parents[1]
W = (1, 9, 4, 3, 5)


def cyclic_integral_topology():
    # In 0 -> Z11 -> Tor_11 H3(Y/C11) -> Z11 ->0, the normalizing
    # C5 acts on the ends by3 (symplectic coinvariant) and9^2=4.
    alpha, beta = 3, pow(9, 2, 11)
    assert (alpha, beta) == (3, 4)
    assert pow(alpha, 5, 11) == pow(beta, 5, 11) == 1
    # A nonsplit extension would be Z121. Every automorphism of that
    # cyclic group has the SAME scalar on its subgroup11Z121 and quotient.
    automorphisms = [a for a in range(121) if s.gcd(a, 121) == 1]
    order5_actions = [a for a in automorphisms if pow(a, 5, 121) == 1]
    assert len(order5_actions) == 5
    assert not any((a % 11, (11*a % 121)//11) == (alpha, beta)
                   for a in automorphisms)
    diagonal = s.diag(alpha, beta)
    J = s.Matrix([[0, 1], [1, 0]])
    assert (diagonal**5-s.eye(2)).applyfunc(lambda z: z % 11) == s.zeros(2)
    assert (diagonal.T*J*diagonal-J).applyfunc(lambda z: z % 11) == s.zeros(2)
    assert (alpha*alpha) % 11 != 1 and (beta*beta) % 11 != 1
    assert s.gcd(int(J.det()), 11) == 1
    smith = smith_normal_form(s.diag(3, 11, 11), domain=ZZ)
    torsion = [int(smith[i, i]) for i in range(3) if abs(smith[i, i]) > 1]
    assert torsion == [11, 33]
    homology = [dict(degree=n, free_rank=int(n in (0, 7)),
                     torsion=[11] if n in (1, 5) else torsion if n == 3 else [])
                for n in range(8)]
    cohomology = [dict(degree=n, free_rank=homology[n]['free_rank'],
                       torsion=homology[n-1]['torsion'] if n else []) for n in range(8)]
    for n in range(8):
        assert cohomology[n]['torsion'] == homology[7-n]['torsion']
        assert cohomology[n]['free_rank'] == homology[7-n]['free_rank']
    # A C11 restriction of the same stable tangent representation.
    c2 = sum(a*b for a, b in combinations(W, 2))
    assert c2 == 176 and c2 % 11 == 0
    return dict(pi1='C11', normalizer_quotient_symmetry='C5',
                H3_extension_end_actions=[alpha, beta],
                nonsplit_Z121_extension_excluded=True,
                splitting_proof='The surviving normalizer acts differently on the two '
                    'Z11 end terms. Any automorphism of Z121 acts identically modulo11 '
                    'on its subgroup and quotient. Therefore the11-primary extension splits.',
                integral_homology=homology, integral_cohomology=cohomology,
                flat_degree4_C_field='Z11 x Z33 = Z3 x Z11 x Z11',
                flat_sector_count=3*11**2,
                eleven_primary_linking_matrix_mod1=[['0', '1/11'], ['1/11', '0']],
                linking_basis_scope='A C5 eigenbasis, rescaled to dual generators; '
                    'not an identified pair of geometric brane cycles.',
                linking_proof='Eigenvalues3 and4 have product1, while neither square '
                    'is1 mod11. Invariance forces both self-pairings to vanish. '
                    'Perfectness forces a nonzero cross-pairing, normalized to1/11.',
                spin_lambda=0,
                lambda_reason='Stable tangent is the real SU5 representation minusR3; '
                    'lambda=-c2 and c2|BC11=176u^2=0.',
                limitations='No full cohomology ring or differential Chern-Simons/Page '
                    'quadratic refinement for this C11 quotient computed here.')


def wilson_line_test():
    cyclic_controls = []
    for n in (2, 3, 4, 5, 6, 7, 11, 25):
        pairs = [(a, b) for a, b in product(range(n), repeat=2)
                 if (3*a+2*b) % n == 0 and a != b]
        cyclic_controls.append(dict(order=n, determinant_one_split_pairs=len(pairs)))
    assert next(r for r in cyclic_controls if r['order'] == 5)['determinant_one_split_pairs'] == 0
    assert next(r for r in cyclic_controls if r['order'] == 11)['determinant_one_split_pairs'] == 10
    charges = (2, 2, 2, -3, -3)
    assert sum(charges) == 0
    root_pairs = [(i, j) for i in range(5) for j in range(5)
                  if i != j and (charges[i]-charges[j]) % 11 == 0]
    assert len(root_pairs) == 8
    centralizer_dimension = 4+len(root_pairs)
    assert centralizer_dimension == 12
    assert all((i < 3) == (j < 3) for i, j in root_pairs)
    assert Counter(a % 11 for a in charges) != Counter(9*a % 11 for a in charges)
    # The faithful5D irrep itself has scalar commutant by Schur: no SM.
    assert len(set(W)) == 5
    return dict(F55_SU5_to_standard_SM_Wilson_line=False,
                obstruction='An image commuting with standard SU3 x SU2 is block-scalar '
                    'on3+2, hence abelian and factors through F55_ab=C5. The determinant '
                    'condition3a+2b=0 mod5 forces a=b, making the image central.',
                cyclic_controls=cyclic_controls,
                C11_SU5_holonomy_exponents=list(charges),
                exact_order=11,
                surviving_offdiagonal_root_pairs=[list(x) for x in root_pairs],
                centralizer_Lie_algebra='su3 + su2 + u1',
                centralizer_dimension=centralizer_dimension,
                nonextension_to_F55='The holonomy eigenvalue multiset differs from that '
                    'of its ninth power; no conjugating P can extend this C11 map to F55.',
                E6_parallel_connection='If both rank-breaking singlet Higgs VEVs are '
                    'parallel and fixed, holonomy lies in their SU5 stabilizer. F55 flat '
                    'holonomy cannot replace the hypercharge adjoint in that chart. '
                    'C11 flat holonomy can break that supplied SU5 algebra to the SM algebra.',
                scope='A conditional gauge-centralizer statement. Neither quotient '
                    'comes with a derived E6/SU5 gauge sector or a chiral fermion spectrum.')


def faithful_E6_control():
    six = W+(0,)
    pair_weights = [sum(six[i] for i in inds) % 11 for inds in combinations(range(6), 2)]
    triple_weights = [sum(six[i] for i in inds) % 11 for inds in combinations(range(6), 3)]
    assert len(pair_weights) == 15 and len(triple_weights) == 20
    assert 0 not in pair_weights and 0 not in triple_weights
    # D fixes the six diagonal SU6 directions. P cycles the first5.
    # Remove the scalar: centralizer in su6 is one-dimensional.
    su6_invariants = 2-1
    rows = []
    for ell in range(5):
        su2_invariants = 1+2*int(2*ell % 5 == 0)
        adjoint = su6_invariants+su2_invariants
        singlets27 = sum(k % 5 == 0 for k in (ell, -ell))
        assert adjoint in (2, 4)
        rows.append(dict(SU2_C5_character=ell, E6_adjoint_invariants=adjoint,
                         supplied_27_invariants=singlets27,
                         centralizer='su2+u1' if ell == 0 else 'u1+u1'))
    return dict(embedding='F55 -> SU6 x SU2 -> E6, with6=faithful5+1',
                branching='78=(35,1)+(1,3)+(20,2);27=(15,1)+(6bar,2), '
                    'up to simultaneous conjugation convention',
                wedge2_C11_fixed=0, wedge3_C11_fixed=0, cases=rows,
                conclusion='This natural faithful F55 embedding also fails to leave '
                    'the SM gauge algebra. This is not a classification of all E6 embeddings.')


def protected_and_topological_tradeoff():
    ambient = []
    cone = []
    for degree in range(13):
        ambient.append(sum(sum(a*b for a, b in zip(m, W)) % 11 == 0 for m in monomials(degree)))
        cone.append(ambient[-1]-(ambient[degree-3] if degree >= 3 else 0))
    assert cone[:5] == [1, 0, 0, 4, 5]
    assert cone[2] == 0
    volume = s.Rational(3, 16*11)
    assert volume == s.Rational(3, 176)
    q = 2*3
    assert q*(q+6) == 72
    # Untwisted BF shadow of Tor H1 paired with Tor H5. Character table
    # checks nondegeneracy. It is not the full11D C-field topological action.
    N = 11
    phase_exponents = [[Fraction(a*b, N) % 1 for b in range(N)] for a in range(N)]
    assert all(any(x for x in phase_exponents[a]) for a in range(1, N))
    assert len({tuple(row) for row in phase_exponents}) == N
    return dict(C11_cone_dimensions_degrees0_through12=cone,
                C11_charge4_holomorphic_marginal_functions=cone[2],
                continuous_flat_C3_modes=0,
                invariant_cubic_complex_structure_deformations=0,
                deformation_source='Parent cubic Jacobian weight-zero relation rank5; '
                    'the entire C11 invariant cubic parameter space is relations.',
                volume_over_S7=str(volume), first_holomorphic_charge=q,
                first_holomorphic_Laplacian=q*(q+6),
                untwisted_particle_string_BF_level=N,
                BF_action='11/(2pi) integral B2 wedge dA1',
                BF_objects='M2 on torsion1-cycle gives an external string; M5 on '
                    'the dual torsion5-cycle gives a particle. Dual generators braid '
                    'by exp(2pi i/11). Their existence as homology classes does not '
                    'compute tensions, stability, screening or flux-induced twists.',
                BF_scope='Uncoupled torsion-linking shadow; the C3 G4 G4 and one-loop '
                    'terms, boundary conditions and full charge identifications remain open.',
                flat_unitary_Dirac_gap_squared='49/4, by the same Friedrich theorem '
                    'as peer c2f8f23a7; still no ordinary flat-twisted Dirac zero modes.',
                tradeoff='C11 permits the conditional SU5 Wilson line while retaining '
                    'no charge4 holomorphic or continuous C3 deformations. Its torsion '
                    'sectors and protected low harmonics differ from the F55 quotient.')


def linking_quantum_double_and_Klein_orbit():
    # A mathematical finite-quadratic-module model of the11-primary linking.
    # This is not the full physical11D C-field Chern-Simons theory.
    n = 11
    labels = list(product(range(n), repeat=2))
    pos = {v: i for i, v in enumerate(labels)}
    q = lambda v: v[0]*v[1] % n
    b = lambda v, w: (v[0]*w[1]+v[1]*w[0]) % n
    for v, w in product(labels, repeat=2):
        total = tuple((v[i]+w[i]) % n for i in range(2))
        assert (q(total)-q(v)-q(w)-b(v, w)) % n == 0
    counts = Counter(q(v) for v in labels)
    assert counts[0] == 21 and all(counts[k] == 10 for k in range(1, n))
    # Exact Gauss sum:21+10*sum_(k=1)^10 zeta^k=11; divided by sqrt121 is1.
    assert counts[0]-counts[1] == 11
    K = s.Matrix([[0, n], [n, 0]])
    assert K.det() == -121
    assert K.inv() == s.Matrix([[0, s.Rational(1, n)], [s.Rational(1, n), 0]])
    zeta = np.exp(2j*np.pi/n)
    Smat = np.array([[zeta**(-b(v, w))/n for w in labels] for v in labels])
    Tmat = np.diag([zeta**q(v) for v in labels])
    # Partial Fourier columns |x,k> =sum_y zeta^(k*y)|x,y>/sqrt(n).
    F = np.zeros((121, 121), dtype=complex)
    for x, k in labels:
        for y in range(n):
            F[pos[(x, y)], pos[(x, k)]] = zeta**(k*y)/np.sqrt(n)
    Sperm, Tperm = np.zeros_like(F), np.zeros_like(F)
    for x, k in labels:
        Sperm[pos[(k, -x % n)], pos[(x, k)]] = 1
        Tperm[pos[(x, (k+x) % n)], pos[(x, k)]] = 1
    errS = float(np.max(abs(F.conj().T@Smat@F-Sperm)))
    errT = float(np.max(abs(F.conj().T@Tmat@F-Tperm)))
    assert max(errS, errT) < 1e-12
    assert float(np.max(abs(np.linalg.matrix_power(Smat@Tmat, 3)-Smat@Smat))) < 1e-12
    Rmat, Rperm = np.zeros_like(F), np.zeros_like(F)
    for x, y in labels:
        Rmat[pos[(3*x % n, 4*y % n)], pos[(x, y)]] = 1
        Rperm[pos[(3*x % n, 3*y % n)], pos[(x, y)]] = 1
    errR = float(np.max(abs(F.conj().T@Rmat@F-Rperm)))
    assert errR < 1e-12
    def sign_class(v):
        v = tuple(a % n for a in v)
        return min(v, tuple(-a % n for a in v))
    sixty = sorted({sign_class(v) for v in labels if v != (0, 0)})
    assert len(sixty) == 60
    ix = {v: i for i, v in enumerate(sixty)}
    gs = tuple(ix[sign_class((v[1], -v[0]))] for v in sixty)
    gt = tuple(ix[sign_class((v[0], v[0]+v[1]))] for v in sixty)
    identity = tuple(range(60))
    permutations, queue = {identity}, [identity]
    for current in queue:
        for generator in (gs, gt):
            following = tuple(generator[current[i]] for i in range(60))
            if following not in permutations:
                permutations.add(following)
                queue.append(following)
    assert len(permutations) == 660
    assert len({g[0] for g in permutations}) == 60
    assert sum(g[0] == 0 for g in permutations) == 11
    right_C5 = tuple(ix[sign_class((3*v[0], 3*v[1]))] for v in sixty)
    assert all(right_C5[gs[i]] == gs[right_C5[i]] and
               right_C5[gt[i]] == gt[right_C5[i]] for i in range(60))
    right_orbits = {frozenset(ix[sign_class((pow(3, k, n)*v[0], pow(3, k, n)*v[1]))]
                             for k in range(5)) for v in sixty}
    assert len(right_orbits) == 12 and all(len(o) == 5 for o in right_orbits)
    def direction(v):
        return (1, v[1]*pow(v[0], -1, n) % n) if v[0] else (0, 1)
    assert len({direction(v) for v in sixty}) == 12
    assert all(len({direction(sixty[i]) for i in o}) == 1 for o in right_orbits)
    # Reuse and validate the parallel matrix/coset dictionary rather than
    # rediscovering its660-flag bijection. g*C11 is labeled by first column +/-.
    source = ROOT/'data/toe_20261117_11cell_660flags_11faces_60Klein_bifactor.json'
    peer = json.loads(source.read_text(encoding='utf-8'))
    correspondence = {}
    for row in peer['explicit_flag_table']:
        a, _, c, _ = row['PSL2_11_matrix']
        point = row['Klein_60point_orbit_id']
        v = sign_class((a, c))
        if point in correspondence:
            assert correspondence[point] == v
        correspondence[point] = v
    assert len(correspondence) == 60 and set(correspondence.values()) == set(sixty)
    return dict(finite_quadratic_group='Z11 x Z11', q='q(x,y)=x*y/11 mod1',
                K_matrix=[[0, 11], [11, 0]], topological_label_count=121,
                q_value_multiplicities=dict(counts), normalized_Gauss_sum=1,
                auxiliary_model='Untwisted quantum double D(Z11), equivalently the '
                    'Abelian Chern-Simons K-matrix11*sigma_x.',
                partial_Fourier_transform='|x,k>=11^(-1/2) sum_y zeta11^(k*y)|x,y>',
                modular_S_on_Fourier_labels='(x,k)->(k,-x)',
                modular_T_on_Fourier_labels='(x,k)->(x,k+x)',
                Fourier_S_error=errS, Fourier_T_error=errT,
                inherited_C5_Fourier_error=errR,
                inherited_C5_on_linking_coordinates='(x,y)->(3x,4y)',
                inherited_C5_on_Fourier_coordinates='(x,k)->(3x,3k)',
                commuting_right_C5_orbit_count=12,
                right_normalizer_bridge='The inherited linking symmetry becomes scalar3 '
                    'on Fourier labels, commuting with the left PSL2(11) action. On '
                    'g*C11 this is right multiplication by diag(3,4). Its12 orbits of5 '
                    'are P1(F11), matching the12 SylowC11 subgroups and their5 Klein points.',
                charge_conjugation_even_dimension=61,
                nonzero_even_orbit_dimension=60, permutation_group_order=660,
                point_stabilizer_order=11,
                parallel_Klein_point_to_sign_vector={str(k): list(v) for k, v in correspondence.items()},
                validated_parallel_dictionary=str(source.relative_to(ROOT)),
                bridge='The60 nonzero vectors modulo sign carry PSL2(11)/C11. '
                    'This is equivariantly the parallel60-point Klein-cubic orbit. '
                    'Removing the origin from the charge-conjugation-even modular '
                    'module realizes exactly that permutation action.',
                limits='This auxiliary modular action is not an isometry group of Y/C11; '
                    'its inherited geometric normalizer quotient is onlyC5. These60 '
                    'Fourier-even states are not60 particle species. The121 labels are '
                    'only the11-primary quadratic model, not all363 flat C-field sectors. '
                    'No physical anyon realization or universal quantum computer derived.')


if __name__ == '__main__':
    result = dict(status='PASS', topology=cyclic_integral_topology(),
                  Wilson=wilson_line_test(), E6_faithful_control=faithful_E6_control(),
                  tradeoff=protected_and_topological_tradeoff(),
                  linking_quantum_model=linking_quantum_double_and_Klein_orbit(),
                  scope='A distinct smooth SUSY geometry with a conditional SM gauge '
                    'centralizer. No chiral SM, dynamical gauge completion or TOE solved.')
    out = ROOT/'data/toe_20261118_klein_C11_Wilson_and_linking.json'
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], C11_flat_C_sectors=result['topology']['flat_sector_count'],
                         SM_centralizer=result['Wilson']['centralizer_dimension'],
                         volume=result['tradeoff']['volume_over_S7'])))
