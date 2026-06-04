"""
BT189/190: Leech Lattice Chain — Substrate to Monster

The substrate chain:
  W(3,3) [240 edges] → E8 [240 roots, 8=λ^q dims]
  E8 → Leech [24=q·λ^q dims, 196560 kissing]
  Leech → Monster [j-const 744=q·248, 196884=Leech_kiss+λ^2·q^4]

Key factorizations:
  Leech_kiss = 196560 = 240 · 819
  819 = q^2 · (q!+1) · (q^2+q+1)  [all substrate!]
  dim(Leech) = 24 = q · dim(E8) = q · λ^q
  196884 = Leech_kiss + λ^2·q^4
"""
import math, json

q, mu, lam = 3, 4, 2
q_fac = math.factorial(q)

leech_kiss = 196560
assert leech_kiss // 240 == 819
assert 819 == q**2 * (q_fac+1) * (q**2+q+1)
assert leech_kiss == lam*math.factorial(mu+1) * q**2 * (q_fac+1) * (q**2+q+1)
assert 24 == q * lam**q  # dim(Leech) = q * dim(E8)
assert 196884 == leech_kiss + lam**2 * q**4
assert 744 == q * (lam**q + lam*math.factorial(mu+1))

result = {
    "breakthrough": "BT189-190",
    "title": "Substrate sporadic chain: W(3,3)→E8→Leech→Monster",
    "date": "2026-06-04",
    "status": "VERIFIED",
    "E8": {"kissing": 240, "dim": 8, "Lie_dim": 248},
    "Leech": {"dim": 24, "dim_formula": "q*lam^q", "kissing": 196560,
              "kiss_formula": "240*q^2*(q!+1)*(q^2+q+1)"},
    "Monster": {"j_const": 744, "j_const_formula": "q*dim(E8)",
                "j_coeff1": 196884, "j_coeff1_formula": "Leech_kiss + lam^2*q^4",
                "Monster_rep_dim": 196883},
}

if __name__ == '__main__':
    print(json.dumps(result, indent=2))
    print('BT189-190: all checks passed')
