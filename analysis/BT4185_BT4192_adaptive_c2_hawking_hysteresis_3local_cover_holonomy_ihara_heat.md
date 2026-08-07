# Passes 4185–4192 — adaptive C2, Hawking criticality, hysteresis, exact 3-local clocks, high-girth covers, and three outside-box closures

## Scope

This packet executes the five physics targets following Passes 4169–4176 and adds three independent finite-model probes. All claims are restricted to the exact finite models stated below. Nothing here establishes a fabricated four-dimensional pump, observed Hawking radiation, physical spacetime hysteresis, a laboratory three-local processor, a fabricated high-girth Holonet, gravity, cosmology, or a theory of everything.

## Pass 4185 — adaptive second-Chern compiler

The parent control is the Wilson–Dirac map

\[
d(k)=(\sin k_1,\sin k_2,\sin k_3,\sin k_4,-3+\sum_i\cos k_i),\qquad \hat d=d/|d|.
\]

The 16 time-reversal-invariant corners remain an exact integer phase certificate. Their mass classes are the already certified sequence \(1,-1,-3,-5,-7\), with binomial multiplicities and alternating chiralities, yielding \(C_2=1\).

For response reconstruction, the packet replaces the earlier endpoint/central-difference mesh with phase-centered hypercell midpoint cubature of the pullback volume density. The audited sequence is

| N per axis | samples | C2 estimate |
|---:|---:|---:|
| 3 | 81 | 6.297860822843193 |
| 5 | 625 | 1.7568099386988092 |
| 7 | 2,401 | 1.1490090416696077 |
| 9 | 6,561 | 1.0328137348691868 |
| 11 | 14,641 | 1.007626813300158 |
| 13 | 28,561 | 1.0018270591558598 |

The first audited mesh whose value rounds to the correct integer is \(7^4=2401\) samples. The first audited mesh below five-percent response error is \(9^4=6561\) samples. Relative to the prior 707,281-node response mesh, the latter is a factor

\[
707281/6561=107.80079256210944
\]

smaller. This is not a proof that 6,561 samples is globally minimal; it is a deterministic compiler improvement while the 16-corner Dirac certificate still supplies the exact topological integer.

## Pass 4186 — Hawking entanglement, steering, and capacity surfaces

Use a symmetric two-mode squeezed thermal core with Hawking squeezing

\[
r(\omega)=\operatorname{atanh}\!\left(e^{-\pi\omega/\kappa}\right),\qquad \kappa=0.4,
\]

followed by one-sided vacuum attenuation of transmissivity \(\eta\). In this calibrated Gaussian core the relevant boundaries separate cleanly:

\[
n_{\rm ent}=\frac{e^{2r}-1}{2},
\]

\[
n_{B\to A}=\sinh^2r,
\]

\[
n_{A\to B}=(2\eta-1)\sinh^2r\quad\text{for }\eta>1/2,
\]

while the pure-loss unassisted quantum-capacity slice is

\[
Q=\max\left\{0,\log_2\frac{\eta}{1-\eta}\right\}.
\]

Thus entanglement survives beyond steering, and the lossy direction cannot Gaussian-steer the partner at all for \(\eta\le 1/2\), exactly where the pure-loss capacity also vanishes.

Representative thresholds are:

| omega | r | entanglement n_th | B→A steering n_th |
|---:|---:|---:|---:|
| 0.1 | 0.4921713785 | 0.8380262449 | 0.2624343094 |
| 0.2 | 0.2109541274 | 0.2624343094 | 0.04516570536 |
| 0.3 | 0.09506557725 | 0.1047041033 | 0.009064722057 |
| 0.4 | 0.04324084828 | 0.04516570536 | 0.001870936599 |
| 0.6 | 0.008983532682 | 0.009064722057 | 0.00008070603051 |

At \(\omega=0.3\), A→B steering has thresholds 0, 0.003625888823, and 0.007251777646 for \(\eta=0.5,0.7,0.9\), respectively.

