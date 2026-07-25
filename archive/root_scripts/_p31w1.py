"""Phase 31 exploration wave 1."""
import math
from fractions import Fraction

q, lam, mu = 3, 2, 4
k, v, f, g = 12, 40, 24, 15
E, T = 240, 160
Theta, Phi3, Phi6, Phi12 = 10, 13, 7, 73
N_eff = 55
r, s = lam, -mu
fq = math.factorial(q)  # 6

print("=== PHASE 31 WAVE 1 ===")

# --- Catalan numbers ---
def catalan(n):
    return math.comb(2*n, n) // (n + 1)

print("\n--- Catalan numbers ---")
print(f"  C(lam)={catalan(lam)}, C(q)={catalan(q)}, C(mu)={catalan(mu)}, C(mu+1)={catalan(mu+1)}")
print(f"  C(lam)=lam? {catalan(lam)==lam}")
print(f"  C(q)=mu+1? {catalan(q)==mu+1}")
print(f"  C(mu)=lam*Phi6=14? {catalan(mu)==lam*Phi6}")
print(f"  C(mu+1)=lam*q*Phi6=42? {catalan(mu+1)==lam*q*Phi6}")
print(f"  C(mu+1)/C(mu)=q? {catalan(mu+1)//catalan(mu)==q}")

# --- Motzkin ---
print("\n--- Motzkin numbers ---")
def motzkin(n):
    if n <= 1: return 1
    M = [0]*(n+1)
    M[0] = M[1] = 1
    for i in range(2, n+1):
        M[i] = M[i-1]
        for j in range(i-1):
            M[i] += M[j]*M[i-2-j]
    return M[n]

print(f"  M(lam)={motzkin(lam)}, M(q)={motzkin(q)}, M(mu)={motzkin(mu)}")
print(f"  M(lam)=lam? {motzkin(lam)==lam}")
print(f"  M(q)=mu? {motzkin(q)==mu}")
print(f"  M(mu)=q^2? {motzkin(mu)==q**2}")

# --- Egyptian fractions ---
print("\n--- Egyptian fractions ---")
ef = Fraction(1,lam)+Fraction(1,q)+Fraction(1,fq)
print(f"  1/lam+1/q+1/q! = 1/{lam}+1/{q}+1/{fq} = {ef} = 1? {ef==1}")
ef2 = Fraction(1,lam)+Fraction(1,mu)+Fraction(1,mu)
print(f"  1/lam+1/mu+1/mu = {ef2}")
ef3 = Fraction(1,q)+Fraction(1,mu)+Fraction(1,k)
print(f"  1/q+1/mu+1/k = {ef3}")

# --- Pochhammer / rising factorials ---
print("\n--- Pochhammer rising factorials ---")
def rising(x, n):
    r = 1
    for i in range(n): r *= (x + i)
    return r

def falling(x, n):
    r = 1
    for i in range(n): r *= (x - i)
    return r

print(f"  (lam)_q = {rising(lam,q)} = f? {rising(lam,q)==f}")
print(f"  (q)_q = {rising(q,q)} = (mu+1)*k=60? {rising(q,q)==(mu+1)*k}")
print(f"  (lam)_mu = {rising(lam,mu)} = E/lam=(mu+1)!? {rising(lam,mu)==E//lam}")
print(f"  (lam)_(mu+1) = {rising(lam,mu+1)} = q*E=720? {rising(lam,mu+1)==q*E}")
print(f"  (k)_q falling = {falling(k,q)}")
print(f"    = k*(k-1)*Theta = {k*(k-1)*Theta}? {falling(k,q)==k*(k-1)*Theta}")

# --- tau(3) = C(Theta, mu+1) ---
print("\n--- Ramanujan tau(3) ---")
print(f"  tau(3)=252 = C(Theta, mu+1) = C(10,5) = {math.comb(Theta, mu+1)}")

# --- Divisor counts ---
print("\n--- Divisor counts ---")
def ndiv(n):
    c = 0
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            c += 2 if i*i != n else 1
    return c

print(f"  d(vk=480) = {ndiv(v*k)} = f? {ndiv(v*k)==f}")
print(f"  d(E=240) = {ndiv(E)} = v/lam? {ndiv(E)==v//lam}")

# --- Generalized pentagonal ---
print("\n--- Generalized pentagonal numbers ---")
gen_pent = set()
for kk in range(-20, 21):
    gp = kk * (3 * kk - 1) // 2
    if gp >= 0:
        gen_pent.add(gp)

for val, name in [(lam,'lam'),(q,'q'),(mu,'mu'),(mu+1,'mu+1'),(fq,'q!'),(Phi6,'Phi6'),
                  (Theta,'Theta'),(k,'k'),(Phi3,'Phi3'),(g,'g'),(f,'f'),(v,'v'),(N_eff,'N_eff')]:
    if val in gen_pent:
        for kk in range(-20, 21):
            if kk*(3*kk-1)//2 == val:
                print(f"  {name}={val} = GP({kk})")

# --- Harshad ---
print("\n--- Harshad numbers ---")
def dsum(n):
    return sum(int(d) for d in str(n))

for val, name in [(lam,'lam'),(q,'q'),(mu,'mu'),(mu+1,'mu+1'),(fq,'q!'),(Phi6,'Phi6'),
                  (Theta,'Theta'),(k,'k'),(Phi3,'Phi3'),(g,'g'),(f,'f'),(v,'v'),
                  (N_eff,'N_eff'),(E,'E'),(T,'T')]:
    if val % dsum(val) == 0:
        print(f"  {name}={val} Harshad (div by {dsum(val)})")

# --- Perfect numbers ---
print("\n--- Perfect/abundant/deficient ---")
def sigma1(n):
    s = 0
    for i in range(1, n+1):
        if n % i == 0: s += i
    return s

