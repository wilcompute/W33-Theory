# Temporal order as an operational readout of W33 symplectic phases

**Date:** 2026-11-20. **Repo baseline:** b1065f344ce3d46d516f40ee0275bd1866f0dbdd. **Status:** a reproducible mathematical and simulation packet, NOT a new physical law or TOE solution. This is a deliberately different direction from the existing E6/E8 count-matching, hypergraph-product codes and causal metric inversions.

## Hypothesis to falsify

A primitive notion of time as the *order of quantum operations* may transduce the finite symplectic structure of W33 into observable interference. A projective symplectic point does not carry a canonical **signed** commutator phase. A cyclic product of three such pairings *is* projectively well defined. Can coherent order control measure the pairwise phases, and can independent informationally complete input preparations show whether their relative phase is truly central rather than detector bias?

**Established prior art, not claimed as our discovery:** W(3,3) is the two-qutrit Pauli commutation geometry (40 points, 40 lines); quantum switches read relative phases of differently ordered gates; the nine qutrit Hesse SIC preparations and their Gram matrix are known. The contribution in this packet is the explicit end-to-end finite protocol, its projectively meaningful triple diagnostic, the tensor-product SIC centrality certificate, quantified sampling conditions, and deliberate falsifiers. No part of this protocol alone establishes emergent spacetime, Einstein dynamics, quark colour, or a chirally compactified E8 vacuum.

## 1. Recover exactly what W33 knows — and what it cannot know

Take nonzero vectors u in F3^4, identifying projective points [u]=[−u]. Fix the alternating pairing

    s(u,v)=u0*v2+u1*v3-u2*v0-u3*v1  (mod 3).

The projective pair is commuting iff s(u,v)=0. The direct enumerator gives 40 projective points, 240 unordered commuting pairs and 540 unordered noncommuting pairs.

**Critical obstruction:** s(−u,v)=−s(u,v), so the sign of a nonzero pair is not an intrinsic projective observable. An arbitrary canonical representative chosen in a program does not solve this problem physically.

For any ordered triple of pairwise nonorthogonal projective points define

    T([u],[v],[w])=s(u,v)*s(v,w)*s(w,u) in F3^\times={+1,−1}.

Rescaling any one vector by −1 flips exactly two factors, so T is independent of all three representative choices. It is invariant under symplectic transformations; reversing the order of two projective points flips its sign. An antisymplectic transformation with multiplier −1 also flips it. This makes T an **oriented projective symplectic pseudoscalar**, not a canonical signed invariant for an *unoriented* triangle.

Verified counts among unordered triples (using index order to orient each triple): 3240 fully noncommuting triples, of which 360 span 2D vector subspaces (180 signs of each kind) and 2880 span 3D subspaces (1440 each kind). Every noncommuting pair has **18** third points noncommuting with both: exactly 9 giving each sign. For any such pair, an antisymplectic similitude fixing both projective endpoints swaps the two nine-element classes. The 360 subspace-dependent triples also follow from 90 nonisotropic projective lines, each with 4 choose 3=4 triples.

**TOE implication:** finite projective incidence identifies *whether* two operators commute, but the chirality sign is additional information. A physically meaningful nonzero sign requires an ordered triple of measurements (or equivalent orientation and reference structure), not mere W33 incidence counts.

## 2. A coherent quantum switch reads the symplectic pairing

Let X|j>=|j+1>, Z|j>=omega^j|j>, omega=exp(2pi i/3), so ZX=omega XZ. For u in F3^4 define the 9-dimensional two-qutrit generalized Pauli operator

    W(u)=[X^(u2) Z^(u0)] tensor [X^(u3) Z^(u1)].

Then exactly W(u)W(v)=omega^{s(u,v)}W(v)W(u).

Apply W(u),W(v) as black-box gates in a **coherent superposition of their two orders** to a pure or mixed 9-dimensional target state rho, with the control initialized in |+>. With branches U0=W(u)W(v), U1=W(v)W(u), the control complex coherence is

    c(u,v,rho)=Tr[U0 rho U1^\dagger]=omega^{s(u,v)}.

