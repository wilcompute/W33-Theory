#!/usr/bin/env python3
"""W33 40-qutrit code: exact Loewy logical geometry, optimal checks, decoder.

This extends, without re-claiming, the previously established [40,11,13]_3
and [40,10,18]_3 classical codes and the 40-qutrit [[40,19,4]]_3 CSS code.
No hardware, threshold, or fault-tolerant ancilla circuit is established.
"""
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_w33_40_qutrit_css as source
import toe_20261119_w33_code_gate_and_decoder as parallel_decoder


def rref_pivot(M):
    a=np.array(M,dtype=np.int64,copy=True)%3
    piv=[];r=0
    for col in range(a.shape[1]):
        q=next((i for i in range(r,a.shape[0]) if a[i,col]),None)
        if q is None: continue
        a[[r,q]]=a[[q,r]]
        a[r]=(a[r]*(1 if a[r,col]==1 else 2))%3
        for i in range(a.shape[0]):
            if i!=r and a[i,col]:a[i]=(a[i]-int(a[i,col])*a[r])%3
        piv.append(col);r+=1
        if r==a.shape[0]:break
    return a[:r],piv


def kernel_basis(M):
    R,piv=rref_pivot(M)
    free=[j for j in range(M.shape[1]) if j not in piv]
    res=[]
    for j in free:
        v=np.zeros(M.shape[1],dtype=np.int64);v[j]=1
        for row,c in enumerate(piv):v[c]=(-R[row,j])%3
        res.append(v)
    return np.array(res,dtype=np.int64)


def det_mod3(M):
    a=np.array(M,dtype=np.int64,copy=True)%3
    n=a.shape[0];det=1
    for c in range(n):
        j=next((j for j in range(c,n) if a[j,c]),None)
        if j is None:return 0
        if j!=c:a[[c,j]]=a[[j,c]];det=(-det)%3
        p=int(a[c,c]);det=det*p%3
        a[c]=(a[c]*(1 if p==1 else 2))%3
        for j in range(c+1,n):
            if a[j,c]:a[j]=(a[j]-int(a[j,c])*a[c])%3
    return int(det)


def logical_middle_layer(HX,HZ):
    C10=source.rref_mod3(HZ).astype(np.int64)
    C11=source.rref_mod3(HX).astype(np.int64)
    one=np.ones(40,dtype=np.int64)
    assert C10.shape==(10,40) and C11.shape==(11,40)
    assert np.array_equal(source.rref_mod3(np.vstack((C10,one))),C11)
    assert np.all((C10@C10.T)%3==0) and np.all(C10.sum(1)%3==0)
    WcapC10perp=kernel_basis(np.vstack((C10,one)))
    assert WcapC10perp.shape==(29,40)
    basis=C10.copy();representatives=[]
    for vec in WcapC10perp:
        if source.rank_mod3(np.vstack((basis,vec)))>len(basis):
            basis=np.vstack((basis,vec));representatives.append(vec)
    E=np.array(representatives,dtype=np.int64)
    assert E.shape==(19,40) and source.rank_mod3(basis)==29
    gram=(E@E.T)%3
    assert source.rank_mod3(gram)==19
    discriminant=det_mod3(gram)
    assert discriminant in (1,2)
    return C10,C11,E,gram,discriminant


def transvection_permutation(points,v):
    index={tuple(q):i for i,q in enumerate(points)}
    out=[]
    for p in points:
        s=source.symplectic(p,v) if hasattr(source,"symplectic") else (
            p[0]*v[1]-p[1]*v[0]+p[2]*v[3]-p[3]*v[2])%3
        q=tuple((p[i]+s*v[i])%3 for i in range(4))
        q=min(q,tuple((-x)%3 for x in q))
        out.append(index[q])
    return tuple(out)


