# Causal exchanges to matter propagation and gauge curvature: a high-risk TOE bridge

**2026-11-19. STATUS:** 22 focused regression tests PASS; independent mathematical derivations and reproducible simulations. No claim of a completed Theory of Everything, novel physical law, new observed effect, or dynamically selected 4D spacetime. W33 is not assumed to be fundamental.

## Why this is the right type of 'home run' attempt

Instead of discovering another numerical correspondence, demand that a tiny common substrate account for **time, dimension, matter propagation and gauge phase** with falsifiable equations. The proposed mathematical scaffold comprises a locally finite causal order, Poisson interval cardinalities as a volume proxy, U(1) phase transport on causal intervals, and a microscopic rule for propagation amplitudes. The fourth ingredient does **not** follow automatically from the first three. Our primary result is a concrete obstruction to a tempting, overly simple construction, plus one constructive repair using an externally specified continuum field equation.

We read recent and parallel repository commits including 017f5cde3, 22ac80224 and 740af8b5b and specifically inspected the older causal-set programs:
- analysis/toe_20261105_causal_growth_without_background.py: unconstrained transitive-percolation causal growth does NOT independently select 4D Minkowski geometry.
- analysis/toe_20261105_causal_poset_measure_correction.py: an exact DAG-presentation entropy factor 2^(R-L) biases the putative causal history measure.
- analysis/toe_20261105_causal_bdg_history_interference.py: finite BDG action-phase sums do not establish a quantum gravity continuum.

We do not relabel these previous failures as solved. Our new testing direction is the **matter plus gauge dynamical kernel**, after separating known prior art from new-to-repository constructions.

Prior work: Johnston, *Particle propagators on discrete spacetime* (2008), https://arxiv.org/abs/0806.3083 ; Surya, *The causal set approach to quantum gravity* (2019), https://doi.org/10.1007/s41114-019-0023-1 ; *Path sums for propagators in causal sets* (PRD 109, 046008, 2024), https://doi.org/10.1103/PhysRevD.109.046008 ; *Link-based causal set propagators in 1+1 dimensions* (2026), https://arxiv.org/abs/2604.24812 ; and earlier causal-set gauge-holonomy treatments, https://www.academia.edu/92351424/8_Gauge_Fields_in_Causal_Set_Theory .

## Gate A. A finite order can statistically encode an already specified Lorentzian dimension

For n events uniformly Poisson-sprinkled inside a d-dimensional Minkowski causal diamond, the probability that an **unordered** random pair is comparable is

    p(d) = Gamma(d+1) Gamma(d/2) / [2 Gamma(3d/2)].

Some literature divides by four rather than two when defining a normalized *directed ordered-pair* count, so one must specify normalization. For d=2,3,4, p(d)=1/2,8/35,1/10. Independent uniform-in-volume diamond sampling, 6,500 events in each input dimension and 240,000 random pair checks give Myrheim–Meyer estimates:

| Spacetime dimension inserted | Recovered dimension |
|---:|---:|
| 2 | 2.0210 |
| 3 | 2.9918 |
| 4 | 3.9468 |

This validates the estimator in known Minkowski embeddings. It does not select 3+1D as a consequence of microscopic dynamics. In 1+1D, ordering points by null coordinate u=t+x and taking the longest increasing sequence in v=t-x gives a causal longest-chain measure. At high density the leading chain height is about 2 sqrt(rho V)=sqrt(2rho) tau for diamond volume V=tau^2/2, permitting an **asymptotic** duration estimator with finite-density bias.

## Gate B. Known Johnston chain sum recovers a relativistic massive scalar exactly in ensemble

For the 1+1 Minkowski diamond with external endpoints separated by proper time tau, define causal matrix C and density rho. The massive retarded kernel is a finite nilpotent series

    K = (1/2) C [I + m^2 C/(2rho)]^(-1).

The expectation of the number of causal chains with k internal events is

    E[(C^(k+1))_ab] = (rho V)^k/(k!)^2, V=tau^2/2.

Hence the **exact Poisson-ensemble mean**, for every positive rho, is

    E[K_ab] = (1/2) J0(m tau).

This is Johnston's established causal-set construction, not a discovery of ours. We independently tested a fast 2D-dominance Fenwick recurrence against a dense matrix inverse at machine precision, and then used 1,200, 1,200 and 1,000 independent Poisson causets:

