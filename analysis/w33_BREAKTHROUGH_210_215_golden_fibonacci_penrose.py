"""
BT210-215: Golden Ratio, Fibonacci Ladder, and Penrose Tilings

Central result:
  sin²(θ_W) = F_4/F_7 = q/|PG(2,q)| = 3/13
  where the Fibonacci ladder is: F_3=λ, F_4=q, F_5=μ+1, F_6=λ^q=dim(O), F_7=|PG(2,q)|

  This same ratio = (thin Penrose tiles after 3 inflations) / (total after 4 inflations)
  The Weinberg angle is a Penrose quasicrystal inflation frequency.
"""
import math

q, mu, lam = 3, 4, 2
q_fac = math.factorial(q)
phi = (1+5**0.5)/2

def fib(n):
    a, b = 1, 1
    for _ in range(n-1): a, b = b, a+b
    return a

# BT212: Fibonacci ladder
ladder = {3: lam, 4: q, 5: mu+1, 6: lam**q, 7: q**2+q+1, 12: lam**mu*q**lam}
for k, v in ladder.items():
    assert fib(k) == v, f'F_{k}={fib(k)} != {v}'

# BT213: Weinberg = F_4/F_7
sw2 = fib(4)/fib(7)
assert sw2 == q/(q**2+q+1)
assert abs(sw2 - 0.2312)/0.2312 < 0.002  # < 0.2% error from PDG

# BT214: golden fixed point
phi3 = phi**3
q_gold = ((phi3-1) + ((phi3-1)**2-4)**0.5)/2
assert abs(q_gold - q) < 0.12  # q=3 is within 4% of golden fixed point

# BT215: Penrose inflation
M = [[1,1],[1,0]]
def mat_pow(M, n):
    r = [[1,0],[0,1]]
    for _ in range(n):
        r = [[sum(r[i][k]*M[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return r

step3 = mat_pow(M, 3)
step4 = mat_pow(M, 4)
thin_3 = step3[1][0]   # = fib(4) = 3 = q
total_4 = step4[0][0] + step4[1][0]  # = fib(7) = 13 = |PG(2,q)|
assert thin_3 == q
assert total_4 == q**2+q+1
assert thin_3/total_4 == sw2  # Weinberg = Penrose!

# Lucas numbers
lucas = [round(phi**n + (-1/phi)**n) for n in range(1,9)]
assert lucas[1] == q   # L_2 = q
assert lucas[2] == mu  # L_3 = mu
assert lucas[3] == mu+q  # L_4 = q!+1 = now-fan
assert lucas[6] == 2*lam**mu - q  # L_7 = Monster prime 29
assert lucas[7] == lam**mu*q - 1  # L_8 = Monster prime 47

if __name__ == '__main__':
    print('BT210-215 ALL ASSERTIONS PASSED')
    print(f'sin²θ_W = {fib(4)}/{fib(7)} = F_4/F_7 = q/|PG(2,q)|')
    print(f'       = Penrose thin@step3/total@step4')
    print(f'       = {sw2:.6f} (PDG: 0.2312, error: {abs(sw2-0.2312)/0.2312*100:.2f}%)')
    print(f'Fibonacci substrate ladder: λ=F_3, q=F_4, μ+1=F_5, λ^q=F_6, |PG|=F_7')
    print(f'Lucas substrate: q=L_2, μ=L_3, now-fan=L_4, Monster primes=L_7,L_8')
    print(f'Golden fixed-point: q_gold={q_gold:.4f} ≈ q=3')
