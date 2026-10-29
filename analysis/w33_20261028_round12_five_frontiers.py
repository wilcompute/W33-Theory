#!/usr/bin/env python3
"""Five independent W33 frontiers, 28 October 2026.

1. One-loop shared-kernel charge selection: rigorous dependence on matter weights.
2. Ternary Bloch exception census and a one-cosine *finite-grid* candidate.
3. Entire infinite-flux three-loop rotor: analytic global energy lower bound.
4. Integral reflection eigensublattice: nontrivial Z2 gluing.
5. Natural H4 -> E6 Weyl/root embedding obstruction and trace-lattice invariants.

No full continuous-Brillouin minimum, matter determinant, Lorentzian gravity,
or derivation of physical coupling ratios is claimed.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import sqrt
from pathlib import Path
import json
import sys

import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261028_three_mixed_loop_minimal_maxwell import (
    bloch_row, rank_mod,
)

R = s.Matrix([[1,0,5,-5,1,0],
              [0,1,-1,0,1,0],
              [0,0,5,-5,0,1]])
M = s.Matrix([[10,5,-6,0],
              [5,10,0,-6],
              [-6,0,12,-6],
              [0,-6,-6,12]])
REF = s.Matrix([[-1,0,0,0],
                [1,1,0,0],
                [-1,0,1,0],
                [0,0,0,1]])
ELECTRIC_G = s.Matrix([[794,-42,768],[-42,22,-52],[768,-52,766]])
CHARGES = [(1,1),(-3,1),(5,1),(-2,-2),(2,-2),(0,4)]
MULTIPLICITIES = [10,5,1,5,5,1]
WEIGHTS = ([F(1,10000)]*3
           + [F(49937,630000),F(21313,378000),F(49241,1350000),
              F(1241,90000),F(142189,3150000),F(1,56)])


def to_int_matrix(mat):
    return [[int(x) for x in row] for row in mat.tolist()]


def matter_response():
    # Identical 27-site Peierls response for each internal species implies
    # Pi_ab(z)=F(z)*sum(dim_species*q_a*q_b).
    Q = s.Matrix(CHARGES)
    Dim = s.diag(*MULTIPLICITIES)
    T = Q.T*Dim*Q
    assert T == s.diag(120,72)
    # Explicit family of species-dependent response factors: change only
    # the 10_(1,1) kernel by eta. The cubic charge Ward identities still hold.
    eta = s.symbols("eta")
    D = s.diag(1+eta,1,1,1,1,1)
    Teta = Q.T*Dim*D*Q
    assert Teta == s.Matrix([[120+10*eta,10*eta],
                             [10*eta,72+10*eta]])
    assert Teta.subs(eta,1)==s.Matrix([[130,10],[10,82]])
    return {
        "status": "EXACT_SHARED_KERNEL_RESPONSE_AND_MASS_SPLITTING_CONTROL",
        "equal_kernel_quadratic_trace":to_int_matrix(T),
        "different_10_multiplet_kernel": "T(eta)=[[120+10eta,10eta],[10eta,72+10eta]]",
        "eta_1_response": to_int_matrix(Teta.subs(eta,1)),
        "eta_1_diagonal_ratio": "65/41",
        "conditional_result": ("For a common 27-site spatial response function F(z), "
            "Pi_ab(z)=F(z)T_ab. Unequal species kernels permit nonzero mixed "
            "response and different diagonal ratio without changing charge "
            "neutrality of the E6 cubic."),
        "parity_selection": ("The previously certified reflection sends "
             "H(theta)=H0+theta J to H(-theta). A reflection-preserving "
             "regulator and vacuum imply theta=0 in this affine family; "
             "theta=+/-2 requires breaking or an anomaly."),
        "missing": ("Actual charged one-loop determinant with native cubic "
            "mass spectrum and six magnetic commutators. This calculation "
            "is a no-identifiability control, NOT a selected theta.")
    }


def _native_rows():
    faces = json.loads((ROOT / "data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json").read_text())
    cover = json.loads((ROOT / "data/w33_pass11991_native_four_period_cover.json").read_text())
    loops = json.loads((ROOT / "data/w33_20261027_native_bloch_face_module.json").read_text())
    return ([x["boundary"] for x in faces["independent_face_basis"]],
            cover["primitive_integer_edge_voltages"],
            loops["commutator_boundaries"])


def _character_rows(exponents, roots, prime, short, volts, loops):
    z = [roots[int(x)] for x in exponents]
    front = [bloch_row(face,volts,z,prime) for face in short]
    six = [bloch_row(face,volts,z,prime) for face in loops]
    mixed = [[sum(int(R[a,j])*six[j][e] for j in range(6)) % prime
              for e in range(135)] for a in range(3)]
    return front,six,mixed


def _prime_root(prime,order):
    for k in range(2,prime):
        if pow(k,order,prime)==1 and all(pow(k,j,prime)!=1 for j in range(1,order)):
            return [pow(k,j,prime) for j in range(order)]
    raise AssertionError("No primitive root of requested order")


def torus_grid():
    short,volts,loops = _native_rows()
    assert len(short)==105 and len(volts)==135 and len(loops)==6
    independent = []
    expected = {
        (1,1,0,0),(2,2,0,0),(1,1,1,0),(2,2,2,0),
        (1,1,0,1),(2,2,0,2),(0,0,2,1),(0,0,1,2),
        (1,1,2,1),(2,2,1,2)
    }
    for prime in (103,109):
        roots = _prime_root(prime,3)
        histogram = {}
        exceptions = []
        for exps in product(range(3),repeat=4):
            front,six,mixed = _character_rows(exps,roots,prime,short,volts,loops)
            r = rank_mod(front+mixed,prime)
            histogram[str(r)] = histogram.get(str(r),0)+1
            if exps != (0,0,0,0) and r < 108:
                assert r==107 and rank_mod(front+six,prime)==108
                assert (exps[0]+exps[3])%3 !=0
                # A single translated difference of *original commutator0*
                # in deck direction (1,0,0,1) lifts the missing rank here.
                assert rank_mod(front+mixed+[six[0]],prime)==108
                exceptions.append(exps)
        assert histogram == {"105":1,"108":70,"107":10}
        assert set(exceptions)==expected
        independent.append({"prime":prime,"roots":roots,
                            "histogram":histogram,
                            "exception_exponents": [list(e) for e in exceptions],
                            "one_cosine_repairs_every_third_root_defect":True})
    # Bad prime warning: an isolated 5-torsion modular defect at prime101
    # does not survive prime151 or181. This is not a complex spectral zero.
    prime_artifact = []
    for prime in (101,151,181):
        roots = _prime_root(prime,5)
        front,six,mixed = _character_rows((4,0,3,3),roots,prime,short,volts,loops)
        r = rank_mod(front+mixed,prime)
        assert r == (107 if prime==101 else 108)
        assert rank_mod(front+six,prime)==108
        prime_artifact.append({"prime":prime,"mixed_rank":r,"six_rank":108})
    return {
        "status": "TWO_PRIME_EXACT_THIRD_ROOT_CENSUS_ONE_TERM_FINITE_GRID_CANDIDATE",
        "order_three_character_count":81,
        "two_prime_controls":independent,
        "candidate_single_extra_cosine":
            "epsilon*(1-cos(f_0(x+e_0+e_3)-f_0(x)))",
        "one_term_grid_result":("Repairs all ten nongauge exceptions on the "
            "complete 81-point third-root character grid at primes103,109."),
        "order_five_bad_prime_control":prime_artifact,
        "critical":("No continuous Brillouin-torus kernel theorem for one "
            "term. Extra exceptional characters can exist at other roots "
            "and nontorsion momentum. The proven twelve-cosine all-momentum "
            "repair remains the valid full-kernel construction.")
    }



def one_term_exact_falsifier():
    """Exact unitary nongauge character where one translated loop is inert."""
    source=json.loads((ROOT/"data/w33_pass12341_12345_geometry.json").read_text())
    W=s.Matrix(source["symbol"]["period_matrix"])
    N=s.Matrix(source["symbol"]["N"])
    assert W==s.Matrix([[0,1,1,-1],[-1,0,1,-1],
                        [0,0,1,-1],[0,0,1,0]])
    assert N==s.Matrix([[10,-5,1,-6],[-5,10,-5,6],
                        [1,-5,10,-6],[-6,6,-6,12]])
    a=(-1+2*s.I*s.sqrt(30))/11
    b=(1+2*s.I*s.sqrt(30))/11
    z=[s.Integer(1),a,b,s.Integer(1)]
    assert s.simplify(a*s.conjugate(a))==1
    assert s.simplify(b*s.conjugate(b))==1
    h=[s.prod(z[j]**int(W[k,j]) for j in range(4)) for k in range(4)]
    assert [s.simplify(x) for x in h]==[-1,b,b,b]
    d=s.Matrix([u-1 for u in h])
    Q=s.simplify((d.T*N*d)[0]/2)
    assert Q==0
    assert s.simplify(5*(a*b-1)**2-10*(a*b-1)*(b-1)+11*(b-1)**2)==0
    assert s.simplify(z[0]*z[3])==1
    return {
      "status":"EXACT_UNITARY_COUNTEREXAMPLE_TO_ONE_TRANSLATED_COSINE",
      "original_character":["1","(-1+2i sqrt(30))/11",
                            "(1+2i sqrt(30))/11","1"],
      "loop_characters":["-1","(1+2i sqrt(30))/11",
                         "(1+2i sqrt(30))/11","(1+2i sqrt(30))/11"],
      "Q_equals_zero_exact":True,
      "translation_e0_plus_e3_factor_equals_one_exact":True,
      "full_unrepaired_magnetic_rank":107,
      "single_cosine_magnetic_rank":107,
      "full_six_commutator_rank":108,
      "rank_scope":("Rank conclusions apply via the already-committed "
            "Pass12341 global Laurent-minor theorem; this function "
            "independently checks its exact Q polynomial at this point."),
      "conclusion":"One cosine fixes the 81 third-root grid but fails globally."
    }

def rotor_exact():
    G = ELECTRIC_G
    minors = [(G-7*s.eye(3))[:n,:n].det() for n in (1,2,3)]
    assert minors == [787,10041,335]
    assert all(x>0 for x in minors)
    # Integer vectors with Euclidean norm²>=4 have G norm²>7*4=28.
    # For norm²<=3 exhaustive 26 nonzero vectors in {-1,0,1}³.
    vals = sorted((int((s.Matrix(u).T*G*s.Matrix(u))[0]),u)
                  for u in product((-1,0,1),repeat=3) if u!=(0,0,0))
    assert vals[0][0]==22 and vals[:2]==[(22,(0,-1,0)),(22,(0,1,0))]
    W=sum(WEIGHTS)
    b_squared=sum(w*w for w in WEIGHTS)/2
    assert W==F(7009,28125) and b_squared==F(297803260427,44651250000000)
    g=F(1,5)
    alpha=11*g*g
    lower=(float(W)+float(alpha)
           -sqrt((float(W)-float(alpha))**2+4*float(b_squared)))/2
    assert 0.2190<lower<0.2191
    return {"status":"RIGOROUS_ENTIRE_THREE_ROTOR_FLUX_GROUND_ENERGY_INTERVAL",
        "electric_gram":to_int_matrix(G),
        "G_minus_7I_leading_minors":[int(x) for x in minors],
        "smallest_nonzero_integer_flux_norm_squared":22,
        "global_integer_minimizers":[list(x) for value,x in vals if value==22],
        "potential_weight_sum":str(W),
        "coupling_vector_norm_squared":str(b_squared),
        "g":"1/5",
        "excited_flux_sector_kinetic_lower":str(alpha),
        "lower_bound_numeric_for_exact_algebraic_formula":lower,
        "upper_bound_exact":str(W),
        "proof":("P=|m=0><m=0|. PHP=W. QHQ>=T_Q>=11g² "
            "since the positive cosine potential is nonnegative. "
            "||QHP||²=sum(w_a²)/2, since all 9 integer charges have "
            "different +/- pairs. The lower 2x2 Schur comparison "
            "[[W,-b],[-b,11g²]] gives an exact algebraic bound. "
            "Trial state |0> gives E0<=W."),
        "boundary":("Rigorous infinite electric-flux *three-rotor* energy "
            "interval at a supplied g, not an infinite-spatial-lattice "
            "gauge mass gap or physical bound.")
    }


def parity_gluing():
    E=s.Matrix.hstack(s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0]),
                      s.Matrix([0,0,0,1]),s.Matrix([2,-1,1,0]))
    assert REF*REF==s.eye(4) and REF.T*M*REF==M
    assert E.det()==-2
    assert REF*E == E*s.diag(1,1,1,-1)
    metric=E.T*M*E
    assert metric==s.Matrix([[10,0,-6,0],[0,12,-6,0],
                             [-6,-6,12,0],[0,0,0,18]])
    return {"status":"EXACT_INDEX_TWO_Z2_PARITY_GLUE_ON_NATIVE_PERIOD_LATTICE",
        "even_sublattice_basis":[[0,1,0,0],[0,0,1,0],[0,0,0,1]],
        "odd_primitive_generator":[2,-1,1,0],
        "stacked_integer_basis_det":-2,
        "quotient":"Z^4/(Lambda_even+Lambda_odd) = Z/2",
        "even_gram":[[10,0,-6],[0,12,-6],[-6,-6,12]],
        "odd_norm_squared":18,
        "restriction":("The real eigenspaces are orthogonal but their "
            "integer eigensublattices do not span the whole period "
            "lattice. A naive untwisted direct-sum reduction misses an "
            "index-two coset. Orbifold twisted sectors and physical "
            "time direction are NOT derived.")
    }


def root_intertwiner_falsifier():
    H4_order=14400;E6_order=51840
    assert E6_order%H4_order !=0 and E6_order%7200 !=0
    trace=s.diag(120,72)
    U=s.Matrix([[1,0],[1,1]])
    assert U.det()==1 and U*trace*U.T==s.Matrix([[120,120],[120,192]])
    assert smith_normal_form(trace,domain=ZZ)==s.diag(24,360)
    return {"status":"DIRECT_H4_TO_E6_WEYL_AND_ROOT_SUBSYSTEM_NO_GO",
        "H4_Weyl_order":H4_order,"E6_Weyl_order":E6_order,
        "H4_rotation_order":7200,
        "Lagrange_no_full_Weyl_group_embedding":True,
        "Lagrange_no_rotation_subgroup_embedding":True,
        "root_obstruction":("A normalized H4 Coxeter simple-root pair "
            "at the order-5 bond has dot product -cos(pi/5), irrational "
            "in Q(sqrt5); E6 equal-length crystallographic root products "
            "are rational (in the usual norm-2 convention integers). "
            "No isometric H4 root subsystem inside E6 roots."),
        "charge_trace":to_int_matrix(trace),
        "GL2Z_rebasis":to_int_matrix(U),
        "rebased_trace":to_int_matrix(U*trace*U.T),
        "charge_trace_determinant":8640,
        "charge_trace_Smith_invariants":[24,360],
        "basis_dependent_5_over_3_diagonal_ratio":True,
        "not_ruled_out":("Correspondences mediated by E8, irrational "
            "icosian projection, representations, or nonfaithful maps "
            "whose definitions are explicitly supplied.")
    }


def run():
    return {"schema":"w33.toe.20261028.five.frontiers.round12",
        "matter":matter_response(),
        "repair":torus_grid(),
        "repair_one_term_counterexample":one_term_exact_falsifier(),
        "rotor":rotor_exact(),
        "parity":parity_gluing(),
        "intertwiner":root_intertwiner_falsifier()}


if __name__=="__main__":
    data=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(data,encoding="utf8")
    else:print(data,end="")
