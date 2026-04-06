"""Phase 31 exploration wave 2."""
import math
from fractions import Fraction

q, lam, mu = 3, 2, 4
k, v, f, g = 12, 40, 24, 15
E, T = 240, 160
Theta, Phi3, Phi6, Phi12 = 10, 13, 7, 73
N_eff = 55
r_val, s_val = lam, -mu
fq = math.factorial(q)  # 6

print("=== PHASE 31 WAVE 2 ===")

# --- Padovan sequence ---
print("\n--- Padovan sequence ---")
def padovan(n):
    if n <= 2: return 1
    a, b, c = 1, 1, 1
    for _ in range(3, n+1):
        a, b, c = b, c, a + b
    return c

for n in range(20):
    p = padovan(n)
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v'}
    if p in targets:
        print(f"  Padovan({n}) = {p} = {targets[p]}")

# --- Perrin sequence ---
print("\n--- Perrin sequence ---")
def perrin(n):
    if n == 0: return 3
    if n == 1: return 0
    if n == 2: return 2
    a, b, c = 3, 0, 2
    for _ in range(3, n+1):
        a, b, c = b, c, a + b
    return c

for n in range(25):
    p = perrin(n)
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',N_eff:'N_eff'}
    if p in targets:
        print(f"  Perrin({n}) = {p} = {targets[p]}")

# --- Look-and-say sequence ---
print("\n--- Look-and-say ---")
def look_and_say(s):
    result = []
    i = 0
    while i < len(s):
        ch = s[i]
        count = 1
        while i + count < len(s) and s[i + count] == ch:
            count += 1
        result.append(str(count) + ch)
        i += count
    return "".join(result)

seq = "1"
for i in range(8):
    print(f"  LAS({i+1}): len={len(seq)}")
    seq = look_and_say(seq)

# --- Semiprime counting ---
print("\n--- Semiprimes ---")
def is_semiprime(n):
    count = 0
    for p in range(2, n+1):
        while n % p == 0:
            count += 1
            n //= p
        if count > 2: return False
    return count == 2

for val, name in [(lam,'lam'),(q,'q'),(mu,'mu'),(mu+1,'mu+1'),(fq,'q!'),(Phi6,'Phi6'),
                  (Theta,'Theta'),(k,'k'),(Phi3,'Phi3'),(g,'g'),(f,'f'),(v,'v'),
                  (N_eff,'N_eff'),(E,'E'),(T,'T')]:
    if is_semiprime(val):
        print(f"  {name}={val} is semiprime")

# --- Practical numbers ---
print("\n--- Practical numbers ---")
def is_practical(n):
    if n == 1: return True
    divs = sorted([d for d in range(1, n+1) if n % d == 0])
    for m in range(1, n+1):
        # Can we write m as subset sum of divs?
        # Simple check: use sigma property
        pass
    # Use Srinivasan criterion
    factors = []
    temp = n
    for p in range(2, n+1):
        if temp % p == 0:
            exp = 0
            while temp % p == 0:
                exp += 1
                temp //= p
            factors.append((p, exp))
        if temp == 1: break
    if not factors: return False
    factors.sort()
    sigma_prod = 1
    for i, (p, e) in enumerate(factors):
        if i > 0 and p > 1 + sigma_prod:
            return False
        sigma_prod *= (p**(e+1) - 1) // (p - 1)
    return True

for val, name in [(lam,'lam'),(q,'q'),(mu,'mu'),(mu+1,'mu+1'),(fq,'q!'),(Phi6,'Phi6'),
                  (Theta,'Theta'),(k,'k'),(Phi3,'Phi3'),(g,'g'),(f,'f'),(v,'v'),
                  (N_eff,'N_eff'),(E,'E'),(T,'T')]:
    if is_practical(val):
        print(f"  {name}={val} is practical")

# --- Highly composite check ---
print("\n--- Highly composite numbers ---")
def ndiv(n):
    c = 0
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            c += 2 if i*i != n else 1
    return c

