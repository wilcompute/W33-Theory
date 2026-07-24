# Passes 681–685 — rigidity, branch separation, waveform optics, anytime dropout, and symbolic control

## Pass 681 — Exact degree-one rigidity of the actual W33 homology module

Let

\[
V=H_1(W(3,3);\mathbf F_2),\qquad \dim V=81,
\]

with its explicit \(PSp(4,3)\cong U_4(2)\) action. Two generated matrices act on
\(V\), and seven explicit group relations impose rank \(6562\) on the
\(2\cdot81^2=13122\)-parameter crossed-homomorphism system. Thus

\[
\dim Z^1=13122-6562=6560.
\]

The simultaneous centralizer is the scalar line, so

\[
\dim B^1=81^2-1=6560.
\]

Therefore

\[
\boxed{H^1(PSp(4,3),\operatorname{End}(V))=0.}
\]

This conclusion does not require the seven relations to be presented as a complete
presentation: principal coboundaries satisfy all relations, while the selected-relation
kernel already has exactly the coboundary dimension. Any omitted relations can only
shrink that kernel, so the true cocycle space is squeezed to equality with \(B^1\).

In degree two, odd dimension splits the scalar line from traceless endomorphisms.
The group is perfect and its Schur multiplier has order two, yielding a canonical
scalar

\[
H^2(PSp(4,3),\mathbf F_2)\cong\mathbf F_2
\]

summand inside \(H^2(PSp(4,3),\operatorname{End}(V))\). The traceless degree-two
sector remains open and is not declared zero.

## Pass 682 — Flat-block/H1 one-branch separation after the cyclotomic correction

On the integral W33 edge-chain complex define the signed-turn operator \(K\). Its
exact spectrum is

\[
-6^{81},\qquad 2^{120},\qquad 4^{24},\qquad 10^{15}.
\]

The homology lattice is exactly the \(-6\)-eigenspace. Under

\[
S=K+6I,
\]

it realizes only the \(M_0\) branch of the abstract \(q=3\) order

\[
\mathbf Z_3[S]/(S(S-6)).
\]

The companion \(M_6\) branch would require a zero eigenvalue of \(K\), but \(K\)
is invertible.

This release incorporates the parallel Pass 676 correction rather than ignoring it:
over \(\mathbf Z[\zeta_3]\), the real two-branch flat-block gluing has invariant
factors

\[
[6,6,3,3]
\]

and \(3\)-primary rank four. None of that interface is internal to the one-branch
W33 \(H_1\) eigenspace. The result is therefore a separation theorem, not a claim
that the cyclotomic correction collapses to one \(\mathbf Z/3\).

## Pass 683 — Waveform-level optical memory falsifier

The phase protocol is simulated in all \(256\) time bins for each output pair with:

- correlated AR(1) phase diffusion;
- finite-bandwidth phase switching and ringing;
- coherent second-harmonic multiphoton amplitude;
- coherent neighbor-mode leakage;
- detector recovery memory;
- saturation hysteresis;
- unequal efficiencies, insertion losses, and background counts.

A balanced \(0,\pi/2,\pi/2,0\) schedule with settling guards and a four-parameter
waveform regression gives

\[
q_{0.95}^{\rm balanced}=0.0480385\text{ rad},
\]

versus

\[
q_{0.95}^{\rm blocked}=0.0592699\text{ rad},
\]

a \(18.95\%\) improvement. A memoryless envelope is measurably optimistic. The
joint-stress scan passes through \(1.75\) and first fails at \(2.0\), while preserving
the original \(286\)-configuration protocol.

## Pass 684 — Open-ended drifting-propensity confidence process

The dropout state is factorized as

\[
\pi_{ij,t}=g_tq_{i,t}q_{j,t},
\]

with separately estimated common-gate and channel states. Each science shot receives
a predictable adaptive pilot packet of \(8,16,32\), or \(64\) gates. Time-uniform
Hoeffding allocations and a declared drift envelope induce simultaneous pair-propensity
intervals.

Restarted covariance e-processes use the infinite prior

\[
w_j=\frac{6}{\pi^2(j+1)^2},\qquad \sum_{j\ge0}w_j=1.
\]

Hence the process is open-ended rather than calibrated to a fixed terminal shot.
In the deterministic replay:

\[
\text{mean pilots/shot}=18.4983,
\]

which saves over \(42\%\) relative to a fixed \(32\)-pilot design; the covariance
change is detected after \(7455\) shots; and

\[
\frac{\|\widehat\Sigma_{\rm dynamic}-\widehat\Sigma_{\rm oracle}\|}
{\|\widehat\Sigma_{\rm frozen}-\widehat\Sigma_{\rm oracle}\|}
=0.0137774.
\]

A separate null replay remains below threshold.

## Pass 685 — Hybrid symbolic controller complex

The seven controller parameters are not one ordinary continuous polytope. The science
quota and two science yields change the stopping combinatorics discretely; the two
tagged costs, outcome overhead, and calibration penalty form continuous min-plus
chambers. The exact declared atlas retains

\[
7776\text{ cells},\qquad22\text{ root phases},\qquad1308\text{ unique pair cells}.
\]

For the nominal science chamber

\[
Q=10,\qquad s_1=6,\qquad s_2=4,
\]

put

\[
x=c_1+o+\kappa,\qquad y=c_2+o+2\kappa,\qquad g=1+o.
\]

The unique tagged-pair region is exactly

\[
x<12,\qquad y<15,\qquad x+y<20,
\]

and

\[
x<4+g\quad\text{or}\quad y<7+g.
\]

Equivalently,

\[
c_1+o+\kappa<12,
\]

\[
c_2+o+2\kappa<15,
\]

\[
c_1+c_2+2o+3\kappa<20,
\]

and

\[
c_1+\kappa<5\quad\text{or}\quad c_2+2\kappa<8.
\]

At \((c_1,c_2,o,\kappa)=(5,7,0,0)\), the continuous calibration radius is \(1/2\),
explaining why the integer atlas accepted only \(\kappa=0\). Reducing the
covariance-tagged calibration coefficient from \(2\) to \(1\) gives only a tie at
\(\kappa=1\); the smallest integer redesign that restores the unique pair is a
two-block credit, reducing that coefficient to zero.

## Verification and boundaries

Every pass emits a deterministic JSON ledger and supports `--check`. The focused
regression uses process-isolated checks so the heavy algebra and simulation verifiers
do not retain one another's allocator state.

- Pass 681 closes degree one exactly; only the scalar part of degree two is closed.
- Pass 682 identifies the signed-turn \(H_1\) branch and does not exclude another W33
  correspondence module containing both cyclotomic branches.
- Pass 683 is a calibrated waveform simulator, not substitute laboratory metrology.
- Pass 684 requires independent pilots, the factorized dropout state, and the declared
  drift envelope.
- Pass 685 gives the exact nominal continuous chamber and the complete integer atlas;
  symbolic facets for all twenty-two phases remain a larger enumeration.
