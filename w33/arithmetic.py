"""
Arithmetic-function closure layer for the W(3,3) substrate.

This packages the exact integer identities behind the recent arithmetic-
closure theorem: the cleanest substrate primitives are mapped back into
the substrate's own integer vocabulary by Euler's totient, divisor count,
and divisor sum.
"""

from __future__ import annotations

from .substrate import E, H1, Phi3, Phi4, Phi6, f, g, k, lambda_, mu, q, q_bang, q_pow_q, v


GAUGE_LAYER = Phi6 * Phi4 + lambda_

PRIMITIVES = {
    "q": q,
    "lam_SRG": lambda_,
    "mu": mu,
    "k": k,
    "Phi_3": Phi3,
    "Phi_4": Phi4,
    "Phi_6": Phi6,
    "q_factorial": q_bang,
    "2^q": 2**q,
    "q^q": q_pow_q,
    "H_1": H1,
    "v": v,
    "f": f,
    "g_neg": g,
    "edges_E": E,
    "lambda_gauge": GAUGE_LAYER,
}

SUBSTRATE_READINGS = {
    1: "unit",
    2: "lam_SRG",
    3: "q",
    4: "mu",
    5: "Csaszar count = q+2",
    6: "q!",
    7: "Phi_6",
    8: "2^q (tomotope cells)",
    10: "Phi_4",
    12: "k",
    13: "Phi_3",
    14: "2 Phi_6",
    15: "g_neg",
    16: "2^mu (binary mu-shell)",
    18: "2 q^2",
    20: "m_4 (Pell mult #4)",
    21: "T_6 (Csaszar edges)",
    23: "Szilassi packet (f-1)",
    24: "f",
    27: "q^q",
    28: "n_even (Klein bitangents)",
    32: "2^(q+2)",
    36: "N_M = |S| = q^2 mu",
    40: "v (W33 vertex count)",
    42: "Hurwitz orbits (Klein)",
    50: "g(K_28) = v + Phi_4",
    54: "2 q^q",
    56: "sextactic = 2^q Phi_6",
    60: "inflation e-folds = |S| + f",
    64: "2^(2q)",
    72: "lambda_gauge",
    80: "2v",
    81: "H_1",
    84: "Csaszar flag count = mu T_6",
    88: "g(K_36) conductor",
    90: "q^2 Phi_4",
    121: "p_Ih^2",
    128: "2^Phi_6",
    195: "5 * (q Phi_3)",
    240: "|E|",
    744: "|E| + Phi_6 lambda_gauge = J-function shift",
}


def prime_factorization(n: int) -> dict[int, int]:
    """Return the prime factorization of a positive integer."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def euler_totient(n: int) -> int:
    """Euler's totient function φ(n)."""
    result = n
    for p in prime_factorization(n):
        result -= result // p
    return result


def divisor_count(n: int) -> int:
    """Number-of-divisors function d(n)."""
    total = 1
    for exponent in prime_factorization(n).values():
        total *= exponent + 1
    return total


def divisor_sum(n: int) -> int:
    """Divisor-sum function σ₁(n)."""
    total = 1
    for p, exponent in prime_factorization(n).items():
        total *= (p ** (exponent + 1) - 1) // (p - 1)
    return total


def radical(n: int) -> int:
    """Squarefree kernel rad(n)."""
    total = 1
    for p in prime_factorization(n):
        total *= p
    return total


def distinct_prime_factor_count(n: int) -> int:
    """Number of distinct prime factors ω(n)."""
    return len(prime_factorization(n))


def total_prime_factor_count(n: int) -> int:
    """Total number of prime factors Ω(n), counted with multiplicity."""
    return sum(prime_factorization(n).values())


def cototient(n: int) -> int:
    """Cototient n - φ(n)."""
    return n - euler_totient(n)


