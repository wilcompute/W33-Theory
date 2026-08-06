# Passes 3981–3988 — five-front closure and three chained photon constructions

## Promoted status

```text
PASS_FIVE_FRONTS_THREE_PHOTON_CONSTRUCTIONS_MONSTER_WORDS_PENDING
767e5fc07b97fb53d9e53d75381fbabf46ab775557a7a19151641d3b64f53ba8
```

This packet starts from the stronger of the two reconciled Passes 3973–3980 certificates. In particular, it does not repeat or weaken the exact fixed-parent extremality proof or the literal orbital-tensor reconstruction.

## 3981 — global `A4=57` extremality retained; uniqueness remains separate

The complete 945-vertex compatibility graph for weight-four words in the dual of the fixed binary `[36,6,16]` parent code has exact maximum clique size

\[
\boxed{57}.
\]

The stronger preceding verifier proves this globally for all doubly-even self-orthogonal extensions containing that parent. The selected maximum code is

\[
D=[36,17,4]
\]

with coordinate stabilizer order 192 and hence parent-group orbit size

\[
\frac{51840}{192}=270.
\]

A complete 57-clique orbit-census program is now present at `analysis/w33_pass3981_max_code_orbit_census.py`. The global extremality theorem is promoted; uniqueness of the maximum-code orbit is not promoted until that exhaustive census finishes and equals 270.

## 3982 — ordering-independent adjacent-factor lower bound 229

Let

\[
K=2A_{36}-J,
\qquad K^2=36I,
\]

be the symmetric 36-port Hadamard transfer matrix. For any ordering and every prefix cut of size `k`, write

\[
K=\begin{pmatrix}A_k&B_k\\B_k^T&D_k\end{pmatrix}.
\]

Then

\[
\boxed{B_kB_k^T=36I-A_k^2.}
\]

Consequently, the cross-cut rank defect is exactly the multiplicity of the eigenvalues `+6` and `-6` of `A_k`. Since

\[
\operatorname{tr}A_k=-k,
\qquad
\operatorname{tr}A_k^2=k^2,
\]

Cauchy–Schwarz bounds the possible defect for every `k`, independently of the port order. The resulting half-sequence is

\[
1,2,3,4,5,5,6,7,7,8,8,8,9,9,9,9,10,9,
\]

and reflection symmetry gives the universal factor bound

\[
\boxed{N_{\rm adjacent}\ge229.}
\]

This raises the previous ordering-independent lower bound from 35 to 229. The published order has cut-rank sum 253. A deterministic exact ordering search found an order with sum

\[
\boxed{251},
\]

so the present rigorous interval is

\[
\boxed{229\le N_{\rm adjacent}^{\rm global}\le398}
\]

for the known exact circuit, while 251 is a stronger order-specific cut-rank target rather than an implemented factorization.

## 3983 — literal rank-48 tensor retained and central Fourier front materialized

The stronger Passes 3973–3980 certificate already reconstructs the five-fiber carrier

\[
1\mid27\mid36\mid40\mid160,
\]

all 48 orbital relations, and all

\[
\boxed{904}
\]

nonzero intersection constants. The literal tensor digest is

```text
a17a375552c102d281e3ba79b602b67aa54a426fd68b1878293763ea65395ff9
```

and its split rational algebra is

\[
\mathbb Q^2\oplus M_2(\mathbb Q)^3\oplus M_3(\mathbb Q)\oplus M_5(\mathbb Q).
\]

The new source `analysis/w33_pass3983_orbital_central_fourier.py` computes the seven-dimensional center directly in the literal orbital basis, constructs a separating central element, and extracts seven rational primitive central idempotents and the `7 x 48` irreducible character table. Those derived Fourier artifacts remain fail-closed until their exact output is frozen; the complete 48-relation multiplication tensor itself is already exact.

## 3984 — nuisance-complete one-photon falsifier

The experimental null model is not merely “arrival time does not change.” It is the identifiable regression

\[
t=a(M,e,d)+bL+\gamma\frac{L}{c}\log M+
\beta_k x_k+\beta_\nu x_\nu+\cdots,
\]

where `M` is mode count, `e` is encoder realization, `d` is detector channel, and the nuisance columns include measured transverse momentum, spectrum, pulse width, intensity, detector walk, and drift.

The frozen design has:

\[
48\text{ randomized cells},\qquad16\text{ parameters},\qquad
\boxed{\operatorname{rank}=16}.
\]

For the declared synthetic benchmark—three path lengths, two encoders, two detectors, 20-ps event jitter, and one million events per cell—the nuisance-projected uncertainty is

\[
\sigma_\gamma\approx2.19\times10^{-9}.
\]

A five-sigma test at `|gamma|=10^-9` requires about

\[
1.2043\times10^8
\]

events per cell under that idealized noise model. More importantly, deliberately omitting measured spatial and spectral covariates creates a false estimate

\[
\widehat\gamma\approx1.1243\times10^{-9},
\]

whereas the complete noiseless model returns approximately zero. This explicitly demonstrates why transverse-structure delay or spectral walk can imitate a node-count speed law.

Capacity remains a separate observable. For the declared symmetric decoding model, the 40-mode point retains about

\[
5.1533\text{ bits/use}
\]

against the ideal `log2(40)=5.3219` bits/use.

