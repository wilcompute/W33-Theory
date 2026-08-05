# Passes 3549–3555 — Borel orbit models, the complete Perkel table, octad curvature, and exact quantum walks

## Status

The exact standard-library verifier reports

```text
PASS_7_FRONTS 251725b948b166f475cf0a44b9d6662280c2dd7a7e12c47fb5ece3d110cc1f6b
```

The focused local regression reports

```text
5 passed
```

This packet executes the five continuations from Passes 3542–3548 and two additional high-risk constructions. It does not claim a degree-57 Moore graph, a Borel-model SAT/UNSAT verdict, or a completed 3,720-instance proof archive.

---

## 3549 — all 24 Borel signatures become exact orbit models

Assume

\[
B=C_{19}\rtimes C_9
\]

acts on a hypothetical

\[
\Gamma=\operatorname{SRG}(3250,57,0,1).
\]

Passes 3537 and 3542 left two vertex-orbit profiles, two displacement levels, and the internal-degree signatures

\[
a+2b=3
\]

or

\[
a+2b=18.
\]

Here \(a\) counts regular Borel orbits with internal \(C_{19}\)-degree two and \(b\) counts those with internal degree four. The low equation gives two solutions and the high equation gives ten. Crossing those twelve signatures with \(P_{19}\) and \(P_{57}\) produces exactly 24 models.

### Burnside variable counts

The element census of \(B\) is

\[
1^1,\qquad 3^{38},\qquad 9^{114},\qquad 19^{18}.
\]

For an odd-order action, a nonidentity element fixes an unordered pair only when it fixes both vertices. Burnside therefore gives

\[
N_2=
\frac{\binom{3250}{2}
+38\binom{f_3}{2}
+114\binom{f_9}{2}}{171}.
\]

For \(P_{19}\), \(f_3=f_9=10\), hence

\[
\boxed{N_2(P_{19})=30{,}915}.
\]

For \(P_{57}\), \(f_3=10\) and \(f_9=1\), hence

\[
\boxed{N_2(P_{57})=30{,}885}.
\]

These are the exact counts of binary edge-orbit variables in a fully \(B\)-invariant graph model.

The corresponding ordered-pair orbital counts are

\[
\boxed{61{,}858\text{ for }P_{19}},
\qquad
\boxed{61{,}792\text{ for }P_{57}}.
\]

### Lazy exact SRG equations

For each ordered-pair orbital representative \((u,v)\), the model imposes

\[
\sum_w e_{uw}e_{vw}
=
\begin{cases}
0,&e_{uv}=1,\\
1,&e_{uv}=0.
\end{cases}
\]

The products are linearized only when a violated relation is activated. This avoids materializing every triple variable at model construction while retaining an exact complete separator.

The companion source

```text
analysis/bt3549_borel_signature_models.py
```

emits all 24 contracts or one named signature.

**Boundary:** these are complete finite \(B\)-invariant model surfaces, not solver verdicts.

---

## 3550 — the complete 21-dimensional Perkel multiplication table

The explicit \(19{:}9\) action on the Perkel graph has 21 orbitals on ordered vertex pairs:

\[
3\text{ orbitals of size }57,
\qquad
18\text{ orbitals of size }171.
\]

Their valencies are correspondingly

\[
1^3,\qquad 3^{18}.
\]

Let \(R_0,\ldots,R_{20}\) be the canonical orbital matrices. Every product has an exact integral expansion

\[
R_iR_j=\sum_k p_{ij}^kR_k.
\]

The complete table has

\[
\boxed{1{,}035}
\]

nonzero structure constants, with

\[
\max p_{ij}^k=3.
\]

Its deterministic sparse-table digest is

```text
a0450717255bd9c7f149e42608450f40a1025d034a429302c49b5d54c5a7d8a9
```

Exactly 93 of the \(21^2=441\) ordered basis pairs commute.

Solving the commutator equations inside the orbital basis gives

\[
\boxed{\dim Z(\mathcal A)=5},
\]

consistent with

\[
\mathcal A
\cong
\mathbb Q
\oplus M_3\!\left(\mathbb Q(\sqrt{-19})\right)
\oplus\mathbb Q(\sqrt{-3}).
\]

This upgrades the prior Wedderburn dimension statement to a literal multiplication table suitable for exact module, code, positivity, and automorphism calculations.

---

## 3551 — the generalized pentad search reaches \(K_8\)

