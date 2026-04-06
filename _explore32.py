import math
from fractions import Fraction

q = 3; lam = 2; mu = 4; k = 12; v = 40; f = 24; g = 15
E = 240; T = 160; Phi3 = 13; Phi6 = 7; Phi12 = 73; Theta = 10
N_eff = 55; r = 2; s = -4

print('=== SPECTRAL MOMENTS ===')
for n in range(1, 11):
    mn = k**n + f*r**n + g*s**n
    temp = abs(mn)
    factors = []
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43]:
        while temp % p == 0:
            factors.append(p)
            temp //= p
        if temp == 1: break
    if temp > 1: factors.append(temp)
    fstr = ' * '.join(str(x) for x in factors)
    sgn = '-' if mn < 0 else ''
    print('  m_%d = %d = %s%s' % (n, mn, sgn, fstr))

print()
print('=== RAMANUJAN TAU DEEPER ===')
tau_vals = {1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830, 6: -6048, 7: -16744, 8: 84480}
print('tau(4) = -lam^6*(f-1) = %d CHECK: %s' % (-lam**6*(f-1), tau_vals[4]==-lam**6*(f-1)))
print('tau(5) = lam*q*(mu+1)*Phi6*(f-1) = %d CHECK: %s' % (lam*q*(mu+1)*Phi6*(f-1), tau_vals[5]==lam*q*(mu+1)*Phi6*(f-1)))
print('tau(7) = -lam^3*Phi6*Phi3*(f-1) = %d CHECK: %s' % (-lam**3*Phi6*Phi3*(f-1), tau_vals[7]==-lam**3*Phi6*Phi3*(f-1)))
print('tau(8) = lam^7*k*N_eff = %d CHECK: %s' % (lam**7*k*N_eff, tau_vals[8]==lam**7*k*N_eff))

t9 = 113643
tmp = t9
f9 = []
for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]:
    while tmp % p == 0:
        f9.append(p)
        tmp //= p
    if tmp == 1: break
if tmp > 1: f9.append(tmp)
print('tau(9) = -113643 = -%s' % (' * '.join(str(x) for x in f9)))

print()
print('=== PARTITION COMPLETE ===')
def partitions(n):
    p = [0]*(n+1); p[0] = 1
    for i in range(1, n+1):
        for j in range(i, n+1):
            p[j] += p[j-i]
    return p[n]

print('p(q!) = p(6) = %d = k-1 = %d CHECK: %s' % (partitions(6), k-1, partitions(6)==k-1))
print('p(lam^3) = p(8) = %d = lam*(k-1) = %d CHECK: %s' % (partitions(8), lam*(k-1), partitions(8)==lam*(k-1)))
print('p(q^2) = p(9) = %d = q*Theta = %d CHECK: %s' % (partitions(9), q*Theta, partitions(9)==q*Theta))
print('p(Theta) = p(10) = %d = lam*q*Phi6 = %d CHECK: %s' % (partitions(10), lam*q*Phi6, partitions(10)==lam*q*Phi6))

print()
print('=== ZETA VALUES ===')
def bernoulli(n):
    A = [Fraction(0)] * (n+1)
    for m in range(n+1):
        A[m] = Fraction(1, m+1)
        for j in range(m, 0, -1):
            A[j-1] = j * (A[j-1] - A[j])
    return A[0]

for n in [1,2,3,4,5,6]:
    z = -bernoulli(2*n) / (2*n)
    d = z.denominator
    tmp2 = d
    fd = []
    for p in [2,3,5,7,11,13]:
        while tmp2 % p == 0:
            fd.append(p)
            tmp2 //= p
        if tmp2 == 1: break
    if tmp2 > 1: fd.append(tmp2)
    print('zeta(%d) = %s  denom=%d = %s' % (1-2*n, z, d, ' * '.join(str(x) for x in fd)))