def jordan_totient(n: int, order: int) -> int:
    """Jordan totient J_order(n)."""
    if order < 1:
        raise ValueError("order must be >= 1")
    result = n**order
    for p in prime_factorization(n):
        pk = p**order
        result = (result // pk) * (pk - 1)
    return result


def arithmetic_derivative(n: int) -> int:
    """Arithmetic derivative D(n), with D(p)=1 and Leibniz extension."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return 0
    return sum(exponent * (n // p) for p, exponent in prime_factorization(n).items())


def substrate_reading(n: int) -> str:
    """Human-readable substrate name for a distinguished integer, if known."""
    return SUBSTRATE_READINGS.get(n, "")


def build_arithmetic_closure_table() -> list[dict[str, int | str]]:
    """Return φ, d, and σ₁ values for the core arithmetic-closure primitives."""
    rows: list[dict[str, int | str]] = []
    for name, n in PRIMITIVES.items():
        phi_n = euler_totient(n)
        d_n = divisor_count(n)
        sigma_n = divisor_sum(n)
        rows.append(
            {
                "primitive": name,
                "value": n,
                "phi_n": phi_n,
                "phi_substrate": substrate_reading(phi_n),
                "d_n": d_n,
                "d_substrate": substrate_reading(d_n),
                "sigma_n": sigma_n,
                "sigma_substrate": substrate_reading(sigma_n),
            }
        )
    return rows


def get_sigma_edge_j_shift() -> int:
    return divisor_sum(E)


def get_sigma_valency_klein_bitangents() -> int:
    return divisor_sum(k)


def get_sigma_leech_exponent_efolds() -> int:
    return divisor_sum(f)


def get_sigma_q_pow_q_vertex_count() -> int:
    return divisor_sum(q_pow_q)


def get_sigma_logical_sector_ihara_square() -> int:
    return divisor_sum(H1)


def get_divisor_count_edges_pell_multiplier() -> int:
    return divisor_count(E)


def get_divisor_count_vertices_tomotope_cells() -> int:
    return divisor_count(v)


def get_divisor_count_valency_factorial() -> int:
    return divisor_count(k)


def get_totient_edges_binary_shell() -> int:
    return euler_totient(E)


def get_totient_gauge_positive_multiplicity() -> int:
    return euler_totient(GAUGE_LAYER)


def get_totient_phi3_valency() -> int:
    return euler_totient(Phi3)


def get_totient_phi6_factorial() -> int:
    return euler_totient(Phi6)


def arithmetic_closure_headlines() -> list[dict[str, int | str | bool]]:
    """Return the strongest exact arithmetic-closure identities."""
    return [
        {
            "identity": "sigma(|E|) = 744",
            "substrate": "= |E| + Phi_6 * lambda_gauge = J-function constant shift",
            "value": get_sigma_edge_j_shift(),
            "expected": 744,
            "match": get_sigma_edge_j_shift() == 744,
        },
        {
            "identity": "sigma(k) = 28",
            "substrate": "= n_even = Klein bitangent count",
            "value": get_sigma_valency_klein_bitangents(),
            "expected": 28,
            "match": get_sigma_valency_klein_bitangents() == 28,
        },
        {
            "identity": "sigma(f) = 60",
            "substrate": "= |S| + f = inflation e-folds",
            "value": get_sigma_leech_exponent_efolds(),
            "expected": 60,
            "match": get_sigma_leech_exponent_efolds() == 60,
        },
        {
            "identity": "sigma(q^q) = v",
            "substrate": "= 40 = vertex count",
            "value": get_sigma_q_pow_q_vertex_count(),
            "expected": v,
            "match": get_sigma_q_pow_q_vertex_count() == v,
        },
        {
            "identity": "sigma(H_1) = 121",
            "substrate": "= p_Ih^2",
            "value": get_sigma_logical_sector_ihara_square(),
            "expected": 121,
            "match": get_sigma_logical_sector_ihara_square() == 121,
        },
        {
            "identity": "d(|E|) = 20",
            "substrate": "= Pell multiplier m_4",
            "value": get_divisor_count_edges_pell_multiplier(),
            "expected": 20,
            "match": get_divisor_count_edges_pell_multiplier() == 20,
        },
        {
            "identity": "d(v) = 2^q",
            "substrate": "= 8 = tomotope cells",
            "value": get_divisor_count_vertices_tomotope_cells(),
            "expected": 2**q,
            "match": get_divisor_count_vertices_tomotope_cells() == 2**q,
        },
        {
            "identity": "d(k) = q!",
            "substrate": "= 6 = Master Equation root",
            "value": get_divisor_count_valency_factorial(),
            "expected": q_bang,
            "match": get_divisor_count_valency_factorial() == q_bang,
        },
        {
            "identity": "phi(|E|) = 64",
            "substrate": "= 2^(2q)",
            "value": get_totient_edges_binary_shell(),
            "expected": 2 ** (2 * q),
            "match": get_totient_edges_binary_shell() == 2 ** (2 * q),
        },
        {
            "identity": "phi(lambda_gauge) = f",
            "substrate": "= 24 = positive spectral multiplicity",
            "value": get_totient_gauge_positive_multiplicity(),
            "expected": f,
            "match": get_totient_gauge_positive_multiplicity() == f,
        },
        {
            "identity": "phi(Phi_3) = k",
            "substrate": "= 12 = valency",
            "value": get_totient_phi3_valency(),
            "expected": k,
            "match": get_totient_phi3_valency() == k,
        },
        {
            "identity": "phi(Phi_6) = q!",
            "substrate": "= 6 = Master Equation root",
            "value": get_totient_phi6_factorial(),
            "expected": q_bang,
            "match": get_totient_phi6_factorial() == q_bang,
        },
    ]


def operator_lift_headlines() -> list[dict[str, int | str | bool]]:
    """Return the strongest exact operator-lift identities beyond φ, d, and σ₁."""
    return [
        {
            "identity": "J_2(lambda) = q",
            "substrate": "= Jordan totient of the overlap parameter gives the field root",
            "value": jordan_totient(lambda_, 2),
            "expected": q,
            "match": jordan_totient(lambda_, 2) == q,
        },
        {
            "identity": "J_2(q) = 2^q",
            "substrate": "= Jordan totient of the field root gives the tomotope shell",
            "value": jordan_totient(q, 2),
            "expected": 2**q,
            "match": jordan_totient(q, 2) == 2**q,
        },
        {
            "identity": "J_2(mu) = k",
            "substrate": "= Jordan totient of the spacetime shell gives the valency",
            "value": jordan_totient(mu, 2),
            "expected": k,
            "match": jordan_totient(mu, 2) == k,
        },
        {
            "identity": "J_4(mu) = |E|",
            "substrate": "= fourth Jordan totient of mu gives the edge count",
            "value": jordan_totient(mu, 4),
            "expected": E,
            "match": jordan_totient(mu, 4) == E,
        },
        {
            "identity": "rad(v) = Phi_4",
            "substrate": "= squarefree kernel of the vertex count gives the quartic cyclotomic",
            "value": radical(v),
            "expected": Phi4,
            "match": radical(v) == Phi4,
        },
        {
            "identity": "cot(v) = f",
            "substrate": "= cototient of the vertex count gives the positive multiplicity",
            "value": cototient(v),
            "expected": f,
            "match": cototient(v) == f,
        },
        {
            "identity": "Omega(v) = mu",
            "substrate": "= total prime factors of the vertex count give the spacetime shell",
            "value": total_prime_factor_count(v),
            "expected": mu,
            "match": total_prime_factor_count(v) == mu,
        },
        {
            "identity": "Omega(|E|) = q!",
            "substrate": "= total prime factors of the edge count give the Master Equation root",
            "value": total_prime_factor_count(E),
            "expected": q_bang,
            "match": total_prime_factor_count(E) == q_bang,
        },
        {
            "identity": "D(2^q) = k",
            "substrate": "= arithmetic derivative of the binary shell gives the valency",
            "value": arithmetic_derivative(2**q),
            "expected": k,
            "match": arithmetic_derivative(2**q) == k,
        },
        {
            "identity": "D(Phi_4) = Phi_6",
            "substrate": "= arithmetic derivative of the quartic cyclotomic gives the Heawood shell",
            "value": arithmetic_derivative(Phi4),
            "expected": Phi6,
            "match": arithmetic_derivative(Phi4) == Phi6,
        },
        {
            "identity": "D(q^q) = q^q",
            "substrate": "= arithmetic derivative fixes the Albert shell",
            "value": arithmetic_derivative(q_pow_q),
            "expected": q_pow_q,
            "match": arithmetic_derivative(q_pow_q) == q_pow_q,
        },
    ]


ARITHMETIC_OPERATORS = {
    "phi": euler_totient,
    "d": divisor_count,
    "sigma_1": divisor_sum,
    "rad": radical,
    "Omega": total_prime_factor_count,
    "cot": cototient,
    "J2": lambda n: jordan_totient(n, 2),
    "J4": lambda n: jordan_totient(n, 4),
    "D": arithmetic_derivative,
}


def apply_operator_chain(n: int, chain: tuple[str, ...] | list[str]) -> int:
    """Apply a named arithmetic-operator chain to a positive integer."""
    value = n
    for op_name in chain:
        try:
            fn = ARITHMETIC_OPERATORS[op_name]
        except KeyError as exc:
            raise KeyError(f"unknown arithmetic operator: {op_name}") from exc
        value = fn(value)
    return value


def safe_apply_operator_chain(n: int, chain: tuple[str, ...] | list[str]) -> int | None:
    """Apply a chain, returning None if an intermediate leaves the positive integers."""
    try:
        return apply_operator_chain(n, chain)
    except ValueError:
        return None


def validate_arithmetic_closure_headlines() -> bool:
    """Return True iff all headline arithmetic identities verify exactly."""
    return all(item["match"] for item in arithmetic_closure_headlines())


def validate_operator_lift_headlines() -> bool:
    """Return True iff all extended operator-lift identities verify exactly."""
    return all(item["match"] for item in operator_lift_headlines())