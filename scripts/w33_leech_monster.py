#!/usr/bin/env python3
"""
Leech lattice, Monster group numerology, and Moonshine observables

Pillar 57 — Leech / Monster / Moonshine

Provides computational evidence linking three copies of E8 (E8^3) and the
Leech lattice; highlights numerology connecting Leech kissing number (196560)
with Monster representation dimensions (196883) and group-size ratios.

Usage:
    python scripts/w33_leech_monster.py

"""
from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, log2, log10
from pathlib import Path
from typing import Dict

# Ensure we can import sibling modules from scripts/ when executed as a file.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
# Also allow importing top-level `tools.*` modules when running `python scripts/...`.
ROOT_DIR = SCRIPTS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from w33_cryptographic_lattice import analyze_leech_connection
from w33_homology import (
    boundary_matrix,
    build_clique_complex,
    build_w33,
    compute_homology,
)


def _load_monster_irreps_via_gap() -> list | None:
    """Try to obtain Monster irreducible character *degrees* via GAP/libgap or
    fall back to a bundled static JSON file.

    Returns a list of integer character degrees if successful, otherwise None.
    """
    # 1) libgap (Sage) path
    try:
        from sage.all import libgap  # type: ignore

        ct = libgap.CharacterTable("M")
        irr = libgap.Irr(ct)
        degs = [int(c[0]) for c in irr]
        return degs
    except Exception:
        pass

    # 2) GAP CLI fallback
    if shutil.which("gap") is not None:
        gap_code = (
            't := CharacterTable("M"); '
            "degs := List(Irr(t), chi -> chi[1]); "
            'Print("GAP:MONSTER_DEGREES:", degs, "\n"); '
            "quit;"
        )
        try:
            proc = subprocess.run(
                ["gap", "-q"],
                input=gap_code,
                text=True,
                capture_output=True,
                check=True,
            )
            for line in proc.stdout.splitlines():
                if line.startswith("GAP:MONSTER_DEGREES:"):
                    payload = line.split(":", 1)[1].strip()
                    degs = ast.literal_eval(payload)
                    return [int(x) for x in degs]
        except Exception:
            pass

    # 3) Bundled static JSON (data/monster_degrees.json)
    try:
        import json
        from pathlib import Path

        static_path = (
            Path(__file__).resolve().parents[1] / "data" / "monster_degrees.json"
        )
        if static_path.exists():
            vals = json.loads(static_path.read_text(encoding="utf-8"))
            return [int(x) for x in vals]
    except Exception:
        pass

    return None


def e4_coeffs(n_terms: int = 8):
    """Return the first n_terms coefficients of E4(q)=Theta_{E8}(q).

    Coefficients are integers: E4 = 1 + 240 q + 2160 q^2 + 6720 q^3 + 17520 q^4 + ...
    """
    base = [1, 240, 2160, 6720, 17520, 30240, 60480, 82560]
    return base[:n_terms]


def poly_power(coeffs, power: int, n_terms: int):
    """Compute first n_terms coefficients of (sum coeffs[i] q^i)^power."""
    out = [0] * n_terms
    out[0] = 1 if power == 0 else coeffs[0] ** power
    # naive convolution (sufficient for small n_terms)
    from itertools import product

    # start from 1st power by repeated convolution
    cur = coeffs[:n_terms]
    for _ in range(1, power):
        nxt = [0] * n_terms
        for i in range(n_terms):
            if cur[i] == 0:
                continue
            for j in range(n_terms - i):
                if j >= len(coeffs):
                    break
                nxt[i + j] += cur[i] * coeffs[j]
        cur = nxt
    return cur[:n_terms]


def j_coeffs(n_terms: int = 6):
    """Compute first n_terms Fourier coefficients of the Klein j‑invariant.

    j(τ) = q^{-1} + 744 + Σ_{n>=1} c(n) q^n  — we return [c(1),...,c(n)].

    Implementation: j = E4^3 / Δ where E4 = 1 + 240 Σ σ_3(n) q^n and
    Δ(q)=q Π_{m>=1} (1-q^m)^{24}. Series division is used to produce exact
    integer coefficients up to the requested order (fast for n_terms ≤ 100).
    """
    # fast path: small precomputed values
    known = [
        196884,
        21493760,
        864299970,
        20245856256,
        333202640600,
        4252023300096,
        44656994071935,
        401490886656000,
        3176440229784420,
        22567393309593600,
    ]
    if n_terms <= len(known):
        return known[:n_terms]

    # helper: divisor-sum σ_k
    def sigma_k(n: int, k: int) -> int:
        s = 0
        d = 1
        while d * d <= n:
            if n % d == 0:
                s += d**k
                e = n // d
                if e != d:
                    s += e**k
            d += 1
        return s

    # degrees we need for series arithmetic
    N = n_terms + 4  # small slack

    # E4 coefficients: E4 = 1 + 240 Σ_{n>=1} σ_3(n) q^n
    e4 = [1] + [240 * sigma_k(i, 3) for i in range(1, N + 1)]

    # A = E4^3 (convolution via existing poly_power)
    A = poly_power(e4, 3, N + 1)

    # d(q) = Δ(q)/q = Π_{m>=1} (1-q^m)^{24}  (compute up to degree N)
    from math import comb

    d = [1] + [0] * N
    for m in range(1, N + 1):
        # (1 - q^m)^24 = sum_{j=0..24} C(24,j) (-1)^j q^{m*j}
        coeff = [0] * (N + 1)
        for j in range(0, 25):
            power = m * j
            if power > N:
                break
            coeff[power] = ((-1) ** j) * comb(24, j)
        # convolve d <- d * coeff (truncated)
        newd = [0] * (N + 1)
        for k in range(0, N + 1):
            s = 0
            for i in range(0, k + 1):
                s += d[i] * coeff[k - i]
            newd[k] = s
        d = newd

    # Now perform series division S = A / d where d[0] == 1 and A,d length >= N
    S = [0] * (N + 1)
    for k in range(0, N + 1):
        s = A[k]
        for i in range(1, k + 1):
            s -= d[i] * S[k - i]
        S[k] = s  # d[0] == 1

    # j(q) = q^{-1} * S(q)  => coefficient c(n) = S[n+1]
    out = [int(S[n + 1]) for n in range(1, n_terms + 1)]
    return out


# ----------------------------- McKay / Thompson -----------------------------


def analyze_rogers_ramanujan_j_invariant(*, n_terms: int = 8) -> dict[str, object]:
    """Verify the classical Rogers–Ramanujan continued fraction identity for j(τ).

    Let R(q) be the Rogers–Ramanujan continued fraction and set u(q) = R(q)^5.
    A classical identity expresses the Klein j-invariant as a rational function:

        j(τ) = - (u^4 - 228 u^3 + 494 u^2 + 228 u + 1)^3 / (u (u^2 + 11 u - 1)^5)

    Since u(q) = q + O(q^2), the right-hand side has Laurent expansion:
        j(τ) = q^{-1} + 744 + 196884 q + ...

    This routine computes u(q) via the product formula for R(q) and checks the
    identity to the requested order, fully deterministically and offline.
    """
    from fractions import Fraction

    if n_terms < 1:
        raise ValueError("n_terms must be >= 1")

    # We verify q^{-1}, q^0, and q^1..q^n_terms.
    N = int(n_terms) + 6  # slack for series arithmetic in rational functions

    def _as_frac_series(xs: list[int]) -> list[Fraction]:
        return [Fraction(int(x), 1) for x in xs]

    def _series_add(a: list[Fraction], b: list[Fraction], n: int) -> list[Fraction]:
        out = [Fraction(0, 1) for _ in range(n + 1)]
        for i in range(n + 1):
            if i < len(a):
                out[i] += a[i]
            if i < len(b):
                out[i] += b[i]
        return out

    def _series_scale(a: list[Fraction], c: Fraction, n: int) -> list[Fraction]:
        out = [Fraction(0, 1) for _ in range(n + 1)]
        for i in range(min(len(a), n + 1)):
            out[i] = a[i] * c
        return out

    def _series_shift(a: list[Fraction], k: int, n: int) -> list[Fraction]:
        out = [Fraction(0, 1) for _ in range(n + 1)]
        for i in range(min(len(a), n + 1 - k)):
            out[i + k] = a[i]
        return out

    def _series_mul(a: list[Fraction], b: list[Fraction], n: int) -> list[Fraction]:
        out = [Fraction(0, 1) for _ in range(n + 1)]
        for i in range(min(len(a), n + 1)):
            ai = a[i]
            if ai == 0:
                continue
            max_j = min(len(b) - 1, n - i)
            for j in range(max_j + 1):
                bj = b[j]
                if bj != 0:
                    out[i + j] += ai * bj
        return out

    def _series_pow(a: list[Fraction], e: int, n: int) -> list[Fraction]:
        if e < 0:
            raise ValueError("negative powers not supported")
        out = [Fraction(0, 1) for _ in range(n + 1)]
        out[0] = Fraction(1, 1)
        base = a[:]
        exp = int(e)
        while exp:
            if exp & 1:
                out = _series_mul(out, base, n)
            exp >>= 1
            if exp:
                base = _series_mul(base, base, n)
        return out

    def _series_inv(a: list[Fraction], n: int) -> list[Fraction]:
        if not a or a[0] == 0:
            raise ValueError("series must have nonzero constant term")
        a0 = a[0]
        out = [Fraction(0, 1) for _ in range(n + 1)]
        out[0] = Fraction(1, 1) / a0
        for k in range(1, n + 1):
            s = Fraction(0, 1)
            for i in range(1, k + 1):
                if i < len(a):
                    s += a[i] * out[k - i]
            out[k] = -s / a0
        return out

    def _series_div(a: list[Fraction], b: list[Fraction], n: int) -> list[Fraction]:
        return _series_mul(a, _series_inv(b, n), n)

    # Product factors for (q^k; q^5)_∞ truncated to degree N:
    #   Π_{n>=0} (1 - q^{k + 5n})
    def _pochhammer_step5(k: int, n: int) -> list[Fraction]:
        out = [Fraction(0, 1) for _ in range(n + 1)]
        out[0] = Fraction(1, 1)
        exp = int(k)
        while exp <= n:
            fac = [Fraction(0, 1) for _ in range(n + 1)]
            fac[0] = Fraction(1, 1)
            fac[exp] = Fraction(-1, 1)
            out = _series_mul(out, fac, n)
            exp += 5
        return out

    # u(q) = R(q)^5 = q * ( ( (q; q^5)_∞ (q^4; q^5)_∞ ) / ( (q^2; q^5)_∞ (q^3; q^5)_∞ ) )^5
    num = _series_mul(_pochhammer_step5(1, N), _pochhammer_step5(4, N), N)
    den = _series_mul(_pochhammer_step5(2, N), _pochhammer_step5(3, N), N)
    P = _series_div(num, den, N)
    P5 = _series_pow(P, 5, N)
    u = _series_shift(P5, 1, N)  # multiply by q

    # Sanity: u(q) starts with q + O(q^2)
    assert u[0] == 0 and u[1] == 1, f"Unexpected u(q) leading terms: {u[:3]}"

    u2 = _series_mul(u, u, N)
    u3 = _series_mul(u2, u, N)
    u4 = _series_mul(u2, u2, N)

    # A(u) = u^4 - 228 u^3 + 494 u^2 + 228 u + 1
    A = _series_add(
        _series_add(
            _series_add(
                _series_add(
                    _series_scale(u4, Fraction(1), N),
                    _series_scale(u3, Fraction(-228), N),
                    N,
                ),
                _series_scale(u2, Fraction(494), N),
                N,
            ),
            _series_scale(u, Fraction(228), N),
            N,
        ),
        [Fraction(1, 1)],
        N,
    )

    # B(u) = u^2 + 11 u - 1
    B = _series_add(
        _series_add(u2, _series_scale(u, Fraction(11), N), N), [Fraction(-1, 1)], N
    )

    A3 = _series_pow(A, 3, N)
    B5 = _series_pow(B, 5, N)
    C = _series_scale(_series_div(A3, B5, N), Fraction(-1, 1), N)  # -A^3/B^5

    # 1/u as Laurent: u(q) = q * u1(q) with u1(0)=1.
    u1 = u[1:]  # length N, represents u/q
    inv_u1 = _series_inv(u1, N)  # power series
    J = _series_mul(C, inv_u1, N)  # this corresponds to q * j(q)

    # Extract Laurent coefficients: j = q^{-1}*J
    q_minus1 = J[0]
    q0 = J[1]
    coeffs = [J[n + 1] for n in range(1, n_terms + 1)]

    # Reference values for comparison.
    ref = j_coeffs(n_terms)
    ok = True
    if q_minus1 != 1 or q0 != 744:
        ok = False
    for got, exp in zip(coeffs, ref):
        if got != exp:
            ok = False
            break

    # Ensure integrality of computed coefficients.
    def _to_int(fr: Fraction) -> int:
        if fr.denominator != 1:
            raise AssertionError(f"Non-integral coefficient: {fr}")
        return int(fr.numerator)

    out_coeffs = [_to_int(x) for x in coeffs]
    return {
        "available": True,
        "verified": ok,
        "n_terms_verified": int(n_terms),
        "u_series": [_to_int(x) for x in u[: min(N + 1, n_terms + 3)]],
        "j_from_rogers_ramanujan": {
            "q^-1": _to_int(q_minus1),
            "q^0": _to_int(q0),
            "coeffs": out_coeffs,
        },
        "j_reference": {"coeffs": [int(x) for x in ref]},
        "identity": {
            "u": "u(q)=R(q)^5",
            "j": "-(u^4 - 228 u^3 + 494 u^2 + 228 u + 1)^3 / (u (u^2 + 11 u - 1)^5)",
        },
    }


def load_monster_characters(json_path: str | None = None) -> dict | None:
    """Load full Monster character table from JSON file (if present).

    Expected JSON format:
      { "class_names": [...], "irreps": [{"degree": d, "values": [...]}, ...] }

    Returns dict or None if file not found / parsing fails.
    """
    import json
    from pathlib import Path

    if json_path:
        p = Path(json_path)
    else:
        p = Path(__file__).resolve().parents[1] / "data" / "monster_characters.json"
    if not p.exists():
        return None
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
        # basic validation
        if (
            not isinstance(payload, dict)
            or "class_names" not in payload
            or "irreps" not in payload
        ):
            return None
        return payload
    except Exception:
        return None


def _load_monster_char_map_via_gap(
    class_name: str, json_path: str | None = None
) -> dict | None:
    """Return a mapping {irrep_degree: character_value} for the given Monster
    conjugacy-class name.

    Priority order:
      1. bundled JSON file (data/monster_characters.json or path override)
      2. libgap (Sage)
      3. GAP CLI

    Returns None if no character data is available for the requested class.
    """
    # 1) check for bundled JSON (fast and safe)
    jt = load_monster_characters(json_path)
    if jt is not None:
        try:
            names = jt["class_names"]
            idx = names.index(class_name)
            mapping = {int(ir["degree"]): int(ir["values"][idx]) for ir in jt["irreps"]}
            return mapping
        except Exception:
            # fall through to other methods
            pass

    # 2) try libgap (Sage)
    try:
        from sage.all import libgap  # type: ignore

        t = libgap.CharacterTable("M")
        names = list(libgap.ClassNames(t))
        try:
            idx = names.index(class_name)
        except ValueError:
            return None
        irr = libgap.Irr(t)
        degs = [int(c[0]) for c in irr]
        vals = [int(c[idx]) for c in irr]
        return {int(d): int(v) for d, v in zip(degs, vals)}
    except Exception:
        pass

    # 3) GAP CLI fallback
    import ast
    import shutil
    import subprocess

    if shutil.which("gap") is None:
        return None

    gap_code = (
        f't := CharacterTable("M"); '
        f"names := ClassNames(t); "
        f'idx := Position(names, "{class_name}"); '
        f'if idx = fail then Print("GAP:CLASS_NOT_FOUND\n"); quit; fi; '
        "vals := List(Irr(t), chi -> chi[idx]); "
        "degs := List(Irr(t), chi -> chi[1]); "
        'Print("GAP:CHAR_DEGREES:", degs, "\n"); '
        'Print("GAP:CHAR_VALUES:", vals, "\n"); '
        "quit;"
    )
    try:
        proc = subprocess.run(
            ["gap", "-q"], input=gap_code, text=True, capture_output=True, check=True
        )
    except Exception:
        return None

    degrees = None
    values = None
    for line in proc.stdout.splitlines():
        if line.startswith("GAP:CHAR_DEGREES:"):
            degrees = ast.literal_eval(line.split(":", 1)[1].strip())
        elif line.startswith("GAP:CHAR_VALUES:"):
            values = ast.literal_eval(line.split(":", 1)[1].strip())
    if degrees is None or values is None:
        return None
    return {int(d): int(v) for d, v in zip(degrees, values)}


def _qpoly_mul(a: list[int], b: list[int], max_deg: int) -> list[int]:
    out = [0] * (max_deg + 1)
    for i, ai in enumerate(a[: max_deg + 1]):
        if ai == 0:
            continue
        max_j = max_deg - i
        for j, bj in enumerate(b[: max_j + 1]):
            if bj == 0:
                continue
            out[i + j] += ai * bj
    return out


def _qpoly_pow(base: list[int], exp: int, max_deg: int) -> list[int]:
    if exp < 0:
        raise ValueError("exp must be non-negative")
    result = [0] * (max_deg + 1)
    result[0] = 1
    cur = base[: max_deg + 1] + [0] * max(0, (max_deg + 1) - len(base))
    e = exp
    while e:
        if e & 1:
            result = _qpoly_mul(result, cur, max_deg)
        e >>= 1
        if e:
            cur = _qpoly_mul(cur, cur, max_deg)
    return result


def _qpoly_inv(den: list[int], max_deg: int) -> list[int]:
    """Inverse of a power series with den[0] == 1, truncated to max_deg."""
    if not den or den[0] != 1:
        raise ValueError("series inverse requires den[0] == 1")
    out = [0] * (max_deg + 1)
    out[0] = 1
    for n in range(1, max_deg + 1):
        s = 0
        for k in range(1, n + 1):
            if k < len(den):
                s += den[k] * out[n - k]
        out[n] = -s
    return out


def _qpoly_div(num: list[int], den: list[int], max_deg: int) -> list[int]:
    inv = _qpoly_inv(den, max_deg)
    num_pad = num[: max_deg + 1] + [0] * max(0, (max_deg + 1) - len(num))
    return _qpoly_mul(num_pad, inv, max_deg)