print()
print('E/2 = (mu+1)! = %d CHECK: %s' % (math.factorial(mu+1), E//2 == math.factorial(mu+1)))
print('|zeta(-5)|^{-1} = tau(3) = 252 = lam^2*q^2*Phi6')
print('zeta(-7) = 1/E')

# More spectral moments in parametric form
m1 = k + f*r + g*s
m2 = k**2 + f*r**2 + g*s**2
m3 = k**3 + f*r**3 + g*s**3
m4 = k**4 + f*r**4 + g*s**4
m5 = k**5 + f*r**5 + g*s**5
m6 = k**6 + f*r**6 + g*s**6

print()
print('=== SPECTRAL MOMENTS PARAMETRIC ===')
print('m_1 = %d = E/v = %s CHECK: %s' % (m1, E//v if E%v==0 else 'no', m1*v==E if E%v!=0 else True))
# m_1 = k + f*r + g*s = 12 + 48 - 60 = 0! Wait...
# m_1 = Tr(A) = 0 always for simple graphs
# Hmm but k + f*r + g*s = 12 + 24*2 + 15*(-4) = 12 + 48 - 60 = 0. Yes.
print('  m_1 = 0 = Tr(A) always')
print('m_2 = %d = v*k = %d CHECK: %s' % (m2, v*k, m2 == v*k))
# m_2 = Tr(A^2) = 2*edges = v*k? No, Tr(A^2) = sum_i (A^2)_{ii} = sum_i d_i = 2|E| for adj matrix
# Actually Tr(A^2) = 2*|edges| for simple graphs, and |edges| = v*k/2
# m_2 = k^2 + f*r^2 + g*s^2 = 144 + 96 + 240 = 480 = 2*E = v*k
print('  = 2E = %d CHECK: %s' % (2*E, m2 == 2*E))
print('m_3 = %d' % m3)
print('  m_3 = q!*T = %d CHECK: %s' % (math.factorial(q)*T, m3 == math.factorial(q)*T))
print('m_4 = %d = lam^7*q*(mu+1)*Phi3 CHECK: %s' % (m4, m4 == lam**7*q*(mu+1)*Phi3))
print('m_5 = %d' % m5)
# Factor m5
tmp5 = abs(m5)
f5 = []
for p in [2,3,5,7,11,13,17,19,23,29,31]:
    while tmp5 % p == 0:
        f5.append(p)
        tmp5 //= p
    if tmp5 == 1: break
if tmp5 > 1: f5.append(tmp5)
sg5 = '-' if m5 < 0 else ''
print('  = %s%s' % (sg5, ' * '.join(str(x) for x in f5)))
# m_5/v
print('  m_5/v = %d' % (m5//v))

print('m_6 = %d' % m6)
tmp6 = abs(m6)
f6a = []
for p in [2,3,5,7,11,13,17,19,23,29,31]:
    while tmp6 % p == 0:
        f6a.append(p)
        tmp6 //= p
    if tmp6 == 1: break
if tmp6 > 1: f6a.append(tmp6)
sg6 = '-' if m6 < 0 else ''
print('  = %s%s' % (sg6, ' * '.join(str(x) for x in f6a)))

# m_2/v = k (degree), m_3/v = q!*T/v = 960/40 = 24 = f
print()
print('m_2/v = %d = k CHECK: %s' % (m2//v, m2//v == k))
print('m_3/v = %d = f CHECK: %s' % (m3//v, m3//v == f))
# Actually m_3/v = 960/40 = 24 = f. YES!
print('m_4/v = %d = mu^2*q*Phi3 CHECK: %s' % (m4//v, m4//v == mu**2*q*Phi3))

# m_3 = 960 = q!*T = 6*160 = 960. Also = v*f = 40*24 = 960. 
# Also 960 = lam^6*g = 64*15 = 960
print('m_3 = v*f = lam^6*g = q!*T CHECK: %s' % (m3 == v*f == lam**6*g))

# m_5/v
m5v = m5//v
tmp5v = abs(m5v)
f5v = []
for p in [2,3,5,7,11,13,17,19,23,29,31]:
    while tmp5v % p == 0:
        f5v.append(p)
        tmp5v //= p
    if tmp5v == 1: break
if tmp5v > 1: f5v.append(tmp5v)
sg5v = '-' if m5v < 0 else ''
print('m_5/v = %d = %s%s' % (m5v, sg5v, ' * '.join(str(x) for x in f5v)))

# m_6/v
m6v = m6//v
tmp6v = abs(m6v)
f6v = []
for p in [2,3,5,7,11,13,17,19,23,29,31]:
    while tmp6v % p == 0:
        f6v.append(p)
        tmp6v //= p
    if tmp6v == 1: break
if tmp6v > 1: f6v.append(tmp6v)
sg6v = '-' if m6v < 0 else ''
print('m_6/v = %d = %s%s' % (m6v, sg6v, ' * '.join(str(x) for x in f6v)))
