"""
Statistical Analysis: Is W(3,3) special among strongly regular graphs?

This script:
1. Enumerates all feasible SRG parameter sets with v <= 1000
2. Defines ~30 "coincidence tests" matching physics/math constants
3. Scores every SRG by how many coincidences it achieves
4. Reports where W(3,3) ranks and which coincidences are genuinely rare
"""

import math
from collections import defaultdict


# ====================================================================
# STEP 1: Enumerate feasible SRG parameter sets
# ====================================================================

def srg_eigenvalues(v, k, lam, mu):
    """Return (r, s, f, g) for integral-eigenvalue SRGs, or None."""
    disc = (lam - mu) ** 2 + 4 * (k - mu)
    sqrt_disc = math.isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None  # irrational eigenvalues (conference graph)

    if (lam - mu + sqrt_disc) % 2 != 0:
        return None

    r = ((lam - mu) + sqrt_disc) // 2
    s = ((lam - mu) - sqrt_disc) // 2

    denom = r - s
    if denom == 0:
        return None

    f_num = -k - (v - 1) * s
    if f_num % denom != 0:
        return None
    f = f_num // denom
    g = v - 1 - f

    if f <= 0 or g <= 0:
        return None

    # Verify: K + f*r + g*s = 0 (trace condition)
    if k + f * r + g * s != 0:
        return None

    return r, s, f, g


def enumerate_srgs(max_v=1000):
    """Enumerate feasible SRG(v,k,λ,μ) parameter sets."""
    srgs = []
    for v in range(5, max_v + 1):
        for k in range(2, v):
            if k > v // 2:
                break
            for mu in range(1, k + 1):
                num = mu * (v - k - 1)
                if num % k != 0:
                    continue
                lam = k - 1 - num // k
                if lam < 0 or lam >= k:
                    continue
                # Verify fundamental equation
                if k * (k - lam - 1) != mu * (v - k - 1):
                    continue

                eig = srg_eigenvalues(v, k, lam, mu)
                if eig is None:
                    continue

                r, s, f, g = eig

                E = v * k // 2
                srgs.append({
                    'v': v, 'k': k, 'lam': lam, 'mu': mu,
                    'r': r, 's': s, 'f': f, 'g': g,
                    'E': E,
                })
    return srgs


# ====================================================================
# STEP 2: Define coincidence tests
# ====================================================================

# Physics / math target constants
TARGETS = {
    'alpha_inv': 137,        # fine structure constant inverse (integer part)
    'e8_roots': 240,         # E₈ root system
    'leech_dim': 24,         # Leech lattice dimension
    'niemeier_count': 24,    # Niemeier lattice count
    'leech_kissing': 196560, # Leech lattice kissing number
    'D_bosonic': 26,         # bosonic string dimension
    'D_super': 10,           # superstring dimension
    'D_M': 11,               # M-theory dimension
    'cox_E6': 12,            # Coxeter number h(E₆)
    'cox_E7': 18,            # Coxeter number h(E₇)
    'cox_E8': 30,            # Coxeter number h(E₈)
    'weyl_E6': 51840,        # |W(E₆)|
    'SM_gauge': (3, 2, 1),   # Standard Model gauge group ranks
    'e6_roots': 72,          # E₆ root count
    'e7_roots': 126,         # E₇ root count
}


def compute_derived(s):
    """Compute all derived quantities for an SRG parameter set."""
    v, k, lam, mu = s['v'], s['k'], s['lam'], s['mu']
    r, ss, f, g = s['r'], s['s'], s['f'], s['g']
    E = s['E']

    d = {}
    d['v'], d['k'], d['lam'], d['mu'] = v, k, lam, mu
    d['r'], d['s'], d['f'], d['g'] = r, ss, f, g
    d['E'] = E
    d['mu2'] = mu ** 2
    d['k2'] = k ** 2
    d['theta'] = k - r    # Laplacian eigenvalue 1
    d['lap_s'] = k - ss   # Laplacian eigenvalue 2

    # All "small" derived quantities the phases use
    d['f_plus_lam'] = f + lam
    d['k_minus_1'] = k - 1
    d['v_minus_k_minus_1'] = v - k - 1
    d['k_minus_1_sq'] = (k - 1) ** 2
    d['k_minus_1_sq_plus_mu2'] = (k - 1) ** 2 + mu ** 2
    d['v_minus_theta'] = v - (k - r)
    d['v_minus_k_minus_theta'] = v - k - (k - r)
    d['f_minus_g'] = f - g
    d['theta_times_f'] = (k - r) * f
    d['mu2_times_g'] = (mu ** 2) * g
    d['two_k_q_formula'] = 2 * k * lam if lam > 0 else 0

    # Cyclotomic-like: test if v+1, v-1, k+1, k-1, etc. are prime
    for name, val in [('v', v), ('k', k), ('f', f), ('g', g),
                      ('k+1', k + 1), ('k-1', k - 1), ('v+1', v + 1)]:
        d[f'is_prime_{name}'] = _is_prime(val)

    # Fibonacci check
    d['fib_k'] = _fibonacci(k) if k <= 50 else None
    d['fib_k_minus_1'] = _fibonacci(k - 1) if k > 0 and k - 1 <= 50 else None

    return d