def group_action_certificate(points,C10,E,gram):
    vectors=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]
    gens=[transvection_permutation(points,v) for v in vectors]
    for g in gens:
        inverse=np.argsort(np.array(g,dtype=np.int64))
        assert source.rank_mod3(np.vstack((C10,C10[:,inverse])))==10
        EP=E[:,inverse]
        assert np.array_equal((EP@EP.T)%3,gram)
    identity=tuple(range(40)); all_perms=[identity];seen={identity};i=0
    while i<len(all_perms):
        a=all_perms[i];i+=1
        for g in gens:
            b=tuple(g[a[j]] for j in range(40))
            if b not in seen:seen.add(b);all_perms.append(b)
        assert len(all_perms)<=25920
    assert len(all_perms)==25920
    # A permutation is trivial on L iff (p(e_i)-e_i).e_j=0 for ALL i,j,
    # since C10 is the exact radical of the 29-dimensional subspace.
    kernel=[]
    for perm in all_perms:
        g=np.array(perm,dtype=np.int64)
        trivial=True
        for i in range(19):
            shifted=np.zeros(40,dtype=np.int64)
            shifted[g]=E[i]
            if np.any(((shifted@E.T)%3)!=gram[i]):
                trivial=False;break
        if trivial:kernel.append(perm)
    assert kernel==[identity]
    return {"transvection_generators":len(gens),
            "generated_projective_symplectic_group_order":len(all_perms),
            "action_on_logical_19_space_faithful":True,
            "representation_preserves_symmetric_dot_quotient":True,
            "logical_action_kernel_order":len(kernel)}


def pgl4_logical_orthogonal_certificate(points,C10,C11,E,gram):
    """Extend PSp logical isometries to PGL4(3), prove faithfulness abstractly.

    Parallel commit 5bd07266 established code invariance under PGL4 and
    transvection Jordan ranks. This independent check adds explicit inherited
    orthogonal form, all 13 generators and an abstract faithful-kernel proof.
    """
    index={tuple(p):i for i,p in enumerate(points)}
    def perm_for(M):
        g=[]
        for v in points:
            q=tuple(int(x)%3 for x in M@np.array(v,dtype=np.int64))
            q=min(q,tuple((-z)%3 for z in q))
            g.append(index[q])
        assert sorted(g)==list(range(40))
        return np.array(g,dtype=np.int64)

    gen_matrices=[]
    for i in range(4):
        for j in range(4):
            if i!=j:
                g=np.eye(4,dtype=np.int64);g[i,j]=1
                gen_matrices.append(g)
    reflect=np.diag([2,1,1,1]).astype(np.int64)
    gen_matrices.append(reflect)
    assert len(gen_matrices)==13

    n=19
    expanded,piv=rref_pivot(np.hstack((gram,np.eye(n,dtype=np.int64))))
    assert piv[:n]==list(range(n))
    gram_inverse=expanded[:,n:]
    assert np.array_equal((gram@gram_inverse)%3,np.eye(n,dtype=np.int64))
    pgl_generators=[]
    for matrix in gen_matrices:
        perm=perm_for(matrix)
        inv=np.argsort(perm)
        assert source.rank_mod3(np.vstack((C10,C10[:,inv])))==10
        assert source.rank_mod3(np.vstack((C11,C11[:,inv])))==11
        EP=E[:,inv]
        assert np.array_equal((EP@EP.T)%3,gram)
        # Orthogonal matrices on logical basis, with C10 the radical.
        M=(EP@E.T@gram_inverse)%3
        assert np.array_equal((M@gram@M.T)%3,gram)
        pgl_generators.append(M)
    T=pgl_generators[0]
    I=np.eye(n,dtype=np.int64)
    N=(T-I)%3
    nil_ranks=[source.rank_mod3(N),source.rank_mod3((N@N)%3),
               source.rank_mod3((N@N@N)%3)]
    assert nil_ranks==[10,3,0]
    assert np.array_equal(np.linalg.matrix_power(T,3)%3,I)
    # Multiplicities of size-three, -two, -one Jordan blocks:
    # r2 = n3, r1 = n2+2n3, n = n1+2n2+3n3.
    n3=nil_ranks[1];n2=nil_ranks[0]-2*n3;n1=19-2*n2-3*n3
    assert [n1,n2,n3]==[2,4,3]
    gl_order=math.prod(3**4-3**j for j in range(4))
    pgl_order=gl_order//2
    assert pgl_order==12130560
    # Standard theorem: PSL4(3) is nonabelian simple, normal of index
    # 2 in PGL4(3), and PGL4(3) has trivial center. Since T belongs to
    # PSL and acts nontrivially, the action kernel K meets PSL trivially.
    # Thus |K|<=2. Any normal subgroup of order two is central, so K=1.
    return {
      "tested_PGL4_generator_count":len(gen_matrices),
      "projective_linear_group_order":pgl_order,
      "projective_special_linear_subgroup_order":pgl_order//2,
      "all_13_generators_preserve_19D_dot_Gram":True,
      "logical_PGL_action_faithful":True,
      "faithfulness_proof":"PSL4(3) simple index2, transvection acts nontrivially; kernel meets PSL trivially hence order<=2; PGL4(3) center trivial",
      "elementary_transvection_nilpotent_ranks":nil_ranks,
      "elementary_transvection_Jordan_block_multiplicities":[n1,n2,n3],
      "prior_result":"Parallel 5bd07266 previously identified PGL4 symmetry and the same transvection ranks; extension is the explicit orthogonal action on Loewy middle quotient and faithful-kernel proof."
    }


