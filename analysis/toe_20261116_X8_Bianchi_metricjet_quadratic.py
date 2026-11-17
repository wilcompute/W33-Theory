"""Second-order gravitational X8 variation with a Bianchi-valid metric 2-jet.

Old X8 audit found first curvature variation identically zero but its
second variation need not. Its chosen deltaR was an unconstrained
so(11)-valued 2-form. Here deltaR is an algebraic RIEMANN tensor,
constructed as a sum of Kulkarni–Nomizu products of symmetric forms.
It obeys antisymmetry in both index pairs, pair exchange symmetry,
and the first algebraic Bianchi identity. Any such algebraic
curvature tensor occurs as the linear curvature perturbation at a
point of a suitable local metric normal-coordinate 2-jet (when
the background metric is fixed at that point).

This is a LOCAL metric-jet existence result; the metric perturbation
does NOT solve linearized 11D supergravity or global boundary data.
"""
from pathlib import Path
import json,sys
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261116_11D_X8_nilpotent_variation as x
from toe_20261116_fivefront_exact_negative_controls import t4_polynomial,add_matrices,add_forms,scale_form
OUT=ROOT/"data"/"toe_20261116_X8_metricjet_Bianchi_secondvariation.json"
N=11

def forms():
    # Two independently supported four-dimensional algebraic
    # Kulkarni-Nomizu tensors; each combines two AdS5 directions with
    # two directions from a distinct S2 factor.
    sympairs=[((0,5),(1,6)),((2,7),(3,8))]
    S=[]
    for spair,tpair in sympairs:
        s=[[0]*N for _ in range(N)]
        t=[[0]*N for _ in range(N)]
        i,j=spair;k,l=tpair
        s[i][j]=s[j][i]=1
        t[k][l]=t[l][k]=1
        S.append((s,t))
    def riem(a,b,c,d):
        out=0
        for s,t in S:
            out+=s[a][c]*t[b][d]+t[a][c]*s[b][d]-s[a][d]*t[b][c]-t[a][d]*s[b][c]
        return out
    # Check complete algebraic Riemann symmetries, including Bianchi.
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    v=riem(a,b,c,d)
                    assert v==-riem(b,a,c,d)
                    assert v==-riem(a,b,d,c)
                    assert v==riem(c,d,a,b)
                    assert v+riem(a,c,d,b)+riem(a,d,b,c)==0
    D=[[{} for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(c+1,N):
                    v=riem(a,b,c,d)
                    if v:
                        f=x.form(c,d)
                        assert len(f)==1
                        mask,sign=next(iter(f.items()))
                        D[a][b][mask]=D[a][b].get(mask,0)+v*sign
    # Matrix curvature variation has zero diagonal and opposite
    # offdiagonal 2forms, as required by Euclidean orthonormal frame.
    for i in range(N):
        assert not D[i][i]
        for j in range(N):
            assert D[i][j]==scale_form(D[j][i],-1)
    return D

def verify():
    R=x.curvature()
    D=forms()
    assert not t4_polynomial(R)
    RD=x.multiply(R,D)
    quadratic=add_forms(
       scale_form(x.trace(x.multiply(x.multiply(RD,R),D)),2),
       x.wedge(x.trace(RD),x.trace(RD)),-1)
    assert quadratic
    # Numeric t=+1,-1 and t=0 check the exact quadratic coefficient,
    # subtracting pure quartic deltaR contribution.
    symmetric=add_forms(t4_polynomial(add_matrices(R,D)),
                        t4_polynomial(add_matrices(R,D,-1)))
    symmetric=add_forms(symmetric,t4_polynomial(D),-2)
    symmetric=add_forms(symmetric,t4_polynomial(R),-2)
    finite=scale_form(symmetric,Fraction(1,2))
    assert finite==quadratic
    return {"status":"PASS_NONZERO_X8_SECOND_VARIATION_FOR_BIANCHI_VALID_METRIC_JET",
      "spacetime_dimension":N,
      "algebraic_curvature_tensor_first_Bianchi_passed":True,
      "index_pair_antisymmetry_and_pair_exchange_passed":True,
      "local_metric_normal_coordinate_2jet_realizability":True,
      "pointwise_X8_background_zero":True,
      "all_first_curvature_X8_variations_zero":True,
      "quadratic_X8_nonzero":True,
      "second_variation_coefficient_by_8form_mask":{str(mask):str(c) for mask,c in quadratic.items()},
      "independent_t_plusminus_finite_difference_passed":True,
      "mathematical_not_physical":"A local metric 2-jet can have this algebraic curvature variation; it is not a physical propagating metric-C3 eigenmode, not a global perturbation solving the EOM, and no physical eight-derivative action or BF shift is computed.",
      "Weyl_or_Ricci_note":"No claim that this perturbation is Ricci-flat, transverse traceless, preserves product symmetries or obeys 11D constraints."}
if __name__=="__main__":
    v=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(v["status"],len(v["second_variation_coefficient_by_8form_mask"]))
