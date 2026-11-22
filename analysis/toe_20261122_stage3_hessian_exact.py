#!/usr/bin/env python3
"""Third-stage Hessian/Witting exact left-coset compiler.

Enumerate all H D N D N D N (|H|=648, |N|=27, D^2=1). Every
unitary matrix is represented in Q(omega) by signed Eisenstein integer
pairs with common denominator. Unlike numerical rounding, left-coset
membership is tested by exact integer multiplication and byte equality.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_further_two_D_exact as E
import toe_20261122_next5_hessian_coset_compiler as C
import toe_20261122_h27_central_fourier_bridge as B
import toe_20261122_witting_one_phase_three_fixed as W
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_stage3_hessian_exact.json'


def dagger(Z):
    Z=np.swapaxes(Z,-3,-2)
    return np.stack((Z[...,0]-Z[...,1],-Z[...,1]),axis=-1)


def fixed_bra_vector():
    # H fixes ray 25 pointwise. Work with its unnormalised Eisenstein bra.
    result=[]
    for a,b in W.all_rays()[25]:
        assert a.denominator==b.denominator==1
        result.append((int(a-b),-int(b)))
    return np.array(result,dtype=np.int64)


def bra(X,v):
    a,b=v[:,0],v[:,1]; c,d=X[...,0],X[...,1]
    return np.stack((np.einsum('i,...ij->...j',a,c)-np.einsum('i,...ij->...j',b,d),
      np.einsum('i,...ij->...j',a,d)+np.einsum('i,...ij->...j',b,c)-np.einsum('i,...ij->...j',b,d)),axis=-1)


def candidates():
    words=C.hessian_words()
    group,_,_,_,_=B.heisenberg_action()
    ids={p:i for i,(_,p) in enumerate(words)}
    nidx=sorted(ids[tuple(int(g(j)) for j in range(40))] for g in group.generate_schreier_sims())
    assert len(nidx)==27
    H,D=E.exact_H_and_D(words);N=H[nidx]
    v=fixed_bra_vector()
    assert len({q.tobytes() for q in bra(H,v)})==1
    DN=E.mulz(D,N) # denominators 3*3=9
    DN_DN=E.mulz(DN[:,None],DN[None,:]).reshape(729,4,4,2) # /81
    DN_DN_DN=E.mulz(DN_DN[:,None],DN[None,:]).reshape(19683,4,4,2) # /729
    assert np.max(np.abs(DN_DN_DN))<32768
    return words,nidx,H,D,DN_DN,DN_DN_DN,v


def partition_left_H(representatives,H,v,denominator):
    """Two reps x,y same H-left coset iff x*y^dagger is in H.

    By exact H-invariance of v^dagger, same bra is necessary. Use it as
    a hash partition, then compare exact integer matrix products for all
    potentially colliding representatives. This is a complete equivalence
    test (not a modular filter or a heuristic).
    """
    assert denominator%3==0
    scaled_H={(h*(denominator*denominator//3)).astype('<i8').tobytes() for h in H}
    sigs=bra(representatives,v).astype('<i8')
    buckets=defaultdict(list)
    for i,row in enumerate(sigs): buckets[row.tobytes()].append(i)
    chosen=[];class_size_hist=Counter(); comparisons=0
    for bucket in buckets.values():
        selected=[]
        for i in bucket:
            for j in selected:
                comparisons+=1
                candidate=E.mulz(representatives[i],dagger(representatives[j]))
                if candidate.astype('<i8').tobytes() in scaled_H:
                    break
            else:selected.append(i)
        chosen.extend(selected)
        class_size_hist[(len(bucket),len(selected))]+=1
    # Every class representative is distinct; every original rep belongs to
    # a tested H orbit. Group left action is free since reps are invertible.
    return chosen,dict(signature_bucket_count=len(buckets),coset_count=len(chosen),
        exact_matrix_membership_comparisons=comparisons,
        signature_class_profile=[dict(bucket_size=k[0],cosets=k[1],buckets=v)
           for k,v in sorted(class_size_hist.items())])


def complex_matrix(Z,denom):
    return (Z[...,0].astype(float)+np.exp(2j*np.pi/3)*Z[...,1].astype(float))/denom


def benchmark(words,nidx,H,R,chosen):
    groupH=complex_matrix(H,3)
    groupR=complex_matrix(R[np.array(chosen)],729)
    assert np.max(abs(groupH@groupH.conj().transpose(0,2,1)-np.eye(4)))<1e-12
    rng=np.random.default_rng(20261122)
    targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
    out=[]
    for t,U in enumerate(targets):
        left=U.conj().T@groupH
        best=(-1.,-1,-1)
        for start in range(0,len(chosen),320):
            batch=groupR[start:start+320]
            tr=np.einsum('hij,rji->hr',left,batch,optimize=True)
            scores=np.abs(tr)/4
            k=int(np.argmax(scores));i,j=np.unravel_index(k,scores.shape)
            if float(scores[i,j])>best[0]:best=(float(scores[i,j]),i,start+j)
        overlap,hi,ri=best
        flat_index=chosen[ri]
        n1,n2,n3=flat_index//729,(flat_index//27)%27,flat_index%27
        word=words[hi][0]+'d'+words[nidx[n1]][0]+'d'+words[nidx[n2]][0]+'d'+words[nidx[n3]][0]
        V=groupH[hi]@groupR[ri]
        assert abs(abs(np.trace(U.conj().T@V))/4-overlap)<1e-11
        out.append(dict(target_index=t,projective_trace_overlap=overlap,
            projective_distance=float(np.sqrt(max(0.,2-2*overlap))),
            process_infidelity=float(1-overlap**2),primitive_word=word,
            primitive_length=len(word),coset_rep_index=flat_index))
    return out


def verify(include_benchmark=True):
    words,nidx,H,D,R2,R3,v=candidates()
    representatives2,info2=partition_left_H(R2,H,v,81)
    representatives3,info3=partition_left_H(R3,H,v,729)
    assert info2['coset_count']==595
    assert 648*info2['coset_count']==385560
    assert info3['coset_count']==12027,info3
    assert 648*info3['coset_count']==7793496
    # Conditional hash of canonical sorted representative matrices (not the
    # core proof; equivalence uses full exact integer matrices).
    digest=hashlib.sha256(b''.join(sorted(R3[representatives3].astype('<i2').tobytes()[i:i+64]
         for i in range(0,R3[representatives3].nbytes,64)))).hexdigest()
    d=dict(status='PASS_THIRD_STAGE_EXACT_FULL_HESSIAN_COSET_CENSUS',
       finite_H_order=648,normal_H27_order=27,third_stage_raw_expressions=648*27**3,
       exact_third_stage_inequivalent_left_H_cosets=info3['coset_count'],
       exact_third_stage_distinct_complex_matrices=648*info3['coset_count'],
       redundant_raw_expressions=648*(27**3-info3['coset_count']),
       stage2_recovery=info2,stage3_coset_classification=info3,
       stage3_common_Eisenstein_denominator=2187,
       stage3_rep_denominator=729,
       stage3_canonical_representative_sha256=digest,
       proof='H fixes ray25 pointwise. Partition 27^3 normalized words by exact fixed-bra signatures. In each bucket, classify x~y iff xy^dagger belongs to the 648 exact Hessian matrices, using pair-integer multiplication and full byte equality. H acts freely on invertible matrices. Thus 12027*648 exact matrices.',
       physical_boundary='Finite third-stage census; no theorem of short-word approximation, hardware fault tolerance or computational energy advantage.')
    if include_benchmark:
       d['three_seeded_Haar_target_benchmarks']=benchmark(words,nidx,H,R3,representatives3)
    return d


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],d['exact_third_stage_distinct_complex_matrices'],[(x['projective_distance'],x['primitive_length']) for x in d['three_seeded_Haar_target_benchmarks']])
if __name__=='__main__':main()
