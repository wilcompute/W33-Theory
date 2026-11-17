#!/usr/bin/env python3
"""Idempotently rewrite the live Holonet blueprint for Passes 2953--2959.

This is deliberately not an append-only integrator. It replaces the compiler-shell
classification, repairs the three-copy scope, sharpens the readout thermodynamics, adds
the actual Bayesian observer, and inserts the hardware evidence gate. Every replacement
is fail-closed against source drift.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "holonet_machine_blueprint.tex"
INPUT = r"\input{analysis/BT2953_BT2959_seven_front_closure_insert}"
LEDGER = "% =====================================================================================\n\\section{The complete ledger}"


def replace_once(text, old, new, label):
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected one exact anchor, found {count}")
    return text.replace(old, new, 1)


def replace_environment(text, starts, new, label):
    if new.strip() in text:
        return text
    start = next((candidate for candidate in starts if candidate in text), None)
    if start is None:
        raise AssertionError(f"{label}: no accepted start marker")
    index = text.index(start)
    end = text.find(r"\end{spec}", index)
    if end < 0:
        raise AssertionError(f"{label}: missing end marker")
    end += len(r"\end{spec}")
    return text[:index] + new + text[end:]


def insert_before_once(text, anchor, insertion, marker, label):
    if marker in text:
        return text
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(f"{label}: expected one anchor, found {count}")
    return text.replace(anchor, insertion + anchor, 1)


def patch(text):
    # Preserve any later parallel pass frontier rather than lowering it.
    text = re.sub(r"Passes 2700--(\d+)", lambda m: f"Passes 2700--{max(int(m.group(1)), 2959)}", text, count=1)

    compiler_new = r'''\begin{spec}[What the worst case actually is, Passes 2885, 2923 and 2953]
Only $188$ of $4{,}199{,}040$ transformations sit at directed distance $19$.  The safe
Pass~2923 description split them into $25$ algebraic profiles without calling those
profiles conjugacy classes.  Explicit closure under conjugation by the full affine group
now gives the actual answer:
\[
  \boxed{12\text{ conjugacy classes intersect the terminal shell}.}
\]
Their shell intersections are
\[
2,22,6,6,4,6,6,4,2,8,12,110,
\]
and the corresponding full class sizes sum to $2{,}730{,}348$.  The dominant shell
contribution is one order-four class: full size $43{,}740$, centralizer order $96$, and
$110$ of the $188$ hard elements.  Thus the earlier $25$ profiles were a strict
\emph{over-refinement}, exactly as their evidence boundary warned.

\smallskip\noindent
The fixed-point incidence of the shell supplies a second exact structure.  Its ternary
Fourier transform on $\mathbb F_3^4$ has support $79/81$.  The only zero characters are
$(0,1,0,0)$ and $(0,2,0,0)$, so hard-shell fixed incidences split exactly
$60+60+60$ across the three $z_p$ slices.  A hoped-for sparse $15/24/40/81$ Hodge or code
identification is refuted; a precise past-phase balance survives.

\smallskip\noindent
All $188$ elements remain a complete compiler regression fixture.  Conjugacy explains
which algebraic species occur; it does not make the directed word metric conjugacy
invariant.
\end{spec}'''
    text = replace_environment(
        text,
        [
            r"\begin{spec}[And what the worst case actually looks like, Pass 2885]",
            r"\begin{spec}[And what the worst case actually looks like, Passes 2885 and 2923]",
        ],
        compiler_new,
        "terminal-shell rewrite",
    )

    chirality_anchor = r"\subsection{Why the first ``no'' could not have been the last word}"
    chirality_insert = r'''\begin{spec}[What one copy can and cannot tell, Passes 2919, 2954 and 2959]
The two middle twelve-ray classes are exchanged by complex conjugation, but their uniform
one-copy ensembles are both exactly $I_4/4$.  Their trace distance is zero: \textbf{no
class-blind one-copy POVM can identify which middle class an unknown uniformly drawn ray
came from.}

If the conjugate pair---equivalently the ray frame---is known, the problem changes.  Every
pair has $|\langle\psi|\bar\psi\rangle|^2=1/3$, so perfect one-shot discrimination is still
impossible, but the optimal success probability is
\[
  p_{\rm Helstrom}=\frac{1+1/\sqrt3}{2}=0.788675\ldots .
\]
No single fixed Pauli covers all twelve pairs.  The minimum local cover is
$\{Y\otimes I,I\otimes Y\}$: one selector bit chooses the qubit, then $S^\dagger$, $H$,
and an ordinary $Z$ readout perform the measurement.  No entangler is required.

The ray phase label $s=\mu+\nu\pmod3$ is $1$ on one middle class and $2$ on the other.
Conjugation is $s\mapsto-s$, exactly the reflection already carried by the $D_{12}$ mirror
on its $C_3$ phase subgroup.  The controller map
$(s,m)\mapsto((-1)^m s,m)$ is reversible.  This is metadata transport, not a physical
antiunitary gate on an unknown state.
\end{spec}

'''
    text = insert_before_once(text, chirality_anchor, chirality_insert,
                              "What one copy can and cannot tell", "chirality insertion")

    old_threecopy = r'''\begin{plain}
So the road forward is narrower and clearer than it was. Two copies are provably not
enough. Super-linear distillation of these states needs three or more copies, or
operations from outside the stabilizer set --- and \S\ref{sec:magic} already reports that
a search for a three-copy advantage found no witness either. This document states that as
the open problem it is, rather than as a promise.
\end{plain}'''
    new_threecopy = r'''\begin{gotwrong}[The three-copy question was asked twice, and the first formulation was wrong]
Pass~2910's factor-wise set-cover code instantiated ray $0$, which belongs to the
\emph{shallow} four-ray class, not the deep engineering target.  It also required every
single-error vector to be rejected.  That condition is sufficient for quadratic
suppression but not necessary: an accepted fault may land collinearly on the accepted
clean logical ray.
\end{gotwrong}

\begin{spec}[Complete three-copy CSS closure, Pass 2956]
Every six-qubit CSS rank-four stabilizer subspace and all sixteen syndromes were exhausted:
\[
43{,}617\text{ CSS subspaces},\qquad697{,}872\text{ projectors}.
\]
There are $54$ projectors for which all accepted single errors are collinear with the
accepted clean vector---the missing mechanism the rejection-only search could not see.
All $54$ clean logical lines are stabilizer lines, however, and none closes on the deep
$M_{36}$ Clifford orbit.

Among $67{,}023$ branches whose clean output \emph{does} close on the deep orbit,
\[
  \boxed{\min\frac{dp_{\rm out}}{dp}\bigg|_{p=0}=1},
\]
attained by $3{,}087$ branches.  The best pure-state success probability among them is
$1/4$, hence twelve raw inputs per accepted output.  An explicit branch has
$q(p)=(2-p)^2/16$ and $p_{\rm out}=p$: it is exactly an identity channel on the noise
parameter.
\end{spec}

\begin{plain}
So three copies do reveal a new stabilizer mechanism, but not a useful deep-magic
protocol.  The exact negative result is CSS-scoped.  The full family of general isotropic
six-qubit $[[6,2]]$ stabilizer subspaces has $213{,}648{,}435$ members and remains open;
operations outside the stabilizer set remain open as well.
\end{plain}'''
    text = replace_once(text, old_threecopy, new_threecopy, "three-copy correction")

    old_readout = '''A support readout throws information away --- that is what ``lossy'' means. Landauer's
principle says throwing information away has an unavoidable energy cost, and here the
cost is exactly computable, because the fibres are exactly known: a mask of weight $k$
has exactly $2^k$ preimages, and there are $\\binom{4}{k}$ such masks.'''
    new_readout = '''A support measurement can be performed reversibly if both the frame and its measurement
record are retained.  Landauer applies when a named representation is reset.  The exact
fibres separate the phase information discarded by replacing a frame with support, the
entropy of the support record itself, a compressed exact identification transcript, and
an implementation's uncompressed stream of snapshots.'''
    text = replace_once(text, old_readout, new_readout, "Landauer scope repair")

    old_landauer_start = r"\begin{spec}[Landauer, at room temperature]"
    new_landauer = r'''\begin{spec}[Representation-specific Landauer floor]
For a uniform frame, $H(X\mid S)=8/3$ bits is the phase information discarded when the
full frame is replaced by its support.  It is \emph{not} the entropy of the support
record, which is $H(S)=3.673183$ bits, and not the minimum exact frame transcript,
$H(X)=\log_2 81=6.339850$ bits.  At $300\,$K the corresponding erasure floors are
$7.656\times10^{-21}$, $1.055\times10^{-20}$, and $1.820\times10^{-20}$ joules.

These are floors for resetting the named records.  They are not detector-energy or CMOS
predictions, and a reversible measurement that retains all records pays no logical-erasure
cost at that stage.
\end{spec}'''
    text = replace_environment(text, [old_landauer_start,
                                     r"\begin{spec}[Representation-specific Landauer floors, Passes 2836 and 2920]"],
                               new_landauer, "Landauer table rewrite")

    rank_anchor = r"\begin{spec}[Measured on UP5K SG48; the per-instruction breakdown]"
    rank_insert = r'''\begin{spec}[The seven-bit rank engine: theorem closed, silicon verdict pending, Pass 2957]
The radix-three code $27x_p+9z_p+3x_f+z_f$ stores all $81$ frames in seven bits and its
four operation tables close all $324$ state/opcode transitions.  That saves one stored
bit relative to four two-bit trits.  It does \textbf{not} imply a smaller execution core:
decode and re-encode logic may cost more than the saved flip-flop.

The same-harness RTL and report parser are source-complete.  The placement jobs remain in
the repository-wide runner queue, so no new LC or timing number is printed here.  The
mechanical decision rule is: replace the execution core only if rank coding wins area
without violating timing; otherwise use it, at most, as compressed context memory.
\end{spec}

'''
    text = insert_before_once(text, rank_anchor, rank_insert,
                              "The seven-bit rank engine: theorem closed", "rank hardware gate")

    observer_anchor = r"\subsection{Enforcing the law in the netlist}"
    observer_insert = r'''\begin{spec}[The observer should optimize actions, not inherit them, Pass 2955]
The minimum-depth noiseless tree was evaluated under a coordinate-asymmetric detector
channel with $c(F_p)=c(Z_p)=1$ and $c(\mathrm{CX})=2$.  It gives aggregate error
$5.869\%$ at expected action cost $4.963$.

An exact horizon-four posterior dynamic program may stop or choose a new operation at
every belief.  At terminal-error weight $100$ it gives
\[
  \text{error}=1.689\%,\qquad \mathbb E[c]=4.927.
\]
The error falls by about $71\%$ while action cost also falls slightly.  This is not a
repetition code placed on the old tree: root operations, later operations, and stopping
are re-optimized.  The result is exact for the stated synthetic channel, horizon, known
initial support and action costs; it is not an infinite-horizon or laboratory-calibrated
optimum.
\end{spec}

'''
    text = insert_before_once(text, observer_anchor, observer_insert,
                              "The observer should optimize actions", "Bayesian observer insertion")

    if INPUT not in text:
        if text.count(LEDGER) != 1:
            raise AssertionError("release ledger anchor drift")
        text = text.replace(LEDGER, INPUT + "\n\n" + LEDGER, 1)
    return text


def main():
    original = BLUEPRINT.read_text(encoding="utf-8")
    migrated = patch(original)
    if patch(migrated) != migrated:
        raise AssertionError("migration is not idempotent")
    if migrated != original:
        BLUEPRINT.write_text(migrated, encoding="utf-8")
        print("changed")
    else:
        print("already integrated")


if __name__ == "__main__":
    main()