Thus the target factors out; the control X mean is Re(c)=1 for commuting pairs and −1/2 otherwise; control minus-Y mean is Im(c)=0 or ±sqrt(3)/2. The latter resolves the representative-dependent sign in a calibrated *lifted* setting. All 780 unordered projective pairs were tested with explicit 9x9 unitary matrices, and agreement was within 1.5e−15. An additional mixed target validates state independence in selected cases.

**Necessary quantum-control boundary:** If one instead randomly performs either definite ordering and discards which order was used, the target output states are identical, because U0=omega^s U1. There is NO observed phase. The coherent order reference is the operational resource. A conventional known-gate circuit can emulate the resulting statistics and does not by itself prove device-independent indefinite causal order. A true black-box switch and independent causal witness would be different claims.

## 3. Certify CENTRAL, rather than just a convenient target-state phase

For general unitaries A,B, define U0=AB, U1=BA and the unitary K=U1^\dagger U0. The control interference on input rho is Tr(rho K). **Exact input independence for all states implies K is scalar**, but testing one target state is insufficient.

A constructive informationally complete verification uses the nine Hesse SIC rank-one projectors P_i generated from fiducial (0,1,-1)/sqrt(2). They satisfy

    Tr(P_i P_j)=(3 delta_ij+1)/4,
    sum_i P_i=3 I3.

Take the 81 product preparations Q_(ij)=P_i tensor P_j. The operator-frame Gram matrix is

    Gamma = G tensor G, G=(3 I9 + J9)/4,
    Gamma^(-1)=G^(-1) tensor G^(-1),
    G^(-1)=(4/3) I9 -(1/9) J9.

Its eigenvalues are 9 once, 9/4 sixteen times, and 9/16 sixty-four times; condition number 16. The 81 complex amplitudes a_k=Tr(Q_k K) reconstruct EVERY complex 9x9 K. Let avg(a)=Tr(K)/9 and delta_k=a_k−avg(a). Then the **exact identity**

    ||K − (Tr K/9) I9||_F^2 = delta† Gamma^(-1) delta

certifies centrality, including the complete distinction between a scalar commutator and a noncentral SU9 operator. This is an application of established SIC informational completeness, with a new explicit switch-based certificate for this testbed.

The run reconstructs a seeded noncentral 9x9 unitary to 1.95e−15 max entry error, yielding noncentral squared norm 5.832074757247981 versus the identical SIC Gram-inverse quadratic certificate. For a truly central Weyl commutator, the largest variation across all 81 probes is under 4.5e−16.

**Common detector visibility and common phase:** If all measured amplitudes are multiplied by the same nonzero complex reference factor, the normalized noncentrality ratio

    (delta†Gamma^(-1)delta)/(a†Gamma^(-1)a)

is unchanged. This is not permission to ignore detector systematics. If visibility varies with the prepared input, even a perfectly central K appears noncentral. A deterministic fake-calibration test with K=omega I gives a **spurious inferred Frobenius noncentral norm ~0.503** under input-dependent visibility! Per-input visibility/SPAM checks are mandatory.

## 4. Shot planning, NOT laboratory data

Assume ideal state preparation, mutually independent accepted shots, a calibrated phase/visibility correction, and a ±1 readout of both control quadratures for each product SIC input. With m=81 complex amplitudes, simultaneously bound each real/imaginary coordinate with Hoeffding radius

    t=sqrt(2 log(4m/delta_conf)/N),

with N accepted shots per quadrature. Therefore, with confidence at least 1−delta_conf,

    ||K−(Tr K/9)I||_F
      <= (4/3) [sqrt(sum |a_hat−avg(a_hat)|^2)+sqrt(2m)*t].