The factorization-field compiler requires \(n\) one-factorizations of \(K_n\), every pair sharing exactly one perfect matching.

The exact small-order census is

\[
\begin{array}{c|c|c|c}
n & \text{perfect matchings} & \text{labelled one-factorizations} & n\text{-family}\\
\hline
4&3&1&\text{no}\\
6&15&6&\text{yes}\\
8&105&6240&\text{yes}.
\end{array}
\]

At \(n=6\), all six one-factorizations form the pentad system and compile to Hoffman–Singleton.

At \(n=8\), an exact eight-object family was found. Every pair shares exactly one factor. Its canonical digest is

```text
13d7544032009f7873be3c7533a9e024251f6649a96b351228f64b90e06b280b
```

and its setwise stabilizer inside \(S_8\) is trivial:

\[
\boxed{|\operatorname{Stab}_{S_8}(\mathcal F)|=1}.
\]

Thus pairwise unique intersection is not a peculiarity of outer \(S_6\); it survives one stage higher.

The curvature does not.

Among the 56 triangle holonomies:

\[
34\text{ are derangements},
\]

while the remaining fixed-point census is

\[
1^4,\qquad2^8,\qquad4^{10}.
\]

Among the 210 simple four-row holonomies:

\[
163\text{ are derangements},
\]

while the remaining fixed-point census is

\[
1^2,\qquad2^{28},\qquad4^9,\qquad8^8.
\]

This is the first exact intermediate-order control for the proposed \(K_{56}\) factorization field.

---

## 3552 — the complete proof archive receives a 64-shard Merkle contract

The proof-DAG language from Pass 3544 already produces independently checkable upper bounds. This pass adds the complete archive protocol.

The 3,720 star-complement instances are partitioned into 64 deterministic shards:

\[
8\text{ shards of }59,
\qquad
56\text{ shards of }58.
\]

Every record binds

- the candidate index and candidate census digest;
- the compatibility-graph digest;
- the exact maximum clique;
- the lower-bound witness;
- the upper-bound proof DAG;
- the independent checker digest.

The aggregator refuses:

- missing or duplicated candidate indices;
- wrong shard ranges;
- candidate-digest drift;
- failed proof checks;
- histogram drift;
- record reordering.

An ordered Merkle root binds all 3,720 final record digests. The synthetic 3,720-leaf self-test root is

```text
1d749e0bde53c832ebb473afda9d8b87fc1973149f379bc7d95c97901021dda8
```

The companion source

```text
analysis/bt3552_clique_proof_archive.py
```

runs one shard or aggregates all 64.

**Boundary:** the protocol and executable archive surface are complete. The full proof payload remains a separately gated heavy workflow artifact.

---

## 3553 — exact quantum-walk and scattering compilers

For W33 and Gewirtz, the restricted adjacency eigenvalues are \(2\) and \(-4\). Therefore

\[
U(t)=e^{-itA}
=
e^{-ikt}P+e^{-2it}E_2+e^{4it}E_{-4}.
\]

Because both graphs are strongly regular, every matrix entry depends only on whether the two vertices are equal, adjacent, or nonadjacent.

### W33

For \(v=40,k=12\),

\[
U_{xx}(t)
=
\frac1{40}e^{-12it}
+\frac35e^{-2it}
+\frac38e^{4it},
\]

\[
U_{xy}(t)
=
\frac1{40}e^{-12it}
+\frac1{10}e^{-2it}
-\frac18e^{4it}
\quad(x\sim y),
\]

and

\[
U_{xy}(t)
=
\frac1{40}e^{-12it}
-\frac1{15}e^{-2it}
+\frac1{24}e^{4it}
\quad(x\nsim y).
\]

Consequently,

\[
|U_{xy}(t)|\le\frac14
\quad(x\sim y),
\qquad
|U_{xy}(t)|\le\frac{2}{15}
\quad(x\nsim y).
\]

Perfect state transfer between distinct W33 vertices is therefore impossible.

The infinite-time average probabilities are

\[
\overline p_{\rm diag}=\frac{401}{800},
\qquad
\overline p_{\rm adj}=\frac{21}{800},
\qquad
\overline p_{\rm non}=\frac{49}{7200}.
\]

### Gewirtz

For \(v=56,k=10\),

\[
|U_{xy}(t)|\le\frac27
\quad(x\sim y),
\qquad
|U_{xy}(t)|\le\frac1{12}
\quad(x\nsim y),
\]