# First highly composites: 1, 2, 4, 6, 12, 24, 36, 48, 60, 120, 180, 240, ...
hcn_list = []
max_d = 0
for n in range(1, 300):
    d = ndiv(n)
    if d > max_d:
        hcn_list.append(n)
        max_d = d

print(f"  HCN up to 300: {hcn_list}")
# ALL of {1, lam, mu, q!, k, f, ..., E} in HCN!
targets = {1:'1',lam:'lam',mu:'mu',fq:'q!',k:'k',f:'f',E:'E'}
for h in hcn_list:
    if h in targets:
        print(f"  HCN {h} = {targets[h]}")

# --- Sum of graph parameters identities ---
print("\n--- Sum identities ---")
print(f"  v+k+f+g = {v+k+f+g}")
print(f"  = q*Phi3*Phi6/(q-lam)? no, = {q*Phi3*Phi6}")
print(f"  v+k = {v+k}, f+g = {f+g} = v-1 = {v-1}")
print(f"  v+k = {v+k} = f+g+lam+1 = {f+g+lam+1}")
print(f"  f-g = {f-g} = q^2? {f-g==q**2}")
print(f"  f*g = {f*g} = {f*g}")
print(f"  f*g = (v-1)*Theta-lam*(Theta-1)? {(v-1)*Theta-lam*(Theta-1)}")
print(f"  f*g = qk*E/{fq*mu}? {q*k*E//(fq*mu)}")
# f*g = 360 = 6*60 = q!*(mu+1)*k
print(f"  f*g = q!*(mu+1)*k = {fq*(mu+1)*k}? {f*g==fq*(mu+1)*k}")
# 360 = (q!)^2 * Theta
print(f"  f*g = (q!)^2*Theta = {fq**2*Theta}? {f*g==fq**2*Theta}")
# 360 = f*g = 24*15 = 8*45 = 2^3 * 45 = 2^3 * 3^2 * 5
# = lam^q * q^2 * (mu+1)
print(f"  f*g = lam^q * q^2 * (mu+1) = {lam**q * q**2 * (mu+1)}? {f*g==lam**q*q**2*(mu+1)}")

# --- Adjacency spectrum deeper ---
print("\n--- Spectrum products ---")
# Product of eigenvalues: k * r^f * s^g = k * lam^f * (-mu)^g
spec_prod = k * lam**f * (-mu)**g
print(f"  det(A) = k*r^f*s^g = {spec_prod}")
print(f"  = k * lam^f * (-mu)^g = {k}*{lam**f}*{(-mu)**g}")
print(f"  det(A) = -k*lam^f*mu^g = {-k*lam**f*mu**g}")
# = -12 * 2^24 * 4^15 = -12 * 2^24 * 2^30 = -12 * 2^54
print(f"  = -k * 2^(f+lam*g) = -k * 2^{f+lam*g} = -{k}*2^{f+lam*g}")
print(f"  = -{k * 2**(f+lam*g)}")

# Trace of A^n
print(f"\n  tr(A^0) = v = {v}")
print(f"  tr(A^1) = 0 (no loops)")
print(f"  tr(A^2) = vk = {v*k} = sum of squares")
print(f"  tr(A^3) = v*lam*(lam+1) = {v*lam*(lam+1)} = number of triangles * 6")
num_triangles = v * lam * (lam + 1) // 6
print(f"  Number of triangles = {num_triangles} = v*lam*(lam+1)/6")
# = 40*2*3/6 = 40
print(f"  = v? {num_triangles==v}!")
# The number of triangles equals v! Each vertex is on lam*(lam+1)/2 = 3 triangles.
# v * 3 / 3 = v. Checks out!

print(f"\n  tr(A^4) = {k + f*lam**4 + g*mu**4}")
print(f"  tr(A^4) = k*lam^3 + (k+lam+mu) sums? Let me compute:")
tr4 = k**4 + f*lam**4 + g*mu**4
print(f"  tr(A^4) = k^4 + f*r^4 + g*s^4 = {k**4} + {f*lam**4} + {g*mu**4} = {tr4}")
# = 20736 + 384 + 3840 = 24960
print(f"  tr(A^4) = {tr4}")
# Paths of length 4 relate to quadrilaterals, triangles through edges, etc.