In the illustrative zero-measured-spread limit, at confidence 99%, requiring this *loose sufficient bound* below 0.25 yields N=95,717 accepted shots per quadrature, or 15,506,154 accepted across 81 x two quadratures. This bound assumes unit visibility (or corrected amplitudes with no calibration uncertainty); known visibility v<1 amplifies the statistical error radius by 1/v and approximately multiplies N by 1/v². The large number is an upper-bound planning figure, NOT a claim of optimal tomography cost.

For just the sign of a *known noncommuting* pair, under calibrated fringe visibility at least 0.8 and bounded phase drift 0.1 radians, a conservative minimal imaginary-control signal is ~0.6494. The Hoeffding two-sided bound falls below 1% with 26 accepted shots (per selected oriented pair). The order sign must be interpreted relative to a chosen operator lift/reference; it is not automatically a projective observable.

## 5. Independent finite-field extension: a multiplier-character law

For every odd prime field F_p, and any three pairwise nonorthogonal projective points, define

    M([u],[v],[w]) = Legendre(s(u,v)*s(v,w)*s(w,u)) in {+1,−1}.

Under independent projective rescalings, each vector appears twice and its scale enters squared; the Legendre sign is therefore well defined. For symplectic similitude g with s(gu,gv)=mu(g)s(u,v), the triangle sign transforms as

    M(g[u],g[v],g[w]) = Legendre(mu(g)) M([u],[v],[w]).

Random finite checks (500 attempts per prime, with invalid/orthogonal triples excluded) pass for p=3,5,7,11. In particular the transformation multiplier −1 flips the sign for p=3,7,11 but not p=5, because −1 is a nonsquare precisely for primes congruent to 3 mod 4. This illustrates how *finite-field arithmetic can make orientation a multiplier character*, not that p=3 is uniquely selected or that a physical fermion chirality/index has emerged. The construction is closely related to established finite symplectic/Maslov sign ideas; novelty claims require an independent literature audit.

## Reproduction

    python analysis/toe_20261120_symplectic_order_sic_switch.py
    python -m unittest discover -s tests -p test_toe_20261120_symplectic_order_sic_switch.py -v

Frozen certificate: data/toe_20261120_projective_switch_sic_certificate.json.

## What this changes in our TOE strategy

1. **Temporal order can be a *measurement resource*, not yet spacetime:** the path interference transduces a projective cocycle into a control phase. This is directly testable but does not derive physical time, locality, causal structure or gravitational dynamics.
2. **Projective incidence is insufficient for signed chirality:** use the oriented projective triple sign and make all gauge/lift choices explicit. A fermionic charged Dirac index is still necessary for actual 4D chirality.
3. **Demand operator-level certification:** a single attractive interference fringe is insufficient; the product-SIC frame provides a calibrated noncentrality certificate.
4. **Separate photonic SU(3) from physical colour gauge SU(3):** optical qutrits simulate its matrices. They are not colour charges. A real gauge-holonomy observable requires an appropriate charged Wilson line, physical sector and gauge-invariant reference. Local gauge transformations alone cannot be measured as matter observables.
5. **Return to physical falsifiability:** build a real programmable coherent-order setup, characterize loss and per-input visibility, then identify an experiment that specifically distinguishes our architecture from ordinary quantum mechanics. Counting W33 commutators or measuring the standard quantum-switch phase does not distinguish a TOE.

## Literature and repository comparisons

- Saniga/Planat et al., two-qutrit generalized Pauli geometry: https://arxiv.org/abs/quant-ph/0701211
- Photonic quantum switch and gate order phase measurement: https://doi.org/10.1103/PRXQuantum.2.010320
- Hesse SIC projectors and their conventional overlaps: https://pmc.ncbi.nlm.nih.gov/articles/PMC5627088/
- Experimental photonic qutrit SIC tomography: https://doi.org/10.1103/PhysRevX.5.041006
- Contemporary quantum switch higher-order causality caution: https://www.nature.com/articles/s42254-024-00739-8
- Existing repository W33 two-qutrit commutation (known), H27 center/SU3 colour quotient (known), and SU3 reference-dependent center detection (known) are all prior art, not newly invented by this packet.