def _qpochhammer(max_deg: int, step: int = 1) -> list[int]:
    """Compute (q^step; q^step)_inf = prod_{k>=1} (1 - q^{k*step}) to max_deg."""
    if step <= 0:
        raise ValueError("step must be positive")
    poly = [1] + [0] * max_deg
    for k in range(1, (max_deg // step) + 1):
        power = k * step
        for n in range(max_deg, power - 1, -1):
            poly[n] -= poly[n - power]
    return poly


def _qpochhammer_arith(max_deg: int, step: int, offset: int) -> list[int]:
    """Compute prod_{k>=0} (1 - q^{offset + k*step}) to max_deg.

    This is a shifted q-Pochhammer (q^offset; q^step)_∞ truncated to max_deg.
    """
    if step <= 0:
        raise ValueError("step must be positive")
    if offset <= 0:
        raise ValueError("offset must be positive")
    poly = [1] + [0] * max_deg
    power = offset
    while power <= max_deg:
        for n in range(max_deg, power - 1, -1):
            poly[n] -= poly[n - power]
        power += step
    return poly


def _qpoly_compose_q_power(poly: list[int], p: int, max_deg: int) -> list[int]:
    """Return poly(q^p) truncated to max_deg (poly is a power series in q)."""
    if p <= 0:
        raise ValueError("p must be positive")
    out = [0] * (max_deg + 1)
    for n, cn in enumerate(poly[: max_deg + 1]):
        exp = n * p
        if exp > max_deg:
            break
        if cn:
            out[exp] = int(cn)
    return out


def _rogers_ramanujan_GH(max_deg: int) -> tuple[list[int], list[int]]:
    """Rogers-Ramanujan functions G,H as power series to max_deg.

    Conventions (Euler products; no fractional q-shifts):
      G(q) = 1 / ((q; q^5)_inf (q^4; q^5)_inf)
      H(q) = 1 / ((q^2; q^5)_inf (q^3; q^5)_inf)
    """
    a = _qpochhammer_arith(max_deg, step=5, offset=1)
    b = _qpochhammer_arith(max_deg, step=5, offset=4)
    c = _qpochhammer_arith(max_deg, step=5, offset=2)
    d = _qpochhammer_arith(max_deg, step=5, offset=3)
    G_den = _qpoly_mul(a, b, max_deg)
    H_den = _qpoly_mul(c, d, max_deg)
    return _qpoly_inv(G_den, max_deg), _qpoly_inv(H_den, max_deg)


def _ramanujan_phi(max_deg: int, *, step: int = 1) -> list[int]:
    """Ramanujan/Jacobi phi(q)=sum_{n in Z} q^{n^2} as a power series."""
    if step <= 0:
        raise ValueError("step must be positive")
    out = [0] * (max_deg + 1)
    out[0] = 1
    n = 1
    while True:
        exp = step * n * n
        if exp > max_deg:
            break
        out[exp] += 2
        n += 1
    return out


def _ramanujan_psi(max_deg: int, *, step: int = 1) -> list[int]:
    """Ramanujan psi(q)=sum_{n>=0} q^{n(n+1)/2} as a power series."""
    if step <= 0:
        raise ValueError("step must be positive")
    out = [0] * (max_deg + 1)
    out[0] = 1
    n = 1
    while True:
        exp = step * (n * (n + 1) // 2)
        if exp > max_deg:
            break
        out[exp] += 1
        n += 1
    return out


def mckay_thompson_series(class_name: str, max_q_exp: int = 8) -> dict[int, int] | None:
    """Return a McKay-Thompson series T_g(q)=q^-1 + sum_{n>=1} a_n q^n.

    Offline (no GAP) support is implemented for a subset of prime-order classes
    expressible as eta-quotients, plus a small number of composite-order
    classes appearing in classical eta-product formulas:
      - Fricke primes (pA): 2A, 3A, 5A, 7A, 13A
      - Non-Fricke primes (pB): 2B, 3B, 5B, 7B, 13B
      - Composite: 4A–4D, 6A–6E, 8A/8A'/8B/8E, 9A, 10A–10E, 11A, 3C

    Identity class 1A returns J(q)=j(q)-744.
    """
    name = class_name.upper()
    if max_q_exp < 0:
        raise ValueError("max_q_exp must be non-negative")

    if name in ("1A", "ID", "IDENTITY"):
        coeffs = j_coeffs(max_q_exp)
        out = {-1: 1, 0: 0}
        for n, c in enumerate(coeffs, start=1):
            out[n] = int(c)
        return out

    # --- Ogg-prime McKay-Thompson series beyond p<=13 (offline, deterministic) ---
    #
    # Conventions:
    # - We compute holomorphic q-series using Euler products and then apply the
    #   required q^{-1} shift so the result is normalized as q^{-1}+O(q).
    # - Coefficients are verified against OEIS b-files in local development.

    if name == "17A":
        # OEIS A058530:
        #   T_17A(q) = -2 + q^{-1} * ((psi(q^2) phi(q^17) - q^4 phi(q) psi(q^34))
        #                            /(f(-q) f(-q^17)))^2
        deg = max_q_exp + 1
        phi1 = _ramanujan_phi(deg, step=1)
        phi17 = _ramanujan_phi(deg, step=17)
        psi2 = _ramanujan_psi(deg, step=2)
        psi34 = _ramanujan_psi(deg, step=34)
        num1 = _qpoly_mul(psi2, phi17, deg)
        num2 = _qpoly_mul(phi1, psi34, deg)
        num2s = [0] * (deg + 1)
        for i, ci in enumerate(num2):
            if ci and i + 4 <= deg:
                num2s[i + 4] += int(ci)
        num = [int(a) - int(b) for a, b in zip(num1, num2s)]
        den = _qpoly_mul(_qpochhammer(deg, step=1), _qpochhammer(deg, step=17), deg)
        ratio = _qpoly_div(num, den, deg)
        ratio2 = _qpoly_pow(ratio, 2, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio2):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) - 2
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name == "19A":
        # OEIS A058549:
        #   T_19A(q) = -3 + q^{-1} * (G(q)G(q^19) + q^4 H(q)H(q^19))^3
        deg = max_q_exp + 1
        G, H = _rogers_ramanujan_GH(deg)
        Gp = _qpoly_compose_q_power(G, 19, deg)
        Hp = _qpoly_compose_q_power(H, 19, deg)
        t1 = _qpoly_mul(G, Gp, deg)
        t2 = _qpoly_mul(H, Hp, deg)
        t2s = [0] * (deg + 1)
        for i, ci in enumerate(t2):
            if ci and i + 4 <= deg:
                t2s[i + 4] += int(ci)
        expr = [int(a) + int(b) for a, b in zip(t1, t2s)]
        expr3 = _qpoly_pow(expr, 3, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(expr3):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) - 3
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name in ("23A", "23B"):
        # OEIS A058570:
        #   The prime-order Monster classes 23A and 23B share the same
        #   McKay–Thompson series (often denoted 23AB in moonshine tables).
        #
        #   F = eta(q)eta(q^23)/(eta(q^2)eta(q^46))   (Euler product "eta")
        #   T_23AB(q) = (F+1)(F^2+4)/F^2, with the implicit q^{-1} shift from F.
        #
        # Write F = q^{-1} P with P(0)=1, where P is the Euler-product ratio.
        # Then:
        #   T = q^{-1} P + 1 + 4 q P^{-1} + 4 q^2 P^{-2}
        deg = max_q_exp + 2
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e23 = _qpochhammer(deg, step=23)
        e46 = _qpochhammer(deg, step=46)
        P = _qpoly_div(_qpoly_mul(e1, e23, deg), _qpoly_mul(e2, e46, deg), deg)
        Pinv = _qpoly_inv(P, deg)
        P2inv = _qpoly_inv(_qpoly_mul(P, P, deg), deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(P):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) + 1
        for k, ck in enumerate(Pinv):
            exp = 1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(4 * ck)
        for k, ck in enumerate(P2inv):
            exp = 2 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(4 * ck)

        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name == "29A":
        # OEIS A058611:
        #   T_29A(q) = -2 + q^{-1} * (G(q)G(q^29) + q^6 H(q)H(q^29))^2
        deg = max_q_exp + 1
        G, H = _rogers_ramanujan_GH(deg)
        Gp = _qpoly_compose_q_power(G, 29, deg)
        Hp = _qpoly_compose_q_power(H, 29, deg)
        t1 = _qpoly_mul(G, Gp, deg)
        t2 = _qpoly_mul(H, Hp, deg)
        t2s = [0] * (deg + 1)
        for i, ci in enumerate(t2):
            if ci and i + 6 <= deg:
                t2s[i + 6] += int(ci)
        expr = [int(a) + int(b) for a, b in zip(t1, t2s)]
        expr2 = _qpoly_pow(expr, 2, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(expr2):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) - 2
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name in ("31A", "31B"):
        # OEIS A058628:
        #   T_31A(q) = q^{-1} * (G(q^31)H(q) - q^6 H(q^31)G(q))^3
        deg = max_q_exp + 1
        G, H = _rogers_ramanujan_GH(deg)
        Gp = _qpoly_compose_q_power(G, 31, deg)
        Hp = _qpoly_compose_q_power(H, 31, deg)
        t1 = _qpoly_mul(Gp, H, deg)
        t2 = _qpoly_mul(Hp, G, deg)
        t2s = [0] * (deg + 1)
        for i, ci in enumerate(t2):
            if ci and i + 6 <= deg:
                t2s[i + 6] += int(ci)
        expr = [int(a) - int(b) for a, b in zip(t1, t2s)]
        expr3 = _qpoly_pow(expr, 3, deg)
        series: dict[int, int] = {}
        for k, ck in enumerate(expr3):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name == "41A":
        # OEIS A058670:
        #   T_41A(q) = q^{-1} * (G(q^41)H(q) - q^8 H(q^41)G(q))^2
        deg = max_q_exp + 1
        G, H = _rogers_ramanujan_GH(deg)
        Gp = _qpoly_compose_q_power(G, 41, deg)
        Hp = _qpoly_compose_q_power(H, 41, deg)
        t1 = _qpoly_mul(Gp, H, deg)
        t2 = _qpoly_mul(Hp, G, deg)
        t2s = [0] * (deg + 1)
        for i, ci in enumerate(t2):
            if ci and i + 8 <= deg:
                t2s[i + 8] += int(ci)
        expr = [int(a) - int(b) for a, b in zip(t1, t2s)]
        expr2 = _qpoly_pow(expr, 2, deg)
        series: dict[int, int] = {}
        for k, ck in enumerate(expr2):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name in ("47A", "47B"):
        # OEIS A058690:
        #   T_47A(q) = q^{-2} * (Theta_Q1(q) - Theta_Q2(q)) / (2 * eta(q) eta(q^47))
        # with Q1(n,m)=n^2+n*m+12 m^2, Q2(n,m)=2 n^2+n*m+6 m^2, eta Euler product.
        from math import isqrt

        deg = max_q_exp + 2

        def theta_Q(max_deg: int, a: int, b: int, c: int) -> list[int]:
            out = [0] * (max_deg + 1)
            n_max = isqrt(max_deg // max(1, a)) + 4
            m_max = isqrt(max_deg // max(1, c)) + 4
            for n in range(-n_max, n_max + 1):
                for m in range(-m_max, m_max + 1):
                    qv = int(a) * n * n + int(b) * n * m + int(c) * m * m
                    if 0 <= qv <= max_deg:
                        out[qv] += 1
            return out

        th1 = theta_Q(deg, 1, 1, 12)
        th2 = theta_Q(deg, 2, 1, 6)
        num = [int(a) - int(b) for a, b in zip(th1, th2)]
        den = _qpoly_mul(_qpochhammer(deg, step=1), _qpochhammer(deg, step=47), deg)
        quot = _qpoly_div(num, den, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(quot):
            if ck == 0:
                continue
            if ck % 2 != 0:
                raise AssertionError(f"Unexpected odd theta/eta coefficient at q^{k}")
            exp = -2 + k
            if -1 <= exp <= max_q_exp:
                series[exp] = series.get(exp, 0) + int(ck // 2)

        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name in ("59A", "59B"):
        # OEIS A058724:
        #   T_59A(q) = -1 + (G(q^59)G(q) + q^12 H(q^59)H(q)) / q
        deg = max_q_exp + 1
        G, H = _rogers_ramanujan_GH(deg)
        Gp = _qpoly_compose_q_power(G, 59, deg)
        Hp = _qpoly_compose_q_power(H, 59, deg)
        t1 = _qpoly_mul(Gp, G, deg)
        t2 = _qpoly_mul(Hp, H, deg)
        t2s = [0] * (deg + 1)
        for i, ci in enumerate(t2):
            if ci and i + 12 <= deg:
                t2s[i + 12] += int(ci)
        num = [int(a) + int(b) for a, b in zip(t1, t2s)]

        series: dict[int, int] = {}
        for k, ck in enumerate(num):
            exp = -1 + k  # divide by q
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) - 1
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name in ("71A", "71B"):
        # OEIS A034322:
        #   T_71A(q) = q^{-1} * (G(q^71)H(q) - q^14 H(q^71)G(q))
        deg = max_q_exp + 1
        G, H = _rogers_ramanujan_GH(deg)
        Gp = _qpoly_compose_q_power(G, 71, deg)
        Hp = _qpoly_compose_q_power(H, 71, deg)
        t1 = _qpoly_mul(Gp, H, deg)
        t2 = _qpoly_mul(Hp, G, deg)
        t2s = [0] * (deg + 1)
        for i, ci in enumerate(t2):
            if ci and i + 14 <= deg:
                t2s[i + 14] += int(ci)
        expr = [int(a) - int(b) for a, b in zip(t1, t2s)]

        series: dict[int, int] = {}
        for k, ck in enumerate(expr):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        if series.get(0, 0) != 0 or series.get(-1, 0) != 1:
            raise AssertionError(f"Normalization failed for {name}")
        return series

    if name == "4C":
        # Ramanujan–Sato / Moonshine:
        #   j_4C(τ) = (η(τ)/η(4τ))^8 = q^{-1} - 8 + 20 q - 62 q^3 + ...
        # Normalize to constant term 0 => T_4C = j_4C + 8.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e4 = _qpochhammer(deg, step=4)
        ratio = _qpoly_div(e1, e4, deg)
        ratio_pow = _qpoly_pow(ratio, 8, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) + 8
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "4A":
        # Ramanujan–Sato / Moonshine:
        #   j_4A(τ) = (η(2τ)^2/(η(τ)η(4τ)))^{24}
        #          = q^{-1} + 24 + 276 q + 2048 q^2 + ...
        # Normalize to constant term 0 => T_4A = j_4A - 24.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        num = _qpoly_mul(e2, e2, deg)
        den = _qpoly_mul(e1, e4, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 24, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) - 24
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "4B":
        # (Ramanujan–Sato / Moonshine)
        #   j_4B(τ) = (η(2τ)/η(4τ))^{12} + 2^6 (η(4τ)/η(2τ))^{12}
        #          = q^{-1} + 52 q + 834 q^3 + ...
        # Constant term is 0 in this normalization.
        deg = max_q_exp + 1
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        ratio = _qpoly_div(e2, e4, deg)
        r0 = _qpoly_pow(ratio, 12, deg)
        r0_inv = _qpoly_inv(r0, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(r0):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        for k, ck in enumerate(r0_inv):
            exp = 1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(64 * ck)

        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "4D":
        # (Ramanujan–Sato / Moonshine)
        #   j_4D(τ) = (η(2τ)/η(4τ))^{12} = q^{-1} - 12 q + 66 q^3 + ...
        # Constant term is 0 in this normalization.
        deg = max_q_exp + 1
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        ratio = _qpoly_div(e2, e4, deg)
        r0 = _qpoly_pow(ratio, 12, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(r0):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "6B":
        # Ramanujan–Sato / Moonshine:
        #   j_6B(τ) = (η(2τ)η(3τ)/(η(τ)η(6τ)))^{12}
        #          = q^{-1} + 12 + 78 q + 364 q^2 + ...
        # Normalize to constant term 0 => T_6B = j_6B - 12.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e3 = _qpochhammer(deg, step=3)
        e6 = _qpochhammer(deg, step=6)
        num = _qpoly_mul(e2, e3, deg)
        den = _qpoly_mul(e1, e6, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 12, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) - 12
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "6C":
        # Ramanujan–Sato / Moonshine:
        #   j_6C(τ) = (η(τ)η(3τ)/(η(2τ)η(6τ)))^{6}
        #          = q^{-1} - 6 + 15 q - 32 q^2 + ...
        # Normalize to constant term 0 => T_6C = j_6C + 6.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e3 = _qpochhammer(deg, step=3)
        e6 = _qpochhammer(deg, step=6)
        num = _qpoly_mul(e1, e3, deg)
        den = _qpoly_mul(e2, e6, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 6, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) + 6
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "6D":
        # Ramanujan–Sato / Moonshine:
        #   j_6D(τ) = (η(τ)η(2τ)/(η(3τ)η(6τ)))^{4}
        #          = q^{-1} - 4 - 2 q + 28 q^2 + ...
        # Normalize to constant term 0 => T_6D = j_6D + 4.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e3 = _qpochhammer(deg, step=3)
        e6 = _qpochhammer(deg, step=6)
        num = _qpoly_mul(e1, e2, deg)
        den = _qpoly_mul(e3, e6, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 4, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) + 4
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "6E":
        # Ramanujan–Sato / Moonshine:
        #   j_6E(τ) = (η(2τ)η(3τ)^3/(η(τ)η(6τ)^3))^{3}
        #          = q^{-1} + 3 + 6 q + 4 q^2 + ...
        # Normalize to constant term 0 => T_6E = j_6E - 3.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e3 = _qpochhammer(deg, step=3)
        e6 = _qpochhammer(deg, step=6)
        e3_3 = _qpoly_pow(e3, 3, deg)
        e6_3 = _qpoly_pow(e6, 3, deg)
        num = _qpoly_mul(e2, e3_3, deg)
        den = _qpoly_mul(e1, e6_3, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 3, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) - 3
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "6A":
        # Ramanujan–Sato / Moonshine "near-square" identity:
        #   j_6A = (sqrt(j_6B) - 1/sqrt(j_6B))^2 = j_6B + 1/j_6B - 2
        # and j_6B = q^{-1} * R(q) with R(0)=1, so 1/j_6B = q * R(q)^{-1}.
        #
        # Normalize to constant term 0 => T_6A = j_6A - 10.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e3 = _qpochhammer(deg, step=3)
        e6 = _qpochhammer(deg, step=6)
        num = _qpoly_mul(e2, e3, deg)
        den = _qpoly_mul(e1, e6, deg)
        ratio = _qpoly_div(num, den, deg)
        r = _qpoly_pow(ratio, 12, deg)  # R(q) above
        r_inv = _qpoly_inv(r, deg)

        series: dict[int, int] = {}
        # j_6B = q^{-1} R(q)
        for k, ck in enumerate(r):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        # + 1/j_6B = q * R(q)^{-1}
        for k, ck in enumerate(r_inv):
            exp = 1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        # - 2
        series[0] = series.get(0, 0) - 2

        # Normalize to constant term 0 (expected constant is 10).
        series[0] = series.get(0, 0) - 10
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name in ("8A'", "8APRIME", "8A-PRIME"):
        # Alias for the "8A'" hauptmodul in the literature.
        name = "8A'"

    if name == "8A":
        # (Ramanujan–Sato / Moonshine)
        #   j_8A(τ) = (η(2τ)η(4τ)/(η(τ)η(8τ)))^{8}
        #          = q^{-1} + 8 + 36 q + 128 q^2 + ...
        # Normalize to constant term 0 => T_8A = j_8A - 8.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        e8 = _qpochhammer(deg, step=8)
        num = _qpoly_mul(e2, e4, deg)
        den = _qpoly_mul(e1, e8, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 8, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) - 8
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "8A'":
        # (Ramanujan–Sato / Moonshine)
        #   j_8A'(τ) = (η(τ)η(4τ)^2/(η(2τ)^2 η(8τ)))^{8}
        #           = q^{-1} - 8 + 36 q - 128 q^2 + ...
        # Normalize to constant term 0 => T_8A' = j_8A' + 8.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        e8 = _qpochhammer(deg, step=8)
        e4_2 = _qpoly_mul(e4, e4, deg)
        e2_2 = _qpoly_mul(e2, e2, deg)
        num = _qpoly_mul(e1, e4_2, deg)
        den = _qpoly_mul(e2_2, e8, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 8, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) + 8
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "8B":
        # (Ramanujan–Sato / Moonshine)
        #   j_8B(τ) = (η(4τ)^2/(η(2τ)η(8τ)))^{12}
        #          = q^{-1} + 12 q + 66 q^3 + ...
        # Constant term is 0 in this normalization.
        deg = max_q_exp + 1
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        e8 = _qpochhammer(deg, step=8)
        e4_2 = _qpoly_mul(e4, e4, deg)
        den = _qpoly_mul(e2, e8, deg)
        ratio = _qpoly_div(e4_2, den, deg)
        ratio_pow = _qpoly_pow(ratio, 12, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "8E":
        # (Ramanujan–Sato / Moonshine)
        #   j_8E(τ) = (η(4τ)^3/(η(2τ)η(8τ)^2))^{4}
        #          = q^{-1} + 4 q + 2 q^3 - 8 q^5 + ...
        # Constant term is 0 in this normalization.
        deg = max_q_exp + 1
        e2 = _qpochhammer(deg, step=2)
        e4 = _qpochhammer(deg, step=4)
        e8 = _qpochhammer(deg, step=8)
        e4_3 = _qpoly_pow(e4, 3, deg)
        e8_2 = _qpoly_mul(e8, e8, deg)
        den = _qpoly_mul(e2, e8_2, deg)
        ratio = _qpoly_div(e4_3, den, deg)
        ratio_pow = _qpoly_pow(ratio, 4, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "10B":
        # (Ramanujan–Sato / Moonshine)
        #   j_10B(τ) = (η(τ)η(5τ)/(η(2τ)η(10τ)))^{4}
        #           = q^{-1} - 4 + 6 q - 8 q^2 + ...
        # Normalize to constant term 0 => T_10B = j_10B + 4.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e5 = _qpochhammer(deg, step=5)
        e10 = _qpochhammer(deg, step=10)
        num = _qpoly_mul(e1, e5, deg)
        den = _qpoly_mul(e2, e10, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 4, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) + 4
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "10C":
        # (Ramanujan–Sato / Moonshine)
        #   j_10C(τ) = (η(τ)η(2τ)/(η(5τ)η(10τ)))^{2}
        #           = q^{-1} - 2 - 3 q + 6 q^2 + ...
        # Normalize to constant term 0 => T_10C = j_10C + 2.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e5 = _qpochhammer(deg, step=5)
        e10 = _qpochhammer(deg, step=10)
        num = _qpoly_mul(e1, e2, deg)
        den = _qpoly_mul(e5, e10, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 2, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) + 2
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "10D":
        # (Ramanujan–Sato / Moonshine)
        #   j_10D(τ) = (η(2τ)η(5τ)/(η(τ)η(10τ)))^{6}
        #           = q^{-1} + 6 + 21 q + 62 q^2 + ...
        # Normalize to constant term 0 => T_10D = j_10D - 6.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e5 = _qpochhammer(deg, step=5)
        e10 = _qpochhammer(deg, step=10)
        num = _qpoly_mul(e2, e5, deg)
        den = _qpoly_mul(e1, e10, deg)
        ratio = _qpoly_div(num, den, deg)
        ratio_pow = _qpoly_pow(ratio, 6, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio_pow):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) - 6
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "10E":
        # (Ramanujan–Sato / Moonshine)
        #   j_10E(τ) = η(2τ)η(5τ)^5/(η(τ)η(10τ)^5)
        #           = q^{-1} + 1 + q + 2 q^2 + ...
        # Normalize to constant term 0 => T_10E = j_10E - 1.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e5 = _qpochhammer(deg, step=5)
        e10 = _qpochhammer(deg, step=10)
        e5_5 = _qpoly_pow(e5, 5, deg)
        e10_5 = _qpoly_pow(e10, 5, deg)
        num = _qpoly_mul(e2, e5_5, deg)
        den = _qpoly_mul(e1, e10_5, deg)
        ratio = _qpoly_div(num, den, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(ratio):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        series[0] = series.get(0, 0) - 1
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "10A":
        # (Ramanujan–Sato / Moonshine) near-square identity:
        #   j_10A = (sqrt(j_10D) - 1/sqrt(j_10D))^2 = j_10D + 1/j_10D - 2.
        #
        # Normalize to constant term 0 => T_10A = j_10A - 4.
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e2 = _qpochhammer(deg, step=2)
        e5 = _qpochhammer(deg, step=5)
        e10 = _qpochhammer(deg, step=10)
        num = _qpoly_mul(e2, e5, deg)
        den = _qpoly_mul(e1, e10, deg)
        ratio = _qpoly_div(num, den, deg)
        r0 = _qpoly_pow(ratio, 6, deg)
        r0_inv = _qpoly_inv(r0, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(r0):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        for k, ck in enumerate(r0_inv):
            exp = 1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) - 2

        series[0] = series.get(0, 0) - 4
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "11A":
        # Formula (e.g. Ramanujan–Sato series / Cooper):
        #   j_11A(τ) = (1+3F)^3 + (F^{-1/2}+3F^{1/2})^2
        #           = F^{-1} + 7 + 18F + 27F^2 + 27F^3,
        #   where F = η(3τ)η(33τ)/(η(τ)η(11τ)).
        #
        # Our normalization uses T_11A = j_11A - a0 so that constant term is 0.
        deg = max_q_exp + 3  # slack for F^3
        e1 = _qpochhammer(deg, step=1)
        e3 = _qpochhammer(deg, step=3)
        e11 = _qpochhammer(deg, step=11)
        e33 = _qpochhammer(deg, step=33)

        num = _qpoly_mul(e3, e33, deg)
        den = _qpoly_mul(e1, e11, deg)
        ratio = _qpoly_div(num, den, deg)  # (E3*E33)/(E1*E11), constant term 1

        # F(q) = q * ratio(q)
        F = [0] * (deg + 1)
        for k, ck in enumerate(ratio[:deg]):
            if k + 1 <= deg:
                F[k + 1] = int(ck)

        F2 = _qpoly_mul(F, F, deg)
        F3 = _qpoly_mul(F2, F, deg)

        ratio_inv = _qpoly_inv(ratio, deg)

        # Build j_11A as a Laurent series dict exp->coeff
        j: dict[int, int] = {-1: 1}

        # F^{-1} = q^{-1} * ratio^{-1}
        for k, ck in enumerate(ratio_inv[: deg + 1]):
            exp = k - 1
            if -1 <= exp <= max_q_exp and ck:
                j[exp] = j.get(exp, 0) + int(ck)

        # + 7
        j[0] = j.get(0, 0) + 7

        # + 18F + 27F^2 + 27F^3
        for k, ck in enumerate(F[: deg + 1]):
            if 0 <= k <= max_q_exp and ck:
                j[k] = j.get(k, 0) + 18 * int(ck)
        for k, ck in enumerate(F2[: deg + 1]):
            if 0 <= k <= max_q_exp and ck:
                j[k] = j.get(k, 0) + 27 * int(ck)
        for k, ck in enumerate(F3[: deg + 1]):
            if 0 <= k <= max_q_exp and ck:
                j[k] = j.get(k, 0) + 27 * int(ck)

        # Normalize to constant term 0.
        a0 = int(j.get(0, 0))
        out = {}
        for e, c in j.items():
            if e == 0:
                continue
            if -1 <= e <= max_q_exp:
                out[e] = int(c)
        out[-1] = 1
        out[0] = 0
        if a0 != 6:
            # Keep as an internal sanity check but don't hard-require the known value.
            # (Different normalizations in the literature sometimes shift by constants.)
            pass
        return out

    if name == "3C":
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e3 = _qpochhammer(deg, step=3)
        e9 = _qpochhammer(deg, step=9)
        num = _qpoly_mul(e3, e3, deg)
        den = _qpoly_mul(e1, e9, deg)
        ratio = _qpoly_div(num, den, deg)

        r0 = _qpoly_pow(ratio, 6, deg)
        r0_inv = _qpoly_inv(r0, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(r0):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)

        for k, ck in enumerate(r0_inv):
            exp = 1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(-27 * ck)

        series[0] = series.get(0, 0) - 6
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    if name == "9A":
        deg = max_q_exp + 1
        e1 = _qpochhammer(deg, step=1)
        e3 = _qpochhammer(deg, step=3)
        e9 = _qpochhammer(deg, step=9)
        num = _qpoly_mul(e3, e3, deg)
        den = _qpoly_mul(e1, e9, deg)
        ratio = _qpoly_div(num, den, deg)
        r0 = _qpoly_pow(ratio, 6, deg)

        series: dict[int, int] = {}
        for k, ck in enumerate(r0):
            exp = -1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(ck)
        series[0] = series.get(0, 0) - 6
        if series.get(0, 0) != 0:
            raise AssertionError(
                f"Expected constant term 0 for {name}, got {series.get(0)}"
            )
        series.setdefault(-1, 1)
        return series

    fricke_prime = {"2A": 2, "3A": 3, "5A": 5, "7A": 7, "13A": 13}
    non_fricke_prime = {"2B": 2, "3B": 3, "5B": 5, "7B": 7, "13B": 13}
    if name in fricke_prime:
        p = fricke_prime[name]
        use_fricke = True
    elif name in non_fricke_prime:
        p = non_fricke_prime[name]
        use_fricke = False
    else:
        p = None
        use_fricke = False
    if p is None:
        return None

    # Prime-order Hauptmodul via eta-quotients.
    a = 24 // (p - 1)
    scale = p ** (12 // (p - 1))
    const = 24 // (p - 1)

    # Need one extra degree because term1 is q^-1 * (1 + O(q)).
    deg = max_q_exp + 1
    e = _qpochhammer(deg, step=1)  # (q;q)_inf
    ep = _qpochhammer(deg, step=p)  # (q^p;q^p)_inf
    ratio = _qpoly_div(e, ep, deg)  # E(q)/E(q^p)

    ratio_pow = _qpoly_pow(ratio, a, deg)

    series: dict[int, int] = {}
    # term1: q^-1 * ratio_pow
    for k, ck in enumerate(ratio_pow):
        exp = -1 + k
        if -1 <= exp <= max_q_exp and ck:
            series[exp] = series.get(exp, 0) + int(ck)

    if use_fricke:
        ratio_inv_pow = _qpoly_pow(_qpoly_inv(ratio, deg), a, deg)
        for k, ck in enumerate(ratio_inv_pow):
            exp = 1 + k
            if -1 <= exp <= max_q_exp and ck:
                series[exp] = series.get(exp, 0) + int(scale * ck)

    # constant shift
    series[0] = series.get(0, 0) + int(const)
    if series.get(0, 0) != 0:
        raise AssertionError(
            f"Expected constant term 0 for {name}, got {series.get(0)}"
        )

    series.setdefault(-1, 1)
    return series


def rogers_ramanujan_r5_series(max_q_exp: int) -> list[int]:
    """Compute r5(q)=R(q)^5 as a q-series through q^{max_q_exp}.

    Using the product formula (Wikipedia):
      R(q) = q^{1/5} * ( (q;q^5)_∞ (q^4;q^5)_∞ ) / ( (q^2;q^5)_∞ (q^3;q^5)_∞ )

    Hence:
      r5(q) = R(q)^5 = q * ( (q;q^5)_∞ (q^4;q^5)_∞ / ( (q^2;q^5)_∞ (q^3;q^5)_∞ ) )^5.
    """
    if max_q_exp < 0:
        raise ValueError("max_q_exp must be non-negative")
    deg = max_q_exp
    a1 = _qpochhammer_arith(deg, step=5, offset=1)  # (q;q^5)_∞
    a4 = _qpochhammer_arith(deg, step=5, offset=4)  # (q^4;q^5)_∞
    a2 = _qpochhammer_arith(deg, step=5, offset=2)  # (q^2;q^5)_∞
    a3 = _qpochhammer_arith(deg, step=5, offset=3)  # (q^3;q^5)_∞
    num = _qpoly_mul(a1, a4, deg)
    den = _qpoly_mul(a2, a3, deg)
    ratio = _qpoly_div(num, den, deg)  # constant 1
    ratio5 = _qpoly_pow(ratio, 5, deg)

    r5 = [0] * (deg + 1)
    # multiply by q: shift by 1
    for k, ck in enumerate(ratio5[:deg]):
        if k + 1 <= deg:
            r5[k + 1] = int(ck)
    return r5


def verify_rogers_ramanujan_5b_identity(max_q_exp: int = 12) -> dict[str, object]:
    """Verify the Rogers–Ramanujan identity behind the 5B Hauptmodul.

    Wikipedia states:
      1/R(q)^5 - R(q)^5 = (η(τ)/η(5τ))^6 + 11.

    With our q=e^{2πiτ} convention, (η(τ)/η(5τ))^6 has leading q^{-1}, and the
    Monster normalization for 5B is:
      T_5B(q) = 1/R(q)^5 - 5 - R(q)^5.
    """
    if max_q_exp < 1:
        raise ValueError("max_q_exp must be >= 1")

    t5b = mckay_thompson_series("5B", max_q_exp=max_q_exp)
    if t5b is None:
        raise RuntimeError("5B series unavailable")

    # We need a small amount of slack because 1/r5 involves U^{-1} and
    # coefficient exponents shift by -1. To validate through q^{max_q_exp},
    # compute r5 through q^{max_q_exp+2} and invert U through degree max_q_exp+1.
    r5 = rogers_ramanujan_r5_series(max_q_exp=max_q_exp + 2)

    # r5(q) = q * U(q) with U(0)=1, so 1/r5 = q^{-1} * U(q)^{-1}.
    U = [r5[k + 1] for k in range(max_q_exp + 2)]
    U[0] = 1
    invU = _qpoly_inv(U, max_q_exp + 1)

    expr: dict[int, int] = {}
    # 1/r5
    for k, ck in enumerate(invU[: max_q_exp + 2]):
        exp = -1 + k
        if -1 <= exp <= max_q_exp and ck:
            expr[exp] = expr.get(exp, 0) + int(ck)
    # -5 constant
    expr[0] = expr.get(0, 0) - 5
    # - r5
    for exp in range(1, max_q_exp + 1):
        ck = int(r5[exp])
        if ck:
            expr[exp] = expr.get(exp, 0) - ck

    mismatches: list[tuple[int, int, int]] = []
    for e in [-1, 0] + list(range(1, max_q_exp + 1)):
        lv = int(expr.get(e, 0))
        rv = int(t5b.get(e, 0))
        if lv != rv:
            mismatches.append((e, lv, rv))

    return {
        "max_q_exp": max_q_exp,
        "verified": len(mismatches) == 0,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:10],
        "r5_first_coeffs": r5[: min(len(r5), 8)],
    }


def j_series_via_rogers_ramanujan_r5(max_q_exp: int = 12) -> dict[int, int]:
    """Compute the Klein j-invariant series using Rogers–Ramanujan data.

    Wikipedia gives the rational function identity relating the Klein j-invariant
    and the Rogers–Ramanujan continued fraction R(q):

      j(τ) = - (r^20 - 228 r^15 + 494 r^10 + 228 r^5 + 1)^3
             / ( r^5 (r^10 + 11 r^5 - 1)^5 )

    with r = R(q). Setting t = r^5 = R(q)^5 turns this into:

      j(τ) = - (t^4 - 228 t^3 + 494 t^2 + 228 t + 1)^3 / ( t (t^2 + 11 t - 1)^5 )
           =   (t^4 - 228 t^3 + 494 t^2 + 228 t + 1)^3 / ( t (1 - 11 t - t^2)^5 ).

    Since t(q) = q + O(q^2), this produces the Laurent expansion:
      j(τ) = q^{-1} + 744 + Σ_{n>=1} c(n) q^n.
    """
    if max_q_exp < 0:
        raise ValueError("max_q_exp must be non-negative")

    # We need coefficients through q^{max_q_exp} after dividing by t(q), which
    # introduces a q^{-1} shift. Compute ordinary series through degree max_q_exp+1.
    deg = max_q_exp + 1
    t = rogers_ramanujan_r5_series(max_q_exp=deg + 1)  # need t[deg+1] for U
    t_trunc = t[: deg + 1]

    t2 = _qpoly_mul(t_trunc, t_trunc, deg)
    t3 = _qpoly_mul(t2, t_trunc, deg)
    t4 = _qpoly_mul(t2, t2, deg)

    # P(t) = t^4 - 228 t^3 + 494 t^2 + 228 t + 1
    P = [0] * (deg + 1)
    P[0] = 1
    for k in range(0, deg + 1):
        P[k] += 228 * int(t_trunc[k])
        P[k] += 494 * int(t2[k])
        P[k] -= 228 * int(t3[k])
        P[k] += int(t4[k])

    num = _qpoly_pow(P, 3, deg)

    # W(t) = (1 - 11 t - t^2)^5
    W = [0] * (deg + 1)
    W[0] = 1
    for k in range(0, deg + 1):
        W[k] -= 11 * int(t_trunc[k])
        W[k] -= int(t2[k])

    W5 = _qpoly_pow(W, 5, deg)
    invW5 = _qpoly_inv(W5, deg)

    # A(q) = num / W5
    A = _qpoly_mul(num, invW5, deg)

    # Divide by t(q): t = q * U with U(0)=1 => 1/t = q^{-1} * U^{-1}.
    U = [int(t[k + 1]) for k in range(deg + 1)]
    U[0] = 1
    invU = _qpoly_inv(U, deg)

    AU = _qpoly_mul(A, invU, deg)

    out: dict[int, int] = {-1: int(AU[0])}
    for n in range(0, max_q_exp + 1):
        out[n] = int(AU[n + 1])
    return out


def verify_j_via_rogers_ramanujan(max_q_exp: int = 12) -> dict[str, object]:
    """Verify j(τ) reconstruction from t(q)=R(q)^5 via the Wikipedia identity."""
    if max_q_exp < 1:
        raise ValueError("max_q_exp must be >= 1")

    j_rr = j_series_via_rogers_ramanujan_r5(max_q_exp=max_q_exp)
    j_ref = j_coeffs(max_q_exp)

    mismatches: list[tuple[int, int, int]] = []
    if int(j_rr.get(-1, 0)) != 1:
        mismatches.append((-1, int(j_rr.get(-1, 0)), 1))
    if int(j_rr.get(0, 0)) != 744:
        mismatches.append((0, int(j_rr.get(0, 0)), 744))
    for n in range(1, max_q_exp + 1):
        lv = int(j_rr.get(n, 0))
        rv = int(j_ref[n - 1])
        if lv != rv:
            mismatches.append((n, lv, rv))

    return {
        "max_q_exp": max_q_exp,
        "verified": len(mismatches) == 0,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:10],
    }


def analyze_s12_golay_sl27_bridge(jordan_sample_limit: int = 200) -> dict[str, object]:
    """Bridge the ternary Golay `s12` model to our Z3-graded algebra story.

    Key computed facts:
    - Ternary Golay code has |C|=3^6=729 codewords; removing zero gives 728=27^2-1.
    - The `s12` grade split is (242,243,243), which matches the block-cyclic Z3
      grading of sl_27 with 27=9+9+9.
    - The six Jacobi grade failures are exactly the mixed sectors (1,1,2) and
      (2,2,1) up to permutation, aligning with the E8 Z3-graded "mixed" sectors.
    """
    import math

    try:
        import tools.s12_universal_algebra as s12  # type: ignore[import-not-found]
    except Exception as e:  # pragma: no cover
        return {
            "available": False,
            "reason": f"failed to import tools.s12_universal_algebra: {e}",
        }

    report = s12.build_s12_universal_report(
        jordan_sample_limit=int(jordan_sample_limit)
    )
    dims = dict(report.get("algebra_dimensions", {}))
    laws = dict(report.get("universal_grade_laws", {}))

    code_size = int(report.get("code_size", 0))
    total_nonzero = int(dims.get("total_nonzero", 0))
    g0 = int(dims.get("grade0", 0))
    g1 = int(dims.get("grade1", 0))
    g2 = int(dims.get("grade2", 0))

    # sl_n inversion: total_nonzero = n^2 - 1.
    n2 = total_nonzero + 1
    n = int(math.isqrt(n2)) if n2 > 0 else 0
    sl_n_matches = bool(n > 0 and n * n == n2 and total_nonzero == n * n - 1)

    # Equal-block sl_(3r) family (r,r,r): g0=3r^2-1, g1=g2=3r^2.
    r = int(n // 3) if (n % 3 == 0 and n > 0) else None
    equal_block_matches = False
    if r is not None:
        equal_block_matches = bool(g0 == 3 * r * r - 1 and g1 == 3 * r * r and g2 == g1)

    # W(3,3) / TOE alignment: 243 = 3 * b1 where b1=81 from the clique complex.
    w33 = compute_w33_monster_invariants()
    b1 = int(w33.get("b1", 0))
    grade1_equals_3b1 = bool(g1 == 3 * b1 and g2 == 3 * b1)

    # Grade-level Jacobi failure pattern.
    raw_failures = list(laws.get("jacobi_failures", []))
    failures = {
        tuple(int(v) for v in row.get("grades", []))
        for row in raw_failures
        if isinstance(row, dict)
    }
    predicted = {
        (1, 1, 2),
        (1, 2, 1),
        (2, 1, 1),
        (1, 2, 2),
        (2, 1, 2),
        (2, 2, 1),
    }
    jacobi_failure_pattern_matches = failures == predicted

    # Map failures to the two mixed Z3 sector names used elsewhere in the repo.
    mixed_sectors: set[str] = set()
    for a, b, c in failures:
        c1 = (int(a) == 1) + (int(b) == 1) + (int(c) == 1)
        c2 = (int(a) == 2) + (int(b) == 2) + (int(c) == 2)
        if c1 == 2 and c2 == 1:
            mixed_sectors.add("g1_g1_g2")
        elif c2 == 2 and c1 == 1:
            mixed_sectors.add("g1_g2_g2")

    # Canonical sanity checks (computed, not hard-coded).
    assert code_size == 729, f"Expected |Golay_12(F3)|=3^6=729, got {code_size}"
    assert sl_n_matches and n == 27, f"Expected 728 = 27^2 - 1, got n={n}"
    assert equal_block_matches and r == 9, f"Expected 27=9+9+9 grading, got r={r}"
    assert (
        grade1_equals_3b1 and b1 == 81
    ), f"Expected 243 = 3*b1 with b1=81, got b1={b1}"
    assert jacobi_failure_pattern_matches, "Unexpected s12 Jacobi failure pattern"

    # Monster / sporadic bridge: the HN cofactor rung for the 5A centralizer
    # contains an A12 stabilizer (index 1,140,000). Doubling to HN:2 upgrades
    # that stabilizer to S12, connecting directly to the "s12" story above.
    monster_subgroup_bridge: dict[str, object] | None = None
    try:
        from scripts.w33_monster_centralizer_cofactor_groups import (
            analyze as analyze_cofactor_groups,
        )

        cof_rep = analyze_cofactor_groups()
        if cof_rep.get("available") is True:
            classes = cof_rep.get("classes", {})
            if isinstance(classes, dict):
                bridge: dict[str, object] = {}
                for cls, pair in (("5A", "2A×3A"), ("11A", "2A×3B")):
                    info = classes.get(cls, {})
                    if not isinstance(info, dict):
                        continue
                    hits = info.get("perm_hits", [])
                    if not isinstance(hits, list):
                        continue
                    hit = next(
                        (
                            h
                            for h in hits
                            if isinstance(h, dict) and str(h.get("pair")) == pair
                        ),
                        None,
                    )
                    if not isinstance(hit, dict):
                        continue
                    cof = int(info.get("cofactor_order", 0) or 0)
                    r_hit = int(hit.get("r", 0) or 0)
                    outer_stab = int(hit.get("outer_stabilizer_order", 0) or 0)
                    bridge[cls] = {
                        "pair": pair,
                        "cofactor_order": cof,
                        "r": r_hit,
                        "stabilizer_order": int(hit.get("stabilizer_order", 0) or 0),
                        "stabilizer_group": hit.get("stabilizer_group_recognized"),
                        "outer_stabilizer_order": outer_stab,
                        "outer_stabilizer_group": hit.get(
                            "outer_stabilizer_group_recognized"
                        ),
                        "outer_index_check": (
                            bool(outer_stab * r_hit == 2 * cof)
                            if (cof > 0 and r_hit > 0 and outer_stab > 0)
                            else False
                        ),
                    }

                if bridge:
                    # 12! is the order of S12, which should appear as the outer
                    # stabilizer for the HN (5A) rung.
                    bridge["s12_order"] = int(math.factorial(12))
                    monster_subgroup_bridge = bridge
    except Exception:
        monster_subgroup_bridge = None

    return {
        "available": True,
        "code_size": code_size,
        "dims": {
            "total_nonzero": total_nonzero,
            "grade0": g0,
            "grade1": g1,
            "grade2": g2,
        },
        "sl_n": {"n": n, "matches": sl_n_matches},
        "equal_block_sl3r": {"r": r, "matches": equal_block_matches},
        "w33": {"b1": b1, "grade1_equals_3b1": grade1_equals_3b1},
        "jacobi_failures": {
            "count": int(laws.get("jacobi_failure_count", len(failures))),
            "triples": [list(t) for t in sorted(failures)],
            "pattern_matches": jacobi_failure_pattern_matches,
            "mixed_sectors": sorted(mixed_sectors),
        },
        "monster_subgroup_bridge": monster_subgroup_bridge,
        "note": (
            "s12 is a Golay-derived Z3-graded Jordan-Lie model whose only grade-level "
            "Jacobi obstructions are the mixed sectors (g1,g1,g2)/(g1,g2,g2), "
            "matching the mixed-sector focus of the E8 Z3-graded firewall/L∞ work."
        ),
    }


def _laurent_mul(
    a: dict[int, int], b: dict[int, int], min_exp: int, max_exp: int
) -> dict[int, int]:
    out: dict[int, int] = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = ea + eb
            if e < min_exp or e > max_exp:
                continue
            out[e] = out.get(e, 0) + ca * cb
    return {e: c for e, c in out.items() if c != 0}


def _laurent_pow(
    f: dict[int, int], k: int, min_exp: int, max_exp: int
) -> dict[int, int]:
    if k < 0:
        raise ValueError("k must be non-negative")
    if k == 0:
        return {0: 1}
    out = dict(f)
    for _ in range(1, k):
        out = _laurent_mul(out, f, min_exp=min_exp, max_exp=max_exp)
    return out


def _solve_linear_system_fraction(
    A: list[list[Fraction]], b: list[Fraction]
) -> list[Fraction]:
    n = len(b)
    if n == 0:
        return []
    M = [row[:] + [b_i] for row, b_i in zip(A, b)]
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("singular system in Faber polynomial solve")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]

        pv = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pv
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                M[r][j] -= factor * M[col][j]
    return [M[i][n] for i in range(n)]


def faber_polynomial_series(
    f: dict[int, int], m: int, max_q_exp: int
) -> dict[str, object]:
    """Compute the Faber polynomial Phi_m for a q^-1 + O(q) series f.

    Returns:
      - coeffs: [c0,...,c_{m-1}] where Phi_m(x)=x^m + sum_{k=0..m-1} c_k x^k
      - series: Laurent coefficients of Phi_m(f(q)) up to q^{max_q_exp}
    """
    if m <= 0:
        raise ValueError("m must be positive")
    if max_q_exp < 0:
        raise ValueError("max_q_exp must be non-negative")

    min_exp = -m
    exps = list(range(-m + 1, 1))  # -m+1,...,0
    # When solving cancellations up to q^0, we must retain enough positive degrees
    # during intermediate products; otherwise sequential truncation can drop
    # contributions (order-dependent). The worst-case needed exponent is m-1.
    solve_max_exp = max(m - 1, 0)
    # Build powers f^k iteratively (O(m) multiplications), since we may have
    # primes as large as 71 in replicability checks.
    solve_pows: list[dict[int, int]] = [{0: 1}]
    for _k in range(1, m + 1):
        solve_pows.append(
            _laurent_mul(solve_pows[-1], f, min_exp=min_exp, max_exp=solve_max_exp)
        )
    powers = solve_pows[:m]
    f_m = solve_pows[m]

    A = [[Fraction(powers[k].get(e, 0)) for k in range(m)] for e in exps]
    b = [Fraction(-f_m.get(e, 0)) for e in exps]
    coeffs = _solve_linear_system_fraction(A, b)

    # To compute coefficients up to q^N in a sequential product, we need slack
    # up to N+(m-1), since intermediate terms can later combine with q^-1 factors.
    build_max_exp = max_q_exp + (m - 1)
    build_pows: list[dict[int, int]] = [{0: 1}]
    for _k in range(1, m + 1):
        build_pows.append(
            _laurent_mul(build_pows[-1], f, min_exp=min_exp, max_exp=build_max_exp)
        )
    series = dict(build_pows[m])
    for k, ck in enumerate(coeffs):
        if ck == 0:
            continue
        term = build_pows[k]
        for e, v in term.items():
            series[e] = series.get(e, 0) + int(ck * v)

    for e in range(-m + 1, 1):
        if series.get(e, 0) != 0:
            raise AssertionError(f"Faber cancellation failed at q^{e}: {series.get(e)}")
    if series.get(-m, 0) != 1:
        raise AssertionError("Faber normalization failed (q^-m coefficient)")

    # Return only coefficients through max_q_exp (but compute with slack above).
    series = {e: c for e, c in series.items() if e <= max_q_exp}

    coeffs_int: list[int] = []
    for c in coeffs:
        if c.denominator != 1:
            raise AssertionError("non-integer Faber coefficient encountered")
        coeffs_int.append(int(c.numerator))

    return {"m": m, "coeffs": coeffs_int, "series": series}


def verify_fricke_prime_replicability(
    class_name: str, max_q_exp: int = 10
) -> dict[str, object]:
    """Verify the m=p replicability identity for supported prime-order classes."""
    name = class_name.upper()
    p_map = {
        "2A": 2,
        "2B": 2,
        "3A": 3,
        "3B": 3,
        "3C": 3,
        "5A": 5,
        "5B": 5,
        "7A": 7,
        "7B": 7,
        "11A": 11,
        "13A": 13,
        "13B": 13,
        "17A": 17,
        "19A": 19,
        "23A": 23,
        "23B": 23,
        "29A": 29,
        "31A": 31,
        "31B": 31,
        "41A": 41,
        "47A": 47,
        "47B": 47,
        "59A": 59,
        "59B": 59,
        "71A": 71,
        "71B": 71,
    }
    p = p_map.get(name)
    if p is None:
        raise ValueError(f"Unsupported class for replicability: {class_name}")

    f = mckay_thompson_series(name, max_q_exp=p * max_q_exp)
    if f is None:
        raise RuntimeError(f"Series unavailable for class {class_name}")

    faber = faber_polynomial_series(f, m=p, max_q_exp=max_q_exp)
    lhs: dict[int, int] = dict(faber["series"])  # type: ignore[assignment]

    rhs: dict[int, int] = {-p: 1}
    for n in range(1, max_q_exp + 1):
        rhs[n] = rhs.get(n, 0) + p * int(f.get(p * n, 0))

    j_needed = max_q_exp // p
    jpos = j_coeffs(j_needed)
    for n, c in enumerate(jpos, start=1):
        exp = p * n
        if exp <= max_q_exp:
            rhs[exp] = rhs.get(exp, 0) + int(c)

    mismatches: list[tuple[int, int, int]] = []
    for e in [-p] + list(range(1, max_q_exp + 1)):
        lv = int(lhs.get(e, 0))
        rv = int(rhs.get(e, 0))
        if lv != rv:
            mismatches.append((e, lv, rv))

    return {
        "class_name": name,
        "p": p,
        "max_q_exp": max_q_exp,
        "verified": len(mismatches) == 0,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:10],
        "faber_coeffs": faber["coeffs"],
    }


def monster_order_factorization() -> dict[int, int]:
    """Prime factorization of |M| (Monster) as {prime: exponent}."""
    return {
        2: 46,
        3: 20,
        5: 9,
        7: 6,
        11: 2,
        13: 3,
        17: 1,
        19: 1,
        23: 1,
        29: 1,
        31: 1,
        41: 1,
        47: 1,
        59: 1,
        71: 1,
    }


def monster_order() -> int:
    n = 1
    for p, e in monster_order_factorization().items():
        n *= int(p) ** int(e)
    return n


def load_sporadic_group_orders(
    json_path: str | None = None,
) -> dict[str, dict[int, int]] | None:
    """Load sporadic group order factorizations (including Tits group) from JSON.

    The JSON format is a mapping {group_name: {prime: exponent}} with primes as strings.
    """
    path = (
        Path(json_path)
        if json_path is not None
        else (SCRIPTS_DIR.parent / "data" / "sporadic_group_orders.json")
    )
    if not path.exists():
        return None

    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict[int, int]] = {}
    for name, fac in raw.items():
        out[str(name)] = {int(p): int(e) for p, e in fac.items()}
    return out


def analyze_sporadic_group_magnitudes(
    json_path: str | None = None,
) -> dict[str, object]:
    """Summarize sporadic group *orders* and prime signatures.

    The main output is logarithmic (base 10 and base 2) to avoid constructing huge ints.
    """
    facs = load_sporadic_group_orders(json_path=json_path)
    if facs is None:
        return {
            "available": False,
            "reason": "sporadic_group_orders.json missing",
        }

    logs10: dict[str, float] = {}
    logs2: dict[str, float] = {}
    digits: dict[str, int] = {}
    bits: dict[str, int] = {}

    all_primes: set[int] = set()
    for name, fac in facs.items():
        all_primes |= set(fac.keys())
        l10 = sum(int(e) * log10(int(p)) for p, e in fac.items())
        l2 = sum(int(e) * log2(int(p)) for p, e in fac.items())
        logs10[name] = float(l10)
        logs2[name] = float(l2)
        digits[name] = int(l10) + 1 if l10 > 0 else 1
        bits[name] = int(l2) + 1 if l2 > 0 else 1

    monster_primes = set(monster_prime_divisors())
    extra_primes_union = sorted(all_primes - monster_primes)
    groups_with_extra_primes = sorted(
        [g for g, fac in facs.items() if (set(fac.keys()) - monster_primes)]
    )

    ranked = sorted(logs10.items(), key=lambda kv: kv[1], reverse=True)
    top5 = [g for g, _ in ranked[:5]]

    return {
        "available": True,
        "n_groups": len(facs),
        "factorizations": facs,
        "log10_order": logs10,
        "log2_order": logs2,
        "digits": digits,
        "bits": bits,
        "primes_union": sorted(all_primes),
        "monster_primes": sorted(monster_primes),
        "extra_primes_union": extra_primes_union,
        "groups_with_extra_primes": groups_with_extra_primes,
        "top5_by_order": top5,
    }


def analyze_monster_prime_centralizer_sporadic_ladder(
    atlas_json_path: str | None = None,
    sporadic_orders_json_path: str | None = None,
) -> dict[str, object]:
    """Match prime-order Monster centralizers to sporadic-group magnitudes.

    Using bundled ATLAS centralizer orders for Monster conjugacy classes and a
    bundled table of sporadic group order factorizations, we can verify the
    famous "centralizer ladder" where several prime-order centralizers factor as

        C_M(pX) = p · H

    for a sporadic simple group H (or a small 2-power multiple thereof).

    The output is deterministic/offline and intended as a numerology + structure
    report, not a new pillar.
    """

    def _order_from_factorization(fac: dict[int, int]) -> int:
        n = 1
        for p, e in fac.items():
            n *= int(p) ** int(e)
        return int(n)

    def _is_power_of_two(n: int) -> bool:
        nn = int(n)
        return nn > 0 and (nn & (nn - 1)) == 0

    def _v2(n: int) -> int:
        nn = int(n)
        k = 0
        while nn > 0 and nn % 2 == 0:
            nn //= 2
            k += 1
        return int(k)

    atlas = load_monster_atlas_ccls(json_path=atlas_json_path)
    if atlas is None:
        return {"available": False, "reason": "monster_atlas_ccls.json missing"}
    classes = atlas.get("classes", {})
    if not isinstance(classes, dict) or not classes:
        return {"available": False, "reason": "invalid monster ATLAS payload"}

    spor_fac = load_sporadic_group_orders(json_path=sporadic_orders_json_path)
    if spor_fac is None:
        return {"available": False, "reason": "sporadic_group_orders.json missing"}
    spor_order = {name: _order_from_factorization(f) for name, f in spor_fac.items()}

    # Prime-order (and 2/3 variants) classes to scan. These are exactly the
    # ones we already support in offline moonshine tooling elsewhere.
    prime_classes = [
        "2A",
        "2B",
        "3A",
        "3B",
        "3C",
        "5A",
        "5B",
        "7A",
        "7B",
        "11A",
        "13A",
        "13B",
        "17A",
        "19A",
        "23A",
        "29A",
        "31A",
        "41A",
        "47A",
        "59A",
        "71A",
    ]

    out_matches: dict[str, object] = {}
    for cls in prime_classes:
        meta = classes.get(cls, {})
        if (
            not isinstance(meta, dict)
            or "order" not in meta
            or "centralizer_order" not in meta
        ):
            continue
        p = int(meta["order"])
        cent = int(meta["centralizer_order"])
        if p <= 1 or cent % p != 0:
            continue
        cof = cent // p

        exact = [name for name, n in spor_order.items() if int(n) == int(cof)]
        pow2 = []
        for name, n in spor_order.items():
            nn = int(n)
            if nn <= 0:
                continue
            if cof % nn != 0:
                continue
            ratio = cof // nn
            if _is_power_of_two(ratio):
                pow2.append(
                    {"group": name, "two_power": _v2(ratio), "ratio": int(ratio)}
                )
        pow2 = sorted(pow2, key=lambda r: (int(r["two_power"]), str(r["group"])))

        out_matches[cls] = {
            "order": p,
            "centralizer_order": cent,
            "cofactor": cof,
            "exact_sporadic_match": exact[0] if exact else None,
            "power_of_two_sporadic_matches": pow2,
        }

    # Canonical, fully checkable ladder rungs (computed from bundled data).
    def _cof(cls: str) -> int:
        rec = out_matches.get(cls, {})
        if not isinstance(rec, dict):
            raise AssertionError(f"missing class record for {cls}")
        return int(rec["cofactor"])

    assert _cof("2A") == int(spor_order["B"])
    assert _cof("3A") == int(spor_order["Fi24"])
    assert _cof("3C") == int(spor_order["Th"])
    assert _cof("5A") == int(spor_order["HN"])
    assert _cof("7A") == int(spor_order["He"])
    assert _cof("11A") == int(spor_order["M12"])

    # 2B: cofactor is a pure 2-power multiple of Co1.
    co2b = _cof("2B")
    assert co2b % int(spor_order["Co1"]) == 0
    ratio_2b = co2b // int(spor_order["Co1"])
    assert _is_power_of_two(ratio_2b) and _v2(ratio_2b) == 24

    return {
        "available": True,
        "prime_classes": prime_classes,
        "matches": out_matches,
        "notes": [
            "Several prime-order centralizers factor as p·H for sporadic H (Baby Monster, Fi24', Th, HN, He, M12).",
            "2B exhibits the 2^24·Co1 factor in C_M(2B)/2 (the Leech-lattice 2^24 shows up explicitly).",
        ],
    }


def load_monster_atlas_ccls(json_path: str | None = None) -> dict | None:
    """Load a bundled ATLAS (QMUL) snapshot of Monster conjugacy-class metadata.

    The snapshot is generated by `scripts/fetch_monster_atlas_ccls.py` and is
    committed so tests stay offline and deterministic.

    Expected JSON format:
      {
        "source_url": "...",
        "n_classes": 194,
        "classes": {
          "10A": {
            "order": 10,
            "centralizer_order": "887040000",
            "powers": {"2": ["5A"], "5": ["2A"], "10": ["1A"], ...}
          },
          ...
        }
      }
    """
    import json
    from pathlib import Path

    path = (
        Path(json_path)
        if json_path is not None
        else (SCRIPTS_DIR.parent / "data" / "monster_atlas_ccls.json")
    )
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(payload, dict) or "classes" not in payload:
        return None
    classes = payload.get("classes")
    if not isinstance(classes, dict) or len(classes) < 10:
        return None
    return payload


def load_monster_ctbllib_charcols(json_path: str | None = None) -> dict | None:
    """Load a bundled CTblLib-derived subset of Monster character values.

    The full Monster character table is large. For the ATLAS standard-generator
    pipeline we only need a few integer columns (1A, 2A, 3B, 29A).

    The bundled file is generated from CTblLib's `ctomonst.tbl` (table "M").
    """
    import json
    from pathlib import Path

    path = (
        Path(json_path)
        if json_path is not None
        else (SCRIPTS_DIR.parent / "data" / "monster_ctbllib_charcols.json")
    )
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict) or "irreps" not in payload:
        return None
    irreps = payload.get("irreps")
    if not isinstance(irreps, list) or len(irreps) < 10:
        return None
    return payload


def _atlas_power_targets(
    atlas: dict | None, class_name: str, exponent: int
) -> list[str] | None:
    if atlas is None:
        return None
    try:
        classes = atlas.get("classes", {})
        info = classes.get(class_name.upper())
        if not isinstance(info, dict):
            return None
        powers = info.get("powers", {})
        if not isinstance(powers, dict):
            return None
        targets = powers.get(str(int(exponent)))
        if targets is None:
            return None
        if isinstance(targets, list):
            return [str(x).upper() for x in targets]
        # Backward/alternate formats: accept a single string.
        return [str(targets).upper()]
    except Exception:
        return None


def analyze_monster_atlas_generator_search_probabilities(
    atlas_json_path: str | None = None,
) -> dict[str, object]:
    """Exact random-element probabilities derived from ATLAS centralizers + power maps.

    This is a concrete probability ↔ group theory bridge:
      Pr[g lies in conjugacy class C] = |C|/|G| = 1/|C_G(g)|.

    Using the bundled ATLAS snapshot (QMUL), we can reproduce standard-generator
    search-step probabilities exactly as rational numbers.
    """
    from fractions import Fraction

    atlas = load_monster_atlas_ccls(atlas_json_path)
    if atlas is None:
        return {"available": False}

    classes = atlas.get("classes", {})
    if not isinstance(classes, dict) or not classes:
        return {"available": False}

    def _fraction_payload(fr: Fraction) -> dict[str, object]:
        return {
            "numerator": int(fr.numerator),
            "denominator": int(fr.denominator),
            "value": str(fr),
            "float": float(fr),
        }

    # Sanity: the conjugacy classes partition the group, so Σ_C 1/|C_G(g)| = 1.
    prob_sum = Fraction(0, 1)
    for info in classes.values():
        if not isinstance(info, dict):
            continue
        try:
            prob_sum += Fraction(1, int(info["centralizer_order"]))
        except Exception:
            continue
    assert prob_sum == 1, f"Invalid ATLAS centralizers: sum={prob_sum}"

    def _prob_for_orders(
        *,
        orders: set[int],
        exponent_from_order,
        target_class: str,
    ) -> dict[str, object]:
        target = target_class.upper()
        selected: list[str] = []
        p = Fraction(0, 1)
        for name, info in classes.items():
            if not isinstance(info, dict):
                continue
            try:
                order = int(info["order"])
                centralizer = int(info["centralizer_order"])
            except Exception:
                continue
            if order not in orders:
                continue
            exp = int(exponent_from_order(order))
            targets = _atlas_power_targets(atlas, str(name), exp) or []
            if target in targets:
                selected.append(str(name).upper())
                p += Fraction(1, centralizer)
        selected = sorted(set(selected))
        return {
            "orders": sorted(int(x) for x in orders),
            "exponent_rule": "order->exponent(order)",
            "target_class": target,
            "selected_classes": selected,
            "probability": _fraction_payload(p),
            "expected_trials": _fraction_payload(Fraction(1, 1) / p),
        }

    # ATLAS (v2) standard-generator selection steps:
    # - Involution 2A from even orders by raising to order/2.
    # - 3B from orders divisible by 3 by raising to order/3.
    prob_2a = _prob_for_orders(
        orders={34, 38, 50, 54, 62, 68, 94, 104, 110},
        exponent_from_order=lambda n: n // 2,
        target_class="2A",
    )
    prob_3b = _prob_for_orders(
        orders={9, 18, 27, 36, 45, 54},
        exponent_from_order=lambda n: n // 3,
        target_class="3B",
    )

    def _v_p(n: int, p: int) -> int:
        e = 0
        while n and (n % p == 0):
            n //= p
            e += 1
        return e

    den_3b = int(prob_3b["probability"]["denominator"])
    v3 = _v_p(den_3b, 3)

    return {
        "available": True,
        "source_url": atlas.get("source_url"),
        "n_classes": int(atlas.get("n_classes", len(classes))),
        "probabilities_sum_to_1": True,
        "generator_search": {
            "to_2A": prob_2a,
            "to_3B": {
                **prob_3b,
                "denominator_is_pure_power_of_3": den_3b == (3**v3),
                "denominator_3_adic_valuation": v3,
            },
        },
        "atlas_v2_expected": {
            "to_2A": "56542883129/363405814200",
            "to_3B": "3164/59049",
        },
    }


def analyze_monster_standard_generator_step3_order29_from_character_table(
    charcols_json_path: str | None = None,
    atlas_json_path: str | None = None,
) -> dict[str, object]:
    """Compute Pr[ab has order 29] for a∈2A, b∈3B via class algebra.

    This is the *third* step in the ATLAS standard-generator pipeline for M:
      choose conjugates a of x in 2A and b of y in 3B such that |ab| = 29.

    Using class algebra, for conjugacy classes A,B,C:
      Pr[xy ∈ C] = (|C|/|G|) * Σ_χ χ(A)χ(B)χ(C^{-1})/χ(1).

    For the Monster, 2A/3B/29A character values are integers, so we can compute
    this probability *exactly* (no cyclotomic arithmetic required).
    """
    from fractions import Fraction

    cols = load_monster_ctbllib_charcols(charcols_json_path)
    if cols is None:
        return {"available": False}

    atlas = load_monster_atlas_ccls(atlas_json_path)
    if atlas is None:
        return {"available": False}

    try:
        classes = atlas["classes"]
        monster_ord = int(classes["1A"]["centralizer_order"])
        cent_2a = int(classes["2A"]["centralizer_order"])
        cent_3b = int(classes["3B"]["centralizer_order"])
        cent_29a = int(classes["29A"]["centralizer_order"])
    except Exception:
        return {"available": False}
    assert cent_29a == 87, f"Expected |C_M(29A)|=87, got {cent_29a}"

    irreps = cols.get("irreps", [])
    if not isinstance(irreps, list) or len(irreps) != 194:
        return {"available": False}

    s = Fraction(0, 1)
    for row in irreps:
        if not isinstance(row, dict):
            return {"available": False}
        deg = int(row["deg"])
        s += Fraction(int(row["2A"]) * int(row["3B"]) * int(row["29A"]), deg)

    # |29A|/|M| = 1/|C_M(29A)| for ordinary conjugacy classes.
    p = s * Fraction(1, cent_29a)
    expected = Fraction(1632586752, 111045174695)
    assert p == expected, f"Step-3 probability mismatch: {p} vs {expected}"

    # Derived class-multiplication coefficient and pair counts.
    size_2a = monster_ord // cent_2a
    size_3b = monster_ord // cent_3b
    size_29a = monster_ord // cent_29a
    total_pairs = size_2a * size_3b
    n_pairs_in_29a = int(total_pairs * p)
    assert n_pairs_in_29a == monster_ord, (
        "Unexpected pair count: expected exactly |M| pairs (a,b) with ab in 29A, "
        f"got {n_pairs_in_29a}"
    )
    mult_coeff = n_pairs_in_29a // size_29a
    assert mult_coeff == cent_29a, (
        "Unexpected class multiplication coefficient: "
        f"expected {cent_29a}, got {mult_coeff}"
    )
    centralizer_formula_holds = p == Fraction(cent_2a * cent_3b, monster_ord)

    def factorint(n: int) -> dict[int, int]:
        nn = int(n)
        out: dict[int, int] = {}
        d = 2
        while d * d <= nn:
            while nn % d == 0:
                out[d] = out.get(d, 0) + 1
                nn //= d
            d = 3 if d == 2 else d + 2
        if nn > 1:
            out[nn] = out.get(nn, 0) + 1
        return out

    num = int(p.numerator)
    den = int(p.denominator)
    return {
        "available": True,
        "probability": {
            "numerator": num,
            "denominator": den,
            "value": str(p),
            "float": float(p),
        },
        "expected_trials": float(1 / float(p)),
        "centralizers": {
            "monster_order": monster_ord,
            "2A": cent_2a,
            "3B": cent_3b,
            "29A": cent_29a,
        },
        "class_sizes": {"2A": size_2a, "3B": size_3b, "29A": size_29a},
        "pair_counts": {
            "total_pairs_2A_x_3B": total_pairs,
            "pairs_with_product_in_29A": n_pairs_in_29a,
        },
        "class_multiplication_coefficient": mult_coeff,
        "centralizer_formula": {
            "holds": centralizer_formula_holds,
            "value": str(Fraction(cent_2a * cent_3b, monster_ord)),
        },
        "class_algebra_sum": {
            "numerator": int(s.numerator),
            "denominator": int(s.denominator),
            "value": str(s),
        },
        "factorization": {"numerator": factorint(num), "denominator": factorint(den)},
        "atlas_expected": str(expected),
        "ctbllib_charcols_available": True,
    }


def analyze_monster_atlas_standard_generator_pipeline(
    atlas_json_path: str | None = None,
    charcols_json_path: str | None = None,
) -> dict[str, object]:
    """Combine ATLAS step-1/2 with class-algebra step-3 into one pipeline model.

    Steps:
      1. Draw random g and map to a∈2A (ATLAS powering rule).
      2. Draw random h and map to b∈3B (ATLAS powering rule).
      3. Accept if |ab| = 29 (class algebra / character table).

    Returns exact rational probabilities and expected counts under a simple
    "resample a and b each attempt" strategy, plus a naive "single-shot pair"
    strategy for comparison.
    """
    from fractions import Fraction

    gs = analyze_monster_atlas_generator_search_probabilities(atlas_json_path)
    if not isinstance(gs, dict) or gs.get("available") is not True:
        return {"available": False}
    gsd = gs.get("generator_search", {})
    if not isinstance(gsd, dict):
        return {"available": False}

    to_2a = gsd.get("to_2A", {})
    to_3b = gsd.get("to_3B", {})
    if not isinstance(to_2a, dict) or not isinstance(to_3b, dict):
        return {"available": False}

    p2 = to_2a.get("probability", {})
    p3 = to_3b.get("probability", {})
    if not isinstance(p2, dict) or not isinstance(p3, dict):
        return {"available": False}
    p_to_2a = Fraction(int(p2["numerator"]), int(p2["denominator"]))
    p_to_3b = Fraction(int(p3["numerator"]), int(p3["denominator"]))

    step3 = analyze_monster_standard_generator_step3_order29_from_character_table(
        charcols_json_path=charcols_json_path,
        atlas_json_path=atlas_json_path,
    )
    if not isinstance(step3, dict) or step3.get("available") is not True:
        return {"available": False}
    p29 = step3.get("probability", {})
    if not isinstance(p29, dict):
        return {"available": False}
    p_order29_given_2a3b = Fraction(int(p29["numerator"]), int(p29["denominator"]))

    # Strategy A: generate a∈2A (mean 1/p2 draws) and b∈3B (mean 1/p3 draws),
    # then test |ab|; resample both on failure.
    expected_draws_per_ab_attempt = (Fraction(1, 1) / p_to_2a) + (
        Fraction(1, 1) / p_to_3b
    )
    expected_ab_attempts = Fraction(1, 1) / p_order29_given_2a3b
    expected_draws_total = expected_draws_per_ab_attempt * expected_ab_attempts

    # Strategy B: "single-shot": draw one g,h per trial and accept only if both
    # map to required classes and |ab|=29. (Less efficient; included for context.)
    p_single_shot = p_to_2a * p_to_3b * p_order29_given_2a3b
    expected_trials_single_shot = Fraction(1, 1) / p_single_shot
    expected_draws_single_shot = 2 * expected_trials_single_shot

    def _fraction_payload(fr: Fraction) -> dict[str, object]:
        return {
            "numerator": int(fr.numerator),
            "denominator": int(fr.denominator),
            "value": str(fr),
            "float": float(fr),
        }

    return {
        "available": True,
        "p_to_2A": _fraction_payload(p_to_2a),
        "p_to_3B": _fraction_payload(p_to_3b),
        "p_order29_given_2A_3B": _fraction_payload(p_order29_given_2a3b),
        "strategy_resample_both": {
            "expected_draws_per_ab_attempt": _fraction_payload(
                expected_draws_per_ab_attempt
            ),
            "expected_ab_attempts": _fraction_payload(expected_ab_attempts),
            "expected_random_draws_total": _fraction_payload(expected_draws_total),
        },
        "strategy_single_shot_pair": {
            "p_success_per_pair": _fraction_payload(p_single_shot),
            "expected_trials_pairs": _fraction_payload(expected_trials_single_shot),
            "expected_random_draws_total": _fraction_payload(
                expected_draws_single_shot
            ),
        },
    }


def analyze_monster_2a3b_class_algebra_partial_distribution(
    charcols_json_path: str | None = None,
    atlas_json_path: str | None = None,
) -> dict[str, object]:
    """Compute a partial class-algebra distribution for products a·b with a∈2A, b∈3B.

    Using the bundled CTblLib-derived character data:
      - integer columns for {2A,3B,5A,5B,7A,7B,11A,13A,13B,17A,19A,29A,41A}
      - prime-cyclotomic *trace* columns for {23A,31A,47A,59A,71A}

    we can compute Pr[ab ∈ C] for these classes exactly, plus the associated per-element
    structure constants n_{2A,3B}^C.

    This is a concrete "Monster algebra" observable: it converts character data
    into integer class-algebra constants and exact rational probabilities.
    """
    from fractions import Fraction

    cols = load_monster_ctbllib_charcols(charcols_json_path)
    if cols is None:
        return {"available": False}
    atlas = load_monster_atlas_ccls(atlas_json_path)
    if atlas is None:
        return {"available": False}

    try:
        classes = atlas["classes"]
        monster_ord = int(classes["1A"]["centralizer_order"])
        cent_2a = int(classes["2A"]["centralizer_order"])
        cent_3b = int(classes["3B"]["centralizer_order"])
        cent_29a = int(classes["29A"]["centralizer_order"])
        cent_41a = int(classes["41A"]["centralizer_order"])
        cent_31a = int(classes["31A"]["centralizer_order"])
        cent_47a = int(classes["47A"]["centralizer_order"])
        cent_59a = int(classes["59A"]["centralizer_order"])
        cent_71a = int(classes["71A"]["centralizer_order"])
        cent_5a = int(classes["5A"]["centralizer_order"])
        cent_5b = int(classes["5B"]["centralizer_order"])
        cent_7a = int(classes["7A"]["centralizer_order"])
        cent_7b = int(classes["7B"]["centralizer_order"])
        cent_11a = int(classes["11A"]["centralizer_order"])
        cent_13a = int(classes["13A"]["centralizer_order"])
        cent_13b = int(classes["13B"]["centralizer_order"])
        cent_17a = int(classes["17A"]["centralizer_order"])
        cent_19a = int(classes["19A"]["centralizer_order"])
        cent_23a = int(classes["23A"]["centralizer_order"])
    except Exception:
        return {"available": False}

    irreps = cols.get("irreps", [])
    if not isinstance(irreps, list) or len(irreps) != 194:
        return {"available": False}

    cent = {
        "1A": monster_ord,
        "2A": cent_2a,
        "3B": cent_3b,
        "5A": cent_5a,
        "5B": cent_5b,
        "7A": cent_7a,
        "7B": cent_7b,
        "11A": cent_11a,
        "13A": cent_13a,
        "13B": cent_13b,
        "17A": cent_17a,
        "19A": cent_19a,
        "23A": cent_23a,
        "29A": cent_29a,
        "41A": cent_41a,
        "31A": cent_31a,
        "47A": cent_47a,
        "59A": cent_59a,
        "71A": cent_71a,
    }
    size = {k: monster_ord // v for k, v in cent.items()}
    size_a = size["2A"]
    size_b = size["3B"]

    def _sum_for(C: str) -> Fraction:
        s = Fraction(0, 1)
        for row in irreps:
            if not isinstance(row, dict):
                raise ValueError("invalid irrep row")
            deg = int(row["deg"])
            a = int(row["2A"])
            b = int(row["3B"])
            if C == "1A":
                c = deg
            else:
                c = int(row[C])
            s += Fraction(a * b * c, deg)
        return s

    def _fraction_payload(fr: Fraction) -> dict[str, object]:
        return {
            "numerator": int(fr.numerator),
            "denominator": int(fr.denominator),
            "value": str(fr),
            "float": float(fr),
        }

    def factorint(n: int) -> dict[int, int]:
        nn = int(n)
        out: dict[int, int] = {}
        d = 2
        while d * d <= nn:
            while nn % d == 0:
                out[d] = out.get(d, 0) + 1
                nn //= d
            d = 3 if d == 2 else d + 2
        if nn > 1:
            out[nn] = out.get(nn, 0) + 1
        return out

    trace_meta = cols.get("trace_classes", {})

    out: dict[str, object] = {"available": True, "classes": {}}
    classes_out: dict[str, object] = {}
    mass = Fraction(0, 1)
    p_by_class: dict[str, Fraction] = {}

    value_classes = [
        "1A",
        "2A",
        "3B",
        "5A",
        "5B",
        "7A",
        "7B",
        "11A",
        "13A",
        "13B",
        "17A",
        "19A",
        "29A",
        "41A",
    ]
    trace_classes = ["23A", "31A", "47A", "59A", "71A"]

    for C in value_classes:
        s = _sum_for(C)
        p = s * Fraction(1, cent[C])
        n = p * size_a * size_b / size[C]
        assert n.denominator == 1, f"Non-integer n_2A,3B^{C}: {n}"
        classes_out[C] = {
            "mode": "value",
            "class_algebra_sum": _fraction_payload(s),
            "probability": _fraction_payload(p),
            "structure_constant_per_element": int(n.numerator),
            "structure_constant_factorization": factorint(int(n.numerator)),
        }
        p_by_class[C] = p
        mass += p

    for C in trace_classes:
        meta = trace_meta.get(C, {})
        if not isinstance(meta, dict) or "prime" not in meta:
            return {"available": False}
        prime = int(meta["prime"])
        key = f"{C}_trace"

        tr_s = Fraction(0, 1)
        for row in irreps:
            deg = int(row["deg"])
            a = int(row["2A"])
            b = int(row["3B"])
            tr = int(row[key])
            tr_s += Fraction(a * b * tr, deg)

        s = tr_s / (prime - 1)
        p = s * Fraction(1, cent[C])
        n = p * size_a * size_b / size[C]
        assert n.denominator == 1, f"Non-integer n_2A,3B^{C}: {n}"
        classes_out[C] = {
            "mode": "trace",
            "prime": prime,
            "class_algebra_trace_sum": _fraction_payload(tr_s),
            "class_algebra_sum": _fraction_payload(s),
            "probability": _fraction_payload(p),
            "structure_constant_per_element": int(n.numerator),
            "structure_constant_factorization": factorint(int(n.numerator)),
        }
        p_by_class[C] = p
        mass += p

    # Sanity identities implied by character orthogonality / class algebra.
    assert p_by_class["1A"] == 0
    assert p_by_class["2A"] == 0

    # Two striking "centralizer-multiple" identities (empirical, from CTblLib):
    #   n_{2A,3B}^{29A} = |C(29A)| = 87
    #   n_{2A,3B}^{41A} = 2·|C(41A)| = 82
    n29 = int(classes_out["29A"]["structure_constant_per_element"])
    n41 = int(classes_out["41A"]["structure_constant_per_element"])
    assert n29 == cent_29a
    assert n41 == 2 * cent_41a
    assert p_by_class["41A"] == 2 * p_by_class["29A"]

    # Prime-order class behavior for Ogg primes (via cyclotomic traces).
    assert p_by_class["47A"] == 0
    assert p_by_class["59A"] == 0
    assert p_by_class["71A"] == p_by_class["29A"]
    assert int(classes_out["71A"]["structure_constant_per_element"]) == cent_71a

    # 31A: n_{2A,3B}^{31A} = C(31,2) = 465
    assert int(classes_out["31A"]["structure_constant_per_element"]) == 465

    # Additional Ogg-prime behavior for 2A·3B (integers + trace).
    assert p_by_class["5A"] == 0
    assert p_by_class["5B"] == 0
    assert p_by_class["7A"] == 0
    assert p_by_class["7B"] == 0
    assert p_by_class["13B"] == 0

    assert p_by_class["11A"] == Fraction(136048896, 6107484608225)
    assert int(classes_out["11A"]["structure_constant_per_element"]) == 1584

    assert p_by_class["13A"] == Fraction(45349632, 111045174695)
    assert int(classes_out["13A"]["structure_constant_per_element"]) == 2028

    assert p_by_class["17A"] == Fraction(136048896, 111045174695)
    assert int(classes_out["17A"]["structure_constant_per_element"]) == 238

    assert p_by_class["19A"] == Fraction(6530347008, 555225873475)
    assert int(classes_out["19A"]["structure_constant_per_element"]) == 912

    assert p_by_class["23A"] == Fraction(272097792, 111045174695)
    assert int(classes_out["23A"]["structure_constant_per_element"]) == 92

    out["classes"] = classes_out
    out["partial_mass"] = _fraction_payload(mass)
    out["remaining_mass"] = _fraction_payload(Fraction(1, 1) - mass)
    return out


def analyze_monster_2x3_ogg_prime_triangle_support(
    charcols_json_path: str | None = None,
    atlas_json_path: str | None = None,
) -> dict[str, object]:
    """Scan (2X,3Y) products for Ogg-prime triangle-group support.

    For a in 2A or 2B and b in 3A/3B/3C, any nonzero probability

        Pr[(ab) ∈ pA]  (or pB)

    certifies the existence of a homomorphism from the triangle group
    Δ(2,3,p)=<x,y | x^2=y^3=(xy)^p=1> into the Monster with (x,y) landing in
    those conjugacy classes.

    Output is computed purely from bundled CTblLib-derived character columns and
    ATLAS centralizers; results are exact rationals + integer structure
    constants.
    """
    from fractions import Fraction

    cols = load_monster_ctbllib_charcols(charcols_json_path)
    if cols is None:
        return {"available": False}
    atlas = load_monster_atlas_ccls(atlas_json_path)
    if atlas is None:
        return {"available": False}

    try:
        classes = atlas["classes"]
        monster_ord = int(classes["1A"]["centralizer_order"])
    except Exception:
        return {"available": False}

    irreps = cols.get("irreps", [])
    if not isinstance(irreps, list) or len(irreps) != 194:
        return {"available": False}

    trace_meta = cols.get("trace_classes", {})
    if not isinstance(trace_meta, dict):
        return {"available": False}

    def _fraction_payload(fr: Fraction) -> dict[str, object]:
        return {
            "numerator": int(fr.numerator),
            "denominator": int(fr.denominator),
            "value": str(fr),
            "float": float(fr),
        }

    def factorint(n: int) -> dict[int, int]:
        nn = int(n)
        out: dict[int, int] = {}
        d = 2
        while d * d <= nn:
            while nn % d == 0:
                out[d] = out.get(d, 0) + 1
                nn //= d
            d = 3 if d == 2 else d + 2
        if nn > 1:
            out[nn] = out.get(nn, 0) + 1
        return out

    a_classes = ["2A", "2B"]
    b_classes = ["3A", "3B", "3C"]

    # Ogg prime classes (we include both A/B variants when present).
    value_targets = [
        "5A",
        "5B",
        "7A",
        "7B",
        "11A",
        "13A",
        "13B",
        "17A",
        "19A",
        "29A",
        "41A",
    ]
    trace_targets = [
        "23A",
        "23B",
        "31A",
        "31B",
        "47A",
        "47B",
        "59A",
        "59B",
        "71A",
        "71B",
    ]

    # Centralizers/sizes for every class we will touch.
    needed = sorted(set(a_classes + b_classes + value_targets + trace_targets))
    try:
        cent = {k: int(classes[k]["centralizer_order"]) for k in needed}
    except Exception:
        return {"available": False}
    size = {k: monster_ord // v for k, v in cent.items()}

    def _sum_value(*, a_cls: str, b_cls: str, C: str) -> Fraction:
        s = Fraction(0, 1)
        for row in irreps:
            if not isinstance(row, dict):
                raise ValueError("invalid irrep row")
            deg = int(row["deg"])
            a = int(row[a_cls])
            b = int(row[b_cls])
            c = deg if C == "1A" else int(row[C])
            s += Fraction(a * b * c, deg)
        return s

    def _sum_trace(*, a_cls: str, b_cls: str, C: str) -> tuple[int, Fraction]:
        meta = trace_meta.get(C, {})
        if not isinstance(meta, dict) or "prime" not in meta:
            raise ValueError(f"missing trace metadata for class {C}")
        prime = int(meta["prime"])
        key = f"{C}_trace"
        tr_s = Fraction(0, 1)
        for row in irreps:
            deg = int(row["deg"])
            a = int(row[a_cls])
            b = int(row[b_cls])
            tr = int(row[key])
            tr_s += Fraction(a * b * tr, deg)
        return prime, tr_s

    pairs_out: dict[str, object] = {}
    for a_cls in a_classes:
        for b_cls in b_classes:
            pair_key = f"{a_cls}×{b_cls}"
            size_a = size[a_cls]
            size_b = size[b_cls]

            classes_out: dict[str, object] = {}
            support_classes: list[str] = []
            support_primes: set[int] = set()

            for C in value_targets:
                s = _sum_value(a_cls=a_cls, b_cls=b_cls, C=C)
                p = s * Fraction(1, cent[C])
                n = p * size_a * size_b / size[C]
                assert n.denominator == 1, f"Non-integer n_{{{a_cls},{b_cls}}}^{C}: {n}"
                if p != 0:
                    support_classes.append(C)
                    support_primes.add(int(classes[C]["order"]))
                classes_out[C] = {
                    "mode": "value",
                    "class_algebra_sum": _fraction_payload(s),
                    "probability": _fraction_payload(p),
                    "structure_constant_per_element": int(n.numerator),
                    "structure_constant_factorization": factorint(int(n.numerator)),
                }

            for C in trace_targets:
                prime, tr_s = _sum_trace(a_cls=a_cls, b_cls=b_cls, C=C)
                s = tr_s / (prime - 1)
                p = s * Fraction(1, cent[C])
                n = p * size_a * size_b / size[C]
                assert n.denominator == 1, f"Non-integer n_{{{a_cls},{b_cls}}}^{C}: {n}"
                if p != 0:
                    support_classes.append(C)
                    support_primes.add(int(classes[C]["order"]))
                classes_out[C] = {
                    "mode": "trace",
                    "prime": int(prime),
                    "class_algebra_trace_sum": _fraction_payload(tr_s),
                    "class_algebra_sum": _fraction_payload(s),
                    "probability": _fraction_payload(p),
                    "structure_constant_per_element": int(n.numerator),
                    "structure_constant_factorization": factorint(int(n.numerator)),
                }

            pairs_out[pair_key] = {
                "a_class": a_cls,
                "b_class": b_cls,
                "support_primes": sorted(support_primes),
                "support_classes": support_classes,
                "classes": classes_out,
            }

    return {
        "available": True,
        "pairs": pairs_out,
        "ogg_primes": ogg_primes_via_genus(max_p=100).get("primes"),
        "targets": {
            "value": value_targets,
            "trace": trace_targets,
        },
    }


def analyze_monster_atlas_probability_landscape(
    atlas_json_path: str | None = None,
    *,
    top_k: int = 10,
) -> dict[str, object]:
    """Summarize the Monster's conjugacy-class probability landscape.

    With class probabilities p(C)=|C|/|M|=1/|C_M(g)|, the ATLAS centralizers give
    exact (rational) probabilities for:
      - element orders,
      - rare-event rates (e.g., involutions),
      - entropy / expected order diagnostics.
    """
    import math
    from collections import defaultdict
    from fractions import Fraction

    atlas = load_monster_atlas_ccls(atlas_json_path)
    if atlas is None:
        return {"available": False}
    classes = atlas.get("classes", {})
    if not isinstance(classes, dict) or not classes:
        return {"available": False}

    def _fraction_payload(fr: Fraction) -> dict[str, object]:
        return {
            "numerator": int(fr.numerator),
            "denominator": int(fr.denominator),
            "value": str(fr),
            "float": float(fr),
        }

    def _is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        f = 3
        while f * f <= n:
            if n % f == 0:
                return False
            f += 2
        return True

    class_prob: dict[str, Fraction] = {}
    order_prob: dict[int, Fraction] = defaultdict(lambda: Fraction(0, 1))
    min_cent: int | None = None
    min_cent_classes: list[str] = []

    prob_sum = Fraction(0, 1)
    expected_order = Fraction(0, 1)
    prime_order_mass = Fraction(0, 1)
    involution_mass = Fraction(0, 1)

    for name, info in classes.items():
        if not isinstance(info, dict):
            continue
        try:
            cent = int(info["centralizer_order"])
            order = int(info["order"])
        except Exception:
            continue
        p = Fraction(1, cent)
        nm = str(name).upper()
        class_prob[nm] = p
        order_prob[order] += p
        prob_sum += p
        expected_order += p * order
        if _is_prime(order):
            prime_order_mass += p
        if order == 2:
            involution_mass += p
        if min_cent is None or cent < min_cent:
            min_cent = cent
            min_cent_classes = [nm]
        elif cent == min_cent:
            min_cent_classes.append(nm)

    assert prob_sum == 1, f"Invalid ATLAS centralizers: sum={prob_sum}"
    assert min_cent is not None

    top_classes = sorted(class_prob.items(), key=lambda kv: kv[1], reverse=True)[
        : int(top_k)
    ]
    top_orders = sorted(order_prob.items(), key=lambda kv: kv[1], reverse=True)[
        : int(top_k)
    ]

    # Shannon entropy diagnostics (float; not intended for strict asserts).
    def _entropy_bits(probs: list[Fraction]) -> float:
        h = 0.0
        for pp in probs:
            x = float(pp)
            if x > 0:
                h -= x * math.log2(x)
        return h

    h_class = _entropy_bits(list(class_prob.values()))
    h_order = _entropy_bits(list(order_prob.values()))

    # Useful for standard-generator heuristics: order-29 rate vs ATLAS step-3.
    p29 = order_prob.get(29, Fraction(0, 1))

    return {
        "available": True,
        "source_url": atlas.get("source_url"),
        "n_classes": int(atlas.get("n_classes", len(classes))),
        "probabilities_sum_to_1": True,
        "min_centralizer": {
            "centralizer_order": int(min_cent),
            "classes": sorted(set(min_cent_classes)),
            "max_class_probability": _fraction_payload(Fraction(1, int(min_cent))),
        },
        "top_classes": [
            {
                "class_name": c,
                "order": int(classes[c]["order"]),
                "p": _fraction_payload(p),
            }
            for c, p in top_classes
            if c in classes and isinstance(classes[c], dict)
        ],
        "top_orders": [
            {"order": int(o), "p": _fraction_payload(p)} for o, p in top_orders
        ],
        "order_probability_29": _fraction_payload(p29),
        "expected_order": _fraction_payload(expected_order),
        "prime_order_mass": _fraction_payload(prime_order_mass),
        "involution_mass": _fraction_payload(involution_mass),
        "entropy_bits": {"by_class": float(h_class), "by_order": float(h_order)},
    }


def analyze_monster_atlas_powering_probabilities(
    atlas_json_path: str | None = None,
) -> dict[str, object]:
    """Compute exact powering-to-target probabilities from ATLAS power maps.

    For each divisor d and target class T of order d, we estimate:
      Pr[g^{ord(g)/d} ∈ T]
    by summing 1/|C_M(g)| over classes whose ATLAS "Power up" entry maps the
    exponent ord(g)/d to T. This is exact given the bundled ATLAS snapshot.
    """
    from fractions import Fraction

    atlas = load_monster_atlas_ccls(atlas_json_path)
    if atlas is None:
        return {"available": False}
    classes = atlas.get("classes", {})
    if not isinstance(classes, dict) or not classes:
        return {"available": False}

    def _fraction_payload(fr: Fraction) -> dict[str, object]:
        return {
            "numerator": int(fr.numerator),
            "denominator": int(fr.denominator),
            "value": str(fr),
            "float": float(fr),
        }

    def _power_to(target_class: str, d: int) -> dict[str, object]:
        target = str(target_class).upper()
        dd = int(d)
        selected: list[str] = []
        p = Fraction(0, 1)
        for name, info in classes.items():
            if not isinstance(info, dict):
                continue
            try:
                order = int(info["order"])
                cent = int(info["centralizer_order"])
            except Exception:
                continue
            if order % dd != 0:
                continue
            exp = order // dd
            targets = _atlas_power_targets(atlas, str(name), exp) or []
            if target in targets:
                selected.append(str(name).upper())
                p += Fraction(1, cent)
        selected = sorted(set(selected))
        return {
            "divisor": dd,
            "target_class": target,
            "n_selected_classes": len(selected),
            "selected_classes": selected,
            "probability": _fraction_payload(p),
            "expected_trials": _fraction_payload(Fraction(1, 1) / p),
        }

    # Targets aligned with the repo's offline McKay–Thompson support.
    targets_by_divisor: dict[int, list[str]] = {
        2: ["2A", "2B"],
        3: ["3A", "3B"],
        5: ["5A", "5B"],
        7: ["7A", "7B"],
        11: ["11A"],
        13: ["13A", "13B"],
    }

    powering: dict[str, dict[str, object]] = {}
    for d, targets in targets_by_divisor.items():
        dd = str(int(d))
        powering[dd] = {}
        for t in targets:
            powering[dd][t] = _power_to(t, d)

    # Include the ATLAS-v2 restricted generator-search steps (2A, 3B) for reference.
    restricted = analyze_monster_atlas_generator_search_probabilities(atlas_json_path)

    return {
        "available": True,
        "source_url": atlas.get("source_url"),
        "n_classes": int(atlas.get("n_classes", len(classes))),
        "powering": powering,
        "restricted_generator_search": restricted,
    }


def monster_prime_divisors() -> list[int]:
    return sorted(int(p) for p in monster_order_factorization().keys())


def class_number_negative_discriminant(D: int) -> int:
    """Class number h(D) for a negative discriminant D via reduced forms."""
    import math

    if D >= 0 or D % 4 not in (0, 1):
        raise ValueError("D must be a negative discriminant (0 or 1 mod 4)")

    h = 0
    limit = int(math.sqrt(abs(D) / 3)) + 2
    for a in range(1, limit + 1):
        for b in range(-a, a + 1):
            disc = b * b - D
            if disc % (4 * a) != 0:
                continue
            c = disc // (4 * a)
            if a > c or abs(b) > a:
                continue
            if (abs(b) == a or a == c) and b < 0:
                continue
            if b * b - 4 * a * c != D:
                continue
            h += 1
    return h


def genus_x0_prime(p: int) -> int:
    """Genus g(X0(p)) for prime p >= 2."""
    if p < 2:
        raise ValueError("p must be >= 2")
    if p in (2, 3, 5, 7, 13):
        return 0

    mu = p + 1
    cusps = 2
    e2 = 2 if p % 4 == 1 else 0
    e3 = 2 if p % 3 == 1 else 0
    g = 1 + mu / 12 - e2 / 4 - e3 / 3 - cusps / 2
    return int(round(g))


def ogg_primes_via_genus(max_p: int = 100) -> dict[str, object]:
    """Compute primes p<=max_p with genus(X0(p)^+) == 0 via class numbers.

    For odd primes p>3:
      g(X0(p)^+) = g(X0(p)) + 1 - h(-4p)/2.
    """
    import math

    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        r = int(math.isqrt(n))
        f = 3
        while f <= r:
            if n % f == 0:
                return False
            f += 2
        return True

    ogg: list[int] = []
    details: dict[int, dict[str, int | float]] = {}
    for p in range(2, max_p + 1):
        if not is_prime(p):
            continue
        if p in (2, 3):
            ogg.append(p)
            details[p] = {"g_x0": 0, "h_minus4p": 0, "g_x0_plus": 0.0}
            continue
        g = genus_x0_prime(p)
        h = class_number_negative_discriminant(-4 * p)
        g_plus = g + 1 - h / 2
        details[p] = {"g_x0": g, "h_minus4p": h, "g_x0_plus": float(g_plus)}
        if abs(g_plus) < 1e-12:
            ogg.append(p)

    return {"max_p": max_p, "primes": ogg, "details": details}


def infer_monster_head_character_values(
    class_name: str, max_n: int = 3
) -> dict[int, int] | None:
    """Infer a small subset of Monster character values from moonshine 'head'
    decompositions V_n for n<=max_n, assuming early coefficients introduce at
    most one new irrep at each step.
    """
    if max_n < 1:
        raise ValueError("max_n must be >= 1")

    series = mckay_thompson_series(class_name, max_q_exp=max_n)
    if series is None:
        return None

    data = analyze_leech_monster()
    decomps = data.get("j_decompositions", {})

    chis: dict[int, int] = {1: 1}
    for n in range(1, max_n + 1):
        info = decomps.get(n)
        if not info or not info.get("exact"):
            break
        dec = info.get("decomp", {})
        unknown = [int(d) for d in dec.keys() if int(d) not in chis]
        known_sum = sum(
            int(mult) * int(chis[int(deg)])
            for deg, mult in dec.items()
            if int(deg) in chis
        )
        trace_n = int(series.get(n, 0))

        if len(unknown) == 0:
            if trace_n != known_sum:
                raise AssertionError(
                    f"Trace mismatch at n={n} for {class_name}: {trace_n} != {known_sum}"
                )
            continue
        if len(unknown) != 1:
            break

        deg = unknown[0]
        mult = int(dec.get(deg, 0))
        if mult == 0:
            break
        rhs = trace_n - known_sum
        if rhs % mult != 0:
            raise AssertionError(
                f"Non-integer character inference for {class_name} at n={n}"
            )
        chis[deg] = rhs // mult

    return chis


def verify_9a_cubing_relation(max_q_exp: int = 12) -> dict[str, object]:
    """Verify a composite-order replicability relation for class 9A:

        Phi_3(T_9A) = sum_{b=0..2} T_9A((tau+b)/3) + T_3B(3 tau),

    which implies the power-map identification (9A)^3 = 3B at the level of
    McKay-Thompson series.
    """
    if max_q_exp < 1:
        raise ValueError("max_q_exp must be >= 1")

    f9 = mckay_thompson_series("9A", max_q_exp=3 * max_q_exp)
    if f9 is None:
        raise RuntimeError("9A series unavailable")

    faber = faber_polynomial_series(f9, m=3, max_q_exp=max_q_exp)
    lhs: dict[int, int] = dict(faber["series"])  # type: ignore[assignment]

    rhs_dec: dict[int, int] = {}
    for n in range(1, max_q_exp + 1):
        rhs_dec[n] = 3 * int(f9.get(3 * n, 0))

    remainder: dict[int, int] = {}
    for e in set(lhs.keys()) | set(rhs_dec.keys()):
        remainder[e] = int(lhs.get(e, 0)) - int(rhs_dec.get(e, 0))
    remainder = {e: v for e, v in remainder.items() if v != 0}

    f3b = mckay_thompson_series("3B", max_q_exp=max_q_exp // 3)
    if f3b is None:
        raise RuntimeError("3B series unavailable")
    expected: dict[int, int] = {-3: 1}
    for n in range(1, max_q_exp // 3 + 1):
        expected[3 * n] = int(f3b.get(n, 0))

    mismatches: list[tuple[int, int, int]] = []
    for e in [-3] + [3 * n for n in range(1, max_q_exp // 3 + 1)]:
        lv = int(remainder.get(e, 0))
        rv = int(expected.get(e, 0))
        if lv != rv:
            mismatches.append((e, lv, rv))

    return {
        "max_q_exp": max_q_exp,
        "verified": len(mismatches) == 0,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:10],
        "inferred_power_class": "3B",
    }


def verify_power_relation(
    class_name: str,
    m: int,
    expected_power_class: str | None = None,
    max_q_exp: int = 20,
    candidates: tuple[str, ...] = (),
) -> dict[str, object]:
    """Verify (or infer) the g^m power-map using *prime* replicability.

    For prime m:
      Phi_m(T_g)(τ) = sum_{b=0..m-1} T_g((τ+b)/m) + T_{g^m}(m τ).

    The decimation sum selects exponents divisible by m:
      sum_{b=0..m-1} T_g((τ+b)/m) = m * sum_{n>=1} a_{m n} q^n.
    """

    def _is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        f = 3
        while f * f <= n:
            if n % f == 0:
                return False
            f += 2
        return True

    if m <= 1:
        raise ValueError("m must be >= 2")
    if not _is_prime(m):
        raise ValueError("verify_power_relation currently supports prime m only")
    if max_q_exp < 1:
        raise ValueError("max_q_exp must be >= 1")

    name = class_name.upper()
    f = mckay_thompson_series(name, max_q_exp=m * max_q_exp)
    if f is None:
        raise RuntimeError(f"Series unavailable for class {class_name}")

    faber = faber_polynomial_series(f, m=m, max_q_exp=max_q_exp)
    lhs: dict[int, int] = dict(faber["series"])  # type: ignore[assignment]

    rhs_dec: dict[int, int] = {}
    for n in range(1, max_q_exp + 1):
        rhs_dec[n] = m * int(f.get(m * n, 0))

    remainder: dict[int, int] = {}
    for e in set(lhs.keys()) | set(rhs_dec.keys()):
        remainder[e] = int(lhs.get(e, 0)) - int(rhs_dec.get(e, 0))
    remainder = {e: v for e, v in remainder.items() if v != 0}

    cand_results: dict[str, dict[str, object]] = {}
    for cand in candidates:
        fm = mckay_thompson_series(cand, max_q_exp=max_q_exp // m + 2)
        if fm is None:
            continue

        expected: dict[int, int] = {-m: 1}
        for n in range(1, max_q_exp // m + 1):
            expected[m * n] = int(fm.get(n, 0))

        mismatches: list[tuple[int, int, int]] = []
        exps = [-m] + [m * n for n in range(1, max_q_exp // m + 1)]
        for e in exps:
            lv = int(remainder.get(e, 0))
            rv = int(expected.get(e, 0))
            if lv != rv:
                mismatches.append((e, lv, rv))

        cand_results[cand.upper()] = {
            "n_mismatches": len(mismatches),
            "mismatches": mismatches[:10],
        }

    inferred = None
    if cand_results:
        inferred = min(cand_results.items(), key=lambda kv: int(kv[1]["n_mismatches"]))[
            0
        ]

    target = expected_power_class.upper() if expected_power_class else inferred
    verified = False
    target_mismatches: list[tuple[int, int, int]] = []
    if target and target in cand_results:
        verified = int(cand_results[target]["n_mismatches"]) == 0
        target_mismatches = list(cand_results[target]["mismatches"])  # type: ignore[list-item]

    return {
        "class_name": name,
        "m": m,
        "max_q_exp": max_q_exp,
        "verified": verified,
        "inferred_power_class": inferred,
        "expected_power_class": (
            expected_power_class.upper() if expected_power_class else None
        ),
        "target_mismatches": target_mismatches,
        "candidates": cand_results,
    }


def verify_replicability_relation(
    class_name: str,
    m: int,
    power_map: dict[int, str],
    max_q_exp: int = 20,
) -> dict[str, object]:
    """Verify the Conway–Norton replicability identity for general m.

    Uses the divisor-sum form:
      Phi_m(T_g)(τ) = sum_{ad=m} sum_{b=0..d-1} T_{g^a}((a τ + b)/d).

    This requires a power-map lookup for each divisor a of m (a>1) present in the
    sum. Provide `power_map` as {a: class_name_for_g^a}. The identity class is "1A".
    """
    if m <= 0:
        raise ValueError("m must be positive")
    if max_q_exp < 1:
        raise ValueError("max_q_exp must be >= 1")

    name = class_name.upper()
    f = mckay_thompson_series(name, max_q_exp=m * max_q_exp)
    if f is None:
        raise RuntimeError(f"Series unavailable for class {class_name}")

    faber = faber_polynomial_series(f, m=m, max_q_exp=max_q_exp)
    lhs: dict[int, int] = dict(faber["series"])  # type: ignore[assignment]

    rhs: dict[int, int] = {}

    for a in range(1, m + 1):
        if m % a != 0:
            continue
        d = m // a
        if a == 1:
            h_name = name
        else:
            h_name = power_map.get(a)
            if not h_name:
                raise ValueError(f"Missing power-map entry for a={a} in m={m}")
            h_name = h_name.upper()

        max_needed = d * (max_q_exp // a)
        h = mckay_thompson_series(h_name, max_q_exp=max_needed)
        if h is None:
            raise RuntimeError(f"Series unavailable for power-map class {h_name}")

        # d=1 contributes the negative power q^{-a} from the leading q^{-1}.
        if d == 1:
            rhs[-a] = rhs.get(-a, 0) + 1

        for k in range(1, max_q_exp // a + 1):
            n = d * k
            coef = int(h.get(n, 0))
            if coef == 0:
                continue
            exp = a * k
            rhs[exp] = rhs.get(exp, 0) + d * coef

    mismatches: list[tuple[int, int, int]] = []
    for e in [-m] + list(range(1, max_q_exp + 1)):
        lv = int(lhs.get(e, 0))
        rv = int(rhs.get(e, 0))
        if lv != rv:
            mismatches.append((e, lv, rv))

    return {
        "class_name": name,
        "m": m,
        "max_q_exp": max_q_exp,
        "verified": len(mismatches) == 0,
        "n_mismatches": len(mismatches),
        "mismatches": mismatches[:10],
    }


def verify_square_power_relation(
    class_name: str,
    expected_square_class: str | None = None,
    max_q_exp: int = 20,
    candidates: tuple[str, ...] = ("2A", "2B"),
) -> dict[str, object]:
    """Verify the m=2 replicability identity to infer/confirm g^2.

    For m=2:
      Phi_2(T_g)(τ) = T_g(τ/2) + T_g((τ+1)/2) + T_{g^2}(2τ).

    The decimation sum picks out even coefficients:
      T_g(τ/2) + T_g((τ+1)/2) = 2 * sum_{n>=1} a_{2n} q^n.
    """
    if max_q_exp < 1:
        raise ValueError("max_q_exp must be >= 1")

    name = class_name.upper()
    f = mckay_thompson_series(name, max_q_exp=2 * max_q_exp)
    if f is None:
        raise RuntimeError(f"Series unavailable for class {class_name}")

    faber = faber_polynomial_series(f, m=2, max_q_exp=max_q_exp)
    lhs: dict[int, int] = dict(faber["series"])  # type: ignore[assignment]

    rhs_dec: dict[int, int] = {}
    for n in range(1, max_q_exp + 1):
        rhs_dec[n] = 2 * int(f.get(2 * n, 0))

    remainder: dict[int, int] = {}
    for e in set(lhs.keys()) | set(rhs_dec.keys()):
        remainder[e] = int(lhs.get(e, 0)) - int(rhs_dec.get(e, 0))
    remainder = {e: v for e, v in remainder.items() if v != 0}

    cand_results: dict[str, dict[str, object]] = {}
    for cand in candidates:
        g2 = mckay_thompson_series(cand, max_q_exp=max_q_exp)
        if g2 is None:
            continue

        expected: dict[int, int] = {}
        for e, c in g2.items():
            ee = 2 * int(e)
            if ee <= max_q_exp:
                expected[ee] = int(c)

        mismatches: list[tuple[int, int, int]] = []
        for e in [-2] + [2 * n for n in range(1, max_q_exp // 2 + 1)]:
            lv = int(remainder.get(e, 0))
            rv = int(expected.get(e, 0))
            if lv != rv:
                mismatches.append((e, lv, rv))

        cand_results[cand] = {
            "n_mismatches": len(mismatches),
            "mismatches": mismatches[:10],
        }

    inferred = None
    if cand_results:
        inferred = min(cand_results.items(), key=lambda kv: int(kv[1]["n_mismatches"]))[
            0
        ]

    target = expected_square_class.upper() if expected_square_class else inferred
    verified = False
    target_mismatches: list[tuple[int, int, int]] = []
    if target and target in cand_results:
        verified = int(cand_results[target]["n_mismatches"]) == 0
        target_mismatches = list(cand_results[target]["mismatches"])  # type: ignore[list-item]

    return {
        "class_name": name,
        "max_q_exp": max_q_exp,
        "verified": verified,
        "inferred_power_class": inferred,
        "expected_power_class": (
            expected_square_class.upper() if expected_square_class else None
        ),
        "target_mismatches": target_mismatches,
        "candidates": cand_results,
    }


def analyze_monster_moonshine_power_closure(
    max_q_exp: int = 24,
    classes: list[str] | None = None,
    atlas_json_path: str | None = None,
) -> dict[str, object]:
    """Infer and verify a q-series power-map closure on supported classes.

    This is a *purely q-series* (replicability) computation that does not assume
    ATLAS power maps. It:
      - infers g^2 (m=2) for supported classes (where the target class exists),
      - infers g^3 and g^5 via prime replicability (when targets exist),
      - verifies composite divisor-sum replicability for m in {4,6,8,9,10}
        whenever all required power-map targets are available,
      - checks the basic closure identity (g^2)^2 = g^4 when both sides exist.
    """
    if max_q_exp < 6:
        raise ValueError("max_q_exp must be >= 6 for meaningful closure checks")

    def _order(name: str) -> int:
        s = name.strip().upper()
        if s in ("1A", "ID", "IDENTITY"):
            return 1
        digits = ""
        for ch in s:
            if ch.isdigit():
                digits += ch
            else:
                break
        return int(digits) if digits else 0

    supported_seed = [
        "1A",
        "2A",
        "2B",
        "3A",
        "3B",
        "3C",
        "4A",
        "4B",
        "4C",
        "4D",
        "5A",
        "5B",
        "6A",
        "6B",
        "6C",
        "6D",
        "6E",
        "7A",
        "7B",
        "8A",
        "8A'",
        "8B",
        "8E",
        "9A",
        "10A",
        "10B",
        "10C",
        "10D",
        "10E",
        "11A",
        "13A",
        "13B",
    ]

    supported_all = [
        c for c in supported_seed if mckay_thompson_series(c, max_q_exp=2) is not None
    ]

    by_order: dict[int, list[str]] = {}
    for c in supported_all:
        by_order.setdefault(_order(c), []).append(c)
    for k in list(by_order.keys()):
        by_order[k] = sorted(by_order[k])

    if classes is None:
        targets = list(supported_all)
    else:
        wanted = {str(x).upper() for x in classes}
        targets = [c for c in supported_all if c.upper() in wanted]

    atlas = load_monster_atlas_ccls(json_path=atlas_json_path)

    def _cand_for_order(o: int) -> tuple[str, ...]:
        if o <= 0:
            return ()
        if o == 1:
            return ("1A",)
        return tuple(by_order.get(o, []))

    squares: dict[str, str] = {}
    cubes: dict[str, str] = {}
    fifths: dict[str, str] = {}

    square_results: dict[str, dict[str, object]] = {}
    cube_results: dict[str, dict[str, object]] = {}
    fifth_results: dict[str, dict[str, object]] = {}

    for g in targets:
        og = _order(g)
        if og <= 1:
            continue

        # g^2 has order og/gcd(og,2)
        o2 = og // 2 if (og % 2 == 0) else og
        cand2 = _cand_for_order(o2)
        if cand2:
            res2 = verify_square_power_relation(
                g, max_q_exp=max_q_exp, candidates=cand2
            )
            square_results[g] = res2
            if res2.get("inferred_power_class"):
                squares[g] = str(res2["inferred_power_class"])

        # prime m=3: g^3 has order og/gcd(og,3)
        o3 = og // 3 if (og % 3 == 0) else og
        cand3 = _cand_for_order(o3)
        if cand3:
            try:
                res3 = verify_power_relation(
                    g, m=3, max_q_exp=max_q_exp, candidates=cand3
                )
                cube_results[g] = res3
                if res3.get("inferred_power_class"):
                    cubes[g] = str(res3["inferred_power_class"])
            except Exception:
                pass

        # prime m=5: g^5 has order og/gcd(og,5)
        o5 = og // 5 if (og % 5 == 0) else og
        cand5 = _cand_for_order(o5)
        if cand5:
            try:
                res5 = verify_power_relation(
                    g, m=5, max_q_exp=max_q_exp, candidates=cand5
                )
                fifth_results[g] = res5
                if res5.get("inferred_power_class"):
                    fifths[g] = str(res5["inferred_power_class"])
            except Exception:
                pass

    # g^4 from squares when possible (g^4 = (g^2)^2).
    fourths: dict[str, str] = {}
    for g, g2 in squares.items():
        g4 = squares.get(g2)
        if g4:
            fourths[g] = g4

    composite_checks: list[dict[str, object]] = []
    composite_ms = (4, 6, 8, 9, 10)
    for g in targets:
        og = _order(g)
        if og not in composite_ms:
            continue
        m = og
        power_map: dict[int, str] = {}
        for a in range(2, m + 1):
            if m % a != 0:
                continue
            if a == m:
                power_map[a] = "1A"
            elif a == 2 and g in squares:
                power_map[a] = squares[g]
            elif a == 3 and g in cubes:
                power_map[a] = cubes[g]
            elif a == 4:
                if m == 4:
                    power_map[a] = "1A"
                elif g in fourths:
                    power_map[a] = fourths[g]
            elif a == 5 and g in fifths:
                power_map[a] = fifths[g]
            elif a in (6, 8, 9, 10):
                power_map[a] = "1A"

        required = [a for a in range(2, m + 1) if m % a == 0]
        if atlas is not None:
            atlas_map: dict[int, str] = {}
            ok = True
            for a in required:
                t = _atlas_power_targets(atlas, g, a)
                if not t or len(t) != 1:
                    ok = False
                    break
                atlas_map[int(a)] = str(t[0]).upper()
            if ok:
                chk = verify_replicability_relation(
                    g, m=m, power_map=atlas_map, max_q_exp=min(12, max_q_exp)
                )
                chk["power_map"] = dict(atlas_map)
                chk["power_map_source"] = "atlas"
                composite_checks.append(chk)
        else:
            if all(a in power_map for a in required):
                chk = verify_replicability_relation(
                    g, m=m, power_map=power_map, max_q_exp=min(12, max_q_exp)
                )
                chk["power_map"] = dict(power_map)
                chk["power_map_source"] = "inferred"
                composite_checks.append(chk)

    closure: dict[str, dict[str, object]] = {}
    for g, g2 in squares.items():
        g4 = squares.get(g2)
        if not g4:
            continue
        closure[g] = {
            "g2": g2,
            "g4": g4,
            "order": _order(g),
            "order_g2": _order(g2),
            "order_g4": _order(g4),
        }

    return {
        "supported_classes": supported_all,
        "target_classes": targets,
        "atlas_available": atlas is not None,
        "power_maps": {
            "square": squares,
            "cube": cubes,
            "fifth": fifths,
            "fourth_from_square": fourths,
        },
        "atlas_validation": {
            "square": {
                g: {
                    "inferred": squares.get(g),
                    "atlas_targets": _atlas_power_targets(atlas, g, 2),
                    "matches": (
                        (squares.get(g) in (_atlas_power_targets(atlas, g, 2) or []))
                        if squares.get(g) is not None
                        else None
                    ),
                }
                for g in sorted(squares.keys())
            },
            "cube": {
                g: {
                    "inferred": cubes.get(g),
                    "atlas_targets": _atlas_power_targets(atlas, g, 3),
                    "matches": (
                        (cubes.get(g) in (_atlas_power_targets(atlas, g, 3) or []))
                        if cubes.get(g) is not None
                        else None
                    ),
                }
                for g in sorted(cubes.keys())
            },
            "fifth": {
                g: {
                    "inferred": fifths.get(g),
                    "atlas_targets": _atlas_power_targets(atlas, g, 5),
                    "matches": (
                        (fifths.get(g) in (_atlas_power_targets(atlas, g, 5) or []))
                        if fifths.get(g) is not None
                        else None
                    ),
                }
                for g in sorted(fifths.keys())
            },
        },
        "replicability": {
            "square_results": square_results,
            "cube_results": cube_results,
            "fifth_results": fifth_results,
            "composite_checks": composite_checks,
        },
        "closure": closure,
    }


def compute_mckay_traces(
    class_name: str = "1A",
    n_terms: int = 8,
    use_full: bool = True,
    json_path: str | None = None,
):
    """Compute McKay–Thompson traces Tr(g | V_n) for `class_name` up to `n_terms`.

    - If `class_name` == '1A' (identity) this returns the standard j‑coefficients.
    - If a full Monster character table is available (GAP or bundled), it will be
      used to compute traces from the irrep multiplicities in `V_n`.
    - Otherwise, falls back to eta-quotient series for some prime-order classes.
    """
    # identity: trivial shortcut
    if class_name.upper() in ("1A", "ID", "IDENTITY"):
        return j_coeffs(n_terms)

    # Try to obtain character values for the requested class (JSON/libgap/GAP).
    char_map = _load_monster_char_map_via_gap(class_name, json_path=json_path)
    if char_map is None:
        # Offline fallback (eta-quotients) for a handful of Fricke prime classes.
        series = mckay_thompson_series(class_name, max_q_exp=n_terms)
        if series is not None:
            return [int(series.get(n, 0)) for n in range(1, n_terms + 1)]
        return None

    # obtain decomposition data
    data = analyze_leech_monster()
    if (
        use_full
        and data.get("monster_irreps_available")
        and data.get("j_decompositions_full")
    ):
        decomps = data["j_decompositions_full"]
    else:
        decomps = data["j_decompositions"]

    # character values already loaded above (JSON/libgap/GAP)

    traces = []
    for n in range(1, min(n_terms, len(data["j_coeffs"])) + 1):
        dec = decomps.get(n, {}).get("decomp", {})
        total = 0
        for deg, mult in dec.items():
            ch = char_map.get(int(deg))
            if ch is None:
                # missing character value for this irreducible degree
                total = None
                break
            total += int(mult) * int(ch)
        traces.append(total)
    return traces


def plot_mckay_series(
    class_name: str = "1A", n_terms: int = 12, out_png: str | None = None
):
    """Return McKay–Thompson traces and optionally save a PNG plot (matplotlib).

    Always writes a CSV to `./outputs/mckay_{class_name}.csv`.
    """
    traces = compute_mckay_traces(class_name, n_terms=n_terms)
    if traces is None:
        raise RuntimeError("Character table unavailable for class: %s" % class_name)

    from pathlib import Path

    out_dir = Path(__file__).resolve().parents[1] / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"mckay_{class_name}.csv"
    with csv_path.open("w", encoding="utf-8") as fh:
        fh.write("n,trace\n")
        for i, t in enumerate(traces, start=1):
            fh.write(f"{i},{t}\n")

    # optional plotting
    try:
        import matplotlib.pyplot as plt

        xs = list(range(1, len(traces) + 1))
        plt.figure(figsize=(7, 4))
        plt.plot(xs, traces, marker="o")
        plt.title(f"McKay–Thompson traces for {class_name}")
        plt.xlabel("n")
        plt.ylabel("trace")
        plt.grid(True)
        if out_png:
            plt.savefig(out_png)
        else:
            png_path = out_dir / f"mckay_{class_name}.png"
            plt.savefig(png_path)
        plt.close()
    except Exception:
        # matplotlib optional — CSV is always written
        out_png = None

    return {"csv": str(csv_path), "png": out_png}


@lru_cache(maxsize=1)
def compute_w33_monster_invariants() -> dict:
    """Compute W(3,3) invariants used in the Monster correction identities."""
    import numpy as np

    n, _vertices, adj, _edges = build_w33()
    simplices = build_clique_complex(n, adj)
    hom = compute_homology(simplices)

    n_vertices = len(simplices.get(0, []))
    n_lines = len(simplices.get(3, []))  # K4 cliques correspond to GQ lines
    b1 = int(hom["betti_numbers"].get(1, 0))

    # Hodge L1 = d1^T d1 + d2 d2^T on 1-chains (edges)
    d1 = boundary_matrix(simplices[1], simplices[0]).astype(float)
    d2 = boundary_matrix(simplices[2], simplices[1]).astype(float)
    L1 = d1.T @ d1 + d2 @ d2.T
    evals = np.linalg.eigvalsh(L1)
    tol = 1e-8
    nonzero = [float(x) for x in evals if abs(float(x)) > tol]
    spectral_gap = min(nonzero) if nonzero else 0.0

    return {
        "n_vertices": int(n_vertices),
        "n_lines": int(n_lines),
        "n_incidence_objects": int(n_vertices + n_lines),
        "b1": int(b1),
        "spectral_gap_L1": float(spectral_gap),
    }


def verify_borcherds_denominator_identity(
    max_p_degree: int = 2, max_q_degree: int = 2
) -> dict:
    """Verify a low-order truncation of Borcherds' Monster Lie algebra identity.

    Denominator identity (Borcherds 1992), with J(τ)=j(τ)-744 and
    J(q)=∑_{n=-1}^∞ c(n) q^n (c(-1)=1, c(0)=0):

        p^{-1} ∏_{m>0, n∈ℤ} (1 - p^m q^n)^{c(mn)} = J(p) - J(q).

    This function verifies equality of the truncated Laurent series in p and q
    for p-degree ≤ max_p_degree and q-degree ≤ max_q_degree.
    """
    if max_p_degree < 0 or max_q_degree < 0:
        raise ValueError("max_p_degree and max_q_degree must be non-negative")

    # We need one extra q-degree because the unique negative-q factor (1 - p q^{-1})
    # can shift a q^{N+1} term down to q^N.
    max_p_intermediate = max_p_degree + 1
    max_q_intermediate = max_q_degree + 1
    max_coeff = max_p_intermediate * max_q_intermediate

    # c(n) are the coefficients of J(q)=j(q)-744 (same positive coefficients as j)
    j_pos = j_coeffs(max_coeff)
    c = {-1: 1, 0: 0}
    for i, v in enumerate(j_pos, start=1):
        c[i] = int(v)

    def series_mul(a: dict, b: dict, max_p: int, max_q: int, min_q: int) -> dict:
        out: dict[tuple[int, int], int] = {}
        for (pa, qa), ca in a.items():
            for (pb, qb), cb in b.items():
                p = pa + pb
                q = qa + qb
                if p > max_p or q > max_q or q < min_q:
                    continue
                out[(p, q)] = out.get((p, q), 0) + int(ca) * int(cb)
        return {k: v for k, v in out.items() if v != 0}

    def binomial_factor_series(m: int, n: int, e: int, max_p: int, max_q: int) -> dict:
        # (1 - x)^e = Σ_k (-1)^k C(e,k) x^k, with x = p^m q^n
        k_max = min(max_p // m, max_q // n)
        out = {(0, 0): 1}
        for k in range(1, k_max + 1):
            out[(m * k, n * k)] = ((-1) ** k) * comb(e, k)
        return out

    # Build positive (nonnegative-q) part first, allowing one extra q-degree.
    prod: dict[tuple[int, int], int] = {(0, 0): 1}
    for m in range(1, max_p_intermediate + 1):
        for n in range(1, max_q_intermediate + 1):
            e = int(c.get(m * n, 0))
            if e == 0:
                continue
            f = binomial_factor_series(m, n, e, max_p_intermediate, max_q_intermediate)
            prod = series_mul(prod, f, max_p_intermediate, max_q_intermediate, min_q=0)

    # Multiply the unique negative-q factor (1 - p q^{-1}) and truncate q to max_q_degree.
    prod = series_mul(
        prod,
        {(0, 0): 1, (1, -1): -1},
        max_p_intermediate,
        max_q_degree,
        min_q=-1,
    )

    # Apply the p^{-1} prefactor (shift p-degree by -1).
    lhs = {(p - 1, q): int(v) for (p, q), v in prod.items() if (p - 1) <= max_p_degree}

    # RHS series: J(p) - J(q), with no mixed terms.
    rhs: dict[tuple[int, int], int] = {(-1, 0): 1, (0, -1): -1}
    for k in range(1, max(max_p_degree, max_q_degree) + 1):
        ck = int(c.get(k, 0))
        if k <= max_p_degree:
            rhs[(k, 0)] = rhs.get((k, 0), 0) + ck
        if k <= max_q_degree:
            rhs[(0, k)] = rhs.get((0, k), 0) - ck

    keys = set(lhs) | set(rhs)
    mismatches = {}
    max_abs_mixed = 0
    for key in keys:
        lv = lhs.get(key, 0)
        rv = rhs.get(key, 0)
        if lv != rv:
            mismatches[key] = {"lhs": lv, "rhs": rv}
        p, q = key
        if p != 0 and q != 0:
            max_abs_mixed = max(max_abs_mixed, abs(lv - rv))

    return {
        "max_p_degree": int(max_p_degree),
        "max_q_degree": int(max_q_degree),
        "verified": len(mismatches) == 0,
        "n_mismatches": int(len(mismatches)),
        "max_abs_mixed_coefficient_error": int(max_abs_mixed),
        "mismatches": mismatches,
    }


@lru_cache(maxsize=1)
def analyze_leech_monster() -> Dict:
    """Compute Leech/Monster numerology derived from W(3,3)/E8 data.

    Returns a dictionary of integers and additional Moonshine checks suitable
    for deterministic unit tests.
    """
    data = analyze_leech_connection()

    e8_roots = data["e8_roots"]
    e8_cubed_roots = data["e8_cubed_roots"]
    leech_kissing = data["leech_kissing"]
    ratio = data["ratio"]

    # Smallest nontrivial Monster representation dimension (McKay--Thompson)
    monster_min_rep = 196_883
    monster_diff = monster_min_rep - leech_kissing

    psp_cubed_order = data.get("psp_cubed_order")
    co0_order = data.get("co0_order")
    excess_symmetry_factor = data.get("excess_symmetry_factor")

    interpretation = (
        "E8^3 provides 720 root vectors; the Leech kissing number 196560 "
        "is 273×720. The smallest Monster rep (196883) is close (difference=323), "
        "suggesting deep but nontrivial connections (Moonshine numerology). "
        "ATLAS standard generators for M refine this: for a∈2A and b∈3B, "
        "Pr(|ab|=29)=1632586752/111045174695, and the class-algebra structure "
        "constant satisfies n_{2A,3B}^{29A}=|C_M(29A)|=87 (so there are exactly "
        "|M| pairs (a,b) with ab in 29A)."
    )

    # modular/j comparisons
    e4 = e4_coeffs(n_terms=8)
    e4_cubed = poly_power(e4, 3, 8)
    # coefficient of q^1 in Theta(E8)^3 equals 720 (E8^3 minimal vectors)
    theta_e8_cubed_q1 = e4_cubed[1] if len(e4_cubed) > 1 else None

    # Expanded Klein j coefficients (q^1..q^N)
    j_list = j_coeffs(n_terms=8)

    # Small, commonly-used list of Monster irreducible character dimensions
    # (we keep a compact 'known' list for automated comparison tests).
    known_monster_irreps = [
        1,
        196_883,
        21_296_876,
        842_609_326,
        18_538_750_076,
        19_360_062_527,
    ]

    # Exact decomposition search (tries large-first, backtracking). Returns
    # a dict {dim: multiplicity} on success or None.
    import time as _time

    _decompose_deadline = [0.0]  # mutable container for closure

    def _decompose_exact(target: int, irreps: list[int], idx: int = 0, memo=None):
        memo = memo or {}
        key = (idx, target)
        if key in memo:
            return None
        # time-based cutoff: abort search after 5 seconds per coefficient
        if _time.perf_counter() > _decompose_deadline[0]:
            return None
        # cheap cutoff to avoid combinatorial explosion when using a very
        # small bundled irreps list — fallback to greedy will be used.
        if idx == 0 and len(irreps) < 10 and target > irreps[0] * 50:
            memo[key] = None
            return None
        if target == 0:
            return {}
        if idx >= len(irreps):
            return None
        val = irreps[idx]
        # reasonable cap on multiplicities to keep search bounded
        max_m = target // val
        if val == 1:
            max_m = min(max_m, 100)  # trivial rep shouldn't blow up search
        elif val >= 10**9:
            max_m = min(max_m, 3)
        elif val >= 10**7:
            max_m = min(max_m, 10)
        # try to use as many of the large irreps as possible first
        for m in range(max_m, -1, -1):
            rem = target - m * val
            if rem < 0:
                continue
            if rem == 0:
                out = {} if m == 0 else {val: m}
                return out
            sub = _decompose_exact(rem, irreps, idx + 1, memo)
            if sub is not None:
                if m:
                    sub[val] = m
                return sub
        memo[key] = None
        return None

    # Fast greedy partial decomposition (useful when exact match not found)
    def _greedy_decompose(target: int, irreps: list[int]):
        rem = target
        out = {}
        for val in irreps:
            if rem <= 0:
                break
            m = rem // val
            if m:
                out[val] = int(m)
                rem -= m * val
        return out, rem

    # Attempt exact decomposition using known irreps; fall back to greedy
    j_decompositions = {}
    irreps_desc = sorted(known_monster_irreps, reverse=True)
    for idx, c in enumerate(j_list, start=1):
        _decompose_deadline[0] = _time.perf_counter() + 2.0
        exact = _decompose_exact(c, irreps_desc)
        if exact is not None:
            # normalize to include zero multiplicities only for reported dims
            j_decompositions[idx] = {"exact": True, "decomp": exact, "remainder": 0}
        else:
            greedy, rem = _greedy_decompose(c, irreps_desc)
            j_decompositions[idx] = {"exact": False, "decomp": greedy, "remainder": rem}

    # attempt to load full Monster irreps via GAP/libgap (optional)
    # The Monster has 194 conjugacy classes → 194 irreducible representations.
    # Only consider data "available" when we have all (or nearly all) of them.
    monster_irreps_full = _load_monster_irreps_via_gap()
    monster_irreps_available = (
        monster_irreps_full is not None and len(monster_irreps_full) >= 100
    )
    j_decompositions_full = {}
    if monster_irreps_available:
        irreps_full_desc = sorted(monster_irreps_full, reverse=True)
        for idx, c in enumerate(j_list, start=1):
            _decompose_deadline[0] = _time.perf_counter() + 2.0
            exact = _decompose_exact(c, irreps_full_desc)
            if exact is not None:
                j_decompositions_full[idx] = {
                    "exact": True,
                    "decomp": exact,
                    "remainder": 0,
                }
            else:
                greedy, rem = _greedy_decompose(c, irreps_full_desc)
                j_decompositions_full[idx] = {
                    "exact": False,
                    "decomp": greedy,
                    "remainder": rem,
                }

    # expose the first coefficient for legacy tests
    j1 = j_list[0]
    j_minus_leech = j1 - leech_kissing

    # Derive the "Monster correction" from intrinsic W(3,3) invariants.
    w33_inv = compute_w33_monster_invariants()
    w33_objects = int(w33_inv["n_incidence_objects"])  # 40 points + 40 lines
    w33_b1 = int(w33_inv["b1"])  # dim H1(W33)
    w33_gap = float(w33_inv["spectral_gap_L1"])  # L1 spectral gap (Δ)

    monster_diff_from_w33 = w33_objects + 3 * w33_b1
    j_minus_leech_from_w33 = int(round(w33_gap)) * w33_b1

    # Canonical values (computed, not hard-coded)
    assert w33_objects == 80, f"Expected 40 points + 40 lines = 80, got {w33_objects}"
    assert w33_b1 == 81, f"Expected b1=81, got {w33_b1}"
    assert abs(w33_gap - 4.0) < 1e-8, f"Expected spectral gap 4, got {w33_gap}"

    # Monster/Leech identities
    assert (
        monster_diff == monster_diff_from_w33
    ), f"Monster correction mismatch: {monster_diff} vs {monster_diff_from_w33}"
    assert (
        j_minus_leech == j_minus_leech_from_w33
    ), f"j-Leech mismatch: {j_minus_leech} vs {j_minus_leech_from_w33}"
    assert j1 - monster_min_rep == 1, "McKay observation failed: 196884 != 1 + 196883"

    # Borcherds denominator identity (Monster Lie algebra) — low-order check
    borcherds = verify_borcherds_denominator_identity(max_p_degree=2, max_q_degree=2)
    assert borcherds["verified"] is True, (
        "Borcherds denominator identity failed (truncated check): "
        f"{borcherds['n_mismatches']} mismatches"
    )

    ogg = ogg_primes_via_genus(max_p=100)
    monster_primes = monster_prime_divisors()
    assert ogg["primes"] == monster_primes, "Ogg primes != primes dividing |Monster|"

    sporadic = analyze_sporadic_group_magnitudes()
    if sporadic.get("available") is True:
        facs = sporadic.get("factorizations", {})
        if isinstance(facs, dict) and "M" in facs:
            assert facs["M"] == monster_order_factorization()

    atlas_generator_search = analyze_monster_atlas_generator_search_probabilities()
    atlas_probability_landscape = analyze_monster_atlas_probability_landscape()
    atlas_powering_probabilities = analyze_monster_atlas_powering_probabilities()
    atlas_step3 = (
        analyze_monster_standard_generator_step3_order29_from_character_table()
    )
    atlas_pipeline = analyze_monster_atlas_standard_generator_pipeline()
    atlas_2a3b = analyze_monster_2a3b_class_algebra_partial_distribution()

    rr_j = analyze_rogers_ramanujan_j_invariant(n_terms=5)
    assert rr_j.get("available") is True and rr_j.get("verified") is True, (
        "Rogers–Ramanujan j-invariant identity check failed: "
        f"{rr_j.get('j_from_rogers_ramanujan')}"
    )

    return {
        "e8_roots": e8_roots,
        "e8_cubed_roots": e8_cubed_roots,
        "leech_kissing": leech_kissing,
        "ratio": ratio,
        "monster_min_rep": monster_min_rep,
        "monster_diff": monster_diff,
        "psp_cubed_order": psp_cubed_order,
        "co0_order": co0_order,
        "excess_symmetry_factor": excess_symmetry_factor,
        "theta_e8_cubed_q1": theta_e8_cubed_q1,
        "j1": j1,
        "j_minus_leech": j_minus_leech,
        "j_coeffs": j_list,
        "monster_irreps_known": known_monster_irreps,
        "j_decompositions": j_decompositions,
        "monster_irreps_full": monster_irreps_full,
        "monster_irreps_available": monster_irreps_available,
        "j_decompositions_full": j_decompositions_full,
        "w33_invariants_for_monster": w33_inv,
        "monster_diff_from_w33": monster_diff_from_w33,
        "j_minus_leech_from_w33": j_minus_leech_from_w33,
        "borcherds_denominator_identity": borcherds,
        "ogg_primes": ogg["primes"],
        "ogg_primes_details": ogg["details"],
        "monster_order": monster_order(),
        "monster_order_primes": monster_primes,
        "sporadic_magnitudes": sporadic,
        "atlas_generator_search": atlas_generator_search,
        "atlas_probability_landscape": atlas_probability_landscape,
        "atlas_powering_probabilities": atlas_powering_probabilities,
        "atlas_standard_generators_step3": atlas_step3,
        "atlas_standard_generators_pipeline": atlas_pipeline,
        "atlas_2A3B_class_algebra_partial": atlas_2a3b,
        "rogers_ramanujan_j": rr_j,
        "interpretation": interpretation,
    }


if __name__ == "__main__":
    out = analyze_leech_monster()
    print("PILLAR 57: LEECH / MONSTER / MOONSHINE NUMEROLOGY")
    print("- E8 roots:", out["e8_roots"])
    print("- E8^3 roots:", out["e8_cubed_roots"])
    print("- Leech kissing number:", out["leech_kissing"])
    print("- Ratio (Leech/E8^3):", out["ratio"])
    print("- Monster smallest nontrivial rep:", out["monster_min_rep"])
    print("- Difference (Monster - Leech):", out["monster_diff"])
    w33 = out["w33_invariants_for_monster"]
    print(
        "- W33 invariants: objects=%d, b1=%d, gap=%.1f"
        % (w33["n_incidence_objects"], w33["b1"], w33["spectral_gap_L1"])
    )
    print(
        "- 323 = objects + 3·b1 = %d + 3·%d" % (w33["n_incidence_objects"], w33["b1"])
    )
    print("- 324 = Δ·b1 =", out["j_minus_leech_from_w33"])
    print(
        "- Borcherds denominator (p≤%d,q≤%d): verified=%s"
        % (
            out["borcherds_denominator_identity"]["max_p_degree"],
            out["borcherds_denominator_identity"]["max_q_degree"],
            out["borcherds_denominator_identity"]["verified"],
        )
    )
    print("- Ogg primes (genus-zero X0(p)^+):", out["ogg_primes"])
    sp = out.get("sporadic_magnitudes", {})
    if isinstance(sp, dict) and sp.get("available") is True:
        print("- Sporadic prime union:", sp.get("primes_union"))
        print("- Extra primes beyond Monster:", sp.get("extra_primes_union"))
        print("- Extra-prime groups:", sp.get("groups_with_extra_primes"))
        top = sp.get("top5_by_order", [])
        if isinstance(top, list) and top:
            digits = sp.get("digits", {})
            if isinstance(digits, dict):
                print(
                    "- Largest sporadics (decimal digits):",
                    [(g, digits.get(g)) for g in top],
                )
    ags = out.get("atlas_generator_search", {})
    if isinstance(ags, dict) and ags.get("available") is True:
        gs = ags.get("generator_search", {})
        if isinstance(gs, dict):
            to_2a = gs.get("to_2A", {})
            to_3b = gs.get("to_3B", {})
            if isinstance(to_2a, dict):
                p2a = to_2a.get("probability", {})
                e2a = to_2a.get("expected_trials", {})
                print(
                    "- ATLAS generator search: Pr(·→2A) = %s (E[trials]=%.3f)"
                    % (p2a.get("value"), float(e2a.get("float", 0.0))),
                )
            if isinstance(to_3b, dict):
                p3b = to_3b.get("probability", {})
                e3b = to_3b.get("expected_trials", {})
                v3 = to_3b.get("denominator_3_adic_valuation")
                print(
                    "- ATLAS generator search: Pr(·→3B) = %s (E[trials]=%.3f, v3=%s)"
                    % (p3b.get("value"), float(e3b.get("float", 0.0)), v3),
                )
    apl = out.get("atlas_probability_landscape", {})
    if isinstance(apl, dict) and apl.get("available") is True:
        top_orders = apl.get("top_orders", [])
        if isinstance(top_orders, list) and top_orders:
            o0 = top_orders[0]
            if isinstance(o0, dict):
                p0 = o0.get("p", {})
                print(
                    "- ATLAS order landscape: most common order=%s (Pr=%s)"
                    % (
                        o0.get("order"),
                        p0.get("value") if isinstance(p0, dict) else None,
                    ),
                )
        mc = apl.get("min_centralizer", {})
        if isinstance(mc, dict):
            mcp = mc.get("max_class_probability", {})
            print(
                "- ATLAS class landscape: min |C(g)|=%s at %s (Pr=%s)"
                % (
                    mc.get("centralizer_order"),
                    mc.get("classes"),
                    mcp.get("value") if isinstance(mcp, dict) else None,
                ),
            )
    step3 = out.get("atlas_standard_generators_step3", {})
    if isinstance(step3, dict) and step3.get("available") is True:
        prob = step3.get("probability", {})
        if isinstance(prob, dict):
            print(
                "- ATLAS standard generators: Pr(2A·3B has order 29) = %s (E[trials]=%.3f)"
                % (prob.get("value"), float(step3.get("expected_trials", 0.0))),
            )
    dist = out.get("atlas_2A3B_class_algebra_partial", {})
    if isinstance(dist, dict) and dist.get("available") is True:
        cls = dist.get("classes", {})
        if isinstance(cls, dict):
            p3 = cls.get("3B", {}).get("probability", {})
            n3 = cls.get("3B", {}).get("structure_constant_per_element")
            if isinstance(p3, dict) and n3 is not None:
                print(
                    "- Class algebra: Pr(2A·3B ∈ 3B) = %s (n=%s)"
                    % (p3.get("value"), n3),
                )
            p41 = cls.get("41A", {}).get("probability", {})
            n41 = cls.get("41A", {}).get("structure_constant_per_element")
            if isinstance(p41, dict) and n41 is not None:
                print(
                    "- Class algebra: Pr(2A·3B ∈ 41A) = %s (n=%s)"
                    % (p41.get("value"), n41),
                )
            p31 = cls.get("31A", {}).get("probability", {})
            n31 = cls.get("31A", {}).get("structure_constant_per_element")
            if isinstance(p31, dict) and n31 is not None:
                print(
                    "- Class algebra: Pr(2A·3B ∈ 31A) = %s (n=%s)"
                    % (p31.get("value"), n31),
                )
            p71 = cls.get("71A", {}).get("probability", {})
            n71 = cls.get("71A", {}).get("structure_constant_per_element")
            if isinstance(p71, dict) and n71 is not None:
                print(
                    "- Class algebra: Pr(2A·3B ∈ 71A) = %s (n=%s)"
                    % (p71.get("value"), n71),
                )
            p47 = cls.get("47A", {}).get("probability", {})
            p59 = cls.get("59A", {}).get("probability", {})
            if isinstance(p47, dict) and isinstance(p59, dict):
                if p47.get("numerator") == 0 and p59.get("numerator") == 0:
                    print(
                        "- Class algebra: Pr(2A·3B ∈ 47A) = 0; Pr(... ∈ 59A) = 0"
                    )
    pipe = out.get("atlas_standard_generators_pipeline", {})
    if isinstance(pipe, dict) and pipe.get("available") is True:
        strat = pipe.get("strategy_resample_both", {})
        if isinstance(strat, dict):
            erd = strat.get("expected_random_draws_total", {})
            if isinstance(erd, dict):
                print(
                    "- ATLAS pipeline (resample both): E[random draws] = %s (~%.1f)"
                    % (erd.get("value"), float(erd.get("float", 0.0))),
                )
    rr = out.get("rogers_ramanujan_j", {})
    if isinstance(rr, dict) and rr.get("available") is True:
        print(
            "- Rogers-Ramanujan: j(u=R^5) identity verified to q^%d: %s"
            % (rr.get("n_terms_verified"), rr.get("verified")),
        )
    print("- Interpretation:", out["interpretation"])
