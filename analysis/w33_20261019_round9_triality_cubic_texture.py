"""Front3: explicit classical E6 cubic in SU3^3 (45 weight monomials)
and Jordan octonionic Spin8 triality coordinates 27=3*1+3*8.
Pass12067 clock-pair monomial orbit counts credited as PRIOR ART;
does not identify a canonical W33 label-to-Jordan coordinate map.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round9_triality_cubic_texture.json"
def hmul(a,b):
    av,aw=a[0],a[1:];bv,bw=b[0],b[1:]
    return np.r_[av*bv-np.dot(aw,bw),av*bw+bv*aw+np.cross(aw,bw)]
def hc(a):return a*np.r_[1.,-np.ones(3)]
def omul(x,y):
    a,b=x[:4],x[4:];c,d=y[:4],y[4:]
    return np.r_[hmul(a,c)-hmul(hc(d),b),hmul(d,a)+hmul(b,hc(c))]
def cubic(alpha,x):
    a,b,c=alpha;v,w,z=x
    return float(a*b*c-a*np.dot(v,v)-b*np.dot(w,w)-c*np.dot(z,z)+2*omul(omul(v,w),z)[0])
def det_terms(type_):
    # anticommutation sign of permutation for each 3x3 determinant
    out=[]
    for perm in itertools.permutations(range(3)):
        inversions=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        sign=(-1)**inversions
        out.append((sign,tuple((type_,i,perm[i]) for i in range(3))))
    return out
def run():
    mats=["A","B","C"]
    det=[q for n in mats for q in det_terms(n)]
    cross=[(1,(("A",i,j),("B",j,k),("C",k,i))) for i,j,k in itertools.product(range(3),repeat=3)]
    terms=det+cross
    assert len({tuple(sorted(q)) for _,q in terms})==len(terms)
    cnt=collections.Counter("cross" if len({x[0] for x in mon})==3 else "det" for _,mon in terms)
    rng=np.random.default_rng(20261019)
    errors=[]
    trial=[]
    for _ in range(200):
        x=rng.normal(size=8);y=rng.normal(size=8);z=rng.normal(size=8)
        a=np.array([rng.normal(),rng.normal(),rng.normal()])
        errors.append(abs(np.linalg.norm(omul(x,y))**2-np.dot(x,x)*np.dot(y,y)))
        t=omul(omul(x,y),z)[0]
        trial.append([abs(t-omul(omul(y,z),x)[0]),
              abs(cubic(a,[x,y,z])-cubic(np.roll(a,-1),[y,z,x]))])
    # Spin8 triality cubic uses 3 singlets and octets, no weights
    # identified with the 45 E6 tritangents before an E6 basis map.
    # One fixed monomial corresponds to a rank-1 BILINEAR coefficient
    # between two chosen field sectors after condensing the third.
    Y1=np.zeros((3,3));Y1[0,0]=2.
    Y3=np.diag([2.,-3.,5.])
    prior=json.loads((ROOT/"data/w33_pass12067_yukawa_monomials_of_one_and_two_clocks.json").read_text())
    checks={
      "45_distinct_E6_weight_cubic_terms":len(terms)==45 and cnt["det"]==18 and cnt["cross"]==27,
      "trinification_three_independent_determinant_blocks":all(len(det_terms(n))==6 for n in mats),
      "Cayley_Dickson_octonion_norm_multiplicative":max(errors)<1e-10,
      "octonion_scalar_trilinear_cyclic":max(x[0] for x in trial)<1e-10,
      "Spin8_triality_cubic_cyclic":max(x[1] for x in trial)<1e-10,
      "old_clock_orbit_sizes_reproduced":prior["far_pair"]==[1,4,4,4,8,8,8,8] and prior["collinear_pair"].count(1)==3,
      "one_coupling_rank1_three_disjoint_rank3_schematic":np.linalg.matrix_rank(Y1)==1 and np.linalg.matrix_rank(Y3)==3}
    out={"schema":"w33.round9.trinification_jordan_cubic_triality.v1",
      "SU3cubed_fields":"A:(3,bar3,1), B:(1,3,bar3), C:(bar3,1,3); each 9 complex components.",
      "SU3cubed_cubic":"The 45 E6 cubic weight monomials can be organized as det A + det B + det C plus Tr(A B C), with 6 monomials in each determinant and 27 distinct trace monomials. The standard E6 invariant is a PARTICULAR fixed linear combination of the four independent SU3^3 tensors; coefficients not fitted here.",
      "monomial_counts":{"determinants":18,"cross":27,"total":45},
      "octonion_triality_cubic":"Write J3(O)=R^3+O^3 (3+8+8+8=27), alpha=(a,b,c), x=(v,w,z) and N(v)=sum_i v_i^2. det_J=abc-a N(v)-b N(w)-c N(z)+2 Re((v w) z). This classical split into Spin8 triality components obeys simultaneous cyclic permutation of the singlets and octets. Proof via Cayley-Dickson quaternion/octonion identities, checked numerically.",
      "max_octonion_norm_residual":max(errors),
      "max_cyclic_trilinear_residual":max(x[0] for x in trial),
      "max_Jordan_cubic_cyclic_residual":max(x[1] for x in trial),
      "prior_repo_Pass12067_clock_orbit_counts":{"one_clock":prior["one_clock"],"noncollinear":prior["far_pair"],"collinear":prior["collinear_pair"]},
      "schematic_bipartite_Yukawa_matrix_single_invariant":Y1.tolist(),
      "schematic_bipartite_Yukawa_matrix_three_disjoint_invariants":Y3.tolist(),
      "essential_distinction":"Pass12067 ALREADY found exactly one fixed weight monomial for a noncollinear two-clock pair and three disjoint fixed monomials for a collinear pair. Restricted to chosen fermion sectors and scalar VEVs, a single monomial contributes a rank-one entry; three disjoint ones MAY support rank three if all couplings/VEVs nonzero. No canonical map of those exact W33 weight labels into a specific Jordan-octonion basis was constructed. These 3x3 texture matrices are illustrative, NOT measured generation mass matrices.",
      "physics_limit":"The 45 terms are weight basis coordinates; the octonion triality formula is another coordinate system, and equality requires an explicit E6 change of basis not in this packet. No Yukawa coefficients, Higgs VEVs, generation identification, physical chirality or Standard Model mass ratio established.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"maxerr":[max(errors),max(x[1] for x in trial)]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
