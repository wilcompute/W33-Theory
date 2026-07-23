# Passes 631–635 — modular Ext, Montes stage zero, minimal Hecke fibre, correlated optics, and joint inference

## Pass 631 — Modular Ext fingerprint and local endomorphism algebra

The characteristic-two top homology module has dimension 125 and is indecomposable. Its full equivariant endomorphism algebra is

\[
\operatorname{End}_{\mathbb F_2[S_8]}(H_2)
\cong \mathbb F_2\oplus J,
\qquad \dim J=2,
\qquad J^2=0.
\]

The only idempotents have ranks 0 and 125. The three nonzero radical maps have ranks

\[
20,34,34.
\]

The two rank-34 maps have the same canonical image, the wing \(\operatorname{im}T\). Their sum has rank 20 and lands exactly on the distinguished 20-dimensional submodule inside that wing.

The modular composition chains are refined to

\[
U_{34}:D_{14}\mid D_6\mid D_8\mid D_6,
\]

and

\[
C_{55}:D_{40}\mid D_1\mid D_{14}.
\]

Consequently the 125-dimensional module has composition multiplicities

\[
D_1^3\oplus D_6^4\oplus D_8^2\oplus D_{14}^3\oplus D_{40}.
\]

Every displayed factor is absolutely irreducible by the full matrix-algebra criterion. This is the complete mod-two endomorphism and extension fingerprint, but not yet a lifted \(\mathbb Z_2[S_8]\) Ext-class certificate.

## Pass 632 — Exact Stage-0 Montes/Okutsu transcript atlas

All

\[
17\times5=85
\]

torsion-prime localizations now carry deterministic transcripts combining:

- complete factorization of the defining polynomial modulo \(p\);
- repeated-factor and derivative-gcd data;
- exact \(p\)-maximal prime-ideal \((e,f)\) profiles;
- tame/wild labels;
- discriminant and power-basis-index reconciliation;
- a SHA256 certificate per localization.

The census is:

\[
54\text{ Dedekind-clean localizations},
\quad31\text{ nonmaximal power bases},
\]

\[
29\text{ ramified localizations},
\quad11\text{ wild localizations},
\quad10\text{ index-only singularities}.
\]

Whenever the power basis is \(p\)-maximal, the modular factor multiplicities and degrees agree exactly with the prime-ideal \((e,f)\) profile. The repository script deterministically emits a Magma driver for all 85 `Montes(... : Field:=true)` calls via `--emit-magma`. Full OM representatives, slopes, residual polynomials, and local integral bases remain an external licensed-run boundary.

## Pass 633 — Unique minimal full-block Wilson fibre

Let

\[
H=\langle(01),(67)\rangle\cong C_2\times C_2.
\]

Every one-dimensional character of \(H\) already separates the four central Wilson holonomy classes, but each misses exactly two of the 22 \(S_8\) Wedderburn blocks.

The unique smallest fibre that both preserves all four class fingerprints and restores all 22 blocks is

\[
V_{\min}=\mathbf1\oplus\chi_{xy},
\]

where \(\chi_{xy}\) is odd on both endpoint transpositions. Thus

\[
\dim V_{\min}=2,
\qquad
\dim\operatorname{Ind}_H^{S_8}V_{\min}=20160,
\]

and

\[
\dim\operatorname{End}_{S_8}
\left(\operatorname{Ind}_H^{S_8}V_{\min}\right)=10128.
\]

This halves the universal regular carrier and reduces the Hecke algebra from 40,320 to 10,128 dimensions.

## Pass 634 — Correlated optical decoder

After the fixed compiler calibration, every cube-stationary rail covariance has the form

\[
\Sigma=\sum_{d=0}^{3}c_dA_d
\]

in the Hamming-distance algebra of \(Q_3\). The Walsh interferometer diagonalizes this entire four-dimensional algebra exactly. Its mode variances are the Krawtchouk transform

\[
\lambda_w=\sum_d c_dK_d(w),
\qquad w=0,1,2,3.
\]

Therefore stationary rail correlations create mode-dependent noise but no decoded-mode crosstalk. Equal physical rail offsets are annihilated by the balanced selector correlations.

A compound-Poisson afterpulse process of branching ratio \(a\) contributes Fano inflation

\[
(1-a)^{-2}.
\]

Combining this with the deterministic output radius gives certified 1% pairwise-union photon thresholds:

- tight: 123;
- laboratory: 255;
- stress: 754;
- wide: 16,119.

The two guard modes are both weight-two Walsh channels and provide a 395-sample variance-inflation sentinel for a 25% departure.

## Pass 635 — Joint optical/e-process co-design

The robust class information is optimized over the three Wilson trace channels while the class, guard, and phase-reference error budgets satisfy

\[
\alpha_c+\alpha_g+\alpha_r=0.01.
\]

Guard measurements are observed on every classification shot, so their e-process evidence accumulates with zero extra acquisition blocks. The continuous alpha allocation reduces to a one-dimensional optimization, followed by exact LP-vertex enumeration and integer certification.

For all four optical profiles the maximin classifier uses only

\[
\operatorname{Tr}(U),\qquad \operatorname{Tr}(U^2),
\]

and assigns zero discrimination samples to \(\operatorname{Tr}(U^3)\). The latter remains a held-out falsification channel.

Certified integer allocations are:

| profile | Tr(U) | Tr(U²) | Tr(U³) | reference | raw photons |
|---|---:|---:|---:|---:|---:|
| tight | 456 | 36 | 0 | 153 | 66,573 |
| laboratory | 462 | 36 | 0 | 153 | 127,143 |
| stress | 476 | 37 | 0 | 154 | 348,994 |
| wide | 507 | 40 | 0 | 155 | 7,071,771 |

The same two ordered class pairs control every optimum: fixed-point-free involution versus double transposition, and order three versus fixed-point-free involution.

## Verification and boundaries

All five scripts are deterministic, certificate-backed, and callable with `--check`. The focused regression executes all five.

Open boundaries are explicit:

- lifting the modular Ext fingerprint to a complete \(\mathbb Z_2[S_8]\) class;
- executing the licensed Montes driver for complete OM transcripts;
- realizing \(\chi_{xy}\) as a minimal physical endpoint parity fibre;
- treating arbitrary nonstationary optical covariance;
- allowing temporal nuisance dependence beyond predictable conditional intervals.
