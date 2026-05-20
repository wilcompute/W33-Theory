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
    return completed_defect_local_factor_from_z(p, z)


def defect_dirichlet_local_factor_from_z(split_prime: int, z: complex) -> complex:
    """Local Dirichlet factor viewed in the spectral coordinate z = p^{-s}."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return (p - 2 + z) / (p - z)


def completed_defect_local_factor_from_z(split_prime: int, z: complex) -> complex:
    """Completed local defect factor in the centered spectral variable z = p^{-s}."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return defect_dirichlet_local_factor_from_z(p, z) * cmath.exp(-2 * (1 - z) * math.log(1 - 1 / p))


def completed_defect_local_centered_reciprocity_from_z(split_prime: int, z: complex) -> complex:
    """Local centered reciprocity in z: Dhat_p(z) Dhat_p(2-z) = 1."""
    p = split_prime
    return completed_defect_local_factor_from_z(p, z) * completed_defect_local_factor_from_z(p, 2 - z)


def defect_spectral_involution(split_prime: int, s: complex) -> complex:
    """Local spectral involution in the s-variable induced by z -> 2-z."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return -cmath.log(2 - prime_weight(p, s)) / math.log(p)


def completed_defect_local_centered_reciprocity_in_s(split_prime: int, s: complex) -> complex:
    """Local reciprocity pulled back to s via the split-prime spectral involution."""
    s_star = defect_spectral_involution(split_prime, s)
    return completed_defect_dirichlet_local_factor(split_prime, s) * completed_defect_dirichlet_local_factor(split_prime, s_star)


def completed_defect_local_log_artanh_form(split_prime: int, z: complex) -> complex:
    """Closed-form logarithm of the completed local factor in centered spectral variable z."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    u = z - 1
    return 2 * cmath.atanh(u / (p - 1)) + 2 * u * math.log(1 - 1 / p)


def completed_defect_local_log_artanh_series(split_prime: int, z: complex, max_terms: int = 8) -> complex:
    """Truncated artanh-series log expansion for the completed local factor."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if max_terms < 1:
        raise ValueError("max_terms must be >= 1")
    u = z - 1
    x = u / (p - 1)
    series = sum((x ** (2 * m + 1)) / (2 * m + 1) for m in range(max_terms))
    return 2 * series + 2 * u * math.log(1 - 1 / p)


def completed_defect_adelic_product(z_by_prime: dict[int, complex]) -> complex:
    """Finite adelic completed defect package on independent split-prime spectral coordinates."""
    value = 1 + 0j
    for p, z in sorted(z_by_prime.items()):
        value *= completed_defect_local_factor_from_z(p, z)
    return value


def completed_defect_adelic_centered_reciprocity(z_by_prime: dict[int, complex]) -> complex:
    """Adelic centered reciprocity: Dhat(z_p) Dhat(2-z_p) = 1 coordinatewise."""
    return completed_defect_adelic_product(z_by_prime) * completed_defect_adelic_product({p: 2 - z for p, z in z_by_prime.items()})


def completed_defect_adelic_log_artanh(z_by_prime: dict[int, complex]) -> complex:
    """Closed-form adelic logarithm as a sum of local artanh packets."""
    total = 0 + 0j
    for p, z in sorted(z_by_prime.items()):
        total += completed_defect_local_log_artanh_form(p, z)
    return total


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


def completed_defect_dirichlet_reciprocity_profile(prime_limits: list[int], s_values: list[float]) -> dict[str, list[dict[str, object]]]:
    """Profile the local spectral involution and centered reciprocity on the diagonal s-line."""
    payload: dict[str, list[dict[str, object]]] = {}
    for s in s_values:
        key = str(s)
        rows = []
        for prime_limit in prime_limits:
            local_rows = []
            for p in split_primes_mod_3(prime_limit):
                reciprocity = completed_defect_local_centered_reciprocity_in_s(p, s)
                local_rows.append(
                    {
                        "split_prime": p,
                        "spectral_involution_real": defect_spectral_involution(p, s).real,
                        "spectral_involution_imag": defect_spectral_involution(p, s).imag,
                        "reciprocity_real": reciprocity.real,
                        "reciprocity_imag": reciprocity.imag,
                    }
                )
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "first_local_rows": local_rows[:6],
                    "max_abs_local_error_from_one": max(abs(row["reciprocity_real"] - 1.0) + abs(row["reciprocity_imag"]) for row in local_rows),
                }
            )
        payload[key] = rows
    return payload


def completed_defect_dirichlet_log_artanh(prime_limit: int, s: complex) -> complex:
    """Exact global log of the completed Dirichlet product via the centered artanh form."""
    total = 0 + 0j
    for p in split_primes_mod_3(prime_limit):
        total += completed_defect_local_log_artanh_form(p, prime_weight(p, s))
    return total


def completed_defect_dirichlet_log_artanh_series(prime_limit: int, s: complex, max_terms: int = 8) -> complex:
    """Truncated global artanh-series expansion of the completed Dirichlet log."""
    total = 0 + 0j
    for p in split_primes_mod_3(prime_limit):
        total += completed_defect_local_log_artanh_series(p, prime_weight(p, s), max_terms=max_terms)
    return total


def completed_defect_spectral_coordinate(split_prime: int, s: complex) -> complex:
    """Centered split-prime spectral coordinate x_p(s) = (p^{-s}-1)/(p-1)."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return (prime_weight(p, s) - 1) / (p - 1)


def completed_defect_counterterm_local(split_prime: int, s: complex, deformation: complex = 1.0) -> complex:
    """Local Mertens-counterterm factor in the completed spectral package."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    return cmath.exp(2 * deformation * (prime_weight(p, s) - 1) * math.log(1 - 1 / p))


def completed_defect_spectral_local_factor(split_prime: int, s: complex, deformation: complex = 1.0) -> complex:
    """Canonical local spectral L-family; deformation=1 recovers the completed Dirichlet factor."""
    x = completed_defect_spectral_coordinate(split_prime, s)
    return ((1 + deformation * x) / (1 - deformation * x)) * completed_defect_counterterm_local(split_prime, s, deformation=deformation)


def completed_defect_spectral_local_log(split_prime: int, s: complex, deformation: complex = 1.0) -> complex:
    """Closed-form logarithm of the local spectral L-family."""
    p = split_prime
    x = completed_defect_spectral_coordinate(split_prime, s)
    return 2 * cmath.atanh(deformation * x) + 2 * deformation * (prime_weight(p, s) - 1) * math.log(1 - 1 / p)


def completed_defect_spectral_L_function(prime_limit: int, s: complex, deformation: complex = 1.0) -> complex:
    """Finite-cutoff completed spectral L-family over split primes."""
    value = 1 + 0j
    for p in split_primes_mod_3(prime_limit):
        value *= completed_defect_spectral_local_factor(p, s, deformation=deformation)
    return value


def completed_defect_spectral_log(prime_limit: int, s: complex, deformation: complex = 1.0) -> complex:
    """Global logarithm of the completed spectral L-family."""
    total = 0 + 0j
    for p in split_primes_mod_3(prime_limit):
        total += completed_defect_spectral_local_log(p, s, deformation=deformation)
    return total


def completed_defect_spectral_reciprocity(prime_limit: int, s: complex, deformation: complex = 1.0) -> complex:
    """Oddness in the deformation variable: Lambda(s;λ)Lambda(s;-λ)=1."""
    return completed_defect_spectral_L_function(prime_limit, s, deformation=deformation) * completed_defect_spectral_L_function(prime_limit, s, deformation=-deformation)


def completed_defect_spectral_profile(prime_limits: list[int], s_values: list[float], deformations: list[float]) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Profile the completed spectral L-family over cutoffs, s-values, and deformation strengths."""
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            for prime_limit in prime_limits:
                value = completed_defect_spectral_L_function(prime_limit, s, deformation=deformation)
                log_value = completed_defect_spectral_log(prime_limit, s, deformation=deformation)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "value_real": value.real,
                        "value_imag": value.imag,
                        "log_real": log_value.real,
                        "log_imag": log_value.imag,
                        "abs_reciprocity_error": abs(completed_defect_spectral_reciprocity(prime_limit, s, deformation=deformation) - 1.0),
                    }
                )
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_local_radius(split_prime: int, s: complex) -> float:
    """Analytic radius in the deformation variable λ for one split-prime local factor."""
    x = completed_defect_spectral_coordinate(split_prime, s)
    magnitude = abs(x)
    if magnitude == 0:
        return math.inf
    return 1.0 / magnitude


def completed_defect_spectral_min_radius(prime_limit: int, s: complex) -> float:
    """Minimum local deformation radius across split primes up to a finite cutoff."""
    radii = [completed_defect_spectral_local_radius(p, s) for p in split_primes_mod_3(prime_limit)]
    if not radii:
        return math.inf
    return min(radii)


def completed_defect_spectral_uniform_radius_lower_bound() -> float:
    """Uniform lower bound on the deformation radius along the positive real s-axis.

    For real s > 0, one has 0 < p^{-s} < 1, so |x_p(s)| = |p^{-s}-1|/(p-1) < 1/(p-1).
    The smallest split prime is p = 7, hence every local factor is analytic for |λ| < 6,
    and therefore every finite-cutoff global log packet has a uniformly convergent odd Taylor
    tower on that disk.
    """
    return 6.0


def completed_defect_spectral_local_log_odd_coefficient(split_prime: int, s: complex, order: int) -> complex:
    """Coefficient of λ^order in the local log Taylor tower of the completed spectral family."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if order < 1:
        raise ValueError("order must be >= 1")
    if order % 2 == 0:
        return 0.0 + 0.0j
    z = prime_weight(p, s)
    x = completed_defect_spectral_coordinate(p, s)
    if order == 1:
        return 2 * x + 2 * (z - 1) * math.log(1 - 1 / p)
    return 2 * (x**order) / order


def completed_defect_spectral_log_odd_coefficient(prime_limit: int, s: complex, order: int) -> complex:
    """Coefficient of λ^order in the finite-cutoff global log Taylor tower."""
    return sum(completed_defect_spectral_local_log_odd_coefficient(p, s, order) for p in split_primes_mod_3(prime_limit))


def completed_defect_spectral_local_log_series(split_prime: int, s: complex, deformation: complex = 1.0, max_order: int = 9) -> complex:
    """Truncated odd Taylor tower for the local log of the completed spectral family."""
    if max_order < 1:
        raise ValueError("max_order must be >= 1")
    total = 0.0 + 0.0j
    for order in range(1, max_order + 1, 2):
        total += (deformation**order) * completed_defect_spectral_local_log_odd_coefficient(split_prime, s, order)
    return total


def completed_defect_spectral_log_series(prime_limit: int, s: complex, deformation: complex = 1.0, max_order: int = 9) -> complex:
    """Truncated odd Taylor tower for the finite-cutoff global log of the completed spectral family."""
    if max_order < 1:
        raise ValueError("max_order must be >= 1")
    total = 0.0 + 0.0j
    for order in range(1, max_order + 1, 2):
        total += (deformation**order) * completed_defect_spectral_log_odd_coefficient(prime_limit, s, order)
    return total


def completed_defect_spectral_series_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
    max_orders: list[int],
) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Profile convergence of the odd Taylor tower to the exact completed spectral log."""
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    uniform_radius = completed_defect_spectral_uniform_radius_lower_bound()
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            for prime_limit in prime_limits:
                exact_log = completed_defect_spectral_log(prime_limit, s, deformation=deformation)
                approximants: dict[str, object] = {}
                for max_order in max_orders:
                    series_log = completed_defect_spectral_log_series(prime_limit, s, deformation=deformation, max_order=max_order)
                    approximants[str(max_order)] = {
                        "series_log_real": series_log.real,
                        "series_log_imag": series_log.imag,
                        "abs_series_error": abs(series_log - exact_log),
                    }
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "exact_log_real": exact_log.real,
                        "exact_log_imag": exact_log.imag,
                        "min_local_radius": completed_defect_spectral_min_radius(prime_limit, s),
                        "uniform_radius_lower_bound": uniform_radius,
                        "approximants": approximants,
                    }
                )
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_local_linear_kernel(split_prime: int, s: complex) -> complex:
    """The convergent local kernel underlying the λ-linear coefficient."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    z = prime_weight(p, s)
    return (z - 1) * (1 / (p - 1) + math.log(1 - 1 / p))


def completed_defect_spectral_local_log_odd_coefficient_bound(split_prime: int, s: complex, order: int) -> float:
    """Absolute convergence majorant for one odd Taylor coefficient."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if order < 1:
        raise ValueError("order must be >= 1")
    if order % 2 == 0:
        return 0.0
    if order == 1:
        return 2 * abs(completed_defect_spectral_local_linear_kernel(p, s))
    return (2 / order) * (completed_defect_spectral_local_radius(p, s) ** (-order))


