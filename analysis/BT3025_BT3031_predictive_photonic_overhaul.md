# Passes 3025–3031 — Predictive photonic architecture and complete paper overhaul

## Executive result

This packet reconciles the source-complete work on `master`, the unmerged seven-front
packet in PR #231, and the parallel paper-overhaul track. The architectural conclusion is
stronger than any single count:

> The Holonet should be organized as a typed predictive controller whose physical actions
> are selected by future decision value. Geometry supplies the state and legal group
> actions; nonabelian curvature supplies route diagnosis; component-resolved optics
> supplies likelihoods; reversible frames absorb fake gates; and only decision-relevant
> information crosses an irreversible boundary.

The packet contains four exact finite closures, two exact synthetic-policy models, one
bounded search frontier, synthesizable self-dual-comb RTL, focused regressions, and a new
canonical paper spine.

## Evidence ladder

- **Exact finite:** independent 28-triangle D4 construction; M36 pair Pauli audit;
  6,480-flag permutation algebra; tetrahedral probability law; self-dual comb census.
- **Exact for an explicit synthetic model:** joint six-action posterior controller and
  causal entropic-curvature tensor.
- **Bounded negative evidence:** 27-triangle collision-cut search.
- **Source-complete, digitally unobserved:** self-dual-comb RTL, manuscript integration,
  synthesis/place, and three PDF builds.
- **Open:** 27-row infeasibility, full 213,648,435-subspace M36 census, full complex
  irreducible decomposition of the flag module, laboratory optical calibration, and
  physical dissipation.

# Pass 3025 — fixed D4 frontier

The complete no/one/two-edge fault universe contains 48,826 hypotheses. An independently
found 28-triangle schedule gives distinct full group-valued syndromes for all 48,826 and
also separates all 1,036 central-`r^2` supports of weight at most two.

The independent schedule is:

```text
012 017 028 034 036 037 056
059 068 125 134 139 158 169
179 237 245 249 267 269 348
358 359 456 478 489 567 678
```

For the central involution, every selected triangle is a parity-check row on the 45 edge
coordinates. Separating all supports of weight at most two is exactly the requirement that
no difference of two such supports—hence no nonzero edge word of weight at most four—lies
in the restricted kernel. This is the relevant distance-five binary coding reduction.

A collision-driven 27-row MILP was run through 259 feasible adversarial schedules and
12,336 accumulated exact collision cuts. No witness appeared. A separate stochastic
search reached nine remaining central-support collision pairs. Neither computation proves
infeasibility. The exact theorem remains

\[
23\le m_{\rm fixed}^{(2)}\le 28.
\]

The adaptive worst-case result from Pass 2996 remains 25, so adaptive operation is already
better than the best fixed construction even before the 27-row problem closes.

# Pass 3026 — M36: subspace magic is not a stabilizer code

The displayed seeded source from the parallel paper track was reproduced exactly:

```text
seed                      2990
random Clifford words     120,000
gates per word            20
Clifford generator count  42
raw qualifying hits       30
projective witnesses      19
orthogonal pairs          18
```

For every orthogonal pair:

- each endpoint is a six-qubit stabilizer state;
- the common same-sign Pauli subgroup has order 8 and binary rank 3;
- a rank-two six-qubit stabilizer code would require five independent common same-sign
  stabilizers, subgroup order 32;
- the pair therefore spans a rank-two subspace but **not** a rank-two stabilizer code;
- projection of the clean three-copy M36 state succeeds with probability \(1/6\);
- the normalized projection has stabilizer Rényi-2 entropy
  \(1.540568381363\) bits;
- it has a two-stabilizer decomposition giving stabilizer-extent upper bound 2.

Thus the rank-two subspaces are genuinely magic-bearing but do not answer the stabilizer
code question. This closes the logical gap in the phrase “two orthogonal stabilizer states
span a code”: they span a subspace, while a stabilizer code is a common Pauli eigenspace.

The fail-closed 495-shard general-isotropic census remains separate. No exhaustive ranking
is claimed before all 213,648,435 subspaces have been observed and aggregated.

# Pass 3027 — exact 6,480-flag representation algebra

The objectwise flag set is reconstructed directly:

\[
X=\{(\{\ell_1,\ell_2\},S,t)\},
\]

