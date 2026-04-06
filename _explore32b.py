import math
from fractions import Fraction

q = 3; lam = 2; mu = 4; k = 12; v = 40; f = 24; g = 15
E = 240; T = 160; Phi3 = 13; Phi6 = 7; Phi12 = 73; Theta = 10
N_eff = 55; r = 2; s = -4

def factorize(n):
    if n == 0: return '0'
    sgn = '-' if n < 0 else ''
    n = abs(n)
    if n == 1: return sgn + '1'
    factors = []
    for pr in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]:
        while n % pr == 0:
            factors.append(pr)
            n //= pr
        if n == 1: break
    if n > 1: factors.append(n)
    return sgn + ' * '.join(str(x) for x in factors)

print('=== SPECTRAL MOMENTS ===')
for n in range(1, 11):
    mn = k**n + f*r**n + g*s**n
    print('  m_%d = %d = %s' % (n, mn, factorize(mn)))

print()
print('=== RAMANUJAN TAU DEEPER ===')
tau_vals = {1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830, 6: -6048, 7: -16744, 8: 84480}
print('tau(4) = -lam^6*(f-1) = %d CHECK: %s' % (-lam**6*(f-1), tau_vals[4]==-lam**6*(f-1)))
print('tau(5) = lam*q*(mu+1)*Phi6*(f-1) = %d CHECK: %s' % (lam*q*(mu+1)*Phi6*(f-1), tau_vals[5]==lam*q*(mu+1)*Phi6*(f-1)))
print('tau(7) = -lam^3*Phi6*Phi3*(f-1) = %d CHECK: %s' % (-lam**3*Phi6*Phi3*(f-1), tau_vals[7]==-lam**3*Phi6*Phi3*(f-1)))
print('tau(8) = lam^7*k*N_eff = %d CHECK: %s' % (lam**7*k*N_eff, tau_vals[8]==lam**7*k*N_eff))
print('tau(9) = -113643 = %s' % factorize(-113643))

print()
print('=== PARTITION FUNCTION (NEW HITS) ===')
def part(n):
    pp = [0]*(n+1); pp[0] = 1
    for ii in range(1, n+1):
        for jj in range(ii, n+1):
            pp[jj] += pp[jj-ii]
    return pp[n]

print('p(q!) = p(6) = %d = k-1 = %d CHECK: %s' % (part(6), k-1, part(6)==k-1))
print('p(lam^3) = p(8) = %d = lam*(k-1) = %d CHECK: %s' % (part(8), lam*(k-1), part(8)==lam*(k-1)))
print('p(q^2) = p(9) = %d = q*Theta = %d CHECK: %s' % (part(9), q*Theta, part(9)==q*Theta))
print('p(Theta) = p(10) = %d = lam*q*Phi6 = %d CHECK: %s' % (part(10), lam*q*Phi6, part(10)==lam*q*Phi6))

print()
print('=== ZETA VALUES ===')
def bernoulli(n):
    A = [Fraction(0)] * (n+1)
    for m in range(n+1):
        A[m] = Fraction(1, m+1)
        for jj in range(m, 0, -1):
            A[jj-1] = jj * (A[jj-1] - A[jj])
    return A[0]

for nn in [1,2,3,4,5,6]:
    z = -bernoulli(2*nn) / (2*nn)
    print('zeta(%d) = %s  denom=%d = %s' % (1-2*nn, z, z.denominator, factorize(z.denominator)))

