# Passes 3787–3794 — exact twirl estimation, Floquet cancellation, distributed clocking, control ports, dynamic topology, and three architecture breakthroughs

## Exact status

The executable certificate reports

```text
PASS_8_FRONTS aa3daf462320badd607a1720479f083df159044f24242e7f46810de30bc2e0d8
```

The focused regression reports

```text
6 passed
```

This packet executes the five architecture attacks proposed after Passes 3743–3750 and adds three deliberately different mechanisms. The central outcome is that the W33 control plane can now be assigned finite costs for symmetry estimation, static-error cancellation, frame dissemination, addressability, rewiring, calibration, spectroscopy, and collective communication.

---

## 3787 — minimum exact observable twirl design

The order-25,920 W33 automorphism group has three ordered-pair orbits:

\[
40\quad\text{diagonal},\qquad
480\quad\text{oriented adjacent},\qquad
1080\quad\text{oriented nonadjacent}.
\]

An exact unweighted estimator of the three orbit averages must visit each ordered-pair target at least once, so it needs at least

\[
40+480+1080=\boxed{1600}
\]

settings. Choosing one shortest group word for every target attains this lower bound.

The exact shortest-word costs are

\[
144+2635+6155=\boxed{8934}
\]

generator macros, with maximum word lengths six, nine, and nine on the three orbit types. The previous full-group sweep costs 211,898 generator macros, so the exact observable estimator is smaller by a factor

\[
\boxed{23.7181553615}.
\]

This closes the minimum unweighted **observable/orbit-estimation** problem. It does not close the stronger active conjugation-channel twirl. The latter retains the previously proved divisibility lower bound

\[
\operatorname{lcm}(40,480,1080)=4320.
\]

---

## 3788 — a forty-step Floquet static-error canceller

The four point-line incidence matchings induce relative permutations of cycle types

\[
(20,20),\qquad(40),\qquad(40),
\]

and generate the complete symmetric group \(S_{40}\). Select either relative forty-cycle and call it \(C\).

For every diagonal error Hamiltonian \(D\),

\[
\frac1{40}\sum_{t=0}^{39}C^{-t}DC^t
=
\frac{\operatorname{tr}D}{40}I.
\]

Therefore every traceless static diagonal disorder mode cancels exactly over one forty-step orbit; only the common-mode component remains. A persistent fault set of size \(f\) is also seen exactly \(f\) times by every routed logical channel over the complete orbit.

The frozen regular-cycle digest is

```text
3746b8b4b89c1572b6e861ffa0ee21ecbd3a87eb10dd763e68e6cf4c84d06ead
```

This is an exact permutation/Floquet decoupling result for static diagonal disorder. It is not a complete Floquet quantum code, a general coherent-error theorem, or a measured filter function.

---

## 3789 — optimal seven-tick distributed frame broadcast

The 80-node point-line incidence network is operated in the telephone/store-and-forward model: one perfect matching is active per tick and every informed endpoint can copy the frame symbol across its active edge.

Starting from point node 14 at schedule phase zero, the exact informed-node census is

\[
1,2,4,8,16,30,54,80.
\]

Thus all forty point nodes and forty line/check nodes receive the frame in

\[
\boxed{7\text{ ticks}}.
\]

No protocol in this model can beat seven ticks because the informed population can at most double per tick:

\[
\left\lceil\log_2 80\right\rceil=7.
\]

The construction is therefore optimal. Its broadcast tree contains 79 edges, has depth seven, and has digest

```text
ab96a90c868710ef5ce4ab425d556197cfbcef302d57c7c084df38f86266c87f
```

This replaces the previous 80-step central-frame-bus lower bound with an optimal seven-tick distributed protocol under the declared communication model.

---

## 3790 — the exact W33 zero-forcing number is 29

The prior packet proved only

\[
24\le Z(W33)\le29.
\]

This packet closes the interval using a complete automorphism-orbit enumeration of reverse zero-forcing sequences. The orbit counts at reverse lengths zero through eleven are

\[
1,1,2,5,16,43,191,769,3024,9772,24852,34890.
\]

Every one of the 34,890 depth-eleven orbits is terminal, and no depth-twelve orbit exists. Hence the longest reverse forcing sequence has length eleven and

\[
\boxed{Z(W33)=40-11=29}.
\]

An explicit minimum zero-forcing set is

\[
\{4,5,7,8,9,10,11,13,14,15,16,17,18,19,20,
24,25,26,27,29,30,31,32,33,34,35,37,38,39\}.
\]

One exact force chain is

\[
8\!\to\!1,
7\!\to\!23,
5\!\to\!36,
10\!\to\!21,
14\!\to\!0,
16\!\to\!6,
6\!\to\!12,
13\!\to\!22,
4\!\to\!28,
22\!\to\!3,
0\!\to\!2.
\]

