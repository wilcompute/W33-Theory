"""Compute the TWO 27-element unipotent radicals of W33 point/line parabolics.

The projective symplectic PSp4(3) point stabilizer and isotropic-line
stabilizer both have order648. Their O_3 normal subgroups have order27 but
need NOT be isomorphic: Heisenberg for points vs C3^3 for lines.
All groups reconstructed from native symplectic transvections.
"""
import json,sys
from pathlib import Path
from collections import Counter
import sympy as S
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W


def unipotent_radical(parabolic):
    H=list(parabolic.generate_schreier_sims())
    syl=parabolic.sylow_subgroup(3)
    Sp=list(syl.generate_schreier_sims())
    Sset=set(Sp)
    assert len(H)==648 and len(Sp)==81
    # Core of a Sylow subgroup is the largest normal p-subgroup O_p(H).
    core=[g for g in Sp if all(h*g*~h in Sset for h in H)]
    C=set(core)
    assert all(g*h in C for g in core for h in core)
    assert all(h*g*~h in C for g in core for h in H)
    center=[g for g in core if all(g*h==h*g for h in core)]
    comm={g*h*~g*~h for g in core for h in core}
    ordercounts=Counter(int(g.order()) for g in core)
    return dict(parabolic_order=len(H),Sylow3_order=len(Sp),
                O3_order=len(C),O3_center_order=len(center),
                O3_derived_order=len(comm),
                O3_element_order_counts={str(k):v for k,v in sorted(ordercounts.items())}),core


def certify_qutrit(K):
    """Construct faithful irreducible dimension-three clock/shift representation."""
    pair=next((x,y) for x in K for y in K if x*y!=y*x)
    x,y=pair
    z=x*y*~x*~y
    assert z.order()==3 and all(z*g==g*z for g in K)
    forms={x**a*y**b*z**c for a in range(3) for b in range(3) for c in range(3)}
    assert forms==set(K)
    om=-S.Rational(1,2)+S.sqrt(3)*S.I/2
    X=S.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    Z=S.diag(1,om,om**2)
    assert X**3==S.eye(3) and S.simplify(Z**3-S.eye(3))==S.zeros(3)
    assert S.simplify(X*Z*X**2*Z**2 - om**2*S.eye(3))==S.zeros(3)
    images=[S.simplify(X**a*Z**b*om**(2*c)) for a in range(3)
            for b in range(3) for c in range(3)]
    # Pairwise distinct exact matrices; traces of noncentral elements vanish.
    assert len({tuple(M) for M in images})==27
    for a in range(3):
        for b in range(3):
            if a or b:
                assert S.simplify(S.trace(X**a*Z**b))==0
    # The commutant of noncommuting clock and shift is only scalar matrices.
    # Hence the 3-dimensional representation is irreducible over C.
    A=S.kronecker_product(S.eye(3),X)-S.kronecker_product(X.T,S.eye(3))
    B=S.kronecker_product(S.eye(3),Z)-S.kronecker_product(Z.T,S.eye(3))
    assert A.col_join(B).rank()==8
    return dict(point_radical_generators="x^3=y^3=z^3=1; z=[x,y] central; all x^a y^b z^c distinct",
                native_order27_elements=27,
                center_commutator_order=3,
                explicit_qutrit_shift_X=[[int(v) for v in row] for row in X.tolist()],
                explicit_qutrit_clock_Z_diagonal=["1","omega","omega^2"],
                omega="exp(2*pi*i/3)",
                qutrit_clock_shift_commutator="X Z X^-1 Z^-1 = omega^2 I3",
                qutrit_Pauli_group_order=27,
                commutant_dimension=1,
                is_irreducible=True,
                conclusion="Point-parabolic H27 has a verified faithful irreducible 3-dimensional Schroedinger/clock-shift model. The line-parabolic C3^3 is distinct and commuting; this is not an identification of physical photons or a unique E6 operator representation.")


def run():
    graph,points,lines=W.levi()
    pidx={p:i for i,p in enumerate(points)}
    lidx={l:i for i,l in enumerate(lines)}
    gp=[];gl=[]
    for v in points:
        point_perm=[pidx[W.projective(tuple((x[k]+W.symplectic(x,v)*v[k])%3
                                                   for k in range(4)))] for x in points]
        line_perm=[lidx[tuple(sorted(point_perm[i] for i in line))]
                   for line in lines]
        gp.append(Permutation(point_perm))
        gl.append(Permutation(line_perm))
    Gp=PermutationGroup(gp);Gl=PermutationGroup(gl)
    assert Gp.order()==Gl.order()==25920
    op,Up=unipotent_radical(Gp.stabilizer(0))
    ol,Ul=unipotent_radical(Gl.stabilizer(0))
    qutrit=certify_qutrit(Up)
    assert op["O3_order"]==ol["O3_order"]==27
    assert op["O3_center_order"]==op["O3_derived_order"]==3,op
    assert op["O3_element_order_counts"]=={"1":1,"3":26},op
    assert ol["O3_center_order"]==27 and ol["O3_derived_order"]==1,ol
    assert ol["O3_element_order_counts"]=={"1":1,"3":26},ol
    out=dict(status="PASS",group="PSp(4,3)",group_order=25920,
             point_parabolic=dict(op,identification="nonabelian extraspecial Heisenberg H27 of exponent3"),
             qutrit_Schrodinger=qutrit,
             isotropic_line_parabolic=dict(ol,identification="elementary Abelian C3^3"),
             core_proof="Core of any Sylow-3 subgroup is O_3(H); enumerated all 648 parabolic elements and tested the 81 Sylow elements under conjugation.",
             fundamental_distinction="The point-parabolic radical is noncommutative H27 (center C3, commutator C3); the line-parabolic radical is the commuting additive Sym^2(F3^2)=F3^3 (center all27). These are distinct but dual-parabolic 27-address/operator geometries inside the SAME W33 group.",
             caution="This is exact finite-group geometry, not an identification of physical spacetime, particle charges, or a unique quantization. Extra identifications with the cubic-surface regular H27 or E6 trinification H27 require an explicit equivariant intertwiner.")
    dest=ROOT/"data/toe_20261118_W33_dual_parabolic_radicals_27.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__":run()
