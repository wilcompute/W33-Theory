# The higher-prime Lorentz Gaussian clock is a three-qudit Clifford circuit

**Research date:** November 8, 2026.  
**Executable producer:** analysis/w33_20261108_odd_prime_clifford_compiler.py  
**Tests:** tests/test_w33_20261108_odd_prime_clifford_compiler.py  
**Workflow:** .github/workflows/w33_20261108_odd_prime_clifford_compiler.yml  
**Full certificate:** data/w33_20261108_odd_prime_clifford_compiler.json, committed and independently regenerable in GitHub Actions.

**Prior repository ownership:** papers/forty_points/sec04_time.tex already identifies the q=3 spectral clock as a Clifford gate (and distinguishes it from a perfect three-qutrit temporal scrambler); analysis/w33_20261108_lorentz_chirp_escape.py already proves the higher-prime determinant Gaussian is flat and unitary but that its principal-logarithm Hamiltonian is nonlocal; the first 27-mode four-SUM/27-tritter compiler is in PASS20261108_DEEP_FIVE_FRONTS.md. This pass adds an explicit uniform generalized-qudit gate synthesis, its field-dependent local rescaling, six-prime Pauli conjugation tests, and honest q^3 rail-resource asymptotics. No independent publication novelty is claimed.

## 1. A constant logical gate-depth theorem, for odd finite fields

Let Fq have odd characteristic and let q(a,b,c)=ac-b² on the 3D vector space Sym2(Fq). Write ζ for a nontrivial additive character and define the Gaussian complex-Hadamard clock

\[
U_{x,y}=q^{-3/2}\,\zeta\bigl(\det(x-y)\bigr).
\]

Set t=(a+c)/2, x=(a-c)/2, keeping b unchanged. Then

\[
ac-b^2=t^2-b^2-x^2.
\]

Let P be the invertible permutation of the q³ computational basis states induced by this linear coordinate change. Define the one-qudit quadratic Fourier gate

\[
H_\sigma(j,k)=q^{-1/2}\,\zeta\bigl(\sigma(j-k)^2\bigr),\qquad \sigma=\pm1.
\]

The three-factor Gaussian identity follows immediately:

\[
\boxed{U=P^{-1}(H_+\otimes H_-\otimes H_-)P.}
\]

The original input/output kernel is consequently uniform, and its unitarity follows from the orthogonality of each one-qudit quadratic Fourier transform. For all odd prime powers q this is a finite-field identity; the included code directly tests prime fields p=3,5,7,11,13,17.

## 2. Four generalized SUMs plus two optional one-qudit multipliers

Let r=2^{-1} in Fq. The forward coordinate map on (a,b,c) is

1. **SUM:** c <- c-a.
2. **SUM:** a <- a+r*c, using the updated c.
3. **Local multiplier:** c <- (-r)*c.

It yields (t,b,x)=(r(a+c),b,r(a-c)). After the three one-qudit Gaussian gates, undo it:

1. **Local multiplier:** c <- (-2)*c.
2. **Inverse SUM:** a <- a-r*c.
3. **Inverse SUM:** c <- c+a.

This uses **four two-qudit controlled SUMs**, **three single-qudit Gaussian Fourier gates**, and **two one-qudit multipliers**. All modular additions and scaling maps are Clifford.

The q=3 simplification is exact and easy to miss: -1/2=1 in F3, so both multiplier gates are the identity. That is why the native 27-event compiler needs only the four SUMs and the 27 three-port Gaussian operations, whereas higher odd-prime realizations need additional local basis relabelings.

## 3. Clifford, not universal computation

Each one-qudit Gaussian unitary has the exact factorization

\[
\boxed{H_\sigma = D_\sigma\,F_{-2\sigma}\,D_\sigma}
\]

where Dσ(j,j)=ζ(σ j²) is a quadratic phase and Fκ(j,k)=q^-1/2 ζ(κjk) is a scaled Fourier transform. All Dσ and Fκ normalize generalized Pauli operators. The code independently conjugates the one-qudit X and Z generators by H+ and H− at each prime and verifies that the result is a single Pauli monomial up to a unit-modulus phase.