The canonical proof-stream digest is

```text
94f90a31640a9504b89cad7262318b4d7356918c03b6968da09ece4959926f60
```

The normal certificate checks the frozen orbit counts, level digests, terminal frontier, witness set, and force chain. The CI heavy-audit mode deterministically regenerates every orbit level. Zero forcing is still a sufficient graph-control certificate under the standard Hamiltonian assumptions; it is not a calibrated pulse-robustness theorem.

---

## 3791 — a dynamically rewired W33/locality hybrid

A degree-twelve local ring with jumps

\[
\{1,2,3,4,5,6\}
\]

was relabelled against W33 to maximize useful hardware reuse. The explicit witness shares

\[
\boxed{128\text{ couplers}}
\]

between the W33 and local phases. Each phase has 240 edges, so the complete reconfigurable inventory is

\[
240+240-128=\boxed{352\text{ couplers}},
\]

rather than 480 disjoint couplers—a 26.67% reduction.

The mixed two-step operator \(AB+BA\) provides at least two cross-phase two-step paths for every unordered channel pair. The full two-phase walk operator

\[
A^2+B^2+AB+BA
\]

has pairwise off-diagonal counts between four and 27. Thus alternating the two phases preserves a nonzero global two-step transport floor while exposing a more local degree-twelve phase.

The relabelling digest is

```text
74a3682024b80dd882aab302d635db6e147084a6c31346cdab1ba2b4f421fea1
```

This is an explicit high-overlap construction, not a proof of maximum overlap, minimum coupler inventory, or minimum physical wirelength.

---

## 3792 BONKERS — eleven actuators become virtual calibration channels

Because \(Z(W33)=29\), twenty-nine physically addressed phase ports suffice for the exact zero-forcing certificate. The remaining eleven modes can be identified sequentially along the force chain.

At every step \(u\to v\), all neighbors of \(u\) except \(v\) have already been calibrated. The residual response at \(u\) therefore isolates the previously unknown response of \(v\).

The ideal graph-linear model consequently supports

\[
\boxed{29\text{ physical actuators}+11\text{ virtualized channels}}
\]

with eleven sequential inference steps. This is exact structural identifiability; it does not provide a noisy calibration condition number or error-propagation bound.

---

## 3793 BONKERS — the Floquet orbit is a Fourier spectrometer

Let the forty-cycle order the physical diagonal-error vector as

\[
(d_0,d_1,\ldots,d_{39}).
\]

Applying the forty characters of the cyclic orbit produces the complete length-forty discrete Fourier transform. The unmodulated character measures the common mode, while the 39 nontrivial characters recover every traceless diagonal component.

The unnormalised Fourier determinant has magnitude

\[
\boxed{40^{20}}
=
109951162777600000000000000000000,
\]

so the transform is invertible. The same permutation orbit can therefore be used either to average away static disorder or to diagnose all 39 non-common diagonal modes.

This is an algebraic spectroscopy design; phase wrapping, finite phase resolution, detector noise, and pulse imperfections remain hardware-model questions.

---

## 3794 BONKERS — reversible fourteen-tick qutrit all-reduce

Reverse the optimal seven-level broadcast tree and accumulate qutrit values using addition modulo three. The network gathers a global sum to the root in seven collision-free ticks. Running the broadcast direction then distributes the result to all 80 nodes in another seven ticks.

The resulting collective primitive is

\[
\boxed{7\text{-tick gather}+7\text{-tick broadcast}=14\text{ ticks}}.
\]

It uses the same 79 tree edges and can carry a global syndrome sum, distributed frame phase, or consensus symbol without an 80-link central bus.

This is a constructive reversible tree protocol. It is not a proof that fourteen ticks is globally optimal under every quantum communication or ancilla model.

---

## Reproduction

```bash
python analysis/w33_pass3787_3794_twirl_floquet_clock_control_hybrid.py
pytest -q tests/test_w33_pass3787_3794_twirl_floquet_clock_control_hybrid.py
```

The complete zero-forcing orbit regeneration is available as a separate fail-closed audit:

```bash
python analysis/w33_pass3787_3794_twirl_floquet_clock_control_hybrid.py \
  --verify-zero-forcing-ledger
```

## Evidence firewall

- The 1,600-setting theorem concerns exact observable/orbit estimation, not active channel twirling.
- Floquet cancellation is exact only for static diagonal disorder.
- The seven-tick broadcast assumes local store-and-forward and one active matching per tick.
- The equality \(Z(W33)=29\) is exact; its physical-control interpretation retains the standard graph-Hamiltonian assumptions.
- The W33/ring hybrid is an explicit construction, not an optimum.
- Virtual actuators, Fourier spectroscopy, and fourteen-tick all-reduce are exact algebraic/control mechanisms, not laboratory demonstrations.
