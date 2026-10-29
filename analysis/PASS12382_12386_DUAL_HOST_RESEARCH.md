# Passes 12382–12386: two-host research and five explicit continuations

Reservation: `08928f58d3afeaedf9235d850576b20bc1841875`, following the
formula-universe refresh `a27bf1888`. No new science commits intervened after
the previous packet `03e5e854a`. GitHub publication preserves that refresh and
the other track's 12369–12376 reservation.

The Windows host **TheHeavyCrown** and the Linux server both ran computations.
GitKraken MCP was invoked through its installed `gk mcp` stdio server on Windows,
with actual status, fetch and worktree tools. The original
`C:\Repos\Theory of Everything` contained unrelated edits, so computation and
cross-host verification used a clean detached worktree,
`C:\Repos\w33_dualhost_12382`, created at the reservation. Synchronization and
preservation receipts record the eventual remote and local states.

## 12382: finite-field elimination makes much larger exact grids practical

For the same exceptional polynomial Q from Pass12346, write

`Q(a,b,c,d)=6*d^2+(-6*a+6*b-6*c-6)*d`
` +5*a^2-5*a*b+a*c+5*b^2-5*b*c-6*b+5*c^2+6`.

For n not divisible by4 choose good primes `p=1 mod n`, `p=3 mod4` and a
primitive n-th root r in Fp. Any exact torsion zero maps to a zero modulo p.
The producer enumerates n^3 triples, takes the two quadratic roots in the
fourth variable, and retains only roots in the n-th-root subgroup. A second
prime eliminates false survivors; final candidates are verified by integer
remainders modulo `Phi_n`. Thus reductions prove exclusions and exact
cyclotomic arithmetic proves retained zeros. A modular survivor alone is
never called an exact zero. The quadratic leading coefficient6 is invertible
at every chosen prime. Integer operations stay within signed64-bit range for
the recorded primes; the small-grid independent tests check the full method.

Windows ran n=`70,77,91,105,121,143,169,195,231,385,715`; the largest job took
about314 seconds. The n=715 grid represents **261,351,000,625** characters,
decided by365,525,875 quadratic triples, not by iterating n^4 points. There
are no nonidentity zeros on that grid. Server jobs add and cross-check grids;
the JSON retains every prime, primitive root, candidate count and exact root.

Combining the new decisions with the previous exact small grids covers36
distinct exact orders and grids totalling289,349,094,520 characters (overlap
between grids is not subtracted). The only nonidentity points found remain
the ten exact order-three points. **Every pure prime-power order allowed by
the earlier464-order bound is now decided**: the full prime-power list is
`2,3,4,5,7,8,9,11,13,16,25,27,32,49,121,169`; only3 occurs nontrivially.
There remain428 necessary mixed orders outside the certified divisor coverage.
Prime-power exclusion does not exclude arbitrary mixed orders.

The reduction principle is standard; the project-specific contribution is the
quadratic elimination producer and its exact enlarged grid decisions. Context:
Conway–Jones, *Trigonometric diophantine equations*,
<https://doi.org/10.4064/aa-30-3-229-240>, and the algorithm literature on sparse
equations in roots of unity. This is not a full torsion classification.

## 12383: metric-matched dispersion, with a fixed repair budget

The previous packet deliberately used unit mixed-loop weights. This continuation
uses the actual matched metric of
`analysis/w33_20261028_three_mixed_loop_minimal_maxwell.py`:

```
K = [[25/9,-5/3,-26/9],[-5/3,11/3,2],[-26/9,2,28/9]].
```

The full135-link operator contains unit short-face terms and `(R L)^dag K(R L)`.
The identity electric link metric, external Hamiltonian time and epsilon=.001
remain supplied. Repair channels0 and5 have weights `(t,2-t)`; the parameter
is constrained to `[.01,1.99]` so both channels remain active. This preserves
the old all-unitary kernel-repair argument. It is not a minimum-coupling theorem.

On24 frozen momenta (four declared points plus20 points from seed12383),
optimize the minimum physical eigenvalue divided by `k^T G k`:

| Quantity | Value |
|---|---:|
| Equal-weight worst sampled ratio | 0.00008708840467274168 |
| Optimized worst sampled ratio | 0.00016913611869078947 |
| Optimized channel weights | (1.989999907580563, 0.010000092419437) |

The approximately94% improvement is **sample-specific**, near the imposed
parameter boundary. It is not an all-momentum energetic optimum. Full-link
infrared eigenvalues converge to the common matched value: along e1 the
target is10/27 and at t=.0005 the three values are approximately
(.37030105,.37036989,.37043754). Along (1,2,-1,1) the target is94/27 and all
three values are within0.1% at the smallest tested step. No physical light
speed, Lorentzian signature or selected Maxwell action follows.

## 12384: interacting finite-frequency Ward identity

Use one up and one down fermion on all27 native sites: a729-dimensional
number-conserving Hubbard sector with onsite U=0,2,8. For a normalized vertex
potential phi, let `u=B phi`, let rho be the two-particle density generated by
phi and include the full Peierls contact term. The producer verifies

`J_u = i[H,rho]`,