_prime_cache = {}
def _is_prime(n):
    if n in _prime_cache:
        return _prime_cache[n]
    if n < 2:
        _prime_cache[n] = False
        return False
    if n < 4:
        _prime_cache[n] = True
        return True
    if n % 2 == 0 or n % 3 == 0:
        _prime_cache[n] = False
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            _prime_cache[n] = False
            return False
        i += 6
    _prime_cache[n] = True
    return True


_fib_cache = {}
def _fibonacci(n):
    if n in _fib_cache:
        return _fib_cache[n]
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    _fib_cache[n] = b
    return b


def von_staudt_clausen_denom(n):
    """Denominator of B_n via Von Staudt-Clausen: prod of primes p where (p-1)|n."""
    if n <= 0 or n % 2 != 0:
        return None
    prod = 1
    for p in range(2, n + 2):
        if _is_prime(p) and n % (p - 1) == 0:
            prod *= p
    return prod


# ====================================================================
# STEP 3: Score each SRG
# ====================================================================

def score_srg(s):
    """
    Score an SRG by counting how many physics/math coincidences it achieves.
    Returns (total_score, dict of matched coincidences).
    """
    d = compute_derived(s)
    v, k, lam, mu = d['v'], d['k'], d['lam'], d['mu']
    r, ss, f, g = d['r'], d['s'], d['f'], d['g']
    E = d['E']
    theta = d['theta']
    mu2 = d['mu2']

    matches = {}

    # --- 1. Fine structure constant: (k-1)² + μ² = 137 ---
    if d['k_minus_1_sq_plus_mu2'] == 137:
        matches['alpha_inv = (k-1)^2 + mu^2'] = 137

    # --- 2. E₈ root count = edge count ---
    if E == 240:
        matches['E8_roots = edges'] = E

    # --- 3. Leech lattice dim = f ---
    if f == 24:
        matches['Leech_dim = f'] = f

    # --- 4. Bosonic string dim = f + λ ---
    if d['f_plus_lam'] == 26:
        matches['D_bosonic = f + lam'] = d['f_plus_lam']

    # --- 5. Superstring dim = Θ ---
    if theta == 10:
        matches['D_super = theta'] = theta

    # --- 6. M-theory dim = k - 1 ---
    if d['k_minus_1'] == 11:
        matches['D_M = k - 1'] = d['k_minus_1']

    # --- 7. Coxeter h(E₆) = k ---
    if k == 12:
        matches['h(E6) = k'] = k

    # --- 8. Coxeter h(E₇) = v - k - θ ---
    if d['v_minus_k_minus_theta'] == 18:
        matches['h(E7) = v-k-theta'] = 18

    # --- 9. Coxeter h(E₈) = v - θ ---
    if d['v_minus_theta'] == 30:
        matches['h(E8) = v-theta'] = 30

    # --- 10. Spectral equipartition: θf = μ²g = E ---
    if theta * f == mu2 * g == E:
        matches['equipartition: theta*f = mu2*g = E'] = E

    # --- 11. α · ω = v (Hoffman) ---
    if ss != 0 and k - ss != 0:
        hoffman = v * (-ss) / (k - ss)
        clique = 1 + k // (-ss) if ss < 0 else None
        if clique and abs(hoffman * clique - v) < 0.001:
            matches['alpha*omega = v (Hoffman)'] = v

    # --- 12. Fibonacci F(k-1) = 89 ---
    fk1 = d.get('fib_k_minus_1')
    if fk1 == 89:
        matches['F(k-1) = 89'] = 89

    # --- 13. F(k) = k² (Fibonacci uniqueness) ---
    fk = d.get('fib_k')
    if fk is not None and fk == d['k2']:
        matches['F(k) = k^2'] = fk

    # --- 14. v - k - 1 = q³ for some integer q ---
    vk1 = d['v_minus_k_minus_1']
    cbrt = round(vk1 ** (1/3))
    if cbrt ** 3 == vk1 and cbrt >= 2:
        matches['v-k-1 = q^3'] = (vk1, cbrt)

    # --- 15. k + 1 is prime (Φ₃ = 13) ---
    if d['is_prime_k+1']:
        matches['k+1 is prime'] = k + 1

    # --- 16. f - g = perfect square ---
    fg = d['f_minus_g']
    if fg > 0:
        sqrt_fg = math.isqrt(fg)
        if sqrt_fg * sqrt_fg == fg:
            matches['f-g = perfect square'] = fg

    # --- 17. Leech kissing = Φ₆·q²·Φ₃·E for some q, Φ₃, Φ₆ ---
    if E > 0 and 196560 % E == 0:
        ratio = 196560 // E
        matches['Leech_kissing divisible by E'] = ratio

    # --- 18. |W(E₆)| = some_combo * E ---
    if E > 0 and 51840 % E == 0:
        ratio = 51840 // E
        matches['|W(E6)| divisible by E'] = ratio

    # --- 19. Von Staudt-Clausen: denom(B_k) uses k+1 ---
    if k % 2 == 0 and k >= 2:
        vsc = von_staudt_clausen_denom(k)
        if vsc and k + 1 > 1 and vsc % (k + 1) == 0:
            matches['denom(B_k) divisible by k+1'] = vsc

    # --- 20. E₆ roots = 2·k·something from params ---
    for q_val in range(2, 10):
        if 2 * k * q_val == 72:
            matches['E6_roots = 2*k*q'] = (72, q_val)
            break

    # --- 21. E₇ roots from parameters ---
    if E // 2 == 120 or 2 * g * (v - k - 1) == 126 * v // v:
        pass  # too indirect
    for q_val in range(2, 10):
        phi6 = k + 1 - q_val - 1 if k > q_val else 0
        if 2 * phi6 * q_val ** 2 == 126:
            matches['E7_roots = 2*phi6*q^2'] = 126

    # --- 22. ζ(-1) = -1/k (k = 12) ---
    if k == 12:
        matches['zeta(-1) = -1/k'] = k

    # --- 23. SM gauge ranks appear: q=3 (SU(3)), lam=2 (SU(2)), and 1 present ---
    # Check if among {lam, mu, r, s, q-candidate} we find {3, 2, 1}
    param_set = {abs(x) for x in [lam, mu, r, ss] if x != 0}
    if lam > 0:
        param_set.add(lam)
    if {1, 2, 3}.issubset(param_set):
        matches['SM gauge {3,2,1} in params'] = sorted(param_set)

    # --- 24. det(P) = ±E (eigenmatrix determinant) ---
    # P = [[1, k, v-k-1], [1, r, -(r+1)], [1, s, -(s+1)]]
    det_P = (1 * (r * (-(ss + 1)) - (-(r + 1)) * ss)
             - k * (1 * (-(ss + 1)) - (-(r + 1)) * 1)
             + (v - k - 1) * (1 * ss - r * 1))
    if abs(det_P) == E:
        matches['|det(P)| = E'] = abs(det_P)

    # --- 25. E = 2 * dim(E₈) * g  (240 = 2·8·15) ---
    if g > 0 and E > 0:
        if E == 2 * 8 * g:
            matches['E = 2*8*g'] = E

    return len(matches), matches


