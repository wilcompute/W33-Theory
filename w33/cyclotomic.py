"""Cyclotomic defect classifiers for the W(3,q) shift tower.

The polynomial pair

    Phi3(q) = q^2 + q + 1,
    Phi6(q) = q^2 - q + 1,

forms the core cyclotomic ladder of the substrate. The arithmetic-semigroup
audit showed that the radical ladder fails exactly when these values are not
squarefree. This module upgrades that observation into an explicit residue-class
classifier: for split primes p ≡ 1 (mod 3), the nonsquarefree defect locus is
controlled by the two Hensel-lifted nontrivial cube roots of unity modulo p^2.
"""

from __future__ import annotations

import cmath
import math
from fractions import Fraction

from .arithmetic import prime_factorization
from .shift_tower import shift_tower_primitives


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def primes_up_to(limit: int) -> list[int]:
    """Return all primes up to the supplied limit by a simple sieve."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    bound = int(limit**0.5)
    for p in range(2, bound + 1):
        if sieve[p]:
            start = p * p
            step = p
            sieve[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return [n for n in range(2, limit + 1) if sieve[n]]


def phi3_value(q: int) -> int:
    return shift_tower_primitives(q)["Phi3"]


def phi6_value(q: int) -> int:
    return shift_tower_primitives(q)["Phi6"]


def eisenstein_norm(a: int, b: int) -> int:
    """Norm N(a + bω) in Z[ω], with ω^2 + ω + 1 = 0."""
    return a * a - a * b + b * b


def phi3_as_eisenstein_norm(q: int) -> int:
    """Phi3(q) = N(q - ω)."""
    return eisenstein_norm(q, -1)


def phi6_as_eisenstein_norm(q: int) -> int:
    """Phi6(q) = N(q + ω)."""
    return eisenstein_norm(q, 1)


def split_primes_mod_3(limit: int) -> list[int]:
    return [p for p in primes_up_to(limit) if p % 3 == 1]


def cyclotomic_prime_support(q: int, family: str) -> dict[str, object]:
    """Classify the prime support of Phi3(q) or Phi6(q) by congruence class."""
    if family not in {"Phi3", "Phi6"}:
        raise ValueError("family must be 'Phi3' or 'Phi6'")

    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    factors = prime_factorization(value)
    support_primes = sorted(factors)
    bad_primes: list[int] = []

    for p in support_primes:
        if family == "Phi3":
            allowed = (p == 3) or (p % 3 == 1)
        else:
            allowed = (p == 3) or (p % 6 == 1)
        if not allowed:
            bad_primes.append(p)

    return {
        "q": q,
        "family": family,
        "value": value,
        "factorization": factors,
        "support_primes": support_primes,
        "bad_primes": bad_primes,
        "exact_support": not bad_primes,
    }


def cyclotomic_prime_support_scan(limit_q: int = 5000) -> dict[str, object]:
    """Audit the prime-support law for Phi3(q) and Phi6(q) on 3 <= q <= limit_q."""
    phi3_bad_examples = []
    phi6_bad_examples = []
    phi3_support_primes = set()
    phi6_support_primes = set()

    for q in range(3, limit_q + 1):
        row3 = cyclotomic_prime_support(q, "Phi3")
        row6 = cyclotomic_prime_support(q, "Phi6")
        phi3_support_primes.update(row3["support_primes"])
        phi6_support_primes.update(row6["support_primes"])
        if not row3["exact_support"]:
            phi3_bad_examples.append(row3)
        if not row6["exact_support"]:
            phi6_bad_examples.append(row6)

    phi3_support_primes = sorted(phi3_support_primes)
    phi6_support_primes = sorted(phi6_support_primes)
    return {
        "limit_q": limit_q,
        "phi3_exact_support": not phi3_bad_examples,
        "phi6_exact_support": not phi6_bad_examples,
        "phi3_bad_examples": phi3_bad_examples,
        "phi6_bad_examples": phi6_bad_examples,
        "phi3_support_primes": phi3_support_primes,
        "phi6_support_primes": phi6_support_primes,
        "phi3_first_support_primes": phi3_support_primes[:12],
        "phi6_first_support_primes": phi6_support_primes[:12],
        "theorem_summary": (
            "Every prime divisor of Phi3(q)=q^2+q+1 is either 3 or congruent to 1 mod 3, and every prime divisor of "
            "Phi6(q)=q^2-q+1 is either 3 or congruent to 1 mod 6. So the cyclotomic packet already lives entirely "
            "on the split-prime side before any squarefree/defect refinement is imposed."
        ),
    }


def primitive_root_mod_prime_square(p: int) -> int:
    """Return a primitive root modulo p^2 for an odd prime p."""
    if not is_prime(p) or p == 2:
        raise ValueError("p must be an odd prime")
    mod = p * p
    phi = p * (p - 1)
    factors = prime_factorization(phi)
    for g in range(2, mod):
        if pow(g, phi, mod) != 1:
            continue
        if all(pow(g, phi // ell, mod) != 1 for ell in factors):
            return g
    raise ValueError(f"no primitive root found modulo {p}^2")


def nontrivial_cube_roots_mod_prime_square(p: int) -> list[int]:
    """Return the two nontrivial order-3 units in (Z/p^2Z)^x for split primes p ≡ 1 mod 3."""
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("p must be a prime congruent to 1 mod 3")
    mod = p * p
    phi = p * (p - 1)
    g = primitive_root_mod_prime_square(p)
    roots = {pow(g, phi // 3, mod), pow(g, 2 * phi // 3, mod)}
    return sorted(roots)


def phi3_roots_mod_prime_square(p: int) -> list[int]:
    """Return the two roots of x^2 + x + 1 ≡ 0 (mod p^2) for split primes p ≡ 1 mod 3."""
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("p must be a prime congruent to 1 mod 3")
    mod = p * p
    roots_mod_p = [r for r in range(p) if (r * r + r + 1) % p == 0]
    roots: list[int] = []
    for r0 in roots_mod_p:
        for t in range(p):
            r = r0 + t * p
            if (r * r + r + 1) % mod == 0:
                roots.append(r)
                break
    return sorted(set(roots))


def phi3_roots_mod_prime_power(p: int, power: int) -> list[int]:
    """Return the two roots of x^2 + x + 1 ≡ 0 (mod p^power) for split primes p ≡ 1 mod 3."""
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("p must be a prime congruent to 1 mod 3")
    if power < 1:
        raise ValueError("power must be >= 1")
    mod = p**power
    roots_mod_p = [r for r in range(p) if (r * r + r + 1) % p == 0]
    if power == 1:
        return sorted(roots_mod_p)

    roots = roots_mod_p
    for exponent in range(2, power + 1):
        prev_mod = p ** (exponent - 1)
        curr_mod = p**exponent
        lifted = []
        for r0 in roots:
            for t in range(p):
                r = r0 + t * prev_mod
                if (r * r + r + 1) % curr_mod == 0:
                    lifted.append(r)
                    break
        roots = sorted(set(lifted))
    return roots


def phi6_roots_mod_prime_square(p: int) -> list[int]:
    """Return the two roots of x^2 - x + 1 ≡ 0 (mod p^2) for split primes p ≡ 1 mod 3."""
    mod = p * p
    return sorted({(-r) % mod for r in phi3_roots_mod_prime_square(p)})


def phi6_roots_mod_prime_power(p: int, power: int) -> list[int]:
    """Return the two roots of x^2 - x + 1 ≡ 0 (mod p^power) for split primes p ≡ 1 mod 3."""
    mod = p**power
    return sorted({(-r) % mod for r in phi3_roots_mod_prime_power(p, power)})


def local_divisibility_density(split_prime: int, valuation_floor: int) -> float:
    """p-adic density of q with v_p(Phi3(q)) >= valuation_floor for split primes p ≡ 1 mod 3."""
    if not is_prime(split_prime) or split_prime % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if valuation_floor < 1:
        raise ValueError("valuation_floor must be >= 1")
    return 2 / (split_prime**valuation_floor)


def local_exact_valuation_density(split_prime: int, valuation: int) -> float:
    """p-adic density of q with v_p(Phi3(q)) exactly equal to valuation."""
    if valuation < 1:
        raise ValueError("valuation must be >= 1")
    p = split_prime
    return local_divisibility_density(p, valuation) - local_divisibility_density(p, valuation + 1)


def valuation_tree(split_prime: int, max_power: int = 5) -> dict[str, object]:
    """Return the lifted residue branches and local densities for a split prime."""
    if max_power < 1:
        raise ValueError("max_power must be >= 1")
    return {
        "prime": split_prime,
        "phi3_roots": {str(power): phi3_roots_mod_prime_power(split_prime, power) for power in range(1, max_power + 1)},
        "phi6_roots": {str(power): phi6_roots_mod_prime_power(split_prime, power) for power in range(1, max_power + 1)},
        "density_at_least": {str(power): local_divisibility_density(split_prime, power) for power in range(1, max_power + 1)},
        "density_exact": {str(power): local_exact_valuation_density(split_prime, power) for power in range(1, max_power + 1)},
    }


def crt_combine_residues(congruences: list[tuple[int, int]]) -> tuple[int, int]:
    """Combine pairwise-coprime congruences x ≡ a_i (mod m_i) by CRT."""
    x, modulus = 0, 1
    for residue, mod in congruences:
        inv = pow(modulus, -1, mod)
        step = ((residue - x) * inv) % mod
        x += modulus * step
        modulus *= mod
    return x % modulus, modulus


def branch_classes_for_split_prime(split_prime: int, family: str = "Phi3", power: int = 2) -> list[int]:
    if family == "Phi3":
        return phi3_roots_mod_prime_power(split_prime, power)
    if family == "Phi6":
        return phi6_roots_mod_prime_power(split_prime, power)
    raise ValueError("family must be 'Phi3' or 'Phi6'")


def finite_cutoff_branch_classes(split_primes: list[int], family: str = "Phi3", power: int = 2) -> dict[str, object]:
    """Return simultaneous CRT branch classes for a finite set of split primes."""
    branches = [branch_classes_for_split_prime(p, family=family, power=power) for p in split_primes]
    congruence_choices = []
    from itertools import product
    for residues in product(*branches):
        congruence_choices.append(list(zip(residues, [p**power for p in split_primes])))

    classes = []
    modulus = 1
    for p in split_primes:
        modulus *= p**power
    for system in congruence_choices:
        x, _ = crt_combine_residues(system)
        classes.append(x)

    classes = sorted(set(classes))
    density = len(classes) / modulus if modulus else 0.0
    return {
        "split_primes": split_primes,
        "family": family,
        "power": power,
        "modulus": modulus,
        "classes": classes,
        "class_count": len(classes),
        "expected_class_count": 2 ** len(split_primes),
        "density": density,
    }


def finite_cutoff_defect_density(split_primes: list[int], power: int = 2) -> float:
    density = 1.0
    for p in split_primes:
        density *= 2 / (p**power)
    return density


def finite_cutoff_avoidance_density(split_primes: list[int], power: int = 2) -> float:
    density = 1.0
    for p in split_primes:
        density *= 1 - 2 / (p**power)
    return density


def finite_adelic_valuation_pgf(split_primes: list[int], t: float) -> float:
    """Exact finite-adelic PGF for the total valuation packet over a finite split-prime set."""
    value = 1.0
    for p in split_primes:
        value *= local_valuation_pgf(p, t)
    return value


def finite_adelic_valuation_euler_factor(split_primes: list[int], s: float) -> float:
    """Finite product of local Euler factors for the total valuation packet."""
    value = 1.0
    for p in split_primes:
        value *= local_valuation_euler_factor(p, s)
    return value


def finite_adelic_expected_valuation(split_primes: list[int]) -> Fraction:
    """Exact mean of the total valuation packet over a finite split-prime set."""
    total = Fraction(0, 1)
    for p in split_primes:
        total += Fraction(2, p - 1)
    return total


def finite_adelic_variance_valuation(split_primes: list[int]) -> Fraction:
    """Exact variance of the total valuation packet over a finite split-prime set."""
    return finite_adelic_expected_valuation(split_primes)


def split_prime_packet_mean(prime_limit: int) -> Fraction:
    """Exact mean/variance of the split-prime valuation packet up to a prime cutoff."""
    total = Fraction(0, 1)
    for p in split_primes_mod_3(prime_limit):
        total += Fraction(2, p - 1)
    return total


def fraction_to_text(value: Fraction, max_digits: int = 1000) -> str | None:
    """Render manageable exact fractions while avoiding giant integer-to-string payloads."""
    numerator_digits = int(value.numerator.bit_length() * math.log10(2)) + 1
    denominator_digits = int(value.denominator.bit_length() * math.log10(2)) + 1
    if max(numerator_digits, denominator_digits) > max_digits:
        return None
    return f"{value.numerator}/{value.denominator}"


def split_prime_packet_profile(prime_limits: list[int]) -> list[dict[str, object]]:
    """Return the growth profile of the split-prime valuation packet over prime cutoffs."""
    rows = []
    for prime_limit in prime_limits:
        mean = split_prime_packet_mean(prime_limit)
        loglog = math.log(math.log(prime_limit)) if prime_limit > 2 else float("-inf")
        rows.append(
            {
                "prime_limit": prime_limit,
                "split_prime_count": len(split_primes_mod_3(prime_limit)),
                "mean_fraction": fraction_to_text(mean),
                "mean": float(mean),
                "variance_fraction": fraction_to_text(mean),
                "variance": float(mean),
                "loglog": loglog,
                "mean_minus_loglog": float(mean) - loglog,
            }
        )
    return rows


def split_prime_packet_pgf(prime_limit: int, t: float) -> float:
    """Finite split-prime PGF cutoff G_X(t) over p<=X, p ≡ 1 (mod 3)."""
    return finite_adelic_valuation_pgf(split_primes_mod_3(prime_limit), t)


def split_prime_mertens_product(prime_limit: int) -> float:
    """Residue-class Mertens kernel over split primes p<=X, p ≡ 1 (mod 3)."""
    product = 1.0
    for p in split_primes_mod_3(prime_limit):
        product *= 1 - 1 / p
    return product


def split_prime_mertens_normalized(prime_limit: int) -> float:
    """Normalized residue-class Mertens kernel sqrt(log X) * Product_{p<=X, p≡1(3)} (1-1/p)."""
    if prime_limit <= 1:
        return 0.0
    return (math.log(prime_limit) ** 0.5) * split_prime_mertens_product(prime_limit)


def split_prime_completed_local_factor(split_prime: int, t: float) -> float:
    """Renormalized local factor with the Mertens singularity removed."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return ((p - 2 + t) / (p - t)) * ((1 - 1 / p) ** (-2 * (1 - t)))


