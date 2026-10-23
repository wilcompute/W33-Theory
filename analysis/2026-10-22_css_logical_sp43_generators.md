# Explicit 20-qutrit logical PSp(4,3) gate representation — 22 October 2026

## Exact finite computation

The projective-point CSS code from W(3,3)'s ternary noncollinearity
matrix B has length 40 and a self-orthogonal row code C of dimension
10, so its logical Pauli label quotient Q = C^perp/C has dimension 20.
The earlier all-q Pascal-CSS theorem proves distance 4 for this code,
giving [[40,20,4]]_3. This is **not** the 240-edge homological CSS code.

This packet converts the previously certified nontrivial logical
transvection/Jordan action into explicit 20-by-20 matrices over F3.
It avoids inferring physical gate locality from abstract group theory.

Let omega be the standard alternating form with J consisting of two
2-by-2 symplectic blocks. For nonzero vectors w define

    tau_w(x) = x + omega(x,w) w.

The following five vectors suffice:

    e1, e2, e3, e4, e1+e3.

The program computes their permutations on the forty projective
points, proves that each preserves B, and constructs 20-by-20 matrices
for their actions on Q. It uses an exact quotient basis over F3 and
checks that every generator preserves the 30-dimensional kernel of B
and the 10-dimensional stabilizer code.

## Exact generator closure

Exhaustive BFS in the 40-point permutation group gives:

| Generator prefixes | Exact group order |
|---|---:|
| e1 | 3 |
| e1,e2 | 24 |
| e1,e2,e3 | 72 |
| e1,e2,e3,e4 | 288 |
| e1,e2,e3,e4,e1+e3 | 25,920 |

This is the entire PSp(4,3) projective incidence group, not the
51,840-element symplectic double cover. Each permutation has cycle
type 1^13 3^9: thirteen fixed points and nine disjoint triple cycles.

The cycle count has an elementary general-prime proof. A nontrivial
transvection fixes the projective hyperplane P(w^perp), containing
p^2+p+1 points of PG(3,p). The remaining p^3 points are moved;
transvections have order p, so those points form exactly p^2
p-cycles. For p=3 this specializes to 13 fixed points and 9 3-cycles.
Over q=p^t the same reasoning gives q^2+q+1 fixed points and
q^3/p cycles of length p (not cycles of length q).

Every induced logical matrix is invertible, has cube equal to identity,
and satisfies rank(T-I) = 10. The exact nontrivial Jordan type is

    J_1^3 + J_2^4 + J_3^3.

One hundred deterministic random words independently check the
logical-matrix composition against the direct permutation action.
Thus there is a concrete representation

    rho : PSp(4,3) -> GL(20,3).

Because PSp(4,3) is simple and rho is nontrivial, rho is faithful.
The logical Z-labels carry the dual action, hence the corresponding
40-coordinate physical permutations implement encoded Clifford
transformations on the CSS code.

## Operational interpretation and limits

All nine 3-cycles are disjoint and can be executed as parallel wire
permutations **in an ideal all-to-all routing model**. A wire
permutation preserves Pauli-error weight; it does not multiply an
existing single-qudit error across qudits. That is a precise
fault-propagation advantage at the logical-circuit level.

However:
- The [[40,20,4]]_3 code consists of forty *physical qutrits*;
  it is not automatically encoded in a single photon or in forty
  optical modes of one photon.
- Real photonic routing connectivity, losses, crosstalk, timing,
  native gate realizations and threshold remain unverified.
- These are Clifford operations. A non-Clifford magic protocol is
  still required for universal computation.
- The result yields no gravitational field equation, chirality
  selection, measured Standard Model parameters, or TOE.

## Independent prior art

The relevant field is modular incidence representation theory, not
a new exceptional-group numerology. We compared against:

1. Chandler, Sin and Xiang (2007), *The permutation action of finite
   symplectic groups of odd characteristic on their standard modules*,
   Journal of Algebra 318, 871-892. DOI 10.1016/j.jalgebra.2007.08.020.
2. Bardoe and Sin (2000), *The permutation modules for GL(n+1,q)
   acting on projective space*, J. London Math. Soc. 61, 58-80.
3. Kaplan and Kim (2024), *Hulls of Projective Reed-Muller Codes*,
   arXiv:2406.04757.

The existence of the action is standard finite geometry; what this
artifact adds to W33-Theory is an exact reproducible **five-generator
logical basis, full closure, and word-level verification**.
No mathematical priority is claimed.

## Reproduction

    python analysis/w33_20261022_css_logical_sp43_generators.py
    python -m pytest -q tests/test_w33_20261022_css_logical_sp43_generators.py

Certificate:
data/PART_20261022_CSS_LOGICAL_SP43_GENERATORS.json.

## Five independent next experiments

1. Determine the full modular composition series of the 20-dimensional
   logical representation, with rational/formal Brauer-character controls.
2. Compile each of the nine disjoint 3-cycles to realistic optical
   or qutrit-hardware routes and compute fault/error budgets.
3. Search the code's full coordinate automorphism group for additional
   logical Clifford gates beyond the symplectic incidence subgroup.
4. Derive the all-prime transvection Jordan formula analytically,
   including the extension class of C in ker(B).
5. Test a non-Clifford injection and distillation circuit on the actual
   [[40,20,4]]_3 syndrome decoder, not on an abstract module alone.
