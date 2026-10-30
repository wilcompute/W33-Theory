# Pass 360 — the alpha code has an exact affine Clifford action

## Result

Pass 359 replaced the remote batch's proposed \([[137,1,3]]\) object by the
exact quadratic-residue CSS code

\[
[[137,1,21]].
\]

Pass 360 determines a nontrivial part of its **actual gate symmetry**.  Let the
137 qubits be indexed by \(\mathbb F_{137}\), let \(Q\) and \(N\) be the two
odd-like binary QR codes, and use \(Q^\perp\) and \(N^\perp\) as the two CSS
check spaces.  For \(a\ne0\), \(b\in\mathbb F_{137}\), write \(P_{a,b}\) for
the qubit permutation induced by \(x\mapsto ax+b\).  Then

\[
\widetilde P_{a,b}=
\begin{cases}
P_{a,b},&a\text{ a quadratic residue},\\
P_{a,b}H^{\otimes137},&a\text{ a quadratic nonresidue}
\end{cases}
\]

normalizes the CSS stabilizer.  These operators form a faithful Clifford copy
of

\[
AGL(1,137)\cong C_{137}:C_{136},\qquad |AGL(1,137)|=18{,}632.
\]

Its index-two pure-permutation subgroup is

\[
C_{137}:C_{68},\qquad |C_{137}:C_{68}|=9{,}316.
\]

The nonresidue coset acts on the one encoded qubit as logical Hadamard:

\[
\overline X\longleftrightarrow\overline Z.
\]

An explicit representative is \(P_{3,0}H^{\otimes137}\), because 3 is a
primitive quadratic nonresidue modulo 137.

## Why the logical gate is exact

The GAP witness constructs the QR/NQR generator and check matrices directly
from the two degree-68 factors of \(x^{137}-1\).  It then verifies, as equalities
of binary row spaces, that

\[
P_{9,0}(Q^\perp)=Q^\perp,
\qquad
P_{9,0}(N^\perp)=N^\perp,
\]

while

\[
P_{3,0}(Q^\perp)=N^\perp,
\qquad
P_{3,0}(N^\perp)=Q^\perp.
\]

Transversal Hadamard exchanges Pauli \(X\) and \(Z\), so the second pair is
exactly the condition needed for \(P_{3,0}H^{\otimes137}\) to normalize the
CSS stabilizer.  The all-ones vector lies in both normalizer codes but in
neither rank-68 check space.  Its odd self-overlap is one, so

\[
\overline X=X(\mathbf 1),\qquad
\overline Z=Z(\mathbf 1)
\]

is an anticommuting logical Pauli pair.  Every affine coordinate permutation
fixes \(\mathbf 1\), and the Hadamard factor exchanges the Pauli labels.  Thus
the induced logical action is proved rather than inferred from classical code
equivalence.

Equivalently, the certificate realizes the exact sequence

\[
1\longrightarrow C_{137}:C_{68}
\longrightarrow \widetilde{AGL}(1,137)
\longrightarrow \langle\overline H\rangle\cong C_2
\longrightarrow1.
\]

## The 138-point projective closure

Add the parity coordinate at infinity.  On
\(\mathbb P^1(\mathbb F_{137})\), GAP constructs the three permutations

\[
x\mapsto x+1,
\qquad x\mapsto9x,
\qquad x\mapsto-1/x.
\]

They preserve the chosen extended \([138,69,22]\) QR code and generate

\[
PSL(2,137),qquad |PSL(2,137)|=1{,}285{,}608.
\]

The action is doubly transitive, and the stabilizer of infinity is precisely
the same residue-affine group \(C_{137}:C_{68}\) of order 9,316.  This closes
the puncture/extension diagram:

\[
\begin{array}{ccc}
C_{137}:C_{68}&<&PSL(2,137)\\
\rotatebox{90}{$\cong$}&&\rotatebox{90}{$\curvearrowright$}\\
\operatorname{Stab}(\infty)&<&\operatorname{Sym}(\widehat Q_{137}).
\end{array}
\]

Adjoining the nonresidue projective multiplier \(x\mapsto3x\) gives an
index-two group of order 2,571,216 with GAP structure
\(PSL(2,137):C_2\), the natural \(PGL(2,137)\) envelope.  It does **not**
preserve one chosen extended code: its nontrivial coset exchanges the extended
QR and NQR codes.  That distinction is checked explicitly and prevents a
common automorphism-group over-read.

## What is inherited and what is new here

The classical parameters and weight distribution are not new: Tjhai,
Tomlinson, Ambroze, and Ahmed determine the augmented \([137,69,21]\) and
extended \([138,69,22]\) QR codes and recall that the extended-code
automorphism group contains \(PSL(2,137)\)
([paper](https://arxiv.org/abs/0801.3926)).  General affine classifications of
prime-length cyclic-code automorphisms are also published by Guenda and
Gulliver ([paper](https://arxiv.org/abs/1207.3132)), and the general mechanism
of a duality permutation composed with transversal gates is the
fold-transversal framework of Breuckmann and Burton
([paper](https://arxiv.org/abs/2202.06647)).

The contribution of Pass 360 is the exact \(p=137\) integration:

1. the QR/NQR check-space transport is computed from the repo's own GAP
   matrices;
2. the nonresidue multiplier and transversal Hadamard are assembled into a
   concrete stabilizer automorphism;
3. the all-ones logical representatives prove the encoded action;
4. explicit Mobius permutations close the affine group into the 138-point
   \(PSL/PGL\) tower; and
5. all claims are emitted as one 37-check machine-readable certificate.

The result-first search found the code parameters and multiplier equivalence in
Pass 359, but no prior repo occurrence of \(9{,}316\), \(18{,}632\),
\(1{,}285{,}608\), \(2{,}571{,}216\), the explicit \(PSL/PGL\) action, or the
logical-Hadamard lift.

## Reproduce

```bash
gap -q analysis/w33_pass360_alpha_code_logical_hadamard.g
python3 -m pytest -q tests/test_pass358_359_gap_github_integrity_alpha_code.py -k pass360
```

Expected GAP summary:

```text
Pass360 status=PASS checks=37 output=data/w33_pass360_alpha_code_logical_hadamard.json
```

## Boundary

This is an exact code-theoretic Clifford symmetry.  It neither identifies
\(1/137\) with the measured fine-structure constant nor supplies a fault-tolerant
hardware implementation.  The number 137 selects the code in this packet; the
certificate does not derive a physical coupling from it.
