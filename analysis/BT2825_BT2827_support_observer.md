# Passes 2825--2827: Finite-Delay Support Observer

## Headline theorem

The binary PG(3,2) support shell is not a deterministic execution quotient of the 81-state ternary frame, but it is an exact finite-delay observer.

There are two complementary forms.

### Adaptive / all-word observer

Refining states by all support observations reachable with instruction words of bounded length gives

\[
\boxed{16\longrightarrow40\longrightarrow78\longrightarrow81}.
\]

The unresolved unordered state-pair counts are

\[
\boxed{272,\;53,\;3,\;0}.
\]

Equivalently, the numbers newly separated at depths 0, 1, 2, and 3 are

\[
\boxed{2968,\;219,\;50,\;3}.
\]

The only pairs surviving through depth two are

\[
(0,0,1,z_f)\sim(0,0,2,z_f),\qquad z_f\in\mathbb F_3.
\]

All three are separated by each of the following length-three words:

\[
\mathrm{CX}_{f\to p}\,F_p\,Z_p,
\]

\[
Z_p\,F_p\,\mathrm{CX}_{p\to f},
\]

\[
Z_p\,F_p\,\mathrm{CX}_{f\to p}.
\]

Thus the adaptive observability index is exactly three.

### Fixed open-loop observer

For one predetermined diagnostic word, observing the initial support mask and the support mask after every prefix gives the best distinct-trajectory counts

\[
\boxed{25,\;40,\;45,\;68,\;77,\;81}
\]

for word lengths 1 through 6.  Therefore no fixed word of length at most five identifies all states, while length six is sufficient.

Exactly eight length-six words are injective.  A canonical choice is

\[
\boxed{
\mathrm{CX}_{p\to f},\;F_p,\;Z_p,\;F_p,\;Z_p,\;\mathrm{CX}_{p\to f}
}.
\]

The eight words factor as

\[
2\times2\times2:
\]

- either controlled-add direction at the entrance,
- either alternating middle pattern \(F_pZ_pF_pZ_p\) or \(Z_pF_pZ_pF_p\),
- either controlled-add direction at the exit.

## Minimal telemetry theorem

The canonical diagnostic word produces seven 4-bit support snapshots, or 28 raw telemetry bits.  Exhaustive column selection proves:

- no seven sampled support bits distinguish all 81 states;
- exactly 48 eight-bit tap sets do;
- therefore the minimum is exactly eight bits.

One canonical tap set uses flattened columns

\[
\boxed{(0,1,2,5,13,21,25,26)}.
\]

In time/coordinate form:

\[
(t_0,x_p),\;(t_0,z_p),\;(t_0,x_f),\;(t_1,z_p),
\]

\[
(t_3,z_p),\;(t_5,z_p),\;(t_6,z_p),\;(t_6,x_f).
\]

Five taps are mandatory across all 48 minimal selectors:

\[
(t_0,z_p),\;(t_0,x_f),\;(t_5,z_p),\;(t_6,z_p),\;(t_6,x_f).
\]

No minimal selector ever samples the \(z_f\) support bit.

## Architectural consequence

The machine does not need to expose ternary phase on its external telemetry interface.  It can:

1. keep the full four-trit frame internally;
2. execute one six-cycle diagnostic word;
3. sample eight binary support taps;
4. recover the exact 81-state frame through an 81-entry decoder ROM.

This sharpens the Pass 2822 boundary:

\[
\boxed{
\text{support is insufficient as instantaneous execution state,}
\quad
\text{but sufficient as finite-delay telemetry.}
}
\]

## Evidence boundary

This is an exact noiseless observability and decoder theorem.  It does not yet establish robustness under readout error, photon loss, dark counts, phase drift, or imperfect gate implementation.  Those require a noisy-channel code-distance analysis and hardware measurements.