# --- Graph complement deeper ---
print("\n--- Complement graph deeper ---")
k_bar = v - k - 1  # 27
lam_bar = v - 2*k + mu - 2  # 18
mu_bar = v - 2*k + lam  # 18
print(f"  Complement: SRG({v},{k_bar},{lam_bar},{mu_bar})")
# Complement eigenvalues
r_bar = -1 - s_val  # -1-(-4) = 3 = q
s_bar = -1 - r_val  # -1-2 = -3 = -q
print(f"  r_bar = -1-s = {r_bar} = q? {r_bar==q}")
print(f"  s_bar = -1-r = {s_bar} = -q? {s_bar==-q}")
# Complement determinant
det_bar = k_bar * r_bar**f * s_bar**g
print(f"  det(A_bar) = k_bar*r_bar^f*s_bar^g = {det_bar}")
print(f"  = q^3 * q^f * (-q)^g = q^3 * q^f * (-1)^g * q^g")
print(f"  = (-1)^g * q^(3+f+g) = (-1)^g * q^(v+2)")
print(f"  = (-1)^{g} * q^{v+2} = {(-1)**g * q**(v+2)}")
print(f"  Match: {det_bar == (-1)**g * q**(v+2)}")

# --- Hoffman bound ---
print("\n--- Hoffman bound ---")
# alpha(G) <= v * (-s) / (k - s) = 40*4/(12+4) = 160/16 = 10 = Theta
alpha_bound = v * mu // (k + mu)
print(f"  Hoffman bound: alpha <= v*mu/(k+mu) = {alpha_bound} = Theta? {alpha_bound==Theta}")
# omega(G) <= 1 - k/s = 1 + k/mu = 1 + 12/4 = 4 = mu
omega_bound = 1 + k // mu
print(f"  Hoffman clique: omega <= 1+k/mu = {omega_bound} = mu? {omega_bound==mu}")

# --- Lovasz theta ---
print("\n--- Lovasz theta ---")
# theta(G) = v*(- s)/(k - s) for vertex-transitive SRG = same as Hoffman = Theta
lovasz = v * mu / (k + mu)
print(f"  Lovasz theta(G) = {lovasz} = Theta? {lovasz==Theta}")
# theta(G_bar) = v * (k - r) / (k - r + (-s - (-1))) 
# For complement: theta_bar = v * (k_bar - r_bar) / (k_bar - r_bar + |s_bar| - something)
# Actually for vertex transitive: theta(G)*theta(G_bar) >= v
# theta(G_bar) = v*(1+r)/(k+1+r) = v*(1+lam)/(k+1+lam) = 40*3/15 = 8
theta_bar = v * (1 + lam) // (k + 1 + lam)
print(f"  Lovasz theta(G_bar) = {theta_bar} = 2^q? {theta_bar==2**q}")
print(f"  theta(G)*theta(G_bar) = {Theta*theta_bar} = v? {Theta*theta_bar==v*2}")
# Hmm let me recalculate. For SRG: theta = 1 - k/s = 1 + k/mu for G
# Actually, for SRG with eigenvalues k >= r > s:
# theta(G) = -v*s/(k-s) and theta(G_bar) = v*(1-s/k) hmm
# Let me just check theta*alpha relation
print(f"  alpha*omega = Theta*mu = {Theta*mu} = v? {Theta*mu==v}")
# alpha * omega = 10 * 4 = 40 = v. Tight!
# This means the graph is both alpha-tight and omega-tight!

