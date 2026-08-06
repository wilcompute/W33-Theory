# Passes 4005–4012 — exact photon revival, compressed delay tomography, coherent memory, and algebra execution gates

## Release status

```text
PASS_EXACT_NONDISPERSIVE_REVIVAL_TOMOGRAPHY_MEMORY_AND_THREE_CONSTRUCTIONS
ORBITAL_RELATION_FUSION_AND_MONSTER_ENGINE_OUTPUTS_PENDING
```

Exact photon certificate:

```text
3e4561f56a0719c85a3b1e9b56f3c79d5d3e0bc4e9a21707a30abd26bb6a5cf2
```

This packet audited the parallel Passes 3997–4004 release before proceeding. That release exactly closed physical scheduling, synthetic delay tomography, maximum-code stabilizer identification, geometry recovery, edge-cycle memory, and metrological delay laws. It did not publish the literal 48-relation fusion output or the GAP/mmgroup Monster execution output. Those two absent artifacts remain fail-closed and are now exposed through draft PR 281, whose workflow uploads generated JSON and logs rather than hiding them behind a push-only job.

# 4005 — exact finite-detuning 80-mode revival

Let `N` be the 40-by-40 point-line incidence matrix of `W(3,3)`, with

\[
NN^{\mathsf T}=4I+A,
\]

and singular values

\[
4^1,\quad(\sqrt6)^{24},\quad0^{15}.
\]

Consider the complete point-bus Hamiltonian

\[
H=g\begin{pmatrix}
0&N\\
N^{\mathsf T}&(\Delta/g)I
\end{pmatrix}.
\]

At the finite parameter values

\[
\boxed{\Delta/g=2\sqrt2},
\qquad
\boxed{gt=\pi/\sqrt2},
\]

the three relevant half-angle windings are exactly

\[
3\pi,\quad2\pi,\quad\pi.
\]

The off-diagonal point-bus blocks therefore vanish exactly. The point action is

\[
\boxed{
U_P=E_{16}-E_6+E_0
=I-2E_6
=-\frac{I+A}{3}+\frac{2J}{15},
}
\]

and the line action is

\[
U_L=F_{16}-F_6+F_0.
\]

Direct exponentiation of the full 80-by-80 Hamiltonian gives operator error

\[
6.55\times10^{-15}
\]

and point-bus leakage below

\[
2.9\times10^{-15}.
\]

This is an exact non-dispersive revival, not a second-order effective-Hamiltonian approximation.

# 4006 — quadratic-form Wigner–Smith tomography

A Hermitian delay operator can be reconstructed from expectation values alone. For basis vectors `e_i`, define

\[
\tau(v)=v^\dagger Qv.
\]

Then

\[
Q_{ii}=\tau(e_i),
\]

\[
\Re Q_{ij}
=\tau\!\left(\frac{e_i+e_j}{\sqrt2}\right)
-\frac{Q_{ii}+Q_{jj}}2,
\]

\[
\Im Q_{ij}
=\frac{Q_{ii}+Q_{jj}}2
-\tau\!\left(\frac{e_i+i e_j}{\sqrt2}\right).
\]

A general Hermitian 40-by-40 matrix therefore needs exactly

\[
\boxed{40^2=1600}
\]

quadratic probes. Reciprocity and real symmetry reduce this to

\[
\boxed{40+\binom{40}{2}=820}.
\]

The exact synthetic W33 reconstruction recovered all 240 edges with maximum matrix error below `2.6e-15`.

For the three-frequency central-difference estimator and linear phase law,

