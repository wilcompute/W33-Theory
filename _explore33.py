import math
from fractions import Fraction

q = 3; lam = 2; mu = 4; k = 12; v = 40; f = 24; g = 15
E = 240; T = 160; Phi3 = 13; Phi6 = 7; Phi12 = 73; Theta = 10
N_eff = 55; r = 2; s = -4

print('=== JACOBI THETA FUNCTIONS ===')
# theta_3(0, q) = sum_{n=-inf}^{inf} q^{n^2}
# For the Leech lattice theta series:
# Theta_Lambda(q) = 1 + 196560*q^4 + 16773120*q^6 + ...
# = 1 + sum a_n q^{2n} where the norm squared is 2n
# Shell multiplicities: 
#  n=0: 1
#  n=1: 0 (no vectors of norm 2 - unimodular!)
#  n=2: 196560 = mu^2*q^3*(mu+1)*Phi6*Phi3
#  n=3: 16773120 = lam^k * q^2 * (mu+1) * Phi6 * Phi3 (from Phase 23)
#  n=4: 398034000

# Shell 5 and beyond
print('=== LEECH LATTICE SHELLS 5+ ===')
# Using theta series: a_n = (65520/691) * (sigma_11(n) - tau(n))
# where sigma_11 is sum of 11th powers of divisors, tau is Ramanujan tau

def sigma11(n):
    s = 0
    for d in range(1, n+1):
        if n % d == 0:
            s += d**11
    return s

# Ramanujan tau
def ram_tau(n):
    # Use the product formula truncated
    # Delta = q * prod_{n>=1} (1-q^n)^24
    # Truncate to sufficient terms
    if n == 0: return 0
    N = max(n + 50, 100)
    coeffs = [0] * (N + 1)
    coeffs[0] = 1
    for m in range(1, N + 1):
        new_coeffs = [0] * (N + 1)
        for j in range(N + 1):
            if coeffs[j] == 0: continue
            for e in range(N + 1):
                idx = j + e * m
                if idx > N: break
                # (1 - x^m)^24: coefficient of x^{e*m} in (1-x^m)^24
                # = C(24, e) * (-1)^e
                if e > 24: break
                c = 1
                for t in range(e):
                    c = c * (24 - t) // (t + 1)
                c *= (-1)**e
                new_coeffs[idx] += coeffs[j] * c
        coeffs = new_coeffs
    # Delta = sum_{n>=0} coeffs[n] * q^{n+1}
    # So tau(n) = coeffs[n-1]
    if n - 1 >= len(coeffs): return None
    return coeffs[n - 1]

for n in range(1, 9):
    tn = ram_tau(n)
    s11 = sigma11(n)
    shell = Fraction(65520, 691) * (s11 - tn)
    print('  shell_%d: sigma_11(%d) = %d, tau(%d) = %d' % (n, n, s11, n, tn))
    print('    a_%d = (65520/691) * (%d - %d) = %s' % (n, s11, tn, shell))

print()
print('=== FACTORIZE SHELL MULTIPLICITIES ===')

def factorize(n):
    if n == 0: return '0'
    sgn = '-' if n < 0 else ''
    n = abs(n)
    if n == 1: return sgn + '1'
    factors = []
    for pr in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193]:
        while n % pr == 0:
            factors.append(pr)
            n //= pr
        if n == 1: break
    if n > 1: factors.append(n)
    return sgn + ' * '.join(str(x) for x in factors)

shells = {}
for n in range(1, 9):
    tn = ram_tau(n)
    s11 = sigma11(n)
    a = Fraction(65520, 691) * (s11 - tn)
    if a.denominator == 1:
        shells[n] = int(a)
        print('shell_%d = %d = %s' % (n, int(a), factorize(int(a))))
    else:
        print('shell_%d = %s (not integer!)' % (n, a))

print()
print('=== E_8 LATTICE THETA SERIES ===')
# Theta_{E8}(q) = 1 + 240*q^2 + 2160*q^4 + 6720*q^6 + ...
# = 1 + sum_{n>=1} 240*sigma_3(n)*q^{2n}
# So coefficient of q^{2n} = 240*sigma_3(n)
for n in range(1, 11):
    s3 = 0
    for d in range(1, n+1):
        if n % d == 0:
            s3 += d**3
    coeff = 240 * s3
    print('E8_shell_%d = E*sigma_3(%d) = 240*%d = %d = %s' % (n, n, s3, coeff, factorize(coeff)))

