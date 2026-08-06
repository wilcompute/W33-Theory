# Passes 4105–4112 — carrier, reference, netlist, decoder, nonlinear patterns, and three bonkers probes

## Evidence boundary

All promoted statements are exact finite algebra, exact correlated-channel formulas, deterministic netlist contracts, rigorous sparse-syndrome bounds, or explicitly stated deterministic numerical simulations. Nothing here is a derived Standard Model, fabricated device, measured experiment, molecular synthesis, gravity, cosmology, or a theory of everything.

Frozen certificate: `data/PART_4105_4112_CARRIER_REFERENCE_NETLIST_DECODER_TURING_BONKERS.json`  
Semantic SHA-256: `836d6b72812b4b999bc6b7f62192deb7166dc5ef2c854827f620b0b1effc7072`

## 4105 — the 99-dimensional carrier is real but incomplete

The proposed module

\[
(C^6\otimes V_1)\oplus(C^3\otimes V_{15})\oplus(C^2\otimes V_{24})
\]

has dimension 99 and commutant `M6 + M3 + M2`. It directly accommodates a `(3,2)`, one anti-triplet, and one doublet, but not a second independent anti-triplet and charged singlet. Hence it cannot contain `Q,u^c,d^c,L,e^c` as independent one-particle multiplets.

Under the sector assignment `Q,e^c -> V1`, `u^c,d^c -> V15`, and `L -> V24`, the exact minimum is

\[
(C^7\otimes V_1)\oplus(C^6\otimes V_{15})\oplus(C^2\otimes V_{24}),
\qquad 7+90+48=145.
\]

The multiplicity decompositions are `C7=(3,2)+(1,1)`, `C6=bar3+bar3`, and `C2=bar2`. All local and global anomaly sums vanish exactly. Attaching the overlap operator supplies Ginsparg–Wilson chirality, not a completed chiral gauge theory.

## 4106 — exact multi-use phase-reference law

For the sine reference

\[
c_n=\sqrt{2/(K+2)}\sin((n+1)\pi/(K+2)),
\]

the sequential cyclic processor acts collectively. For basis strings `x,y`,

\[
\mathcal E_N(|x\rangle\langle y|)=z_{|x|-|y|}|x\rangle\langle y|.
\]

For `m>=0`,

\[
C_m={ (K+1-m)\cos(m\theta)+\sin((m+1)\theta)/\sin\theta\over K+2},
\]

\[
B_m=\sum_{n=0}^{m-1}c_nc_{m-1-n},
\qquad
z_m=e^{im\phi}C_m+e^{-i(K+1-m)\phi}B_m.
\]

Equal-Hamming-weight coherences are preserved exactly. For fixed `N`, the worst error scales as `O(N^2/K^2)` and the wrap term as `O(N^3/K^3)`. At `K=256`, worst errors through `N=1,5,10,20` are approximately `7.36e-5, 1.81e-3, 7.11e-3, 2.73e-2`.

## 4107 — fabrication netlist

The exact route table compiles into four coherent 80-mode branches. Each branch contains 40 parallel point-line swap cells. A balanced binary selector uses three couplers and the inverse recombiner uses three more. The signal depth is five layers.

A recirculating five-query QSP device uses one 160-swap signal block, six selector/recombiner couplers, six phase shifters, and five coherent passes. A spatially unrolled device uses 800 swap cells, 30 selector/recombiner couplers, and six phase shifters.

## 4108 — robust three-bond syndrome decoding

For `y=De+n`, `||n||<=epsilon`, exhaustively minimize the residual over the 682,641 supports of size at most three. Two candidate errors differ on at most six edges. Because the Levi girth is eight, every such union is a forest. The worst six-edge forest is a path, giving

\[
\sigma_6=2\sin(\pi/14)=0.4450418679.
\]

Therefore

\[
||\hat e-e||_2\le {2\epsilon\over\sigma_6}.
\]

If every nonzero amplitude exceeds `4 epsilon/sigma6`, thresholding recovers the exact support. Noiseless three-error decoding is unique.

## 4109 — nonlinear Turing saturation

Add componentwise cubic saturation to the two earlier linear selectors. Deterministic BDF integration to `t=500` from the same seed converges entirely into the intended eigenspace:

- the first model has lambda-10 modal purity numerically 1 and residual `2.06e-12`;
- the second has lambda-16 modal purity numerically 1 and residual `2.65e-12`.

Thus nonlinear saturation preserves the 24-versus-15 spectral selection for these explicit kinetics.

## 4110 — bonkers: exact average consensus in two rounds

Because the only nonzero Laplacian eigenvalues are 10 and 16,

\[
{J\over40}=(I-L/10)(I-L/16)=I-{13\over80}L+{1\over160}L^2.
\]

Each node computes `r=Lx`, then `s=Lr`, then outputs `x-13r/80+s/160`. Every node obtains the exact global average after two nearest-neighbour rounds. One round is impossible because one linear factor cannot annihilate both nonzero eigenvalues while preserving the zero mode.

## 4111 — bonkers: random-walk navigation geometry

The simple-walk spectrum is `1^1,(1/6)^24,(-1/3)^15`. Effective resistance and rank-three symmetry give exact hitting times

\[
H_{\rm adjacent}=39,
\qquad
H_{\rm nonadjacent}=42.
\]

The Kemeny constant is

\[
24/(1-1/6)+15/(1+1/3)=801/20.
\]

## 4112 — bonkers: W33 Hückel shells

For `H=alpha I+beta A`, `beta<0`, the orbital shells are `alpha+12 beta` (1), `alpha+2 beta` (24), and `alpha-4 beta` (15), with spin capacities 2, 48, and 30. Electron counts 2, 50, and 80 are closed shells. The 50-electron gap is exactly `6|beta|` and its total one-electron energy is `50 alpha+120 beta`.

At 40 electrons the middle shell has ten holes and

\[
\binom{48}{10}=6,540,715,896
\]

Slater determinants before interactions split the degeneracy.
