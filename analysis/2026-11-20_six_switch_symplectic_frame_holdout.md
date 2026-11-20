# Six-setting qutrit order-interference reconstruction — with a nonlinear-device falsifier

**Date:** 2026-11-20. **Scope:** follow-up to analysis/2026-11-20_temporal_order_projective_chirality_sic.md and executable analysis/toe_20261120_symplectic_order_sic_switch.py. Mathematical results are standard finite symplectic linear algebra applied to a proposed optical audit, not new laws of nature.

## Reduce the apparent 780-pair task

Let e0,e1,e2,e3 be an explicitly calibrated basis of F3^4. A symplectic pairing is specified by an alternating 4x4 matrix J, with exactly six independent upper-triangular entries J_ab. For a *promised* Weyl representation W(u), coherent order interference gives

    c(u,v)=Tr[W(u)W(v) rho (W(v)W(u))†]=omega^(u^T J v).

Measuring the six pairs (ea,eb) reconstructs J; then all 780 unordered pairs of the 40 projective labels are predictable without an additional fitted parameter. For the repo's canonical J, only J02=J13=1 (other upper-triangle entries zero), but we explicitly tested **arbitrary scrambled invertible bases** rather than relying on that known coordinate form.

The Python producer generates 24 independent invertible GL4(F3) basis frames, builds their actual two-qutrit Weyl gates, reconstructs all six commutation phases, and checks 780 pair predictions in each frame: **18,720** checked pairs, maximum matrix commutator discrepancy 2.01e-15.

## Pfaffian gate: rejecting spurious degenerate geometry

For an alternating 4x4 matrix whose six upper entries are (a,b,c,d,e,f), its Pfaffian is

    pf(J)=a*f - b*e + c*d mod 3;
    det(J)=pf(J)^2 mod 3.

There are 3^6=729 alternating forms over F3. Precisely 261 are singular and **468 nondegenerate**. Proof: group coefficients as x=(a,b,c), y=(f,−e,d), so pf=x·y. For x=0 there are 27 zero products; for each of 26 nonzero x there are 9 orthogonal y, yielding 27+26*9=261 singular forms. The code exhaustively enumerates all 729 possibilities and checks the count. All nondegenerate alternating forms in four dimensions are isomorphic under a linear coordinate change: their multiplicity is not a physical family prediction.

## Finite-shot certificate under explicit calibration

For six basis pairs, read out two independent +/-1-valued control quadratures for each (real and imaginary phase). If visibility v is independently bounded below by 0.8 and the uncontrolled phase offset by 0.1 radians, the minimum distance from the true complex expectation to the nearest wrong angular classification region is

    rho = 0.8*sin(pi/3 - 0.1) = 0.6494257405429492.

Use each quadrature N times and a union of Hoeffding bounds over 12 real sample means. With probability at least 1−delta,

    max_real_coordinate_error <= sqrt(2 log(24/delta)/N)

and each complex amplitude has error <=sqrt(2) times that bound. To ensure angle classification never crosses the nearest of the 3 equally spaced phase sectors, choose a 0.99 safety multiplier on rho, yielding

    N >= 4 log(24/delta)/(0.99*rho)^2.

At delta=.01 this gives **N=76 accepted shots per quadrature**, so six pairs x two quadratures require **912 accepted shots** in total. This is a deliberately conservative *conditional* shot count. It excludes attempts lost to postselection, drift outside the independent calibration, state preparation errors and non-IID sampling. A seeded 2,000-trial simulation of independent drift and visibility within the assumptions produced zero failures; the mathematical union bound, not that simulation, supplies the stated confidence guarantee.

## Failure mode: a malicious or physically nonlinear address map can fake all six

Six commutator phases identify the form only if the hardware **already obeys the Weyl/additive-label representation law**. They do not independently certify that law.

Construct an antisymmetric fake table

    f(u,v)=s(u,v) + u0*u1*v2 - v0*v1*u2  (mod 3).

For each of the six basis-vector pairs, the extra term vanishes, so ALL calibrations return the honest J. However with u=e0+e1, v=e2 the bilinear prediction is s(u,v)=1 while the fake table gives f(u,v)=2. One explicit composite-word holdout detects the mismatch. This is a *data falsifier*: the fake table need not arise from a globally consistent projective group representation, which is exactly why the device's representation assumption cannot be silently inferred from six points.

A meaningful physical demonstration must therefore calibrate six basis pairs, verify nondegeneracy, then test additional compound displacements W(u+v) versus W(u)W(v) up to central phase, including multiple independently chosen holdouts and drift/SPAM consistency checks. To certify black-box indefinite causal order, use a separate appropriate causal witness. A known-gate optical circuit reproducing predicted interference alone is insufficient.

## Physical implications and hard boundary

This compresses an **operational test of the already-known two-qutrit commutation algebra**. It does not reduce the QEC code's physical qutrit count, derive particle masses, determine Minkowski time, or measure physical QCD colour. It is a potentially inexpensive falsifiable *geometry-to-phase testbed* for the Information System's proposed relation between interaction ordering and finite symplectic geometry.

**Reproduce:**

    python analysis/toe_20261120_six_switch_symplectic_frame.py
    python -m unittest discover -s tests -p test_toe_20261120_six_switch_symplectic_frame.py -v

Frozen output: data/toe_20261120_six_switch_symplectic_frame.json.

References: https://arxiv.org/abs/quant-ph/0701211 ; https://doi.org/10.1103/PRXQuantum.2.010320 . Prior repo machinery: analysis/toe_20261120_symplectic_order_sic_switch.py.