again excluding perfect state transfer.

The infinite-time average probabilities are

\[
\overline p_{\rm diag}=\frac{813}{1568},
\qquad
\overline p_{\rm adj}=\frac{57}{1568},
\qquad
\overline p_{\rm non}=\frac{37}{14112}.
\]

### Nonbacktracking poles

The exact nonbacktracking channels are obtained from

\[
z^2-\theta z+(k-1)=0.
\]

For W33 they are

\[
11,\ 1,\quad
1\pm i\sqrt{10},\quad
-2\pm i\sqrt7,
\]

together with the extra \(\pm1\) sector of multiplicity 200.

For Gewirtz they are

\[
9,\ 1,\quad
1\pm2i\sqrt2,\quad
-2\pm i\sqrt5,
\]

together with the extra \(\pm1\) sector of multiplicity 224.

This converts the typed analytic port from Pass 3546 into exact transition-amplitude and scattering data.

---

## 3554 BONKERS — the 21 Borel channels collapse to 11 observables plus 10 phases

Transpose permutes the 21 Perkel orbital matrices.

Only the identity orbital is individually self-transpose. The other twenty form ten transpose pairs. Therefore

\[
\boxed{\dim\mathcal A^{+}=11},
\qquad
\boxed{\dim\mathcal A^{-}=10},
\]

where \(\mathcal A^{+}\) is the symmetric part and \(\mathcal A^{-}\) is the skew part.

Under

\[
\mathcal A
\cong
\mathbb Q
\oplus M_3\!\left(\mathbb Q(\sqrt{-19})\right)
\oplus\mathbb Q(\sqrt{-3}),
\]

this becomes

\[
\mathcal A^{+}
\cong
\mathbb R
\oplus\operatorname{Herm}_3(\mathbb C)
\oplus\mathbb R
\]

after the imaginary-quadratic embeddings.

The dimensions are

\[
1+9+1=11.
\]

Thus every real symmetric \(19{:}9\)-equivariant kernel—Gram matrix, covariance, Hamiltonian, or positive semidefinite witness—lives in an eleven-parameter observable sector. The ten skew channels carry the complementary oriented phase data.

This is an exact algebraic compression, not a physical gauge-field identification.

---

## 3555 BONKERS — the octad compiles to an 82-vertex near-Moore falsifier

Feeding the \(K_8\) family into the factorization-field compiler gives a graph with

\[
82\text{ vertices},
\qquad
369\text{ edges},
\qquad
\deg=9.
\]

Its exact edge digest is

```text
3e35e4e9d151eef83a1b0c53aed5169c0a2756bf4aa9363f9cd5c336ee2880d3
```

The graph has

\[
\boxed{\operatorname{diameter}=3},
\qquad
\boxed{60\text{ triangles}},
\qquad
\boxed{422\text{ four-cycles}}.
\]

For adjacent pairs, the common-neighbor census is

\[
0^{217},\qquad1^{124},\qquad2^{28}.
\]

For nonadjacent pairs it is

\[
0^{828},\qquad1^{1644},\qquad2^{312},\qquad3^{168}.
\]

The 828 nonadjacent pairs with no common neighbor are exactly the unordered distance-three pairs.

This is a sharp control experiment:

\[
\boxed{\text{pairwise factor intersection is the static design layer; holonomy is the Moore curvature layer}.}
\]

The \(n=8\) construction satisfies the former and fails the latter in a completely quantified way.

---

## Reproduction

```bash
python analysis/bt3549_3555_borel_pentad_quantum_walk.py
pytest -q tests/test_bt3549_bt3555_borel_pentad_quantum_walk.py
python analysis/bt3549_borel_signature_models.py
python analysis/bt3552_clique_proof_archive.py --self-test
```

One proof shard is generated with

```bash
python analysis/bt3552_clique_proof_archive.py \
  --shard 0 \
  --json evidence/pass3549_3555/proof_shard_00.json
```

## Claim boundaries

- M57 remains open.
- None of the 24 Borel orbit models has a SAT/UNSAT verdict here.
- The full 3,720 proof payload is not promoted before its heavy workflow finishes.
- The \(K_8\) graph is an exact falsifier/control, not a Moore graph.
- Quantum-walk and scattering formulas are graph dynamics, not measured optical hardware.
- No laboratory, particle, spacetime, energy, or successful-PDF claim follows from source publication.
