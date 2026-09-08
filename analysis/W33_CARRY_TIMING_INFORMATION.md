# Work, stored content and timing information are different quantities

This packet derives exact laws for the existing counter zipper and constructs
a reversible timing-record eraser. It connects the universal guest's execution
costs to information accounting without identifying software writes with heat.

## Exact preemption cost, including arbitrary starting values

Let `s(x)` count the ones in the binary representation of x, and let k(x) count
its trailing ones. Increment gives `s(x+1)-s(x)=1-k(x)`. The existing zipper
takes `2k(x)+3` ticks and emits `2k(x)+1` verified bit-write operations: k scan
frames, one pivot and k reconstructed digits. Consequently, for L increments
from a, the sums telescope:

\[
 T(a,L)=5L+2s(a)-2s(a+L),\qquad
 W(a,L)=3L+2s(a)-2s(a+L).
\]

From zero, `T(0,M)=5M-2s(M)` and `W(0,M)=3M-2s(M)`. The potential `2s(x)`
therefore makes the amortized microtick cost exactly five. This specializes the
standard binary-counter potential argument, documented in
[MIT's algorithm course](https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/d9a4dadcde8f58811056d4bf5bc403df_final_sol.pdf).
It is not a new amortized-analysis principle.

The repo already owns the macro construction law `2M-s(M)` and the retained
node count M in `W33_AUTHENTICATED_COUNTER_MACHINE.md`, under “Storage reuse is
different from proof work.” Therefore interruptibility adds exactly `M-s(M)`
bit-write operations. It adds **no distinct bit nodes** to this retained
monotone workload: every unary scan stack represents `2^j-1 <= x`, and every
partially reconstructed result is a canonical suffix of `x+1`. Earlier smaller
values already supply those nodes. Only the new full counter value adds one.
This induction assumes retention of all previous nodes and does not apply to
an archive that has collected them.

The actual authenticated backend checks every prefix through M=256:
1278 ticks, 766 bit-write operations and 256 distinct nodes. The prior macro
count is 511; the preemption tax is 255 write operations. Repeated writes of
an existing content-addressed node are counted as work, not fresh allocation.
Another 2080 offset intervals check the telescoping tick law independently.

## An exact timing-observation theorem

Let X be uniform on `0,...,2^n-1`. Execute L=`2^m` ordinary, unbounded increments,
where `0 <= m < n`, and observe **each increment's exact completion tick count**.
No modulo-counter implementation is assumed: n specifies the initial ensemble.
Write the timing transcript as Z. Then

\[
 I(X;Z)=H(Z)=m+2-2^{1-(n-m)}\quad\text{bits}.
\]

Proof: write X=qL+r. Exactly one of `X+1,...,X+L` is divisible by L. Its position
is `L-r`, so the unique timing with carry length at least m identifies r.
That carry length is `m+k(q)`. All other carry lengths are determined by r.
Thus the transcript and the pair `(r,k(q))` determine each other. The low part r
is uniform and independent of q, contributing m bits. Put b=`n-m`. For uniform
b-bit q, the distribution of k(q) is

\[
 P(k=j)=2^{-j-1}\ (0\le j<b),\qquad P(k=b)=2^{-b}.
\]

Summing its entropy gives `H(k)=2-2^(1-b)`, proving the formula. The executable
checks both directions of the sufficient statistic and exact rational entropy
for all 45 `(n,m)` pairs with `1 <= n <= 9`.

One timing leaks fewer than two bits, but **`2^(n-1)` consecutive timings identify
the whole n-bit input**. For n=8, a 128-increment trace identifies X completely.
This concerns an ideal observer of individual completion times; noise, padding,
aggregation, interleaving and access restrictions change the observation model.
It is not a claim that an external observer can read these times on hardware.

Observing only the **total batch duration** gives a different exact law. The
low m bits cancel in the telescoping cost, leaving
`T(X,L)=5L+2k(q)-2`. Hence

\[
 I(X;T(X,2^m))=2-2^{1-(n-m)}.
\]

Discarding the individual completion times removes exactly m bits of observable
information. For n=8,m=7, all 128 completion times identify eight bits, while
their sum reveals only one. All 45 census cases verify this second identity
with exact rational entropy. This is a precise reason to specify which timing
observable an architecture exposes; merely batching instructions does not
establish that intermediate emissions are hidden.

## Physics: an explicit reversible eraser, not a zero-energy assertion

The retained final counter is `Y=X+L`, so X and hence Z can be reconstructed
from Y. Therefore `H(Z|Y)=0`, despite positive `H(Z)` for an observer without Y.
This is realized by a named finite map, not merely an entropy calculation.
Encode the possible transcripts as integer labels c(Z). Define the oracle
`f(Y)=c(trace(Y-L,L))` on valid final values and zero outside that range. Then

\[
 U:(Y,R)\longmapsto(Y,R\mathbin{\mathrm{xor}}f(Y))
\]

is an involutive permutation on the entire finite register space. On the
correlated records `(Y,c(Z))`, it gives `(Y,0)` while preserving Y. For n=5,m=2,
the executable checks all 1024 register states, bijectivity and the inverse,
and all 32 intended record resets. Here `H(Z)=15/4` bits and `H(Z|Y)=0`.
As a permutation of basis states, U also defines a unitary; no coherent device,
efficient circuit synthesis or physical implementation is supplied.

In an ideal classical erasure model, resetting a record without usable side
information has the entropy-dependent lower bound `k_B T ln(2) H(Z)`; retaining
and using Y removes this particular conditional-information lower bound.
That does not remove switching losses, control work, heat from other discarded
records or finite-time costs. The distinction follows
[Bennett's account of reversible computation and erasure](https://arxiv.org/abs/physics/0210005).
The existing `w33_holovm_thermodynamic_ledger.py`, read in full, already warns that
GC payload bytes do not establish physical erasures. This packet adds an exact
correlated timing ensemble and an explicit eraser to that boundary; it does not
retract the older ledger's expressly conditional model.

The computation lesson is that the observer and retained side information are
part of the resource specification. More write operations need not create more
distinct content, and a record informative to one observer may be reversibly
reset by an owner holding correlated state. Future physical experiments need
to specify that state and observation model before assigning an erasure cost.

## Reproduce and scope

```sh
python analysis/w33_carry_timing_information.py
```

This regenerates `w33_carry_timing_information_certificate.json`; all checks pass.
The proof applies to this zipper's tick semantics and the stated uniform
ensemble. It is not a universal law of arbitrary programs or a measured energy
advantage. Corpus searches by formulas and result terms found the prior macro
popcount law and unrelated compressed-payload hits; the prior law is cited
above. No worldwide novelty claim is made. Full history/manuscript intake is
still incomplete. The separate durable owner was published as `f6b916191`.
