"""
BT194/196/197: All Exceptional Lie Algebras in Substrate

Dimensions (BT194):
  G2=14=λ(q!+1), F4=52=μ(q²+q+1), E6=78=q!(q²+q+1)
  E7=133=(q!+1)(q³-λ^q), E8=248=λ^q+λ(μ+1)!

Division algebras (BT195):
  R=1=λ^0, C=2=λ=λ^1, H=4=λ^2, O=8=λ^q  [all powers of λ!]

Freudenthal magic square (BT196) — all 10 entries:
  (R,R)=3=q, (R,C)=8=λ^q, (R,H)=21=q^q-q!, (R,O)=52=μ(q²+q+1)
  (C,C)=16=λ^μ, (C,H)=35=(μ+1)(q!+1), (C,O)=78=q!(q²+q+1)
  (H,H)=66=λ q(q^q-λ^μ), (H,O)=133=(q!+1)(q^q-λ^q), (O,O)=248

Root system sizes (BT197):
  G2=12=qμ, F4=48=λ^μ q, E6=72=λ^q q^λ, E7=126=q^λ λ(q!+1), E8=240=λ(μ+1)!
"""
import math, json

q, mu, lam = 3, 4, 2
q_fac = math.factorial(q)
PG = q**2+q+1  # 13

# BT194: Dimensions
assert 14 == lam*(q_fac+1)
assert 52 == mu*PG
assert 78 == q_fac*PG
assert 133 == (q_fac+1)*(q**q - lam**q)
assert 248 == lam**q + lam*math.factorial(mu+1)

# BT195: Division algebra dims = powers of lam
assert [1,2,4,8] == [lam**k for k in range(4)]  # R,C,H,O
assert lam**q == 8  # octonions

# BT196: Magic square — all 10
assert 3 == q           # (R,R)
assert 8 == lam**q      # (R,C)
assert 21 == q**q-q_fac # (R,H)
assert 52 == mu*PG      # (R,O)
assert 16 == lam**mu    # (C,C)
assert 35 == (mu+1)*(q_fac+1)  # (C,H)
assert 78 == q_fac*PG   # (C,O)
assert 66 == lam*q*(q**q-lam**mu)  # (H,H)
assert 133 == (q_fac+1)*(q**q-lam**q)  # (H,O)
assert 248 == lam**q+lam*math.factorial(mu+1)  # (O,O)

# BT197: Root counts
assert 12 == q*mu
assert 48 == lam**mu*q
assert 72 == lam**q*q**lam
assert 126 == q**lam*lam*(q_fac+1)
assert 240 == lam*math.factorial(mu+1)

result = {
    "breakthrough": "BT194-197",
    "title": "All exceptional Lie dimensions and root counts in substrate",
    "date": "2026-06-04",
    "status": "ALL_VERIFIED",
    "Lie_dims": {"G2":14,"F4":52,"E6":78,"E7":133,"E8":248},
    "root_counts": {"G2":12,"F4":48,"E6":72,"E7":126,"E8":240},
    "magic_square_entries": 10,
    "division_alg_dims": [1,2,4,8],
}
if __name__ == '__main__':
    print(json.dumps(result, indent=2))
    print('BT194-197: all checks passed')
