# Passes 3989–3996 — sparse W33 photonics, complete maximum-code orbits, central fusion lattice, Monster acquisition, and causal memory

## Release status

```text
PASS_EXACT_FIVE_FRONT_THREE_BONKERS
MONSTER_WORDS_FULL_FOURIER_COEFFICIENT_FREEZE_AND_PHOTON_LAB_PENDING
```

Combined semantic manifest:

```text
16397906a63553464abb18b0f65f839a7265afe9ef2fe712857c7e0efc977d27
```

This packet combines independently reproduced code-orbit certificates with two complementary physical W33 coupler models, the complete central fusion lattice of the rank-48 algebra, an explicit maximal-overgroup Monster acquisition search, and a new Wigner–Smith formulation of the user's proposal that time behaves as accumulated history or memory.

# 3989 — an 80-mode degree-four incidence coupler

Let `N` be the `40×40` point-line incidence matrix of `W(3,3)`. Every point and line has incidence degree four, and

\[
NN^{\mathsf T}=4I+A_{W33}.
\]

The bipartite incidence graph therefore has 80 modes, only 160 couplings, girth eight, and exact spectrum

\[
\boxed{-4^1,\;(-\sqrt6)^{24},\;0^{30},\;(\sqrt6)^{24},\;4^1.}
\]

For equal point-bus coupling `g` and bus detuning `Delta`, second-order elimination gives

\[
H_{\rm eff}=-\frac{g^2}{\Delta}NN^{\mathsf T}
=-\frac{g^2}{\Delta}(A+4I)+O(g^4/\Delta^3).
\]

Thus the declared interaction time

\[
\boxed{t=\frac{\pi\Delta}{2g^2}}
\]

implements the W33 reflection in the dispersive limit, up to the controlled higher-order error. This gives a degree-four physical lift of a degree-twelve effective Hamiltonian.

The exact incidence identity and spectra are proved. Fabrication, loss, crossing layout, simultaneous calibration, and higher-order device performance are not claimed.

# 3990 — a one-flight 40-mode W33 coupler and exact echo

A still simpler ideal model uses forty modes with equal coupling on the 240 W33 edges:

\[
i\frac{d\psi}{dz}=\kappa A_{W33}\psi.
\]

Because the adjacency spectrum is

\[
12^1,\quad2^{24},\quad(-4)^{15},
\]

one interaction area

\[
\boxed{\kappa z=\frac\pi2}
\]

gives

\[
\boxed{
 e^{-i\pi A/2}=-\frac{I+A}{3}+\frac{2J}{15}.
}
\]

This is an exact real symmetric involution. Each row has amplitude `-1/5` on the input point and its twelve neighbors and amplitude `2/15` on its twenty-seven nonneighbors.

For uniform fractional interaction error `epsilon`, the relative phase slopes in units of `pi epsilon` are

\[
-6,\;-1,\;2
\]

with multiplicities `1,24,15`. Their weighted first moment vanishes because `Tr A=0`, while the weighted second moment is three. Hence

\[
F_{\rm pro}=1-3\pi^2\epsilon^2+O(\epsilon^3),
\]

\[
F_{\rm avg}=1-\frac{120}{41}\pi^2\epsilon^2+O(\epsilon^3).
\]

Uniform coupling-length miscalibration therefore has no linear average-fidelity penalty.

For the complement `B=J-I-A`,

\[
A+B=J-I
\]

is geometry-blind on the 39-dimensional nonuniform space, while

\[
D=A-B
\]

has spectrum

\[
\boxed{-15^1,\;5^{24},\;(-7)^{15}.}
\]

If a commuting common perturbation `C` enters both arms,

\[
e^{-it(A+C)}e^{+it(B+C)}=e^{-it(A-B)}
\]

exactly. The dual-geometry echo therefore cancels common commuting error while preserving the W33 contrast channel.

# 3991 — complete classification of maximum fixed-parent codes

The fixed binary character code is