def split_prime_completed_pgf(prime_limit: int, t: float) -> float:
    """Completed split-prime Euler product with the logarithmic Mertens kernel removed."""
    value = 1.0
    for p in split_primes_mod_3(prime_limit):
        value *= split_prime_completed_local_factor(p, t)
    return value


def completed_local_centered_reciprocity(split_prime: int, offset: float) -> float:
    """Return C_p(1+u) C_p(1-u) for the completed local factor."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return split_prime_completed_local_factor(p, 1 + offset) * split_prime_completed_local_factor(p, 1 - offset)


def completed_global_centered_reciprocity(prime_limit: int, offset: float) -> float:
    """Return C_X(1+u) C_X(1-u) for the completed split-prime product."""
    return split_prime_completed_pgf(prime_limit, 1 + offset) * split_prime_completed_pgf(prime_limit, 1 - offset)


def completed_local_log_nth_derivative_at_one(split_prime: int, order: int) -> float:
    """Exact nth derivative of log C_p(t) at t=1 for the completed local factor."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if order < 1:
        raise ValueError("order must be >= 1")
    if order == 1:
        return completed_local_log_derivative_at_one(p)
    if order % 2 == 0:
        return 0.0
    return 2 * math.factorial(order - 1) / ((p - 1) ** order)