The finite disorder envelope remains the previously frozen correlated-Gaussian nine-cell audit: \(\sigma_r=0.35\), correlation length two cells, and log-negativity range 0.08229191750 to 0.5298852171. Therefore this pass closes the analytic entanglement/steering/capacity core and ties it to the committed disorder envelope, but does not claim an exact capacity theorem for arbitrary five-dimensional continuous disorder.

## Pass 4187 — saturating scale backreaction and true hysteresis

The positive occupation feedback of Pass 4171 ended in a saddle node rather than bistability. Add the simplest saturating term,

\[
\dot s=\gamma\left[\ln80-4s+g n_B(2e^{-s})-h n_B(2e^{-s})^2\right],\qquad h=0.004.
\]

The two saddle-node couplings are

\[
g_-=0.48155795490354825,
\qquad
g_+=1.1377609142984069.
\]

Hence \(g_-<g<g_+\) is a genuine three-fixed-point window. At \(g=0.5\):

| s | derivative | ln80/s | stability |
|---:|---:|---:|---|
| 1.2568469367 | -3.1626010235 | 3.4865237020 | stable |
| 4.2806819287 | +3.7642402888 | 1.0236748975 | unstable |
| 4.9471634287 | -8.1605223556 | 0.8857654892 | stable |

The saddle nodes occur at \((s,g)=(4.6222697829,0.4815579549)\) and \((1.9790746182,1.1377609143)\). Quasistatic sweeps through the interval therefore possess a controlled hysteresis loop between two stable scale branches. This is a finite nonlinear mean-field memory model, not physical spacetime hysteresis.

## Pass 4188 — exact three-local autonomous history clock

Pass 4172 reduced the 25-state Gray history clock from seven-local to four-local. The remaining obstacle is removed exactly by expanding each original gate transition into two legal substeps.

For original transition \(t\):

1. use the spectator-condition AND flag to flip the changing Gray bit and activate a one-hot transition ancilla \(q_t\);
2. use \(q_t\) to perform the corresponding two-site SWAP and deactivate \(q_t\).

The first propagation term touches one AND flag, one Gray bit, and \(q_t\): three bodies. The second touches \(q_t\) and the two data sites: three bodies. AND constraints and one-hot legality penalties are also at most three-local.

The 24-gate program becomes a 49-state legal chain with engineered couplings

\[
J_j=\Omega\sqrt{(j+1)(48-j)},\qquad j=0,\ldots,47.
\]

Its exact spectrum is

\[
-48\Omega,-46\Omega,\ldots,+48\Omega,
\]

so the legal gap remains \(2\Omega\), perfect endpoint transfer occurs at \(\pi/(2\Omega)\), and the full revival remains \(\pi/\Omega\). The endpoint data operation is still \(U_{\rm shift}^3=I\).

Resource count: five Gray clock qubits, 72 static AND ancillas, and 24 transition ancillas. The auxiliary count is therefore 96. This is an exact 3-local construction on an expanded history space; it is not an ancilla-minimality theorem.

## Pass 4189 — escaping the Levi 2-lift obstruction

The corrected base Levi graph has 80 vertices, 160 edges, degree four, girth eight, and free fundamental group rank

\[
160-80+1=81.
\]

Exact simple-cycle counts are

\[
N_8=1620,\qquad N_{10}=5184,\qquad N_{12}=43200.
\]

The previous signed 2-lift obstruction only forbids eliminating all base eight-cycles with a \(\mathbb Z_2\) voltage. It does not forbid higher voltage groups.

Take the Fermat prime \(p=65537\) and assign each oriented base edge the deterministic voltage

\[
v_e=\operatorname{first64}(\operatorname{SHA256}(\texttt{W33:COVER:1:e}))\bmod65537.
\]

The SHA-256 of the resulting ordered 160-voltage vector is

`809d22e8ad93d1da23bcc720ba5eacbe997b7f2fba81c10e753d6d901e8ca503`.

Direct enumeration finds zero zero-voltage cycles at lengths 8, 10, and 12. Therefore the 65,537-fold cyclic cover has

\[
5,242,960\text{ vertices},\qquad10,485,920\text{ edges}
\]

and certified girth at least 14.

