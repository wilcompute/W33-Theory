# November 20, 2026 — Five independently tested TOE gates plus an adjustable qutrit code

**Research status:** exact finite mathematics and explicitly model-conditional demonstrations, not a physical Theory of Everything. Baseline: GitHub master 31d247e0c3d04ec828ced9c22f7a454005d0ce2c. Reproduction programs: analysis/toe_20261120_repetition_dial_codes.py and analysis/toe_20261120_four_physics_controls.py, with focused tests under tests/test_toe_20261120_fivefront_continuation.py.

## 1. Quantum coding: exact distance dial, including [[1833,81,8]]_3

Already in the repo: the native W33 Levi graph has V=80, E=160, girth 8 and reduced oriented incidence A of dimension 79 x 160. Prior art: analysis/toe_20261120_mixed_levi_repetition_hgp.py (length-3 mixed product), analysis/toe_20261120_graph_repetition_asymmetric_family.py (graph generalization), and analysis/w33_20261009_toe28_hypergraph_product_rate_distance.py (large self product).

The new specialization replaces the length-three repetition matrix with the signed (L-1) x L repetition matrix B_L. For every integer L >= 2, form the conventional ternary CSS hypergraph product

  H_X = [ A tensor I_L  |  I_79 tensor B_L^T ]

  H_Z = [ I_160 tensor B_L  |  -A^T tensor I_(L-1) ].

The minus sign ensures H_X H_Z^T = 0 mod 3. Full row ranks are 79L and 160(L-1), giving N=239L-79 and K=81.

**Distance-X proof.** If x is in ker(H_Z), successive first-block edge slices differ by elements of the cut space im(A^T). Therefore all L slices have the same class modulo that cut space. If that class is zero, x is an H_X stabilizer; otherwise each slice has nonzero weight and weight(x)>=L. Occupying the L repetitions of one nonbridge Levi edge gives a weight-L logical X with nontrivial pairing to a girth-cycle logical Z. Thus d_X=L exactly.

**Distance-Z proof.** For z in ker(H_X), sum each edge's L first-block coordinates, obtaining a graph cycle in ker(A), since every B_L^T column sums to zero. If the projected cycle vanishes, z is an H_Z stabilizer because im(B_L^T) comprises the zero-sum vectors and B_L^T is injective. Otherwise graph girth forces weight(z)>=8. One oriented octagon in one repetition column gives a weight-eight paired logical Z, so d_Z=8 exactly.

Consequently the exact parameter family is **[[239L-79,81,d_X=L,d_Z=8]]_3**. Checked L=2,3,4,5,8,11. At L=8: N=1833, K=81, d_X=d_Z=8, X-check rank=632, Z-check rank=1120, maximum check weights X=6/Z=4, site-check degrees X=2/Z=4. An independently written server-side graph+CSS rebuild also verified zero mod-3 commutator and K=81. Standard HGP theory is prior art; the value here is a reproducible W33-specific finite design point, not a novel coding paradigm. This code needs 1833 distinct physical qutrit subsystems, not one photon; its physical noise threshold, gates and overhead remain untested.

## 2. Exceptional matter: anomaly consistency does not select three families

Established E6 branching: 27 -> 16_(+1) + 10_(-2) + 1_(+4) under Spin(10) x U(1)_psi. Normalizing Dynkin indices T(16)=2, T(10)=1, exact sums yield:

- Mixed gravitational-U1: 16(1)+10(-2)+1(4)=0.
- U1 cubic: 16(1)^3+10(-2)^3+1(4)^3=0.
- Spin(10)^2-U1: 2(1)+1(-2)=0.

The charge rules permit 16*16*10 and 10*10*1 but not 16*16*1. An actual 1_(+4) VEV can allow an exotic 10_(-2) mass only if a nonzero coupling exists; it does not alone mass the 16_(+1). Most importantly these anomalies cancel for any integer number of complete 27 copies. They cannot select three chiral families. A charged 4D Dirac index, actual compactification, global vacuum, Yukawa matrices and measured masses are still missing. This is an exact audit of established algebra, not a new E6 representation theorem.

External reference: https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1

## 3. Gravity: causal order alone fails to determine local curvature

On a 1+1 spacetime consider g_a = exp(2 a x^2) (-dt^2+dx^2). The positive conformal factor leaves every causal relation on the same set of coordinate events unchanged, hence also the finite Hasse graph. But scalar curvature is R_a=-4a exp(-2a x^2), and the coordinate rectangle [-1,1]x[-1,1] has physical volume V_a=2 integral_{-1}^1 exp(2a x^2) dx.

