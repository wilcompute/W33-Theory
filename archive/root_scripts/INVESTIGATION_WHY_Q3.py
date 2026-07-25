"""
DEEP INVESTIGATION: Why q = 3?
===============================
Compute W(q,q) generalized quadrangle SRG parameters for q = 2,3,4,5,7,8,9
and check which physics constraints each one satisfies.

The selection principle: q=3 should be the ONLY value where all constraints
are simultaneously satisfiable.
"""
from fractions import Fraction
import math

def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0: return False
    return True

def srg_params(q):
    """Compute SRG parameters for W(q,q) generalized quadrangle."""
    v = (q + 1) * (q**2 + 1)
    k = q * (q + 1)
    lam = q - 1
    mu = q + 1
    
    # Eigenvalues of SRG with these parameters
    # r, s are roots of x² - (λ - μ)x - (k - μ) = 0
    # = x² - (q-1-(q+1))x - (q(q+1)-(q+1)) = x² + 2x - (q+1)(q-1) = x² + 2x - (q²-1)
    # Wait, let me use the standard formula:
    # r, s = ((λ-μ) ± √((λ-μ)² + 4(k-μ))) / 2
    disc = (lam - mu)**2 + 4*(k - mu)
    sqrt_disc = math.isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None  # Not a perfect square — can't be SRG (shouldn't happen for GQ)
    
    r = ((lam - mu) + sqrt_disc) // 2
    s = ((lam - mu) - sqrt_disc) // 2
    
    # Multiplicities
    # f = k(s+1)(s-λ) / (μ(s-r))  ... using standard formulas
    # f = (v-1)*(-s)*(s+1)/(k-s)(r-s) ... let me use the direct formula
    # For W(q,q): r = q-1, s = -(q+1)
    # f = q(q²+1), g = q²(q+1)   ... let me compute from formula
    
    # Standard: f = k(k-s)(μ-s-1) / (μ(r-s)(r+1))... 
    # Actually, easiest for GQ(q,q):
    # f = v·(k+s) / (k+s - r·(v-1-k)/(k-s)... let me just use:
    # f·r + g·s = -k, f + g = v - 1
    # So f = (v-1)·s + k) / (s - r)... wait:
    # f + g = v - 1
    # f·r + g·s = -k
    # => f·r + (v-1-f)·s = -k
    # => f·(r-s) = -k - (v-1)·s
    # => f = (-k - (v-1)·s) / (r - s)
    
    f = (-k - (v - 1) * s) // (r - s)
    g = v - 1 - f
    
    E = v * k // 2  # edges
    
    return {
        'q': q, 'v': v, 'k': k, 'lam': lam, 'mu': mu,
        'r': r, 's': s, 'f': f, 'g': g, 'E': E,
        'disc': disc, 'sqrt_disc': sqrt_disc
    }

