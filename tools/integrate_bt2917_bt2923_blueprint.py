#!/usr/bin/env python3
"""Idempotently integrate Passes 2917--2923 into the live Holonet blueprint.

The migration is fail-closed. It refuses to run if the current blueprint no longer
contains the exact theorem anchors whose interpretation is being repaired.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BLUEPRINT=ROOT/'holonet_machine_blueprint.tex'
INPUT=r'\input{analysis/BT2917_BT2923_seven_front_breakthrough_insert}'
LEDGER='% =====================================================================================\n\\section{The complete ledger}'

def replace_once(text,old,new,label):
    if new in text:return text
    count=text.count(old)
    if count!=1:raise AssertionError(f'{label}: expected exactly one anchor, found {count}')
    return text.replace(old,new,1)

def replace_block(text,start,end,new,label):
    if new.strip() in text:return text
    i=text.find(start)
    if i<0:raise AssertionError(f'{label}: start anchor missing')
    j=text.find(end,i+len(start))
    if j<0:raise AssertionError(f'{label}: end anchor missing')
    j+=len(end)
    return text[:i]+new+text[j:]

def patch(text):
    # Never lower a later parallel pass frontier.
    text=re.sub(r'Passes 2700--(\d+)',lambda m:f"Passes 2700--{max(int(m.group(1)),2923)}",text,count=1)

    old_head=r'''\headline{The linear rate $2/3$ is not a property of the branch that was found. It is a
\emph{bound on the entire two-copy stabilizer family}.}'''
    new_head=r'''\begin{spec}[The missing first-order census, Pass 2918]
The no-quadratic theorem above excludes slope zero but does not, by itself, prove that
$2/3$ is the smallest positive slope.  Enumerating every closed branch supplies the
missing implication:
\[
\begin{array}{c|r|r|c}
\text{class} & \text{closed} & \text{improving} & \min dp'/dp\\\hline
4\text{-ray shallow} & 2302 & 0 & 1\\
12\text{-ray middle A} & 964 & 0 & 1\\
12\text{-ray middle B} & 964 & 0 & 1\\
8\text{-ray deep} & 3393 & 48 & \mathbf{2/3}
\end{array}
\]
Twelve deep branches attain $2/3$; the other thirty-six improving branches have
$2-2\sqrt3/3\approx0.845299$.  For any randomized accepted-output mixture,
$a_{\rm mix}=\sum_jw_jq_{0,j}a_j/\sum_jw_jq_{0,j}$, a success-weighted convex
combination.  Mixing cannot beat $2/3$ or cancel the linear term.
\end{spec}

\headline{The $2/3$ rate is the global minimum of the full two-copy $[[4,2]]$
stabilizer-projector family.  That statement now follows from the first-order census,
not merely from the absence of a quadratic branch.}'''
    text=replace_once(text,old_head,new_head,'M36 slope reasoning')

    middle_anchor=r'\subsection{Why the first ``no\'\' could not have been the last word}'
    middle_insert=r'''\begin{spec}[What distinguishes the two middle classes, Pass 2919]
Complex conjugation exchanges the two twelve-ray classes and fixes the shallow and deep
classes setwise.  Their complete probability spectra against all $60$ stabilizer states
are identical, so no probability-only overlap statistic separates them.  In a fixed
Pauli frame every expectation containing an odd number of $Y$ factors reverses sign,
while every even-$Y$ expectation agrees.  The missing datum is antiunitary phase
chirality, not another fidelity score.
\end{spec}

'''
    if 'What distinguishes the two middle classes, Pass 2919' not in text:
        if text.count(middle_anchor)!=1:raise AssertionError('middle-class insertion anchor drift')
        text=text.replace(middle_anchor,middle_insert+middle_anchor,1)

    line_anchor=r'''\begin{plain}
Which is a satisfying place to end up.'''
    line_insert=r'''\begin{spec}[Outside-box falsifier, Pass 2922]
The tempting next guess is that the chosen classical line itself induces the
$4+8+12+12$ Clifford partition.  It does not.  The full order-$1296$ setwise line
stabilizer is transitive on all $36$ magic points.  Its order-$54$ pointwise stabilizer
has four orbits of size $9$, exactly the coordinate families.  The Clifford classes
therefore require the additional complex/Pauli phase structure; they are not suborbits
of the finite geometry with one line marked.
\end{spec}

'''
    if 'Outside-box falsifier, Pass 2922' not in text:
        if text.count(line_anchor)!=1:raise AssertionError('line-stabilizer insertion anchor drift')
        text=text.replace(line_anchor,line_insert+line_anchor,1)

    diameter_start=r'\begin{spec}[And what the worst case actually looks like, Pass 2885]'
    diameter_new=r'''\begin{spec}[And what the worst case actually looks like, Passes 2885 and 2923]
Only $188$ of $4{,}199{,}040$ elements sit at distance exactly $19$.  The full shell now
has an objectwise algebraic census: $25$ profiles with affine orders
\[
4^{110},\;5^6,\;6^2,\;8^{22},\;9^2,\;10^6,\;12^{32},\;18^8.
\]
Exactly $174$ fix one frame, $12$ fix none, and $2$ fix three.  Directed inversion is
asymmetric: inverse depths are $16^{18},17^{46},18^{48},19^{76}$, so only $76$ hardest
elements have hardest inverses.

The negative conclusion of Pass 2885 survives and sharpens: the shell is not one
nameable species.  The positive engineering conclusion survives too: all $188$ belong
in the compiler regression fixture.  The $25$ profiles are not called conjugacy classes
without a separate conjugacy calculation.
\end{spec}'''
    text=replace_block(text,diameter_start,r'\end{spec}',diameter_new,'diameter-shell refinement')

    old_plain='''A support readout throws information away --- that is what ``lossy'' means. Landauer's
principle says throwing information away has an unavoidable energy cost, and here the
cost is exactly computable, because the fibres are exactly known: a mask of weight $k$
has exactly $2^k$ preimages, and there are $\\binom{4}{k}$ such masks.'''
    new_plain='''A support measurement need not erase anything if the full frame and the measurement
record are retained reversibly.  Landauer applies when a named representation is reset.
The exact fibres let us distinguish four costs that earlier wording compressed into the
phrase ``a support readout'': discarding phase, erasing the support record, erasing a
compressed exact identification transcript, and resetting an uncompressed stream of
raw support snapshots.'''
    text=replace_once(text,old_plain,new_plain,'Landauer plain-language repair')

    land_start=r'\begin{spec}[Landauer, at room temperature]'
    land_new=r'''\begin{spec}[Representation-specific Landauer floors, Passes 2836 and 2920]
For a uniform frame at $300\,$K:
\[
\begin{array}{l|c|c}
\text{irreversibly erased record} & \text{entropy} & k_BT\ln2\text{ floor}\\\hline
\text{phase after retaining support} & H(X\mid S)=8/3 & 7.656\times10^{-21}\,\mathrm{J}\\
\text{support outcome} & H(S)=4\log_2 3-8/3 & 1.055\times10^{-20}\,\mathrm{J}\\
\text{compressed exact frame transcript} & H(X)=\log_2 81 & 1.820\times10^{-20}\,\mathrm{J}\\
\text{naive adaptive four-bit snapshots} & 4(1+94/27)=484/27 & 5.146\times10^{-20}\,\mathrm{J}
\end{array}
\]
The old $8/3$-bit number is specifically the conditional phase information lost when the
full frame is replaced by support.  It is not the entropy of the support record and not
the reset cost of an adaptive raw transcript.  Every number above is a lower bound for
erasing the named record, not a detector-energy measurement.
\end{spec}'''
    text=replace_block(text,land_start,r'\end{spec}',land_new,'Landauer specification repair')

    text=replace_once(text,
      r"\textbf{All of this machine's irreducible dissipation is in readout.} That is not a",
      r"\textbf{Bijective logical compute has zero Landauer floor; irreversibility enters when a readout, transcript, or routing record is reset.} That is not a",
      'compute/readout thermodynamic scope')

    support_anchor=r'\subsection{Enforcing the law in the netlist}'
    support_insert=r'''\begin{spec}[Storage and noisy diagnosis are different codes, Passes 2917 and 2920]
A seven-bit radix-three rank stores all $81$ execution frames losslessly and closes all
$324$ state/opcode transitions.  This does not contradict the eight-support-tap lower
bound: rank is an internal state code, while support taps identify the state through
observations.  The rank engine's area and timing await observed synthesis against the
measured $43$-cell arithmetic engine.

\smallskip\noindent
The adaptive observer is rebuilt at worst depth $4$ and uniform mean $94/27$.  Under
independent asymmetric support-bit models, exact repeated-count maximum-likelihood
routing with three samples per decision reduces modelled end-to-end error from
$12.58\%$ to $0.765\%$ for symmetric $2\%$ flips and from $27.94\%$ to $2.48\%$ in a
loss-dominated stress profile, at exactly triple raw readout cost.  These are complete
finite-channel sums, not detector calibration or a globally optimal noisy policy.
\end{spec}

'''
    if 'Storage and noisy diagnosis are different codes, Passes 2917 and 2920' not in text:
        if text.count(support_anchor)!=1:raise AssertionError('support-code insertion anchor drift')
        text=text.replace(support_anchor,support_insert+support_anchor,1)

    if INPUT not in text:
        if text.count(LEDGER)!=1:raise AssertionError('release-ledger insertion anchor drift')
        text=text.replace(LEDGER,INPUT+'\n\n'+LEDGER,1)
    return text

def main():
    original=BLUEPRINT.read_text(encoding='utf-8')
    migrated=patch(original)
    if migrated!=original:BLUEPRINT.write_text(migrated,encoding='utf-8')
    if patch(migrated)!=migrated:raise AssertionError('migration is not idempotent')
    print('changed' if migrated!=original else 'already integrated')
if __name__=='__main__':main()