where \(\ell_1,\ell_2\) are skew isotropic W33 lines, \(S\) is one of the three spreads
containing them, and \(t\) is one of their four common isotropic transversals.

Exact counts are:

\[
|X|=540\cdot3\cdot4=6,480.
\]

The 40 symplectic transvections generate a point permutation group of order 25,920,
namely the projective symplectic action. It acts transitively on \(X\). The stabilizer of
one flag is exactly

\[
H\cong V_4.
\]

The fixed-point character of the four stabilizer elements on \(X\) is

\[
6480,\;288,\;288,\;24.
\]

Burnside's lemma gives the number of \(H\)-orbits on \(X\):

\[
\frac{6480+288+288+24}{4}=1770.
\]

Therefore the transitive permutation representation
\(\mathbb C[X]\cong {\rm Ind}_{V_4}^{PSp(4,3)}1\) has exact permutation rank and
commutant dimension

\[
\boxed{1770}.
\]

Its stabilizer-orbit census is:

```text
24 orbits of size 1
264 orbits of size 2
1482 orbits of size 4
```

There is a real dimensional bridge

\[
6480=27(81+120+24+15)=27\cdot240,
\]

but it is not a representation theorem. The exact commutant invariant shows that a naive
“27 identical copies of four independent Hodge sectors” reading is unjustified. A
fail-closed GAP script with explicit point generators and explicit flag stabilizer is
included to compute the full irreducible multiplicities without guessing a subgroup-class
fusion.

# Pass 3028 — component-resolved tetrahedral shell

For tetrahedral Bloch vectors \(n_i\),

\[
E_i=\frac14(I+n_i\cdot\sigma),\qquad
\rho_j=\frac12(I+\eta n_j\cdot\sigma),
\]

and therefore

\[
p(i\mid j)=\frac14(1+\eta n_i\cdot n_j).
\]

With a symmetric four-label transport channel of correctness \(q\), the final row is

\[
p_{\rm correct}=q\frac{1+\eta}{4}+(1-q)\frac{1-\eta/3}{4},
\]

with three equal wrong probabilities.

The frozen component stack uses one internally coherent synthetic record:

```text
survival                         0.675
OAM correct given survival       0.975
slot correct given OAM           0.9900018993
address transport q              0.9652518519
valid-click probability          0.6748667493
```

At perfect intrinsic tetrahedral visibility, the compiler predicts:

```text
conditional correct outcome      0.4884172840
each wrong outcome               0.1705275720
bits per detected photon         0.1895477156
bits per launched photon         0.1279194507
```

The ideal independent-copy ML success values reproduce the exact tetrahedral sequence:

```text
1 copy   0.5000000000
3        0.5833333333
5        0.6736111111
8        0.7700617284
12       0.8510260679
```

After component erasure and crosstalk, the corresponding 12-launched-copy success is
0.7485677394.

The shell is therefore not selected because it maximizes raw bits per photon. It is
selected when the four-way \(V_4/A_4\) covariance and informational completeness are worth
the lower single-copy discrimination rate.

# Pass 3029 — one posterior controller for three photon families

A finite hidden state was defined as

```text
route fault × calibration health × chirality = 8 states.
```

The action alphabet is:

1. route-curvature triangle;
2. component calibration probe;
3. chirality copy;
4. stop.

For the explicit sparse prior, component likelihoods, action costs, and horizon six, exact
dynamic programming chooses route diagnosis first and then uses all three measurement
families. Its expected action counts are approximately:

```text
route       1.11794850
calibrate   1.83582862
chirality   2.17514482
total       5.12892194
```

The comparison silo baseline is seven actions. The joint controller's expected terminal
weighted risk is 0.02448499 after expected action cost 0.01079719.

The architectural rule is:

> Spend the next photon where it minimizes expected downstream Bayes loss, not where an
> independently scheduled subsystem says a measurement is due.

# Pass 3030 — causal entropic curvature

For actions \(a,b\) with outcomes \(Y_a,Y_b\), define

\[
K(a,b)=I(S;Y_a,Y_b)-I(S;Y_a)-I(S;Y_b)
      =I(S;Y_b\mid Y_a)-I(S;Y_b).
\]

This measures overlap or synergy between diagnostic actions. In the frozen joint model:

```text
K(route,calibrate)    -0.0144196927 bits
K(route,chirality)    -0.0004209092
K(calibrate,chirality)-0.0042849075
Frobenius norm         0.0212821585
```

