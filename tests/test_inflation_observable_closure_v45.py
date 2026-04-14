"""
Phase V45 — Exact inflation observable closure relations
=========================================================

The repaired inflation sector now closes exactly.
Two seemingly different e-fold derivations agree:

    N = E/mu = 240/4 = 60
    N = 2(v - Phi_4) = 2(40 - 10) = 60

From that single graph-fixed value we obtain the exact packet

    n_s      = 1 - 2/N      = 29/30
    r        = 12/N^2       = 1/300
    running  = -2/N^2       = -1/1800
    n_T      = -r/8         = -1/2400
    f_NL     = (5/12)(n_s-1)= -1/72

and the observable closure identities

    r       = 3(1 - n_s)^2
    running = -(1 - n_s)^2 / 2 = -r/6
    n_T     = -r/8 = 3*running/4
    f_NL    = -5(1 - n_s)/12
"""

from fractions import Fraction as Fr

# W(3,3) data
v, k, lam, mu = 40, 12, 2, 4
E = v * k // 2
Phi4 = 10


class TestV45_EfoldBridge:
    def test_two_efold_derivations_match_exactly(self):
        n_from_edges = E // mu
        n_from_modes = 2 * (v - Phi4)
        assert n_from_edges == 60
        assert n_from_modes == 60
        assert n_from_edges == n_from_modes

    def test_edge_mode_bridge_identity(self):
        assert E == 2 * mu * (v - Phi4)
        assert E == 8 * (v - Phi4)


class TestV45_ObservablePacket:
    def test_exact_packet_values(self):
        N = E // mu
        ns = Fr(N - 2, N)
        r = Fr(12, N * N)
        running = Fr(-2, N * N)
        nt = -r / 8
        fnl = Fr(5, 12) * (ns - 1)

        assert ns == Fr(29, 30)
        assert r == Fr(1, 300)
        assert running == Fr(-1, 1800)
        assert nt == Fr(-1, 2400)
        assert fnl == Fr(-1, 72)


class TestV45_ClosureRelations:
    def test_r_from_ns(self):
        ns = Fr(29, 30)
        r = Fr(1, 300)
        assert r == 3 * (1 - ns) ** 2

    def test_running_from_ns_and_r(self):
        ns = Fr(29, 30)
        r = Fr(1, 300)
        running = Fr(-1, 1800)
        assert running == -((1 - ns) ** 2) / 2
        assert running == -r / 6

    def test_tensor_tilt_from_r_and_running(self):
        r = Fr(1, 300)
        running = Fr(-1, 1800)
        nt = Fr(-1, 2400)
        assert nt == -r / 8
        assert nt == 3 * running / 4

    def test_fnl_from_ns(self):
        ns = Fr(29, 30)
        fnl = Fr(-1, 72)
        assert fnl == -Fr(5, 12) * (1 - ns)

    def test_full_closure_packet(self):
        N = E // mu
        ns = Fr(N - 2, N)
        r = Fr(12, N * N)
        running = Fr(-2, N * N)
        nt = -r / 8
        fnl = Fr(5, 12) * (ns - 1)

        closure = {
            'bridge': N == 2 * (v - Phi4),
            'r_ns': r == 3 * (1 - ns) ** 2,
            'run_ns': running == -((1 - ns) ** 2) / 2,
            'run_r': running == -r / 6,
            'nt_r': nt == -r / 8,
            'nt_run': nt == 3 * running / 4,
            'fnl_ns': fnl == -Fr(5, 12) * (1 - ns),
        }
        assert all(closure.values())