def completed_log_nth_derivative_at_one(prime_limit: int, order: int) -> float:
    """Finite-cutoff nth derivative of log C_X(t) at t=1."""
    return sum(completed_local_log_nth_derivative_at_one(p, order) for p in split_primes_mod_3(prime_limit))


def completed_higher_cumulant_profile(prime_limits: list[int], orders: list[int]) -> dict[str, list[dict[str, object]]]:
    """Profile the centered reciprocity and higher completed cumulants at t=1."""
    payload: dict[str, list[dict[str, object]]] = {}
    for order in orders:
        key = str(order)
        rows = []
        for prime_limit in prime_limits:
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "split_prime_count": len(split_primes_mod_3(prime_limit)),
                    "log_derivative_at_one": completed_log_nth_derivative_at_one(prime_limit, order),
                }
            )
        payload[key] = rows
    return payload


def completed_reciprocity_profile(prime_limits: list[int], offsets: list[float]) -> dict[str, list[dict[str, object]]]:
    """Profile the exact centered reciprocity C_X(1+u) C_X(1-u)=1 numerically."""
    payload: dict[str, list[dict[str, object]]] = {}
    for offset in offsets:
        key = str(offset)
        rows = []
        for prime_limit in prime_limits:
            product = completed_global_centered_reciprocity(prime_limit, offset)
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "offset": offset,
                    "reciprocity_product": product,
                    "abs_error_from_one": abs(product - 1.0),
                }
            )
        payload[key] = rows
    return payload


