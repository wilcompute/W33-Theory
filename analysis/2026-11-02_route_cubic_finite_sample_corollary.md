# Finite-sample cubic tomography of the 216 route carrier

**Scope:** classical sampling theorem on the finite W33 route-code oracle. No assumption of simultaneously measurable noncommuting quantum observables.

The exact integer reconstruction in `analysis/w33_20261102_route_216_cubic_tomography.py` says that for each distinct W33 triple `a,b,c`, a uniformly random one of the 216 route supports gives the sign product `X=Z_sa Z_sb Z_sc\in\{-1,1\}` with mean

* `1/2` when `a,b,c` lie on a W33 line;
* at most `1/18` otherwise (actual other means `1/18,0,-1/9,-2/9`).

Thus the threshold `5/18` separates the two classes with margin `2/9`. There are `C(40,3)=9,880` triples. Draw `n` independent uniformly distributed route supports, reusing their entire 40-coordinate sign labels to evaluate every triple. Hoeffding's inequality followed by a union bound gives

\[
\Pr(\text{at least one wrongly classified triple})
\le 2{40\choose3}\exp(-2n/81).
\]

Consequently `n=588` route-support samples guarantee **at least 99% simultaneous classification probability** under the ideal iid classical oracle model. The estimator does not require all 216 possible supports to be sampled.

For an explicitly specified *independent symmetric sign-flip channel* on each sampled coordinate with probability `epsilon<1/2`, every cubic mean is attenuated by `(1-2 epsilon)^3`. The threshold and margin must be attenuated correspondingly, so a sufficient budget is

\[
n\ge\left\lceil \frac{81}{2(1-2\epsilon)^6}
\log\frac{2{40\choose3}}{\delta}\right\rceil .
\]

`analysis/w33_20261102_route_cubic_sampling_budget.py` computes and checks this budget (including a 5% independent bit-flip control). The result is distribution-free beyond the specified uniform iid support sampling and independent flip channel. Arbitrary correlated noise does not inherit this bound.

**Physical firewall:** the 40 labels of a route support are *classical incidence data*, not a claim that 40 incompatible quantum outcomes are jointly accessible from one photon or shot. A quantum tomography proposal requires an explicit state preparation and joint-measurement-compatible POVM/instrument model before interpreting `n=588` as a laboratory photon count. This is an operational complexity certificate for a classical oracle, not a quantum resource estimate.
