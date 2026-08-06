# Passes 3973–3980 — extremal-code geometry, exact mesh neighborhood, photon experiment, rank-48 tensor, and three constructions

## Exact status

```text
PASS_EXACT_57_GEOMETRY_MESH_RADIUS1_TENSOR_EXPERIMENT_MODEL_MONSTER_FAIL_CLOSED
769f2f1b29e832050fbf148f38ab64acd992766d5dc758a525b3f97e6e77d44e
```

This packet continues the exact Passes 3957–3972 frontier without changing their physical firewall. It treats the user's photon idea as a family of competing, falsifiable resource models rather than assuming that an internal node count changes the invariant vacuum front velocity.

## Pass 3973 — the 57-code support geometry is exactly \(T(10)\sqcup T(4)\sqcup T(4)\)

The deterministic 57-word extension of the fixed binary \([36,6,16]\) character code again produces the maximal doubly-even code

\[
D=[36,17,4]
\]

with weight enumerator

\[
1+57z^4+852z^8+7332z^{12}+57294z^{16}
+57294z^{20}+7332z^{24}+852z^{28}+57z^{32}+z^{36}.
\]

Join two weight-four words when their supports intersect in two coordinates. The component census is

\[
57=45+6+6.
\]

The 45-vertex component has ten maximal cliques of size nine. Every vertex belongs to exactly two such cliques, every unordered pair of clique labels occurs exactly once, and two vertices are adjacent exactly when their two-label pairs intersect. Therefore

\[
\boxed{G_{45}\cong T(10)=L(K_{10}).}
\]

Each six-vertex component is the octahedral graph: its complement is three disjoint edges, equivalently

\[
\boxed{G_6\cong T(4)=L(K_4).}
\]

Hence the exact support decomposition is

\[
\boxed{57=\binom{10}{2}+2\binom{4}{2}.}
\]

### Enumerator rigidity and the extremality boundary

For every maximal doubly-even \([36,17]\) extension of the fixed \([36,6,16]\) code whose dual has minimum distance at least four, put \(t=A_4\). MacWilliams symmetry forces

\[
A_8=11t+225,\qquad A_{12}=9555-39t,\qquad A_{16}=55755+27t,
\]

with the reflected coefficients at weights 20, 24, 28 and 32. The dual coefficients include

\[
B_4=t,\quad B_6=6(t+7),\quad B_8=11t+225,
\]

\[
B_{10}=12(5t+483),\quad B_{12}=39(245-t),
\]

\[
B_{14}=6(14505-49t),\quad B_{16}=27(t+2065),\quad B_{18}=456(t+455).
\]

Nonnegativity alone gives only

\[
\boxed{t\le245.}
\]

Thus \(t=57\) is an exact and highly structured stratum, but this packet does **not** claim global \(A_4\)-extremality.

## Pass 3974 — exact radius-one local optimum of the 36-port mesh

The established exact adjacent-mode factorization uses

\[
398\text{ nontrivial rotations},\qquad 232\text{ exact zero eliminations},\qquad69\text{ layers}.
\]

Every one of the

\[
\binom{36}{2}=630
\]

single transpositions of the port order was replayed in the exact multiquadratic arithmetic used by Pass 3958. The minimum remains 398 rotations; no transposition improves it. Exactly 22 transpositions tie the base count, and every candidate has depth 69. The complete audit digest is

```text
d0e4b57c47e8db57def844d9d9da63b3e7cda0652b05473fcebc5884fbd8d80f
```

Therefore the current ordering is an exact radius-one local optimum in full permutation space. This is not a proof of global rotation or depth optimality.

## Pass 3975 — a slope/intercept one-photon falsifier

The physically safe null hypothesis is

\[
t(M,L)=a(M)+\frac{L}{c},
\]

where \(M\) is the encoded orthogonal-mode alphabet, \(a(M)\) absorbs encoder, decoder, detector, and pulse-shape latency, and the propagation slope is independent of \(M\).

The proposed experiment uses a heralded 1550-nm photon with a fixed spectral envelope and randomly interleaves unitary alphabets

\[
M\in\{2,4,8,16,40\}.
\]

At two or more free-space lengths, fit

\[
t(M,L)=a(M)+b(M)L.
\]

A mode-dependent intercept is ordinary device latency. A reproducible mode-dependent slope, surviving encoder swaps, spectral-envelope matching, and length scaling, would falsify the invariant-front null. Capacity is measured separately through the full decoding confusion matrix and mutual information.

For a symmetric \(M\)-ary channel with total error probability \(\epsilon\),

\[
I(M,\epsilon)=\log_2 M+(1-\epsilon)\log_2(1-\epsilon)
+\epsilon\log_2\!\left(\frac{\epsilon}{M-1}\right).
\]

At \(M=40\), the ideal direct-sum capacity is \(\log_2 40\approx5.32193\) bits per use; it is about 5.18828 bits at one-percent symmetric error and 4.77126 bits at five-percent error.

An illustrative statistics-only calculation for a 10-km baseline, 50-ps single-event timing jitter, one million events per setting, and a five-sigma test of

\[
c_{\rm eff}(M)=c(M/2)^\gamma
\]

gives \(|\gamma|\sim2.50\times10^{-9}\). This is not a projected experimental bound: clock drift, mode-dependent optical path, detector walk, atmospheric delay, and pulse reshaping will dominate unless the slope/intercept design is enforced.