# --- Strongly regular complement of complement ---
print("\n--- SRG identities ---")
# vk(k-lam-1) = k(v-k-1)mu  -- fundamental SRG equation  
lhs = v * k * (k - lam - 1)
rhs = k * (v - k - 1) * mu
print(f"  vk(k-lam-1) = {lhs} = k(v-k-1)mu = {rhs}? {lhs==rhs}")
# Actually the correct form: k(k-lam-1) = (v-k-1)*mu
lhs2 = k * (k - lam - 1)
rhs2 = (v - k - 1) * mu
print(f"  k(k-lam-1) = {lhs2} = (v-k-1)*mu = {rhs2}? {lhs2==rhs2}")

# --- Krein conditions ---
print("\n--- Krein parameters ---")
# For SRG with eigenvalues k, r, s and multiplicities 1, f, g:
# Krein condition 1: (r+1)(k+r+2*r*s) <= (k+r)*(s+1)^2
kr1_lhs = (r_val+1)*(k+r_val+2*r_val*s_val)
kr1_rhs = (k+r_val)*(s_val+1)**2
print(f"  Krein 1: {kr1_lhs} <= {kr1_rhs}? {kr1_lhs<=kr1_rhs}")
# Krein condition 2: (s+1)(k+s+2*r*s) <= (k+s)*(r+1)^2
kr2_lhs = (s_val+1)*(k+s_val+2*r_val*s_val)
kr2_rhs = (k+s_val)*(r_val+1)**2
print(f"  Krein 2: {kr2_lhs} <= {kr2_rhs}? {kr2_lhs<=kr2_rhs}")
# When Krein is tight, we get Q-polynomial association scheme  
print(f"  Krein 1 tight? {kr1_lhs==kr1_rhs}")
print(f"  Krein 2 tight? {kr2_lhs==kr2_rhs}")

# --- Coclique extension / conf designs ---
print("\n--- Design parameters ---")
# From SRG, we get 2-designs.
# A clique of size mu=4 gives a 2-(v,mu,lam) design? No.
# Actually, the neighbors of each vertex form a (lam)-regular graph on k vertices.
# The blocks of the 1-(v,k,k) design from adjacency...

# --- Seidel spectrum ---
print("\n--- Seidel matrix ---")
# Seidel matrix S = J - I - 2A, eigenvalues: v-1-2k, -1-2r, -1-2s
seidel_k = v - 1 - 2*k
seidel_r = -1 - 2*r_val
seidel_s = -1 - 2*s_val
print(f"  Seidel eigenvalues: {seidel_k}, {seidel_r}, {seidel_s}")
print(f"  = {seidel_k} = g? {seidel_k==g}")
print(f"  = {seidel_r} = -mu-1? {seidel_r==-(mu+1)}")
print(f"  = {seidel_s} = Phi6? {seidel_s==Phi6}")
# Seidel eigenvalues are g, -(mu+1), Phi6 !!
# With multiplicities 1, f, g

# --- Signless Laplacian ---
print("\n--- Signless Laplacian Q = D + A ---")
# For k-regular: Q = kI + A, so eigenvalues are k+eigenvalue
sl_k = 2*k
sl_r = k + r_val
sl_s = k + s_val
print(f"  Q eigenvalues: {sl_k}, {sl_r}, {sl_s}")
print(f"  = {sl_k} = f? {sl_k==f}")
print(f"  = {sl_r} = lam*Phi6? {sl_r==lam*Phi6}")
print(f"  = {sl_s} = 2^q? {sl_s==2**q}")
# Signless Laplacian eigenvalues: f=24, lam*Phi6=14, 2^q=8

