# BT1468--BT1470: ABI expander, claim dependency DAG, and transcription UI

## BT1468 — closure ABI expander

The BT1467 closure packet ABI is now executable.  Given

\[
(c,s,o)\in C_3\times C_2\times C_2,
\qquad
\mathrm{strand}=4c+2s+o,
\]

BT1468 regenerates:

\[
12\text{ packets},\qquad 48\text{ events},\qquad 72\text{ active/guard rows}.
\]

The active columns are \(14\mathrm{strand}+13\), and the guard columns cover the
full tail \(216,\ldots,239\).  This proves the ABI is not just descriptive; it
is executable and regenerates the closure rows used by the decoder pipeline.

## BT1469 — paper-claim dependency DAG

The paper claims are now represented as a DAG:

\[
\text{Szilassi coordinates}
\to
\text{closure bus}
\to
\text{group/decoder/ABI},
\]

with resonance and blocked claims downstream.  The firewall rule is:

\[
\text{blocked/speculative claims never support exact claims.}
\]

The real-world model node is terminal, and formula-level claims must pass through
transcription/audit before any promotion is allowed.

## BT1470 — formula transcription UI packet

The manual transcription packet is now available in both CSV and Markdown.  It
has one row for each target equation:

\[
49,\quad50,\quad64,\quad65,\quad66.
\]

Each row includes formula image reference, raw formula field, parser expression
field, target class, residual, and claim tier.  Equation (65) is marked against
\(12/13\), while equation (66) is marked against Schwinger \(\alpha/\pi\).

## Current architecture

\[
\boxed{
\text{executable closure ABI}
+\text{claim dependency DAG}
+\text{manual transcription UI}
}
\]
