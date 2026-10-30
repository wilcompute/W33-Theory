# Audit hold — Passes 126–156 and the submission packet

**Status: NOT SUBMISSION-READY (2026-07-09).**

This is an evidence firewall, not a rejection of the exact W33 programme.
The 14 commits added after Pass 125 were read file by file and cross-checked
against the executable repository, `w33_paper.tex`, and `docs/index.html`.
They contain useful exploratory calculations, but the submission-facing
claims do not currently follow from them.

## Decisive mathematical errors

1. **Basic W33 data are wrong in the submission sources.**
   `PAPER_INTRODUCTION.tex` says a line has 13 points and uses spectral
   multiplicities `(1,27,12)`. For \(W(3,3)\), a line has \(q+1=4\) points
   and the adjacency spectrum is
   \[
   12^1,\quad 2^{24},\quad(-4)^{15}.
   \]
   The parameters \((40,12,2,4)\) do not determine a unique graph without
   additional structure; there are two rank-three GQ(3,3) point graphs.

2. **The zeta formula uses the wrong multiplicities and Euler exponent.**
   `PAPER_SECTION2_ZETA.tex` uses `27,12` and
   \((1-u^2)^{20}\). Bass's formula requires
   \[
   (1-u^2)^{|E|-|V|}=(1-u^2)^{200}
   \]
   and adjacency exponents \(24,15\). Its displayed Hashimoto factorization
   is therefore not the characteristic polynomial of W33.

3. **The Bernoulli/zeta dictionary is arithmetically false.**
   The correct special values include
   \[
   \zeta(-3)=+\frac1{120},\qquad
   \zeta(-5)=-\frac1{252},\qquad
   \zeta(-7)=+\frac1{240}.
   \]
   Also \(\Phi_{12}(3)=3^4-3^2+1=73\), not 137.

4. **The binary code and lattice are misidentified.**
   The W33 adjacency code established elsewhere in the repository is the
   self-orthogonal \([40,16,8]\) code, not a self-dual \([40,20,4]\) code.
   Its scaled Construction-A lattice has determinant \(2^8\), so it is not
   even unimodular or the Leech lattice. Consequently the theta and
   Moonshine claims in `PAPER_SECTION5_MODULAR.tex` and
   `w33_submission.tex` do not follow.

5. **Several displayed numerical formulas do not equal their stated values.**
   Examples in `LIVE_PDG2025_ALIGNMENT_LEDGER.md` include
   \(3/(4\cdot13)=3/52\ne0.3077\),
   \(40/7560\ne0.00385\), and
   \(1-2/3^2=7/9\ne29/30\). The prediction table in
   `w33_submission.tex` similarly labels expressions with unrelated decimal
   values.

6. **The physics scripts search or insert formulas; they do not derive them.**
   Passes 129–140 and 154–156 repeatedly try candidate expressions, insert
   observed constants or expected values, and report proximity. Such output
   may be useful hypothesis generation, but it cannot support “zero free
   parameters,” Standard-Model derivation, uncertainty, or sigma claims.

7. **The formal/computational closure claims fail their own stated boundary.**
   Pass 143 conflates the extended ternary Golay code with a perfect code and
   identifies the wrong anyon theory as Fibonacci-universal. Pass 145 uses
   real matrix rank for a mod-3 claim and references `math` before import.
   Pass 146 prints a Lean sketch without running Lean and starts from the
   false identity \(q!=2^q\) at \(q=3\). Pass 141 includes a trivial Perron
   pole in its “nontrivial” circle test.

8. **The doily subpacket mixes one exact result with invalid downstream
   claims.** The \(K_6\) edge/doily bijection in Pass 71 is useful and exact.
   The claimed CSS parameters in Pass 73 do not follow from the printed
   ranks, and the later constants/QEC/particle interpretations are not
   established by the code.

## What remains usable

- Exact finite-geometry constructions may be retained after independent
  verification, notably the Pass 71 \(K_6\)/doily bijection.
- Exploratory numerical scripts may remain as clearly labelled searches.
- Pass 157 is independent of the submission packet. It uses the established
  W33 adjacency matrix and exact integer/modular arithmetic only.

## Release gate

Do not submit `w33_submission.tex`, use the sigma ledger, or describe Passes
126–156 as theorems until:

- the W33 spectrum, code, lattice, zeta, and cyclotomic data are corrected;
- every observable is separated into **derived**, **fitted**, or
  **post-selected**;
- uncertainty propagation and external data versions are explicit;
- every claimed formal proof is executed by its named prover;
- the submission compiles without generated placeholder sections; and
- an independent claim-to-witness table passes.

The exact mathematical track should be developed separately from the
phenomenology track until those gates close.
