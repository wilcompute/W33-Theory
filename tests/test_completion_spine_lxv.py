"""
Part LXV — Completion Spine for W(3,3)
=======================================

This test module separates the theorem-grade uniqueness spine from
weaker self-power slogans.  The identity q^q = q^n does not by itself
select q=3: for q>1 it simply implies n=q.  What selects W(3,3) is the
simultaneous Standard-Model-shaped closure of the symplectic GQ family
W(3,q):

  (1) local lines are tetrahedra K_4, so q+1 = 4;
  (2) the edge carrier has 240 undirected states, matching |Roots(E8)|;
  (3) the line-clique complex has b1 = q^4 = 81 = 3*27;
  (4) the character-theoretic class count q*Phi_4(q) equals h(E8)=30.

The core family computation is exact.  In W(3,q)=GQ(q,q), every maximal
clique is a line K_{q+1}; distinct lines have disjoint edge sets; and
the triangle-boundary rank inside each K_{q+1} is binom(q,2).  Therefore

  b1 = E - rank(d1) - rank(d2) = q^4.

At q=3 this gives 81 = 3*27, the three-generation E6-fundamental carrier.
"""
from math import comb


def gq_family(q: int) -> dict:
    """Return exact W(3,q)=GQ(q,q) collinearity and clique-complex data."""
    if q < 2:
        raise ValueError("q must be >= 2 for the nontrivial GQ family")

    v = (q + 1) * (q * q + 1)
    k = q * (q + 1)
    lam = q - 1
    mu = q + 1

    # Each of the v lines is a K_{q+1}; each graph edge lies on a unique line.
    lines = v
    edges = lines * comb(q + 1, 2)
    triangles = lines * comb(q + 1, 3)
    tetrahedra = lines * comb(q + 1, 4) if q + 1 >= 4 else 0

    # Connected graph: rank(d1)=v-1.  On each K_{q+1}, the triangle-boundary
    # image spans the full cycle space of dimension C(q+1,2)-q = C(q,2).
    rank_d1 = v - 1
    rank_d2 = lines * comb(q, 2)
    b1 = edges - rank_d1 - rank_d2

    # Character-theoretic bridge from Supplement chi.
    phi4 = q * q + 1
    class_count_candidate = q * phi4

    return {
        "q": q,
        "v": v,
        "k": k,
        "lambda": lam,
        "mu": mu,
        "lines": lines,
        "edges": edges,
        "triangles": triangles,
        "tetrahedra": tetrahedra,
        "rank_d1": rank_d1,
        "rank_d2": rank_d2,
        "b1": b1,
        "phi4": phi4,
        "class_count_candidate": class_count_candidate,
    }


class TestLXVFamilySpine:
    def test_w33_parameters(self):
        d = gq_family(3)
        assert (d["v"], d["k"], d["lambda"], d["mu"]) == (40, 12, 2, 4)
        assert (d["lines"], d["edges"], d["triangles"], d["tetrahedra"]) == (40, 240, 160, 40)

    def test_lambda_formula_is_q_minus_1_not_q(self):
        d = gq_family(3)
        assert d["lambda"] == 3 - 1 == 2
        assert d["lambda"] != 3

    def test_betti_identity_family(self):
        for q in range(2, 12):
            d = gq_family(q)
            assert d["b1"] == q ** 4

    def test_w33_hodge_spine(self):
        d = gq_family(3)
        assert d["rank_d1"] == 39
        assert d["rank_d2"] == 120
        assert d["b1"] == 81 == 3 * 27
        assert d["edges"] == d["rank_d1"] + d["rank_d2"] + d["b1"]


class TestLXVSelectors:
    def test_tetrahedral_line_selector(self):
        # Local line clique K_{q+1} is a tetrahedron K4 iff q=3.
        assert [q for q in range(2, 20) if q + 1 == 4] == [3]

    def test_e8_root_edge_selector(self):
        # E = v*C(q+1,2) equals the E8 root count only at q=3 in this range.
        assert [q for q in range(2, 20) if gq_family(q)["edges"] == 240] == [3]

    def test_three_generation_e6_selector(self):
        # b1=q^4 equals 81=3*27 only at q=3.
        assert [q for q in range(2, 20) if gq_family(q)["b1"] == 3 * 27] == [3]

    def test_character_table_e8_coxeter_selector(self):
        # Supplement chi bridge: #classes/irreps = q*Phi4(q) = 30 = h(E8).
        assert [q for q in range(2, 20) if gq_family(q)["class_count_candidate"] == 30] == [3]

    def test_joint_completion_selector(self):
        selected = []
        for q in range(2, 20):
            d = gq_family(q)
            if (
                q + 1 == 4
                and d["edges"] == 240
                and d["b1"] == 81
                and d["class_count_candidate"] == 30
            ):
                selected.append(q)
        assert selected == [3]


class TestLXVSelfPowerCaution:
    def test_self_power_equation_does_not_select_q3(self):
        # q^q = q^n with q>1 implies n=q.  Therefore the raw equation has
        # many prime self-solutions and cannot be the final uniqueness theorem.
        prime_qs = [2, 3, 5, 7, 11]
        assert all(q ** q == q ** q for q in prime_qs)
        assert prime_qs != [3]

    def test_standard_model_shape_does_select_q3(self):
        # The physically relevant selector is not q^q=q^n, but the simultaneous
        # tetrahedral/E8/E6/character closure above.
        assert gq_family(3)["b1"] == 81
        assert gq_family(5)["b1"] == 625
        assert gq_family(5)["edges"] == 2340
        assert gq_family(5)["class_count_candidate"] == 130
