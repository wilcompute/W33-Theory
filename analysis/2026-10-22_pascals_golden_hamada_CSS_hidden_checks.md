# October 22, 2026 — Pascal CSS distances, golden Hamada recurrence, and hidden line constraints

**Scope:** exact finite projective geometry and quantum-code parameters; classical RH remains unproved. These results build on published Hamada/Smith rank theorems and earlier repository W33 code work; no mathematical priority or physical hardware claim is made.

## Existing repo results checked

- The rank formula rank_Fp(B) = binomial(p+2,3)^t and B²=0 over Fp for W(3,p^t) appear in analysis/w33_20261022_six_algebra_optics_frontiers.py and earlier incidence rank research.
- analysis/w33_pass5744_5751_quadratic_code_overlays.py already establishes the q=3 ternary self-orthogonal code, its dual distance 4 and CSS [[40,20,4]]_3. It establishes complete line checks only at q=3.
- The projective hyperplane p-rank is classical (Smith 1969); the general point-line p-rank transfer is Hamada (1968), presented explicitly in Eric Moorhouse, p-Ranks Lecture 5 (https://ericmoorhouse.org/slides/5_p-Ranks.pdf).
- Projective geometric code minimum-weight literature: Lavrauw–Storme–Van de Voorde, https://arxiv.org/abs/1201.3290.

## I. Exact all-prime-power CSS distance

Let q=p^t and v=(q+1)(q²+1), the points of PG(3,q). Define B_xy=1 if the symplectic pairing of projective points x,y is nonzero, else 0. Over Fp, B is symmetric, B²=0 and its rank is r=binomial(p+2,3)^t. Hence row(B) is self-orthogonal and gives a q-characteristic CSS code with k=v-2r.

**Proof that the quantum distance is precisely q+1:**

There are v hyperplanes; through each point pass h=q²+q+1 hyperplanes, and through each pair pass q+1. Suppose a word in ker B has support S of r0<=q points. Since q*h=v-1, some hyperplane avoids all of S. Its complement row forces the coordinate sum c(S)=0. For each s in S there also exists a hyperplane containing s and no other member of S because h-(q-1)(q+1)=q+2>0. Its complement row forces c(S)-c_s=0, so every c_s=0. Thus there is no nonzero dual word of weight <=q.

A projective line has exactly q+1 points. Every hyperplane either contains that line or intersects it in one point; the line has 0 or q points outside the hyperplane, both zero mod p. Thus its indicator lies in ker B and has weight q+1. Each B row has coordinate sum q³=0 mod p, whereas the line indicator has coordinate sum q+1=1 mod p, so the line is outside row(B): a nontrivial CSS logical operator.

Consequently, for all prime powers q=p^t,

    CSS = [[(q+1)(q²+1), (q+1)(q²+1)-2*binomial(p+2,3)^t, q+1]]_p.

The code reconstructs the finite fields and validates B², modular rank, projective line indicators and the hyperplane counting bounds for q=2,3,4,5,8,9. Results:
q2 [[15,7,3]]_2;
q3 [[40,20,4]]_3;
q4 [[85,53,5]]_2;
q5 [[156,86,6]]_5;
q8 [[585,457,9]]_2;
q9 [[820,620,10]]_3.

**Important:** Projective-line indicators are classical dual parity-check words but *nontrivial quantum logical operators*. They are NOT interchangeable with CSS stabilizer generators, which must lie in row(B).

## II. Ambient line checks lose completeness at extension fields

Each physical coordinate belongs to exactly q²+q+1 projective lines. These form q²+q+1 disjoint-by-helper local recovery groups, each using q other symbols in the classical code row(B).

However, although the 130 projective lines at q=3 span the full 30-dimensional classical dual, the same phenomenon fails at q=4 and q=8.

Independent finite-field RREF line enumeration and modular row elimination:

| q | projective lines | rank of their checks | dim dual | missing checks |
|---:|---:|---:|---:|---:|
| 2 | 35 | 11 | 11 | 0 |
| 3 | 130 | 30 | 30 | 0 |
| 4 | 357 | 61 | 69 | 8 |
| 5 | 806 | 121 | 121 | 0 |
| 8 | 4745 | 401 | 521 | 120 |

At q=9, Hamada's published transfer predicts a line rank of 590 versus dim dual 720: 130 missing independent directions. The 7462x820 ternary incidence matrix has not been fully eliminated in this pass.

## III. Hamada transfer gives a genuine golden-ratio recurrence

Let c_j be the coefficient of x^j in (1+x+...+x^(p-1))^4 and let

    M_p = [[c_(p-1),c_(p-2)],
           [c_(2p-1),c_(2p-2)]].

Hamada's known formula for point-line incidence in PG(3,p^t) is rank = 1+tr(M_p^t). By explicit binomial simplification,

    M_p = [[p(p+1)(p+2)/6, p(p-1)(p+1)/6],
           [2p(p-1)(p+1)/3, p(2p²+1)/3]].

At p=2, M2=[[4,1],[4,6]], eigenvalues 5±sqrt5. Their ratio is phi² exactly. Therefore binary line rank is

    1+2^t*5^(t/2)*Lucas(t)    (t even)
    1+2^t*5^((t+1)/2)*Fib(t) (t odd).

The producer checks both integer identities against the matrix-power rank formula for twelve positive t values. The ranks begin 11,61,401,2801,20001.

This is an intrinsic Q(sqrt5) transfer law, not a decimal-to-phinary conversion. The two eigenvalues have unequal complex absolute values and CANNOT be conjugate eigenvalues of a single pure-weight finite-field Frobenius packet. Thus a zeta critical line cannot be inferred from these transfer eigenvalues.

## IV. A universal positive hidden-check gap at q=p²

Combining the dual dimension and Hamada rank gives the closed expression

    gap(p,2)=p²(p-1)²(5p²+4p+8)/18.

It is strictly positive for all primes p. Examples from exact transfer arithmetic: p2 ->8, p3 ->130, p5 ->3400, p7 ->27538, p11 ->441650.

For q=2^t, the all-t formula is

    gap(t) = 8^t+2^t-(5+sqrt5)^t-(5-sqrt5)^t.

At t=1 it vanishes. At every t>=2 it is strictly positive, because (8,2) strictly majorizes (5+sqrt5,5-sqrt5), their sums agree, and x^t is strictly convex. For growing t the number of sparse line-check directions is O((5+sqrt5)^t), but the full dual dimension grows as 8^t: most dual directions escape line generation.

## V. Reproduction and boundaries

Producer: analysis/w33_20261022_allq_pascal_CSS_exact_distance.py
Producer: analysis/w33_20261022_hamada_golden_hidden_checks.py
Tests: tests/test_w33_20261022_allq_pascal_CSS_exact_distance.py
Tests: tests/test_w33_20261022_hamada_golden_hidden_checks.py
CI: .github/workflows/w33-allq-pascal-CSS-exact-distance.yml
CI: .github/workflows/w33-pascal-CSS-hamada-hidden-checks.yml

Generated certificates:
data/w33_20261022_allq_pascal_CSS_exact_distance.json
data/w33_20261022_hamada_golden_hidden_checks.json

The all-q CSS CI passed. Later Hamada-specific CI should be checked for final status; do not claim an unverified latest run has passed.

These identities are exact finite arithmetic and projective geometry. They are not hardware fidelity measurements, fault-tolerance thresholds, a canonical arithmetic Galois/Weil operator, a quantum theory of spacetime, or a proof of the classical Riemann hypothesis.

## Independent high-value follow-ups

1. Construct the missing dual parity-check modules in q4 and q8, determining their minimum weight, automorphism characters and field-descent decomposition.
2. Identify the natural Z[phi] module for the golden two-state transfer, and prove exactly which primes split, remain inert or ramify. Test whether any arithmetic motive can support the *mixed* transfer spectrum, rather than incorrectly asserting Weil purity.
3. Decode the exact CSS family under explicit independent depolarizing and correlated noise models, and model syndrome extraction costs from the dense B stabilizers.
4. Reproduce the finite-prime CCM spectral triple with certified interval arithmetic and correct Hilbert metric. Compare all low Xi moments and universal completed Weil positivity tests, not merely first-zero agreement.
5. Extend Hamada's Pascal-carry transfer algorithm beyond PG(3,q) to higher-dimensional symplectic and polar incidence, testing whether new low-dimensional modular representation algebras occur.
