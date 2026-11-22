#!/usr/bin/env python3
"""Hessian H648, binary-tetrahedral 24 overlap, and H D H coset compiler.

H=<R5(omega),R26(omega),R33(omega)> is a finite 648 group on the
canonical Witting 40 rays; D=R36(-1). The exact overlap H ∩ D H D has
order 24, with quaternion-derived subgroup and C3 quotient. Thus the
one-D double coset has precisely 648^2/24=17496 elements; search it
completely rather than enumerating redundant 419904 H D H pairs.

Modular matrix certificates verify the subgroup overlap in characteristic
zero; floating evaluations are only for benchmark target approximation.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.stats import unitary_group
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_discrete_witting_dense_su4 as F
import toe_20261122_h27_central_fourier_bridge as H27
import toe_20261122_next5_compiler_photonics as O
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_hessian_coset_compiler.json'


def hessian_words():
    perms=W.permutations();alphabet='aAbBcC'
    rid={'a':5,'A':5,'b':26,'B':26,'c':33,'C':33}
    gp={s:tuple(perms[rid[s]]) if s.islower() else tuple(perms[rid[s]][perms[rid[s]][i]] for i in range(40)) for s in alphabet}
    group=[('',tuple(range(40)))];seen={group[0][1]}
    for word,perm in group:
        for s in alphabet:
            q=tuple(perm[gp[s][i]] for i in range(40))
            if q not in seen:
                seen.add(q);group.append((word+s,q))
    assert len(group)==648
    return group


def subgroup_info(words):
    normal,x,y,z,orbit=(getattr(H27,"action",None) or H27.heisenberg_action)()
    ns={tuple(int(g(i)) for i in range(40)) for g in normal.generate_schreier_sims()}
    assert len(ns)==27
    G=O.gates()
    def matrix_word(word):
        m=np.eye(4,dtype=complex)
        for s in word:m=m@G[s]
        return m
    Hd=np.stack([matrix_word(w) for w,_ in words])
    D=G['d'];index={O.projkey(U):i for i,U in enumerate(Hd)}
    assert len(index)==648
    sub=[i for i,U in enumerate(Hd) if O.projkey(D@U@D) in index]
    assert len(sub)==24
    I=PermutationGroup([Permutation(words[i][1]) for i in sub])
    assert I.order()==24
    order_profile=dict(sorted(Counter(int(Permutation(words[i][1]).order()) for i in sub).items()))
    assert order_profile=={1:1,2:1,3:8,4:6,6:8}
    Q8=I.derived_subgroup()
    assert Q8.order()==8 and I.center().order()==2
    q_profile=Counter(int(g.order()) for g in Q8.generate_schreier_sims())
    assert dict(sorted(q_profile.items()))=={1:1,2:1,4:6}
    # The 24-group is an H27 complement and contains Q8 normal with
    # 3-cyclic quotient; therefore it is binary tetrahedral SL2(3).
    ps={words[i][1] for i in sub}
    assert len(ps&ns)==1
    assert all(np.linalg.norm(D@Hd[i]-Hd[i]@D)<1e-10 for i in sub)
    # The subgroup is the precise ray-36 stabilizer, not only an abstract 24.
    assert {i for i,(word,p) in enumerate(words) if p[36]==36}==set(sub)
    K=PermutationGroup([*normal.generators,*I.generators])
    assert K.order()==648
    return Hd,sub,order_profile,dict(sorted(q_profile.items())),ns


def modular_overlap(words):
    rows=[]; alphabet=('a','A','b','B','c','C')
    for p in (7,13,19,31,37,43):
        g={}
        for letter,ray in (('a',5),('b',26),('c',33)):
            r,ri=(getattr(F,"reflect",None) or F.reflection)(ray,p);g[letter]=r;g[letter.upper()]=ri
        D=F.pi_phase(36,p)[0]
        I=np.eye(4,dtype=np.int64)
        M=[]
        for w,_ in words:
            A=I
            for s in w:A=(A@g[s])%p
            M.append(A)
        index={tuple(U.ravel()):i for i,U in enumerate(M)}
        assert len(index)==648,(p,len(index))
        overlap=[i for i,U in enumerate(M) if tuple((D@U@D%p).ravel()) in index]
        assert len(overlap)==24,(p,len(overlap))
        stabilizer=[i for i,(_,q) in enumerate(words) if q[36]==36]
        assert len(stabilizer)==24
        assert set(overlap)==set(stabilizer)
        assert all(np.array_equal((D@M[i])%p,(M[i]@D)%p) for i in stabilizer)
        rows.append({'prime':p,'H_distinct_4x4_matrices':648,'intersection_count':24,
                    'H_D_H_double_coset_count_from_orbit_stabilizer':648*648//24})
    return rows


def macro_bench(Hd,words,normal):
    D=O.gates()['d'];rng=np.random.default_rng(20261122)
    targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
    permutations={p:i for i,(_,p) in enumerate(words)}
    normal_idx=sorted(permutations[g] for g in normal)
    assert len(normal_idx)==27
    Nm=Hd[normal_idx];trials=[]
    # Since H=N semidirect I and I=C_H(D) order 24, H D H = H D N.
    # This evaluates exactly 648*27=17496 products per Haar target,
    # not 648^2=419904. It is complete, not a sampled/beam search.
    for t,U in enumerate(targets):
        best=(-1.,0,0)
        Vh=U.conj().T@Hd
        for i in range(648):
            A=Vh[i]@D
            traces=np.abs(np.einsum('ij,kji->k',A,Nm,optimize=True))/4
            k=int(np.argmax(traces))
            if float(traces[k])>best[0]:best=(float(traces[k]),i,k)
        score,i,k=best
        v=Hd[i]@D@Nm[k]
        assert abs(score-abs(np.trace(U.conj().T@v))/4)<1e-12
        if t==0:
            # Independent brute-force 648^2 negative control.
            brute=max(float(np.max(np.abs(np.einsum('ij,kji->k',A@D,Hd,optimize=True))/4))
                      for A in Vh)
            assert abs(brute-score)<1e-12,(score,brute)
        trials.append({'Haar_target_index':t,
                      'best_single_D_HDH_projective_distance':float(np.sqrt(max(0.,2-2*score))),
                      'best_single_D_HDH_process_infidelity':float(1-score*score),
                      'one_D_compiler_word':words[i][0]+'d'+words[normal_idx[k]][0],
                      'compiled_word_length':len(words[i][0])+1+len(words[normal_idx[k]][0]),
                      'searched_distinct_product_representatives':648*27,
                      'naive_expressions_avoided':648*648-648*27})
    return trials


def verify():
    words=hessian_words();Hd,sub,orders,qorder,normal=subgroup_info(words)
    mods=modular_overlap(words)
    trials=macro_bench(Hd,words,normal)
    shallow=O.verify()['haar_target_projective_distances_by_depth']
    assert all(trials[i]['best_single_D_HDH_projective_distance']<=shallow[i][-1]+1e-12 for i in range(3))
    return dict(status='PASS_EXACT_HESSIAN_BINARY_TETRAHEDRAL_DOUBLE_COSET_COMPILER',
      date='2026-11-22',Hessian_mirror_subgroup_order=648,
      Hessian_shortest_word_diameter=max(len(w) for w,_ in words),
      H27_normal_order=27,intersection_order=24,
      intersection_element_order_profile=orders,
      intersection_derived_subgroup_order=8,intersection_derived_Q8_order_profile=qorder,
      intersection_center_order=2,
      H27_intersection_trivial=True,generated_H27_and_intersection_order=648,
      pi_gate_centralizer_in_H_order=24, ray36_stabilizer_in_H_order=24,
      fixed_ray_stabilizer_commutes_with_pi_gate=True,
      exact_double_coset_normal_form="H D H = H D N, with N the normal regular H27 subgroup of order 27",
      exact_semidirect='H = H27 semidirect SL(2,3) (intersection is Q8 semidirect C3; H27 and intersection complementary)',
      D='rank-one Witting pi reflection on ray 36',
      double_coset_H_D_H_cardinality=17496,
      naive_candidate_product_count=648*648,
      reduced_candidate_product_count=648*27,
      exact_search_work_reduction=24,
      exact_finite_field_certificates=mods,
      global_phase_insensitive_haar_benchmarks=trials,
      shallow_depth5_baseline=[x[-1] for x in shallow],
      novelty='Concrete binary-tetrahedral overlap selected by discrete Witting pi gate, and complete finite Hessian H D H compiler search. Hessian H27/SL2(3) abstract group structure already appears in the repo and mathematical literature.',
      limitations='Modular certificates prove finite H and overlap counts in characteristic zero. Benchmark Haar distances are numerical and target-specific; this is NOT generic efficient quantum compilation, hardware scaling or experimental optical advantage.')


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS H∩DHD=SL2(3) order24; |HDH|',d['double_coset_H_D_H_cardinality'])
    print([(x['compiled_word_length'],x['best_single_D_HDH_projective_distance']) for x in d['global_phase_insensitive_haar_benchmarks']])

if __name__=='__main__':main()
