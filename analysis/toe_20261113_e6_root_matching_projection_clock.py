#!/usr/bin/env python3
"""Exact signed-E6 cubic clock audit: 36 orthogonal root matchings,
clock projection, 108-edge obstruction, torus 3-torsion census,
a sparse rank-12 compatible replacement and full Q(sqrt(3)) polynomial check.

Critically: the history->E6 address change conjugates BOTH rows and columns.
No prior uncommitted assistant results are assumed true.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
import sys,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_e6_root_matching_projection_clock.json"

def load():
    cert=json.loads((ROOT/"data/toe_20261108_exact_signed_cubic_stabilizer.json").read_text(encoding="utf-8"))
    original=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text(encoding="utf-8"))
    bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text(encoding="utf-8"))
    terms={tuple(sorted(map(int,r["triple"]))):(1 if int(r["sign"])%3==1 else -1) for r in original["solution"]["d_triples"]}
    assert len(terms)==45
    mapi=np.array([G.VID[tuple(map(int,bridge["maps"]["e6id_to_current_H27_address"][str(i)]))] for i in range(27)],dtype=int)
    assert sorted(mapi.tolist())==list(range(27))
    D=G.build()[2][np.ix_(mapi,mapi)].astype(np.int64)
    assert np.array_equal(D.T,-D) and np.array_equal(D@D@D,-27*D)
    assert int(np.trace(D.T@D))==216
    M=[]
    for records in cert["cubic_27"]["generators"]:
        x=np.zeros((27,27),dtype=np.int64)
        for i,j,v in records:x[i,j]=v
        M.append(x)
    assert len(M)==78
    diag=[x for x in M if np.count_nonzero(x-np.diag(np.diag(x)))==0]
    roots=[x for x in M if np.count_nonzero(x-np.diag(np.diag(x)))>0]
    assert len(diag)==6 and len(roots)==72
    return cert,terms,D,mapi,roots

def pack_roots(roots):
    seen={}
    for R in roots:
        assert np.array_equal(R@R,np.zeros((27,27),dtype=np.int64))
        K=R-R.T
        assert np.array_equal(K.T,-K)
        upper=tuple((i,j,int(K[i,j])) for i,j in combinations(range(27),2) if K[i,j])
        assert len(upper)==6
        if upper[0][2]<0:
            K=-K
            upper=tuple((i,j,-v) for i,j,v in upper)
        assert all(abs(z)==1 for _,_,z in upper)
        seen[upper]=K
    assert len(seen)==36
    ordered=sorted(seen.items())
    keys=[k for k,_ in ordered]
    Ks=[K for _,K in ordered]
    edges=Counter((i,j) for k in keys for i,j,_ in k)
    assert len(edges)==216 and set(edges.values())=={1}
    assert all(np.array_equal(K@K@K,-K) for K in Ks)
    assert all(int(np.trace(K.T@K))==12 for K in Ks)
    return keys,Ks

def inf_check(X,terms):
    coefficient=defaultdict(int)
    for triple,sgn in terms.items():
        for p,source in enumerate(triple):
            for target in np.flatnonzero(X[source]):
                tr=list(triple);tr[p]=int(target)
                coefficient[tuple(sorted(tr))]+=int(sgn)*int(X[source,target])
    residual={str(k):v for k,v in coefficient.items() if v}
    assert not residual,residual
    return len(coefficient)

def algebra(Ks):
    n=len(Ks)
    C=np.zeros((n,n,n),dtype=np.int32)
    active=0
    for i in range(n):
        for j in range(i+1,n):
            bracket=Ks[i]@Ks[j]-Ks[j]@Ks[i]
            if not np.any(bracket):continue
            active+=1
            reconstructed=np.zeros((27,27),dtype=np.int64)
            for k,K in enumerate(Ks):
                numerator=int(np.trace(K.T@bracket))
                assert numerator%12==0,(i,j,k,numerator)
                c=numerator//12
                if c:
                    C[i,j,k]=c
                    C[j,i,k]=-c
                    reconstructed+=c*K
            assert np.array_equal(bracket,reconstructed),(i,j)
    assert np.array_equal(C,-C.swapaxes(0,1))
    ad=[C[i,:,:].T.astype(np.int64) for i in range(n)]
    killing=np.array([[int(np.trace(ad[i]@ad[j])) for j in range(n)] for i in range(n)],dtype=np.int64)
    assert np.array_equal(killing,killing.T)
    eig=np.linalg.eigvalsh(killing)
    assert max(eig)<-1e-7,eig
    regular=[]
    rng=np.random.default_rng(20261113)
    for trial in range(20):
        h=rng.integers(-7,8,size=n)
        operator=sum((int(h[i])*ad[i] for i in range(n)),np.zeros((n,n),dtype=np.int64))
        r=int(np.linalg.matrix_rank(operator,tol=1e-8))
        regular.append(r)
    return {
      "dimension":36,
      "nonzero_pairs_of_basis_commutators":active,
      "bracket_closed_exact_integer":True,
      "killing_negative_definite":True,
      "killing_diagonal":np.diag(killing).tolist(),
      "killing_off_diagonal_nonzero_count":int(np.count_nonzero(killing-np.diag(np.diag(killing)))),
      "adjoint_ranks_trial":regular,
      "maximal_observed_adjoint_rank":max(regular),
      "generic_centralizer_dimension":36-max(regular),
      "bracket_nonzero_structure_coefficients":int(np.count_nonzero(C))}

def torus(cert):
    hs=cert["cubic_27"]["root_structure"]["simple_coroots"]
    assert len(hs)==6
    H=np.zeros((6,27),dtype=int)
    for k,entries in enumerate(hs):
        for i,j,v in entries:
            assert i==j
            H[k,int(i)]=int(v)
    groups=Counter()
    c3=0
    for phase in product(range(3),repeat=6):
        v=(np.asarray(phase,dtype=int)@H)%3
        mult=tuple(int(np.count_nonzero(v==a)) for a in range(3))
        groups[mult]+=1
        if mult==(19,4,4):c3+=1
    assert sum(groups.values())==729
    assert groups==Counter({(27,0,0):1,(0,27,0):1,(0,0,27):1,
                           (15,6,6):72,(6,15,6):72,(6,6,15):72,(9,9,9):510}),groups
    assert c3==0
    return {"torus_3_torsion_points_checked":729,
            "spectral_multiplicity_census":{"%d,%d,%d"%k:v for k,v in sorted(groups.items())},
            "original_spectrum":"19,4,4","original_trace":15,
            "original_trace_excluded_by_E6_order_three_torus":True,
            "possible_traces_in_27":["0","9","9omega","9omega^2",
                                    "27","27omega","27omega^2"],
            "scope":"Uses the certified coroot representation and maximal-torus conjugacy theorem for connected complex E6; a torus-point census is not a conjugacy-class census."}

def qmul(x,y):
    # (a+b sqrt3)/2 represented by (a,b) to minimize denominators;
    # pair product returns numerator for product with /4, not /2.
    a,b=x;c,d=y
    return (a*c+3*b*d,a*d+b*c)

def cubic_finite(K,terms):
    # 2V = A+sqrt3 B, A=2I+3K², B=K
    I=np.eye(27,dtype=np.int64)
    A=2*I+3*K@K
    B=K.copy()
    assert int(np.count_nonzero(A))<=27 and int(np.count_nonzero(B))==12
    coeff=defaultdict(lambda:[0,0])
    # N(V x) expands each 3-variable monomial with 1/8 denominators:
    for tri,sgn in terms.items():
        options=[]
        for row in tri:
            z=[(j,(int(A[row,j]),int(B[row,j]))) for j in range(27) if A[row,j] or B[row,j]]
            options.append(z)
        for ((i,u),(j,v),(k,w)) in product(*options):
            p=qmul(qmul(u,v),w)
            coeff[tuple(sorted((i,j,k)))][0]+=sgn*p[0]
            coeff[tuple(sorted((i,j,k)))][1]+=sgn*p[1]
    coeff={k:tuple(v) for k,v in coeff.items() if tuple(v)!=(0,0)}
    expected={k:(8*v,0) for k,v in terms.items()}
    assert coeff==expected,[(k,coeff.get(k),expected.get(k)) for k in set(coeff)|set(expected) if coeff.get(k)!=expected.get(k)][:10]
    M=A.astype(float)/2+math.sqrt(3)*B.astype(float)/2
    assert np.max(abs(M.T@M-I))<1e-13
    assert np.max(abs(M@M@M-I))<2e-13
    return M,{"finite_polynomial_identity_in_Qsqrt3":True,"45_monomials_exactly_preserved":True,
              "order_three":True,"matrix_M_is_orthogonal":True,
              "active_rotation_pairs":6,"untouched_E6_coordinates":15,
              "rotation_matrix_on_each_pair":"cos(2pi/3) I + sin(2pi/3) J, with J^2=-I",
              "finite_gate":"V=I+(sqrt3/2) K+(3/2) K²"}

def choi(M,mapi):
    # transport back into the 27 history-ordered tensor-product carrier,
    # keeping the distinction from the native E6 basis.
    inv=np.argsort(mapi)
    T=M[np.ix_(inv,inv)].reshape([3]*6)
    records=[]
    for abc in combinations(range(6),3):
        rest=tuple(i for i in range(6) if i not in abc)
        mat=T.transpose(abc+rest).reshape(27,27)
        r=int(np.linalg.matrix_rank(mat,tol=1e-9))
        gram=mat@mat.T
        purity=float(np.trace(gram@gram)/(27*27))
        maximally=bool(np.max(abs(gram-np.eye(27)))<1e-10)
        records.append({"cut":"".join(map(str,abc)),"schmidt_rank":r,"purity":round(purity,12),"maximally_mixed":maximally})
    return {"six_leg_choi_3by3_cuts":20,"maximally_mixed_cuts":sum(a["maximally_mixed"] for a in records),
            "schmidt_rank_census":dict(Counter(str(a["schmidt_rank"]) for a in records)),
            "cut_records":records,
            "boundary":"Tensor factorization is the original F3^3 history basis after inverse E6 address relabeling; basis-transport changes subsystem locality."}

def main():
    cert,terms,D,mapi,roots=load()
    keys,Ks=pack_roots(roots)
    assert all(not np.any(Ks[i]*Ks[j]) for i in range(36) for j in range(i+1,36))
    for K in Ks:inf_check(K,terms)
    edgesD={(i,j) for i,j in combinations(range(27),2) if D[i,j]!=0}
    assert len(edgesD)==108 and np.linalg.matrix_rank(D)==8
    overlaps=[sum(int(D[i,j])*v for i,j,v in key) for key in keys]
    local=[sum((i,j) in edgesD for i,j,_ in key) for key in keys]
    sq=sum(a*a for a in overlaps)
    norm_pro=Fraction(sq,3)
    assert norm_pro==Fraction(46,3),norm_pro
    residual=Fraction(216)-norm_pro
    assert residual==Fraction(602,3)
    assert not any(x==6 for x in local)
    assert any(x>0 and overlaps[j]!=0 for j,x in enumerate(local))
    best=min((6-n, -abs(overlaps[i]),i) for i,n in enumerate(local) if overlaps[i])
    chosen=best[2];K=Ks[chosen]
    assert not np.any(K+K.T) and np.array_equal(K@K@K,-K)
    # Projection has coefficients <D,K_i>/<K_i,K_i> = overlap_i/6.
    # Every root matching has six disjoint unordered edges.
    projected=sum((Fraction(overlaps[i],6) for i in range(36) if overlaps[i]),Fraction(0))
    assert projected.denominator in (1,2,3,6)
    algebra_data=algebra(Ks)
    torus_data=torus(cert)
    M,finite=cubic_finite(K,terms)
    choi_data=choi(M,mapi)
    report={
      "schema":"toe.e6.root_matching_projection_order3.v1",
      "status":"PASS_ROOT_PACKET_SKIPS_DENSE_PROJECTION_LINEAR_SOLVE",
      "coordinate_firewall":"D_E6 = D_history[np.ix_(E6_to_history,E6_to_history)] permutes BOTH axes",
      "root_system":{"72_noncartan_root_generators":len(roots),
                     "36_skew_root_pairs":len(Ks),
                     "each_pair_six_disjoint_two_coordinate_rotation_edges":True,
                     "total_root_packet_edges":216,
                     "different_root_packet_edges_never_overlap":True,
                     "remaining_skew_edges_outside_36_packet_span":351-216,
                     "root_packet_bracket":algebra_data},
      "original":{"rank":int(np.linalg.matrix_rank(D)),"undirected_null_edges":len(edgesD),
                  "frobenius_norm_squared":216,"original_gate_eigen_multiplicities":[19,4,4]},
      "projection":{"root_packet_overlaps_signed":overlaps,
                    "packet_null_edge_overlap_hist":dict(Counter(map(str,local))),
                    "sum_signed_overlap_squares":sq,
                    "compatible_projection_frobenius_norm_squared":str(norm_pro),
                    "residual_frobenius_norm_squared":str(residual),
                    "retained_fraction":str(norm_pro/Fraction(216)),
                    "exact_Frobenius_orthogonal":True,
                    "null_edge_supported_skew_cubic_kernel_dimension":0,
                    "null_edge_support_obstruction_proof":"Each compatible K is a linear combination of 36 orthogonal six-edge root packets with disjoint edge supports. No complete packet lies in the original 108-edge null graph, so the only compatible generator entirely supported there is zero."},
      "torus_census":torus_data,
      "replacement":{"chosen_packet_index":chosen,
                     "signed_overlap_with_D_on_upper_triangle":overlaps[chosen],
                     "matching_six_edges":[list(z) for z in keys[chosen]],
                     "overlap_edges_count":local[chosen],
                     "unavoidable_new_edges_for_this_root_generator":6-local[chosen],
                     "rank":int(np.linalg.matrix_rank(K)),
                     "finite_gate_eigen_multiplicities":[15,6,6],
                     "finite_gate_trace":9,
                     "infinitesimal_cubic_invariance_checked":True,
                     **finite},
      "holographic_comparison":choi_data,
      "boundary":"Within fixed Euclidean E6 address metric and 27D signed cubic; not an unqualified E6(6) spacetime model or demonstration of a physical field theory."
    }
    OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],
                      "root_packets":len(Ks),
                      "root_packet_commutators":algebra_data["nonzero_pairs_of_basis_commutators"],
                      "generic_centralizer":algebra_data["generic_centralizer_dimension"],
                      "projection":report["projection"]["compatible_projection_frobenius_norm_squared"],
                      "residual":report["projection"]["residual_frobenius_norm_squared"],
                      "packet_overlap_hist":report["projection"]["packet_null_edge_overlap_hist"],
                      "best_replacement_new_edges":report["replacement"]["unavoidable_new_edges_for_this_root_generator"],
                      "torus":report["torus_census"]["spectral_multiplicity_census"],
                      "choi_maximally_mixed":choi_data["maximally_mixed_cuts"]},indent=2,sort_keys=True),flush=True)
    return report
if __name__=="__main__":main()
