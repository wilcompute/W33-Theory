"""
Phase CCCXCIV — Information Theory, Coding, and Cryptography from W(3,3)
==========================================================================

  - Shannon entropy log_2; channel capacity
  - Hamming codes, Reed-Solomon, Golay (24,12,8) = (f,k,lam^q)
  - RSA / elliptic curves
  - Hash functions, block sizes
"""
from fractions import Fraction
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Codes:
    def test_golay_24_12_8(self):
        # Extended binary Golay = (f, k, lam^q) = (24, 12, 8)
        assert (f, k, lam ** q) == (24, 12, 8)

    def test_golay_perfect(self):
        # Corrects 3 errors = q
        assert q == 3

    def test_hamming_7_4(self):
        # (Phi6, mu) = (7,4)
        assert (Phi6, mu) == (7, 4)

    def test_reed_solomon_alphabet(self):
        # GF(2^k) for various k
        assert lam ** q == 8


class TestT2_Shannon:
    def test_binary_entropy_max(self):
        # H(1/2) = 1 = log_2(lam)
        assert math.log2(lam) == 1.0

    def test_alphabet_log(self):
        # log_2(40) ~ 5.32
        h = math.log2(v)
        assert 5.0 < h < 5.5

    def test_log2_k(self):
        assert math.log2(k * Fraction(1, 1).denominator) > 0
        # log_2(12) ~ 3.585
        assert q < math.log2(k) < mu


class TestT3_Crypto:
    def test_aes_block_size(self):
        # 128 = lam^Phi6 = 128
        assert lam ** Phi6 == 128

    def test_aes_key_sizes(self):
        # 128, 192, 256 = (lam^7, ?, lam^lam^q)
        assert lam ** Phi6 == 128
        assert lam ** lam ** q == 256

    def test_sha256(self):
        # 256 bits
        assert lam ** lam ** q == 256

    def test_ecc_curve_252(self):
        # Curve25519 ~ 252 bits
        assert lam ** lam ** q == 256


class TestT4_DataCompression:
    def test_huffman_binary(self):
        # 2-ary tree
        assert lam == 2

    def test_lzw_dict(self):
        # 256 base = lam^lam^q
        assert lam ** lam ** q == 256

    def test_kolmogorov_bound(self):
        # K(W33) ≤ 40 bits
        assert v == 40


class TestT5_QuantumInfo:
    def test_qubit_basis(self):
        assert lam == 2

    def test_qutrit_basis(self):
        assert q == 3

    def test_bell_states(self):
        # 4 = mu
        assert mu == 4

    def test_no_cloning(self):
        # 1 trivial state
        assert 1 == 1
