# Five computational frontiers: radix, noise, workloads, circuits and physics

This extends `W33_CARRY_TIMING_INFORMATION.md` (025d44bc0). The important
connection is operational: **the information needed to undo a record depends
on how that record was produced**. Exact timing can be reconstructed from the
final counter. Independent measurement noise cannot. We supply executable
models, proofs and a gate list, with physical calibration still open.

## 1. Radix changes both work and information

For radix b, let s_b(x) be the digit sum and k_b(x) the number of trailing
(b-1) digits. Then

    s_b(x+1)-s_b(x) = 1-(b-1)k_b(x).

An abstract digit zipper with k scan ticks, one pivot tick, k unwind ticks,
one close tick and one commit tick has the exact cost

    T_b(a,L) = 3L + 2[L+s_b(a)-s_b(a+L)]/(b-1).

The potential 2s_b/(b-1) gives amortized cost 3+2/(b-1): five for binary,
four for ternary. This counts abstract digit ticks. A trit operation can cost
more physically than a bit operation; no energy advantage follows. The code
executes the digit rewrite, not only the closed formula, and checks 6144
intervals across radices 2,3,4,5. The authenticated VM remains binary.

For uniform X in 0..b^n-1 and L=b^m increments, 0<=m<n, write X=qL+r and d=n-m.
The timing transcript is equivalent to (r,k_b(q)): the unique carry of length
at least m occurs at position L-r; all other carries are determined by r.
This also covers m=0, when the transcript has a single element. The carry law is

    P(k=j)=(b-1)/b^(j+1), j<d; P(k=d)=b^(-d).
    h_b(d)=(1-b^(-d))*[b*log2(b)/(b-1)-log2(b-1)].
    H(individual timings)=m*log2(b)+h_b(d).
    H(total duration)=h_b(d).

The entropy formula follows by summing the truncated geometric distribution.
For the total duration, substitute the digit-sum change of q into the cost law:

    T_b(X,b^m)=3b^m+2[(b^m-1)/(b-1)+k_b(q)].

Thus the aggregate is an injective function of k_b(q). The executable checks
both directions of transcript equivalence and both entropies in 40 ensembles.
Probability multiplicities are exact; logarithms use floating arithmetic.

Unlike binary, a b^(n-1)-increment trace need not identify the entire input.
For ternary it leaves **2/3 bit** of input uncertainty: the top trit is separated
into {2} and {0,1}, not three individual values. These are classical trits; a
coherent qutrit circuit and its physical control costs are not established.

## 2. Noise hides input and creates a different erasure problem

Let Z be the exact timing vector, Y=X+L the final counter, and O=Z+E the
observed vector, with independent additive errors E. For a finite error alphabet,

    H(O|Y)=H(E), and I(X;O)=H(O)-H(E).

Proof: Y determines X and Z. For any fixed Y, translation by Z is a bijection
between E and O. Independence makes its conditional entropy H(E). Since X and
Y determine one another, the mutual-information identity follows. For L
independent errors, H(E)=L H(E_1).

Our explicit channel uses per-timing jitter {-2,0,2} ticks with probabilities
{1/4,1/2,1/4}. These are modeled measurement errors, not calibrated hardware
noise. A second layer adds another independent copy; data processing predicts
that leakage cannot increase. Exact rational joint-distribution enumeration
checks normalization and computes the following information in bits for n=3:

| Timings | Exact | One jitter layer | Two jitter layers |
|---|---:|---:|---:|
| 1 | 1.750000 | 0.808965 | 0.526194 |
| 2 | 2.500000 | 1.364110 | 0.931244 |
| 4 | 3.000000 | 2.005035 | 1.526319 |

One jitter sample has 1.5 bits of entropy. Four samples therefore leave six
bits of record entropy even for an owner holding Y. The exact-record eraser
cannot reset those errors without additional side information. In an ideal
symmetric, isothermal memory model, discarding this noise record incurs the
corresponding conditional-information erasure bound. This is not a measurement
of heat, nor a claim that noise generation itself must dissipate that amount.
Keeping a reversible noise seed, or never retaining the noisy record, changes
the accounting. Discarding a physical environment carrying the seed also changes
which system boundary must be considered.

## 3. Mixed workloads expose a representation limit