def code_word_histogram_and_minwords(B,target):
    n=B.shape[0];hist={}; candidates=[]
    for start in range(0,3**n,3000):
        indexes=np.arange(start,min(start+3000,3**n),dtype=np.int64)
        digits=np.column_stack([(indexes//(3**k))%3 for k in range(n)])
        words=(digits@B)%3
        weights=np.count_nonzero(words,axis=1)
        vals,counts=np.unique(weights,return_counts=True)
        for v,count in zip(vals,counts):hist[int(v)]=hist.get(int(v),0)+int(count)
        if target==18:
            for j in np.where(weights==target)[0]:
                w=words[j]
                if w[np.flatnonzero(w)[0]]==1:candidates.append(w.copy())
    return dict(sorted(hist.items())),np.array(candidates,dtype=np.int64)


def greedy_checks(candidates,size,counts,rng):
    selected=[];basis=np.empty((0,40),dtype=np.int64)
    available=np.ones(len(candidates),dtype=bool)
    for _ in range(size):
        scores=[]
        for i,x in enumerate(candidates):
            if not available[i]:continue
            next_degree=counts+(x!=0)
            score=(int(next_degree.max()),float(np.sum(next_degree**2))/40+
                    .8*float(rng.random()))
            scores.append((score,i))
        scores.sort()
        for _,i in scores:
            if source.rank_mod3(np.vstack((basis,candidates[i])))>len(basis):
                basis=np.vstack((basis,candidates[i]))
                counts+=(candidates[i]!=0)
                available[i]=False
                selected.append(i)
                break
        else:raise AssertionError("short of independent candidates")
    return selected,counts


def edge_colored_incidence_schedule(Xchecks,Zchecks):
    """Construct 18 disjoint-ancilla-data gate layers (NOT a verified CSS circuit).

    Complete the 40x40 padded Tanner multigraph to 18-regularity,
    then remove 18 perfect matchings using finite deterministic DFS.
    Added edges represent dummy interactions and are not emitted.
    """
    H=np.vstack((Xchecks,Zchecks))
    m,n=H.shape
    assert (m,n)==(21,40)
    original=(H!=0).astype(np.int64)
    C=np.zeros((40,40),dtype=np.int64)
    C[:m,:]=original
    row_def=18-C.sum(axis=1)
    col_def=18-C.sum(axis=0)
    assert row_def.min()>=0 and col_def.min()>=0
    assert sum(row_def)==sum(col_def)
    l=r=0
    while l<40 and r<40:
        if row_def[l]==0:l+=1;continue
        if col_def[r]==0:r+=1;continue
        k=min(int(row_def[l]),int(col_def[r]))
        C[l,r]+=k;row_def[l]-=k;col_def[r]-=k
    assert np.all(C.sum(axis=1)==18)
    assert np.all(C.sum(axis=0)==18)
    remaining_original=original.copy()
    schedule=[]
    for _ in range(18):
        right_owner=[-1]*40
        def augment(left,seen):
            for right in np.flatnonzero(C[left]):
                if seen[right]:continue
                seen[right]=True
                if right_owner[right]==-1 or augment(right_owner[right],seen):
                    right_owner[right]=left
                    return True
            return False
        for left in range(40):
            assert augment(left,[False]*40)
        layer=[]
        for data,check in enumerate(right_owner):
            assert check>=0 and C[check,data]>0
            C[check,data]-=1
            if check<m and remaining_original[check,data]:
                remaining_original[check,data]-=1
                layer.append([int(check),int(data),int(H[check,data])])
        assert len({e[0] for e in layer})==len(layer)
        assert len({e[1] for e in layer})==len(layer)
        schedule.append(layer)
    assert np.all(C==0) and np.all(remaining_original==0)
    assert sum(len(layer) for layer in schedule)==323
    return schedule


def optimize_checks(HX,HZ,C10,C11):
    h11,_=code_word_histogram_and_minwords(C11,13)
    h10,Zc=code_word_histogram_and_minwords(C10,18)
    assert h11[13]==80
    assert h10[18]==1560 and len(Zc)==780
    assert min(k for k in h11 if k>0)==13
    assert min(k for k in h10 if k>0)==18
    best=None
    for trial in range(20):
        rng=np.random.default_rng(100+trial)
        counts=np.zeros(40,dtype=np.int64)
        xi,counts=greedy_checks(HX,11,counts,rng)
        zi,counts=greedy_checks(Zc,10,counts,rng)
        key=(int(counts.max()),int(np.sum(counts**2)))
        if best is None or key<best[0]:best=(key,xi,zi,counts.copy())
    key,xi,zi,counts=best
    Xbasis=HX[xi];Zbasis=Zc[zi]
    assert source.rank_mod3(Xbasis)==11 and source.rank_mod3(Zbasis)==10
    assert np.all((Xbasis@Zbasis.T)%3==0)
    assert np.all(np.count_nonzero(Xbasis,axis=1)==13)
    assert np.all(np.count_nonzero(Zbasis,axis=1)==18)
    assert key[0]<=9
    raw_interactions=11*13+10*27
    optimized_interactions=11*13+10*18
    assert (raw_interactions,optimized_interactions)==(413,323)
    # Bipartite edge chromatic number equals maximum degree (Konig).
    # Check nodes max degree 18; data nodes at most 9.
    max_degree=max(int(np.max(np.count_nonzero(np.vstack((Xbasis,Zbasis)),axis=1))),
                   int(counts.max()))
    assert max_degree==18
    schedule=edge_colored_incidence_schedule(Xbasis,Zbasis)
    # Parallel commit 3edb3b9 proved a stronger asymmetric decoder:
    # X radius1, Z radius2. Transfer that SAME decoder (not a new
    # algorithm) to the minimum-interaction CSS generators.
    decX,_=parallel_decoder.build_decoder(Zbasis,1)
    decZ,_=parallel_decoder.build_decoder(Xbasis,2)
    assert (len(decX),len(decZ))==(81,3201)
    return {
        "prior_classical_C11_weight_enumerator":{str(k):v for k,v in h11.items()},
        "prior_classical_C10_weight_enumerator":{str(k):v for k,v in h10.items()},
        "weight13_X_check_basis_size":11,
        "weight18_Z_check_basis_size":10,
        "X_basis_closed_neighborhood_row_ids":xi,
        "Z_basis_vectors":Zbasis.tolist(),
        "checks_rank_X":source.rank_mod3(Xbasis),
        "checks_rank_Z":source.rank_mod3(Zbasis),
        "old_check_interactions":raw_interactions,
        "proven_minimum_independent_check_interactions":optimized_interactions,
        "relative_reduction":(raw_interactions-optimized_interactions)/raw_interactions,
        "data_qudit_max_incidence":int(counts.max()),
        "data_qudit_degree_histogram":{str(k):int(np.count_nonzero(counts==k))
                                      for k in sorted(set(counts))},
        "minimum_ancilla_data_two_qudit_rounds":max_degree,
        "parallel_bias_aware_decoder_syndrome_sizes_on_optimized_checks":[len(decX),len(decZ)],
        "parallel_bias_aware_decoder_exact_component_patterns":len(decX)*len(decZ),
        "parallel_decoder_credit":"Parallel 3edb3b9 first established tX=1,tZ=2 decoder; this verifies the same correction radius under optimal check basis.",
        "explicit_collision_free_gate_layers":schedule,
        "gate_layer_counts":[len(x) for x in schedule],
        "rounds_proof":"18 perfect matchings of padded Tanner multigraph; real-gate set has 323 edges exactly once",
        "fault_tolerance_boundary":"Collision-free incidence schedule ONLY; simultaneous X/Z ancilla algebra, hooks, noisy readout and connectivity not certified. Sequential-type schedule requires at most 31 layers."
    }


def lookup_single_errors(H):
    keys={bytes(np.zeros(H.shape[0],dtype=np.uint8)):None}
    for i in range(40):
        for a in (1,2):
            syn=bytes(((a*H[:,i])%3).astype(np.uint8))
            assert syn not in keys
            keys[syn]=(i,a)
    assert len(keys)==81
    return keys


def two_fault_decoder(HX,HZ):
    lx=lookup_single_errors(HZ)  # detect X faults by Z checks
    lz=lookup_single_errors(HX)  # detect Z faults by X checks
    paulis=[(a,b) for a in range(3) for b in range(3) if a or b]
    cases=0;exact=0
    for i in range(40):
        for j in range(i+1,40):
            for a,b in paulis:
                for c,e in paulis:
                    cases+=1
                    sx=bytes(((a*HZ[:,i]+c*HZ[:,j])%3).astype(np.uint8))
                    sz=bytes(((b*HX[:,i]+e*HX[:,j])%3).astype(np.uint8))
                    if sx not in lx or sz not in lz:continue
                    wanted_x={(k,v) for k,v in [(i,a),(j,c)] if v}
                    wanted_z={(k,v) for k,v in [(i,b),(j,e)] if v}
                    got_x=set() if lx[sx] is None else {lx[sx]}
                    got_z=set() if lz[sz] is None else {lz[sz]}
                    if wanted_x==got_x and wanted_z==got_z:exact+=1
    assert (cases,exact)==(49920,6240)
    guarantee=[]
    for p in (.001,.005,.01,.02,.05):
        p0=(1-p)**40
        p1=40*p*(1-p)**39
        p2=math.comb(40,2)*p*p*(1-p)**38
        guarantee.append({"physical_fault_probability":p,
                          "provably_corrected_probability_lower_bound":
                          round(p0+p1+p2/8,10)})
    return {"single_sector_weight1_syndrome_keys_including_zero":81,
            "full_single_physical_qutrit_Pauli_faults_exactly_corrected":320,
            "two_distinct_fault_cases":cases,
            "two_fault_cases_exactly_corrected_by_separate_t1_decoder":exact,
            "two_fault_conditional_exact_recovery_fraction":exact/cases,
            "exact_two_fault_success_family":"one pure X and one pure Z, either ordering",
            "probability_guarantees":guarantee,
            "noise_assumption":"independent uniform nonidentity Pauli per faulty qutrit",
            "boundaries":["guaranteed lower bounds, not full logical error rates for faults>=3",
                          "no repeated noisy syndrome extraction or correlated noise model"]}


def transversal_gate_nogos(HX,HZ):
    assert set(np.count_nonzero(HX,axis=1))=={13}
    h=HX[0]
    # A CSS zero logical basis state is uniform on the X-check row space.
    # T9^tensor n maps |0> -> itself, |h> -> zeta9^sum(h_i^3)|h>,
    # with weight(h)=13. These amplitudes must agree if code preserved.
    relative_cubic_phase=int(sum(int(x)**3 for x in h)%9)
    assert relative_cubic_phase==4
    return {
        "uniform_T9_transversal_preserves_code":False,
        "witness_X_stabilizer_weight":13,
        "T9_relative_phase_exponent_mod9":relative_cubic_phase,
        "proof":"Code zero logical state has uniform amplitudes over C_X; T9 assigns 1 and zeta9^4 to two C_X words",
        "uniform_Fourier_transversal_preserves_code":False,
        "Fourier_no_go":"swaps pure X/Z check ranks 11 versus 10, impossible without modifying stabilizer",
        "scope":"rules out these naive UNIFORM transversals, not arbitrary logical nonClifford injection"
    }


def certify():
    points,A,HX,HZ=source.checks()
    C10,C11,E,Gram,discriminant=logical_middle_layer(HX,HZ)
    symmetry=group_action_certificate(points,C10,E,Gram)
    pgl=pgl4_logical_orthogonal_certificate(points,C10,C11,E,Gram)
    checks=optimize_checks(HX,HZ,C10,C11)
    decoder=two_fault_decoder(HX,HZ)
    gates=transversal_gate_nogos(HX,HZ)
    return {
        "status":"PASS",
        "code":"[[40,19,4]]_3 with dX=4,dZ=6",
        "prior_work":"C10,C11,N²=J, W33 Loewy 10/19/10 and first CSS code preexist",
        "new_logical_identification":"(1^perp intersect C10^perp)/C10",
        "logical_quotient_dimension":E.shape[0],
        "logical_Gram_rank_mod3":source.rank_mod3(Gram),
        "logical_Gram_determinant_mod3":discriminant,
        "logical_bilinear_form":"nondegenerate inherited symmetric dot product",
        "logical_symmetry":symmetry,
        "full_PGL_orthogonal_action":pgl,
        "optimal_check_basis":checks,
        "decoder":decoder,
        "transversal_gate_nogos":gates
    }


if __name__=="__main__":
    result=certify()
    out=ROOT/"data"/"toe_20261119_w33_logical_decoder_certificate.json"
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"status":"PASS","code":result["code"],
         "logical_group":result["logical_symmetry"]["generated_projective_symplectic_group_order"],
         "min_check_weight":result["optimal_check_basis"]["proven_minimum_independent_check_interactions"],
         "schedule_rounds":result["optimal_check_basis"]["minimum_ancilla_data_two_qudit_rounds"],
         "two_fault_success":result["decoder"]["two_fault_conditional_exact_recovery_fraction"],
         "file":str(out)}))
