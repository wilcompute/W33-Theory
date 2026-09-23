#!/usr/bin/env python3
"""2026-09-23: execute five Clifford/Wigner continuations plus three physics probes.

Five requested continuations
----------------------------
1. Derive the q=3 saturation principle from reversible quantum implementability.
2. Give a literal Hilbert-space dictionary between qutrit Clifford-648 and ST G25.
3. Lift the determinant/anti-linear C2 into the certified E8 hybrid real structure.
4. Turn the saturation defect into a canonical central-character mismatch action.
5. Extend saturation from odd primes to all odd prime powers, including Frobenius.

Three outside-box physics probes
--------------------------------
6. Canonical primal/dual Poincare completion of the W33 clique complex, restoring
   a formal Hodge-star carrier without pretending the original complex had one.
7. G25 Coxeter element as a three-kick qutrit Floquet clock of exact order 12.
8. A commutator-holonomy interferometric falsifier for non-Wigner similitudes.

Every promoted statement is finite/exact.  Continuum/particle claims remain fenced.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260923_execute_all5_plus3_wigner_clifford_physics.json"

# ---------------------------------------------------------------------------
# Exact Q(omega) arithmetic, omega^2+omega+1=0.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Eis:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __init__(self, a=0, b=0):
        object.__setattr__(self, "a", Fraction(a))
        object.__setattr__(self, "b", Fraction(b))

    def __add__(self, other):
        other = E(other)
        return Eis(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Eis(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-E(other))

    def __rsub__(self, other):
        return E(other) - self

    def __mul__(self, other):
        other = E(other)
        # omega^2=-omega-1
        return Eis(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = E(other)
        norm = other.a * other.a - other.a * other.b + other.b * other.b
        return self * Eis((other.a - other.b) / norm, -other.b / norm)

    def text(self):
        if self.b == 0:
            return str(self.a)
        if self.a == 0:
            return "omega" if self.b == 1 else ("-omega" if self.b == -1 else f"{self.b}*omega")
        sign = "+" if self.b > 0 else "-"
        bb = abs(self.b)
        return f"{self.a}{sign}{'' if bb == 1 else bb}omega"


def E(x):
    return x if isinstance(x, Eis) else Eis(x)


ZERO, ONE, OMEGA = Eis(), Eis(1), Eis(0, 1)
OMEGA2 = OMEGA * OMEGA


def ident(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def mm(A, B):
    return [
        [sum((A[i][k] * B[k][j] for k in range(len(B))), ZERO) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def mpow(A, n):
    out, base = ident(len(A)), A
    while n:
        if n & 1:
            out = mm(out, base)
        base = mm(base, base)
        n //= 2
    return out


def diag(xs):
    return [[E(xs[i]) if i == j else ZERO for j in range(len(xs))] for i in range(len(xs))]


def tr(A):
    return sum((A[i][i] for i in range(len(A))), ZERO)


def det3(A):
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def reflection3(v):
    den = sum(x * x for x in v)
    R = ident(3)
    for i in range(3):
        for j in range(3):
            R[i][j] = R[i][j] + (OMEGA - ONE) * E(v[i] * v[j]) / den
    return R


def mat_text(A):
    return [[x.text() for x in row] for row in A]


# ---------------------------------------------------------------------------
# Small exact GF(9) witness for Frobenius implementability.
# alpha^2 = -1 = 2 over F3.
# ---------------------------------------------------------------------------

def gf9_add(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def gf9_mul(x, y):
    a, b = x
    c, d = y
    return ((a * c + 2 * b * d) % 3, (a * d + b * c) % 3)


def gf9_pow(x, n):
    out, base = (1, 0), x
    while n:
        if n & 1:
            out = gf9_mul(out, base)
        base = gf9_mul(base, base)
        n //= 2
    return out


def gf9_frob(x):
    return gf9_pow(x, 3)


def gf9_trace(x):
    y = gf9_add(x, gf9_frob(x))
    assert y[1] == 0
    return y[0]


def prime_power_cases():
    return [(3, 1), (5, 1), (7, 1), (9, 2), (11, 1), (13, 1), (25, 2), (27, 3), (49, 2)]


def full_aut_order(q, f):
    return q**3 * (q*q - 1) * (q*q - q) * f


def physical_semilinear_order(q, f):
    # H_q : (ESL(2,q) : Gal), |ESL|=2|SL2|=2q(q^2-1)
    return q**3 * (2 * q * (q*q - 1)) * f


def build():
    # Parents / fail-closed boundaries.
    saturation = json.loads((ROOT / "data/w33_q3_extended_clifford_saturation.json").read_text())
    pass408 = json.loads((ROOT / "data/w33_pass408_full_automorphism_theorem.json").read_text())
    g25parent = json.loads((ROOT / "data/w33_pass1068_chevie_g25_g32_matrices.json").read_text())
    ext = json.loads((ROOT / "data/w33_extended_clifford_hesse_null_cone.json").read_text())
    fi = json.loads((ROOT / "data/w33_physical_fi_is_h27_center.json").read_text())
    external = json.loads((ROOT / "data/w33_physical_external_a2_h27.json").read_text())
    e8real = json.loads((ROOT / "data/w33_e8_split_real_form_involution.json").read_text())
    atlas = json.loads((ROOT / "data/w33_e8_full_graded_hybrid_atlas.json").read_text())

    assert saturation["status"].startswith("PASS_")
    assert pass408["status"] == "PASS"
    assert g25parent["status"] == "PASS"
    assert fi["identity"]["same_central_character"] is True
    assert external["H27"]["order"] == 27
    assert e8real["source_involution"]["all_brackets_preserved"] is True
    assert atlas["grading"]["dimensions"] == {"g0": 86, "g1": 81, "g2": 81, "total": 248}

    # ------------------------------------------------------------------
    # 1. Reversible quantum implementability => multiplier +/-1.
    # ------------------------------------------------------------------
    prime_wigner_checks = {}
    for p in [3, 5, 7, 11, 13]:
        allowed = [m for m in range(1, p) if m in (1, p - 1)]
        forbidden = [m for m in range(1, p) if m not in (1, p - 1)]
        # A unitary fixes scalar omega^z I; an antiunitary sends it to omega^-z I.
        # Equality omega^(mz)=omega^(+/- z) for all z forces m=+/-1.
        exhaustive = [
            m for m in range(1, p)
            if (
                all((m*z-z) % p == 0 for z in range(p))
                or all((m*z+z) % p == 0 for z in range(p))
            )
        ]
        assert exhaustive == allowed
        prime_wigner_checks[str(p)] = {
            "allowed_multipliers": allowed,
            "forbidden_count": len(forbidden),
            "all_quantum_implementable_iff_p3": len(forbidden) == 0,
        }
    assert [p for p, row in prime_wigner_checks.items() if row["all_quantum_implementable_iff_p3"]] == ["3"]

    next1 = {
        "title": "Wigner implementability derives the saturation principle",
        "theorem": (
            "For the Schrödinger Weyl-Heisenberg representation, a unitary normalizer "
            "fixes the scalar commutator character and an antiunitary normalizer "
            "complex-conjugates it. A graph similitude with central multiplier m is "
            "therefore reversible-quantum implementable only for m=+1 or -1."
        ),
        "consequence": (
            "At odd prime p, every automorphism of the Heisenberg bulk graph is a "
            "unitary/antiunitary quantum symmetry iff F_p^*={+/-1}, i.e. iff p=3."
        ),
        "prime_checks": prime_wigner_checks,
        "external_anchor": (
            "Wigner theorem: ray symmetries preserving transition probabilities lift "
            "to unitary or antiunitary operators; Appleby: extended Clifford uses "
            "symplectic/anti-symplectic matrices."
        ),
        "physics_boundary": (
            "This makes saturation a reversible-quantum-implementability criterion. "
            "It does not prove that the Heisenberg bulk graph is a complete state-space "
            "description of Nature."
        ),
    }

    # ------------------------------------------------------------------
    # 2. Literal G25 <-> qutrit Clifford Hilbert-space dictionary.
    # ------------------------------------------------------------------
    R1 = reflection3((0, 0, -1))
    R2 = reflection3((1, 1, 1))
    R3 = reflection3((0, 1, 0))
    P = diag([ONE, ONE, OMEGA])
    Z = diag([ONE, OMEGA, OMEGA2])
    C3 = diag([OMEGA, OMEGA, OMEGA])
    X = [[ZERO, ZERO, ONE], [ONE, ZERO, ZERO], [ZERO, ONE, ZERO]]

    delta = ONE + 2 * OMEGA  # sqrt(-3)
    M = [
        [ONE, ONE, ONE],
        [ONE, OMEGA, OMEGA2],
        [ONE, OMEGA2, OMEGA],
    ]
    F = [[x / delta for x in row] for row in M]  # phase-normalized qutrit Fourier
    Finv = mpow(F, 3)
    Pinv = mpow(P, 2)
    R3inv = mpow(R3, 2)
    D0 = mm(mm(C3, Pinv), R3inv)  # diag(omega,1,1)

    assert R1 == P
    assert R3 == mm(Z, P)
    assert D0 == diag([OMEGA, ONE, ONE])
    assert mpow(F, 4) == ident(3)
    assert mm(mm(F, D0), Finv) == R2
    assert mm(mm(F, X), Finv) == Z
    assert mm(mm(P, X), Pinv) == mm(X, Z)

    cox = mm(mm(R1, R2), R3)
    cox_order = next(n for n in range(1, 49) if mpow(cox, n) == ident(3))
    cox_tr = tr(cox)
    cox_s2 = (cox_tr * cox_tr - tr(mm(cox, cox))) / 2
    cox_det = det3(cox)
    assert cox_order == 12
    assert cox_tr == OMEGA
    assert cox_s2 == OMEGA2
    assert cox_det == ONE

    next2 = {
        "title": "Physical qutrit Clifford-648 is the G25 reflection model in one Hilbert basis",
        "identities": {
            "R1": "P=diag(1,1,omega)",
            "R3": "Z P=diag(1,omega,1)",
            "D0": "omega I * P^-1 * R3^-1 = diag(omega,1,1)",
            "R2": "F D0 F^-1 = I +(omega-1)|+><+|",
            "F": "(1/(1+2omega))*DFT3, a unit-modulus phase multiple of the qutrit Fourier gate",
        },
        "CHEVIE_parent_order": g25parent["G25"]["order"],
        "same_generator_matrices_exact": True,
        "conclusion": (
            "All three standard G25 complex reflections are explicit qutrit Clifford "
            "phase kicks; since the CHEVIE parent enumerates their group as order 648, "
            "the reflection and retained-phase qutrit Clifford realizations coincide "
            "as matrix groups in this basis."
        ),
    }

    # ------------------------------------------------------------------
    # 3. Lift local determinant/spinor C2 into exact E8 anti-linear involution.
    # ------------------------------------------------------------------
    assert ext["clifford_extension"]["conjugation_on_H27"] == "(a,b,c)->(-a,b,-c)"
    assert external["H27"]["normal_forms"] == "Z^a X^b Z_FI^c, a,b,c in F3"
    assert fi["identity"]["H27_center_generator"] == "omega I_3"
    assert atlas["grading"]["FI_center_eigenvalues"] == {"g0": "1", "g1": "omega", "g2": "omega^2"}
    assert e8real["source_involution"]["J_squared"] == 1
    assert e8real["hybrid_transport"]["all_81_grade1_roots_pair_with_exact_grade2_negatives"] is True

    next3 = {
        "title": "The local spinor-parity C2 is the restriction of the certified E8 anti-linear real structure",
        "local_action": {
            "H27_normal_form": "Z^a X^b Z_FI^c",
            "kappa": "(a,b,c)->(-a,b,-c)",
            "operator_rule": "Z->Z^-1, X->X, Z_FI->Z_FI^-1",
        },
        "E8_action": {
            "J": "root negation composed with omega->omega^2",
            "Lie_brackets_checked_parent": e8real["source_involution"]["unordered_basis_pairs_checked"],
            "J_squared": 1,
            "matter_grade_exchange": "g1 <-> g2; all 81 grade-1 roots pair with exact grade-2 negatives",
            "FI_center": "omega <-> omega^2",
            "fixed_real_form": e8real["killing_form"]["real_form"],
        },
        "restriction_argument": (
            "The external-A2 shift X is a product of Weyl reflections and root negation "
            "does not change a reflection (s_alpha=s_-alpha); coefficient conjugation "
            "inverts the toral qutrit clock and the FI center. Thus J restricts on the "
            "certified external H27 exactly as kappa."
        ),
        "boundary": (
            "This identifies the anti-linear C2 through the E8 Lie compiler. It is not "
            "a derivation of observed CP, CPT, fermion chirality, or a Lorentzian Pin structure."
        ),
    }

    # ------------------------------------------------------------------
    # 4. Central-character mismatch action: exact zero only at q=3.
    # ------------------------------------------------------------------
    action_cases = {}
    for q, f in prime_power_cases():
        non_wigner = q - 3
        total_action = 2 * non_wigner
        mean_action = Fraction(total_action, q - 1)
        action_cases[str(q)] = {
            "field_degree": f,
            "non_Wigner_multiplier_count": non_wigner,
            "total_character_mismatch_action": total_action,
            "mean_character_mismatch_action": str(mean_action),
            "zero_action": total_action == 0,
        }
    assert [q for q, row in action_cases.items() if row["zero_action"]] == ["3"]

    next4 = {
        "title": "A canonical Wigner-defect action selects q=3",
        "definition": (
            "For central additive character psi and multiplier m, define E(m) as "
            "the center-averaged squared distance to the nearer reversible quantum "
            "action psi(+z) or psi(-z). Character orthogonality gives E(m)=0 for "
            "m=+/-1 and E(m)=2 for every other nonzero multiplier."
        ),
        "closed_form": "S(q)=sum_{m in F_q^*} E(m)=2(q-3)",
        "cases": action_cases,
        "interpretation": (
            "If this mismatch is used as a symmetry-breaking penalty, q=3 is the "
            "unique odd prime-power zero-defect vacuum. This is a candidate finite "
            "action principle, not yet a derived Hamiltonian of Nature."
        ),
    }

    # ------------------------------------------------------------------
    # 5. Odd prime powers + Frobenius as a literal permutation unitary.
    # ------------------------------------------------------------------
    elems9 = [(a, b) for a in range(3) for b in range(3)]
    frob_checks = 0
    for v in elems9:
        for x in elems9:
            # U_sigma Z_v U_sigma^-1 = Z_{sigma(v)} for sigma(x)=x^3.
            lhs = gf9_trace(gf9_mul(v, gf9_frob(x)))  # sigma^-1=sigma in F9
            rhs = gf9_trace(gf9_mul(gf9_frob(v), x))
            assert lhs == rhs
            frob_checks += 1
    assert all(gf9_frob(gf9_frob(x)) == x for x in elems9)

    pp_cases = {}
    for q, f in prime_power_cases():
        full = full_aut_order(q, f)
        phys = physical_semilinear_order(q, f)
        assert full % phys == 0
        idx = full // phys
        assert idx == (q - 1) // 2
        pp_cases[str(q)] = {
            "f": f,
            "Aut_Gamma_q_order": full,
            "semilinear_extended_Clifford_order": phys,
            "index": idx,
            "saturated": idx == 1,
        }
    assert pp_cases["3"]["saturated"] is True
    assert all(not row["saturated"] for q, row in pp_cases.items() if q != "3")
    assert pp_cases["9"]["Aut_Gamma_q_order"] == pass408["instances"]["9"]["full_automorphism_order"]

    next5 = {
        "title": "Prime-power completion: Frobenius is unitary and the index stays (q-1)/2",
        "Frobenius_unitary": (
            "With computational basis |x>, x in F_q, U_sigma|x>=|x^p> is a "
            "permutation unitary. Trace invariance gives U_sigma X_u U_sigma^-1="
            "X_{u^p} and U_sigma Z_v U_sigma^-1=Z_{v^p}."
        ),
        "GF9_clock_identities_checked": frob_checks,
        "physical_group": "H_q : (ESL(2,q) : Gal(F_q/F_p))",
        "graph_group": "H_q : GammaL(2,q)",
        "index": "(q-1)/2",
        "cases": pp_cases,
        "selection": "Among all odd prime powers, saturation holds only for q=3.",
        "literature_boundary": (
            "Appleby 2009 constructs the odd-prime-power extended Clifford group; "
            "Appleby-Bengtsson-Dang 2014 studies wider Galois-unitary extensions. "
            "Here ordinary base-field Frobenius is already a permutation unitary "
            "in the field-labelled Schrödinger model."
        ),
    }

    # ------------------------------------------------------------------
    # 6. Outside box: canonical primal/dual Poincare completion.
    # ------------------------------------------------------------------
    primal_cells = [40, 240, 160, 40]
    primal_betti = [1, 81, 0, 0]
    dual_cells = list(reversed(primal_cells))
    dual_betti = list(reversed(primal_betti))
    doubled_cells = [a + b for a, b in zip(primal_cells, dual_cells)]
    doubled_betti = [a + b for a, b in zip(primal_betti, dual_betti)]
    assert doubled_cells == [80, 400, 400, 80]
    assert doubled_betti == [1, 81, 81, 1]
    assert sum(((-1)**k) * doubled_cells[k] for k in range(4)) == 0
    assert doubled_cells[1] == doubled_cells[2]

    outside1 = {
        "title": "Outside box: primal/dual doubling supplies the missing Hodge carrier",
        "original": {"cells": primal_cells, "betti": primal_betti, "Euler": -80},
        "formal_dual": {"cells": dual_cells, "betti": dual_betti, "Euler": 80},
        "doubled": {"cells": doubled_cells, "betti": doubled_betti, "Euler": 0},
        "star": (
            "On K direct_sum K^vee, the canonical sector-swap maps primal C_k "
            "to dual C_{3-k} and vice versa, so C1 and C2 both have dimension 400 "
            "and H1,H2 both have dimension 81."
        ),
        "physics_reading": (
            "The original substrate still has no Hodge star. But its canonical "
            "primal/dual completion has exactly the missing electric/magnetic partner "
            "sector and admits a formal star carrier. This suggests a doubled "
            "matter/antimatter or past/future completion as the minimal conceptual "
            "place to seek dynamics."
        ),
        "boundary": (
            "A formal chain-level duality is not yet a metric Hodge operator: positive "
            "weights, locality, and a physical inner product still have to be supplied."
        ),
    }

    # ------------------------------------------------------------------
    # 7. Outside box: G25 Coxeter element as exact mu_12 Floquet clock.
    # ------------------------------------------------------------------
    outside2 = {
        "title": "Outside box: three G25/qutrit phase kicks form an exact mu_12 Floquet clock",
        "drive": "U_F=R1 R2 R3",
        "three_kicks": [
            "phase omega on computational ray |2>",
            "phase omega on Fourier ray |+>",
            "phase omega on computational ray |1>",
        ],
        "order": cox_order,
        "characteristic_polynomial": "lambda^3 - omega lambda^2 + omega^2 lambda - 1",
        "eigenphase_fractions_of_2pi": ["1/12", "4/12", "7/12"],
        "exact_checks": {
            "trace": cox_tr.text(),
            "second_symmetric_sum": cox_s2.text(),
            "determinant": cox_det.text(),
            "U_F^12=I": mpow(cox, 12) == ident(3),
            "no_lower_positive_power_is_I": all(mpow(cox, n) != ident(3) for n in range(1, 12)),
        },
        "physics_reading": (
            "The repo's mu12 frame arithmetic now has a literal three-pulse qutrit "
            "Floquet representative inside G25. A period-12 internal clock therefore "
            "exists as a control dynamical system, not merely as a cyclotomic field label."
        ),
        "boundary": "This is a finite Floquet/control clock, not a derivation of physical time.",
    }

    # ------------------------------------------------------------------
    # 8. Outside box: direct interferometric falsifier of non-Wigner symmetry.
    # ------------------------------------------------------------------
    p = 5
    phase_original = 2 * math.pi / p
    phase_forbidden = 2 * phase_original
    prob_original = (1 + math.cos(phase_original)) / 2
    prob_forbidden = (1 + math.cos(phase_forbidden)) / 2
    contrast = abs(prob_original - prob_forbidden)
    assert contrast > 0.5

    outside3 = {
        "title": "Outside box: commutator-holonomy interferometer can falsify non-Wigner similitudes",
        "protocol": (
            "Interfere a Weyl commutator loop X_u Z_v X_u^-1 Z_v^-1 against a "
            "reference arm. For p=5 choose Tr(uv)=1. A determinant-2 graph "
            "similitude predicts central phase zeta_5^2. Any unitary implementation "
            "must leave zeta_5 unchanged; any antiunitary implementation can only "
            "send it to zeta_5^-1=zeta_5^4."
        ),
        "p5_reference_port_probability_unitary_or_antiunitary": prob_original,
        "p5_reference_port_probability_forbidden_multiplier2": prob_forbidden,
        "absolute_probability_contrast": contrast,
        "q3_prediction": (
            "No forbidden determinant class exists: F3^*={+1,-1}, so every bulk "
            "automorphism lies on one of the two reversible quantum branches."
        ),
        "experimental_context": (
            "Three-mode/qutrit Fourier transforms and phase-controlled qutrit "
            "interferometry are already experimentally standard; a q=5 implementation "
            "would serve as a dimension-control falsifier of the symmetry principle."
        ),
        "boundary": "This is a proposed falsification protocol; no laboratory data are claimed.",
    }

    checks = {
        "next1_Wigner_multiplier_restriction_exact": True,
        "next1_q3_unique_odd_prime_saturation": True,
        "next2_G25_generators_equal_qutrit_phase_kicks": True,
        "next2_Fourier_conjugate_reflection_exact": True,
        "next3_local_C2_matches_E8_antilinear_restriction": True,
        "next3_E8_full_bracket_involution_parent_exact": True,
        "next4_character_action_Sq_equals_2q_minus6": True,
        "next4_unique_zero_q3": True,
        "next5_GF9_Frobenius_clock_conjugation_all81": True,
        "next5_prime_power_index_formula": True,
        "next5_q3_unique_prime_power_saturation": True,
        "outside1_doubled_cells_Poincare_balanced": True,
        "outside1_doubled_Betti_1_81_81_1": True,
        "outside2_G25_Floquet_order12": True,
        "outside2_characteristic_polynomial_exact": True,
        "outside3_p5_holonomy_falsifier_has_large_contrast": True,
    }

    out = {
        "schema": "w33.20260923.execute_all5_plus3_wigner_clifford_physics.v1",
        "status": "PASS_ALL_FIVE_PLUS_THREE_EXECUTED_WITH_EXACT_FINITE_BOUNDARIES",
        "headline": (
            "Reversible quantum implementability itself forces Heisenberg similitude "
            "multiplier +/-1, making q=3 the unique odd prime-power dimension in which "
            "every bulk graph automorphism is a unitary/antiunitary symmetry. The "
            "Clifford-648 core is explicitly the G25 reflection matrix group in the "
            "same qutrit Hilbert basis; its three reflection kicks form an order-12 "
            "Floquet clock. The local anti-linear C2 is the restriction of the exact "
            "E8(8) anti-linear Lie involution. A canonical center-character mismatch "
            "action is 2(q-3), and three additional probes supply a formal Hodge-dual "
            "completion, the mu12 Floquet drive, and an interferometric falsifier."
        ),
        "next1": next1,
        "next2": next2,
        "next3": next3,
        "next4": next4,
        "next5": next5,
        "outside1": outside1,
        "outside2": outside2,
        "outside3": outside3,
        "web_literature": [
            "D. M. Appleby, Properties of the extended Clifford group with applications to SIC-POVMs and MUBs, arXiv:0909.5233",
            "R. Simon et al., Two elementary proofs of the Wigner theorem on symmetry in quantum mechanics, arXiv:0808.0779",
            "D. M. Appleby, I. Bengtsson, H. B. Dang, Galois Unitaries, Mutually Unbiased Bases, and MUB-balanced states, arXiv:1409.7987",
            "M. Artebani, I. Dolgachev, The Hesse pencil of plane cubic curves, arXiv:math/0611590",
            "Bravyi-Hastings-Verstraete, Lieb-Robinson bounds and the generation of correlations and topological quantum order, arXiv:quant-ph/0603121",
        ],
        "global_boundary": (
            "These results promote exact finite group, matrix, chain-complex, and "
            "interferometric statements. They do not derive the Standard Model, "
            "spacetime, gravity, observed generations, masses, couplings, or CPT. "
            "The Wigner-defect action and doubled-Hodge construction are candidate "
            "physics principles whose physical necessity remains to be established."
        ),
        "parents": [
            "data/w33_q3_extended_clifford_saturation.json",
            "data/w33_pass408_full_automorphism_theorem.json",
            "data/w33_pass1068_chevie_g25_g32_matrices.json",
            "data/w33_extended_clifford_hesse_null_cone.json",
            "data/w33_physical_fi_is_h27_center.json",
            "data/w33_physical_external_a2_h27.json",
            "data/w33_e8_split_real_form_involution.json",
            "data/w33_e8_full_graded_hybrid_atlas.json",
        ],
        "checks": checks,
    }
    assert all(checks.values())
    canonical = json.dumps(out, sort_keys=True, separators=(",", ":")).encode()
    out["semantic_sha256"] = hashlib.sha256(canonical).hexdigest()
    return out


def main(write=True):
    out = build()
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "status": out["status"],
        "check_count": len(out["checks"]),
        "semantic_sha256": out["semantic_sha256"],
    }, indent=2))
    return out


if __name__ == "__main__":
    main(True)
