# Passes 3743–3750 — symmetry operating system, correlated decoding, hybrid factory, grand tournament, preregistration, and three architecture breakthroughs

## Exact status

The executable verifier reports

```text
PASS_8_FRONTS 67ce2d0ab105d8809dd6ae1af60381e1181d9a08c9032ce1dad1130f7bb8ff62
```

The focused local regression reports

```text
6 passed
```

This packet treats W33 as a control, scheduling, calibration, and diagnostic architecture around a protected carrier. It deliberately separates exact finite mathematics from optical pulse synthesis and measured hardware behavior.

## 3743 — four-generator symmetry operating system

The 40 projective symplectic transvections were regenerated directly on the W33 point set. A greedy exact closure finds four generators with vectors

\[
(0,0,0,1),\quad(0,1,0,0),\quad(0,0,1,1),\quad(1,0,0,0),
\]

and closure

\[
\boxed{|\langle g_1,g_2,g_3,g_4\rangle|=25{,}920}.
\]

Each generator has cycle census

\[
1^{13}3^9
\]

and therefore needs 18 arbitrary transpositions under a naïve swap decomposition. The Cayley-word compiler reaches every automorphism with

\[
\boxed{\operatorname{diam}=11},
\qquad
\overline \ell=8.17507716049.
\]

An exact sweep through all 25,920 symmetries uses 211,898 generator pulses. These are permutation macros, not calibrated optical sequences.

## 3744 — correlated space-time decoder

A two-state hidden Markov benchmark was frozen with transition matrix

\[
\begin{pmatrix}
49/50&1/50\\
1/4&3/4
\end{pmatrix},
\]

stationary bad-state probability \(2/27\), good-state flip probability \(10^{-3}\), and bad-state flip probability \(1/4\).

For eight repeated observations of a fixed syndrome bit, the exact MAP error is

\[
1.1395646255\times10^{-3}
\]

when observations are consecutive. Sampling the same check only once every four ticks replaces the transition kernel by its fourth power and gives

\[
\boxed{6.3819353522\times10^{-5}},
\]

only

\[
\boxed{0.0560032771}
\]

of the consecutive error. The four-match incidence schedule also guarantees that a one-tick global burst strikes at most one interaction incident on any point or line.

This is an explicit model result, not a measured noise law. It is consistent with current process-tensor decoding work, where maximum-likelihood decoders explicitly account for non-Markovian temporal correlations rather than assuming iid faults.

## 3745 — hybrid 81-register resource factory

The protected resource graph is organized as

\[
40\text{ point registers}+40\text{ line-check registers}+1\text{ frame/clock register}.
\]

It contains

\[
160\text{ incidence links}+80\text{ frame links}
=\boxed{240\text{ logical links}}.
\]

Encoding all 81 logical qutrits with the previously verified \([[3,1,2]]_3\) block code requires

\[
243\text{ physical qutrits},\qquad729\text{ triple-rail modes}.
\]

An exhaustive search over all \(3^9\) bilinear coupling matrices proves that a logical qutrit controlled phase needs at least three nonzero physical controlled-phase terms. One minimum matrix is

\[
W=\begin{pmatrix}
0&0&1\\
0&1&0\\
1&0&0
\end{pmatrix}\pmod 3.
\]

Thus the complete 240-link logical resource requires at least

\[
\boxed{720\text{ physical controlled-phase terms}}.
\]

At fusion success probability \(1/2\), ten attempts are needed for \(99.9\%\) success per physical link, giving a worst-case 7,200 attempt slots. A single frame bus has an unavoidable serial-depth lower bound of 80; parallel fanout requires extra cat-state, cluster-state, or matter-memory resources. This makes the resource bottleneck explicit.

## 3746 — grand geometry tournament

The complete degree-12 Cayley family on

\[
\mathbb Z_2^3\times\mathbb Z_5
\]

was enumerated. There are

\[
\boxed{167{,}356}
\]

valid generator selections, of which 165,984 are connected and 37,513 have diameter two.

The best spectral gap in this entire family is

\[
9.527864045<\boxed{10\text{ for W33}}.
\]

A noncyclic competitor can attain minimum nonedge common-neighbour count four, but its counts are

\[
4^{18},6^8,12^1,
\]

with nonzero variance. Twenty-eight Cayley graphs have zero variance, but all have uniform value two rather than four. A deterministic sample of 1,000 random 12-regular graphs has best observed gap \(7.644416652\), and no sampled graph has W33's uniform nonedge law.

The fixed \(5\times8\) layout witnesses also expose the tradeoff: W33's frozen Manhattan wirelength proxy is 884, while the local ring reaches 538. W33 wins the tested redundancy and expansion metrics, but not the locality proxy. The layouts are heuristic witnesses, not minimum embeddings.

