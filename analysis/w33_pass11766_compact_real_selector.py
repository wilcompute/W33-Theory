#!/usr/bin/env python3
"""Pass 11766: compact-real shell/Weyl projector obstruction and a minimal real-linear repair.

This is a representation-theoretic scope correction. Its proposed auxiliary
complex structure is an EXTRA FIELD INPUT, not an E8-derived chiral measure.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS11766_COMPACT_REAL_SELECTOR.json"
C = s.Rational(15, 343)
J = s.Matrix([[0, -1], [1, 0]])
I2 = s.eye(2)


def hash_source(path):
    b = (ROOT / path).read_bytes()
    if path.endswith(".json"):
        b = json.dumps(json.loads(b.decode()), sort_keys=True, separators=(",", ":")).encode()
    else:
        b = b.replace(b"\r\n", b"\n")
    return hashlib.sha256(b).hexdigest()


def real_e8_grade_audit():
    """The canonical real 2-plane of an order-three orthogonal E8 adjoint action.

    Its global multiplicities 86 + 81 + 81 are certified by earlier E8 work.
    This calculation is the exactly equivalent real rotation-plane normal form,
    not an explicit reconstruction of all 248 E8 root operators.
    """
    U = -s.Rational(1, 2)*I2 + s.sqrt(3)/2*J
    assert U.T*U == I2 and U**3 == I2
    A = s.simplify((U - U.T)/(s.I*s.sqrt(3)))
    assert A == -s.I*J
    assert A*A == I2 and A.H == A
    assert s.conjugate(A) == -A
    plus = (I2 + A)/2
    minus = (I2 - A)/2
    assert plus*plus == plus and minus*minus == minus
    assert plus*minus == s.zeros(2)
    assert s.conjugate(plus) == minus
    assert plus.rank() == minus.rank() == 1

    # A real vector cannot live in just one of the two complex grades.
    # If P+ v=0 for a real v then conjugation forces P- v=0, hence v=0.
    x, y = s.symbols("x y", real=True)
    v = s.Matrix([x, y])
    assert (s.conjugate(plus*v) - minus*v).applyfunc(s.simplify) == s.zeros(2, 1)
    assert s.simplify(plus + minus) == I2

    # The Hesse-fixed-vacuum shell filter is complex-linear Hermitian but
    # cannot preserve the original compact real form for nonzero W.
    Hc = s.expand(C**2)*(I2 + A)**2
    assert Hc.H == Hc and s.simplify(Hc-4*C*C*plus) == s.zeros(2)
    assert s.conjugate(Hc) != Hc
    assert s.simplify(s.conjugate(Hc)-4*C*C*minus) == s.zeros(2)

    # No real symmetric nontrivial projector commutes with the order-3
    # irreducible rotation plane: its real commutant is a I + b J, and
    # the symmetric part has b=0.
    a, b, cc, dd = s.symbols("a b cc dd", real=True)
    X = s.Matrix([[a, b], [cc, dd]])
    comm = X*J-J*X
    assert comm == s.Matrix([[b+cc, dd-a], [dd-a, -b-cc]])
    assert s.simplify(X-X.T).shape == (2, 2)

    # Add one independent real complex-structure plane.
    S = s.kronecker_product(J,J)
    U2 = s.kronecker_product(U,I2)
    F = s.diag(1,-1)
    R = s.kronecker_product(F,I2)
    assert S.T == S and S*S == s.eye(4)
    assert S*U2 == U2*S and R*S*R == -S
    Pp, Pm = (s.eye(4)+S)/2, (s.eye(4)-S)/2
    assert Pp.rank() == Pm.rank() == 2
    assert Pp == Pp.T and Pm == Pm.T

    # At W=+/- C rho^6, the compact-real filter is positive and leaves
    # one REAL 2-dimensional subspace per original real rotation plane.
    rows = []
    for sign in (+1,-1):
        HH = (C*s.eye(4) + sign*C*S)**2
        expected = 4*C*C * (Pp if sign == 1 else Pm)
        assert s.simplify(HH-expected) == s.zeros(4)
        assert s.simplify(HH.T-HH) == s.zeros(4)
        rows.append(dict(W_sign=sign, matter_kernel_real_dimension=81*2,
                         matter_gapped_real_dimension=81*2,
                         neutral_kernel_real_dimension=86*2,
                         matter_gap_over_lambda_rho12=str(4*C*C)))

    return dict(
        status="PASS_REAL_FORM_OBSTRUCTION_AND_AUXILIARY_PLANE_REPAIR",
        compact_real_E8_adj_dimension=248,
        complexified_branching="86 + 81_(omega) + 81_(omega^2)",
        compact_real_branching="86 fixed real + 81 real rotation planes",
        one_shell_complex_projector="P_plus=(M+C)/2, P_minus=(M-C)/2; conjugation interchanges them",
        real_kernel_obstruction="(ker P_plus) intersect real grade-plane = {0}, likewise for ker P_minus; selecting only one 81-dimensional complex shell cannot act on a nonzero real adjoint matter vector",
        original_filter_reality="Fixed-vacuum H_shell=(c M+W C)^2 is Hermitian on V_C but fails to map the compact real V_R into itself whenever cW != 0",
        minimal_real_commutant="End_R(R^2) commuting with order-3 rotation = R[I,J]; symmetric part = R I; no rank-one real symmetric grading projector",
        extra_input="one independent real 2-plane carrying J_aux^2=-I",
        repair="S=J_E8 tensor J_aux; S is real symmetric, S^2=M tensor I, commutes with the grading, and flips under CP reflection of J_E8",
        real_filter="H_real=lambda[c rho^6 (M tensor I) + W S]^2 with c=15/343",
        real_total_dimension=248*2,
        doubled_neutral_dimension=86*2,
        doubled_matter_dimension=162*2,
        vacuum_rows=rows,
        boundary="The repaired 162-real-dimensional light matter space can be endowed with the auxiliary complex structure to count as 81 complex coordinates, but this requires an independent complex-field/spectator structure and is NOT obtained by projecting the original real E8 adjoint alone. Full E8 covariance is not asserted (only its E6 x SU3 grading centralizer); chiral fermion measure and anomalies remain open."
    )


def spin10_real_audit():
    gd = json.loads((ROOT/"data/w33_pass10961_albert_clifford9_gammas.json").read_text())
    gamma9 = [s.Matrix([[s.Rational(v) for v in row] for row in M]) for M in gd["gamma9"]]
    I16, Z16 = s.eye(16), s.zeros(16)
    gam = [
        s.Matrix.vstack(s.Matrix.hstack(Z16, x), s.Matrix.hstack(x, Z16))
        for x in gamma9
    ] + [s.diag(I16, -I16)]
    I32 = s.eye(32)
    V = I32
    for g in gam:
        assert g == s.conjugate(g)
        V = V*g
    assert V.T == -V and V*V == -I32
    chi = s.I*V
    assert chi*chi == I32 and chi.H == chi
    assert s.conjugate(chi) == -chi
    Pp, Pm = (I32+chi)/2, (I32-chi)/2
    assert s.conjugate(Pp) == Pm
    assert Pp.rank() == Pm.rank() == 16
    for i,j in itertools.combinations(range(10),2):
        B=gam[i]*gam[j]
        assert B*V == V*B
    assert gam[9]*V*gam[9] == -V

    # A second real complex-structure plane converts imaginary chi
    # into a real self-adjoint involution on the doubled carrier.
    S=s.kronecker_product(V,J)
    I64=s.eye(64)
    assert S.T == S and S*S == I64
    assert s.kronecker_product(gam[9],I2)*S*s.kronecker_product(gam[9],I2) == -S
    assert (I64+S).rank() == (I64-S).rank() == 32

    rows=[]
    for sign in (+1,-1):
        H=(C*I64+sign*C*S)**2
        assert s.simplify(H-2*C*C*(I64+sign*S))==s.zeros(64)
        rows.append(dict(W_sign=sign, light_real_dimension=32,
                         heavy_real_dimension=32,
                         light_complex_dimension_given_aux_structure=16,
                         gap_over_lambda_rho12=str(4*C*C)))
    return dict(
        status="PASS_REAL_CLIFFORD32_WEYL_PROJECTOR_REQUIRES_COMPLEX_STRUCTURE",
        actual_gamma_count=len(gam),
        Clifford_volume="V=Gamma_1...Gamma_10, real skew, V^2=-I",
        chirality="Chi=i V, purely imaginary Hermitian involution",
        conjugate_Weyl_spaces="ordinary complex conjugation exchanges Chi=+1 and Chi=-1",
        compact_real_obstruction="Neither complex Weyl-16 projector preserves the 32-real-dimensional Clifford carrier; its image intersects that original real space trivially when considered as a single pure Weyl eigenspace",
        gauge_invariance="V commutes with all 45 Spin10 bivectors",
        repaired_real_involution="S=V tensor J_aux, real symmetric with S^2=I on R^64; commutes with the bivector gauge action",
        repaired_vacuum_rows=rows,
        caution="Conjugation by the REAL Gamma_10 has the same adjoint action on Chi as the complex two-tick clock i Gamma_10, but is not the same spinor operator. The doubled structure introduces extra real degrees of freedom and is not a derived physical chiral fermion measure."
    )


def produce():
    result=dict(status="PASS11766_REALITY_FIREWALL_WITH_MINIMAL_AUXILIARY_COMPLEX_STRUCTURE",
                pass_number=11766, reservation="7a8a13721d4f7ae45d6776b458b822b2bf82f71a",
                E8=real_e8_grade_audit(), Spin10=spin10_real_audit())
    sources=[
      "analysis/w33_pass11608_11613_chiral_unification.py",
      "analysis/w33_pass11607_hesse_cp_weyl_selector.py",
      "analysis/w33_pass11593_unique_weyl_selector.py",
      "data/w33_pass10961_albert_clifford9_gammas.json",
      "analysis/2026-09-21_e8_a2_center_vs_coxeter_order3.md"
    ]
    result["source_sha256"]={p:hash_source(p) for p in sources}
    result["producer_sha256"]=hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n",b"\n")).hexdigest()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return result

if __name__=="__main__":
    produce()