# ====================================================================
# MAIN ANALYSIS
# ====================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("STATISTICAL ANALYSIS: Is W(3,3) special among SRGs?")
    print("=" * 70)

    print("\nEnumerating feasible SRG parameter sets (v <= 1000)...")
    srgs = enumerate_srgs(max_v=1000)
    print(f"Found {len(srgs)} feasible parameter sets\n")

    # Score all
    results = []
    for s in srgs:
        score, matches = score_srg(s)
        results.append((score, s, matches))

    results.sort(key=lambda x: -x[0])

    # ---- PART A: Top-scoring SRGs ----
    print("=" * 70)
    print("TOP 20 SRGs BY COINCIDENCE COUNT")
    print("=" * 70)
    for rank, (score, s, matches) in enumerate(results[:20], 1):
        label = f"SRG({s['v']},{s['k']},{s['lam']},{s['mu']})"
        is_w33 = " *** W(3,3) ***" if (s['v'] == 40 and s['k'] == 12
                                       and s['lam'] == 2 and s['mu'] == 4) else ""
        print(f"\n#{rank}: {label}  score={score}{is_w33}")
        print(f"     r={s['r']}, s={s['s']}, f={s['f']}, g={s['g']}, E={s['E']}")
        for name, val in sorted(matches.items()):
            print(f"     ✓ {name} = {val}")

    # ---- PART B: Score distribution ----
    print("\n" + "=" * 70)
    print("SCORE DISTRIBUTION")
    print("=" * 70)
    score_counts = defaultdict(int)
    for score, _, _ in results:
        score_counts[score] += 1
    for sc in sorted(score_counts.keys(), reverse=True):
        bar = "█" * score_counts[sc] if score_counts[sc] <= 50 else "█" * 50 + f"...+{score_counts[sc]-50}"
        print(f"  Score {sc:2d}: {score_counts[sc]:5d} SRGs  {bar}")

    # ---- PART C: W(3,3) position ----
    w33_rank = None
    w33_score = None
    for rank, (score, s, matches) in enumerate(results, 1):
        if s['v'] == 40 and s['k'] == 12 and s['lam'] == 2 and s['mu'] == 4:
            w33_rank = rank
            w33_score = score
            w33_matches = matches
            break

    print("\n" + "=" * 70)
    print("W(3,3) = SRG(40,12,2,4) ANALYSIS")
    print("=" * 70)
    print(f"Score: {w33_score}")
    print(f"Rank: #{w33_rank} out of {len(results)} SRGs")
    print(f"Percentile: top {100*w33_rank/len(results):.2f}%")
    print(f"\nMatched coincidences ({w33_score}):")
    for name, val in sorted(w33_matches.items()):
        print(f"  ✓ {name} = {val}")

    # ---- PART D: Per-test rarity ----
    print("\n" + "=" * 70)
    print("PER-TEST RARITY (how many SRGs match each test)")
    print("=" * 70)
    test_counts = defaultdict(int)
    for _, _, matches in results:
        for name in matches:
            test_counts[name] += 1

    rarity = sorted(test_counts.items(), key=lambda x: x[1])
    for name, cnt in rarity:
        pct = 100 * cnt / len(results)
        unique = " [UNIQUE to W(3,3)]" if cnt == 1 and name in w33_matches else ""
        print(f"  {name:45s} : {cnt:5d}/{len(results)} ({pct:5.2f}%){unique}")

    # Count tests that ONLY W(3,3) satisfies
    unique_to_w33 = [name for name, cnt in test_counts.items()
                     if cnt == 1 and name in w33_matches]
    print(f"\nTests UNIQUE to W(3,3): {len(unique_to_w33)}")
    for name in unique_to_w33:
        print(f"  ★ {name}")

    # ---- PART E: Expected hits under null ----
    print("\n" + "=" * 70)
    print("NULL HYPOTHESIS: EXPECTED COINCIDENCE COUNT")
    print("=" * 70)
    # For each test, compute P(match) = count/total
    # Expected score under random SRG = sum of P(match)
    total = len(results)
    expected = sum(cnt / total for cnt in test_counts.values())
    variance = sum((cnt / total) * (1 - cnt / total) for cnt in test_counts.values())
    std = math.sqrt(variance)
    z_score = (w33_score - expected) / std if std > 0 else 0
    print(f"Expected score (random SRG): {expected:.2f}")
    print(f"Standard deviation: {std:.2f}")
    print(f"W(3,3) score: {w33_score}")
    print(f"Z-score: {z_score:.2f}")
    print(f"Interpretation: W(3,3) is {z_score:.1f}σ above the mean")

    # ---- PART F: Ties at W(3,3)'s score ----
    tied = [(s2, m2) for sc2, s2, m2 in results if sc2 == w33_score]
    print(f"\nSRGs with SAME score as W(3,3) ({w33_score}): {len(tied)}")
    for s2, m2 in tied[:10]:
        label = f"SRG({s2['v']},{s2['k']},{s2['lam']},{s2['mu']})"
        print(f"  {label}: {sorted(m2.keys())}")