## 3747 — preregistered hardware challenge

A machine-readable preregistration was frozen before data. It compares three devices:

1. W33;
2. the route-optimal degree-matched circulant;
3. a local-ring degree-matched control.

The locked structural endpoints include degree 12, 240 supported couplers, the matrix identity

\[
A^2=8I-2A+4J,
\]

40 recovered lines, 160 line triangles, and the marked-resolvent atlas.

The primary operational endpoint requires W33 to beat both controls by at least \(2\times10^{-4}\) on the worst-nonedge two-hop task under matched programmed transmissivity. The experiment also fails if twirling does not reduce the residual outside \(\operatorname{span}\{I,A,J\}\) below 10%, or if the four-tick schedule hides serialization or unreported resources.

For 64,000 simultaneously controlled probabilities, tolerance 0.01, and familywise error 0.01, the locked Hoeffding bound is

\[
\boxed{81{,}825\text{ shots per tomography setting}}.
\]

The primary effect-size test requires at least 264,915,869 shots per device under the conservative bound.

## 3748 BONKERS — the four-tick schedule generates \(S_{40}\)

Each perfect matching maps the 40 points bijectively to the 40 lines. Relative round maps therefore act as permutations on the point labels. The three consecutive relative maps have cycle types

\[
(40),\qquad(4,4,32),\qquad(4,6,13,17),
\]

and generate

\[
\boxed{S_{40}}.
\]

The exact group order is

\[
40!=815915283247897734345611269596115894272000000000.
\]

Thus the syndrome schedule is not merely a four-coloring: as a classical Floquet routing microcode, its relative round permutations generate every permutation of the 40 point channels. This is not yet a coherent quantum gate set.

## 3749 BONKERS — exact twirling has a large physical price

The W33 action has ordered-pair orbit sizes

\[
40,\quad480,\quad1080.
\]

Any unweighted exact twirl must distribute a source pair uniformly over each orbit, so its sample count must be divisible by

\[
\operatorname{lcm}(40,480,1080)=\boxed{4{,}320}.
\]

This is only a necessary lower bound. A deterministic 4,320-element hashed subset still misses 13 of the 1,080 nonadjacent targets and has highly nonuniform counts. The known exact construction uses all 25,920 automorphisms, requiring 211,898 compiled generator pulses.

Therefore the algebraic \(1600\to3\) channel compression remains exact, but physical twirling is not free. Smaller designs or weighted quadratures must be proved rather than assumed.

## 3750 BONKERS — passive symmetry versus controllability

Because W33 has three adjacency eigenvalues, every passive analytic function of the fixed adjacency Hamiltonian lies in

\[
\boxed{\operatorname{span}\{I,A,J\}},
\]

a three-dimensional algebra. Strong symmetry compresses calibration but also collapses passive expressivity.

The adjacency eigenvalue multiplicity 24 gives the zero-forcing lower bound

\[
Z(W33)\ge24.
\]

An explicit 29-vertex zero-forcing set and eleven-step force chain were found, proving

\[
\boxed{24\le Z(W33)\le29}.
\]

Under the standard graph-control hypotheses, 29 independently addressable diagonal phase ports suffice for full operator controllability. The exact minimum remains open. This result converts the vague requirement for 'local control' into a finite port-count target.

## Reproduction

```bash
python analysis/w33_pass3743_3750_symmetry_os_spacetime_factory_tournament.py
pytest -q tests/test_w33_pass3743_3750_symmetry_os_spacetime_factory_tournament.py
```

## Evidence firewall

- Automorphism macros are exact permutations, not measured pulse sequences.
- The HMM and fusion models are declared benchmarks, not empirical device laws.
- The Cayley tournament is exhaustive only for the stated family; random regular results are a deterministic sample.
- The fixed-grid layouts are heuristic witnesses.
- The hardware challenge is prospective and may falsify W33 advantage.
- \(S_{40}\) holonomy is classical routing, not coherent universality.
- The 4,320 twirl bound is necessary, not sufficient.
- The control-port result proves only the interval \(24\le Z(W33)\le29\).

## Primary external context

- Burgarth, D'Alessandro, Hogben, Severini, and Young, *Zero forcing, linear and quantum controllability for systems evolving on networks*, arXiv:1111.1475.
- Kobayashi et al., *Tensor-network decoders for process tensor descriptions of non-Markovian noise*, arXiv:2412.13739.
- Chan et al., *Tailoring fusion-based photonic quantum computing schemes to quantum emitters*, arXiv:2410.06784.
