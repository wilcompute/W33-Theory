# Passes 6017–6024 — post-closure integrity repair

## Executive result

The Pass5957–6016 “full closure” packet contained four different claim-tier failures. This packet repairs them at the producer level rather than merely adding a note.

### Repaired live artifacts

- `scripts/w33_ce2_anchor22_closure.py` now reports anchor 22 as open beyond three imported witnesses.
- `scripts/w33_yukawa_radical_pair_closure.py` retains the real-spectrum calculation and refutes the equal-coordinate generation flag.
- `scripts/w33_k3_glue_slot_realization.py` now computes the actual gcd 1 and labels the nonzero glue matrix as a formal inserted avatar.
- `scripts/w33_bridge_full_closure_theorem.py` is now a corrected tiered ledger, not a “full closure theorem.”
- `tools/qiskit/toe_bridge_completed_avatar_oracle.py` is now an encoding/search scaffold and explicitly states that no phase oracle is implemented.
- `docs/pass_5957_6016_summary.md` is replaced with the corrected summary.

## Pass6017 — CE2 anchor 22 was not globally closed

The historical producer imported three witness rows, then defined a synthetic function

```python
ce2_triple_weight(22,j,k)
```

whose return values were hard-coded `1/54` or `1/108` functions of integer labels. It then looped `j,k=1,...,39` and called the resulting nonzero count a “full orbit.” No W(3,3) automorphism group or CE2 tensor data entered that loop.

Its “cancellation” check was also only a denominator test: multiplying an already chosen `1/54` or `1/108` coefficient by 54 or 108 yields an integer by construction.

Therefore:

\[
\boxed{\text{CE2 anchor 22 remains open beyond the three imported witnesses.}}
\]

The live producer has been rewritten accordingly.

## Pass6018 — Yukawa radical pairs: real spectra yes, generation flag no

The two displayed symmetric blocks are

\[
A=\begin{pmatrix}367&-55\\-55&175\end{pmatrix},\qquad
B=\begin{pmatrix}323&275\\275&659\end{pmatrix}.
\]

Their exact invariants are

\[
\operatorname{tr}A=542,\quad \det A=61200,\quad \Delta_A=48964>0,
\]

\[
\operatorname{tr}B=982,\quad \det B=137232,\quad \Delta_B=415396>0.
\]

So both spectra are genuinely real.

However, the equal-coordinate vector `(1,1)` is not an eigenvector. A vector `(1,1)` is an eigenvector of a symmetric 2x2 matrix iff the two row sums agree. Here:

\[
A(1,1)^T=(312,120)^T,
\]

\[
B(1,1)^T=(598,934)^T.
\]

Thus the claimed machine-precision alignment with the proposed generation flag is refuted.

Retained theorem:

\[
\boxed{\text{both displayed radical-pair blocks have real spectra.}}
\]

Open: any K3-side or physical Yukawa realization, and any generation-flag theorem.

## Pass6019 — K3 glue script failed its own gcd assertion

The historical producer called

\[
(780,7944,62600,53979)
\]

a primitive generator of gcd 217. In fact

\[
\boxed{\gcd(780,7944,62600,53979)=1.}
\]

Therefore its historical `assert g == 217` fails.

The identity

\[
\frac{217}{12}\,780=14105
\]

is exact, but it is not a consequence of the vector gcd.

The nonzero glue in the same producer was inserted explicitly as an `I_81` tail-to-head block. Consequently the 162-dimensional square-zero matrix is a valid **formal avatar**, not a realized K3 curvature operator.

The live file now records exactly that distinction and leaves the genuine K3-side nonzero off-diagonal witness open.

## Pass6020 — bridge coefficients are formal parameters, not geometric invariants

The historical packet attached `351/(4*pi^2)` and `10530/pi^2` to the formal avatar. Because the transport/gcd premise was false and no K3 curvature witness was produced, those coefficients are not promoted by this packet as K3 geometric or physical invariants.

They may remain as parameters of the formal model.

## Pass6021 — downstream closure ledger inherited superseded physics

The historical “full closure theorem” listed as proved:

- Yang–Mills gap 1818 MeV;
- neutrino mass 0.0500 eV;
- inflationary `r=1/45`;
- scalar resonance 3.206 TeV.

Pass5957–5964 had already downgraded all four to **ANSATZ/COMPARISON-ONLY**. The live closure ledger has now been rewritten so those statuses propagate correctly.

## Pass6022 — Qiskit completed-avatar file was not an implemented oracle

The historical Qiskit file chose constants

```text
MARKED_CE2 = closed_22
MARKED_YUKAWA = both_real
MARKED_GLUE = nonzero_formal
```

and computed a Grover iteration count conditional on that preselected shard.

When Qiskit was available, the circuit itself only executed Hadamards followed by measurement. There was no reversible predicate, phase marking, multi-controlled target condition, or amplitude-amplification operator computing the theorem conditions from encoded data.

Therefore it was an encoding/search **specification**, not a theorem oracle.

The live file is now explicitly a search scaffold. Its state counts and conditional Grover arithmetic remain useful if a genuine predicate circuit is later supplied.

## Pass6023 — corrected claim tiers

Current status:

- CE2 anchor 22: **OPEN beyond three witnesses**.
- CE2 anchor 23: **SEEDED / partial**.
- Yukawa pair A/B spectra: **EXACT REAL 2x2 SPECTRA**.
- generation flag from those blocks: **REFUTED**.
- K3 glue: **FORMAL AVATAR ONLY**.
- genuine K3 glue realization: **OPEN**.
- completed-avatar Qiskit object: **SEARCH SCAFFOLD ONLY**.
- Pass5933–5956 masses/inflation: **ANSATZ/COMPARISON-ONLY**.

## Pass6024 — evidence rule

Three fail-closed rules are now explicit:

1. A global orbit is not verified by inventing a coefficient rule on integer labels; the actual group action and object values must be constructed.
2. A hand-inserted matrix normal form is a formal avatar, not a geometric realization.
3. A Grover/oracle artifact is not implemented until its marked predicate is computed reversibly from the encoded input rather than assigned as a constant.

These rules preserve the valid algebra while preventing formal scaffolds from silently becoming physical or geometric theorems downstream.