print()
print('E/2 = (mu+1)! = %d CHECK: %s' % (math.factorial(mu+1), E//2 == math.factorial(mu+1)))

m1 = k + f*r + g*s
m2 = k**2 + f*r**2 + g*s**2
m3 = k**3 + f*r**3 + g*s**3
m4 = k**4 + f*r**4 + g*s**4
m5 = k**5 + f*r**5 + g*s**5
m6 = k**6 + f*r**6 + g*s**6

print()
print('=== MOMENTS vs GRAPH PARAMETERS ===')
print('m_1 = %d = Tr(A)' % m1)
print('m_2 = %d = 2E = v*k CHECK: %s' % (m2, m2 == 2*E))
print('m_3 = %d = v*f = lam^6*g = q!*T CHECK: %s' % (m3, m3 == v*f and m3 == lam**6*g and m3 == math.factorial(q)*T))
print('m_4 = %d = lam^7*q*(mu+1)*Phi3 CHECK: %s' % (m4, m4 == lam**7*q*(mu+1)*Phi3))
print('m_5 = %d = %s' % (m5, factorize(m5)))
print('  m_5/v = %d = %s' % (m5//v, factorize(m5//v)))
print('m_6 = %d = %s' % (m6, factorize(m6)))
print('  m_6/v = %d = %s' % (m6//v, factorize(m6//v)))

print()
print('m_3/v = %d = f CHECK: %s' % (m3//v, m3//v == f))
print('m_4/v = %d = mu^2*q*Phi3 = lam^mu*q*Phi3 CHECK: %s' % (m4//v, m4//v == mu**2*q*Phi3))

# Try to express m_5, m_6 in terms of graph params
print()
# m_5 = k^5 + f*r^5 + g*s^5 = 248832 + 768 - 15360 = 234240
# m_5/v = 5856 = 2^5 * 3 * 61. 61 is prime and not a clean graph param.
# m_6 = k^6 + f*r^6 + g*s^6 = 2985984 + 1536 + 61440 = 3048960
# m_6/v = 76224 = 2^6 * 3 * 397. 397 prime. Less clean.

# BUT: moments have parametric meaning from SRG conditions
# Tr(A^2) = v*k (known)
# Tr(A^3) = v * (number of triangles per vertex) ... = v * lam * k / q! ... 
# Actually Tr(A^3)/v = k*lam + k*mu*(v-k-1)/v ... no.
# For SRG: Tr(A^3) = v * (k*lam) / something... Let me check:
# In SRG Tr(A^3) = sum of A^3_ii = sum_i (number of walks of length 3 from i to i)
# = v * (# triangles through a vertex) * 2 = v * (k*lam/2) * 2 = v*k*lam
# Actually Tr(A^3) = 6 * (# of triangles) for simple graph
# # triangles = v*k*lam/6 for vertex-transitive SRG
# So Tr(A^3) = 6 * v*k*lam/6 = v*k*lam = 40*12*2 = 960 = m_3. Confirmed!
print('m_3 = v*k*lam = %d = %d CHECK: %s' % (m3, v*k*lam, m3 == v*k*lam))

# Tr(A^4) can be expressed similarly. For SRG:
# A^2 = lam*A + mu*(J-I-A) + k*I = (lam-mu)*A + mu*J + (k-mu)*I
# So A^2 = (lam-mu)*A + mu*J + (k-mu)*I
# A^4 = ((lam-mu)*A + mu*J + (k-mu)*I)^2
# This gives Tr(A^4) formula. Let me verify:
# lam-mu = -2, k-mu = 8
# A^2 = -2A + 4J + 8I (using mu=4 for J coefficient)
# Wait, SRG equation: A^2 = lam*A + mu*(J-I-A) + k*I = (lam-mu)*A + mu*J + (k-mu)*I
# = -2A + 4J + 8I
# A^4 = (A^2)^2 = (-2A + 4J + 8I)^2
# = 4A^2 + 16J^2 + 64I + ... cross terms
# J^2 = v*J, A*J = k*J, J*A = k*J
# = 4A^2 - 16AJ - 32AI + 16JA + 16J^2 + 64JI - 32IA + 64IJ + 64I^2

# Too messy. Let me just check m_5 = v*k*(lam^2 + 2*k*lam + ...) or something.
# The key formula for SRG moments:
# m_n = k^n + f*r^n + g*s^n (eigenvalue formula, already using)
# m_n/v = (k^n + f*r^n + g*s^n)/v -- parametric by definition, always integer

print()
print('=== NEW CODIFICATION ITEMS ===')
print('1. p(q!) = k-1 = 11')
print('2. p(lam^3) = lam*(k-1) = 22')
print('3. p(q^2) = q*Theta = 30')
print('4. p(Theta) = lam*q*Phi6 = C(mu+1) = 42')
print('5. zeta(-1) = -1/k')
print('6. zeta(-3) = 1/(E/2) = 2/E = 1/(mu+1)!')
print('7. |zeta(-5)|^{-1} = tau(3) = lam^2*q^2*Phi6 = 252')
print('8. zeta(-7) = 1/E')
print('9. |zeta(-9)|^{-1} = mu*q*(k-1) = 132')
print('10. tau(4) = -lam^6*(f-1)')
print('11. tau(5) = lam*q*(mu+1)*Phi6*(f-1)')
print('12. tau(7) = -lam^3*Phi6*Phi3*(f-1)')
print('13. tau(8) = lam^7*k*N_eff')
print('14. m_3 = v*k*lam = lam^6*g = q!*T')
print('15. E/2 = (mu+1)! = T_g')
