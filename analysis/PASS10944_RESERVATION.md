# Pass 10944 — five-front computational closure

This packet executes the five fronts left by Pass 10943 and the parallel
temporal E8 work. Its executable witness is
`analysis/w33_pass10944_five_front_computational_closure.py`.

## 1. The missing 54-dimensional intertwiner is an exact no-go

The positive parabolic slice P is two copies of the regular H27 module. Its
restriction contains each of the nine linear characters twice and the two
three-dimensional Schrodinger irreducibles with multiplicity six each. The
Fourier quotient `S2+L` instead contains each linear character three times,
no `V_omega`, and nine copies of `V_omega^2`.

Consequently the two 54-dimensional spaces are not isomorphic H27 modules.
The maximum rank of an H27-equivariant map is

```text
9 min(2,3) + 3 min(6,0) + 3 min(6,9) = 36.
```

This explains the repeated rank-36 barrier and rules out the requested
invertible equivariant intertwiner. Exact elimination over `Q(omega)` gives
the optimal replacement: 36 coordinate directions from P and 18 from the
opposite grade-minus-two slice Q form a quotient basis modulo S1. The JSON
certificate records every selected coordinate.

## 2. The E6 cubic is a universal reversible clock opcode

For the committed signed cubic

```text
N(x) = sum d_ijk x_i x_j x_k mod 3,
```

define

```text
E6_CUBIC_TICK(direction,x,t):  t <- t + direction*N(x) mod 3.
```

Negating `direction` is the exact inverse. Phase kickback gives
`U_N|x> = omega^N(x)|x>`, the product of 45 commuting signed qutrit CCZ
gates. Conjugating a Pauli X produces a non-Pauli quadratic Clifford phase,
so the gate is third-level and non-Clifford.

One supported triad supplies a stronger compiler. Copy a control trit x into
a clean rail, fix the third rail to one, apply X to the target, and apply the
sign-corrected inverse tick. The target update is

```text
t <- t + 1 - x^2,
```

which is exactly a `|0>`-controlled qutrit X because `1-x^2` is one only at
`x=0`. Both ancillas are returned. Roy, van de Wetering and Yeh prove that
this controlled-X plus the qutrit Fourier gate is approximately universal in
every odd prime dimension (arXiv:2307.10095). Pass 10944 supplies the exact
E6-cubic realization of their primitive.

## 3. The four M36 selectors carry the full S4 action

Enumeration of all 432 affine transformations gives

```text
AGL(2,3) -> PGL(2,3) ~= S4
kernel order 18, image order 24.
```

Every permutation of the four null/Hesse/M36 families has 18 affine lifts.
The canonical three-resource/one-calibration assignment has S3 stabilizer and
full preimage order 108. Explicit GL(2,3) matrices moving family D to each of
the four selector positions are frozen in the certificate. Thus no family is
geometrically preferred. This is label covariance; the corresponding optical
unitaries still require calibration.

## 4. Circuit-level Golay syndrome and injection core

The executable circuit model contains six transversal eleven-location banks:
X-syndrome SUM, Z-syndrome SUM, R-injection controlled-X-squared, and three
destructive measurement banks. There are 66 active locations. Every one of
the

```text
1 + 66 + C(66,2) = 2,212
```

fault sets of size at most two was enumerated. Coordinate transversality keeps
the surviving block-error support and bad measurement-symbol support at weight
at most two, within the distance-five decoder.

Under independent location noise p, the conservative core bound is

```text
P_fail <= 1 - sum_(j=0)^2 C(66,j) p^j (1-p)^(66-j)
       = 45,760 p^3 + O(p^4).
```

The claim is conditioned on accepted clean encoded inputs. More generally an
input support of size s and r new coordinate-local faults is covered only for
`s+r <= 2`. If each of the three accepted encoded blocks violates that
contract with probability q, `P_total <= 3q + P_fail`. The preparation and
verification factories behind q remain a separate open circuit audit.

## 5. Physical four-to-three-mode and pump specifications

For family f, the matrix Wf deletes mode f. All 36 rays satisfy

```text
Wf Wf^dagger = I3,
Wf^dagger Wf = I4-|f><f|,
dark amplitude = 0.
```

The four families use dark modes 0,1,2,3 respectively. A sufficient 99-percent
conditional-fidelity allocation is

- core transform fidelity at least `0.9966554934`;
- residual phase at most about `0.057864` radians;
- differential loss at most about `0.502881` dB.

Dark-port leakage is budgeted separately at `1e-3`, requiring at least 30 dB
extinction. This avoids conflating conditional fidelity with success loss.

For the two-jump Strange reservoir, the ideal gap is `gamma/2`; one-percent
coherence settling requires `gamma*t >= 2 log 100`. A conservative resolvent
bound gives

```text
||delta rho_ss||_1 <= 16 epsilon + 8 epsilon^2.
```

The one-percent steady-state target therefore requires relative jump-operator
error below the certified epsilon in the JSON. These are falsifiable design
targets, not measurements or predictions.

## Scope

The finite module obstruction, quotient basis, reversible opcode, S4 selector
action, 66-location fault model, and interface inequalities are exact within
their declared models. The packet does not claim a microscopic cubic
Hamiltonian, an encoded-ancilla factory, a fabricated mode router, or measured
Holonet performance.