| rho | Monte Carlo mean K | Exact 0.5 J0(1.6) |
|---:|---:|---:|
| 12 | 0.226728 | 0.227701 |
| 45 | 0.228900 | 0.227701 |
| 120 | 0.226613 | 0.227701 |

All means agree within their reported Monte Carlo uncertainty. A retarded one-body kernel is NOT itself a Hilbert-space vacuum, a Feynman propagator, a derivation of mass, or a quantum theory of gravity.

## Gate C. Exact obstruction: Wilson phases do not automatically yield gauge-coupled dynamics

Choose a constant external electric field E in 1+1 Minkowski spacetime, A_t=0, A_x=E t, and charge q. The covariant derivative is D_mu=partial_mu-i q A_mu. For a source at (0,0), the straight Wilson phase is

    U(t,x)=exp(i qE tx/2).

Inside the future cone put s=t^2-x^2 and use the gauge-covariant ansatz

    G_R(t,x)=(1/2) U(t,x) f(s).

Substitution into the **continuum** minimally coupled Klein–Gordon equation, (D_t^2-D_x^2+m^2)G_R=0 away from the source, reduces exactly to the ordinary differential equation

    4(s f''+f') + [m^2+(qE)^2 s/4] f=0, f(0)=1.

The regular power series f(s)=sum_n c_n s^n obeys

    c[0]=1, c[-1]=0;
    4(n+1)^2 c[n+1] + m^2 c[n] + (qE)^2 c[n-1]/4=0.

This construction has two independent exact limits:
- E=0: f(s)=J0(m sqrt(s)), the familiar free 1+1 retarded massive scalar.
- m=0: f(s)=J0(qE s/4), a **nonzero electric-curvature tail** even for a massless charged scalar.

We checked the series against independent adaptive ODE integration and a numerical covariant PDE residual. An elementary bare Wilson-hop retarded ansatz, G=(1/2)U at m=0, is gauge-covariant yet has a nonzero covariant wave-operator residual proportional to (qE)^2 s/4. The corrected response cancels it.

At tau=2, x=0, m=0, qE=.9:

    naive phase-only response = 0.500000000
    correct charged response = 0.403761899
    missed correction = 0.096238101.

This is a **precise failure gate for a simplistic order-plus-U(1)-phase ontology**: gauge covariance is necessary but not dynamically sufficient. We also verify Wilson-loop two-path phase differences equal qE times enclosed oriented spacetime area and that arbitrary local rephasings transform the endpoint kernel covariantly. Genuine nonzero curvature is distinguishable from pure gauge.

## Gate D. An exact finite-density, unbiased, event-count estimator of charged propagation

A more constructive connection comes from the Poisson falling-factorial identity. For N~Poisson(rho V),

    E[(N)_n]=(rho V)^n, (N)_n=N(N-1)...(N-n+1).

Since s=2V in a 1+1 causal diamond, a continuum wave-series monomial s^n can be replaced by the finite random estimator (2/rho)^n (N)_n. Therefore

    fhat_N = sum_(n=0)^N c_n (2/rho)^n (N)_n

is an **ensemble-unbiased estimator** of the charged KG radial factor f(2V) at *any* positive density rho under the specified continuum background and convergence assumptions:

    E[fhat_N] = sum_(n>=0) c_n(2V)^n = f(2V).

The estimator contains only the Poisson event count N, sprinkling density rho, and the externally supplied physical inputs m,qE from the KG equation. **It does NOT derive electric charge, m, E or the dynamics from counting alone.** It is a mathematical construction showing that when dynamics is correctly specified, causal event-count factorial moments can encode its amplitudes without a large-density bias.

Independent Monte Carlo tests with 10,000 Poisson draws each:

| rho | m | qE | Exact f | Mean fhat | Standard error |
|---:|---:|---:|---:|---:|---:|
| 12 | 0 | .9 | .807524 | .807870 | .000749 |
| 12 | .8 | .9 | .324955 | .325530 | .001319 |
| 80 | 0 | .9 | .807524 | .807666 | .000288 |
| 80 | .8 | .9 | .324955 | .325183 | .000509 |

All results lie within one standard error of the calculated continuum values. The power-series coefficient recurrence, small finite-N factorial identities, limiting Bessel forms and independent differential-equation solutions are all tested.

**Scientific level:** Poisson factorial unbiasedness is standard probability mathematics, and the constant-field KG dynamics is stipulated. This is a new-to-this-repository explicit crosswalk between an external charged wave equation, causal interval counts and U(1) holonomy, NOT a new empirically established theory of matter.

## Gate E. In four dimensions the propagation kernel MUST change

In 1+1 dimensions, the free massless retarded scalar has support *throughout* the forward light cone. In 3+1 flat spacetime the massless scalar response instead sits **on** the null cone, G_ret=(1/2pi) theta(t) delta(s), s=t^2-r^2. For a 4D Alexandrov interval, the volume is

    V4(s)=pi s^2/24.

If a Poisson set of density rho has no event between causally related endpoints, the conditional probability of a direct causal **link** is exp[-rho V4(s)]. The scaled 4D link kernel is

    K4_rho(s)=sqrt(rho)/(2 pi sqrt(6)) exp[-rho pi s^2/24], s>=0.

It converges in the distributional sense to delta(s)/(2pi). We checked the integral normalization against the constant test and the e^(-s) test at rho=1,16,256,4096, with the characteristic null-shell width scaling as rho^(-1/2).

This is known causal-set physics. It exposes a tough universality requirement: **one unchanged “constant amplitude for every causally related pair” kernel cannot reproduce both the 2D interior response and the 4D null-shell response.** A foundational exchange model must select a dimension and its propagation rules dynamically rather than inserting a metric and specialized kernel by hand.

## Synthesis: the actual opportunity versus the missing physics

The candidate common structure is **causal order + interval-volume statistics + unitary gauge transport + dynamical amplitudes**. It unifies multiple descriptions at the level of one fixed-background mathematical test. The sharp negative result is that order/counts and Wilson link phases alone do not fix correct charged propagation; the field-curvature coupling must be dynamical. An equally sharp gap is that the partial order has not independently generated Lorentzian Einstein gravity or four dimensions.

Missing: a dimension-selection mechanism, full metric/graviton dynamics, a physical quantum vacuum and Born probabilities, chiral spinors with anomalies and spin-statistics, non-Abelian Yang–Mills constraints, matter backreaction and measurable predictions for masses/couplings. None is established by the simulations.

## Reproduction

    python analysis/toe_20261119_causal_exchange_gauge_homerun.py
    python -m unittest discover -s tests -p test_toe_20261119_causal_exchange_gauge_homerun.py -v

Source: analysis/toe_20261119_causal_exchange_gauge_homerun.py
Regression: tests/test_toe_20261119_causal_exchange_gauge_homerun.py
Numerical output: data/toe_20261119_causal_exchange_propagator_gauge_gate.json

22 focused tests PASS, including independent dense versus fast chain sums, exact KG coefficient and special-function checks, 10,000-sample charged estimator tests, gauge covariance, nonzero Wilson-loop flux, charged-PDE failure and repair, relativistic invariance checks, and distributional 4D null-cone scaling.

## Five independent, high-upside research experiments

1. **4D Dirac/chirality:** derive a regulator for Weyl/Dirac fermions and anomaly-free generations on *unembedded* causal partial orders; require correct Clifford/Ward identities and avoid fermion doubling, mirror tuning and fake gauge representations.
2. **Gauge without a prescribed electric field:** obtain an SU(3)×SU(2)×U(1) bundle, Gauss constraints and local Yang–Mills/Maxwell action from a microscopic causal algebra. Demand the constant-E KG Green function above as a fixed, independent unit test.
3. **Einstein dynamics and dimensional selection:** define an intrinsically weighted quantum measure over causal histories, not DAG presentations; dynamically recover four-dimensional local Lorentz symmetry and Einstein curvature with graviton degrees of freedom.
4. **Quantum state reconstruction:** construct the positive Hilbert space, vacuum, Born rule and causal S-matrix from the retarded kernels, proving spectral/optical-theorem constraints; an isolated retarded Green function is not a quantum theory.
5. **Nonconstant/non-Abelian extension:** derive the first curvature and field-gradient coefficients for a gauge-covariant 3+1 path-sum/heat kernel, then test full Ward identities and spin transport. If only ad hoc tuning recovers known coefficients, reject the proposed microscopic rule.

**Recommendation:** Spend the next serious effort on a mathematically unique, dimension-independent microscopic **kernel-generating principle**. One must derive the gauge-curvature term, not insert a continuum charged KG equation as we did. That is the scientifically meaningful potential home run.
