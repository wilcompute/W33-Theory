# Randomness / decryptability five-front execution

This packet executes the five continuations opened by `W33_OBSERVER_RELATIVE_RANDOMNESS.md`.

## 1. Contextual decryption obstruction

`analysis/w33_contextual_decryption_obstruction.py`

A local one-click key chooses one point in every commuting context. A single global noncontextual key would be a 0/1 valuation whose line sums all equal one, i.e. an ovoid.

The exact finite search gives:

- `W(2)`: 15 contexts, 3 choices/context, **6** global keys;
- `W(3,3)`: 40 contexts, 4 choices/context, **0** global keys.

So the cryptographic metaphor splits cleanly:

- classical epistemic randomness may be missing a global key;
- the W33 one-click contextual model has no context-independent global key to reveal.

Boundary: this is selection/ovoid contextuality, not a claim that every quantum-contextuality notion reduces to ovoid nonexistence.

## 2. Observer-information lattice

`analysis/w33_observer_information_lattice.py`

For the two-sample retained-noise record `O`, primitive observer side information is `Y,S0,S1`.

Exact values include:

- `H(O|Y)=3` bits;
- `H(O|Y,S0)=H(O|Y,S1)=1.5` bits;
- `H(O|Y,S0,S1)=0`;
- `Pguess(O|Y)=1/4` so `Hmin(O|Y)=2` bits;
- full side information gives `Pguess=1`.

The script enumerates the full eight-state inclusion lattice and checks monotonicity of Shannon and min entropy under added side information.

## 3. Causal accessibility

`analysis/w33_causal_accessibility_randomness.py`

The same side information is attached to 1+1D events and an observer may condition only on its past light cone.

Along the worldline `x=0`:

- at `t=0`, only `Y` is accessible and the residual entropy is 3 bits;
- at `t=2`, `Y+S0` is accessible and the residual is 1.5 bits;
- at `t=4`, `Y+S0+S1` is accessible and the record is exactly decryptable.

At the same coordinate time `t=2`, an observer at `x=2` instead has `Y+S1`. Thus decryptability is observer-location dependent even for the same underlying event.

Boundary: this is a causal toy model, not an identification of relativistic horizons with cryptographic ciphers.

## 4. Seeded vs ideal-quantum source harness

`analysis/w33_seeded_vs_quantum_entropy_harness.py`

The deterministic seeded map

`Y=(73*S+41) mod 256`

is a permutation of one byte. Therefore a seedless observer sees exactly the uniform byte distribution:

- `H(Y)=Hmin(Y)=8` bits;
- `H(Y|S)=0`;
- total-variation distance from the ideal uniform byte reference is exactly zero.

Both source marginals are exhaustively fed through the same HoloVM `add-r1-into-r0` guest over all 256 byte values. Because HoloVM is deterministic, identical input distributions give identical terminal-state distributions.

This is the crucial separation: downstream statistics need not reveal whether the source was seeded or physically random. Provenance lives in side information and certification evidence.

Boundary: the built-in quantum arm is an ideal Born-uniform reference, **not** a laboratory or device-independent certificate. The harness accepts external certification metadata but does not self-certify it.

## 5. Determinism vs universal prediction

`analysis/w33_determinism_prediction_boundary.py`

The operational predictor is one-sided:

- if HALT occurs within the simulation horizon, return `HALTS`;
- otherwise return `UNKNOWN`, never `NONHALT`.

For every fuel value 1..16, the certificate constructs a program that exceeds that horizon and then halts with more fuel. A known infinite-loop guest remains `UNKNOWN` at horizons through 64.

This finite witness separates deterministic transition semantics from finite-horizon prediction. The stronger all-program boundary follows from the repository's universal two-counter core: under ordinary Turing-computability assumptions, a total HALT/NONHALT oracle for all encoded executions would decide the halting problem.

## Synthesis

The five fronts replace the binary question “random or deterministic?” with a layered object:

1. **Gluing:** does a global context-independent key exist at all?
2. **Information:** what side information does this observer possess?
3. **Causality:** what side information can physically have reached the observer?
4. **Provenance:** are identical-looking samples seeded, ideal-random, or externally certified?
5. **Computation:** even with deterministic laws and complete state, is the requested prediction computable/decidable?

The strongest compact formulation is therefore:

> Randomness is an observer-, resource-, context-, and causality-relative failure of recoverability. Encryption is one engineered way to create that failure. Contextuality can obstruct a single global classical key, and universality can obstruct a total predictor even when the local transition law is deterministic.

All five scripts are gated in `.github/workflows/w33_vm_retention_output_audit.yml`.
