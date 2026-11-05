# November 5, 2026 — Odd-field null-history clock and continuum guard

**Status:** analytic finite-field theorem with executable checks; NOT a physical time or gravity theorem.

## Source and novelty audit

- `papers/forty_points/main.pdf`, Section 4.4, constructs the 27-event qutrit clock with
  adjacency spectrum `8^1, 2^12, (-1)^8, (-4)^6` and order-three tick.
- `analysis/PASS11540_HISTORY_VO33_ORIENTATION_SQUARE.md` identifies the graph as
  parabolic affine polar `VO(3,3)`.
- `analysis/PASS11541_HISTORY_QUADRATIC_SHELL_SCHEME.md` gives the full q=3
  association-scheme eigenmatrix. `analysis/w33_pass11547_history_hamming_canonical_clock.py`
  exhibits its exceptional `K_3` triple-tensor/Hamming realization.
- This does **not** invent affine polar graphs, finite Gauss sums, or quantum walks.
  The contribution is their **general odd-field clock implication** and a
  quantitative obstruction to the naive growing-field continuum limit.
  References: https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/generators/classical_geometries.html
  and https://pmc.ncbi.nlm.nih.gov/articles/PMC9858314/ .

## Theorem: universal spectral clock

Let `q` be an odd prime power and
`V=Sym_2(F_q)~F_q^3`, with `Q(t,x,y)=t^2-x^2-y^2`.
Join distinct elements `v,w` when `Q(v-w)=0`. The resulting Cayley graph
has `n=q^3` vertices, degree `k=q^2-1`, and exactly

| adjacency eigenvalue | multiplicity |
|---|---:|
| q^2-1 | 1 |
| q-1 | q(q^2-1)/2 |
| -1 | q^2-1 |
| -(q+1) | q(q-1)^2/2 |

Its Laplacian has levels `0, q(q-1), q^2, q(q+1)`. Thus the
finite-dimensional unitary `U_q=exp(-2*pi*i*L/q^2)` has **exact order q**,
with fixed eigenspace dimension `q^2` and other two phases primitive
qth roots, of multiplicities `q(q^2-1)/2` and `q(q-1)^2/2`.
For q=3 this is precisely the clock in the manuscript; **spectral recurrence alone
does not select a ternary physical clock**.

### Analytic proof

Write the connection set `C={v != 0:Q(v)=0}`. The standard Gauss-sum
identity counts `|C|=q^2-1`; characters of the translation group
diagonalize its Cayley adjacency. For a nonzero dual character indexed
by `m`, the cone Fourier sum is
`-1` when `Q*(m)=0`, and otherwise
`-1+q*chi(-Q*(m))`, where `chi` is the quadratic character and
`Q*=Q` in the diagonal coordinates. The nonzero dual null vectors
number `q^2-1`. For each nonzero field value `a`,
`# {m:Q*(m)=a}=q^2+q*chi(-a)`.
Summing over the two nonzero square classes produces the asserted
multiplicities. This proof works for **odd prime powers**, although the
supplied executable checks five **prime** fields.

## Quantified no-go for the naive continuum scaling

Set `P=A/(q^2-1)` and `J` the all-ones matrix.
The exact operator norm on the complement of constants is

`||P-J/q^3||_2=1/(q-1) -> 0`.

The normalized Laplacian `L/q^2` has spectral mean
`1-q^-2` and variance `q^-2-q^-4 -> 0`.
Its empirical spectral measure therefore collapses to a point mass
at 1 rather than developing the low-frequency spectrum of a local
continuum Laplacian. This rules out **this unweighted, full-symmetry,
stochastic-normalization limit** as a route to nontrivial local wave or
Einstein dynamics. It does **not** rule out suitably weighted graphs,
new embeddings, causal propagation, selected null directions, or another
continuum construction.

The q=3 Hamming distance-three factorization is also arithmetically
exceptional: `(q-1)^3=q^2-1` holds for q>=3 precisely at q=3.
So the spectral q-clock generalizes, while that specific three-factor
Hamming clock does not.

## Reproduction

`python analysis/w33_20261105_general_q_null_clock_continuum_guard.py`

Writes `data/w33_20261105_general_q_null_clock_continuum_guard.json`.
Checks q=3,5,7 by exact integer adjacency minimal-polynomial identity;
for q=3,5,7,11,13 independently checks Fourier eigenvalues and
multiplicities numerically with explicit rounding tolerance.
Floating FFT verification is **not** mislabeled as an exact-computer proof;
the general statement rests on the Gauss-sum argument above.