print()
print('=== CONWAY-NORTON MONSTER: MONSTROUS MOONSHINE ===')
# j(tau) = q^{-1} + 744 + 196884q + 21493760q^2 + ...
# 196884 = 196560 + 324 = Leech_shell_2 + 18^2
# 196884 = 4 * 49221 = 4 * 3 * 16407 = 12 * 16407
# 16407 = 3 * 5469 = 3 * 3 * 1823 = 9 * 1823. 1823 prime.
# So 196884 = 2^2 * 3^3 * 1823
j1 = 196884
print('j_1 = 196884 = %s' % factorize(j1))
# 196884 / 4 = 49221 = 3^3 * 1823
# 1823 is prime. Not clean.

# 744 = 8*93 = 8*3*31 = lam^3*q*31
# 744 = 24*31 = f*31
print('744 = f*31 = %s' % factorize(744))

# 21493760 = ?
j2 = 21493760
print('j_2 = 21493760 = %s' % factorize(j2))

# The McKay observation: 196884 = 1 + 196883
# 196883 is the dimension of the smallest faithful rep of the Monster!
# dim(V1) = 196883 = 47*59*71
print('dim(Monster V1) = 196883 = %s' % factorize(196883))

print()
print('=== DOUBLE FACTORIALS ===')
# (2n-1)!! = 1*3*5*...*(2n-1)
for n in range(1, 13):
    df = 1
    for i in range(1, 2*n, 2):
        df *= i
    print('  (%d)!! = %d = %s' % (2*n-1, df, factorize(df)))

print()
print('=== STIRLING NUMBERS S(n,k) DEEPER ===')
# S(n,2) = 2^{n-1} - 1
for n in range(2, 16):
    sn2 = 2**(n-1) - 1
    print('  S(%d, lam) = %d = %s' % (n, sn2, factorize(sn2)))

print()
print('=== POCHHAMMER / RISING FACTORIAL ===')
# (q)_n = q*(q+1)*...*(q+n-1) "q-ascending"
for n in range(1, 11):
    poch = 1
    for i in range(n):
        poch *= (q + i)
    print('  (q)_%d = %d = %s' % (n, poch, factorize(poch)))

print()
print('=== CONTINUED FRACTION OF SQRT(v) ===')
# sqrt(40) = 6.324...
# CF: [6; 3, 12, 3, 12, ...]  period 2!
import decimal
decimal.getcontext().prec = 50
sv = decimal.Decimal(v).sqrt()
print('sqrt(v) = sqrt(40) = %s' % sv)
# CF computation
val = sv
cf = []
for _ in range(10):
    a = int(val)
    cf.append(a)
    rem = val - a
    if rem < 1e-30: break
    val = 1 / rem
print('CF(sqrt(v)) = %s' % cf)
# [6, 3, 12, 3, 12, ...] -> period = [3, 12] = [q, k]!
print('  Period: [q, k] = [3, 12]!')
# sqrt(40) = [6; 3, 12, 3, 12, ...]  integer part = q! = 6

print()
print('=== CONTINUED FRACTION OF SQRT(N_eff) ===')
sn = decimal.Decimal(N_eff).sqrt()
print('sqrt(N_eff) = sqrt(55) = %s' % sn)
val = sn
cf2 = []
for _ in range(12):
    a = int(val)
    cf2.append(a)
    rem = val - a
    if rem < 1e-30: break
    val = 1 / rem
print('CF(sqrt(N_eff)) = %s' % cf2)

print()
print('=== CONTINUED FRACTION OF SQRT(Phi12) ===')
sp = decimal.Decimal(Phi12).sqrt()
print('sqrt(Phi12) = sqrt(73) = %s' % sp)
val = sp
cf3 = []
for _ in range(12):
    a = int(val)
    cf3.append(a)
    rem = val - a
    if rem < 1e-30: break
    val = 1 / rem
print('CF(sqrt(Phi12)) = %s' % cf3)