\[
Q_h=\frac{\sin(h\theta' L)}{h},
\]

so

\[
Q_h-Q=-\frac{h^2}{6}(\theta')^3L^3+O(h^4).
\]

Richardson extrapolation removes this leading bias and the measured successive error ratios approach sixteen.

The causal firewall is unchanged: Wigner–Smith delay is dwell/group-delay memory. A precursor or causal-front observable must be measured independently, and `Q` must be subtracted before interpreting a mode-count-dependent front slope.

# 4007 — exact bright-sector write, hold, and read

Let `E_16,E_6,E_0` be point projectors and `F_16,F_6,F_0` the corresponding line projectors. Define the polar partial isometry

\[
T=N^{\mathsf T}\left(\frac{E_{16}}4+\frac{E_6}{\sqrt6}\right).
\]

Then

\[
T^{\mathsf T}T=E_{16}+E_6,
\qquad
TT^{\mathsf T}=F_{16}+F_6.
\]

With

\[
X=\begin{pmatrix}0&T^{\mathsf T}\\T&0\end{pmatrix},
\]

the write gate

\[
\boxed{W=e^{-i\pi X/2}}
\]

swaps the 25-dimensional point-bright sector into the line-bright sector while fixing both 15-dimensional dark sectors.

A diagonal hold phase on the bus followed by `W^dagger` returns

\[
\boxed{
e^{-i\phi_0}E_0+e^{-i\phi_6}E_6+e^{-i\phi_{16}}E_{16}
}
\]

on the point modes. Thus the sequence implements every spectral phase gate in the three-dimensional adjacency algebra. The test with three unrelated phases had operator error below `2.7e-15` and leakage below `3.1e-15`. Choosing

\[
(\phi_0,\phi_6,\phi_{16})=(0,\pi,0)
\]

returns the W33 reflection.

This proves a controlled-Hamiltonian synthesis. It does not prove that the dense polar coupling `T` has already been fabricated.

# 4008 — literal relation-fusion execution gate

The required frozen output remains absent:

```text
data/PART_3999_ORBITAL_RELATION_FUSION.json
```

The observable workflow in draft PR 281 executes the immutable 48-relation, 904-constant tensor through the exact rational central Fourier transform, forms equal-character relation blocks, refines them until every fused product is block-constant, and tests all pairwise mergers. It uploads both generated JSON files and both logs even on failure.

No relation-fusion rank or merger count is promoted before the generated artifact is inspected. The already-proved center remains

\[
\mathbb Q^2\oplus M_2(\mathbb Q)^3\oplus M_3(\mathbb Q)\oplus M_5(\mathbb Q).
\]

# 4009 — observable Monster execution gate

The required executed summary likewise remains absent:

```text
data/PART_4000_MONSTER_EXECUTION_SUMMARY.json
```

The second job in draft PR 281 installs GAP character tables and `mmgroup`, clones the published maximal-subgroup generator database, executes the maximal-overgroup class-fusion sieve, performs the bounded order-three quadruple search, and uploads the acquisition JSON, summary JSON, strict word artifact if one exists, and all logs.

Until four portable words pass the order-25,920 closure, object-action, code, Norton, line-split, and class-fusion firewalls, the correct state is

```text
PENDING_EXPLICIT_MONSTER_U42_WORDS_AND_EXECUTED_CLASS_FUSION
```

A negative bounded search would still not prove absence.

# 4010 — bonkers: revival arithmetic is an integer quadric

Every exact zero-leakage reflection revival of the uniform-detuning incidence Hamiltonian is constrained by

\[
\boxed{3n_{16}^2-8n_6^2+5k^2=0},
\]

with phase parities

\[
n_{16}+k\equiv0\pmod2,
\qquad
n_6+k\equiv1\pmod2.
\]

The physical parameters are

\[
\frac{\Delta}{g}
=k\sqrt{\frac{24}{n_6^2-k^2}},
\]

\[
gt=2\pi\sqrt{\frac{n_6^2-k^2}{24}}.
\]

The smallest positive primitive solution is

\[
\boxed{(n_{16},n_6,k)=(3,2,1)},
\]

which gives the finite-detuning revival above. Since `n_6^2-k^2 >= 3` for an admissible positive solution and equality forces this triple, it is the shortest member of the revival family. Seventy primitive solutions with indices below 600 were enumerated.

# 4011 — bonkers: the delay matrix is a self-calibrating geometry oracle

Let

\[
\tau=\frac{\operatorname{Tr}Q}{480}.
\]

An ideal W33 delay matrix obeys the basis-free polynomial checksum

\[
\boxed{Q(Q-10\tau I)(Q-16\tau I)=0}.
\]

The three projectors are reconstructed without external timing calibration:

\[
E_0=\frac{(Q-10\tau I)(Q-16\tau I)}{160\tau^2},
\]

\[
E_{10}=\frac{Q(16\tau I-Q)}{60\tau^2},
\]

\[
E_{16}=\frac{Q(Q-10\tau I)}{96\tau^2}.
\]

The finite geometry itself follows from

\[
\boxed{A=-\frac{Q-(\operatorname{Tr}Q/40)I}{\tau}}.
\]

Thus a measured device has an internal algebraic checksum: deviations of the cubic polynomial directly quantify departure from the ideal W33 delay geometry.

# 4012 — bonkers: synchronized self-similar clock

For `m` commuting physical copies of the exact 80-mode revival Hamiltonian, all factors reach their revival at the same time

\[
\boxed{gt=\pi/\sqrt2},
\]

and the point action is

\[
U_P^{\otimes m}.
\]

Since one factor has `+1` multiplicity 16 and `-1` multiplicity 24, the tensor eigenspace dimensions are

\[
\boxed{
m_+=\frac{40^m+(-8)^m}{2},
\qquad
m_-=\frac{40^m-(-8)^m}{2}.
}
\]

The logical address space grows as `40^m` while the ideal parallel clock period remains constant. This is a synchronization theorem, not a hardware-compression theorem: independently instantiated factors require growing physical resources.

# Evidence boundary

Executed and exact:

- the complete 80-by-80 finite-detuning revival;
- zero-leakage point and line involutions;
- 1,600/820-probe quadratic-form tomography;
- central-difference and Richardson error laws;
- the polar bright-sector write-hold-read construction;
- the revival Diophantine quadric and its shortest solution;
- the basis-free Wigner–Smith checksum and projectors;
- synchronized tensor-clock multiplicities.

Still pending:

- inspected literal relation-fusion output;
- inspected GAP/mmgroup Monster output and portable words;
- physical synthesis of the polar coupling;
- fabricated hardware and measured scattering matrices;
- any mode-dependent vacuum light speed or literal hidden-node ontology;
- remote CI and manuscript PDF evidence.
