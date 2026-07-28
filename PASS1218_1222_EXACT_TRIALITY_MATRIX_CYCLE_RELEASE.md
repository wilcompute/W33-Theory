# Passes 1218–1222 — Exact Triality, Matrix-Unit, and Cycle Release

Status: **machine-checkable exact release**

This packet executes the five non-sequential frontiers opened by Passes 1193–1197. It also audits draft PR #166: its abstract Wedderburn manifest and short-cycle boundary were useful inputs, but the branch is stale and does not contain the carrier-level intertwiners or length-seven/eight orbit classification completed here.

## Pass 1218 — The \(81_+\)/\(81_-\) physical-sector bridge

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

The two explicit maps

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

The character-table obstruction is now resolved exactly:

\[
\boxed{81_-=81_+\otimes\operatorname{sgn}}.
\]

Hence

\[
\dim\operatorname{Hom}_{W(E_6)}(81_+,81_-)=0,
\]

\[
\dim\operatorname{Hom}_{W(E_6)}(81_+\otimes\operatorname{sgn},81_-)=1,
\]

while their restrictions to \(PSp(4,3)\) are the same irreducible module. The physical Levi sector therefore sees the projective Steinberg module; the \(+/-\) label is an outer-extension choice.

## Pass 1219 — Actual \(M_3\) and \(M_{21}\) matrix units

### Carrier-level \(M_3\) Steinberg block

On each 432 carrier, let \(K_{2C}\) be the class sum of the 36-element outer involution class. Its exact spectrum is

\[
36^1,\;24^{12},\;18^{60},\;12^{90},\;9^{128},\;6^{60},\;4^{81}.
\]

Therefore the integer numerator

\[
N=(K-36I)(K-24I)(K-18I)(K-12I)(K-9I)(K-6I)
\]

satisfies

\[
N^2=716800N,
\qquad
\operatorname{rank}(N)=81.
\]

Let \(\tau\) be the central \(A_2\) Coxeter element cycling the three 432 carriers. The nine factorized operators

\[
\boxed{E_{ij}=\frac1{716800}\,\tau_{j\to i}N_j}
\]

satisfy

\[
E_{ij}E_{k\ell}=\delta_{jk}E_{i\ell}.
\]

This is a carrier-coordinate realization of the full Steinberg multiplicity algebra \(M_3(\mathbb Q)\), not merely an abstract block count.

### Orbit-anchored \(M_{21}\) residual block

The exact multiplicity of the 20-dimensional constituent on the fourteen \(A_2\)-triple orbits is

\[
0,0,1,1,1,1,1,1,1,3,3,3,3,3,
\]

whose sum is 22. The explicit cubic incidence matrix has column distribution

\[
0^{2000},\qquad6^{240},
\]

and its 240 live columns are exactly orbit 8. Thus the unique 20-copy on the size-240 carrier is the cubic image copy; deleting it leaves the geometrically anchored 21-copy kernel block

\[
6\cdot 20\;\text{from the six 27-carriers},
\quad
6\cdot20\;\text{from the two 270-carriers},
\quad
9\cdot20\;\text{from the three 432-carriers}.
\]

The verifier constructs and hashes all \(21^2=441\) sparse multiplicity-space units and verifies their multiplication law exhaustively; the checked-in certificate stores the digest and boundary samples. The orbit blocks are canonical; copy coordinates inside multiplicity-three orbit blocks remain an explicit Wedderburn gauge.

## Pass 1220 — Equality of the two degree-432 Hecke algebras

Let

\[
G=W(E_6),\quad N=PSp(4,3),\quad H=S_5,\quad K=A_5=H\cap N.
\]

The carrier has the two coset descriptions

\[
G/H\cong N/K.
\]

The stronger result is that \(H\) and \(K\) have **exactly the same orbit partition** on all 432 points. Both subdegree lists are

\[
1,1,5^6,10^4,20^9,30^4,60.
\]

Consequently

\[
\boxed{
\operatorname{End}_{W(E_6)}\mathbb Q[G/S_5]
=
\operatorname{End}_{PSp(4,3)}\mathbb Q[N/A_5]
}
\]

as the same 26-dimensional orbital algebra, with identical relation matrices and identical structure constants. It remains noncommutative; one explicit witness is

\[
p_{1,2}^{3}=0,
\qquad
p_{2,1}^{3}=1.
\]

## Pass 1221 — Literal primitive cycle orbits at lengths seven and eight

The direct enumeration is replaced by a rooted-edge slice. Every group orbit intersects the slice of primitive cycles rooted at one canonical directed edge. The slice is quotiented by the directed-edge stabilizer and by transporter-normalized cyclic rerooting. Orbit sizes then follow exactly from

\[
|\mathcal O|=\frac{480}{n}\,|\mathcal O\cap\text{rooted slice}|.
\]

### Length seven

\[
\pi_7=2,739,840.
\]

Under \(PSp(4,3)\):

\[
108\text{ orbits},
\quad
960^1,\;8640^2,\;25920^{105}.
\]

Under \(W(E_6)\):

\[
57\text{ orbits},
\quad
960^1,\;17280^1,\;25920^5,\;51840^{50}.
\]

Six projective orbits remain fixed under the outer extension and 51 pairs fuse.

### Length eight

\[
\pi_8=26,750,160.
\]

Under \(PSp(4,3)\):

\[
1066\text{ orbits}
\]

with sizes

\[
240^1,\;480^1,\;6480^{10},\;8640^3,\;12960^{45},\;25920^{1006}.
\]

Under \(W(E_6)\):

\[
565\text{ orbits}
\]

with sizes

\[
240^1,\;480^1,\;6480^4,\;8640^1,\;12960^{14},
\;17280^1,\;25920^{63},\;51840^{480}.
\]

Sixty-four projective orbits remain fixed and 501 pairs fuse. The complete deterministic `--full-output` stream stores a representative, orbit size, stabilizer order, simplicity flag, vertex-multiplicity partition, and the projective-to-Weyl fusion map for every orbit. The compact checked-in certificate stores all distributions, record counts, boundary samples, and the SHA-256 of that stream.

## Pass 1222 — The normalizer triality verdict

Reflections in two roots of the fixed \(A_2\) commute with all \(W(E_6)\) generators and generate

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

matching the 1120 unoriented \(A_2\) subsystems.

The requested torsor test has a precise correction:

- the three 432 carriers carry the full transitive \(S_3\) triality action, but each color has stabilizer order 2, so they are \(S_3/S_2\), **not** an \(S_3\) torsor;
- the orientation-preserving \(C_3\) subgroup is free and transitive on the three 432 colors;
- the six 27-carriers carry a regular, free, transitive \(S_3\) action and are the genuine signed \(S_3\) torsor.

## Verification

```bash
PYTHONPATH=analysis python analysis/w33_pass1218_81_sign_twist_intertwiner.py
PYTHONPATH=analysis python analysis/w33_pass1219_m3_m21_matrix_units.py
PYTHONPATH=analysis python analysis/w33_pass1220_a5_s5_hecke_equality.py
PYTHONPATH=analysis python analysis/w33_pass1221_literal_cycle_orbits_7_8.py
PYTHONPATH=analysis python analysis/w33_pass1222_a2_normalizer_triality.py
pytest -q tests/test_w33_pass1218_1222.py
```

The release distinguishes exact carrier-coordinate statements, gauge-fixed multiplicity coordinates, and abstract representation equivalences. No physical implementation claim follows solely from these finite-module identities.