The negative values identify redundant information induced by the shared calibration
nuisance.

Raw mutual-information efficiency ranks chirality first. The six-step consequence-weighted
dynamic field instead ranks route first:

```text
Q(route)       0.0352821819
Q(calibrate)   0.0363621255
Q(chirality)   0.0383444910
Q(stop)        0.7250000000
```

Thus information volume and causal decision value are not the same quantity. This is an
information-geometric controller diagnostic, not a claim about spacetime curvature.

# Pass 3031 — self-dual photonic comb

The prior synchronization word was optimal against cyclic substitutions but not invariant
under the desired reversal. An exhaustive search over all

\[
\frac{12!}{(3!)^4}=369,600
\]

balanced words found:

```text
cyclic distance 9                    63,744
distance 9 and D4-self-dual             384
also maximum cyclic run at most 2       192
```

A canonical selected word is

\[
\boxed{001032122313}.
\]

It has cyclic distance nine, corrects four substitutions, has maximum run two, and obeys

\[
\pi(w_{8-t})=w_t,
\qquad
\pi=(0\;2),
\]

where \(\pi\) is a \(D_4\) reflection fixing slots 1 and 3.

The 89/233 Christoffel calendar has reflection axis 88 modulo 233. Chinese remaindering
with the phase axis 8 gives the unique full-comb reversal origin

\[
a\equiv88\pmod{233},\qquad a\equiv8\pmod{12},
\]

namely

\[
\boxed{a=1952\pmod{2796}}.
\]

The complete reversal law is

\[
R(t)=1952-t\pmod{2796}.
\]

The 2,796-tick comb contains:

- 1,068 calibration events;
- 89 events in every D12 phase;
- global event gaps only 2 or 3;
- per-phase gaps only 24, 36, or 60.

The shell's order-three phase is inverted by the outer \(C_2\) in
\({\rm Aut}(A_4)\cong S_4\), while the same \(S_4\) extension supplies the slot reflection.
This gives a typed reversible extension without allowing shell opcodes to mutate the
protected \(D_4\) route registers.

# Complete paper overhaul

The papers are reorganized around one evidence-first spine.

## Part I — The finite object

- canonical construction of \(W(3,3)\);
- points, isotropic lines, spreads, skew pairs, and the 6,480 flag bundle;
- exact group actions and representation algebra;
- explicit separation of dimensions, modules, and analogies.

## Part II — The predictive machine

- native mixed-radix controller;
- D4 curvature and fixed/adaptive localization;
- typed A4 shell and protected D4 core;
- zero/one/two-transvection route control;
- fake-gate/frame-tracking rewrite rules;
- self-dual 2,796-tick comb.

## Part III — The optical and quantum layer

- component-resolved OAM/slot/detector channel;
- tetrahedral shell;
- sequential chirality receiver;
- nine-gate M36 branch;
- exact distinction among stabilizer states, stabilizer subspaces, and stabilizer codes.

## Part IV — Information, thermodynamics, and evidence

- joint posterior controller;
- causal entropic curvature;
- predictive memory and reset boundary;
- exact/modelled/measured claim ledger;
- queued workflows and falsifiers;
- unresolved 27-row, full M36, character, optical, and hardware questions.

Historical theorem inserts remain available as an evidence ledger, but they no longer define
the narrative order. The new front matter states the architecture and falsification
boundaries before the historical development.

# Literature boundary

The following sources motivate methods but do not supply any project-specific number:

- Leone, Oliviero, and Hamma, *Stabilizer Rényi entropy*, arXiv:2106.12587.
- Leone and Bittel, *Stabilizer entropies are monotones for magic-state resource theory*,
  arXiv:2404.11652.
- Tian et al., *Minimum-Consumption Discrimination of Quantum States via Globally Optimal
  Adaptive Measurements*, PRL 132, 110801 (2024).
- Still et al., *Thermodynamics of Prediction*, PRL 109, 120604 (2012).
- Nagase and Sagawa, *Thermodynamically optimal information gain in finite-time
  measurement*, PR Research 6, 033239 (2024).
- Medendorp et al., experimental SIC-POVM implementation, QELS 2010 QFF4.

The exact schedules, group actions, controller values, and comb word in this packet are
repository computations.
