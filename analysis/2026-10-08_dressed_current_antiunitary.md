# 2026-10-08 — Hidden dressed antiunitary of the exact W33 current Hamiltonian

**Status: exact algebraic construction, 160/160 integer incidence checks.** This explicitly refines the companion canonical-K firewall. Bare complex conjugation breaks the proposed dynamics; a different, *dressed* antiunitary preserves it exactly. No emergent physical time arrow or observed CPT/CP statement follows.

## Input and provenance

Use Pass11767's W33 point-line Levi incidence set (40 points, 40 lines, 160 flags) and Pass11769's proposed represented current energy on the 78-dimensional real configuration carrier

W = {q in R^80 : sum(point coordinates)=sum(line coordinates)=0},

with [q_i,p_j]=i delta_ij on W and

    U_e=P_W(e_point + e_line),  V_e=P_W(e_point - e_line),
    a=1/sqrt(20),  J_e=(V_e.q+a)(U_e.p+a),  H=sum_e J_e^2.

The two factors of each current commute because U_e.V_e=0.

## The hidden symmetry

Let D=diag(+I_40,-I_40) on the point/line coordinate blocks. Since D exchanges the constant vector u=(1,...,1) and the bipartition sign vector s=(ones40,-ones40), it preserves W and restricts to an orthogonal involution on W. Moreover D P_W=P_W D. Therefore, **for every actual incidence**

    D U_e=V_e,    D V_e=U_e.

The linear phase-space involution

    S(q,p)=(D p,D q)

is **anti-symplectic**, not symplectic: S^2=1 and S^T Omega S=-Omega, with Omega((q,p),(q',p'))=q.p'-p.q'. By the standard Fourier implementation there is an antiunitary on L2(W):

    (T psi)(q)=(2*pi)^(-dim(W)/2) integral_W exp(i q.D x) conj(psi(x)) dx.

Here dim(W)=78, so the coefficient is (2*pi)^(-39). As D^2=I, Fourier inversion gives T^2=I on Schwartz functions (then by extension). T q T^-1=D p and T p T^-1=D q. Consequently

    T J_e T^-1=(U_e.p+a)(V_e.q+a)=J_e,
    T H T^-1=H.

Each current, not just the summed Hamiltonian, is invariant. The Friedrichs extension also commutes with T, since the invariant nonnegative quadratic form determines it.

The verifier checks D U_e=V_e, D V_e=U_e, U_e.V_e=0 and the 40+40 incidence degrees for all 160 rows, with exactly integral numerators (scaled by 40). It verifies the 78-dimensional projected block carrier and D orthogonality.

## Why this changes the physical reading

The companion *bare* K test remains valid:

    K:q->q,p->-p;
    H-K H K^-1 = 4a sum_e (V_e.q+a)^2 (U_e.p) !=0,

with 1560 exact ordered-pair witnesses and classical symbol difference 1/25. But this **does not imply that H intrinsically breaks time reversal**, because T above is a distinct antiunitary symmetry. Thus the Pass11769 optimized Gaussian phase f<0 is not evidence for a dynamically selected arrow in a T-asymmetric microscopic law. T maps the Gaussian into a different correlated state in general; it need not remain inside the selected two-parameter ansatz.

This does not identify T with **physical** spacetime time reversal, and does not imply observed weak CP/CPT. D is a sign operation on types of internal *Levi coordinates*, not a nonexistent point-line incidence duality of W(3,3) at odd q. A physical interpretation requires a specified observable algebra, dynamical localization and coupling to measured fields. It remains open whether the ground-state sector is gapped, normalizable, degenerate or thermodynamically irreversible under coarse graining.

**Reproduction:** `python analysis/w33_20261008_dressed_current_antiunitary.py`; regression `tests/test_w33_20261008_dressed_current_antiunitary.py`. The distinction between an exact algebraic antiunitary and its physical interpretation is a mandatory boundary.
