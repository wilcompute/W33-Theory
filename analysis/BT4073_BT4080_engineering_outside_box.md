# Passes 4073–4080: five engineering closures and three outside-box physics probes

## Evidence status

This packet promotes exact finite algebra, deterministic numerical certificates, and explicitly delimited first-order perturbation theory. It does **not** report fabricated hardware, laboratory data, a finite exact reusable irrational-phase catalyst, a fault-tolerance threshold, a chiral Standard Model, a Euclidean mechanical embedding, a global nonlinear synchronization theorem, gravity, cosmology, or a theory of everything.

Frozen certificate:

`0304eef2ec49efabf5721ed47a35e48064530f459f2964ae49e455ef1d3c5a31`

## Pass 4073 — exact four-router block encoding

The 80-vertex Levi graph is four-regular and bipartite. Its 160 edges admit a deterministic factorization into four perfect matchings. Let `P_j` be the permutation involution that swaps the endpoints of matching `j`. Then

\[
P_j^2=I,\qquad \sum_{j=0}^3 P_j=A_L.
\]

With a balanced four-path selector

\[
B|00\rangle={1\over2}\sum_{j=0}^3|j\rangle
\]

and controlled router

\[
U_{\rm sel}=\sum_j |j\rangle\langle j|\otimes P_j,
\]

the selected block is exactly

\[
(\langle00|B^\dagger\otimes I)U_{\rm sel}(B|00\rangle\otimes I)={A_L\over4}.
\]

The normalized spectrum is

\[
-1^1,\quad(-\sqrt6/4)^{24},\quad0^{30},\quad(\sqrt6/4)^{24},\quad1^1.
\]

This converts the prior abstract QSP oracle into a concrete four-route interferometric architecture. If the selector-state error is at most `eps`, the block error is at most `2 eps + eps^2`; combined with the five-query QSP sequence, the conservative error budget is

\[
5(2\epsilon+\epsilon^2)+6\delta_\phi.
\]

## Pass 4074 — binomial phase-reference processor

For

\[
|A_\phi\rangle={|0\rangle+e^{i\phi}|1\rangle\over\sqrt2},\qquad e^{i\phi}={-4+3i\over5},
\]

compress `K` copies into the symmetric Hamming-weight basis. The program amplitudes are

\[
c_n={\sqrt{\binom Kn}\over2^{K/2}}e^{in\phi}.
\]

A data-controlled cyclic lowering of the `K+1` dimensional reference multiplies data coherence by

\[
z_K=e^{i\phi}S_K+2^{-K}e^{-iK\phi},
\]

where

\[
S_K=2^{-K}\sum_{n=1}^{K}\sqrt{\binom K{n-1}\binom Kn}.
\]

The one-use channel obeys

\[
\|\mathcal E_K-\mathcal U_\phi\|_\diamond
\le |z_K-e^{i\phi}|
\le1-S_K+2^{-K}.
\]

For `K=64`,

\[
z_{64}=-0.7937730374482906+0.5953297780862179i,
\]

and the error is `0.00778370318963677`.

This removes the doubled-angle hierarchy and its depth explosion. It does not beat the asymptotic raw-state law: `1-S_K ~ 1/(2K)`. The reference is only approximately catalytic because the two data branches leave program states with overlap `z_K`; correlations and degradation must be budgeted under reuse.

## Pass 4075 — smallest non-Abelian multiplicity extensions

The original W33 permutation module is multiplicity-free:

\[
\mathbb C^{40}=V_1\oplus V_{24}\oplus V_{15}.
\]

The smallest extension whose exact commutant has separate `M_3` and `M_2` factors uses multiplicities

\[
(m_1,m_{24},m_{15})=(3,1,2),
\]

with total dimension

\[
3+24+30=57.
\]

Its commutant is

\[
M_3(\mathbb C)\oplus\mathbb C\oplus M_2(\mathbb C),
\]

with unitary group `U(3) × U(1) × U(2)`. Freezing the spectator `U(1)` and imposing the determinant-one relation gives

\[
S(U(3)\times U(2))\cong{SU(3)\times SU(2)\times U(1)\over\mathbb Z_6}.
\]

The central determinant embedding has charge ratio

\[
q_3:q_2=-{1\over3}:{1\over2}=-2:3.
\]

A separate dimension-45 extension, with multiplicity six on the singlet, carries a `3×2` bifundamental inside `U(6)`, but unwanted `U(6)` generators then require further breaking.

The current Dirac walk is vectorlike. Perturbative left-minus-right gauge anomalies cancel, and the weak block contains 30 left-handed doublets after converting right-handed fields to left conjugates, so the mod-two Witten count is even. Chirality, observed hypercharges, generations, and the Standard Model matter representation are not derived.

## Pass 4076 — four-gap leakage-notch control

The `H_1` flat energy is `-2J`; the bright gaps are

\[
\Delta/J\in\{4-\sqrt6,4,4+\sqrt6,8\}.
\]

Their squared-gap polynomial is

\[
\prod_r(z+\Delta_r^2)
=z^4+124z^3+4644z^2+53056z+102400.
\]

For a smooth base envelope `h(t)` whose derivatives through order seven vanish at the endpoints, define

