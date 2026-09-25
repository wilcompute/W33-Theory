# Pass 10941 — triality VM five-front closure

Pass 10941 executes the five independent fronts reserved in commit
`d55f09d0b`. It converts the trialitarian contact-parabolic result into
coordinate, instruction-set, arithmetic, representation-theoretic, and
laboratory-facing objects. Every physical number introduced below is marked
as a declared design target.

## 1. The requested split-D4 rational conjugation has a centroid obstruction

The 18-dimensional rational core has Levi centroid the cubic field

\[
K=\mathbb Q[\theta]/(\theta^3-\theta^2-53\theta-120).
\]

A split \(A_1^3\) Levi has centroid \(\mathbb Q^3\). These algebras cannot be
isomorphic: the field has no nontrivial idempotent while \(\mathbb Q^3\) has
six. Therefore no rational Lie-algebra conjugation to the split D4 contact
parabolic exists.

The replacement certificate constructs two independent exact coordinate
charts from the 248-coordinate E8 realization into one fixed rational
trialitarian presentation. Their pivot determinants are

\[
1,
\qquad
-\frac{473476163093}{11659575003397200}.
\]

They agree on all 103 nonzero unordered brackets, and all \(18^3=5832\)
ordered basis Jacobi identities vanish. A split Chevalley chart becomes a
valid target only after scalar extension to a splitting field of \(K\).

## 2. The central-product phase space compiles to a seven-qutrit Clifford ABI

Write

\[
\mathfrak h_7/Z=W_8\widehat\oplus U_6^\perp.
\]

In a canonical hyperbolic basis this is a seven-mode symplectic register. The
compiler emits 24 elementary lane-local transvections and one bridge
transvection in direction \(e_3+e_4\). Exact modular commutator closure gives

\[
\dim(\mathfrak{sp}_8\oplus\mathfrak{sp}_6)=57
\quad\longrightarrow\quad
\dim\mathfrak{sp}_{14}=105
\]