def completed_defect_spectral_log_odd_tail_bound(prime_limit: int, order: int) -> float:
    r"""A simple explicit tail majorant for the odd Taylor coefficients beyond a finite cutoff.

    For order >= 3, use the crude comparison \sum_{n > X} n^{-order}.
    For order = 1, the linear kernel is O(p^{-2}), so we use a coarse 2/X bound.
    """
    if order < 1 or order % 2 == 0:
        raise ValueError("order must be a positive odd integer")
    x = max(prime_limit - 1, 1)
    if order == 1:
        return 2 / x
    return 2 / (order * (order - 1) * (x ** (order - 1)))


def completed_defect_spectral_infinite_cutoff_profile(
    prime_limits: list[int],
    s_values: list[float],
    odd_orders: list[int],
) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Numerical convergence profile for the infinite-cutoff odd Taylor coefficients."""
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for order in odd_orders:
            order_key = str(order)
            rows = []
            previous = None
            for prime_limit in prime_limits:
                coeff = completed_defect_spectral_log_odd_coefficient(prime_limit, s, order)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "coefficient_real": coeff.real,
                        "coefficient_imag": coeff.imag,
                        "abs_jump_from_previous": abs(coeff - previous) if previous is not None else None,
                        "tail_bound": completed_defect_spectral_log_odd_tail_bound(prime_limit, order),
                    }
                )
                previous = coeff
            payload[outer_key][order_key] = rows
    return payload


def completed_defect_spectral_local_log_lambda_derivative(
    split_prime: int,
    s: complex,
    order: int,
    deformation: complex = 0.0,
) -> complex:
    """Exact λ-derivative of the local spectral log at an arbitrary deformation point."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if order < 1:
        raise ValueError("order must be >= 1")
    x = completed_defect_spectral_coordinate(p, s)
    z = prime_weight(p, s)
    if order == 1:
        return 2 * x / (1 - (deformation * x) ** 2) + 2 * (z - 1) * math.log(1 - 1 / p)
    return math.factorial(order - 1) * (x**order) * (
        (1 / ((1 - deformation * x) ** order)) + ((-1) ** (order - 1)) / ((1 + deformation * x) ** order)
    )


def completed_defect_spectral_log_lambda_derivative(
    prime_limit: int,
    s: complex,
    order: int,
    deformation: complex = 0.0,
) -> complex:
    """Finite-cutoff λ-derivative of the global spectral log."""
    total = 0.0 + 0.0j
    for p in split_primes_mod_3(prime_limit):
        total += completed_defect_spectral_local_log_lambda_derivative(p, s, order, deformation=deformation)
    return total


def completed_defect_spectral_deformation_cumulant_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformation_points: list[float],
    orders: list[int],
) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Profile deformation-side cumulants/Hessians at λ=0, λ=1, or other points."""
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformation_points:
            inner_key = str(deformation)
            rows = []
            for prime_limit in prime_limits:
                row = {"prime_limit": prime_limit}
                for order in orders:
                    deriv = completed_defect_spectral_log_lambda_derivative(prime_limit, s, order, deformation=deformation)
                    row[f"order_{order}_real"] = deriv.real
                    row[f"order_{order}_imag"] = deriv.imag
                rows.append(row)
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_action(prime_limit: int, s: complex, deformation: complex = 1.0) -> complex:
    """Completed spectral action / free-energy functional: minus the global spectral log."""
    return -completed_defect_spectral_log(prime_limit, s, deformation=deformation)


def completed_defect_spectral_order_parameter(prime_limit: int, s: complex, deformation: complex = 1.0) -> complex:
    """Deformation-side order parameter: first derivative of the spectral action."""
    return -completed_defect_spectral_log_lambda_derivative(prime_limit, s, 1, deformation=deformation)


def completed_defect_spectral_hessian(prime_limit: int, s: complex, deformation: complex = 1.0) -> complex:
    """Deformation-side Hessian / susceptibility of the spectral action."""
    return -completed_defect_spectral_log_lambda_derivative(prime_limit, s, 2, deformation=deformation)


def completed_defect_spectral_free_energy_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Profile the spectral action, order parameter, and Hessian on real slices."""
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            for prime_limit in prime_limits:
                action = completed_defect_spectral_action(prime_limit, s, deformation=deformation)
                order_parameter = completed_defect_spectral_order_parameter(prime_limit, s, deformation=deformation)
                hessian = completed_defect_spectral_hessian(prime_limit, s, deformation=deformation)
                third = -completed_defect_spectral_log_lambda_derivative(prime_limit, s, 3, deformation=deformation)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "action_real": action.real,
                        "action_imag": action.imag,
                        "order_parameter_real": order_parameter.real,
                        "order_parameter_imag": order_parameter.imag,
                        "hessian_real": hessian.real,
                        "hessian_imag": hessian.imag,
                        "third_derivative_real": third.real,
                        "third_derivative_imag": third.imag,
                        "information_content": -action.real,
                    }
                )
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_log_compact_tail_bound(prime_limit: int, deformation_radius: float) -> float:
    """Certified uniform tail bound for the completed spectral log on |λ| <= deformation_radius.

    For real s > 0, the local spectral coordinate satisfies |x_p(s)| < 1/(p-1). Splitting the
    local log into the convergent linear kernel plus the odd artanh tail gives the coarse bound

        |log Λ_∞ - log Λ_X| <= 2ρ/X + ρ^3 / (3(1-(ρ/X)^2)X^2)

    with X replaced by max(prime_limit, 6), since the first split prime is p = 7 and thus p-1 >= 6.
    This is uniform in s on the positive real axis and uniform on compact λ-disks with 0 <= ρ < 6.
    """
    if prime_limit < 1:
        raise ValueError("prime_limit must be >= 1")
    if deformation_radius < 0:
        raise ValueError("deformation_radius must be >= 0")
    if deformation_radius >= completed_defect_spectral_uniform_radius_lower_bound():
        raise ValueError("deformation_radius must be < 6 for a uniform compact-disk tail bound")
    if deformation_radius == 0:
        return 0.0
    base = float(max(prime_limit, 6))
    linear_tail = 2 * deformation_radius / base
    ratio = deformation_radius / base
    odd_tail = (deformation_radius**3) / (3 * (1 - ratio**2) * (base**2))
    return linear_tail + odd_tail


def completed_defect_spectral_relative_error_bound(prime_limit: int, deformation_radius: float) -> float:
    """Relative multiplicative error bound for the finite-cutoff spectral L-approximant on |λ| <= ρ."""
    return math.expm1(completed_defect_spectral_log_compact_tail_bound(prime_limit, deformation_radius))