\[
C=[36,6,16].
\]

Its dual contains 945 admissible weight-four words. The compatibility graph, joining pairs with even support intersection, is regular of degree 624 and has maximum clique size 57.

Two independent exact implementations agree that there are precisely

\[
\boxed{945}
\]

maximum cliques. Under the parent-preserving group

\[
O_6^-(2)\cong U_4(2):2,
\qquad |G|=51{,}840,
\]

they split into exactly three orbits:

\[
\boxed{540+270+135=945.}
\]

Their stabilizer orders are

\[
\boxed{96,\;192,\;384.}
\]

The 945 compatibility vertices themselves split as `135+810`. The orbit of 540 maximum codes contains `3+54` words from these two vertex orbits, while the orbits of 270 and 135 contain `15+42`.

Every maximum code has dimension seventeen, minimum weight four, and the same weight distribution

\[
\begin{aligned}
1&+57z^4+852z^8+7332z^{12}+57294z^{16}\\
 &+57294z^{20}+7332z^{24}+852z^{28}+57z^{32}+z^{36}.
\end{aligned}
\]

Every orbit also has the same intersection-two component parameters

\[
\boxed{
\operatorname{SRG}(45,16,8,4)
\sqcup2\operatorname{SRG}(6,4,2,4),
}
\]

equivalently `T(10) ⊔ 2T(4)`, and coordinate profile `9^20,3^16`.

Thus uniqueness is false, but the fixed-parent maximum-code problem is completely classified into three exact group orbits.

# 3992 — the complete central fusion lattice

The rank-48 orbital algebra has split simple degrees

\[
\boxed{1,1,2,2,2,3,5}
\]

and regular ranks

\[
1,1,4,4,4,9,25.
\]

Its seven-dimensional center has one unital subalgebra for every partition of its seven primitive central idempotents. All

\[
\boxed{877}
\]

set partitions were enumerated exactly. The counts by central dimension are

\[
1,\;63,\;301,\;350,\;140,\;21,\;1.
\]

After quotienting by the order-twelve relabeling group of equal-degree sectors, there are exactly

\[
\boxed{198}
\]

inequivalent central fusion types, distributed as

\[
1,\;23,\;68,\;66,\;31,\;8,\;1.
\]

These are exact central fusion subalgebras. A central partition need not lift to a combinatorial fusion of the 48 orbital relations. The existing self-publishing Fourier verifier is separately recomputing the full primitive-idempotent coefficient and character-table file.

# 3993 — Monster acquisition through explicit maximal overgroups

The external route is now concrete rather than aspirational.

The GAP stage enumerates direct `U4(2)`-to-Monster class fusions and compatible compositions through Monster maximal-subgroup tables. The Python stage matches those tables to the published explicit `mmgroup` maximal-subgroup generator database, builds bounded element pools, searches for order-three quadruples with the exact pair-order fingerprint

\[
3,6,6,6,6,6,
\]

requires every three-generator subgroup to have order 648, and requires the full closure to have order 25,920.

A candidate is promoted only after portable `MM` words survive:

- integer round trips;
- pair and triple relations;
- exact group order;
- the 36-axis action;
- the 135-frame and 120-Norton hashes;
- the `[36,6]` code distribution;
- the `45+216+270+120` line split;
- the class-fusion and restricted-character gate.

No candidate artifact has yet passed all these conditions. The correct status remains

```text
PENDING_EXPLICIT_MONSTER_U42_WORDS_AND_CLASS_FUSION
```

# Bonkers I — Wigner–Smith time is an exact memory operator

For a frequency-dependent W33 scattering unitary

\[
S(\omega)=e^{i\theta(\omega)L_{W33}},
\]

the Wigner–Smith operator is

\[
\boxed{
Q(\omega)=-iS(\omega)^\dagger\frac{dS}{d\omega}
=\theta'(\omega)L_{W33}.
}
\]

Its proper-delay sectors are therefore