def check_physics(p):
    """Check all physics constraints for a W(q,q) graph.
    Returns dict of constraint name -> (passes: bool, detail: str)."""
    q = p['q']
    v, k, lam, mu = p['v'], p['k'], p['lam'], p['mu']
    r, s, f, g, E = p['r'], p['s'], p['f'], p['g'], p['E']
    
    results = {}
    
    # === GAUGE GROUP ===
    # SM gauge: SU(3)×SU(2)×U(1) has dim 8+3+1 = 12
    results['SM gauge dim = k'] = (k == 12, f'k={k}')
    
    # SU(5) GUT: dim = N²-1 for N = fund rep
    # Need f = N²-1 for some integer N
    su5_N = None
    for N in range(2, 100):
        if N*N - 1 == f:
            su5_N = N
            break
    results['SU(5): f = N²-1'] = (su5_N is not None, f'f={f}, N={su5_N}')
    
    # SO(10): dim = N(N-1)/2, need C(alpha,2) where alpha = v/(mu)... 
    # Actually: alpha = v·|s|/(k+|s|) for SRG
    alpha = Fraction(v * abs(s), k + abs(s))
    results['Lovász α integer'] = (alpha.denominator == 1, f'α={alpha}')
    alpha_int = int(alpha) if alpha.denominator == 1 else None
    if alpha_int:
        so10_dim = alpha_int * (alpha_int - 1) // 2
        results['SO(10): C(α,2) = 45'] = (so10_dim == 45, f'C({alpha_int},2)={so10_dim}')
    else:
        results['SO(10): C(α,2) = 45'] = (False, f'α not integer')
    
    # === FERMION CONTENT ===
    # SM fermions/gen (no ν_R) should be 15
    results['SM fermions g=15'] = (g == 15, f'g={g}')
    
    # SO(10) spinor = s² should be 16  
    results['SO(10) spinor s²=16'] = (s**2 == 16, f's²={s**2}')
    
    # 3 generations
    results['q=3 generations'] = (q == 3, f'q={q}')
    
    # === LIE ALGEBRAS ===
    # dim(E₈) = 248: need E + k - mu = 248 (or some formula)
    # For W(q,q): E = v·k/2, dim_E8 should be derivable  
    # In our theory: dim(E₈) = E + rank(E₈) = E + 8... but what IS rank(E₈)?
    # rank(E₈) = k - mu for q=3 → 12-4=8. Let's check if k-mu=8 always
    rank_e8_candidate = k - mu
    dim_e8_candidate = E + rank_e8_candidate
    results['dim(E₈)=248 from E+k-μ'] = (dim_e8_candidate == 248, f'E+k-μ={E}+{rank_e8_candidate}={dim_e8_candidate}')
    
    # E₈ kissing number = 240 = E
    results['E₈ kissing = E = 240'] = (E == 240, f'E={E}')
    
    # dim(E₆) = 78 = 2v - λ
    dim_e6_candidate = 2*v - lam
    results['dim(E₆)=78 from 2v-λ'] = (dim_e6_candidate == 78, f'2v-λ={dim_e6_candidate}')
    
    # dim(F₄) = 52 = v + k
    dim_f4_candidate = v + k
    results['dim(F₄)=52 from v+k'] = (dim_f4_candidate == 52, f'v+k={dim_f4_candidate}')
    
    # === GOLAY CODE ===
    # [f, k, k-mu] should be [24, 12, 8]
    results['Golay [f,k,k-μ]=[24,12,8]'] = (
        f == 24 and k == 12 and k - mu == 8,
        f'[{f},{k},{k-mu}]'
    )
    
    # === MAGIC SQUARE ROW C = 137 ===
    ms_A2 = k - mu     # 8
    ms_A2A2 = k + mu   # 16
    # C(Φ₆,3) where Φ₆ = (q⁶-1)/lcm(lower) = ... for generic q this is harder
    # For q=3: Φ₆ = Φ₆(3) = 3⁶-1 factored... = 7
    # Actually Φ_n(q) = cyclotomic polynomial evaluated at q
    # Φ₁(q) = q-1, Φ₂(q) = q+1, Φ₃(q) = q²+q+1, Φ₆(q) = q²-q+1
    phi6 = q**2 - q + 1
    phi3 = q**2 + q + 1
    ms_A5 = phi6 * (phi6 - 1) * (phi6 - 2) // 6  # C(Φ₆, 3)
    dim_e6_ms = 2*v - lam  # E₆ dim
    row_C = ms_A2 + ms_A2A2 + ms_A5 + dim_e6_ms
    results['Magic square row C = 137'] = (row_C == 137, f'row_C={row_C}')
    
    # === MERSENNE PRIMES ===
    # Check if {lam, q, q+r, phi6, phi3} are all Mersenne exponents
    mersenne_candidates = [lam, q, q + r, phi6, phi3]
    is_mersenne = [is_prime(2**p - 1) for p in mersenne_candidates if p > 0]
    all_mersenne = all(is_mersenne) and len(mersenne_candidates) == 5
    results['All 5 params Mersenne exp'] = (all_mersenne, 
        f'{mersenne_candidates} → {is_mersenne}')
    
    # === PERFECT NUMBERS ===
    # First perfect = k/lam = 6?
    if lam > 0:
        perf1_candidate = k // lam if k % lam == 0 else -1
        results['1st perfect k/λ=6'] = (perf1_candidate == 6, f'k/λ={k}/{lam}={perf1_candidate}')
    else:
        results['1st perfect k/λ=6'] = (False, f'λ=0')
    
    # 2nd perfect = v-k = 28?
    results['2nd perfect v-k=28'] = (v - k == 28, f'v-k={v-k}')
    
    # === SPORADIC GROUPS ===
    results['26 sporadics = f+λ'] = (f + lam == 26, f'f+λ={f+lam}')
    
    # === SM PARTICLE COUNT ===
    results['SM particles k+f+μ=v'] = (k + f + mu == v, f'k+f+μ={k+f+mu}, v={v}')
    
    # === VERTEX COUNT ===
    # v = 40 specifically
    results['v = 40'] = (v == 40, f'v={v}')
    
    # === STRING DIMENSIONS ===
    # Superstring D=10 = alpha
    if alpha_int:
        results['D_super = α = 10'] = (alpha_int == 10, f'α={alpha_int}')
    else:
        results['D_super = α = 10'] = (False, f'α not int')
    # Bosonic D=26 = f+lambda
    results['D_bosonic = f+λ = 26'] = (f + lam == 26, f'f+λ={f+lam}')
    # M-theory D=11 = ?
    
    # === E₈ DECOMPOSITION ===
    # E₈ → E₆ × SU(q): adjoint + color + matter + antimatter
    # 78 + 8 + 27q + 27q = 248?
    k_comp = v - k - 1 + mu  # complement degree... actually k̄ = v-k-1
    k_comp_real = v - k - 1
    # For q=3: k̄ = 27, decomp = 78+8+81+81=248
    # General: dim_E6 + (k-mu) + 2×k̄×q = ?
    decomp = dim_e6_ms + (k - mu) + 2 * k_comp_real * q
    results['E₈ decomp sums to 248'] = (decomp == 248, 
        f'{dim_e6_ms}+{k-mu}+2×{k_comp_real}×{q}={decomp}')
    
    # === FIBONACCI ===
    # Magic square total = F(k+mu)?
    # Compute magic square total
    ms_C3 = phi6 * (phi6 - 1) // 2  # C(Φ₆, 2)
    dim_e7a = v * q + phi3  # 133 for q=3
    row_R = q + ms_A2 + ms_C3 + dim_f4_candidate
    row_H = ms_C3 + ms_A5 + k*(k-1)//2 + dim_e7a
    row_O = dim_f4_candidate + dim_e6_ms + dim_e7a + dim_e8_candidate
    total_ms = row_R + row_C + row_H + row_O
    # Fibonacci
    a, b = 0, 1
    for _ in range(k + mu):
        a, b = b, a + b
    fib_kmu = a
    results['MS total = Fibonacci(k+μ)'] = (total_ms == fib_kmu, 
        f'total={total_ms}, F({k+mu})={fib_kmu}')
    
    # === COXETER ===
    # h(E₈) = v - alpha should be 30
    if alpha_int:
        h_e8 = v - alpha_int
        results['h(E₈) = v-α = 30'] = (h_e8 == 30, f'v-α={v}-{alpha_int}={h_e8}')
    else:
        results['h(E₈) = v-α = 30'] = (False, 'α not int')
    
    # === MONSTER ===
    # g = 15 = number of Monster prime factors
    results['Monster primes = g = 15'] = (g == 15, f'g={g}')
    
    return results