\[
f(t)={h^{(8)}+124h^{(6)}+4644h^{(4)}+53056h''+102400h\over102400}.
\]

Then

\[
F(\omega)=H(\omega){\prod_r(\Delta_r^2-\omega^2)\over102400},
\]

so

\[
F(\Delta_r)=0
\]

for all four bright gaps, while

\[
\int f(t)dt=\int h(t)dt.
\]

Every first-order `H_1`-to-bright transition amplitude therefore vanishes, independent of the local diagonal control matrix element. Leakage amplitude begins at second order in control strength and leakage probability at fourth order, rather than the generic quadratic probability. Applying the notch envelope to every SK1 segment combines first-order amplitude-error cancellation with first-order spectral-leakage cancellation.

## Pass 4077 — six experimental falsification contracts

1. **Four-router block:** the selected process block must have only the five certified normalized spectral values and their exact multiplicities.
2. **Five-query QSP:** the spectral sectors must map to `(-1,-1,0,+1,+1)`.
3. **K=64 phase reference:** process coherence must equal the certified complex multiplier within implementation error.
4. **Four-gap notch:** perturbative leakage must change from quadratic to quartic leading probability.
5. **Dirac walk:** halving lattice spacing must asymptotically halve generator error, with a one-step causal cube.
6. **Reflection control:** an isolated reflection must remain period two with pure-state time-average entropy no greater than one bit.

These are experiment designs and null tests; no laboratory result is reported.

## Pass 4078 — mechanical Maxwell–Calladine dual

Treat the oriented Levi incidence matrix `D` as a scalar equilibrium matrix. Then

\[
C=D^T
\]

maps 80 node displacements to 160 spring extensions, while

\[
Q=D
\]

maps spring tensions to nodal forces. Since `rank D=79`,

\[
n_{\rm zero}=1,\qquad n_{\rm selfstress}=81,
\]

and

\[
n_{\rm zero}-n_{\rm selfstress}=1-81=80-160=-80.
\]

After pinning one node, the translational mechanism disappears while all 81 self-stress states remain. The spring dynamical matrix is

\[
{k\over m}DD^T,
\]

with squared-frequency spectrum

\[
0^1,(4-\sqrt6)^{24},4^{30},(4+\sqrt6)^{24},8^1.
\]

The stress projector is exactly the protected-memory projector:

\[
P_{\rm selfstress}=I-D^T(DD^T)^+D=P_{H_1}.
\]

Thus the photonic topological memory has an exact mechanical interpretation as an 81-dimensional state-of-self-stress manifold.

## Pass 4079 — exact nonequilibrium work statistics

For

\[
H(g)=gL_{W33},
\]

the energy levels are `0`, `10g`, and `16g` with degeneracies `1`, `24`, and `15`. A sudden quench `g_0→g_1` leaves eigenvectors unchanged and yields exactly three work values:

\[
0,\quad10\Delta g,\quad16\Delta g.
\]

The distribution is

\[
P(W)={\delta(W)+24e^{-10\beta g_0}\delta(W-10\Delta g)+15e^{-16\beta g_0}\delta(W-16\Delta g)\over Z_0}.
\]

Its characteristic function is closed form, and the Jarzynski identity holds exactly:

\[
\langle e^{-\beta W}\rangle={Z_1\over Z_0}=e^{-\beta\Delta F}.
\]

At `β=0.4`, `g0=1`, `g1=1.5`, the work probabilities are approximately

\[
(0.6828275,0.3001541,0.01701836)
\]

at work values `(0,5,8)`. The mean work is `1.6369175`, the free-energy change is `0.8069171`, and the dissipated work is `0.8300004`.

## Pass 4080 — exact W33 synchronization spectrum

For the normalized Sakaguchi–Kuramoto model

\[
\dot\theta_i=\omega_i+{K\over12}\sum_jA_{ij}\sin(\theta_j-\theta_i-\alpha),
\]

the synchronous frequency for identical oscillators is

\[
\Omega=\omega-K\sin\alpha.
\]

Linearization gives

\[
\dot\delta=-{K\cos\alpha\over12}L_{W33}\delta.
\]

The nonzero decay rates are therefore

\[
{5\over6}K\cos\alpha\quad(24\text{ modes}),
\]

and

\[
{4\over3}K\cos\alpha\quad(15\text{ modes}).
\]

The synchronous state is locally asymptotically stable modulo global phase exactly when `K cos α>0`. The relaxation-time ratio is

\[
{\tau_{24}\over\tau_{15}}={8\over5}.
\]

For zero-mean weak frequency disorder,

\[
\theta_*= {12\over K\cos\alpha}L^+\delta\omega,
\]

and

\[
\|\theta_*\|_2\le{6\over5|K\cos\alpha|}\|\delta\omega\|_2.
\]

This is a local and weak-disorder result, not a global nonlinear synchronization theorem.

## Primary context

The packet uses established block-encoding and QSP architectures, arbitrary-angle phase-catalysis work as a comparison rather than an achieved resource, modern results on correlation and degradation in quantum reference-frame catalysis, Maxwell–Calladine mechanics, two-projective-measurement work statistics, and graph-Laplacian synchronization analysis. All W33-specific formulas and numerical certificates are reconstructed by the packet verifier.