at both 3 and 103. Adding Heisenberg translations yields the full logical
seven-qutrit Clifford/stabilizer instruction set. The bare compiler remains
classically simulable. The new universal-instruction bridge lowers every one
of the 25 listed transvections exactly into the fixed-interaction photonic
alphabet `F_i`, `P_i`, and `CZ_ij`; the longest frozen Clifford macro has
length seven. This matches the standard modular-arithmetic description of
qudit Clifford operations in
[Hostens--Dehaene--De Moor](https://arxiv.org/abs/quant-ph/0408190) and the
magic-resource boundary in
[Bravyi--Kitaev](https://arxiv.org/abs/quant-ph/0403025).

The fixed-interaction ADQC theorem already on master supplies the missing ideal
logical opcode. A programmed analyzer branch implements

\[
K_m=3^{-1/2}X^{-m}FT,
\qquad
T=\operatorname{diag}(1,\zeta_9,\zeta_9^{-1}),
\]

with input-independent outcome probability $1/3$. Tracking $X^{-m}$ and
applying the compiled $F^{-1}$ produces $T$ on any of the seven modes. The
same fixed interaction supplies $CZ$, while the bridge generator connects the
four data modes to the three control modes. Thus the ideal instruction set is
seven-qutrit Clifford+$T$, which is approximately universal by
[Glaudell--Ross--van de Wetering--Yeh](https://arxiv.org/abs/2202.09235).

The resource identity is exact. If 

\[
|M_T\rangle=T|+\rangle,
\]

then the three programmed analyzer vectors obey

\[
|b_m\rangle=Z^{-m}|M_T^*\rangle.
\]

Their ninth-root exponent triples are $(0,8,1)$, $(0,5,4)$, and
$(0,2,7)$, and their maximum single-qutrit stabilizer fidelity is
0.712386014201. Measurement programming therefore relocates the same
non-stabilizer cyclotomic resource; it does not remove the need for magic. As a
second ideal port, all nine Pass 411 Choi-injection feed-forward words compile
into Heisenberg translations and at most five VM micro-operations.

This closes algebraic/logical universality under a supplied non-stabilizer
analyzer or Choi pair. It does not prove a physical photon-memory interaction,
an endogenous magic factory, or a fault-tolerance threshold. In particular,
the Pass 416 direct five-qutrit $T$-orbit search returns fidelity
0.918222659014 from a pure input and therefore does not distill this $T$
state. The Pass 411 distance-three expression is only a combinatorial bound.
The exact dark Strange ray remains a candidate source, but no dynamical
preparation, conversion-to-$T$, or protected injection map is known. No
rank-one stabilizer witness is used by this bridge.

At the ramified prime 3 this is a canonical logical ABI. The current rational
Asai basis has denominators divisible by 3, so the certificate does not perform
an invalid coordinatewise reduction of that chart.

## 3. The common W90 has a characteristic-zero integral target lattice

On the 240 signed W33 edges, let \(\rho\) be the integral signed-permutation
action and \(\chi_{90}\) the unique common irreducible character. The GAP
producer evaluates the central idempotent

\[
e_{90}=\frac{90}{51840}\sum_{g\in W(E_6)}
\chi_{90}(g^{-1})\rho(g)=\frac1{48}A.
\]

The frozen primitive integer matrix \(A\) is \(240\times240\), has 33,600
nonzero entries, commutes with all three group generators, and satisfies

\[
A^2=48A,
\qquad \operatorname{tr}(A)=4320,
\qquad \operatorname{rank}_{\mathbb Q}(A)=90.
\]

Thus \(L_{90}=A\mathbb Z^{240}\) is an explicit rank-90, W(E6)-stable integral
lattice whose rational span is the common W90. The GF(103) transducer is its
good-prime reduction. The primitive matrix has ranks 14 and 25 modulo 2 and
3, but rank 90 modulo 5, 7, and 103; this exposes real bad-prime degeneration
rather than a characteristic-zero obstruction. The certificate does not
claim that the old MeatAxe basis matrix lifts entry by entry.

## 4. Ramification becomes an automatic-differentiation instruction set

At each ramified prime \(p\in\{3,43,733\}\), the cubic centroid algebra is

\[
\mathbb F_p[\epsilon]/(\epsilon^2)\times\mathbb F_p.
\]

The exact register word is `(value, tangent, simple-branch value)`. The
producer freezes invertible coefficient/chart transforms and the opcodes
`DADD`, `DMUL`, `DINV`, `DFMA`, `DPOLY`, and `DCOMPOSE`. It proves all nine
basis products at each prime, 192 polynomial derivative identities, and 192
composition chain rules. The square-zero element maps to `(0,1,0)` exactly.
This gives first-order forward automatic differentiation in the ramified
finite algebra, consistent with the standard dual-number rule reviewed by
[Baydin et al.](https://jmlr.csail.mit.edu/papers/volume18/17-468/17-468.pdf).

## 5. The minimal eight-root control frame now has a normalized falsifier

For each compact root-plane generator \(G_j\), define

\[
\widehat G_j=G_j/\sqrt{120},
\qquad -B(\widehat G_j,\widehat G_j)=1.
\]

The six optimal microframes have integer L1 weights

\[
(4,5,5,4,5,5)
\]

and run for 72 ticks each. With the declared reference pulse area
\(\theta_0=\pi/2\), the complete AB cycle has weighted angle
\(28\theta_0=14\pi\). Under the declared relative integrated Hamiltonian
error \(\rho\), Duhamel gives

\[
\|\widetilde U-U\|\le e^{28\theta_0\rho}-1.
\]

The one-percent operator-error target therefore requires
\(\rho\le 2.262349058116424\times10^{-4}\). A separately declared 90 percent
unconditional survival target allows at most 0.4575749056 dB per AB cycle, or
0.0762624843 dB per microframe under equal allocation. End-to-end process
tomography, microframe omission, and root-plane sign reversal are the stated
falsifiers. No pulse duration, loss, crosstalk, or laboratory success is
inferred from the E8 algebra.

## Executables and frozen witnesses

- `analysis/w33_pass10941_rational_triality_coordinate_chart.py`
- `analysis/w33_pass10941_symplectic_vm_gate_compiler.py`
- `analysis/w33_pass10941_qutrit_universal_instruction_bridge.py`
- `analysis/w33_pass10941_w90_integral_lift.g`
- `analysis/w33_pass10941_w90_integral_lift.py`
- `analysis/w33_pass10941_ramified_dual_ad.py`
- `analysis/w33_pass10941_normalized_root_hamiltonian.py`
- `data/w33_pass10941_*.json`
- `data/w33_pass10941_w90_integral_projector.tsv`

The five claims are exact within their stated algebraic or declared-design
models. They do not derive spacetime, Standard Model parameters, gravity, or
a physical device from the finite structures.