For a nonzero move across the edge joining u-1 and u, either INC or DEC costs
3+2*v2(u), where v2 counts trailing zero bits. DEC on zero is a one-tick no-op.
Consequently, for any valid path,

    T = (#zero DEC) + 3*(#moves) + 2*sum_u crossings(u)*v2(u).

Unlike a monotone run, this depends on the path's edge-crossing multiplicities,
not just its endpoints. The actual authenticated verifier checks 256 five-step
paths starting at 0..7, including repeated zero decrements.

The cycle (2^k-1) -> 2^k -> (2^k-1) costs exactly **4k+6 ticks** and **4k+1
bit-write operations**, checked for k=0..16. The missing decrement pivot write
comes from removing the leading one rather than constructing a noncanonical
leading zero. For k=16 this is 70 ticks and 65 writes, despite returning to the
same value. This extends the already documented macro alternation example in
`W33_AUTHENTICATED_COUNTER_MACHINE.md`; alternation itself is not newly discovered.

No potential depending only on counter state can assign both operations a
uniform constant amortized tick cost: its changes cancel on this cycle, whose
cost grows without bound with k. This is a limit of this representation and
instruction schedule, not a limit on universal computation. Redundant signed
digits or a lazy arithmetic representation could change the cost model, but
would require new canonicalization, equality and authenticated-memory rules.

## 4. A linear circuit replaces the lookup eraser

The previous eraser explicitly named a finite permutation but used a lookup
oracle. We now synthesize only NOT, CNOT and Toffoli gates, with clean ancillas.
Use the sufficient-statistic record (r,k) rather than a lexicographic transcript
label; both encode exactly the same timing information.

Set d=n-m. On valid final counters, floor(Y/2^m)=q+1, so

    r = Y mod 2^m; k = v2(floor(Y/2^m)).

For j=1..d, compute t_j, the AND of the complemented lowest j bits of this high
part. This is a prefix chain on d clean ancillas. Then k=sum_j t_j. Its binary
bit ell is XOR of t_j over j divisible by 2^ell: successive integer counts
toggle that bit exactly at those thresholds. CNOT these bits and r into the
record, then run the prefix computation backwards. The input and ancillas are
restored, while the record is XORed with the timing statistic.

The construction defines a total reversible circuit: outside the valid Y
ensemble, k is the zero-prefix count capped at d. It does not use the older
oracle's arbitrary zero extension on invalid Y. Its valid erasure behavior is
the same, with a different explicitly documented encoding.

Exact gate counts are

    NOT: 2d; Toffoli: 2(d-1);
    CNOT: m+2+2d-popcount(d);
    clean ancillas: d; record width: m+bit_length(d).

Thus circuit size is linear in n, even though a full timing transcript can have
2^m entries. For n=5,m=2: **6 NOT, 8 CNOT, 4 Toffoli**, three clean ancillas and
four record bits. The certificate includes the complete gate list. All Y and
record inputs are checked with clean ancillas for 28 sizes n=1..7,m<n,
including invalid Y; inverse restoration and all intended resets are checked.
Every elementary gate is itself a permutation even on dirty ancillas, but the
stated oracle requires their clean initialization. This is not a gate-optimality
claim. Standard reversible-gate machinery is prior work:
[Barenco et al., Elementary gates for quantum computation](https://arxiv.org/abs/quant-ph/9503016).

## 5. Connection to experimental work, with source provenance

[Jun, Gavrilov and Bechhoefer (2014), Table I](https://www.sfu.ca/chaos/assets/papers/2014/prl14-reprint.pdf)
reports fitted asymptotic work of 0.71 +/- 0.03 kBT for full erasure and
0.05 +/- 0.03 kBT for a no-erasure control. The full-erasure value differs from
ln(2) by 0.562 reported uncertainty units. These are measurements of a colloidal
feedback-trap protocol extrapolated to slow operation, not Holonet measurements.
The certificate records the source, table, manually transcribed fitted values,
and the absence of raw trajectories. We do not transfer the experiment's
finite-time coefficients to the VM.

For the previous 3.75-bit exact record, the ideal unconditioned entropy bound
at an assumed 300 K is 1.076617e-20 J. With usable Y, its conditional-information
bound is zero. The noisy-record theorem above identifies precisely when that
zero ceases to apply. Neither number predicts switching losses or total system
energy. A Holonet measurement still requires device data; local powercap exposed
no energy counters, and `w33_accelerator_calibration_request.py` supplies an
unfilled physical-evidence contract, not calibration. Work also must not be
silently equated with heat without accounting for internal-energy changes.

## Parallel changes: negativity has a computational interpretation

GitKraken found W33 unchanged since 025d44bc0 and four new Holotrade commits,
3aa3ad6, e62261f, 1075622 and 66062ec. Their mass-16 census, inherited-orbit split,
depth and indecomposability certificates concern load profiles; tau_2 remains
open. We read the new sources and certificates without rerunning the long
censuses. Per decision-17889096, depth and indecomposability distinguish different
properties; neither proves blocker existence.

There is a direct algebraic connection worth preserving. Since each pencil has
four lines, N^T x=e and sum(e)=4k imply sum(x)=k. Therefore

    min_{integer N^T x=e} ||x||_1 = k + 2*depth(e).

This follows from ||x||_1=sum(x)+2*sum max(0,-x_p), not from a new solver run.
For normalized signed pencil coefficients x/k, the minimum l1 norm is
1+2*depth/k. Sampling pencils with probability proportional to |x_p| gives an
unbiased signed estimator for any bounded line observable: sample a uniform
line of that pencil and multiply the observable by sign(x_p)*||x||_1/k.
For observables bounded by one, its second moment is at most (||x||_1/k)^2.
The reported mass-12 depth-one class gives 25/9; inherited mass-16 depth-one
classes give 9/4; the mass-16 depth-two class gives 4. These are bounds for this
specified integer-pencil sampler, not optimal variances, quantum magic, or
hardware overhead. A fractional decomposition may have a different optimum.
The general connection between signed sampling and l1 weight is prior work;
see [Pashayan, Wallman and Bartlett](https://arxiv.org/abs/1503.07525).
Here the specialization is to integer pencil preimages, not a quantum circuit.
The depth-one/two solver's [-60,60] box does not exclude a better solution:
any candidate with negativity D<=2 has every coordinate between -D and k+D.
The certificate does not store coordinate witnesses, so executable sampling
of those particular orbits still needs their preimages exported.

## Reproduction and limits

    python analysis/w33_computation_resource_frontiers.py

The generated `w33_computation_resource_frontiers_certificate.json` covers all
five targets. Result/formula searches checked the existing macro, carry,
thermodynamic and hardware-contract material, the result index, and the new
Holotrade depth work. No worldwide novelty claim is made. The original full
three-day history and recursive manuscript intake remains incomplete. This
packet establishes mathematical and executable progress, not a completed
physical computer or a measured Holonet dissipation advantage.