Numerical checks: for a=0,.15,.25, origin scalar curvatures are 0,-.6,-1, while corresponding volumes are 4,4.4387291157,4.7798306476. Eight explicit events have identical order and Hasse relations in all three spacetimes. Thus order alone cannot fix curvature or metric scale. This explicitly instantiates the standard Malament-type conformal result. Causal-set approaches that supplement ordering by number/volume are not ruled out; Einstein dynamics has not been derived.

External reference: https://doi.org/10.1007/s41114-019-0023-1

## 4. SU3: center holonomy needs a coherent reference

Take the qutrit Weyl shift X and clock Z with ZX=omega XZ, omega=exp(2pi i/3). Their group commutator K=Z X Z-dagger X-dagger is omega times the identity. Exact finite calculation verifies both operators lie in SU3 and the commutator is central.

The fundamental trace is 3 omega, while the adjoint character equals |tr_fund K|^2-1=8, identical to the identity character. Acting by conjugation on any qutrit density operator likewise leaves it unchanged. This adjoint-center blindness was ALREADY established in repo Pass5709; it is not claimed as new.

The operational distinction appears only with a coherent controlled-K reference path: preparing a control qubit in |+> and measuring in the X basis gives P(+|identity)=1 and P(+|K)=1/4. Common SU3 gauge conjugation of X and Z leaves this unchanged. Under perfect iid Bernoulli shots and a midpoint decision threshold of 0.625, an elementary Hoeffding bound is below 1% after 19 shots. This ideal count excludes reference phase drift, controlled-gate errors, detector bias and photon losses. This is a reference requirement/falsifier, not a laboratory demonstration.

## 5. Genuine three-time qutrit memory: adversarial-loss guard

The new source theorem in Beyer et al. (arXiv:2611.17268, 2026) describes a generalized-dimensional MUB three-time witness. The parallel repo commit 31d247e already gave a conservative seven-setting frequency method under IID accepted trials. This continuation adds an explicit guard against lost outcomes without assuming their state is depolarized.

For calibrated acceptance probability at least eta for each prepared input, accepted probabilities p_j constrain every trace-preserving completion of missing trials to eta*p_j <= p_j_true <= eta*p_j+1-eta. Fidelity monotonicity under the chosen measurement bounds each quantum root fidelity by the classical Bhattacharyya sum using the upper allowed coordinates. For the first channel, the nonunitality lower bound is S1>=max(0,3eta*r0-1). Their difference yields a conservative witness upper bound, conditional on stationarity, representative calibrated acceptance, legitimate CPTP completion and specified measurement settings.

Using only a prospective reference model gamma=.75 and late depolarization epsilon=.01, conservative upper bounds for eta=1,.995,.99,.985 are -0.789493,-0.346887,-0.015867,+0.264454. The model-dependent sign threshold is eta=0.9897351649185687. Thus approximately 1.03% uncharacterized loss can make this specific worst-case certificate inconclusive. It does not make the process classical.

At eta=.995 and confidence delta=.01, simultaneous 21-coordinate Hoeffding radius sqrt(log(42/delta)/(2N)) gives a sufficient N=155,975 accepted trials per setting (seven settings, 1,091,825 accepted total) for a negative prospective conservative upper bound. The bound is not device independent: detector efficiency must be independently calibrated, no unfair postselection can be hidden, and all channel assumptions require separate experimental checks. There are no real device measurements here.

Source theorem: https://arxiv.org/abs/2611.17268

## Reproduce and scientific boundary

Run:
  python analysis/toe_20261120_repetition_dial_codes.py
  python analysis/toe_20261120_four_physics_controls.py
  python -m unittest discover -s tests -p test_toe_20261120_fivefront_continuation.py -v

Regenerate data/toe_20261120_repetition_dial_codes.json and data/toe_20261120_four_physics_controls.json. The focused tests verify full sparse CSS commutation, ranks and logical pairings; the E6 charge sums; curvature/volume nonidentifiability; SU3 central interferometric distinction; and calibrated worst-case memory loss statistics.

**Five independent physical blockers remain:** (i) a genuine anomaly-free chiral UV matter/Dirac construction; (ii) fault-path and decoder thresholds for hardware qutrit CSS codes; (iii) a density-plus-causal-metric continuum gravitational action; (iv) a stable controlled-Wilson optical phase reference; (v) independent efficiency calibration and full-process memory certification. Neither the algebra nor the finite simulations solve an experimental Theory of Everything.