\[
\boxed{0^1,\quad(10\theta')^{24},\quad(16\theta')^{15}.}
\]

The mean proper delay is

\[
\boxed{12\theta'},
\]

its variance is

\[
\boxed{12(\theta')^2},
\]

and its total delay trace is

\[
\boxed{480\theta'}.
\]

This is the operational version of “time as memory”: `Q` measures frequency sensitivity, dwell time, and energy-like storage in a multiport. More internal resonant structure can increase stored history or density of states without changing the vacuum causal front.

A literal hidden-node signal is now sharply defined: after reconstructing and subtracting `Q`, matching spectrum and transverse momentum, and separating causal-front timing from pulse-peak delay, a residual mode-count-dependent propagation slope would falsify the invariant-front null.

# Bonkers II — self-similar delay shells form an exact history ledger

For `m` independent W33 factors, the proper-delay multiplicity polynomial is

\[
\boxed{(1+24z^{10}+15z^{16})^m.}
\]

The address space contains

\[
40^m
\]

modes, while the proper delays add. Thus

\[
\langle\tau\rangle=12m\theta',
\qquad
\operatorname{Var}(\tau)=12m(\theta')^2.
\]

The exact information-delay ratio is

\[
\boxed{
\frac{\log_2(40^m)}{\langle\tau\rangle}
=\frac{\log_2 40}{12\theta'}.
}
\]

It is independent of tensor depth. Meanwhile

\[
\frac{\sigma_\tau}{\langle\tau\rangle}=\frac1{\sqrt{12m}}.
\]

Self-similarity therefore expands address space and accumulated history in lockstep while making the normalized history depth increasingly sharp.

# Bonkers III — dark memory, Floquet clock, and causal impedance

The 80-mode incidence lift has thirty exact zero modes: fifteen point-dark and fifteen line-dark coordinates. The bright space has dimensions one and twenty-four. Relative phase between dark and bright sectors supplies a clock-referenced memory degree of freedom without identifying time itself with RAM.

The exact quarter-step

\[
V=e^{-i\pi L/4}=I-(1+i)E_{10}
\]

has order four and satisfies

\[
V^2=I-2E_{10}.
\]

This gives an exact Floquet clock internal to the engineered graph dynamics.

Under tensor powers of the incidence map,

\[
\operatorname{rank}(N^{\otimes m})=25^m,
\]

\[
\dim\ker(N^{\otimes m})=40^m-25^m,
\]

so the dark fraction is

\[
\boxed{1-(5/8)^m.}
\]

Finally, a Lieb–Robinson-type internal causal cone has schematic physical speed

\[
v_{\rm int}\lesssim a\,C_{LR}(\Delta)J/\hbar.
\]

For self-similar node refinement to preserve the same physical cone, the product

\[
\boxed{aJ}
\]

must remain fixed. Packing more serial nodes while keeping coupling strength fixed slows the internal cone; node density by itself cannot determine or raise vacuum `c`.

# Evidence boundary

Exact in this packet:

- both W33 coupler graph identities and spectra;
- the direct one-flight transfer matrix and uniform-error expansion;
- the dual-geometry echo identities;
- the complete 945-code, three-orbit maximum census;
- all 877 central partitions and 198 inequivalent central fusion types;
- the incidence dark-space, Floquet, and tensor-rank laws;
- the Wigner–Smith operator, delay sectors, moments, and self-similar shell polynomial.

Declared models or future measurements:

- dispersive device accuracy beyond the exact leading Hamiltonian;
- a fabricated 40- or 80-mode array;
- reconstructed electromagnetic Wigner–Smith delays;
- the Lieb–Robinson prefactor and hardware mapping;
- measured capacity, loss, timing, or front velocity.

Still fail-closed:

- portable Monster `MM` words and executed character fusion;
- the pending full orbital primitive-idempotent coefficient freeze;
- variable vacuum light speed;
- literal hidden photon nodes;
- remote CI/PDF success and laboratory validation.