More importantly, the base graph fundamental group is the free group \(F_{81}\). Free groups are residually finite. For every target length \(L\), one can choose a finite-index normal subgroup containing none of the finitely many nontrivial reduced words of length at most \(L\). The corresponding finite regular graph cover therefore has girth greater than \(L\). Thus W(3,3)-locally-incidence-preserving finite covers with girth tending to infinity exist abstractly.

The explicit cyclic cover is one concrete finite witness; the residual-finiteness statement proves existence of an unbounded-girth family but does not furnish an efficient explicit tower for every target girth.

## Pass 4190 — bonkers: the two Wilson loops are already a universal single-qubit gate set

The two frozen Wilczek–Zee holonomies satisfy

\[
U_y^3=U_z^3=I,
\]

and do not commute. Their commutator has

\[
\operatorname{tr}[U_y,U_z]=-\frac14,
\]

so its eigenphases are \(\pm\theta\) with

\[
\cos\theta=-\frac18,
\qquad \theta=1.696124157962962\ldots
\]

If \(\theta/\pi\) were rational, the rational-cosine theorem would force a rational cosine to lie in \(\{0,\pm1/2,\pm1\}\), contradicting \(-1/8\). Therefore the commutator has infinite order.

The generated subgroup is nonabelian and infinite. A proper infinite closed subgroup of \(SU(2)\) is contained in a torus or its normalizer. It cannot lie in a torus because the generators do not commute; and two noncommuting odd-order elements cannot both lie in a torus normalizer. Hence the closure is

\[
\boxed{\overline{\langle U_y,U_z\rangle}=SU(2)}.
\]

So the exact geometric loops from Pass 4137 already form a dense universal single-qubit holonomic gate set. This says nothing yet about fault tolerance, two-qubit universality, or laboratory implementation.

## Pass 4191 — bonkers: exact Ihara factorization and Ramanujan property

The degree-four Levi adjacency spectrum is

\[
4^1,\quad (-4)^1,\quad (\sqrt6)^{24},\quad(-\sqrt6)^{24},\quad0^{30}.
\]

All nontrivial eigenvalues satisfy \(|\lambda|\le2\sqrt3\), so the graph is a bipartite Ramanujan graph.

Bass's determinant relation gives the exact inverse Ihara zeta polynomial

\[
\boxed{\zeta^{-1}(u)=
(1-u^2)^{81}(1-9u^2)(1+9u^4)^{24}(1+3u^2)^{30}.}
\]

The Hashimoto spectral radius is exactly three, the zeta radius is \(1/3\), and all nontrivial Hashimoto roots have modulus \(\sqrt3\). This is an exact finite graph spectral statement, not a physical vacuum partition function.

## Pass 4192 — bonkers: heat-kernel dimension falsifier

For the same Levi graph the Laplacian spectrum is

\[
0^1,\quad8^1,\quad(4-\sqrt6)^{24},\quad(4+\sqrt6)^{24},\quad4^{30}.
\]

The exact return probability is

\[
P(t)=\frac{1+e^{-8t}+24e^{-(4-\sqrt6)t}+24e^{-(4+\sqrt6)t}+30e^{-4t}}{80}.
\]

Define the diffusion spectral dimension

\[
d_s(t)=-2\frac{d\ln P(t)}{d\ln t}.
\]

It reaches its unique maximum at

\[
t_*=1.60655330558
\]

with

\[
\boxed{d_s^{\max}=3.47143073390<4}.
\]

Therefore the actual finite Levi heat kernel does not independently reproduce the separate channel-balance \(d_s=4\) attractor. This is a useful negative result: the four-dimensional channel-balance model cannot be justified simply by pointing at diffusion on the bare Levi graph.

## Evidence boundary

The frozen certificate is `data/PART_4185_4192_ADAPTIVE_C2_HAWKING_HYSTERESIS_3LOCAL_COVER_HOLONOMY_IHARA_HEAT.json`. The deterministic verifier and focused pytest recompute the principal numerical and combinatorial claims. The public and manuscript artifacts must preserve the protected `master:/docs` Pages contract; `docs/index.html` is not edited by this packet.
