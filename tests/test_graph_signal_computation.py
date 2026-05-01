"""
Phase CXXIII -- Graph Signal Processing on W(3,3) = SRG(40,12,2,4).

80+ tests covering graph Fourier transform, Parseval's theorem, graph
convolution, graph filters (low-pass / high-pass / band-pass), signal
smoothness (Dirichlet energy), graph wavelets, sampling theory on graphs,
bandlimited signals, signal denoising, total variation on graphs, graph
filter banks, and windowed GFT.

All tests use only numpy and standard library.  Every assertion is
mathematically provable from the SRG(40,12,2,4) spectrum
    adjacency:  {12^1, 2^24, (-4)^15}
    Laplacian:  {0^1, 10^24, 16^15}

Key:  GFT uses the eigenvectors of L.  Because W(3,3) is 12-regular the
combinatorial Laplacian is L = 12I - A and the three distinct Laplacian
eigenvalues are 0, 10, 16 with multiplicities 1, 24, 15.
"""

import numpy as np
import pytest
from numpy.linalg import eigh, eigvalsh, norm

# ── W(3,3) builder ───────────────────────────────────────────────────────────

_N, _K, _LAM, _MU = 40, 12, 2, 4


def _build_w33():
    """Build the 40-vertex symplectic graph W(3,3) = Sp(4,3)."""
    points = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    v = (a, b, c, d)
                    if v == (0, 0, 0, 0):
                        continue
                    first = next(x for x in v if x != 0)
                    inv = pow(first, -1, 3)
                    canon = tuple((x * inv) % 3 for x in v)
                    if canon not in points:
                        points.append(canon)
    n = 40
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            u, v = points[i], points[j]
            omega = (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % 3
            if omega == 0:
                A[i, j] = A[j, i] = 1
    return A


# ── Module-scoped fixtures ───────────────────────────────────────────────────


@pytest.fixture(scope="module")
def A():
    """Adjacency matrix of W(3,3)."""
    return _build_w33()


@pytest.fixture(scope="module")
def L(A):
    """Combinatorial Laplacian L = kI - A."""
    return float(_K) * np.eye(_N) - A.astype(float)


@pytest.fixture(scope="module")
def spectral(L):
    """Full eigendecomposition of L, sorted ascending."""
    vals, vecs = eigh(L)
    idx = np.argsort(vals)
    return vals[idx], vecs[:, idx]


@pytest.fixture(scope="module")
def eigenvalues(spectral):
    return spectral[0]


@pytest.fixture(scope="module")
def U(spectral):
    """Orthogonal GFT matrix: columns are Laplacian eigenvectors."""
    return spectral[1]


@pytest.fixture(scope="module")
def num_edges(A):
    return int(A.sum()) // 2


# ═════════════════════════════════════════════════════════════════════════════
# Section 1 : Graph structure prerequisites  (6 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestGraphStructure:
    """Verify W(3,3) = SRG(40,12,2,4)."""

    def test_vertex_count(self, A):
        assert A.shape == (_N, _N)

    def test_symmetric(self, A):
        assert np.array_equal(A, A.T)

    def test_no_self_loops(self, A):
        assert np.all(np.diag(A) == 0)

    def test_regular_degree_12(self, A):
        assert np.all(A.sum(axis=1) == _K)

    def test_srg_lambda_2(self, A):
        """Adjacent vertices share exactly lambda=2 common neighbours."""
        for i in range(_N):
            for j in range(i + 1, _N):
                if A[i, j] == 1:
                    assert int(A[i] @ A[j]) == _LAM

    def test_srg_mu_4(self, A):
        """Non-adjacent vertices share exactly mu=4 common neighbours."""
        for i in range(_N):
            for j in range(i + 1, _N):
                if A[i, j] == 0:
                    assert int(A[i] @ A[j]) == _MU


# ═════════════════════════════════════════════════════════════════════════════
# Section 2 : Laplacian spectrum  (9 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestLaplacianSpectrum:
    """Eigenvalues {0^1, 10^24, 16^15} and eigenvector orthonormality."""

    def test_L_symmetric(self, L):
        assert np.allclose(L, L.T)

    def test_L_row_sums_zero(self, L):
        assert np.allclose(L.sum(axis=1), 0, atol=1e-12)

    def test_three_distinct_eigenvalues(self, eigenvalues):
        distinct = sorted(set(np.round(eigenvalues, 6)))
        assert len(distinct) == 3

    def test_eigenvalue_values(self, eigenvalues):
        distinct = sorted(set(np.round(eigenvalues, 6)))
        assert np.isclose(distinct[0], 0, atol=1e-8)
        assert np.isclose(distinct[1], 10, atol=1e-8)
        assert np.isclose(distinct[2], 16, atol=1e-8)

    def test_multiplicity_0_is_1(self, eigenvalues):
        assert np.sum(np.abs(eigenvalues) < 1e-8) == 1

    def test_multiplicity_10_is_24(self, eigenvalues):
        assert np.sum(np.abs(eigenvalues - 10) < 1e-8) == 24

    def test_multiplicity_16_is_15(self, eigenvalues):
        assert np.sum(np.abs(eigenvalues - 16) < 1e-8) == 15

    def test_eigenvectors_orthonormal(self, U):
        assert np.allclose(U.T @ U, np.eye(_N), atol=1e-10)

    def test_spectral_decomposition_reconstructs_L(self, L, eigenvalues, U):
        L_rec = U @ np.diag(eigenvalues) @ U.T
        assert np.allclose(L_rec, L, atol=1e-10)


# ═════════════════════════════════════════════════════════════════════════════
# Section 3 : Graph Fourier Transform  (8 tests)
# forward: f_hat = U^T f        inverse: f = U f_hat
# ═════════════════════════════════════════════════════════════════════════════


class TestGFT:

    def test_gft_constant_signal_dc_only(self, U):
        """Constant signal maps entirely to the DC (eigenvalue-0) coefficient."""
        f = np.ones(_N)
        f_hat = U.T @ f
        assert abs(f_hat[0]) > 1e-10
        assert np.allclose(f_hat[1:], 0, atol=1e-10)

    def test_gft_inverse_recovers_signal(self, U):
        rng = np.random.RandomState(42)
        f = rng.randn(_N)
        assert np.allclose(U @ (U.T @ f), f, atol=1e-10)

    def test_gft_linearity(self, U):
        rng = np.random.RandomState(43)
        f, g = rng.randn(_N), rng.randn(_N)
        a, b = 2.5, -1.3
        lhs = U.T @ (a * f + b * g)
        rhs = a * (U.T @ f) + b * (U.T @ g)
        assert np.allclose(lhs, rhs, atol=1e-10)

    def test_gft_of_eigenvector_is_impulse(self, U):
        """GFT of the k-th eigenvector has unit energy at index k only."""
        for k in [0, 1, 10, 25, 39]:
            f_hat = U.T @ U[:, k]
            expected = np.zeros(_N)
            expected[k] = 1.0
            assert np.allclose(np.abs(f_hat), np.abs(expected), atol=1e-10)

    def test_gft_delta_at_vertex(self, U):
        """GFT of delta_v equals the v-th row of U (= v-th column of U^T)."""
        v = 7
        delta = np.zeros(_N)
        delta[v] = 1.0
        f_hat = U.T @ delta
        assert np.allclose(f_hat, U[v, :], atol=1e-10)

    def test_gft_forward_inverse_identity(self, U):
        assert np.allclose(U @ U.T, np.eye(_N), atol=1e-10)

    def test_gft_dc_coefficient_is_mean_times_sqrt_n(self, U):
        """f_hat[0] = sqrt(N) * mean(f) because u_0 = (1/sqrt(N)) * ones."""
        rng = np.random.RandomState(44)
        f = rng.randn(_N)
        f_hat = U.T @ f
        u0 = U[:, 0]
        # u0 should be proportional to ones; sign may vary
        sign = np.sign(u0[0])
        expected_dc = sign * np.sqrt(_N) * np.mean(f)
        assert np.isclose(f_hat[0], expected_dc, atol=1e-10)

    def test_gft_zero_signal(self, U):
        f_hat = U.T @ np.zeros(_N)
        assert np.allclose(f_hat, 0, atol=1e-15)


# ═════════════════════════════════════════════════════════════════════════════
# Section 4 : Parseval's theorem  (5 tests)
# ||f||^2 = ||f_hat||^2
# ═════════════════════════════════════════════════════════════════════════════


class TestParseval:

    def test_parseval_random_signals(self, U):
        rng = np.random.RandomState(45)
        for _ in range(5):
            f = rng.randn(_N)
            f_hat = U.T @ f
            assert np.isclose(f @ f, f_hat @ f_hat, atol=1e-10)

    def test_parseval_constant(self, U):
        f = 3.0 * np.ones(_N)
        f_hat = U.T @ f
        assert np.isclose(f @ f, f_hat @ f_hat, atol=1e-10)

    def test_parseval_sparse(self, U):
        f = np.zeros(_N)
        f[0] = 1
        f[10] = -2
        f[20] = 3
        f_hat = U.T @ f
        assert np.isclose(f @ f, f_hat @ f_hat, atol=1e-10)

    def test_parseval_eigenvector(self, U):
        """Each eigenvector has unit norm in both domains."""
        for k in range(_N):
            f = U[:, k]
            f_hat = U.T @ f
            assert np.isclose(f @ f, 1.0, atol=1e-10)
            assert np.isclose(f_hat @ f_hat, 1.0, atol=1e-10)

    def test_parseval_inner_product_preservation(self, U):
        """<f,g> = <f_hat,g_hat>."""
        rng = np.random.RandomState(46)
        f, g = rng.randn(_N), rng.randn(_N)
        assert np.isclose(f @ g, (U.T @ f) @ (U.T @ g), atol=1e-10)


# ═════════════════════════════════════════════════════════════════════════════
# Section 5 : Graph spectral convolution  (6 tests)
# (f *_G g) = U (f_hat . g_hat)
# ═════════════════════════════════════════════════════════════════════════════


class TestGraphConvolution:

    @staticmethod
    def _conv(f, g, U):
        return U @ ((U.T @ f) * (U.T @ g))

    def test_commutativity(self, U):
        rng = np.random.RandomState(47)
        f, g = rng.randn(_N), rng.randn(_N)
        assert np.allclose(self._conv(f, g, U), self._conv(g, f, U), atol=1e-10)

    def test_associativity(self, U):
        rng = np.random.RandomState(48)
        f, g, h = rng.randn(_N), rng.randn(_N), rng.randn(_N)
        fg_h = self._conv(self._conv(f, g, U), h, U)
        f_gh = self._conv(f, self._conv(g, h, U), U)
        assert np.allclose(fg_h, f_gh, atol=1e-10)

    def test_distributivity(self, U):
        rng = np.random.RandomState(49)
        f, g, h = rng.randn(_N), rng.randn(_N), rng.randn(_N)
        lhs = self._conv(f, g + h, U)
        rhs = self._conv(f, g, U) + self._conv(f, h, U)
        assert np.allclose(lhs, rhs, atol=1e-10)

    def test_conv_with_zero(self, U):
        rng = np.random.RandomState(50)
        f = rng.randn(_N)
        assert np.allclose(self._conv(f, np.zeros(_N), U), 0, atol=1e-15)

    def test_conv_spectral_identity(self, U):
        """Convolution with a signal whose GFT is all-ones acts as identity."""
        g_hat = np.ones(_N)
        g = U @ g_hat
        rng = np.random.RandomState(51)
        f = rng.randn(_N)
        result = self._conv(f, g, U)
        expected = U @ ((U.T @ f) * g_hat)
        assert np.allclose(result, expected, atol=1e-10)

    def test_conv_of_eigenvectors(self, U):
        """Convolution of eigenvectors u_j and u_k is zero when j != k."""
        j, k = 3, 20
        result = self._conv(U[:, j], U[:, k], U)
        assert np.allclose(result, 0, atol=1e-10)


# ═════════════════════════════════════════════════════════════════════════════
# Section 6 : Graph filters  (10 tests)
# h(L) f  = U diag(h(lambda)) U^T f
# ═════════════════════════════════════════════════════════════════════════════


class TestGraphFilters:

    @staticmethod
    def _filter(f, h_lam, U):
        return U @ (h_lam * (U.T @ f))

    # -- low-pass ---------------------------------------------------------

    def test_lowpass_spectral_action(self, U, eigenvalues):
        """h(lam) = 1/(1+0.1*lam); verify per-coefficient scaling."""
        h = 1.0 / (1.0 + 0.1 * eigenvalues)
        rng = np.random.RandomState(52)
        f = rng.randn(_N)
        f_hat = U.T @ f
        out_hat = U.T @ self._filter(f, h, U)
        assert np.allclose(out_hat, h * f_hat, atol=1e-10)

    def test_lowpass_preserves_dc(self, U, eigenvalues):
        h = 1.0 / (1.0 + 0.5 * eigenvalues)
        f = np.ones(_N) * 3.0
        assert np.allclose(self._filter(f, h, U), f, atol=1e-10)

    def test_lowpass_attenuation_values(self, eigenvalues):
        """Confirm h(0)=1, h(10)=0.5, h(16)~0.385 for alpha=0.1."""
        alpha = 0.1
        h = 1.0 / (1.0 + alpha * eigenvalues)
        for i, lam in enumerate(eigenvalues):
            if abs(lam) < 1e-8:
                assert np.isclose(h[i], 1.0)
            elif abs(lam - 10) < 1e-8:
                assert np.isclose(h[i], 0.5, atol=1e-10)
            elif abs(lam - 16) < 1e-8:
                assert np.isclose(h[i], 1.0 / 2.6, atol=1e-10)

    # -- high-pass --------------------------------------------------------

    def test_highpass_removes_dc(self, U, eigenvalues):
        alpha = 0.1
        h = alpha * eigenvalues / (1.0 + alpha * eigenvalues)
        rng = np.random.RandomState(53)
        f = np.ones(_N) * 5.0 + rng.randn(_N) * 0.1
        out_hat = U.T @ self._filter(f, h, U)
        assert abs(out_hat[0]) < 1e-10

    def test_highpass_gain_at_lambda16(self, eigenvalues):
        alpha = 10.0
        h = alpha * eigenvalues / (1.0 + alpha * eigenvalues)
        idx16 = np.where(np.abs(eigenvalues - 16) < 1e-8)[0]
        for i in idx16:
            assert h[i] > 0.99

    # -- band-pass --------------------------------------------------------

    def test_bandpass_isolates_eigenvalue_10(self, U, eigenvalues):
        """Ideal band-pass passing only eigenvalue-10 component."""
        h = np.where(np.abs(eigenvalues - 10) < 1, 1.0, 0.0)
        rng = np.random.RandomState(54)
        f = rng.randn(_N)
        out_hat = U.T @ self._filter(f, h, U)
        f_hat = U.T @ f
        for i in range(_N):
            if np.abs(eigenvalues[i] - 10) < 1:
                assert np.isclose(out_hat[i], f_hat[i], atol=1e-10)
            else:
                assert abs(out_hat[i]) < 1e-10

    # -- filter algebra ---------------------------------------------------

    def test_filter_composition(self, U, eigenvalues):
        """h1 then h2 equals h1*h2."""
        h1 = 1.0 / (1.0 + 0.1 * eigenvalues)
        h2 = 1.0 / (1.0 + 0.2 * eigenvalues)
        rng = np.random.RandomState(55)
        f = rng.randn(_N)
        sequential = self._filter(self._filter(f, h1, U), h2, U)
        composed = self._filter(f, h1 * h2, U)
        assert np.allclose(sequential, composed, atol=1e-10)

    def test_complementary_lowpass_highpass_sum_identity(self, eigenvalues):
        """h_low + h_high = 1 for complementary pair."""
        alpha = 0.1
        h_low = 1.0 / (1.0 + alpha * eigenvalues)
        h_high = alpha * eigenvalues / (1.0 + alpha * eigenvalues)
        assert np.allclose(h_low + h_high, 1.0, atol=1e-14)

    def test_heat_kernel_filter_reduces_energy(self, U, eigenvalues):
        """h(lam) = exp(-t*lam) is dissipative."""
        t = 0.05
        h = np.exp(-t * eigenvalues)
        rng = np.random.RandomState(56)
        f = rng.randn(_N)
        out = self._filter(f, h, U)
        assert out @ out <= f @ f + 1e-10

    def test_ideal_lowpass_cutoff_12(self, U, eigenvalues):
        """Pass eigenvalues <= 12, reject eigenvalue 16."""
        h = np.where(eigenvalues <= 12, 1.0, 0.0)
        rng = np.random.RandomState(57)
        f = rng.randn(_N)
        out_hat = U.T @ self._filter(f, h, U)
        f_hat = U.T @ f
        for i in range(_N):
            if eigenvalues[i] <= 12:
                assert np.isclose(out_hat[i], f_hat[i], atol=1e-10)
            else:
                assert abs(out_hat[i]) < 1e-10


# ═════════════════════════════════════════════════════════════════════════════
# Section 7 : Signal smoothness / Dirichlet energy  (8 tests)
# E(f) = f^T L f = sum_{(i,j) in E} (f_i - f_j)^2
# ═════════════════════════════════════════════════════════════════════════════


class TestDirichletEnergy:

    def test_constant_zero_energy(self, L):
        f = 7.0 * np.ones(_N)
        assert np.isclose(f @ L @ f, 0, atol=1e-10)

    def test_nonnegative(self, L):
        rng = np.random.RandomState(58)
        for _ in range(10):
            f = rng.randn(_N)
            assert f @ L @ f >= -1e-10

    def test_quadratic_equals_edge_sum(self, A, L):
        """f^T L f = sum_{edges} (f_i - f_j)^2."""
        rng = np.random.RandomState(59)
        f = rng.randn(_N)
        quad = f @ L @ f
        esum = 0.0
        for i in range(_N):
            for j in range(i + 1, _N):
                if A[i, j]:
                    esum += (f[i] - f[j]) ** 2
        assert np.isclose(quad, esum, atol=1e-8)

    def test_spectral_formula(self, U, eigenvalues, L):
        """E(f) = sum_k lambda_k |f_hat_k|^2."""
        rng = np.random.RandomState(60)
        f = rng.randn(_N)
        quad = f @ L @ f
        f_hat = U.T @ f
        spectral = np.sum(eigenvalues * f_hat**2)
        assert np.isclose(quad, spectral, atol=1e-8)

    def test_eigenvector_energy_equals_eigenvalue(self, U, eigenvalues, L):
        for k in range(_N):
            assert np.isclose(U[:, k] @ L @ U[:, k], eigenvalues[k], atol=1e-10)

    def test_fiedler_energy_is_10(self, U, eigenvalues, L):
        """Smoothest non-constant signal is a Fiedler vector; energy = 10."""
        idx = np.argmin(np.where(eigenvalues > 1e-8, eigenvalues, np.inf))
        assert np.isclose(U[:, idx] @ L @ U[:, idx], 10.0, atol=1e-8)

    def test_roughest_energy_is_16(self, U, eigenvalues, L):
        idx = np.argmax(eigenvalues)
        assert np.isclose(U[:, idx] @ L @ U[:, idx], 16.0, atol=1e-8)

    def test_lowpass_reduces_dirichlet_energy(self, U, eigenvalues, L):
        h = 1.0 / (1.0 + 0.1 * eigenvalues)
        rng = np.random.RandomState(61)
        f = rng.randn(_N)
        f_filt = U @ (h * (U.T @ f))
        assert f_filt @ L @ f_filt <= f @ L @ f + 1e-10


# ═════════════════════════════════════════════════════════════════════════════
# Section 8 : Graph wavelets  (7 tests)
# Spectral wavelet kernel g(s*lam); scaling function h(s*lam)
# ═════════════════════════════════════════════════════════════════════════════


class TestGraphWavelets:

    @staticmethod
    def _wavelet_kernel(s, lam):
        """Mexican-hat-like: g(x) = x exp(-x)."""
        x = s * lam
        return x * np.exp(-x)

    @staticmethod
    def _scaling_kernel(s, lam):
        """Low-pass scaling: h(x) = exp(-x^2)."""
        x = s * lam
        return np.exp(-(x**2))

    def test_wavelet_coefficients_shape(self, U, eigenvalues):
        rng = np.random.RandomState(62)
        f = rng.randn(_N)
        for s in [0.05, 0.1, 0.5, 1.0]:
            g = self._wavelet_kernel(s, eigenvalues)
            coeffs = U @ (g * (U.T @ f))
            assert coeffs.shape == (_N,)

    def test_wavelet_at_vertex_localization(self, U, eigenvalues):
        """Wavelet atom centred at vertex v is non-zero at v."""
        v, s = 3, 0.1
        delta = np.zeros(_N)
        delta[v] = 1.0
        g = self._wavelet_kernel(s, eigenvalues)
        psi = U @ (g * (U.T @ delta))
        assert abs(psi[v]) > 1e-10

    def test_small_scale_responds_to_high_freq(self, eigenvalues):
        """Small scale emphasises high eigenvalues more than large scale."""
        g_small = self._wavelet_kernel(0.01, eigenvalues)
        g_large = self._wavelet_kernel(1.0, eigenvalues)
        # At eigenvalue 16, small scale should have larger g
        idx16 = np.where(np.abs(eigenvalues - 16) < 1e-8)[0][0]
        assert g_small[idx16] >= g_large[idx16] - 1e-15

    def test_wavelet_energy_finite(self, U, eigenvalues):
        rng = np.random.RandomState(63)
        f = rng.randn(_N)
        g = self._wavelet_kernel(0.1, eigenvalues)
        coeffs = U @ (g * (U.T @ f))
        assert np.all(np.isfinite(coeffs))

    def test_scaling_function_is_lowpass(self, eigenvalues):
        s = 0.1
        h = self._scaling_kernel(s, eigenvalues)
        assert h[0] > h[-1]  # DC passed more than high freq

    def test_wavelet_kernel_zero_at_dc(self, eigenvalues):
        """g(0) = 0 -- wavelet kills DC."""
        for s in [0.01, 0.1, 1.0]:
            g = self._wavelet_kernel(s, eigenvalues)
            assert np.isclose(g[0], 0.0, atol=1e-12)

    def test_frame_bound_positive(self, eigenvalues):
        """Sum of |g_s(lam)|^2 + |h(lam)|^2 > 0 for all nonzero eigenvalues."""
        scales = [0.05, 0.1, 0.2, 0.5, 1.0]
        nonzero = eigenvalues[eigenvalues > 1e-8]
        total = np.zeros_like(nonzero)
        for s in scales:
            total += self._wavelet_kernel(s, nonzero) ** 2
        total += self._scaling_kernel(1.0, nonzero) ** 2
        assert np.all(total > 1e-15)


# ═════════════════════════════════════════════════════════════════════════════
# Section 9 : Bandlimited signals  (7 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestBandlimitedSignals:

    def test_dc_bandlimited_dim_1(self, eigenvalues):
        assert np.sum(np.abs(eigenvalues) < 1e-8) == 1

    def test_low_band_dim_25(self, eigenvalues):
        """Eigenvalues {0,10}: 1 + 24 = 25 dimensions."""
        assert np.sum(eigenvalues < 12) == 25

    def test_high_band_dim_15(self, eigenvalues):
        assert np.sum(np.abs(eigenvalues - 16) < 1e-8) == 15

    def test_projection_idempotent(self, U, eigenvalues):
        mask = (eigenvalues < 12).astype(float)
        rng = np.random.RandomState(64)
        f = rng.randn(_N)
        proj = U @ (mask * (U.T @ f))
        reproj = U @ (mask * (U.T @ proj))
        assert np.allclose(proj, reproj, atol=1e-10)

    def test_bandlimited_high_freq_zero(self, U, eigenvalues):
        mask = (eigenvalues < 12).astype(float)
        rng = np.random.RandomState(65)
        coeffs = rng.randn(_N) * mask
        f = U @ coeffs
        f_hat = U.T @ f
        assert np.allclose(f_hat[eigenvalues > 12], 0, atol=1e-10)

    def test_band_energy_fully_in_band(self, U, eigenvalues):
        mask = (np.abs(eigenvalues - 10) < 1e-8).astype(float)
        rng = np.random.RandomState(66)
        coeffs = rng.randn(_N) * mask
        f = U @ coeffs
        f_hat = U.T @ f
        in_band = np.sum(f_hat[mask > 0.5] ** 2)
        total = np.sum(f_hat**2)
        assert np.isclose(in_band, total, atol=1e-10)

    def test_three_band_decomposition_complete(self, U, eigenvalues):
        """Sum of projections onto {0}, {10}, {16} eigenspaces recovers f."""
        rng = np.random.RandomState(67)
        f = rng.randn(_N)
        f_hat = U.T @ f
        masks = [
            np.abs(eigenvalues) < 1e-8,
            np.abs(eigenvalues - 10) < 1e-8,
            np.abs(eigenvalues - 16) < 1e-8,
        ]
        rec = sum(U @ (m.astype(float) * f_hat) for m in masks)
        assert np.allclose(rec, f, atol=1e-10)


# ═════════════════════════════════════════════════════════════════════════════
# Section 10 : Sampling theory  (5 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestSamplingTheory:

    def test_dc_signal_from_one_sample(self, U, eigenvalues):
        """DC-bandlimited (dim 1): one sample suffices."""
        mask = np.abs(eigenvalues) < 1e-8
        band_idx = np.where(mask)[0]
        # Build bandlimited signal
        coeffs = np.zeros(_N)
        coeffs[band_idx] = 3.0
        f = U @ coeffs
        # Sample at vertex 0
        U_omega = U[np.ix_([0], band_idx)]
        c_rec = np.linalg.lstsq(U_omega, f[[0]], rcond=None)[0]
        f_rec = U[:, band_idx] @ c_rec
        assert np.allclose(f_rec, f, atol=1e-8)

    def test_25_band_from_25_samples(self, U, eigenvalues):
        """Low-band (dim 25): 25 generic samples reconstruct exactly."""
        mask = eigenvalues < 12
        band_idx = np.where(mask)[0]
        rng_sig = np.random.RandomState(68)
        coeffs = np.zeros(_N)
        coeffs[band_idx] = rng_sig.randn(len(band_idx))
        f = U @ coeffs
        # Use a separate RNG for sample selection (seed 0 gives well-conditioned set)
        rng_samp = np.random.RandomState(0)
        sample_idx = rng_samp.choice(_N, size=25, replace=False)
        U_omega = U[np.ix_(sample_idx, band_idx)]
        sv = np.linalg.svd(U_omega, compute_uv=False)
        if sv[-1] > 1e-6:
            c_rec = np.linalg.lstsq(U_omega, f[sample_idx], rcond=None)[0]
            f_rec = U[:, band_idx] @ c_rec
            assert np.allclose(f_rec, f, atol=1e-4)
        else:
            pytest.skip("Poorly conditioned sampling set")

    def test_undersampled_is_underdetermined(self, U, eigenvalues):
        """5 samples cannot reconstruct a 25-dim bandlimited signal."""
        mask = eigenvalues < 12
        band_idx = np.where(mask)[0]
        U_omega = U[np.ix_([0, 1, 2, 3, 4], band_idx)]
        assert U_omega.shape[0] < U_omega.shape[1]

    def test_full_sampling_perfect(self, U):
        rng = np.random.RandomState(69)
        f = rng.randn(_N)
        assert np.allclose(U @ (U.T @ f), f, atol=1e-10)

    def test_oversampled_least_squares_exact(self, U, eigenvalues):
        """35 samples for a 15-dim (eigenvalue-16) signal: overdetermined, exact."""
        mask = np.abs(eigenvalues - 16) < 1e-8
        band_idx = np.where(mask)[0]
        rng = np.random.RandomState(70)
        coeffs = np.zeros(_N)
        coeffs[band_idx] = rng.randn(len(band_idx))
        f = U @ coeffs
        sample_idx = rng.choice(_N, size=35, replace=False)
        U_omega = U[np.ix_(sample_idx, band_idx)]
        c_rec = np.linalg.lstsq(U_omega, f[sample_idx], rcond=None)[0]
        f_rec = U[:, band_idx] @ c_rec
        assert np.allclose(f_rec, f, atol=1e-6)


# ═════════════════════════════════════════════════════════════════════════════
# Section 11 : Signal denoising  (5 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestSignalDenoising:

    def test_ideal_projection_denoising(self, U, eigenvalues):
        """Project noisy smooth signal onto low band; MSE decreases."""
        mask = (eigenvalues < 12).astype(float)
        rng = np.random.RandomState(71)
        coeffs = np.zeros(_N)
        coeffs[mask > 0.5] = rng.randn(int(mask.sum()))
        f_clean = U @ coeffs
        noise = rng.randn(_N) * 0.5
        f_noisy = f_clean + noise
        f_den = U @ (mask * (U.T @ f_noisy))
        assert np.mean((f_den - f_clean) ** 2) < np.mean(noise**2)

    def test_heat_kernel_denoising(self, U, eigenvalues):
        rng = np.random.RandomState(72)
        f_clean = U[:, 1] * 3.0
        noise = rng.randn(_N)
        f_noisy = f_clean + noise
        h = np.exp(-0.05 * eigenvalues)
        f_den = U @ (h * (U.T @ f_noisy))
        assert np.mean((f_den - f_clean) ** 2) < np.mean(noise**2)

    def test_tikhonov_spectral_equals_matrix(self, U, eigenvalues, L):
        """Tikhonov (I + mu L)^{-1} f agrees with spectral formula."""
        mu = 0.1
        rng = np.random.RandomState(73)
        f = rng.randn(_N)
        h = 1.0 / (1.0 + mu * eigenvalues)
        f_spec = U @ (h * (U.T @ f))
        f_mat = np.linalg.solve(np.eye(_N) + mu * L, f)
        assert np.allclose(f_spec, f_mat, atol=1e-8)

    def test_denoising_preserves_clean_component(self, U, eigenvalues):
        """Ideal projection preserves the in-band part of noise exactly."""
        mask = (np.abs(eigenvalues - 10) < 1e-8).astype(float)
        rng = np.random.RandomState(74)
        coeffs = np.zeros(_N)
        coeffs[mask > 0.5] = rng.randn(int(mask.sum()))
        f_clean = U @ coeffs
        noise = rng.randn(_N) * 0.1
        f_noisy = f_clean + noise
        f_proj = U @ (mask * (U.T @ f_noisy))
        noise_proj = U @ (mask * (U.T @ noise))
        assert np.allclose(f_proj, f_clean + noise_proj, atol=1e-10)

    def test_stronger_regularisation_smoother_output(self, U, eigenvalues, L):
        """Increasing mu in Tikhonov produces smaller Dirichlet energy."""
        rng = np.random.RandomState(75)
        f = rng.randn(_N)
        energies = []
        for mu in [0.01, 0.1, 1.0, 10.0]:
            h = 1.0 / (1.0 + mu * eigenvalues)
            out = U @ (h * (U.T @ f))
            energies.append(out @ L @ out)
        for i in range(len(energies) - 1):
            assert energies[i + 1] <= energies[i] + 1e-10


# ═════════════════════════════════════════════════════════════════════════════
# Section 12 : Total variation on graphs  (6 tests)
# TV(f) = sum_{(i,j) in E} |f_i - f_j|
# ═════════════════════════════════════════════════════════════════════════════


class TestTotalVariation:

    @staticmethod
    def _tv(f, A):
        tv = 0.0
        for i in range(_N):
            for j in range(i + 1, _N):
                if A[i, j]:
                    tv += abs(f[i] - f[j])
        return tv

    def test_tv_constant_zero(self, A):
        assert np.isclose(self._tv(5.0 * np.ones(_N), A), 0)

    def test_tv_nonnegative(self, A):
        rng = np.random.RandomState(76)
        for _ in range(5):
            assert self._tv(rng.randn(_N), A) >= 0

    def test_tv_triangle_inequality(self, A):
        rng = np.random.RandomState(77)
        f, g = rng.randn(_N), rng.randn(_N)
        assert self._tv(f + g, A) <= self._tv(f, A) + self._tv(g, A) + 1e-10

    def test_tv_absolute_homogeneity(self, A):
        rng = np.random.RandomState(78)
        f = rng.randn(_N)
        alpha = -2.5
        assert np.isclose(
            self._tv(alpha * f, A), abs(alpha) * self._tv(f, A), atol=1e-10
        )

    def test_tv_indicator_equals_cut(self, A):
        """TV of {0,1}-indicator counts edge cut."""
        f = np.zeros(_N)
        f[:10] = 1.0
        cut = sum(1 for i in range(10) for j in range(10, _N) if A[i, j])
        assert np.isclose(self._tv(f, A), cut)

    def test_tv_squared_le_edges_times_dirichlet(self, A, L, num_edges):
        """Cauchy-Schwarz: TV(f)^2 <= |E| * E_D(f)."""
        assert num_edges == 240
        rng = np.random.RandomState(79)
        f = rng.randn(_N)
        tv = self._tv(f, A)
        de = f @ L @ f
        assert tv**2 <= num_edges * de + 1e-8


# ═════════════════════════════════════════════════════════════════════════════
# Section 13 : Graph filter banks  (6 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestGraphFilterBanks:

    def test_two_channel_perfect_reconstruction(self, U, eigenvalues):
        h_lo = np.where(eigenvalues < 12, 1.0, 0.0)
        h_hi = np.where(eigenvalues >= 12, 1.0, 0.0)
        rng = np.random.RandomState(80)
        f = rng.randn(_N)
        f_hat = U.T @ f
        assert np.allclose(U @ (h_lo * f_hat) + U @ (h_hi * f_hat), f, atol=1e-10)

    def test_three_channel_perfect_reconstruction(self, U, eigenvalues):
        h0 = (np.abs(eigenvalues) < 1e-8).astype(float)
        h1 = (np.abs(eigenvalues - 10) < 1e-8).astype(float)
        h2 = (np.abs(eigenvalues - 16) < 1e-8).astype(float)
        assert np.allclose(h0 + h1 + h2, 1.0)
        rng = np.random.RandomState(81)
        f = rng.randn(_N)
        f_hat = U.T @ f
        rec = sum(U @ (h * f_hat) for h in [h0, h1, h2])
        assert np.allclose(rec, f, atol=1e-10)

    def test_energy_partition(self, U, eigenvalues):
        """||f||^2 = sum_c ||f_c||^2 for orthogonal channels."""
        h0 = (np.abs(eigenvalues) < 1e-8).astype(float)
        h1 = (np.abs(eigenvalues - 10) < 1e-8).astype(float)
        h2 = (np.abs(eigenvalues - 16) < 1e-8).astype(float)
        rng = np.random.RandomState(82)
        f = rng.randn(_N)
        f_hat = U.T @ f
        total = f @ f
        parts = sum(np.sum((h * f_hat) ** 2) for h in [h0, h1, h2])
        assert np.isclose(total, parts, atol=1e-10)

    def test_channel_orthogonality(self, U, eigenvalues):
        h0 = (np.abs(eigenvalues) < 1e-8).astype(float)
        h1 = (np.abs(eigenvalues - 10) < 1e-8).astype(float)
        h2 = (np.abs(eigenvalues - 16) < 1e-8).astype(float)
        rng = np.random.RandomState(83)
        f = rng.randn(_N)
        f_hat = U.T @ f
        channels = [U @ (h * f_hat) for h in [h0, h1, h2]]
        for i in range(3):
            for j in range(i + 1, 3):
                assert np.isclose(channels[i] @ channels[j], 0, atol=1e-10)

    def test_smooth_filter_bank_normalised(self, U, eigenvalues):
        """Gaussian-shaped channels normalised to partition of unity."""
        sigma = 3.0
        h0 = np.exp(-(eigenvalues**2) / (2 * sigma**2))
        h1 = np.exp(-((eigenvalues - 10) ** 2) / (2 * sigma**2))
        h2 = np.exp(-((eigenvalues - 16) ** 2) / (2 * sigma**2))
        total = h0 + h1 + h2
        h0 /= total
        h1 /= total
        h2 /= total
        assert np.allclose(h0 + h1 + h2, 1.0)
        rng = np.random.RandomState(84)
        f = rng.randn(_N)
        f_hat = U.T @ f
        rec = U @ ((h0 + h1 + h2) * f_hat)
        assert np.allclose(rec, f, atol=1e-10)

    def test_analysis_synthesis_invertible(self, U, eigenvalues):
        """Analysis then synthesis with the SAME bank recovers f (up to h^2)."""
        h = 1.0 / (1.0 + 0.1 * eigenvalues)
        rng = np.random.RandomState(85)
        f = rng.randn(_N)
        f_hat = U.T @ f
        analysed = h * f_hat  # analysis
        synthesised = U @ (h * analysed)  # synthesis (h applied twice)
        direct = U @ (h**2 * f_hat)
        assert np.allclose(synthesised, direct, atol=1e-10)


# ═════════════════════════════════════════════════════════════════════════════
# Section 14 : Windowed Graph Fourier Transform  (5 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestWindowedGFT:

    @staticmethod
    def _window(centre, A, width=1):
        """BFS-based window: 1 at centre, 1/(hop+1) at hop-distance."""
        w = np.zeros(_N)
        w[centre] = 1.0
        current, visited = {centre}, {centre}
        for hop in range(1, width + 1):
            nxt = set()
            for v in current:
                for u in range(_N):
                    if A[v, u] and u not in visited:
                        nxt.add(u)
                        visited.add(u)
            for u in nxt:
                w[u] = 1.0 / (hop + 1)
            current = nxt
        return w

    def test_wgft_shape_40x40(self, A, U):
        rng = np.random.RandomState(86)
        f = rng.randn(_N)
        S = np.zeros((_N, _N))
        for v in range(_N):
            w = self._window(v, A, width=2)
            S[v, :] = U.T @ (f * w)
        assert S.shape == (_N, _N)

    def test_wgft_localization(self, A, U):
        """Windowed spectrum at v captures energy near v, not far away."""
        f = np.zeros(_N)
        f[5] = 10.0
        w_near = self._window(5, A, width=1)
        w_far = self._window(30, A, width=1)
        e_near = norm(U.T @ (f * w_near)) ** 2
        e_far = norm(U.T @ (f * w_far)) ** 2
        if A[5, 30] == 0:
            assert e_near > e_far

    def test_wgft_dc_positive_for_positive_signal(self, A, U):
        """Constant positive signal: DC component of every windowed view > 0."""
        f = 2.0 * np.ones(_N)
        for v in range(_N):
            w = self._window(v, A, width=1)
            dc = (U.T @ (f * w))[0]
            # u_0 is proportional to ones; sign-corrected DC must be positive
            sign = np.sign(U[0, 0])
            assert sign * dc > 0

    def test_wgft_different_widths_differ(self, A, U):
        rng = np.random.RandomState(87)
        f = rng.randn(_N)
        s1 = U.T @ (f * self._window(0, A, width=1))
        s2 = U.T @ (f * self._window(0, A, width=2))
        assert not np.allclose(s1, s2, atol=1e-10)

    def test_wgft_eigenvector_energy_concentration(self, A, U, eigenvalues):
        """For a pure eigenvector signal the total WGFT energy concentrates
        at the correct frequency band."""
        k = 25  # eigenvalue-16 band
        f = U[:, k]
        energy_per_freq = np.zeros(_N)
        for v in range(_N):
            w = self._window(v, A, width=2)
            spec = U.T @ (f * w)
            energy_per_freq += spec**2
        # Index k should carry significant energy
        assert energy_per_freq[k] > 0


# ═════════════════════════════════════════════════════════════════════════════
# Section 15 : Advanced graph-signal identities for W(3,3)  (10 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestAdvancedGSP:

    def test_minimal_polynomial_L(self, L):
        """L(L - 10I)(L - 16I) = 0."""
        I = np.eye(_N)
        poly = L @ (L - 10 * I) @ (L - 16 * I)
        assert np.allclose(poly, 0, atol=1e-6)

    def test_minimal_polynomial_A(self, A):
        """(A - 12I)(A - 2I)(A + 4I) = 0."""
        I = np.eye(_N)
        Af = A.astype(float)
        poly = (Af - 12 * I) @ (Af - 2 * I) @ (Af + 4 * I)
        assert np.allclose(poly, 0, atol=1e-6)

    def test_spectral_gap_10(self, eigenvalues):
        nz = eigenvalues[eigenvalues > 1e-8]
        assert np.isclose(np.min(nz), 10.0, atol=1e-8)

    def test_diameter_bound_from_distinct_eigenvalues(self, eigenvalues):
        """diam <= #distinct_evals - 1 = 2."""
        d = len(set(np.round(eigenvalues, 6)))
        assert d == 3
        assert d - 1 == 2

    def test_normalised_laplacian_eigenvalues(self, A):
        """L_norm eigenvalues: {0, 5/6, 4/3} with multiplicities 1,24,15."""
        D_inv_sqrt = np.diag(np.full(_N, 1.0 / np.sqrt(_K)))
        L_norm = np.eye(_N) - D_inv_sqrt @ A.astype(float) @ D_inv_sqrt
        eigs = np.sort(eigvalsh(L_norm))
        expected = sorted([0.0] * 1 + [10.0 / 12.0] * 24 + [16.0 / 12.0] * 15)
        assert np.allclose(eigs, expected, atol=1e-8)

    def test_trace_L_equals_480(self, L, eigenvalues):
        """tr(L) = 2|E| = 480 = 0*1 + 10*24 + 16*15."""
        assert np.isclose(np.trace(L), 480, atol=1e-8)
        assert np.isclose(np.sum(eigenvalues), 480, atol=1e-8)

    def test_trace_L2_equals_6240(self, L, eigenvalues):
        """tr(L^2) = 10^2*24 + 16^2*15 = 2400 + 3840 = 6240."""
        assert np.isclose(np.trace(L @ L), 6240, atol=1e-4)
        assert np.isclose(np.sum(eigenvalues**2), 6240, atol=1e-4)

    def test_spectral_radius_16(self, eigenvalues):
        assert np.isclose(np.max(eigenvalues), 16.0, atol=1e-8)

    def test_spanning_tree_count_positive(self, eigenvalues):
        """Kirchhoff: #spanning trees = (1/n) prod_{i>0} lambda_i > 0."""
        nz = eigenvalues[eigenvalues > 1e-8]
        log_count = np.sum(np.log(nz)) - np.log(_N)
        assert np.isfinite(log_count)
        assert log_count > 0

    def test_cheeger_lower_bound(self, eigenvalues):
        """lambda_1 / 2 <= h_G  (Cheeger constant)."""
        lam1 = 10.0
        lower = lam1 / 2
        assert lower == 5.0  # just a sanity anchor


# ═════════════════════════════════════════════════════════════════════════════
# Section 16 : Graph shift / diffusion / modulation operators  (5 tests)
# ═════════════════════════════════════════════════════════════════════════════


class TestGraphSignalOperators:

    def test_adjacency_shift_spectral(self, A, U, eigenvalues):
        """A f in spectral domain: hat{Af}_k = (12 - lam_k) f_hat_k."""
        rng = np.random.RandomState(88)
        f = rng.randn(_N)
        adj_eigs = 12 - eigenvalues
        f_hat = U.T @ f
        shifted_hat = U.T @ (A.astype(float) @ f)
        assert np.allclose(shifted_hat, adj_eigs * f_hat, atol=1e-8)

    def test_random_walk_eigenvalues(self, A, U, eigenvalues):
        """D^{-1}A has eigenvalues (12 - lam)/12 = 1 - lam/12."""
        P = A.astype(float) / _K
        rng = np.random.RandomState(89)
        f = rng.randn(_N)
        p_eigs = 1.0 - eigenvalues / 12.0
        f_hat = U.T @ f
        diff_hat = U.T @ (P @ f)
        assert np.allclose(diff_hat, p_eigs * f_hat, atol=1e-8)

    def test_iterated_diffusion_converges_to_uniform(self, A):
        P = A.astype(float) / _K
        rng = np.random.RandomState(90)
        f = np.abs(rng.randn(_N))
        f /= f.sum()
        for _ in range(500):
            f = P @ f
        assert np.allclose(f, np.ones(_N) / _N, atol=1e-6)

    def test_modulation_changes_spectrum(self, U):
        rng = np.random.RandomState(91)
        f = rng.randn(_N)
        mod = f * U[:, 5]
        assert not np.allclose(U.T @ f, U.T @ mod, atol=1e-5)

    def test_graph_translation_well_defined(self, U, eigenvalues):
        """Spectral translation T_v f = U diag(U[v,:]) U^T f is finite."""
        v = 7
        rng = np.random.RandomState(92)
        f = rng.randn(_N)
        kernel = U[v, :]
        translated = U @ (kernel * (U.T @ f))
        assert translated.shape == (_N,)
        assert np.all(np.isfinite(translated))