def completed_local_log_derivative_at_one(split_prime: int) -> float:
    """First derivative of log of the completed local factor at t=1."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return 2 / (p - 1) + 2 * math.log(1 - 1 / p)


def completed_cumulant_constant(prime_limit: int) -> float:
    """Finite-cutoff first cumulant/tangent constant of the completed product at t=1."""
    return sum(completed_local_log_derivative_at_one(p) for p in split_primes_mod_3(prime_limit))


def completed_tangent_profile(prime_limits: list[int]) -> list[dict[str, object]]:
    """Profile convergence of the completed tangent/cumulant constant at t=1."""
    rows = []
    for prime_limit in prime_limits:
        mean = float(split_prime_packet_mean(prime_limit))
        mertens = split_prime_mertens_product(prime_limit)
        tangent = completed_cumulant_constant(prime_limit)
        rows.append(
            {
                "prime_limit": prime_limit,
                "split_prime_count": len(split_primes_mod_3(prime_limit)),
                "packet_mean": mean,
                "mertens_product": mertens,
                "twice_log_mertens": 2 * math.log(mertens),
                "completed_tangent_constant": tangent,
                "recombined": mean + 2 * math.log(mertens),
            }
        )
    return rows


def prime_weight(split_prime: int, s: complex) -> complex:
    """Return p^{-s} on the principal branch."""
    return cmath.exp(-s * math.log(split_prime))


def defect_dirichlet_local_factor(split_prime: int, s: complex) -> complex:
    """Local Dirichlet/Euler factor E[p^{-sV_p}] for the split-prime defect packet."""
    p = split_prime
    z = prime_weight(p, s)
    return (p - 2 + z) / (p - z)


def defect_dirichlet_product(prime_limit: int, s: complex) -> complex:
    """Finite-cutoff global defect Dirichlet product over split primes."""
    value = 1 + 0j
    for p in split_primes_mod_3(prime_limit):
        value *= defect_dirichlet_local_factor(p, s)
    return value


def completed_defect_dirichlet_local_factor(split_prime: int, s: complex) -> complex:
    """Completed local Dirichlet factor with the split-prime Mertens singularity removed."""
    p = split_prime
    z = prime_weight(p, s)
    return defect_dirichlet_local_factor(p, s) * cmath.exp(-2 * (1 - z) * math.log(1 - 1 / p))


def completed_defect_dirichlet_product(prime_limit: int, s: complex) -> complex:
    """Finite-cutoff completed global Dirichlet product over split primes."""
    value = 1 + 0j
    for p in split_primes_mod_3(prime_limit):
        value *= completed_defect_dirichlet_local_factor(p, s)
    return value


def completed_defect_dirichlet_log_derivative(prime_limit: int, s: complex) -> complex:
    """Logarithmic derivative of the completed defect Dirichlet product."""
    total = 0 + 0j
    for p in split_primes_mod_3(prime_limit):
        z = prime_weight(p, s)
        zprime = -math.log(p) * z
        total += zprime * (1 / (p - 2 + z) + 1 / (p - z) + 2 * math.log(1 - 1 / p))
    return total


def completed_defect_dirichlet_profile(prime_limits: list[int], s_values: list[float]) -> dict[str, list[dict[str, object]]]:
    """Profile the completed defect Dirichlet package on positive real s-values."""
    payload: dict[str, list[dict[str, object]]] = {}
    for s in s_values:
        key = str(s)
        rows = []
        for prime_limit in prime_limits:
            raw = defect_dirichlet_product(prime_limit, s)
            completed = completed_defect_dirichlet_product(prime_limit, s)
            deriv = completed_defect_dirichlet_log_derivative(prime_limit, s)
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "raw_real": raw.real,
                    "raw_imag": raw.imag,
                    "completed_real": completed.real,
                    "completed_imag": completed.imag,
                    "completed_log_derivative_real": deriv.real,
                    "completed_log_derivative_imag": deriv.imag,
                }
            )
        payload[key] = rows
    return payload


def eisenstein_split_ideal_data(split_prime: int, power: int = 1) -> dict[str, object]:
    """Symbolic split-prime ideal packet above p in Z[ω]."""
    if not is_prime(split_prime) or split_prime % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    mod = split_prime**power
    roots = phi3_roots_mod_prime_power(split_prime, power)
    packet = []
    for index, residue in enumerate(roots, start=1):
        conjugate_residue = (-1 - residue) % mod
        phi6_residue = (-residue) % mod
        packet.append(
            {
                "ideal_label": f"pi_{split_prime}_{index}",
                "split_prime": split_prime,
                "power": power,
                "phi3_residue": residue,
                "phi6_residue": phi6_residue,
                "ideal_generator": f"({split_prime}, ω-{residue})",
                "conjugate_ideal_generator": f"({split_prime}, ω-{conjugate_residue})",
            }
        )
    return {
        "split_prime": split_prime,
        "power": power,
        "modulus": mod,
        "packet": packet,
        "theorem_summary": (
            "For split primes p ≡ 1 mod 3, the two roots of x^2+x+1 modulo p^n define the two prime ideals above p in Z[ω], "
            "written symbolically as (p, ω-r)."
        ),
    }


def eisenstein_ideal_witness(q: int, family: str) -> dict[str, object]:
    """Translate a cyclotomic factorization witness into prime-ideal language in Z[ω]."""
    if family not in {"Phi3", "Phi6"}:
        raise ValueError("family must be 'Phi3' or 'Phi6'")
    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    factors = prime_factorization(value)
    witnesses = []
    target_sign = "q-ω" if family == "Phi3" else "q+ω"

    for p, exponent in sorted(factors.items()):
        if not is_prime(p) or p % 3 != 1:
            continue
        packet = eisenstein_split_ideal_data(p, power=exponent)
        q_mod = q % (p**exponent)
        chosen = None
        for row in packet["packet"]:
            residue = row["phi3_residue"] if family == "Phi3" else row["phi6_residue"]
            if residue == q_mod:
                chosen = row
                break
        if chosen is not None:
            witnesses.append(
                {
                    "split_prime": p,
                    "valuation": exponent,
                    "q_mod_prime_power": q_mod,
                    "ideal_label": chosen["ideal_label"],
                    "ideal_generator": chosen["ideal_generator"],
                    "packet_target": target_sign,
                    "statement": f"{chosen['ideal_label']}^{exponent} divides ({target_sign}) in Z[ω]",
                }
            )

    return {
        "q": q,
        "family": family,
        "value": value,
        "factorization": factors,
        "target_packet": target_sign,
        "ideal_witnesses": witnesses,
    }


def cyclotomic_ljunggren_reduction(q: int, family: str) -> dict[str, object]:
    """Reduce Phi3/Phi6 perfect powers to the Ljunggren equation x^2 + 3 = 4 y^n."""
    if family not in {"Phi3", "Phi6"}:
        raise ValueError("family must be 'Phi3' or 'Phi6'")
    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    x = 2 * q + 1 if family == "Phi3" else 2 * q - 1
    return {
        "q": q,
        "family": family,
        "x": x,
        "value": value,
        "equation_check": x * x + 3 == 4 * value,
        "equation": f"{x}^2 + 3 = 4*{value}",
    }


def cyclotomic_known_perfect_power_solutions() -> list[dict[str, object]]:
    """Known nontrivial positive-q perfect-power solutions obtained from the Ljunggren equation."""
    return [
        {"family": "Phi3", "q": 18, "value": 343, "base": 7, "exponent": 3, "x": 37},
        {"family": "Phi6", "q": 19, "value": 343, "base": 7, "exponent": 3, "x": 37},
    ]


def cyclotomic_perfect_power_theorem() -> dict[str, object]:
    """Return the global perfect-power theorem package via reduction to x^2+3=4y^n."""
    return {
        "reduction": (
            "Phi3(q)=y^n iff (2q+1)^2 + 3 = 4 y^n, and Phi6(q)=y^n iff (2q-1)^2 + 3 = 4 y^n. "
            "Thus nontrivial perfect-power points on the cyclotomic packet reduce to the classical Ljunggren equation x^2+3=4y^n."
        ),
        "classical_input": "Ljunggren theorem: the only nontrivial positive solution of x^2+3=4y^n with y>1, n>1 is (x,y,n)=(37,7,3).",
        "solutions": cyclotomic_known_perfect_power_solutions(),
        "theorem_summary": (
            "For q>=3 and n>1, the only nontrivial perfect-power values in Phi3(q)=q^2+q+1 and Phi6(q)=q^2-q+1 are "
            "Phi3(18)=7^3 and Phi6(19)=7^3."
        ),
    }


def split_prime_packet_pgf_profile(prime_limits: list[int], t_values: list[float]) -> dict[str, list[dict[str, object]]]:
    """Profile the global PGF decay and its logarithmically normalized shadow."""
    payload: dict[str, list[dict[str, object]]] = {}
    for t in t_values:
        key = str(t)
        rows = []
        for prime_limit in prime_limits:
            pgf = split_prime_packet_pgf(prime_limit, t)
            exponent = 1 - t
            normalized = pgf * (math.log(prime_limit) ** exponent) if prime_limit > 1 else pgf
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "pgf": pgf,
                    "normalizing_exponent": exponent,
                    "normalized_pgf": normalized,
                }
            )
        payload[key] = rows
    return payload


def split_prime_completed_pgf_profile(prime_limits: list[int], t_values: list[float]) -> dict[str, list[dict[str, object]]]:
    """Profile the completed split-prime product and its factorization of the normalized shadow."""
    payload: dict[str, list[dict[str, object]]] = {}
    for t in t_values:
        key = str(t)
        rows = []
        for prime_limit in prime_limits:
            pgf = split_prime_packet_pgf(prime_limit, t)
            mertens = split_prime_mertens_product(prime_limit)
            normalized_mertens = split_prime_mertens_normalized(prime_limit)
            completed = split_prime_completed_pgf(prime_limit, t)
            exponent = 1 - t
            shadow_recovered = completed * (normalized_mertens ** (2 * exponent))
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "pgf": pgf,
                    "mertens_product": mertens,
                    "normalized_mertens": normalized_mertens,
                    "completed_pgf": completed,
                    "normalizing_exponent": exponent,
                    "shadow_recovered": shadow_recovered,
                }
            )
        payload[key] = rows
    return payload


def local_valuation_pgf(split_prime: int, t: float) -> float:
    """Probability generating function E[t^V] for V = v_p(Phi3(q)) on the p-adic defect tree."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return (p - 2 + t) / (p - t)


