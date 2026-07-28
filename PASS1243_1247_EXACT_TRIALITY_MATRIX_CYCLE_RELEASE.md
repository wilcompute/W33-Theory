# Passes 1243–1247 — Exact Triality, Matrix-Unit, and Cycle Release

Status: **machine-checkable exact release**

This collision-protected packet closes the five frontiers opened by Passes 1193–1197 and left partial or planned by the parallel Passes 1238–1242 synthesis track. Draft PR #166 supplied useful abstract Wedderburn and short-cycle hints, but it did not contain the carrier-level intertwiners, complete matrix-unit construction, or length-seven/eight orbit classification completed here.

The full reviewed Python source is stored transparently in nine small text chunks, verified against archive SHA-256 `d2e1e9d4e6c520f8402d831d8bfa563a14f24e8d2ec4cea0faed87f13dca44e4`, and executed in memory by `scripts/pass1243_1247_bundle_runtime.py`. Canonical wrapper paths remain ordinary executable Python files.

## Pass 1243 — The \(81_+\)/\(81_-\) physical-sector bridge

Let \(B\) be the 480-dimensional directed-edge Hashimoto operator and let \(T\colon\mathbb Q^{480}\to\mathbb Q^{160}\) fold a directed collinearity edge \((p\to q)\) to the Levi flag \((p,\ell(p,q))\). Let \(E_4=K/160\) be the rank-81 Levi cycle projector.

The exact Hashimoto projectors onto eigenvalues \(+1\) and \(-1\) are

\[
P_+=\frac{q_+(B)}{-3200},\qquad
q_+(x)=x^6-8x^5-17x^4-140x^3-253x^2-1452x-1331,
\]

\[
P_-=\frac{q_-(B)}{2688},\qquad
q_-(x)=x^6-10x^5+x^4-124x^3+11x^2-1210x+1331.
\]

The explicit maps

\[
\Phi_+=E_4TP_+,
\qquad
\Phi_-=E_4TP_-
\]

both have rank 81 over \(\mathbb F_{1000003}\), are boundaryless, and intertwine all five generators of \(PSp(4,3)\). Their exact target operators are

\[
E_4TP_+T^{\mathsf T}E_4=2E_4,
\qquad
E_4TP_-T^{\mathsf T}E_4=E_4.
\]

The extension obstruction resolves as

\[
\boxed{81_-=81_+\otimes\operatorname{sgn}}.
\]

Thus

\[
\dim\operatorname{Hom}_{W(E_6)}(81_+,81_-)=0,
\qquad
\dim\operatorname{Hom}_{W(E_6)}(81_+\otimes\operatorname{sgn},81_-)=1,
\]

while the restrictions to \(PSp(4,3)\) are the same irreducible module. The Levi sector sees the projective Steinberg module; the \(+/-\) label is an outer-extension choice.

## Pass 1244 — Actual \(M_3\) and \(M_{21}\) matrix units

On each 432 carrier, let \(K_{2C}\) be the class sum of the 36-element outer involution class. Its exact spectrum is

\[
36^1,\;24^{12},\;18^{60},\;12^{90},\;9^{128},\;6^{60},\;4^{81}.
\]

The integer numerator

\[
N=(K-36I)(K-24I)(K-18I)(K-12I)(K-9I)(K-6I)
\]

satisfies

\[
N^2=716800N,
\qquad
\operatorname{rank}(N)=81.
\]

If \(\tau\) is the central \(A_2\) Coxeter element cycling the three 432 carriers, the nine factorized operators

\[
\boxed{E_{ij}=\frac1{716800}\,\tau_{j\to i}N_j}
\]

satisfy

\[
E_{ij}E_{k\ell}=\delta_{jk}E_{i\ell}.
\]

This realizes the Steinberg multiplicity algebra \(M_3(\mathbb Q)\) in carrier coordinates.

For the species-20 residual block, the constituent multiplicities on the fourteen \(A_2\)-triple orbits are

\[
0,0,1,1,1,1,1,1,1,3,3,3,3,3,
\]

summing to 22. The cubic incidence matrix has column distribution

\[
0^{2000},\qquad6^{240},
\]

and the 240 live columns are exactly orbit 8. Removing its unique species-20 image copy leaves a geometrically anchored multiplicity-21 kernel block. The verifier constructs all \(21^2=441\) sparse units, with digest `1c733affab714f307e909bee6e4778ec8b010205e14e2431f1b058580b7663dd`, and verifies the full matrix-unit law. Orbit blocks are canonical; copy coordinates inside multiplicity-three orbit blocks remain an explicit Wedderburn gauge.