# --- Normalized Laplacian ---
print("\n--- Normalized Laplacian ---")
# For k-regular: eigenvalues are 1 - lambda_i/k
nl_k = 1 - Fraction(k, k)  # = 0
nl_r = 1 - Fraction(r_val, k)
nl_s = 1 - Fraction(s_val, k)
print(f"  NL eigenvalues: {nl_k}, {nl_r}, {nl_s}")
print(f"  = 0, {nl_r}, {nl_s}")
print(f"  = 0, 1-lam/k = 1-1/q! = (q!-1)/q! = {nl_r}")
print(f"  = 0, {(fq-1)}/{fq}, Phi3/k = {nl_s}? {nl_s==Fraction(Phi3,k)}")
# Hmm: 1 - r/k = 1 - 2/12 = 10/12 = 5/6 = (mu+1)/q!
print(f"  1 - r/k = (mu+1)/q! = {Fraction(mu+1,fq)}? {nl_r==Fraction(mu+1,fq)}")
# 1 - s/k = 1 + mu/k = 1 + 1/q = (q+1)/q = (mu+1)/q  Hmm
# 1 + 4/12 = 16/12 = 4/3 = mu/q
print(f"  1 - s/k = mu/q = {Fraction(mu,q)}? {nl_s==Fraction(mu,q)}")

# --- Adjacency matrix at graph parameters ---
print("\n--- Matrix power traces ---")
# tr(A^n) = k^n + f*r^n + g*s^n
for n in range(2, 9):
    tr = k**n + f*r_val**n + g*s_val**n
    print(f"  tr(A^{n}) = {tr}")

# --- Ihara zeta function ---
print("\n--- Ihara zeta (reciprocal eval at u) ---")
# For k-regular on v vertices: zeta^(-1)(u) = (1-u^2)^(E-v) * det(I - uA + u^2(k-1)I)
# = (1-u^2)^(E-v) * prod_i (1 - u*lambda_i + u^2*(k-1))
# At u=1: (1-1)^(E-v) = 0, so zeta has pole at u=1
# At u=1/k: each factor (1 - lambda_i/k + (k-1)/k^2)
# At u=1/sqrt(k-1): Ramanujan bound

# --- Line graph ---
print("\n--- Line graph L(G) ---")
# L(G) of k-reg with v vertices: has E = vk/2 = 240 vertices
# L(G) is (2k-2)-regular = 22-regular
# Eigenvalues of L(G): lambda_i + lambda_j - 2 for adjacent i,j
# For SRG: L(G) eigenvalues include 2k-2, r+k-2, 2r-2, r+s-2, 2s-2
lg_eigs = sorted(set([2*k-2, r_val+k-2, 2*r_val-2, r_val+s_val-2, 2*s_val-2]), reverse=True)
print(f"  L(G) eigenvalues include: {lg_eigs}")
print(f"  = {[2*k-2, r_val+k-2, 2*r_val-2, r_val+s_val-2, 2*s_val-2]}")
print(f"  = [22, 12, 2, -4, -10]")
print(f"  = [2(k-1), k, lam, -mu, -Theta]")
print(f"  2(k-1) = {2*(k-1)}")
print(f"  k = {k}")
print(f"  lam = {lam}")
print(f"  -mu = {-mu}")
print(f"  -Theta = {-Theta}")

# --- Laplacian eigenvalues ---
print("\n--- Laplacian L = kI - A ---")
lap_k = 0
lap_r = k - r_val
lap_s = k - s_val
print(f"  Laplacian eigenvalues: {lap_k}, {lap_r}, {lap_s}")
print(f"  = 0, k-lam, k+mu = 0, {lap_r}, {lap_s}")
print(f"  = 0, Theta, k+mu = 0, {Theta}, {k+mu}")
print(f"  k+mu = {k+mu} = lam^mu? {k+mu==lam**mu}")
# Laplacian eigenvalues: 0, Theta=10, lam^mu=16
# spanning tree count = v^(-1) * Theta^f * (lam^mu)^g = ...
kappa = Theta**f * (lam**mu)**g // v
print(f"  Spanning trees kappa = Theta^f * (k+mu)^g / v = {Theta}^{f} * {k+mu}^{g} / {v}")
print(f"  = {Theta**f} * {(k+mu)**g} / {v}")
print(f"  = {Theta**f * (k+mu)**g // v}")