def local_valuation_euler_factor(split_prime: int, s: float) -> float:
    """Dirichlet/Euler-factor form E[p^{-sV}] for the local valuation law."""
    p = split_prime
    return local_valuation_pgf(p, p ** (-s))


def local_expected_valuation(split_prime: int) -> float:
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return 2 / (p - 1)


def local_variance_valuation(split_prime: int) -> float:
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return 2 / (p - 1)


def is_nonsquarefree_cyclotomic_value(q: int, family: str) -> bool:
    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    return any(exponent > 1 for exponent in prime_factorization(value).values())


def defect_match_for_q(q: int, family: str) -> dict[str, object]:
    """Return the matching split-prime residue witness for a defect q, if one exists."""
    if family not in {"Phi3", "Phi6"}:
        raise ValueError("family must be 'Phi3' or 'Phi6'")
    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    factors = prime_factorization(value)
    roots_fn = phi3_roots_mod_prime_square if family == "Phi3" else phi6_roots_mod_prime_square

    for p, exponent in factors.items():
        if exponent <= 1 or p % 3 != 1 or not is_prime(p):
            continue
        residues = roots_fn(p)
        if q % (p * p) in residues:
            return {
                "matched": True,
                "prime": p,
                "residues_mod_p2": residues,
                "q_mod_p2": q % (p * p),
                "value": value,
                "factorization": factors,
            }

    return {
        "matched": False,
        "value": value,
        "factorization": factors,
    }