## 3985 — Monster acquisition gate strengthened, embedding still fail-closed

The strict existing gate still requires four portable serialized `MM` words and checks generator, pair-product, triple-subgroup, closure-order, and complete element-order signatures.

This packet adds two upstream executable gates:

1. a GAP/CTblLib sieve of all admissible class fusions
   \[
   U_4(2)\longrightarrow\mathbb M,
   \]
   together with decomposition of the restricted Monster `196883` character;
2. an `mmgroup` engine and canonical-integer round-trip test.

This is a real narrowing of the acquisition problem, but it does not manufacture the missing words. The promoted status remains

```text
PENDING_EXPLICIT_MM_WORDS_AND_CLASS_FUSION_EXECUTION
```

until a concrete four-word candidate passes the full object-action firewall.

Recent primary work demonstrates that reproducible explicit `mmgroup` generators can be constructed for Monster maximal subgroups, but it does not provide the required `U4(2)` candidate for this repository. The relevant source is Dietrich–Lee–Pisani–Popiel, *Journal of Algebra* 689 (2026), 862–895.

# Three chained photon constructions

## 3986 — W33 spectral metrology

For the W33 Laplacian

\[
L=12I-A,
\]

the exact spectrum is

\[
0^1,\qquad10^{24},\qquad16^{15}.
\]

A localized mode has

\[
\langle L\rangle=12,
\qquad
\operatorname{Var}(L)=12,
\]

so its ideal pure-state quantum Fisher information for the coupling-time parameter is

\[
\boxed{F_Q=48}.
\]

The optimal superposition of the extremal spectral sectors has

\[
\boxed{F_Q=16^2=256}.
\]

For `m` independent copies, localized product probes give `48m`, while an ideal spectral cat gives `256m^2`. These are exact ideal-generator figures, not achieved laboratory sensitivities.

## 3987 — dual-geometry echo

Let

\[
B=J-I-A
\]

be the complement adjacency. On the three W33 spectral sectors,

\[
A:(12,2,-4),
\qquad
B:(27,-3,3).
\]

Therefore

\[
A+B:(39,-1,-1),
\]

which is geometry-blind on the entire 39-dimensional nonuniform sector, while

\[
A-B:(-15,5,-7)
\]

resolves the two protected nontrivial sectors. The sum arm is an exact common-mode control; the difference arm is the geometry-sensitive signal. The full ideal spectral-range QFI of the difference generator is

\[
\boxed{20^2=400},
\]

and the protected nonuniform-sector value is

\[
\boxed{12^2=144}.
\]

## 3988 — one analog flight implements a global 40-mode reflection

At half the exact W33 Laplacian period,

\[
U=e^{-i\pi L/2}=I-2E_{10}.
\]

Using the strongly regular projectors gives the rational closed form

\[
\boxed{
U=-\frac13(I+A)+\frac{2}{15}J.
}
\]

Thus every row has exactly two amplitudes:

\[
-\frac15
\quad\text{on the point and its 12 neighbors},
\]

and

\[
\frac{2}{15}
\quad\text{on its 27 nonneighbors}.
\]

The matrix is a real symmetric involution:

\[
\boxed{U^2=I.}
\]

This is a major conceptual clarification for the photon processor. One engineered continuous-time evolution can perform a global 40-mode operation in parallel; it need not represent forty sequential orthogonal state changes inside one optical period.

For a genuine `m`-fold tensor carrier, rows of `U^{\otimes m}` collapse into only `m+1` amplitude shells. If `r` coordinates are in the nonneighbor class, then

\[
\operatorname{mult}(m,r)=\binom mr13^{m-r}27^r,
\]

\[
\operatorname{amp}(m,r)=
\left(-\frac15\right)^{m-r}
\left(\frac{2}{15}\right)^r.
\]

Self-similarity therefore compresses the exact analog kernel description from `40^m` entries to `m+1` shell types. It compresses control description—not Hilbert-space dimension, not energy cost, and not vacuum light speed.

Programmable electro-optic waveguide arrays have already demonstrated tunable high-dimensional Hamiltonians and 11-dimensional single-photon control, making an engineered graph-Hamiltonian interpretation substantially more conservative than a hidden-node variable-`c` ontology. The current W33 formula is an exact target transfer matrix, not a fabricated device or measured result.

## Evidence boundary

### Exact and promoted

- fixed-parent global `A4=57` extremality from the reconciled Passes 3973–3980 verifier;
- literal 48-relation, 904-constant orbital tensor;
- universal adjacent-factor lower bound 229;
- exact cut-rank sums 253 and 251 for two explicit orders;
- full-rank nuisance design and its noiseless omitted-variable demonstration;
- W33 QFI identities, dual-geometry spectra, exact rational reflection, and tensor-shell law.

### Executable but not promoted beyond the gate

- complete maximum-code orbit census;
- orbital-basis primitive central idempotents and character table;
- GAP/CTblLib Monster fusion output and `mmgroup` engine certificate.

### Open

- uniqueness of the maximum-code orbit;
- global adjacent-circuit optimum or a physical circuit attaining cut sum 251;
- laboratory photon timing, capacity, Hamiltonian, or QFI measurements;
- literal hidden photon nodes or mode-dependent vacuum `c`;
- explicit Monster `U4(2)` words and executed class fusion;
- remote CI/PDF success unless separately observed.
