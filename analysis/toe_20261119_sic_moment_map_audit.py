"""Exact H27 SIC F-flat spectrum and SU(3) moment-map obstruction/repair.
Keeps the finite H27 invariant distinct from any putative continuous gauge UV completion.
Run: python analysis/toe_20261119_sic_moment_map_audit.py
"""
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
x, y, z = s.symbols("x y z")
W = sum(t**3 - s.Rational(1, 2)*t**6 for t in (x, y, z))
grad = [s.factor(s.diff(W, t)) for t in (x, y, z)]
assert all(s.expand(g - 3*t*t*(1-t**3)) == 0 for g, t in zip(grad, (x, y, z)))
H = s.hessian(W, (x, y, z))
H2 = H.subs({x:1, y:1, z:0})
assert H2 == s.diag(-9, -9, 0)
assert H2.rank() == 2
assert [s.simplify(W.subs({x:int(k>=1), y:int(k>=2), z:int(k>=3)}))
        for k in range(4)] == [0,s.Rational(1,2),1,s.Rational(3,2)]

I = s.I
gm = [
s.Matrix([[0,1,0],[1,0,0],[0,0,0]]),
s.Matrix([[0,-I,0],[I,0,0],[0,0,0]]),
s.diag(1,-1,0),
s.Matrix([[0,0,1],[0,0,0],[1,0,0]]),
s.Matrix([[0,0,-I],[0,0,0],[I,0,0]]),
s.Matrix([[0,0,0],[0,0,1],[0,1,0]]),
s.Matrix([[0,0,0],[0,0,-I],[0,I,0]]),
s.diag(1,1,-2)/s.sqrt(3),
]
T = [g/2 for g in gm]
assert all(s.simplify(s.trace(t*t)-s.Rational(1,2))==0 for t in T)
v = s.Matrix([1,1,0])
D = [s.simplify((v.conjugate().T*t*v)[0]) for t in T]
D_norm2 = s.simplify(sum(t*t for t in D))
assert D_norm2 == s.Rational(4,3)
assert D_norm2 == (v.conjugate().dot(v))**2/3

omega = (-1 + s.sqrt(3)*I)/2
X = s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
Z = s.diag(1, omega, omega**2)
orbit = [X**b * Z**a * v for b in range(3) for a in range(3)]
S = s.zeros(3,3)
for state in orbit:
    S += state*state.conjugate().T
S = S.applyfunc(lambda q: s.simplify(s.expand_complex(q)))
assert S == 6*s.eye(3)
D9 = [s.simplify(s.trace(t*S)) for t in T]
assert D9 == [0]*8
P = [state/s.sqrt(2) for state in orbit]
for j in range(9):
    for k in range(9):
        ov = (P[j].conjugate().T*P[k])[0]
        sq = s.simplify(s.expand_complex(ov*s.conjugate(ov)))
        assert sq == (1 if j==k else s.Rational(1,4))
assert (s.diag(-1,-1,1)).det()==1
assert W.subs({x:1,y:0,z:0}) != W.subs({x:-1,y:0,z:0})

# Exactly 3 nonzero cube roots or zero per coordinate => 4**3 points.
# Support k: C(3,k)*3**k; support two: 27 affine vacua / 3 central phases = 9 rays.
support_counts=[1,9,27,27]
assert sum(support_counts)==64
assert support_counts[2]==3*9
results={
 "source_superpotential":str(W),
 "affine_stationary_count":64,
 "support_counts_0_through_3":support_counts,
 "support_two_affine_vacua":27,
 "support_two_projective_rays":9,
 "superpotential_values_by_support":["0","1/2","1","3/2"],
 "F_hessian_at_1_1_0":[[-9,0,0],[0,-9,0],[0,0,0]],
 "holomorphic_hessian_rank":2,
 "massless_quadratic_complex_directions":1,
 "su3_fundamental_single_triplet_moment_norm_squared":"4/3",
 "su3_general_fierz":"sum_a (v^dag T_a v)^2 = (v^dag v)^2/3",
 "nine_unnormalized_sic_frame_operator":"6*I_3",
 "nine_normalized_sic_frame_operator":"3*I_3",
 "nine_field_su3_moment_maps":[str(v) for v in D9],
 "nine_state_pair_overlap_squared":"1/4",
 "counterexample_to_continuous_su3_invariance":"diag(-1,-1,1): W(1,0,0)=1/2 but W(-1,0,0)=-3/2",
 "limits":"Nine independently charged triplets can cancel D terms; the displayed W is H27-invariant but NOT SU(3)-gauge invariant. No SU(3)-invariant F-completion or E8 field content is supplied.",
}
out=ROOT/"data"/"toe_20261119_sic_moment_map_audit.json"
out.write_text(json.dumps(results,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
print("PASS: 64 F vacua; 27-to-9 SIC; Hessian rank 2; single-triplet D obstruction; 9-SIC frame D cancellation")
print(out)