print(f"  q!=6: sigma={sigma1(fq)}, perfect? {sigma1(fq)==2*fq}")
print(f"  k=12: sigma={sigma1(k)}, abundant by {sigma1(k)-2*k}")
print(f"  f=24: sigma={sigma1(f)}, abundant by {sigma1(f)-2*f}")

# --- v = lam^2 + (q!)^2 ---
print(f"\n  v = lam^2 + (q!)^2 = {lam**2 + fq**2}? {lam**2 + fq**2 == v}")

# --- Power sums r^n + s^n ---
print("\n--- Power sums r^n+s^n ---")
for n in range(1, 13):
    ps = lam**n + (-mu)**n
    print(f"  r^{n}+s^{n} = {ps}")

# --- Arithmetic derivative ---
print("\n--- Arithmetic derivative ---")
def ad(n):
    if n <= 1: return 0
    result = 0
    temp = n
    for p in range(2, int(n**0.5)+2):
        while temp % p == 0:
            result += n // p
            temp //= p
    if temp > 1:
        result += n // temp
    return result

for val, name in [(lam,'lam'),(q,'q'),(mu,'mu'),(mu+1,'mu+1'),(fq,'q!'),(Phi6,'Phi6'),
                  (Theta,'Theta'),(k,'k'),(Phi3,'Phi3'),(g,'g'),(f,'f'),(v,'v'),
                  (N_eff,'N_eff'),(E,'E'),(T,'T')]:
    d = ad(val)
    print(f"  {name}'={d}", end="")
    targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
               Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',N_eff:'N_eff',E:'E',T:'T',Phi12:'Phi12'}
    if d in targets:
        print(f" = {targets[d]}", end="")
    print()

# --- Collatz ---
print("\n--- Collatz stopping times ---")
def collatz(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3*n + 1
        steps += 1
    return steps

targets = {lam:'lam',q:'q',mu:'mu',mu+1:'mu+1',fq:'q!',Phi6:'Phi6',
           Theta:'Theta',k:'k',Phi3:'Phi3',g:'g',f:'f',v:'v',N_eff:'N_eff'}
for val, name in [(lam,'lam'),(q,'q'),(mu,'mu'),(mu+1,'mu+1'),(fq,'q!'),(Phi6,'Phi6'),
                  (Theta,'Theta'),(k,'k'),(Phi3,'Phi3'),(g,'g'),(f,'f'),(v,'v')]:
    cs = collatz(val)
    label = targets.get(cs, "")
    print(f"  Collatz({name}={val})={cs}" + (f" = {label}" if label else ""))

# --- CF of key ratios ---
print("\n--- Continued fractions of ratios ---")
def cf(num, den, max_t=10):
    terms = []
    for _ in range(max_t):
        if den == 0: break
        qv = num // den
        terms.append(qv)
        num, den = den, num - qv * den
    return terms

print(f"  CF(k/v) = CF(3/10) = {cf(3, 10)}")
print(f"  CF(f/g) = CF(8/5) = {cf(8, 5)}")
print(f"  CF(Phi12/Phi3) = CF(73/13) = {cf(73, 13)}")
print(f"  (v-1)/k = 39/12 = Phi3/mu? {(v-1)*mu==k*Phi3}")

# --- Compositions ---
print("\n--- Compositions / binomial ---")
print(f"  C(Theta-1, q-1) = C(9,2) = {math.comb(9,2)} = qk=36? {math.comb(9,2)==q*k}")
print(f"  C(k-1, q-1) = C(11,2) = {math.comb(11,2)} = N_eff? {math.comb(11,2)==N_eff}")
print(f"  C(k-1, mu-1) = C(11,3) = {math.comb(11,3)} = q*N_eff? {math.comb(11,3)==q*N_eff}")
print(f"  C(v-1, lam-1) = C(39,1) = {math.comb(39,1)} = v-1")
print(f"  C(f, mu) = C(24,4) = {math.comb(24,4)} = g*k*Phi6*fq? Let me check: {math.comb(24,4)}")
val = math.comb(f, mu)
print(f"    = {val} = k*Theta*Phi6*fq/6? {val}")

# --- Repunit ---
print("\n--- Repunits ---")
for n in range(1, 8):
    rn = (10**n - 1) // 9
    extra = ""
    if rn == k - 1: extra = " = k-1"
    print(f"  R_{n} = {rn}{extra}")

# --- Largest prime factors ---
print("\n--- Largest prime factors (smoothness) ---")
def lpf(n):
    if n <= 1: return 0
    largest = 1
    for p in range(2, int(n**0.5)+2):
        while n % p == 0:
            largest = p
            n //= p
    if n > 1: largest = n
    return largest

for val, name in [(v,'v'),(k,'k'),(f,'f'),(g,'g'),(E,'E'),(T,'T'),(N_eff,'N_eff'),(Theta,'Theta')]:
    l = lpf(val)
    targets2 = {2:'lam',3:'q',5:'mu+1',7:'Phi6',11:'k-1',13:'Phi3'}
    label = targets2.get(l, str(l))
    print(f"  lpf({name}={val}) = {l} = {label}, so {val} is {l}-smooth")

# Check all key params are mu+1-smooth
all_5smooth = all(lpf(x) <= mu+1 for x in [v, k, f, g, E, T])
print(f"  v,k,f,g,E,T all (mu+1)-smooth? {all_5smooth}")
# N_eff = 5*11, Theta = 2*5, Phi3 = 13
print(f"  N_eff (mu+1)-smooth? {lpf(N_eff) <= mu+1}: lpf={lpf(N_eff)}")

print("\nDONE WAVE 1")
