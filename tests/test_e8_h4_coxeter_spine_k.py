"""
Supplement K - Common Coxeter spine of E8 and H4.

This test suite records the sharper bridge behind Supplement J:
E8 and H4 share Coxeter number h=30, the H4 degree sequence embeds
inside the E8 degree sequence, and both sequences are generated from
the same W(3,3) constants.
"""
from math import prod


q = 3
v, k, lam, mu = 40, 12, 2, 4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7

h = q * Phi4
rank_e8 = k - mu
rank_h4 = mu

E8_DEGREES = (
    lam,
    k - mu,
    k,
    Phi3 + 1,
    k + mu + lam,
    E // k,
    f,
    h,
)
H4_DEGREES = (
    lam,
    k,
    E // k,
    h,
)

E8_EXPONENTS = tuple(d - 1 for d in E8_DEGREES)
H4_EXPONENTS = tuple(d - 1 for d in H4_DEGREES)


class TestK1SharedCoxeterNumber:
    def test_h_is_w33_generated(self):
        assert h == q * Phi4 == 30

    def test_e8_rank_is_w33_gap(self):
        assert rank_e8 == k - mu == 8

    def test_h4_rank_is_w33_mu(self):
        assert rank_h4 == mu == 4

    def test_e8_root_shell_from_rank_times_h(self):
        assert rank_e8 * h == E == 240

    def test_h4_root_shell_from_rank_times_h(self):
        assert rank_h4 * h == E // 2 == 120


class TestK2E8CoxeterData:
    def test_e8_degrees_from_w33_constants(self):
        assert E8_DEGREES == (2, 8, 12, 14, 18, 20, 24, 30)

    def test_e8_exponents(self):
        assert E8_EXPONENTS == (1, 7, 11, 13, 17, 19, 23, 29)

    def test_e8_positive_roots_sum_exponents(self):
        assert sum(E8_EXPONENTS) == E // 2 == 120

    def test_e8_roots_rank_h(self):
        assert rank_e8 * (max(E8_EXPONENTS) + 1) == E

    def test_e8_weyl_order_product_degrees(self):
        assert prod(E8_DEGREES) == 696_729_600


class TestK3H4CoxeterData:
    def test_h4_degrees_from_w33_constants(self):
        assert H4_DEGREES == (2, 12, 20, 30)

    def test_h4_exponents(self):
        assert H4_EXPONENTS == (1, 11, 19, 29)

    def test_h4_positive_roots_sum_exponents(self):
        assert sum(H4_EXPONENTS) == E // 4 == 60

    def test_h4_roots_rank_h(self):
        assert rank_h4 * (max(H4_EXPONENTS) + 1) == E // 2

    def test_h4_order_product_degrees(self):
        assert prod(H4_DEGREES) == 14_400


class TestK4EmbeddingPattern:
    def test_h4_degrees_embed_in_e8_degrees(self):
        assert set(H4_DEGREES).issubset(set(E8_DEGREES))

    def test_h4_exponents_embed_in_e8_exponents(self):
        assert set(H4_EXPONENTS).issubset(set(E8_EXPONENTS))

    def test_visible_h4_degrees_are_w33_local_spine(self):
        visible = (lam, k, E // k, h)
        assert visible == H4_DEGREES

    def test_hidden_e8_degrees_complete_the_rank8_shell(self):
        hidden = tuple(d for d in E8_DEGREES if d not in H4_DEGREES)
        assert hidden == (8, 14, 18, 24)

    def test_hidden_product_is_weyl_order_ratio(self):
        assert prod(E8_DEGREES) // prod(H4_DEGREES) == prod((8, 14, 18, 24))


class TestK5GroupOrderClosure:
    def test_weyl_order_ratio(self):
        assert prod(E8_DEGREES) // prod(H4_DEGREES) == 48_384

    def test_ratio_is_w33_factorization(self):
        assert 48_384 == lam ** (k - mu) * q ** q * Phi6

    def test_ratio_factorizes_by_rank_cycle_and_phi6(self):
        assert 48_384 == 2**8 * 3**3 * 7

    def test_e8_to_h4_root_ratio_is_two(self):
        assert (rank_e8 * h) // (rank_h4 * h) == 2

    def test_coxeter_spine_summary(self):
        spine = {
            "h": h,
            "E8_roots": rank_e8 * h,
            "H4_roots": rank_h4 * h,
            "E8_degrees": E8_DEGREES,
            "H4_degrees": H4_DEGREES,
        }
        assert spine["h"] == 30
        assert spine["E8_roots"] == 240
        assert spine["H4_roots"] == 120
        assert set(spine["H4_degrees"]).issubset(spine["E8_degrees"])
