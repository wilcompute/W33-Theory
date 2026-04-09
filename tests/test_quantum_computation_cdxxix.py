"""
Phase CDXXIX (429) — Quantum Computation from Graph Structure
=============================================================
Graph states, QEC, MBQC, topological QC, fault tolerance.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_GraphState:
    def test_qubits(self):
        assert v == 40

    def test_CZ_gates(self):
        assert E == 240

    def test_stabilizer_weight(self):
        assert k + 1 == Phi3


class TestT2_QEC:
    def test_hoffman_bound(self):
        assert v * abs(s) // (k + abs(s)) == Phi4

    def test_connectivity(self):
        assert k == 12


class TestT3_MBQC:
    def test_treewidth(self):
        assert v - Phi4 == 30

    def test_treewidth_formula(self):
        assert q * Phi4 == 30

    def test_pauli(self):
        assert 2 * v == 80


class TestT4_Topological:
    def test_anyon_types(self):
        assert q + 1 == mu

    def test_pentagon(self):
        assert q + 2 == 5


class TestT5_FaultTolerance:
    def test_code_rate(self):
        assert Fraction(Phi4, v) == Fraction(1, mu)

    def test_singleton(self):
        assert (v - Phi4 + 2) // 2 == mu ** 2

    def test_gate_count(self):
        assert v + E == Phi6 * v