def defect_residue_classifier(limit_q: int = 1000, prime_limit: int = 200) -> dict[str, object]:
    split_primes = split_primes_mod_3(prime_limit)
    residue_table = {
        str(p): {
            "Phi3": phi3_roots_mod_prime_square(p),
            "Phi6": phi6_roots_mod_prime_square(p),
            "order3_units": nontrivial_cube_roots_mod_prime_square(p),
        }
        for p in split_primes
    }

    phi3_failures = []
    phi6_failures = []
    phi3_exact = True
    phi6_exact = True

    for q in range(3, limit_q + 1):
        if is_nonsquarefree_cyclotomic_value(q, "Phi3"):
            witness = defect_match_for_q(q, "Phi3")
            row = {"q": q, **witness}
            phi3_failures.append(row)
            phi3_exact = phi3_exact and bool(witness["matched"])
        if is_nonsquarefree_cyclotomic_value(q, "Phi6"):
            witness = defect_match_for_q(q, "Phi6")
            row = {"q": q, **witness}
            phi6_failures.append(row)
            phi6_exact = phi6_exact and bool(witness["matched"])

    return {
        "limit_q": limit_q,
        "prime_limit": prime_limit,
        "split_primes": split_primes,
        "residue_table": residue_table,
        "phi3_failures": phi3_failures,
        "phi6_failures": phi6_failures,
        "phi3_exact_classifier": phi3_exact,
        "phi6_exact_classifier": phi6_exact,
        "exact_classifier": phi3_exact and phi6_exact,
        "cube_root_restatement": (
            "x^2 + x + 1 ≡ 0 (mod p^2) iff x is a nontrivial cube root of unity modulo p^2, because "
            "x^3 - 1 = (x - 1)(x^2 + x + 1). For split primes p ≡ 1 (mod 3) there are exactly two such roots, "
            "and the Phi6 roots are their negatives modulo p^2."
        ),
    }