and, at imaginary frequencies0,.5,2,8,

`K_uu(i omega) = omega^2 * chi_rho_rho(i omega)`.

Residuals are below1e-12 for every recorded case. At omega=.5 the scalar
susceptibilities decrease with U: .00128866605, .00127267589, .00124776101.
The literal native-triangle response is also recorded. Omitting the contact
term fails the Ward test. This is an interacting finite-frequency calculation,
not merely a charge-count identity or the previous free432-site determinant.

Separately, exact SM-plus-right-neutrino hypercharge and B-L inventories have
vanishing linear and cubic Abelian moments. The charge inventory is not the
Hubbard Hilbert space and does not make the finite model chiral. A four-dimensional
interacting chiral measure, anomaly matching beyond this inventory, dynamical
masses and a selected frequency-dependent gauge action remain unbuilt.

## 12385: audit a concrete four-dimensional string input

The primary source <https://arxiv.org/abs/2011.04113v2> supplies a particular
S-class Pati–Salam example in equations5.1 and7.4. The producer now contains
its13-by64 real-fermion boundary basis and13-by13 GGSO matrix. It checks
order-two overlap congruences, GGSO reciprocity and diagonal phases, the
listed top-Yukawa phase conditions, and level matching for the published
low-order partition terms. Changing one GGSO entry fails reciprocity.

The published zero constant term does not remove the off-shell term
`2 q^0 qbar^-1`. The executable distinguishes that term from a physical
level-matched tachyon. Published low-order series coefficients are stored as
source data, not falsely described as independently regenerated coefficients.

These are necessary input and consistency checks. The full8192-by8192
spin-structure phase extension, complete massive spectrum, numerical S test,
Higgs vacuum and W33 embedding have **not** been constructed. The source's
tachyon-freedom and chirality conclusions are not independently certified by
these necessary checks. This is a concrete alternative input beyond the
99-model Z6-II sample, not a completed new string vacuum or a zero-CC result.

## 12386: a faithful quantum bridge beyond the permutation obstruction

The old rank-nine map used the **regular address27**, whose central characters
cannot all map into a centre-trivial coordinate-permutation module. That
obstruction remains. A different source is the **operator27**: nine copies of
the three-dimensional Schrödinger representation, the type already associated
with the trinification H27. The two27-dimensional spaces are not interchangeable.

Choose a nine-code orbit of the two disjoint three-cycles on eight Hamming
coordinates. Build the actual CSS vectors `|C_v>` in the256-dimensional qubit
amplitude space. Their exact Gram matrix is `(3I+J)/4`, so the nine Fourier
combinations are independent: their squared norms are3 for the trivial character
and3/4 for the other eight. Normalize them to `|chi_(r,s)>`.

Add **one auxiliary qutrit**, with

`sigma(a,b,c)=omega^c X^a Z^(-b)`.

This follows exactly the native law `c+C-b*A`. Define the explicit isometry

`T(|r,s> tensor |psi>) = |chi_(r,s)> tensor X^s Z^r |psi>`.

The target action is the actual eight-qubit coordinate permutation tensor
sigma. Every one of the27 native group elements satisfies the intertwining
identity in the full768-amplitude space. The map has rank27 and `T^dag T=I`;
the largest numerical intertwining residual is below5e-16. The controlled-Weyl
phase identity and all729 group products are also checked modulo3 exactly.
The centre acts as omega, supplied by the added qutrit, so this operator
representation is faithful. Omitting that carrier restores the obstruction.

This is a specific realization of standard finite-Heisenberg character
untwisting; see <https://arxiv.org/abs/2104.14890> for the established central-
character representation framework. It does not derive the extra qutrit from
W33, produce a native E6 action or specify a hardware preparation circuit.
It closes the previously unnamed quantum intertwiner at the cost of an
explicit added resource.

## Reproduction

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python analysis/w33_pass12383_12386_dualhost_fronts.py
python analysis/w33_pass12382_cyclotomic_sieve.py 15,21,35,55,65 output.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest -q tests/test_pass12382_12386_dualhost.py tests/test_pass12377_12381_continuation.py
```

The combined server suite passes12 tests. Windows receipts record actual
producer versions, numerical comparisons and its own test results. The original
paper remains the fully read211-page pinned text from the preceding packet;
this packet makes no new complete historical-reading claim. No TOE closure is
claimed. Full repository-index refresh and local synchronization are recorded
in the final receipt rather than inferred from starting a process.

## Five independent next investigations

1. Replace finite grids by a complete torsion-coset elimination covering the428
   remaining necessary orders, with a machine-checkable certificate.
2. Obtain certified lower bounds on the repaired normalized stiffness over the
   continuous torus, including neighborhoods of exceptional characters.
3. Build a chiral regulator with its measure and temporal gauge field, then test
   the interacting Ward identity beyond a fixed two-particle sector.
4. Reconstruct the concrete S-model's entire spin-structure sum and regenerate
   its spectrum before asserting modular or vacuum viability.
5. Derive or physically prepare the auxiliary qutrit and the27-state Hamming
   isometry, and test whether a full E6 action has a useful native realization.