Therefore the entire three-qudit determinant clock lies in the **generalized Clifford group**. Its constant logical depth and flat port intensities do not make the circuit computationally universal. Universality needs an additional verified non-Clifford gate/state/injection mechanism and fault-tolerant error model. This conclusion is consistent with (and extends in field size) the pre-existing Forty Points discussion at q=3.

The module is **not** a local continuous-time Hamiltonian on the graph's null edges: an exactly compact logical circuit on three tensor registers can correspond to very nonlocal long-range couplings in the single-particle 125-rail graph. Those are inequivalent notions of locality.

## 4. Optics resource estimates with the routing cost explicitly excluded

Represent the three logical q-level registers as q³ single-photon rail modes. Each one-qudit Gaussian gate acts on q levels and must be replicated across the q² settings of the two other coordinates. There are three such local gates, so **3q² independent q-port Gaussian modules**.

An arbitrary q-by-q unitary can be decomposed into no more than q(q−1)/2 two-mode mixing interactions. A conservative internal-local-gate bound is therefore (3/2)q³(q−1) interactions, versus q³(q³−1)/2 in a generic universal q³-mode mesh.

| Prime p | Rails p³ | Local p-port Gaussian modules | Internal two-mode upper bound | Generic mesh upper bound |
|---|---:|---:|---:|---:|
| 3 | 27 | 27 | 81 | 351 |
| 5 | 125 | 75 | 750 | 7,750 |
| 7 | 343 | 147 | 3,087 | 58,653 |
| 11 | 1,331 | 363 | 19,965 | 885,115 |
| 13 | 2,197 | 507 | 39,546 | 2,412,306 |
| 17 | 4,913 | 867 | 117,912 | 12,066,328 |

The internal-local gate bound scales as O(p^4), versus O(p^6) for a generic full unitary mesh. **This is not a complete physical resource advantage.** The four controlled-SUMs are large rail permutations that may introduce routing, crossings, switch depth, loss, crosstalk and phase drift. Multiplication by field scalars is also an internal rail permutation, not free hardware. The earlier 84-adjacent-swap optimized arrangement applies specifically to the q=3 three-b-block layout; it is not automatically transferable to p=5 or higher. No fabricated device or quantitative loss model is produced here.

## 5. Verification

The independent authorized desktop executed the six-prime constructor, checked every displacement type for every p, sampled independent input/output pairs, verified all local H± unitaries and quadratic Fourier factorizations, and checked each H± Pauli X/Z image. The gate count and asymptotic resource formulas were also independently asserted. **22/22 focused tests passed** in the isolated environment, without modifying the ongoing desktop's staged/uncommitted work. GitHub Actions separately regenerates the JSON certificate when its workflow runs.

At the finite-field level, the derivation is exact; numerical floating-point checks serve only as reproducibility witnesses. There is no novel quantum mechanics or experimentally demonstrated TOE in this identity.

## Five independent falsifiers

1. **Non-Clifford photonics:** prove an available physical non-Gaussian/magic operation on the same three-register single-photon encoding, and check whether it escapes the present stabilizer-only computational class.
2. **Full routing design:** optimize q=5 125-rail permutations and all p-port-group changes, including loss and coherent error; do not claim 750 physical couplers without this.
3. **Local generator obstruction:** characterize the logarithms of the determinant-clock unitary under a null-local Hamiltonian ansatz. A compact quantum circuit is not sufficient.
4. **Gauge polarizations:** couple the H1 harmonic spectrum to dynamical exact/coexact 1-forms to construct a two-mode, translation-covariant physical gauge bundle.
5. **Symmetry fidelity:** measure the q=5 full-affine symmetry-breaking witness with interferometric phases; compare the index-two isometry-preserving clock against the exact no-go bound for full GL2 covariance.