## Pass 3976 — complete rank-48 multiplication tensor in Wedderburn coordinates

The characteristic-zero centralizer algebra is

\[
\boxed{
\mathbb Q^2\oplus M_2(\mathbb Q)^3\oplus M_3(\mathbb Q)\oplus M_5(\mathbb Q).
}
\]

Its block sizes are

\[
1,1,2,2,2,3,5,
\]

so its dimension is

\[
1^2+1^2+3\cdot2^2+3^2+5^2=48
\]

and its center has dimension seven. A full matrix-unit basis and all nonzero products

\[
e_{ij}^{(r)}e_{kl}^{(s)}=\delta_{rs}\delta_{jk}e_{il}^{(r)}
\]

are serialized. There are

\[
1^3+1^3+3\cdot2^3+3^3+5^3=178
\]

nonzero structure constants. This closes the multiplication tensor in split Wedderburn coordinates; converting it to the 48 geometric orbital-relation basis remains open.

## Pass 3977 — Monster execution gate remains fail-closed

The required observable artifact

```text
data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json
```

is absent. Existing abstract \(U_4(2){:}2\) fingerprints do not supply serialized `mmgroup` words and do not execute the Monster class-fusion or character-restriction calculation. Therefore

\[
\boxed{\texttt{PENDING\_EXPLICIT\_MONSTER\_WORDS\_AND\_CLASS\_FUSION}.}
\]

No Monster embedding is promoted.

## Pass 3978 — the photon-capacity trilemma

Three resource models must not be conflated.

1. **Direct sum:** one photon over \(M\) orthogonal alternatives has ideal classical capacity at most \(\log_2 M\) bits per use.
2. **Tensor product:** \(N\log_2 d\) bits require \(N\) physically independent \(d\)-state factors, not merely \(N\) named internal nodes.
3. **Serial dynamics:** mutually orthogonal state changes are constrained by energy and elapsed time; they are not free labels.

This is the strongest defensible version of “the photon is the computer”: the photon can carry and coherently transform a high-dimensional mode alphabet, while the number of sequential orthogonal operations remains a separate dynamical resource.

## Pass 3979 — the time-bandwidth packing law

For a temporal/frequency encoding concentrated to half-bandwidth \(W\) and duration \(T\), the prolate-spheroidal Shannon number gives the engineering estimate

\[
M\sim2WT.
\]

At \(W=20\,\mathrm{GHz}\), approximately 40, 81, and 729 concentrated temporal modes require durations of about 1.0 ns, 2.025 ns, and 18.225 ns, corresponding to vacuum lengths of about 0.300 m, 0.607 m, and 5.464 m. A larger alphabet can therefore demand a larger spacetime support even while the front remains at \(c\).

## Pass 3980 — self-similar address-density invariant

For the Cartesian power \(W(3,3)^{\square m}\),

\[
|V|=40^m,\qquad \operatorname{diam}=2m.
\]

The ideal direct-sum address capacity is \(m\log_2 40\), so

\[
\boxed{
\frac{\log_2|V|}{\operatorname{diam}}=\frac{\log_2 40}{2}\approx2.660964
}
\]

bits per graph-diameter step. Combining the serial orthogonalization bound \(L_{\min}/\lambda\ge m/2\) with the same alphabet gives

\[
\boxed{
\frac{\log_2|V|}{L_{\min}/\lambda}\le2\log_2 40\approx10.643856.
}
\]

Self-similarity preserves an address-density law. It does not alter vacuum \(c\).

## Evidence boundary

### Exact here

- reconstruction of the 57-word code and explicit \(T(10)\sqcup2T(4)\) support geometry;
- one-parameter MacWilliams enumerator rigidity;
- all-630 exact transposition audit of the 36-port ordering;
- the 48-dimensional matrix-unit multiplication tensor;
- algebraic capacity, timing, and self-similarity formulas.

### Modeled here

- symmetric-channel information values;
- illustrative timing sensitivity;
- the Slepian Shannon-number engineering estimate.

### Still open

- global \(A_4\)-extremality;
- global mesh optimum;
- a performed one-photon experiment;
- the geometric orbital-basis rank-48 tensor;
- Monster words and class fusion;
- any variable-vacuum-\(c\) ontology;
- hardware or laboratory validation.

## Primary external references used for the physical firewall

- N. Margolus and L. B. Levitin, “The maximum speed of dynamical evolution,” *Physica D* 120 (1998), DOI 10.1016/S0167-2789(98)00054-2.
- H. J. Landau and H. O. Pollak, “Prolate spheroidal wave functions, Fourier analysis and uncertainty—II,” *Bell System Technical Journal* 40 (1961), DOI 10.1002/j.1538-7305.1961.tb03977.x.
- D. Slepian, “Prolate spheroidal wave functions, Fourier analysis and uncertainty—III,” *Bell System Technical Journal* 41 (1962), DOI 10.1002/j.1538-7305.1962.tb03279.x.
- A. Babazadeh et al., “High-dimensional single-photon based quantum gates,” *Physical Review Letters* 119, 180510 (2017), DOI 10.1103/PhysRevLett.119.180510.
- L. Yu et al., “High-dimensional time-bin quantum key distribution over 60-km fiber,” *Nature Communications* 16, 171 (2025), DOI 10.1038/s41467-024-55345-0.