print("=" * 100)
print("  INVESTIGATION: W(q,q) GENERALIZED QUADRANGLES FOR q = 2, 3, 4, 5, 7, 8, 9")
print("  Which field order q produces a self-consistent physics?")
print("=" * 100)

# Only prime powers are valid for GQ
prime_powers = [2, 3, 4, 5, 7, 8, 9]

all_results = {}
for q in prime_powers:
    p = srg_params(q)
    if p is None:
        print(f"\nq={q}: NOT A VALID SRG")
        continue
    
    print(f"\n{'─'*100}")
    print(f"  W({q},{q}):  v={p['v']}, k={p['k']}, λ={p['lam']}, μ={p['mu']}")
    print(f"  eigenvalues r={p['r']}, s={p['s']}")
    print(f"  multiplicities f={p['f']}, g={p['g']},  E={p['E']}")
    print(f"{'─'*100}")
    
    results = check_physics(p)
    all_results[q] = results
    
    passes = sum(1 for v in results.values() if v[0])
    total = len(results)
    
    for name, (passed, detail) in results.items():
        status = "✓ PASS" if passed else "✗ fail"
        print(f"  {status}  {name}: {detail}")
    
    print(f"\n  SCORE: {passes}/{total} constraints satisfied")

# === SUMMARY TABLE ===
print(f"\n\n{'='*100}")
print("  SUMMARY: CONSTRAINT SATISFACTION BY FIELD ORDER q")
print(f"{'='*100}")

constraint_names = list(all_results[3].keys())

# Header
print(f"{'Constraint':<35}", end="")
for q in prime_powers:
    if q in all_results:
        print(f"  q={q:<3}", end="")
print()
print("─" * 35 + "─" * 7 * len([q for q in prime_powers if q in all_results]))

for name in constraint_names:
    print(f"{name:<35}", end="")
    for q in prime_powers:
        if q in all_results:
            passed = all_results[q][name][0]
            print(f"  {'✓':<4}" if passed else f"  {'✗':<4}", end="")
    print()

print()
print("─" * 35 + "─" * 7 * len([q for q in prime_powers if q in all_results]))
print(f"{'TOTAL':<35}", end="")
for q in prime_powers:
    if q in all_results:
        score = sum(1 for v in all_results[q].values() if v[0])
        total = len(all_results[q])
        print(f"  {score}/{total:<3}", end="")
print()

# === THE KEY QUESTION ===
print(f"\n\n{'='*100}")
print("  THE SELECTION PRINCIPLE")
print(f"{'='*100}")

q3_score = sum(1 for v in all_results[3].values() if v[0])
q3_total = len(all_results[3])
print(f"\n  q=3 satisfies {q3_score}/{q3_total} constraints.")

best_non3 = 0
best_q = None
for q in prime_powers:
    if q != 3 and q in all_results:
        score = sum(1 for v in all_results[q].values() if v[0])
        if score > best_non3:
            best_non3 = score
            best_q = q
print(f"  Best non-q=3: q={best_q} with {best_non3}/{q3_total} constraints.")
print(f"  Gap: {q3_score - best_non3} constraints uniquely satisfied by q=3")

# What constraints does ONLY q=3 satisfy?
print(f"\n  Constraints satisfied ONLY by q=3:")
for name in constraint_names:
    only_q3 = all_results[3][name][0] and all(
        not all_results[q][name][0] for q in prime_powers if q != 3 and q in all_results
    )
    if only_q3:
        print(f"    ★ {name}: {all_results[3][name][1]}")

# What constraint does q=3 fail?
print(f"\n  Constraints q=3 FAILS:")
for name in constraint_names:
    if not all_results[3][name][0]:
        print(f"    ✗ {name}: {all_results[3][name][1]}")