def completed_defect_spectral_global_limit_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Profile finite-cutoff approximants to the standalone infinite-cutoff spectral L-object.

    Each row reports the finite-cutoff value together with a certified log-tail bound and the
    induced relative multiplicative error bound for the true infinite-cutoff object.
    """
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    uniform_radius = completed_defect_spectral_uniform_radius_lower_bound()
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            previous_log = None
            deformation_radius = abs(deformation)
            for prime_limit in prime_limits:
                value = completed_defect_spectral_L_function(prime_limit, s, deformation=deformation)
                log_value = completed_defect_spectral_log(prime_limit, s, deformation=deformation)
                tail_bound = completed_defect_spectral_log_compact_tail_bound(prime_limit, deformation_radius)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "value_real": value.real,
                        "value_imag": value.imag,
                        "log_real": log_value.real,
                        "log_imag": log_value.imag,
                        "action_real": -log_value.real,
                        "action_imag": -log_value.imag,
                        "abs_jump_from_previous_log": abs(log_value - previous_log) if previous_log is not None else None,
                        "uniform_radius_lower_bound": uniform_radius,
                        "log_tail_bound": tail_bound,
                        "relative_value_error_bound": completed_defect_spectral_relative_error_bound(prime_limit, deformation_radius),
                        "abs_reciprocity_error": abs(completed_defect_spectral_reciprocity(prime_limit, s, deformation=deformation) - 1.0),
                    }
                )
                previous_log = log_value
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_real_local_coordinates(split_prime: int, s: float) -> dict[str, float]:
    """Positive real-slice coordinates for the completed spectral packet on s > 0."""
    p = split_prime
    if not is_prime(p) or p % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    z = float(prime_weight(p, s).real)
    y = 1.0 - z
    a = y / (p - 1)
    kernel = 1 / (p - 1) + math.log(1 - 1 / p)
    return {
        "p": float(p),
        "z": z,
        "y": y,
        "a": a,
        "kernel": kernel,
        "log_counterterm_strength": -math.log(1 - 1 / p),
    }


def completed_defect_spectral_local_order_parameter_real(split_prime: int, s: float, deformation: float = 1.0) -> float:
    """Local order parameter of the real-slice spectral action F = -log Λ."""
    coords = completed_defect_spectral_real_local_coordinates(split_prime, s)
    a = coords["a"]
    if abs(deformation) >= 1 / a:
        raise ValueError("deformation lies outside the local analytic domain")
    y = coords["y"]
    kernel = coords["kernel"]
    geometric = (deformation**2) * (a**2) / ((int(coords["p"]) - 1) * (1 - (deformation * a) ** 2))
    return 2 * y * (kernel + geometric)


def completed_defect_spectral_local_hessian_real(split_prime: int, s: float, deformation: float = 1.0) -> float:
    """Local Hessian / susceptibility of the real-slice spectral action."""
    coords = completed_defect_spectral_real_local_coordinates(split_prime, s)
    a = coords["a"]
    if abs(deformation) >= 1 / a:
        raise ValueError("deformation lies outside the local analytic domain")
    return 4 * deformation * (a**3) / ((1 - (deformation * a) ** 2) ** 2)


def completed_defect_spectral_order_parameter_tail_bound(prime_limit: int, deformation_radius: float) -> float:
    """Certified compact-disk tail bound for the infinite-cutoff order parameter."""
    if prime_limit < 1:
        raise ValueError("prime_limit must be >= 1")
    if deformation_radius < 0:
        raise ValueError("deformation_radius must be >= 0")
    if deformation_radius >= completed_defect_spectral_uniform_radius_lower_bound():
        raise ValueError("deformation_radius must be < 6 for a uniform compact-disk tail bound")
    x = float(max(prime_limit, 6))
    return 2 / x + (deformation_radius**2) / ((1 - (deformation_radius / x) ** 2) * (x**2))


def completed_defect_spectral_hessian_tail_bound(prime_limit: int, deformation_radius: float) -> float:
    """Certified compact-disk tail bound for the infinite-cutoff Hessian on the real slice."""
    if prime_limit < 1:
        raise ValueError("prime_limit must be >= 1")
    if deformation_radius < 0:
        raise ValueError("deformation_radius must be >= 0")
    if deformation_radius >= completed_defect_spectral_uniform_radius_lower_bound():
        raise ValueError("deformation_radius must be < 6 for a uniform compact-disk tail bound")
    x = float(max(prime_limit, 6))
    if deformation_radius == 0:
        return 0.0
    return (2 * deformation_radius) / (((1 - (deformation_radius / x) ** 2) ** 2) * (x**2))


def completed_defect_spectral_phase_geometry_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, list[dict[str, object]]]]:
    """Profile the monotone order parameter / convex Hessian geometry of the real-slice spectral action."""
    payload: dict[str, dict[str, list[dict[str, object]]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            previous_order = None
            previous_hessian = None
            for prime_limit in prime_limits:
                order_parameter = completed_defect_spectral_order_parameter(prime_limit, s, deformation=deformation)
                hessian = completed_defect_spectral_hessian(prime_limit, s, deformation=deformation)
                action = completed_defect_spectral_action(prime_limit, s, deformation=deformation)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "action_real": action.real,
                        "order_parameter_real": order_parameter.real,
                        "hessian_real": hessian.real,
                        "order_tail_bound": completed_defect_spectral_order_parameter_tail_bound(prime_limit, abs(deformation)),
                        "hessian_tail_bound": completed_defect_spectral_hessian_tail_bound(prime_limit, abs(deformation)),
                        "order_positive": order_parameter.real > 0 if deformation >= 0 else order_parameter.real < 0,
                        "hessian_positive": hessian.real > 0 if deformation > 0 else abs(hessian.real) < 1e-18,
                        "order_jump_from_previous": (order_parameter.real - previous_order) if previous_order is not None else None,
                        "hessian_jump_from_previous": (hessian.real - previous_hessian) if previous_hessian is not None else None,
                    }
                )
                previous_order = order_parameter.real
                previous_hessian = hessian.real
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_order_parameter_real_global(prime_limit: int, s: float, deformation: float = 1.0) -> float:
    """Real order parameter M_X(s;λ) on the positive real spectral slice."""
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    value = completed_defect_spectral_order_parameter(prime_limit, s, deformation=deformation)
    return float(value.real)


def completed_defect_spectral_hessian_real_global(prime_limit: int, s: float, deformation: float = 1.0) -> float:
    """Real Hessian χ_X(s;λ) on the positive real spectral slice."""
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    value = completed_defect_spectral_hessian(prime_limit, s, deformation=deformation)
    return float(value.real)


def completed_defect_spectral_equation_of_state_inverse(
    prime_limit: int,
    s: float,
    target_order_parameter: float,
    deformation_max: float = 5.9,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> float:
    """Invert λ ↦ M_X(s;λ) on the real physical branch by monotone bisection."""
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    if deformation_max <= 0 or deformation_max >= completed_defect_spectral_uniform_radius_lower_bound():
        raise ValueError("deformation_max must satisfy 0 < deformation_max < 6")
    if tolerance <= 0:
        raise ValueError("tolerance must be > 0")
    lower = 0.0
    upper = deformation_max
    lower_value = completed_defect_spectral_order_parameter_real_global(prime_limit, s, lower)
    upper_value = completed_defect_spectral_order_parameter_real_global(prime_limit, s, upper)
    if not (lower_value <= target_order_parameter <= upper_value):
        raise ValueError("target_order_parameter must lie in the monotone branch range [M(0), M(deformation_max)]")
    for _ in range(max_iterations):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = completed_defect_spectral_order_parameter_real_global(prime_limit, s, midpoint)
        if abs(midpoint_value - target_order_parameter) <= tolerance:
            return midpoint
        if midpoint_value < target_order_parameter:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def completed_defect_spectral_legendre_dual(
    prime_limit: int,
    s: float,
    target_order_parameter: float,
    deformation_max: float = 5.9,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> dict[str, float]:
    """Finite-cutoff Legendre dual of the completed spectral action on the monotone branch."""
    deformation = completed_defect_spectral_equation_of_state_inverse(
        prime_limit,
        s,
        target_order_parameter,
        deformation_max=deformation_max,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )
    action = completed_defect_spectral_action(prime_limit, s, deformation=deformation).real
    hessian = completed_defect_spectral_hessian_real_global(prime_limit, s, deformation=deformation)
    dual = deformation * target_order_parameter - action
    return {
        "deformation": deformation,
        "action": action,
        "order_parameter": target_order_parameter,
        "hessian": hessian,
        "dual": dual,
    }


def completed_defect_spectral_equation_of_state_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, list[dict[str, float | int]]]]:
    """Profile the invertible equation of state and Legendre dual branch."""
    payload: dict[str, dict[str, list[dict[str, float | int]]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            for prime_limit in prime_limits:
                target_order = completed_defect_spectral_order_parameter_real_global(prime_limit, s, deformation=deformation)
                dual_packet = completed_defect_spectral_legendre_dual(prime_limit, s, target_order)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "target_deformation": deformation,
                        "target_order_parameter": target_order,
                        "recovered_deformation": dual_packet["deformation"],
                        "abs_inverse_error": abs(dual_packet["deformation"] - deformation),
                        "action": dual_packet["action"],
                        "dual": dual_packet["dual"],
                        "hessian": dual_packet["hessian"],
                    }
                )
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_infinite_equation_of_state_interval(
    prime_limit: int,
    s: float,
    target_order_parameter: float,
    deformation_max: float = 5.9,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> dict[str, float]:
    """Certified enclosure for the infinite-cutoff inverse branch λ_∞(s;M).

    If T_X is the order-parameter tail bound on [0, deformation_max], then

        M_X(λ) <= M_∞(λ) <= M_X(λ) + T_X

    and monotonicity yields the inverse enclosure

        λ_X(max(M - T_X, M_X(0))) <= λ_∞(M) <= λ_X(M)

    whenever the targets lie in the finite-cutoff branch range.
    """
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    if deformation_max <= 0 or deformation_max >= completed_defect_spectral_uniform_radius_lower_bound():
        raise ValueError("deformation_max must satisfy 0 < deformation_max < 6")
    lower_branch_value = completed_defect_spectral_order_parameter_real_global(prime_limit, s, 0.0)
    upper_branch_value = completed_defect_spectral_order_parameter_real_global(prime_limit, s, deformation_max)
    tail = completed_defect_spectral_order_parameter_tail_bound(prime_limit, deformation_max)
    if target_order_parameter < lower_branch_value or target_order_parameter > upper_branch_value + tail:
        raise ValueError("target_order_parameter must lie in the certified infinite-cutoff branch range")
    upper_target = min(target_order_parameter, upper_branch_value)
    lower_target = max(target_order_parameter - tail, lower_branch_value)
    upper_lambda = completed_defect_spectral_equation_of_state_inverse(
        prime_limit,
        s,
        upper_target,
        deformation_max=deformation_max,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )
    lower_lambda = completed_defect_spectral_equation_of_state_inverse(
        prime_limit,
        s,
        lower_target,
        deformation_max=deformation_max,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )
    return {
        "lower_lambda": lower_lambda,
        "upper_lambda": upper_lambda,
        "interval_width": upper_lambda - lower_lambda,
        "tail_bound": tail,
    }


def completed_defect_spectral_infinite_dual_branch_profile(
    reference_prime_limit: int,
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, dict[str, object]]]:
    """Profile monotone finite-cutoff inverse branches converging to the infinite-cutoff dual branch.

    Targets are fixed from the reference cutoff so that all later cutoffs lie on the same common branch.
    """
    payload: dict[str, dict[str, dict[str, object]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            target_order = completed_defect_spectral_order_parameter_real_global(reference_prime_limit, s, deformation=deformation)
            rows = []
            previous_lambda = None
            previous_dual = None
            for prime_limit in prime_limits:
                recovered = completed_defect_spectral_equation_of_state_inverse(prime_limit, s, target_order)
                dual_packet = completed_defect_spectral_legendre_dual(prime_limit, s, target_order)
                interval = completed_defect_spectral_infinite_equation_of_state_interval(prime_limit, s, target_order)
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "target_order_parameter": target_order,
                        "reference_deformation": deformation,
                        "recovered_lambda": recovered,
                        "abs_reference_gap": deformation - recovered,
                        "lambda_drop_from_previous": (previous_lambda - recovered) if previous_lambda is not None else None,
                        "dual": dual_packet["dual"],
                        "dual_drop_from_previous": (previous_dual - dual_packet["dual"]) if previous_dual is not None else None,
                        "interval_lower_lambda": interval["lower_lambda"],
                        "interval_upper_lambda": interval["upper_lambda"],
                        "interval_width": interval["interval_width"],
                        "tail_bound": interval["tail_bound"],
                    }
                )
                previous_lambda = recovered
                previous_dual = dual_packet["dual"]
            payload[outer_key][inner_key] = {
                "reference_prime_limit": reference_prime_limit,
                "target_order_parameter": target_order,
                "rows": rows,
            }
    return payload


def completed_defect_spectral_dual_stiffness(
    prime_limit: int,
    s: float,
    target_order_parameter: float,
    deformation_max: float = 5.9,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> dict[str, float]:
    """Finite-cutoff dual curvature packet for the completed spectral action.

    On the monotone real branch the Legendre dual satisfies

        dΓ_X / dM = λ_X,
        d²Γ_X / dM² = dλ_X / dM = 1 / χ_X,

    where χ_X is the Hessian / susceptibility of the primal free energy.
    """
    dual_packet = completed_defect_spectral_legendre_dual(
        prime_limit,
        s,
        target_order_parameter,
        deformation_max=deformation_max,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )
    hessian = dual_packet["hessian"]
    stiffness = math.inf if hessian <= 0 else 1 / hessian
    return {
        "deformation": dual_packet["deformation"],
        "action": dual_packet["action"],
        "order_parameter": dual_packet["order_parameter"],
        "hessian": hessian,
        "dual": dual_packet["dual"],
        "stiffness": stiffness,
    }


def completed_defect_spectral_infinite_dual_stiffness_interval(
    prime_limit: int,
    s: float,
    target_order_parameter: float,
    deformation_max: float = 5.9,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> dict[str, float]:
    """Certified enclosure for the infinite-cutoff dual stiffness Υ∞ = Γ∞'' = dλ∞/dM.

    Combine the MCXII inverse enclosure λ_- <= λ_∞ <= λ_+ with the compact-disk Hessian
    tail bound 0 <= χ_∞ - χ_X <= H_X(ρ) and the monotonicity of χ_X in λ on the physical
    branch. This yields

        χ_X(λ_-) <= χ_∞(λ_∞) <= χ_X(λ_+) + H_X(ρ),

    and therefore the reciprocal-stiffness bracket

        1 / (χ_X(λ_+) + H_X(ρ)) <= Υ_∞ <= 1 / χ_X(λ_-).
    """
    lambda_interval = completed_defect_spectral_infinite_equation_of_state_interval(
        prime_limit,
        s,
        target_order_parameter,
        deformation_max=deformation_max,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )
    lower_lambda = lambda_interval["lower_lambda"]
    upper_lambda = lambda_interval["upper_lambda"]
    hessian_tail = completed_defect_spectral_hessian_tail_bound(prime_limit, deformation_max)
    lower_hessian_bound = completed_defect_spectral_hessian_real_global(prime_limit, s, lower_lambda)
    upper_hessian_bound = completed_defect_spectral_hessian_real_global(prime_limit, s, upper_lambda) + hessian_tail

    lower_stiffness = 0.0 if upper_hessian_bound <= 0 else 1 / upper_hessian_bound
    upper_stiffness = math.inf if lower_hessian_bound <= 0 else 1 / lower_hessian_bound
    stiffness_interval_width = math.inf if math.isinf(upper_stiffness) else upper_stiffness - lower_stiffness

    return {
        "lower_lambda": lower_lambda,
        "upper_lambda": upper_lambda,
        "lambda_interval_width": lambda_interval["interval_width"],
        "order_parameter_tail_bound": lambda_interval["tail_bound"],
        "lower_hessian_bound": lower_hessian_bound,
        "upper_hessian_bound": upper_hessian_bound,
        "hessian_tail_bound": hessian_tail,
        "lower_stiffness": lower_stiffness,
        "upper_stiffness": upper_stiffness,
        "stiffness_interval_width": stiffness_interval_width,
    }


def completed_defect_spectral_infinite_dual_stiffness_profile(
    reference_prime_limit: int,
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, dict[str, object]]]:
    """Profile the reciprocal-susceptibility / dual-stiffness branch toward infinite cutoff."""
    payload: dict[str, dict[str, dict[str, object]]] = {}
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            target_order = completed_defect_spectral_order_parameter_real_global(reference_prime_limit, s, deformation=deformation)
            rows = []
            previous_width = None
            previous_stiffness = None
            for prime_limit in prime_limits:
                dual_packet = completed_defect_spectral_dual_stiffness(
                    prime_limit,
                    s,
                    target_order,
                    deformation_max=deformation,
                )
                interval = completed_defect_spectral_infinite_dual_stiffness_interval(
                    prime_limit,
                    s,
                    target_order,
                    deformation_max=deformation,
                )
                width = interval["stiffness_interval_width"]
                rows.append(
                    {
                        "prime_limit": prime_limit,
                        "reference_deformation": deformation,
                        "target_order_parameter": target_order,
                        "recovered_lambda": dual_packet["deformation"],
                        "recovered_hessian": dual_packet["hessian"],
                        "recovered_stiffness": dual_packet["stiffness"],
                        "dual": dual_packet["dual"],
                        "interval_lower_stiffness": interval["lower_stiffness"],
                        "interval_upper_stiffness": interval["upper_stiffness"],
                        "stiffness_interval_width": width,
                        "lambda_interval_width": interval["lambda_interval_width"],
                        "hessian_tail_bound": interval["hessian_tail_bound"],
                        "stiffness_jump_from_previous": abs(dual_packet["stiffness"] - previous_stiffness) if previous_stiffness is not None else None,
                        "interval_width_drop_from_previous": (previous_width - width) if previous_width is not None and not math.isinf(previous_width) and not math.isinf(width) else None,
                    }
                )
                previous_width = width
                previous_stiffness = dual_packet["stiffness"]
            payload[outer_key][inner_key] = {
                "reference_prime_limit": reference_prime_limit,
                "target_order_parameter": target_order,
                "rows": rows,
            }
    return payload


def completed_defect_spectral_real_packet(prime_limit: int, s: float, deformation: float = 1.0) -> dict[str, float]:
    """Thermodynamic packet of the completed spectral branch on the positive real slice."""
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    action = completed_defect_spectral_action(prime_limit, s, deformation=deformation).real
    order_parameter = completed_defect_spectral_order_parameter_real_global(prime_limit, s, deformation=deformation)
    hessian = completed_defect_spectral_hessian_real_global(prime_limit, s, deformation=deformation)
    stiffness = math.inf if hessian <= 0 else 1 / hessian
    dual = deformation * order_parameter - action
    return {
        "prime_limit": float(prime_limit),
        "s": s,
        "deformation": deformation,
        "action": action,
        "order_parameter": order_parameter,
        "hessian": hessian,
        "stiffness": stiffness,
        "dual": dual,
    }


def completed_defect_spectral_uniform_wall_packet(prime_limit: int, s: float) -> dict[str, float]:
    """Finite wall packet at the uniform deformation scale λ = 6 on the real spectral slice.

    For every finite real s > 0, each local radius is strictly larger than 6, so the completed
    spectral branch extends continuously to the uniform wall scale λ = 6 even though the global
    compact-disk theory only guarantees analyticity on |λ| < 6.
    """
    wall = completed_defect_spectral_uniform_radius_lower_bound()
    packet = completed_defect_spectral_real_packet(prime_limit, s, deformation=wall)
    packet["uniform_wall"] = wall
    return packet


def completed_defect_spectral_uniform_wall_profile(
    prime_limits: list[int],
    s_values: list[float],
    deformations: list[float],
) -> dict[str, dict[str, list[dict[str, float]]]]:
    """Profile the finite real branch as it approaches the uniform wall scale λ = 6."""
    payload: dict[str, dict[str, list[dict[str, float]]]] = {}
    wall = completed_defect_spectral_uniform_radius_lower_bound()
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for deformation in deformations:
            inner_key = str(deformation)
            rows = []
            previous = None
            for prime_limit in prime_limits:
                packet = completed_defect_spectral_real_packet(prime_limit, s, deformation=deformation)
                row = {
                    **packet,
                    "uniform_wall": wall,
                    "wall_gap": wall - deformation,
                    "order_jump_from_previous": (packet["order_parameter"] - previous["order_parameter"]) if previous is not None else None,
                    "hessian_jump_from_previous": (packet["hessian"] - previous["hessian"]) if previous is not None else None,
                    "stiffness_jump_from_previous": (packet["stiffness"] - previous["stiffness"]) if previous is not None else None,
                }
                rows.append(row)
                previous = packet
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_wall_effective_packet(prime_limit: int, s: float) -> dict[str, float]:
    """Exact wall packet together with first-order boundary effective coefficients in ε = 6 - λ."""
    wall_packet = completed_defect_spectral_uniform_wall_packet(prime_limit, s)
    wall = completed_defect_spectral_uniform_radius_lower_bound()
    third = -completed_defect_spectral_log_lambda_derivative(prime_limit, s, 3, deformation=wall).real
    hessian = wall_packet["hessian"]
    stiffness = wall_packet["stiffness"]
    return {
        **wall_packet,
        "third_derivative": third,
        "epsilon_order_slope": hessian,
        "epsilon_hessian_slope": third,
        "epsilon_stiffness_slope": (third / (hessian**2)) if hessian > 0 else math.inf,
        "wall_epsilon": 0.0,
        "wall_stiffness": stiffness,
    }


def completed_defect_spectral_wall_effective_profile(
    prime_limits: list[int],
    s_values: list[float],
    epsilons: list[float],
) -> dict[str, dict[str, list[dict[str, float]]]]:
    """Profile the first-order boundary effective theory around λ = 6 using ε = 6 - λ."""
    payload: dict[str, dict[str, list[dict[str, float]]]] = {}
    wall = completed_defect_spectral_uniform_radius_lower_bound()
    for s in s_values:
        outer_key = str(s)
        payload[outer_key] = {}
        for epsilon in epsilons:
            if epsilon <= 0 or epsilon > wall:
                raise ValueError("epsilons must satisfy 0 < epsilon <= 6")
            inner_key = str(epsilon)
            rows = []
            for prime_limit in prime_limits:
                wall_packet = completed_defect_spectral_wall_effective_packet(prime_limit, s)
                actual = completed_defect_spectral_real_packet(prime_limit, s, deformation=wall - epsilon)
                predicted_order = wall_packet["order_parameter"] - wall_packet["epsilon_order_slope"] * epsilon
                predicted_hessian = wall_packet["hessian"] - wall_packet["epsilon_hessian_slope"] * epsilon
                predicted_stiffness = wall_packet["stiffness"] + wall_packet["epsilon_stiffness_slope"] * epsilon
                rows.append(
                    {
                        "prime_limit": float(prime_limit),
                        "epsilon": epsilon,
                        "deformation": wall - epsilon,
                        "actual_order_parameter": actual["order_parameter"],
                        "predicted_order_parameter": predicted_order,
                        "order_error": abs(actual["order_parameter"] - predicted_order),
                        "actual_hessian": actual["hessian"],
                        "predicted_hessian": predicted_hessian,
                        "hessian_error": abs(actual["hessian"] - predicted_hessian),
                        "actual_stiffness": actual["stiffness"],
                        "predicted_stiffness": predicted_stiffness,
                        "stiffness_error": abs(actual["stiffness"] - predicted_stiffness),
                    }
                )
            payload[outer_key][inner_key] = rows
    return payload


def completed_defect_spectral_dual_softening_density(prime_limit: int, s: float, deformation: float) -> float:
    """Positive density whose λ-integral gives the loss of dual stiffness toward the wall."""
    hessian = completed_defect_spectral_hessian_real_global(prime_limit, s, deformation=deformation)
    if hessian <= 0:
        return math.inf
    third = -completed_defect_spectral_log_lambda_derivative(prime_limit, s, 3, deformation=deformation).real
    return third / (hessian**2)


def completed_defect_spectral_boundary_transfer_packet(
    prime_limit: int,
    s: float,
    interior_deformation: float = 4.0,
    wall_deformation: float = 6.0,
    subintervals: int = 120,
) -> dict[str, float]:
    """Exact interior-to-wall transfer packet between λ = 4 and λ = 6 on the real slice.

    The endpoint differences are exact. Trapezoidal quadratures numerically certify the three transport
    identities

        F(6)-F(4) = ∫_4^6 M(λ) dλ,
        M(6)-M(4) = ∫_4^6 χ(λ) dλ,
        Σ(4)-Σ(6) = ∫_4^6 τ(λ)/χ(λ)^2 dλ.
    """
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    if not (0 <= interior_deformation < wall_deformation):
        raise ValueError("need 0 <= interior_deformation < wall_deformation")
    if subintervals < 2:
        raise ValueError("subintervals must be >= 2")

    interior = completed_defect_spectral_real_packet(prime_limit, s, deformation=interior_deformation)
    wall = completed_defect_spectral_real_packet(prime_limit, s, deformation=wall_deformation)

    def trapz(func):
        step = (wall_deformation - interior_deformation) / subintervals
        total = 0.5 * (func(interior_deformation) + func(wall_deformation))
        for index in range(1, subintervals):
            total += func(interior_deformation + index * step)
        return total * step

    integrated_order = trapz(lambda deformation: completed_defect_spectral_order_parameter_real_global(prime_limit, s, deformation=deformation))
    integrated_hessian = trapz(lambda deformation: completed_defect_spectral_hessian_real_global(prime_limit, s, deformation=deformation))
    integrated_dual_softening = trapz(lambda deformation: completed_defect_spectral_dual_softening_density(prime_limit, s, deformation=deformation))

    delta_action = wall["action"] - interior["action"]
    delta_order = wall["order_parameter"] - interior["order_parameter"]
    delta_stiffness = interior["stiffness"] - wall["stiffness"]
    width = wall_deformation - interior_deformation

    return {
        "prime_limit": float(prime_limit),
        "s": s,
        "interior_deformation": interior_deformation,
        "wall_deformation": wall_deformation,
        "interior_action": interior["action"],
        "wall_action": wall["action"],
        "interior_order_parameter": interior["order_parameter"],
        "wall_order_parameter": wall["order_parameter"],
        "interior_hessian": interior["hessian"],
        "wall_hessian": wall["hessian"],
        "interior_stiffness": interior["stiffness"],
        "wall_stiffness": wall["stiffness"],
        "delta_action": delta_action,
        "delta_order_parameter": delta_order,
        "delta_stiffness": delta_stiffness,
        "integrated_order": integrated_order,
        "integrated_hessian": integrated_hessian,
        "integrated_dual_softening": integrated_dual_softening,
        "action_transfer_error": abs(delta_action - integrated_order),
        "order_transfer_error": abs(delta_order - integrated_hessian),
        "stiffness_transfer_error": abs(delta_stiffness - integrated_dual_softening),
        "average_order_parameter": delta_action / width,
        "average_hessian": delta_order / width,
        "average_dual_softening": delta_stiffness / width,
    }


def completed_defect_spectral_wall_log_tail_bound(prime_limit: int) -> float:
    """Certified wall-log tail bound at the real boundary scale λ = 6 for cutoffs X >= 7.

    Once the finite cutoff has already included the first split prime p = 7, every remaining tail
    prime satisfies p - 1 >= X with X >= 7. Therefore the odd artanh tail is still uniformly
    summable at λ = 6 and the linear kernel keeps its O(p^-2) decay. A coarse explicit majorant is

        |log Λ_∞(6) - log Λ_X(6)|
        <= 12/X + 72 / ((1-(6/X)^2) X^2)

    for X >= 7.
    """
    if prime_limit < 7:
        raise ValueError("prime_limit must be >= 7 for the wall-tail bound at λ = 6")
    x = float(max(prime_limit, 7))
    ratio = 6.0 / x
    return 12.0 / x + 72.0 / ((1.0 - ratio**2) * (x**2))


def completed_defect_spectral_wall_relative_error_bound(prime_limit: int) -> float:
    """Relative multiplicative wall-value error bound induced by the wall-log tail bound."""
    return math.expm1(completed_defect_spectral_wall_log_tail_bound(prime_limit))


def completed_defect_spectral_wall_order_parameter_tail_bound(prime_limit: int) -> float:
    """Certified tail bound for the infinite-cutoff wall order parameter M_∞(s;6)."""
    if prime_limit < 7:
        raise ValueError("prime_limit must be >= 7 for the wall order-parameter tail bound")
    x = float(max(prime_limit, 7))
    ratio = 6.0 / x
    return 2.0 / x + 36.0 / ((1.0 - ratio**2) * (x**2))


def completed_defect_spectral_wall_hessian_tail_bound(prime_limit: int) -> float:
    """Certified tail bound for the infinite-cutoff wall Hessian χ_∞(s;6)."""
    if prime_limit < 7:
        raise ValueError("prime_limit must be >= 7 for the wall Hessian tail bound")
    x = float(max(prime_limit, 7))
    ratio = 6.0 / x
    return 12.0 / (((1.0 - ratio**2) ** 2) * (x**2))


def completed_defect_spectral_infinite_wall_packet(prime_limit: int, s: float) -> dict[str, float]:
    """Finite wall packet together with certified infinite-cutoff enclosures at λ = 6.

    This upgrades the finite wall packet from MCXV to a genuine infinite-cutoff boundary object.
    For X >= 7, the wall action, order parameter, and Hessian converge monotonically from below,
    while the dual stiffness inherits a reciprocal enclosure from the Hessian bracket.
    """
    if prime_limit < 7:
        raise ValueError("prime_limit must be >= 7 for the infinite wall packet")
    wall_packet = completed_defect_spectral_uniform_wall_packet(prime_limit, s)
    action_tail = completed_defect_spectral_wall_log_tail_bound(prime_limit)
    order_tail = completed_defect_spectral_wall_order_parameter_tail_bound(prime_limit)
    hessian_tail = completed_defect_spectral_wall_hessian_tail_bound(prime_limit)
    hessian = wall_packet["hessian"]
    stiffness = wall_packet["stiffness"]
    lower_stiffness = 0.0 if hessian + hessian_tail <= 0 else 1.0 / (hessian + hessian_tail)
    upper_stiffness = math.inf if hessian <= 0 else 1.0 / hessian
    dual_error = 6.0 * order_tail + action_tail
    return {
        **wall_packet,
        "action_tail_bound": action_tail,
        "relative_value_error_bound": completed_defect_spectral_wall_relative_error_bound(prime_limit),
        "order_tail_bound": order_tail,
        "hessian_tail_bound": hessian_tail,
        "lower_infinite_action": wall_packet["action"],
        "upper_infinite_action": wall_packet["action"] + action_tail,
        "lower_infinite_order_parameter": wall_packet["order_parameter"],
        "upper_infinite_order_parameter": wall_packet["order_parameter"] + order_tail,
        "lower_infinite_hessian": hessian,
        "upper_infinite_hessian": hessian + hessian_tail,
        "lower_infinite_stiffness": lower_stiffness,
        "upper_infinite_stiffness": upper_stiffness,
        "stiffness_interval_width": (upper_stiffness - lower_stiffness) if not math.isinf(upper_stiffness) else math.inf,
        "dual_abs_error_bound": dual_error,
        "lower_infinite_dual": wall_packet["dual"] - dual_error,
        "upper_infinite_dual": wall_packet["dual"] + dual_error,
    }


def completed_defect_spectral_infinite_wall_profile(
    prime_limits: list[int],
    s_values: list[float],
) -> dict[str, list[dict[str, float]]]:
    """Profile convergence of the completed wall packet toward its infinite-cutoff boundary object."""
    payload: dict[str, list[dict[str, float]]] = {}
    for s in s_values:
        rows = []
        previous_action = None
        previous_order = None
        previous_hessian = None
        previous_stiffness = None
        previous_width = None
        for prime_limit in prime_limits:
            packet = completed_defect_spectral_infinite_wall_packet(prime_limit, s)
            rows.append(
                {
                    **packet,
                    "prime_limit": float(prime_limit),
                    "action_jump_from_previous": (packet["action"] - previous_action) if previous_action is not None else None,
                    "order_jump_from_previous": (packet["order_parameter"] - previous_order) if previous_order is not None else None,
                    "hessian_jump_from_previous": (packet["hessian"] - previous_hessian) if previous_hessian is not None else None,
                    "stiffness_drop_from_previous": (previous_stiffness - packet["stiffness"]) if previous_stiffness is not None else None,
                    "stiffness_interval_width_drop_from_previous": (previous_width - packet["stiffness_interval_width"]) if previous_width is not None else None,
                }
            )
            previous_action = packet["action"]
            previous_order = packet["order_parameter"]
            previous_hessian = packet["hessian"]
            previous_stiffness = packet["stiffness"]
            previous_width = packet["stiffness_interval_width"]
        payload[str(s)] = rows
    return payload


def completed_defect_spectral_infinite_compact_real_packet(
    prime_limit: int,
    s: float,
    deformation: float,
) -> dict[str, float]:
    """Finite packet with certified infinite-cutoff enclosure on a compact real branch."""
    if abs(deformation) >= completed_defect_spectral_uniform_radius_lower_bound():
        raise ValueError("compact infinite packet requires |deformation| < 6")
    packet = completed_defect_spectral_real_packet(prime_limit, s, deformation=deformation)
    deformation_radius = abs(deformation)
    action_tail = completed_defect_spectral_log_compact_tail_bound(prime_limit, deformation_radius)
    order_tail = completed_defect_spectral_order_parameter_tail_bound(prime_limit, deformation_radius)
    hessian_tail = completed_defect_spectral_hessian_tail_bound(prime_limit, deformation_radius)
    hessian = packet["hessian"]
    lower_stiffness = 0.0 if hessian + hessian_tail <= 0 else 1.0 / (hessian + hessian_tail)
    upper_stiffness = math.inf if hessian <= 0 else 1.0 / hessian
    dual_error = deformation_radius * order_tail + action_tail
    return {
        **packet,
        "action_tail_bound": action_tail,
        "relative_value_error_bound": completed_defect_spectral_relative_error_bound(prime_limit, deformation_radius),
        "order_tail_bound": order_tail,
        "hessian_tail_bound": hessian_tail,
        "lower_infinite_action": packet["action"],
        "upper_infinite_action": packet["action"] + action_tail,
        "lower_infinite_order_parameter": packet["order_parameter"],
        "upper_infinite_order_parameter": packet["order_parameter"] + order_tail,
        "lower_infinite_hessian": hessian,
        "upper_infinite_hessian": hessian + hessian_tail,
        "lower_infinite_stiffness": lower_stiffness,
        "upper_infinite_stiffness": upper_stiffness,
        "stiffness_interval_width": (upper_stiffness - lower_stiffness) if not math.isinf(upper_stiffness) else math.inf,
        "dual_abs_error_bound": dual_error,
        "lower_infinite_dual": packet["dual"] - dual_error,
        "upper_infinite_dual": packet["dual"] + dual_error,
    }


def completed_defect_spectral_infinite_boundary_corridor_packet(
    prime_limit: int,
    s: float,
    interior_deformation: float = 4.0,
    wall_deformation: float = 6.0,
    subintervals: int = 160,
) -> dict[str, float]:
    """Certified infinite-cutoff corridor from a compact interior packet to the wall packet.

    MCXX gives the finite-cutoff transfer across [4, 6]. MCXXI gives the infinite-cutoff wall
    endpoint. This packet combines the compact interior enclosure with the wall enclosure, so the
    true infinite endpoint deltas are trapped between explicit finite-cutoff bounds.
    """
    wall = completed_defect_spectral_uniform_radius_lower_bound()
    if wall_deformation != wall:
        raise ValueError("infinite boundary corridor currently uses the certified wall deformation 6")
    if not (0 <= interior_deformation < wall_deformation):
        raise ValueError("need 0 <= interior_deformation < wall_deformation")

    interior = completed_defect_spectral_infinite_compact_real_packet(prime_limit, s, interior_deformation)
    wall_packet = completed_defect_spectral_infinite_wall_packet(prime_limit, s)
    transfer = completed_defect_spectral_boundary_transfer_packet(
        prime_limit,
        s,
        interior_deformation=interior_deformation,
        wall_deformation=wall_deformation,
        subintervals=subintervals,
    )

    action_lower = wall_packet["lower_infinite_action"] - interior["upper_infinite_action"]
    action_upper = wall_packet["upper_infinite_action"] - interior["lower_infinite_action"]
    order_lower = wall_packet["lower_infinite_order_parameter"] - interior["upper_infinite_order_parameter"]
    order_upper = wall_packet["upper_infinite_order_parameter"] - interior["lower_infinite_order_parameter"]
    hessian_lower = wall_packet["lower_infinite_hessian"] - interior["upper_infinite_hessian"]
    hessian_upper = wall_packet["upper_infinite_hessian"] - interior["lower_infinite_hessian"]
    stiffness_lower = interior["lower_infinite_stiffness"] - wall_packet["upper_infinite_stiffness"]
    stiffness_upper = interior["upper_infinite_stiffness"] - wall_packet["lower_infinite_stiffness"]
    dual_lower = wall_packet["lower_infinite_dual"] - interior["upper_infinite_dual"]
    dual_upper = wall_packet["upper_infinite_dual"] - interior["lower_infinite_dual"]

    return {
        "prime_limit": float(prime_limit),
        "s": s,
        "interior_deformation": interior_deformation,
        "wall_deformation": wall_deformation,
        "interior_action_tail_bound": interior["action_tail_bound"],
        "wall_action_tail_bound": wall_packet["action_tail_bound"],
        "interior_order_tail_bound": interior["order_tail_bound"],
        "wall_order_tail_bound": wall_packet["order_tail_bound"],
        "interior_hessian_tail_bound": interior["hessian_tail_bound"],
        "wall_hessian_tail_bound": wall_packet["hessian_tail_bound"],
        "finite_delta_action": transfer["delta_action"],
        "finite_delta_order_parameter": transfer["delta_order_parameter"],
        "finite_delta_hessian": transfer["wall_hessian"] - transfer["interior_hessian"],
        "finite_stiffness_loss": transfer["delta_stiffness"],
        "finite_dual_delta": wall_packet["dual"] - interior["dual"],
        "integrated_order": transfer["integrated_order"],
        "integrated_hessian": transfer["integrated_hessian"],
        "integrated_dual_softening": transfer["integrated_dual_softening"],
        "action_transfer_error": transfer["action_transfer_error"],
        "order_transfer_error": transfer["order_transfer_error"],
        "stiffness_transfer_error": transfer["stiffness_transfer_error"],
        "infinite_delta_action_lower_bound": action_lower,
        "infinite_delta_action_upper_bound": action_upper,
        "infinite_delta_action_interval_width": action_upper - action_lower,
        "infinite_delta_order_parameter_lower_bound": order_lower,
        "infinite_delta_order_parameter_upper_bound": order_upper,
        "infinite_delta_order_parameter_interval_width": order_upper - order_lower,
        "infinite_delta_hessian_lower_bound": hessian_lower,
        "infinite_delta_hessian_upper_bound": hessian_upper,
        "infinite_delta_hessian_interval_width": hessian_upper - hessian_lower,
        "infinite_stiffness_loss_lower_bound": stiffness_lower,
        "infinite_stiffness_loss_upper_bound": stiffness_upper,
        "infinite_stiffness_loss_interval_width": stiffness_upper - stiffness_lower,
        "infinite_dual_delta_lower_bound": dual_lower,
        "infinite_dual_delta_upper_bound": dual_upper,
        "infinite_dual_delta_interval_width": dual_upper - dual_lower,
        "finite_delta_action_in_corridor": action_lower <= transfer["delta_action"] <= action_upper,
        "finite_delta_order_parameter_in_corridor": order_lower <= transfer["delta_order_parameter"] <= order_upper,
        "finite_delta_hessian_in_corridor": hessian_lower <= transfer["wall_hessian"] - transfer["interior_hessian"] <= hessian_upper,
        "finite_stiffness_loss_in_corridor": stiffness_lower <= transfer["delta_stiffness"] <= stiffness_upper,
        "finite_dual_delta_in_corridor": dual_lower <= wall_packet["dual"] - interior["dual"] <= dual_upper,
    }


def completed_defect_spectral_infinite_boundary_corridor_profile(
    prime_limits: list[int],
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, list[dict[str, float]]]:
    """Profile the contraction of the infinite-cutoff interior-to-wall corridor."""
    payload: dict[str, list[dict[str, float]]] = {}
    for s in s_values:
        rows = []
        previous_action_width = None
        previous_order_width = None
        previous_hessian_width = None
        previous_stiffness_width = None
        previous_dual_width = None
        for prime_limit in prime_limits:
            packet = completed_defect_spectral_infinite_boundary_corridor_packet(prime_limit, s, subintervals=subintervals)
            rows.append(
                {
                    **packet,
                    "action_corridor_width_drop_from_previous": (
                        previous_action_width - packet["infinite_delta_action_interval_width"]
                        if previous_action_width is not None
                        else None
                    ),
                    "order_corridor_width_drop_from_previous": (
                        previous_order_width - packet["infinite_delta_order_parameter_interval_width"]
                        if previous_order_width is not None
                        else None
                    ),
                    "hessian_corridor_width_drop_from_previous": (
                        previous_hessian_width - packet["infinite_delta_hessian_interval_width"]
                        if previous_hessian_width is not None
                        else None
                    ),
                    "stiffness_corridor_width_drop_from_previous": (
                        previous_stiffness_width - packet["infinite_stiffness_loss_interval_width"]
                        if previous_stiffness_width is not None
                        else None
                    ),
                    "dual_corridor_width_drop_from_previous": (
                        previous_dual_width - packet["infinite_dual_delta_interval_width"]
                        if previous_dual_width is not None
                        else None
                    ),
                }
            )
            previous_action_width = packet["infinite_delta_action_interval_width"]
            previous_order_width = packet["infinite_delta_order_parameter_interval_width"]
            previous_hessian_width = packet["infinite_delta_hessian_interval_width"]
            previous_stiffness_width = packet["infinite_stiffness_loss_interval_width"]
            previous_dual_width = packet["infinite_dual_delta_interval_width"]
        payload[str(s)] = rows
    return payload


def completed_defect_spectral_infinite_boundary_average_packet(
    prime_limit: int,
    s: float,
    interior_deformation: float = 4.0,
    wall_deformation: float = 6.0,
    subintervals: int = 160,
) -> dict[str, float]:
    """Average-density version of the certified infinite-cutoff boundary corridor."""
    corridor = completed_defect_spectral_infinite_boundary_corridor_packet(
        prime_limit,
        s,
        interior_deformation=interior_deformation,
        wall_deformation=wall_deformation,
        subintervals=subintervals,
    )
    width = wall_deformation - interior_deformation
    if width <= 0:
        raise ValueError("corridor width must be positive")

    def scaled_interval(input_prefix: str, output_prefix: str) -> dict[str, float]:
        lower = corridor[f"{input_prefix}_lower_bound"] / width
        upper = corridor[f"{input_prefix}_upper_bound"] / width
        return {
            f"{output_prefix}_lower_bound": lower,
            f"{output_prefix}_upper_bound": upper,
            f"{output_prefix}_interval_width": upper - lower,
        }

    order_average = scaled_interval("infinite_delta_action", "infinite_average_order_parameter")
    hessian_average = scaled_interval("infinite_delta_order_parameter", "infinite_average_hessian")
    third_average = scaled_interval("infinite_delta_hessian", "infinite_average_third_derivative")
    softening_average = scaled_interval("infinite_stiffness_loss", "infinite_average_dual_softening")
    dual_average = scaled_interval("infinite_dual_delta", "infinite_average_dual_delta_density")

    finite_average_order = corridor["finite_delta_action"] / width
    finite_average_hessian = corridor["finite_delta_order_parameter"] / width
    finite_average_third_derivative = corridor["finite_delta_hessian"] / width
    finite_average_dual_softening = corridor["finite_stiffness_loss"] / width
    finite_average_dual_delta_density = corridor["finite_dual_delta"] / width

    return {
        **corridor,
        "corridor_width": width,
        "finite_average_order_parameter": finite_average_order,
        "finite_average_hessian": finite_average_hessian,
        "finite_average_third_derivative": finite_average_third_derivative,
        "finite_average_dual_softening": finite_average_dual_softening,
        "finite_average_dual_delta_density": finite_average_dual_delta_density,
        **order_average,
        **hessian_average,
        **third_average,
        **softening_average,
        **dual_average,
        "finite_average_order_parameter_in_corridor": (
            order_average["infinite_average_order_parameter_lower_bound"]
            <= finite_average_order
            <= order_average["infinite_average_order_parameter_upper_bound"]
        ),
        "finite_average_hessian_in_corridor": (
            hessian_average["infinite_average_hessian_lower_bound"]
            <= finite_average_hessian
            <= hessian_average["infinite_average_hessian_upper_bound"]
        ),
        "finite_average_third_derivative_in_corridor": (
            third_average["infinite_average_third_derivative_lower_bound"]
            <= finite_average_third_derivative
            <= third_average["infinite_average_third_derivative_upper_bound"]
        ),
        "finite_average_dual_softening_in_corridor": (
            softening_average["infinite_average_dual_softening_lower_bound"]
            <= finite_average_dual_softening
            <= softening_average["infinite_average_dual_softening_upper_bound"]
        ),
        "finite_average_dual_delta_density_in_corridor": (
            dual_average["infinite_average_dual_delta_density_lower_bound"]
            <= finite_average_dual_delta_density
            <= dual_average["infinite_average_dual_delta_density_upper_bound"]
        ),
    }


def completed_defect_spectral_infinite_boundary_average_profile(
    prime_limits: list[int],
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, list[dict[str, float]]]:
    """Profile contraction of average density intervals across the zero-sheet corridor."""
    payload: dict[str, list[dict[str, float]]] = {}
    for s in s_values:
        rows = []
        previous_order_width = None
        previous_hessian_width = None
        previous_third_width = None
        previous_softening_width = None
        previous_dual_width = None
        for prime_limit in prime_limits:
            packet = completed_defect_spectral_infinite_boundary_average_packet(
                prime_limit,
                s,
                subintervals=subintervals,
            )
            rows.append(
                {
                    **packet,
                    "average_order_width_drop_from_previous": (
                        previous_order_width - packet["infinite_average_order_parameter_interval_width"]
                        if previous_order_width is not None
                        else None
                    ),
                    "average_hessian_width_drop_from_previous": (
                        previous_hessian_width - packet["infinite_average_hessian_interval_width"]
                        if previous_hessian_width is not None
                        else None
                    ),
                    "average_third_derivative_width_drop_from_previous": (
                        previous_third_width - packet["infinite_average_third_derivative_interval_width"]
                        if previous_third_width is not None
                        else None
                    ),
                    "average_dual_softening_width_drop_from_previous": (
                        previous_softening_width - packet["infinite_average_dual_softening_interval_width"]
                        if previous_softening_width is not None
                        else None
                    ),
                    "average_dual_delta_width_drop_from_previous": (
                        previous_dual_width - packet["infinite_average_dual_delta_density_interval_width"]
                        if previous_dual_width is not None
                        else None
                    ),
                }
            )
            previous_order_width = packet["infinite_average_order_parameter_interval_width"]
            previous_hessian_width = packet["infinite_average_hessian_interval_width"]
            previous_third_width = packet["infinite_average_third_derivative_interval_width"]
            previous_softening_width = packet["infinite_average_dual_softening_interval_width"]
            previous_dual_width = packet["infinite_average_dual_delta_density_interval_width"]
        payload[str(s)] = rows
    return payload


def completed_defect_spectral_third_derivative_real_global(prime_limit: int, s: float, deformation: float = 1.0) -> float:
    """Real third λ-derivative of the completed spectral action on the positive real branch."""
    if s <= 0:
        raise ValueError("s must be > 0 on the real spectral slice")
    return float(-completed_defect_spectral_log_lambda_derivative(prime_limit, s, 3, deformation=deformation).real)


def _completed_defect_spectral_endpoint_bracket_witness(
    target: float,
    lower_deformation: float,
    upper_deformation: float,
    value_at_deformation,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> dict[str, float]:
    """Select a deformation witness by endpoint-bracket bisection."""
    if not lower_deformation < upper_deformation:
        raise ValueError("need lower_deformation < upper_deformation")
    lower_residual = value_at_deformation(lower_deformation) - target
    upper_residual = value_at_deformation(upper_deformation) - target
    if abs(lower_residual) <= tolerance:
        deformation = lower_deformation
    elif abs(upper_residual) <= tolerance:
        deformation = upper_deformation
    elif lower_residual * upper_residual > 0:
        raise ValueError("target is not bracketed by endpoint values")
    else:
        low = lower_deformation
        high = upper_deformation
        low_residual = lower_residual
        deformation = 0.5 * (low + high)
        for _ in range(max_iterations):
            deformation = 0.5 * (low + high)
            residual = value_at_deformation(deformation) - target
            if abs(residual) <= tolerance:
                break
            if low_residual * residual <= 0:
                high = deformation
            else:
                low = deformation
                low_residual = residual
    value = value_at_deformation(deformation)
    return {
        "deformation": deformation,
        "value": value,
        "target": target,
        "abs_residual": abs(value - target),
    }


def completed_defect_spectral_boundary_mean_witness_packet(
    prime_limit: int,
    s: float,
    interior_deformation: float = 4.0,
    wall_deformation: float = 6.0,
    subintervals: int = 160,
) -> dict[str, float]:
    """Mean-density deformation witnesses inside the zero-sheet corridor [4, 6]."""
    average = completed_defect_spectral_infinite_boundary_average_packet(
        prime_limit,
        s,
        interior_deformation=interior_deformation,
        wall_deformation=wall_deformation,
        subintervals=subintervals,
    )

    order_witness = _completed_defect_spectral_endpoint_bracket_witness(
        average["finite_average_order_parameter"],
        interior_deformation,
        wall_deformation,
        lambda deformation: completed_defect_spectral_order_parameter_real_global(prime_limit, s, deformation=deformation),
    )
    hessian_witness = _completed_defect_spectral_endpoint_bracket_witness(
        average["finite_average_hessian"],
        interior_deformation,
        wall_deformation,
        lambda deformation: completed_defect_spectral_hessian_real_global(prime_limit, s, deformation=deformation),
    )
    third_witness = _completed_defect_spectral_endpoint_bracket_witness(
        average["finite_average_third_derivative"],
        interior_deformation,
        wall_deformation,
        lambda deformation: completed_defect_spectral_third_derivative_real_global(prime_limit, s, deformation=deformation),
    )
    dual_softening_witness = _completed_defect_spectral_endpoint_bracket_witness(
        average["finite_average_dual_softening"],
        interior_deformation,
        wall_deformation,
        lambda deformation: completed_defect_spectral_dual_softening_density(prime_limit, s, deformation=deformation),
    )

    return {
        **average,
        "order_mean_deformation": order_witness["deformation"],
        "order_mean_value": order_witness["value"],
        "order_mean_abs_residual": order_witness["abs_residual"],
        "hessian_mean_deformation": hessian_witness["deformation"],
        "hessian_mean_value": hessian_witness["value"],
        "hessian_mean_abs_residual": hessian_witness["abs_residual"],
        "third_derivative_mean_deformation": third_witness["deformation"],
        "third_derivative_mean_value": third_witness["value"],
        "third_derivative_mean_abs_residual": third_witness["abs_residual"],
        "dual_softening_mean_deformation": dual_softening_witness["deformation"],
        "dual_softening_mean_value": dual_softening_witness["value"],
        "dual_softening_mean_abs_residual": dual_softening_witness["abs_residual"],
        "mean_deformation_ladder_ordered": (
            interior_deformation
            < dual_softening_witness["deformation"]
            < order_witness["deformation"]
            < hessian_witness["deformation"]
            < third_witness["deformation"]
            < wall_deformation
        ),
        "primal_mean_deformation_ladder_ordered": (
            interior_deformation
            < order_witness["deformation"]
            < hessian_witness["deformation"]
            < third_witness["deformation"]
            < wall_deformation
        ),
    }


def completed_defect_spectral_boundary_mean_witness_profile(
    prime_limits: list[int],
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, list[dict[str, float]]]:
    """Profile the finite mean-density witnesses selected inside the zero-sheet corridor."""
    payload: dict[str, list[dict[str, float]]] = {}
    for s in s_values:
        rows = []
        previous_order = None
        previous_hessian = None
        previous_third = None
        previous_softening = None
        for prime_limit in prime_limits:
            packet = completed_defect_spectral_boundary_mean_witness_packet(
                prime_limit,
                s,
                subintervals=subintervals,
            )
            rows.append(
                {
                    **packet,
                    "order_mean_deformation_jump_from_previous": (
                        abs(packet["order_mean_deformation"] - previous_order) if previous_order is not None else None
                    ),
                    "hessian_mean_deformation_jump_from_previous": (
                        abs(packet["hessian_mean_deformation"] - previous_hessian) if previous_hessian is not None else None
                    ),
                    "third_derivative_mean_deformation_jump_from_previous": (
                        abs(packet["third_derivative_mean_deformation"] - previous_third) if previous_third is not None else None
                    ),
                    "dual_softening_mean_deformation_jump_from_previous": (
                        abs(packet["dual_softening_mean_deformation"] - previous_softening) if previous_softening is not None else None
                    ),
                }
            )
            previous_order = packet["order_mean_deformation"]
            previous_hessian = packet["hessian_mean_deformation"]
            previous_third = packet["third_derivative_mean_deformation"]
            previous_softening = packet["dual_softening_mean_deformation"]
        payload[str(s)] = rows
    return payload


def completed_defect_spectral_boundary_barycentric_witness_packet(
    prime_limit: int,
    s: float,
    interior_deformation: float = 4.0,
    wall_deformation: float = 6.0,
    subintervals: int = 160,
) -> dict[str, float]:
    """Barycentric coordinates of the mean-density witnesses on the zero-sheet corridor."""
    witness = completed_defect_spectral_boundary_mean_witness_packet(
        prime_limit,
        s,
        interior_deformation=interior_deformation,
        wall_deformation=wall_deformation,
        subintervals=subintervals,
    )
    width = wall_deformation - interior_deformation
    if width <= 0:
        raise ValueError("corridor width must be positive")

    soft = (witness["dual_softening_mean_deformation"] - interior_deformation) / width
    order = (witness["order_mean_deformation"] - interior_deformation) / width
    hessian = (witness["hessian_mean_deformation"] - interior_deformation) / width
    third = (witness["third_derivative_mean_deformation"] - interior_deformation) / width
    gaps = {
        "interior_to_softening_barycentric_gap": soft,
        "softening_to_order_barycentric_gap": order - soft,
        "order_to_hessian_barycentric_gap": hessian - order,
        "hessian_to_third_derivative_barycentric_gap": third - hessian,
        "third_derivative_to_wall_barycentric_gap": 1.0 - third,
    }

    return {
        **witness,
        "dual_softening_barycentric_coordinate": soft,
        "order_barycentric_coordinate": order,
        "hessian_barycentric_coordinate": hessian,
        "third_derivative_barycentric_coordinate": third,
        **gaps,
        "barycentric_gap_sum": sum(gaps.values()),
        "barycentric_ladder_ordered": 0.0 < soft < order < hessian < third < 1.0,
        "primal_barycentric_ladder_ordered": 0.0 < order < hessian < third < 1.0,
    }


def completed_defect_spectral_boundary_barycentric_witness_profile(
    prime_limits: list[int],
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, list[dict[str, float]]]:
    """Profile barycentric stabilization of the mean-density witness ladder."""
    payload: dict[str, list[dict[str, float]]] = {}
    for s in s_values:
        rows = []
        previous_soft = None
        previous_order = None
        previous_hessian = None
        previous_third = None
        for prime_limit in prime_limits:
            packet = completed_defect_spectral_boundary_barycentric_witness_packet(
                prime_limit,
                s,
                subintervals=subintervals,
            )
            rows.append(
                {
                    **packet,
                    "dual_softening_barycentric_jump_from_previous": (
                        abs(packet["dual_softening_barycentric_coordinate"] - previous_soft) if previous_soft is not None else None
                    ),
                    "order_barycentric_jump_from_previous": (
                        abs(packet["order_barycentric_coordinate"] - previous_order) if previous_order is not None else None
                    ),
                    "hessian_barycentric_jump_from_previous": (
                        abs(packet["hessian_barycentric_coordinate"] - previous_hessian) if previous_hessian is not None else None
                    ),
                    "third_derivative_barycentric_jump_from_previous": (
                        abs(packet["third_derivative_barycentric_coordinate"] - previous_third) if previous_third is not None else None
                    ),
                }
            )
            previous_soft = packet["dual_softening_barycentric_coordinate"]
            previous_order = packet["order_barycentric_coordinate"]
            previous_hessian = packet["hessian_barycentric_coordinate"]
            previous_third = packet["third_derivative_barycentric_coordinate"]
        payload[str(s)] = rows
    return payload


def completed_defect_spectral_boundary_barycentric_stability_packet(
    prime_limits: list[int],
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, object]:
    """Finite stability signature for barycentric witness coordinates."""
    if len(prime_limits) < 3:
        raise ValueError("need at least three prime limits to measure two cutoff jumps")
    if len(s_values) < 1:
        raise ValueError("need at least one s-value")
    profile = completed_defect_spectral_boundary_barycentric_witness_profile(
        prime_limits,
        s_values,
        subintervals=subintervals,
    )
    coordinate_keys = {
        "dual_softening": "dual_softening_barycentric_coordinate",
        "order": "order_barycentric_coordinate",
        "hessian": "hessian_barycentric_coordinate",
        "third_derivative": "third_derivative_barycentric_coordinate",
    }
    gap_keys = {
        "interior_to_softening": "interior_to_softening_barycentric_gap",
        "softening_to_order": "softening_to_order_barycentric_gap",
        "order_to_hessian": "order_to_hessian_barycentric_gap",
        "hessian_to_third_derivative": "hessian_to_third_derivative_barycentric_gap",
        "third_derivative_to_wall": "third_derivative_to_wall_barycentric_gap",
    }

    per_s: dict[str, object] = {}
    finite_ratios = []
    for s in s_values:
        rows = profile[str(s)]
        first = rows[-3]
        middle = rows[-2]
        final = rows[-1]
        ratios = {}
        for name, key in coordinate_keys.items():
            first_jump = abs(middle[key] - first[key])
            second_jump = abs(final[key] - middle[key])
            ratio = None if second_jump == 0.0 else first_jump / second_jump
            if ratio is not None:
                finite_ratios.append(ratio)
            ratios[name] = {
                "first_jump": first_jump,
                "second_jump": second_jump,
                "contraction_ratio": ratio,
                "second_jump_zero": second_jump == 0.0,
            }
        per_s[str(s)] = {
            "coordinate_jump_ratios": ratios,
            "final_coordinates": {name: final[key] for name, key in coordinate_keys.items()},
            "final_gaps": {name: final[key] for name, key in gap_keys.items()},
            "final_gap_sum": final["barycentric_gap_sum"],
            "barycentric_ladder_ordered": final["barycentric_ladder_ordered"],
            "all_coordinate_contractions_ge_100": all(
                row["second_jump_zero"] or row["contraction_ratio"] >= 100.0 for row in ratios.values()
            ),
        }

    cross_s_shift = None
    if len(s_values) >= 2:
        lower = profile[str(s_values[0])][-1]
        upper = profile[str(s_values[-1])][-1]
        coordinate_offsets = {name: upper[key] - lower[key] for name, key in coordinate_keys.items()}
        gap_offsets = {name: upper[key] - lower[key] for name, key in gap_keys.items()}
        ordered_offsets = [
            coordinate_offsets["dual_softening"],
            coordinate_offsets["order"],
            coordinate_offsets["hessian"],
            coordinate_offsets["third_derivative"],
        ]
        cross_s_shift = {
            "from_s": s_values[0],
            "to_s": s_values[-1],
            "coordinate_offsets": coordinate_offsets,
            "gap_offsets": gap_offsets,
            "all_witnesses_shift_toward_wall": all(value > 0.0 for value in coordinate_offsets.values()),
            "coordinate_offsets_strictly_increase": all(
                ordered_offsets[index] < ordered_offsets[index + 1] for index in range(len(ordered_offsets) - 1)
            ),
            "wall_gap_shrinks": gap_offsets["third_derivative_to_wall"] < 0.0,
            "gap_offset_sum": sum(gap_offsets.values()),
        }

    return {
        "prime_limits": prime_limits,
        "s_values": s_values,
        "profile": profile,
        "per_s": per_s,
        "cross_s_shift": cross_s_shift,
        "minimum_finite_contraction_ratio": min(finite_ratios) if finite_ratios else math.inf,
    }


def completed_defect_spectral_boundary_barycentric_wallward_flow_packet(
    prime_limit: int,
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, object]:
    """Finite wallward-flow packet for barycentric witnesses along an s-ladder.

    The packet tracks how the four barycentric witness coordinates move as s varies on the
    positive real spectral slice, together with the companion wall gap.
    """
    if prime_limit < 1:
        raise ValueError("prime_limit must be >= 1")
    if len(s_values) < 2:
        raise ValueError("need at least two s-values")
    if any(s <= 0 for s in s_values):
        raise ValueError("all s-values must be > 0 on the real spectral slice")
    if any(s_values[index] >= s_values[index + 1] for index in range(len(s_values) - 1)):
        raise ValueError("s_values must be strictly increasing")

    rows: list[dict[str, object]] = []
    previous = None
    for s in s_values:
        packet = completed_defect_spectral_boundary_barycentric_witness_packet(
            prime_limit,
            s,
            subintervals=subintervals,
        )
        coordinate = {
            "dual_softening": packet["dual_softening_barycentric_coordinate"],
            "order": packet["order_barycentric_coordinate"],
            "hessian": packet["hessian_barycentric_coordinate"],
            "third_derivative": packet["third_derivative_barycentric_coordinate"],
        }
        jumps = None
        if previous is not None:
            jumps = {
                name: coordinate[name] - previous["coordinate"][name]
                for name in coordinate
            }
        rows.append(
            {
                **packet,
                "coordinate": coordinate,
                "coordinate_jump_from_previous": jumps,
                "wall_gap_jump_from_previous": (
                    packet["third_derivative_to_wall_barycentric_gap"] - previous["wall_gap"] if previous is not None else None
                ),
            }
        )
        previous = {
            "coordinate": coordinate,
            "wall_gap": packet["third_derivative_to_wall_barycentric_gap"],
        }

    positive_coordinate_jumps = []
    negative_wall_gap_jumps = []
    for row in rows[1:]:
        jumps = row["coordinate_jump_from_previous"]
        assert isinstance(jumps, dict)
        positive_coordinate_jumps.append(all(value > 0.0 for value in jumps.values()))
        wall_jump = row["wall_gap_jump_from_previous"]
        assert isinstance(wall_jump, float)
        negative_wall_gap_jumps.append(wall_jump < 0.0)

    first_row = rows[0]
    last_row = rows[-1]
    midpoint_crossing_rows = [
        index
        for index, row in enumerate(rows)
        if row["dual_softening_barycentric_coordinate"] >= 0.5
    ]
    midpoint_crossing_index = midpoint_crossing_rows[0] if midpoint_crossing_rows else None
    midpoint_crossing_interval = None
    if midpoint_crossing_index is not None and midpoint_crossing_index > 0:
        midpoint_crossing_interval = {
            "left_s": rows[midpoint_crossing_index - 1]["s"],
            "right_s": rows[midpoint_crossing_index]["s"],
        }

    coordinate_offsets = {
        name: last_row["coordinate"][name] - first_row["coordinate"][name]
        for name in first_row["coordinate"]
    }

    return {
        "prime_limit": prime_limit,
        "s_values": s_values,
        "rows": rows,
        "all_coordinate_jumps_positive": all(positive_coordinate_jumps),
        "all_wall_gap_jumps_negative": all(negative_wall_gap_jumps),
        "all_barycentric_ladders_ordered": all(row["barycentric_ladder_ordered"] for row in rows),
        "wall_gap_strictly_decreases": all(negative_wall_gap_jumps),
        "coordinate_offsets": coordinate_offsets,
        "dual_softening_crosses_half": midpoint_crossing_index is not None,
        "dual_softening_midpoint_crossing_index": midpoint_crossing_index,
        "dual_softening_midpoint_crossing_interval": midpoint_crossing_interval,
        "initial_wall_gap": first_row["third_derivative_to_wall_barycentric_gap"],
        "final_wall_gap": last_row["third_derivative_to_wall_barycentric_gap"],
        "wall_gap_drop": first_row["third_derivative_to_wall_barycentric_gap"] - last_row["third_derivative_to_wall_barycentric_gap"],
    }


def completed_defect_spectral_boundary_barycentric_dispersion_turning_packet(
    prime_limit: int,
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, object]:
    """Finite turning-law packet for entropy/concentration of barycentric gap coordinates.

    Entropy is Shannon entropy of the five positive barycentric gaps; concentration is the
    quadratic concentration index \\sum g_i^2. This packet detects the finite turning point
    of dispersion along an s-ladder while retaining the wallward-flow diagnostics.
    """
    flow = completed_defect_spectral_boundary_barycentric_wallward_flow_packet(
        prime_limit,
        s_values,
        subintervals=subintervals,
    )
    rows = flow["rows"]

    decorated_rows: list[dict[str, object]] = []
    previous_entropy = None
    previous_concentration = None
    for row in rows:
        gaps = [
            row["interior_to_softening_barycentric_gap"],
            row["softening_to_order_barycentric_gap"],
            row["order_to_hessian_barycentric_gap"],
            row["hessian_to_third_derivative_barycentric_gap"],
            row["third_derivative_to_wall_barycentric_gap"],
        ]
        entropy = -sum(gap * math.log(gap) for gap in gaps)
        concentration = sum(gap * gap for gap in gaps)
        dominant_gap = max(
            [
                ("interior_to_softening", row["interior_to_softening_barycentric_gap"]),
                ("softening_to_order", row["softening_to_order_barycentric_gap"]),
                ("order_to_hessian", row["order_to_hessian_barycentric_gap"]),
                ("hessian_to_third_derivative", row["hessian_to_third_derivative_barycentric_gap"]),
                ("third_derivative_to_wall", row["third_derivative_to_wall_barycentric_gap"]),
            ],
            key=lambda pair: pair[1],
        )[0]
        decorated_rows.append(
            {
                **row,
                "gap_entropy": entropy,
                "gap_concentration": concentration,
                "dominant_gap": dominant_gap,
                "gap_entropy_jump_from_previous": (entropy - previous_entropy) if previous_entropy is not None else None,
                "gap_concentration_jump_from_previous": (
                    concentration - previous_concentration if previous_concentration is not None else None
                ),
            }
        )
        previous_entropy = entropy
        previous_concentration = concentration

    entropy_values = [row["gap_entropy"] for row in decorated_rows]
    concentration_values = [row["gap_concentration"] for row in decorated_rows]
    entropy_peak_index = max(range(len(entropy_values)), key=lambda index: entropy_values[index])
    concentration_trough_index = min(range(len(concentration_values)), key=lambda index: concentration_values[index])

    entropy_jumps = [row["gap_entropy_jump_from_previous"] for row in decorated_rows[1:]]
    concentration_jumps = [row["gap_concentration_jump_from_previous"] for row in decorated_rows[1:]]
    assert all(jump is not None for jump in entropy_jumps)
    assert all(jump is not None for jump in concentration_jumps)

    entropy_sign_pattern = [1 if jump > 0 else (-1 if jump < 0 else 0) for jump in entropy_jumps]
    concentration_sign_pattern = [1 if jump > 0 else (-1 if jump < 0 else 0) for jump in concentration_jumps]

    return {
        "prime_limit": prime_limit,
        "s_values": s_values,
        "rows": decorated_rows,
        "all_coordinate_jumps_positive": flow["all_coordinate_jumps_positive"],
        "all_wall_gap_jumps_negative": flow["all_wall_gap_jumps_negative"],
        "wall_gap_strictly_decreases": flow["wall_gap_strictly_decreases"],
        "dominant_gap_all_interior_to_softening": all(
            row["dominant_gap"] == "interior_to_softening" for row in decorated_rows
        ),
        "entropy_peak_index": entropy_peak_index,
        "entropy_peak_s": decorated_rows[entropy_peak_index]["s"],
        "entropy_peak_value": entropy_values[entropy_peak_index],
        "concentration_trough_index": concentration_trough_index,
        "concentration_trough_s": decorated_rows[concentration_trough_index]["s"],
        "concentration_trough_value": concentration_values[concentration_trough_index],
        "entropy_sign_pattern": entropy_sign_pattern,
        "concentration_sign_pattern": concentration_sign_pattern,
        "entropy_rises_then_falls": entropy_sign_pattern.count(1) > 0
        and entropy_sign_pattern.count(-1) > 0
        and entropy_sign_pattern.index(-1) > entropy_sign_pattern.index(1),
        "concentration_falls_then_rises": concentration_sign_pattern.count(-1) > 0
        and concentration_sign_pattern.count(1) > 0
        and concentration_sign_pattern.index(1) > concentration_sign_pattern.index(-1),
    }


def completed_defect_spectral_boundary_barycentric_recurrence_resonance_packet(
    prime_limit: int,
    s_values: list[float],
    subintervals: int = 160,
) -> dict[str, object]:
    """Finite recurrence/resonance packet for barycentric dispersion data.

    This upgrades the MCXXVIII turning law by analyzing the sampled entropy and
    concentration sequences in two complementary ways:

    * discrete Fourier magnitudes, to measure the spectral weight of the ladder;
    * best-fit order-two linear recurrences, to detect short arithmetic memory.

    The packet is deliberately finite and cautious: it certifies a shared
    resonance at the same sampled s-value where entropy peaks and concentration
    reaches its trough, together with dominant DC mass and a leading first
    harmonic on the sampled ladder.
    """
    dispersion = completed_defect_spectral_boundary_barycentric_dispersion_turning_packet(
        prime_limit,
        s_values,
        subintervals=subintervals,
    )
    rows = dispersion["rows"]
    entropy_values = [row["gap_entropy"] for row in rows]
    concentration_values = [row["gap_concentration"] for row in rows]

    def _dft_abs(values: list[float]) -> list[float]:
        count = len(values)
        return [
            abs(
                sum(
                    value * cmath.exp(-2j * math.pi * harmonic * index / count)
                    for index, value in enumerate(values)
                )
            )
            for harmonic in range(count)
        ]

    def _harmonic_packet(values: list[float]) -> dict[str, object]:
        magnitudes = _dft_abs(values)
        dc = magnitudes[0]
        if len(magnitudes) == 1:
            dominant_raw_index = None
            dominant_index = None
            dominant_value = None
        else:
            dominant_value = max(magnitudes[1:])
            dominant_raw_index = min(
                index
                for index, value in enumerate(magnitudes[1:], start=1)
                if abs(value - dominant_value) < 1e-12
            )
            dominant_index = min(dominant_raw_index, len(magnitudes) - dominant_raw_index)
        return {
            "dft_abs": magnitudes,
            "dc_component": dc,
            "dc_dominates_nonzero_harmonics": dc > max(magnitudes[1:], default=0.0),
            "dominant_nonzero_harmonic_raw_index": dominant_raw_index,
            "dominant_nonzero_harmonic_index": dominant_index,
            "dominant_nonzero_harmonic_abs": dominant_value,
            "normalized_dft_abs": [value / dc if dc != 0.0 else math.inf for value in magnitudes],
            "conjugate_symmetric": all(
                abs(magnitudes[index] - magnitudes[-index]) < 1e-12
                for index in range(1, len(magnitudes))
            ),
        }

    def _order_two_recurrence(values: list[float]) -> dict[str, object]:
        if len(values) < 3:
            raise ValueError("need at least three values for an order-two recurrence fit")
        x_prev2 = values[:-2]
        x_prev1 = values[1:-1]
        targets = values[2:]
        s11 = sum(value * value for value in x_prev2)
        s12 = sum(left * right for left, right in zip(x_prev2, x_prev1))
        s22 = sum(value * value for value in x_prev1)
        t1 = sum(left * target for left, target in zip(x_prev2, targets))
        t2 = sum(right * target for right, target in zip(x_prev1, targets))
        determinant = s11 * s22 - s12 * s12
        if abs(determinant) < 1e-15:
            raise ValueError("degenerate recurrence fit")
        coefficient_prev2 = (t1 * s22 - t2 * s12) / determinant
        coefficient_prev1 = (s11 * t2 - s12 * t1) / determinant
        residuals = [
            target - (coefficient_prev2 * prev2 + coefficient_prev1 * prev1)
            for prev2, prev1, target in zip(x_prev2, x_prev1, targets)
        ]
        max_abs_residual = max(abs(value) for value in residuals)
        rms_residual = math.sqrt(sum(value * value for value in residuals) / len(residuals))
        return {
            "coefficients": [coefficient_prev2, coefficient_prev1],
            "residuals": residuals,
            "max_abs_residual": max_abs_residual,
            "rms_residual": rms_residual,
        }

    entropy_harmonics = _harmonic_packet(entropy_values)
    concentration_harmonics = _harmonic_packet(concentration_values)
    entropy_recurrence = _order_two_recurrence(entropy_values)
    concentration_recurrence = _order_two_recurrence(concentration_values)

    resonance_coincides = dispersion["entropy_peak_s"] == dispersion["concentration_trough_s"]
    resonance_s = dispersion["entropy_peak_s"] if resonance_coincides else None

    return {
        "prime_limit": prime_limit,
        "s_values": s_values,
        "rows": rows,
        "shared_resonance_detected": resonance_coincides,
        "shared_resonance_s": resonance_s,
        "entropy_peak_s": dispersion["entropy_peak_s"],
        "concentration_trough_s": dispersion["concentration_trough_s"],
        "entropy_sign_pattern": dispersion["entropy_sign_pattern"],
        "concentration_sign_pattern": dispersion["concentration_sign_pattern"],
        "dominant_gap_all_interior_to_softening": dispersion["dominant_gap_all_interior_to_softening"],
        "wall_gap_strictly_decreases": dispersion["wall_gap_strictly_decreases"],
        "all_coordinate_jumps_positive": dispersion["all_coordinate_jumps_positive"],
        "all_wall_gap_jumps_negative": dispersion["all_wall_gap_jumps_negative"],
        "entropy_harmonics": entropy_harmonics,
        "concentration_harmonics": concentration_harmonics,
        "entropy_recurrence": entropy_recurrence,
        "concentration_recurrence": concentration_recurrence,
    }


def completed_defect_dirichlet_log_artanh_profile(prime_limits: list[int], s_values: list[float], max_terms: int = 8) -> dict[str, list[dict[str, object]]]:
    """Profile the closed-form and truncated artanh-series logs of the completed Dirichlet package."""
    payload: dict[str, list[dict[str, object]]] = {}
    for s in s_values:
        key = str(s)
        rows = []
        for prime_limit in prime_limits:
            exact = completed_defect_dirichlet_log_artanh(prime_limit, s)
            series = completed_defect_dirichlet_log_artanh_series(prime_limit, s, max_terms=max_terms)
            rows.append(
                {
                    "prime_limit": prime_limit,
                    "exact_log_real": exact.real,
                    "exact_log_imag": exact.imag,
                    "series_log_real": series.real,
                    "series_log_imag": series.imag,
                    "abs_series_error": abs(exact - series),
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


def exact_branch_congruence_valuation(q: int, split_prime: int, family: str, max_power: int | None = None) -> dict[str, object]:
    """Exact valuation on the matching Eisenstein branch via successive Hensel congruences."""
    if family not in {"Phi3", "Phi6"}:
        raise ValueError("family must be 'Phi3' or 'Phi6'")
    if not is_prime(split_prime) or split_prime % 3 != 1:
        raise ValueError("split_prime must be a prime congruent to 1 mod 3")

    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    exponent = prime_factorization(value).get(split_prime, 0)
    roots_fn = phi3_roots_mod_prime_power if family == "Phi3" else phi6_roots_mod_prime_power
    if max_power is None:
        max_power = max(1, exponent + 2)

    matched_residues: dict[str, int] = {}
    valuation = 0
    for power in range(1, max_power + 1):
        target = q % (split_prime**power)
        residues = roots_fn(split_prime, power)
        if target in residues:
            valuation = power
            matched_residues[str(power)] = target
        else:
            break

    exact_residue_mod_pn = matched_residues.get(str(valuation)) if valuation > 0 else None
    next_match = None
    if valuation + 1 <= max_power:
        next_target = q % (split_prime ** (valuation + 1))
        next_residues = roots_fn(split_prime, valuation + 1)
        if next_target in next_residues:
            next_match = next_target

    target_packet = "q-ω" if family == "Phi3" else "q+ω"
    return {
        "q": q,
        "family": family,
        "split_prime": split_prime,
        "value": value,
        "phi_exponent": exponent,
        "branch_valuation": valuation,
        "target_packet": target_packet,
        "matched_residues": matched_residues,
        "exact_residue_mod_pn": exact_residue_mod_pn,
        "extends_to_next_power": next_match is not None,
        "next_match_mod_pn1": next_match,
        "exact_criterion_holds": (valuation == exponent) and (next_match is None),
        "statement": (
            f"v_pi({target_packet})={valuation} iff q is congruent to the branch residue modulo {split_prime}^{valuation} "
            f"but not modulo {split_prime}^{valuation + 1}."
        ),
    }


def eisenstein_local_global_valuation_packet(q: int, family: str) -> dict[str, object]:
    """Assemble the exact local-global valuation data on all split primes dividing Phi3(q) or Phi6(q)."""
    if family not in {"Phi3", "Phi6"}:
        raise ValueError("family must be 'Phi3' or 'Phi6'")
    value = phi3_value(q) if family == "Phi3" else phi6_value(q)
    factors = prime_factorization(value)
    rows = []
    for p in sorted(factors):
        if is_prime(p) and p % 3 == 1:
            rows.append(exact_branch_congruence_valuation(q, p, family))
    return {
        "q": q,
        "family": family,
        "value": value,
        "factorization": factors,
        "split_prime_rows": rows,
        "all_exact": all(row["exact_criterion_holds"] for row in rows),
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