def perfect_power_decomposition(n: int) -> tuple[bool, int | None, int | None]:
    """Return whether n is a perfect power a^k with k>1, and one witness if so."""
    max_k = n.bit_length()
    for k in range(2, max_k + 1):
        lo, hi = 1, 1 << ((n.bit_length() + k - 1) // k)
        while lo <= hi:
            mid = (lo + hi) // 2
            p = mid**k
            if p == n:
                return True, mid, k
            if p < n:
                lo = mid + 1
            else:
                hi = mid - 1
    return False, None, None


def cyclotomic_perfect_power_scan(limit_q: int = 100000) -> dict[str, object]:
    """Scan Phi3(q) and Phi6(q) for perfect powers up to the supplied q-limit."""
    phi3_hits = []
    phi6_hits = []

    for q in range(3, limit_q + 1):
        ok3, base3, exponent3 = perfect_power_decomposition(phi3_value(q))
        if ok3:
            phi3_hits.append({"q": q, "value": phi3_value(q), "base": base3, "exponent": exponent3})

        ok6, base6, exponent6 = perfect_power_decomposition(phi6_value(q))
        if ok6:
            phi6_hits.append({"q": q, "value": phi6_value(q), "base": base6, "exponent": exponent6})

    return {
        "limit_q": limit_q,
        "phi3_hits": phi3_hits,
        "phi6_hits": phi6_hits,
        "phi3_unique_cube_defect": phi3_hits == [{"q": 18, "value": 343, "base": 7, "exponent": 3}],
        "phi6_unique_cube_defect": phi6_hits == [{"q": 19, "value": 343, "base": 7, "exponent": 3}],
    }


def defect_density_partial_product(prime_limit: int = 200000) -> dict[str, object]:
    """Return the split-prime Euler-product density estimate for the defect locus."""
    partial = 1.0
    primes = split_primes_mod_3(prime_limit)
    for p in primes:
        partial *= 1 - 2 / (p * p)
    return {
        "prime_limit": prime_limit,
        "split_primes": primes,
        "squarefree_complement_density_estimate": partial,
        "defect_density_estimate": 1 - partial,
    }


def empirical_defect_density(limit_q: int = 20000) -> dict[str, object]:
    """Return empirical defect densities for Phi3 and Phi6 on 3 <= q <= limit_q."""
    total = max(0, limit_q - 2)
    phi3_count = sum(1 for q in range(3, limit_q + 1) if is_nonsquarefree_cyclotomic_value(q, "Phi3"))
    phi6_count = sum(1 for q in range(3, limit_q + 1) if is_nonsquarefree_cyclotomic_value(q, "Phi6"))
    return {
        "limit_q": limit_q,
        "phi3_count": phi3_count,
        "phi6_count": phi6_count,
        "phi3_density": (phi3_count / total) if total else 0.0,
        "phi6_density": (phi6_count / total) if total else 0.0,
    }