## Pass 1245 — Equality of the two degree-432 Hecke algebras

Let

\[
G=W(E_6),\quad N=PSp(4,3),\quad H=S_5,\quad K=A_5=H\cap N.
\]

The carrier has the coset descriptions

\[
G/H\cong N/K.
\]

More strongly, \(H\) and \(K\) have exactly the same orbit partition on all 432 points. Their shared subdegree list is

\[
1,1,5^6,10^4,20^9,30^4,60.
\]

Therefore

\[
\boxed{
\operatorname{End}_{W(E_6)}\mathbb Q[G/S_5]
=
\operatorname{End}_{PSp(4,3)}\mathbb Q[N/A_5]
}
\]

as the same 26-dimensional orbital algebra, with identical relation matrices and structure constants. It is noncommutative; one explicit witness is

\[
p_{1,2}^{3}=0,
\qquad
p_{2,1}^{3}=1.
\]

The exact structure-constant digest is `46f42fdb10b985e01ca523d6027886c6c2fec3f7687fa5c686c6e8b590eb53e6`.

## Pass 1246 — Literal primitive cycle orbits at lengths seven and eight

A rooted-edge slice replaces infeasible global enumeration. Every group orbit intersects the primitive-cycle slice rooted at one canonical directed edge. Quotienting by the directed-edge stabilizer and transporter-normalized cyclic rerooting gives

\[
|\mathcal O|=\frac{480}{n}\,|\mathcal O\cap\text{rooted slice}|.
\]

At length seven,

\[
\pi_7=2,739,840.
\]

The \(PSp(4,3)\) action has 108 orbits with sizes

\[
960^1,\;8640^2,\;25920^{105},
\]

while \(W(E_6)\) has 57 orbits with sizes

\[
960^1,\;17280^1,\;25920^5,\;51840^{50}.
\]

Six projective orbits remain fixed under the outer extension and 51 pairs fuse.

At length eight,

\[
\pi_8=26,750,160.
\]

The \(PSp(4,3)\) action has 1,066 orbits with sizes

\[
240^1,\;480^1,\;6480^{10},\;8640^3,\;12960^{45},\;25920^{1006},
\]

while \(W(E_6)\) has 565 orbits with sizes

\[
240^1,\;480^1,\;6480^4,\;8640^1,\;12960^{14},
\;17280^1,\;25920^{63},\;51840^{480}.
\]

Sixty-four projective orbits remain fixed and 501 pairs fuse. The deterministic full representative/fusion stream has digest `132eb1cfc8437540761b893094794f2b2986aa1c4af7669436db55c316a4b0ac`.

## Pass 1247 — The normalizer triality verdict

Reflections in two roots of the fixed \(A_2\) commute with every \(W(E_6)\) generator and generate

\[
W(A_2)\cong S_3.
\]

The direct-product subgroup has order

\[
|W(E_6)\times W(A_2)|=51840\cdot6=311040.
\]

The full \(A_2\)-subsystem normalizer has order

\[
622080,
\]

and index

\[
\frac{|W(E_8)|}{622080}=1120,
\]

matching the 1,120 unoriented \(A_2\) subsystems.

The torsor test has a precise correction:

- the three 432 carriers carry the full transitive \(S_3\) triality action, but each color has stabilizer order 2, so they form \(S_3/S_2\), not an \(S_3\) torsor;
- the orientation-preserving \(C_3\) subgroup is free and transitive on the three 432 colors;
- the six 27-carriers carry a regular, free, transitive \(S_3\) action and are the genuine signed \(S_3\) torsor.

## Verification

```bash
python scripts/pass1243_1247_bundle_runtime.py
python analysis/w33_pass1243_81_sign_twist_intertwiner.py
python analysis/w33_pass1244_m3_m21_matrix_units.py
python analysis/w33_pass1245_a5_s5_hecke_equality.py
python analysis/w33_pass1246_literal_cycle_orbits_7_8.py
python analysis/w33_pass1247_a2_normalizer_triality.py
pytest -q tests/test_w33_pass1243_1247.py
```

The release distinguishes exact carrier-coordinate statements, gauge-fixed multiplicity coordinates, and abstract representation equivalences. No physical implementation claim follows solely from these finite-module identities.