# --- Magic constant ---
print("\n--- Magic squares ---")
# M(n) = n(n^2+1)/2
for n in range(1, 15):
    mc = n*(n*n+1)//2
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',N_eff:'N_eff',E:'E'}
    if mc in targets:
        print(f"  Magic({n}) = {mc} = {targets[mc]}")

# --- Multiples/ratios ---
print("\n--- Key ratios ---")
print(f"  E/k = {E//k} = v/lam = {v//lam}")
print(f"  E/f = {E//f} = Theta = {Theta}")
print(f"  E/g = {E//g} = k+mu = lam^mu = {lam**mu}")
print(f"  E/Theta = {E//Theta} = f = {f}")
print(f"  T/k = {T//k} = Phi3+1? {T//k==Phi3+1}")
print(f"  T/v = {T//v} = mu = {mu}")
print(f"  T/mu = {T//mu} = v = {v}")
print(f"  vk = {v*k} = lam*E = {lam*E}")
print(f"  vk/q = {v*k//q} = T = {T}")

# --- Digit sum identities ---
print("\n--- Digit sums ---")
def dsum(n):
    return sum(int(d) for d in str(n))

print(f"  S(v)={dsum(v)}, S(k)={dsum(k)}, S(f)={dsum(f)}, S(g)={dsum(g)}")
print(f"  S(E)={dsum(E)}, S(T)={dsum(T)}, S(Phi12)={dsum(Phi12)}")
print(f"  S(v)=S(mu)? {dsum(v)==dsum(mu)}")
print(f"  S(E)=S(q!)? {dsum(E)==dsum(fq)}")

# --- Nim values / Sprague-Grundy ---
# Skip, too esoteric

# --- Power tower / tetration ---
print("\n--- Tetration ---")
# lam^^q = 2^^3 = 2^(2^2) = 2^4 = 16 = lam^mu = mu^2
print(f"  lam^^q = 2^^3 = 2^(2^2) = {2**(2**2)} = lam^mu = mu^2 = {lam**mu}? {2**(2**2)==lam**mu}")
# q^^lam = 3^^2 = 3^3 = 27 = q^q
print(f"  q^^lam = 3^^2 = 3^3 = {3**3} = q^3? {3**3==q**3}")

# --- Polygonal numbers deeper ---
print("\n--- More polygonal ---")
# Centered triangular: 1, 4, 10, 19, 31, 46, ...  CT(n) = (3n^2+3n+2)/2
def cent_tri(n):
    return (3*n*n + 3*n + 2) // 2

for n in range(10):
    ct = cent_tri(n)
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v'}
    if ct in targets:
        print(f"  CT({n}) = {ct} = {targets[ct]}")

# Centered hexagonal: 1, 7, 19, 37, 61, 91, ...  CH(n) = 3n^2+3n+1 = 3n(n+1)+1
def cent_hex(n):
    return 3*n*(n+1) + 1

for n in range(10):
    ch = cent_hex(n)
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',Phi12:'Phi12'}
    if ch in targets:
        print(f"  CentHex({n}) = {ch} = {targets[ch]}")

# Cake numbers: 1, 2, 4, 8, 15, 26, 42, 64, 93, 130, 176, 232, 299, ...
# C(n) = C(n,0) + C(n,1) + C(n,2) + C(n,3) = (n^3+5n+6)/6
def cake(n):
    return (n**3 + 5*n + 6) // 6

for n in range(20):
    c = cake(n)
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',N_eff:'N_eff',E:'E',Phi12:'Phi12'}
    if c in targets:
        print(f"  Cake({n}) = {c} = {targets[c]}")

# Lazy caterer: 1, 2, 4, 7, 11, 16, 22, 29, 37, 46, 56, ...
# LC(n) = n(n+1)/2 + 1 = T(n)+1
def lazy_cat(n):
    return n*(n+1)//2 + 1

for n in range(20):
    lc = lazy_cat(n)
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',N_eff:'N_eff',Phi12:'Phi12'}
    if lc in targets:
        print(f"  LazyCat({n}) = {lc} = {targets[lc]}")

print("\nDONE WAVE 2")
