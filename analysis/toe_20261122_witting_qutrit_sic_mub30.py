#!/usr/bin/env python3
"""Exact Witting 40 -> 1 + 4 qutrit MUBs + triple-lift Hesse SIC.

Derives a 30-effect rank-one informationally complete POVM using any one
of four qutrit MUB triples, rather than the previous 39-effect design.
All incidence, overlaps and normalization are checked in Q(omega) exactly.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_witting_minimal_lie_control as L
import toe_20261122_h27_central_fourier_bridge as H
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_witting_qutrit_sic_mub30.json'
ZERO=W.Z;ONE=W.O

def dots(v,w):
    x=ZERO
    for a,b in zip(v,w):x=W.add(x,W.mul(W.conj(a),b))
    return x

def abs2(z):
    q=W.mul(z,W.conj(z));assert q[1]==0
    return q[0]

def qmatrix_sum(projectors,indices):
    zero=W.Z
    return tuple(tuple(sumz(P[i][j] for P in (projectors[k] for k in indices))
                      for j in range(4)) for i in range(4))

def sumz(zs):
    x=ZERO
    for z in zs:x=W.add(x,z)
    return x

def P_of(v):
    norm=dots(v,v)
    assert norm[1]==0 and norm[0] in (1,3)
    return tuple(tuple(W.scale(W.mul(v[i],W.conj(v[j])),F(1,norm[0]))
         for j in range(4)) for i in range(4))

def mat_scaled(A,s):
    return tuple(tuple(W.scale(z,s) for z in row) for row in A)

def mat_add(A,B):
    return tuple(tuple(W.add(A[i][j],B[i][j]) for j in range(4)) for i in range(4))

def mat_eq(A,B):return A==B

def verify():
    rays=W.all_rays(); P=[P_of(v) for v in rays]
    I=tuple(tuple(ONE if i==j else ZERO for j in range(4)) for i in range(4))
    p25=P[25];subspace=mat_add(I,mat_scaled(p25,F(-1)))
    perms=W.permutations();O27=sorted(W.orbit_and_paths(perms));O12=sorted(set(range(40))-set(O27)-{25})
    assert len(O27)==27 and len(O12)==12
    # Orthogonality graph on the 12-line orthogonal complement gives 4 disjoint K3s.
    unassigned=set(O12);bases=[]
    while unassigned:
        a=min(unassigned);basis=sorted(j for j in O12 if dots(rays[a],rays[j])==ZERO)
        basis=sorted(set(basis+[a]));assert len(basis)==3
        assert all(dots(rays[x],rays[y])==ZERO for x in basis for y in basis if x!=y)
        assert not(set(basis)-unassigned)
        bases.append(basis);unassigned-=set(basis)
    assert len(bases)==4
    assert all(mat_eq(qmatrix_sum(P,b),subspace) for b in bases)
    all_cross=[abs2(dots(rays[i],rays[j]))/(dots(rays[i],rays[i])[0]*dots(rays[j],rays[j])[0]) for a,b in enumerate(bases)
                   for k in range(a+1,4) for i in b for j in bases[k]]
    assert len(all_cross)==54 and set(all_cross)=={F(1,3)}
    # The central H27 element partitions the 27-ray orbit into nine triples.
    normal,x,y,z,orbit=H.heisenberg_action()
    fibers=sorted([sorted(f) for f in H.center_fibers(z,orbit)])
    assert len(fibers)==9 and {u for f in fibers for u in f}==set(O27)
    projected={}
    v25=rays[25]
    for j in O27:
        v=rays[j]
        comp=W.scale(dots(v25,v),F(1,3))
        projected[j]=tuple(W.sub(v[k],W.mul(v25[k],comp)) for k in range(4))
        assert dots(projected[j],projected[j])==(F(2,3)*dots(v,v)[0],F(0))
    for f in fibers:
        for i in f:
            for j in f:assert abs2(dots(projected[i],projected[j]))/(dots(projected[i],projected[i])[0]*dots(projected[j],projected[j])[0])==1
    for a,f in enumerate(fibers):
        for g in fibers[a+1:]:
            for i in f:
                for j in g:assert abs2(dots(projected[i],projected[j]))/(dots(projected[i],projected[i])[0]*dots(projected[j],projected[j])[0])==F(1,4)
    # Hesse affine-plane dictionary: each MUB vector is orthogonal to a
    # 3-point line of the nine projected SIC states and has squared
    # overlap 1/2 with the other six; these are the 12 affine lines.
    affine_zero_lines={}
    for ray in O12:
        hits=[]
        for k,f in enumerate(fibers):
            rep=projected[f[0]]
            v=abs2(dots(rep,rays[ray]))/(dots(rep,rep)[0]*dots(rays[ray],rays[ray])[0])
            assert v in {F(0),F(1,2)}
            if v==0:hits.append(k)
        assert len(hits)==3
        affine_zero_lines[ray]=hits
    assert len(set(map(tuple,affine_zero_lines.values())))==12
    for b in bases:
        assert sorted(k for ray in b for k in affine_zero_lines[ray])==list(range(9))
    for a,b in enumerate(bases):
        for other in bases[a+1:]:
            assert all(len(set(affine_zero_lines[i])&set(affine_zero_lines[j]))==1
                for i in b for j in other)
    # Exact minimality within the requirement that ALL 27 universal-control
    # rays have strictly positive weights. For any normalized POVM made
    # from the 27 rays and blocked rays of total weight 1 (by Q pairing),
    # a SIC point not on a chosen blocked zero-line forces sum of its three
    # universal-ray weights to vanish, contradicting their positivity.
    # Covering all 9 points requires at least 3 zero-lines, and 3 lines
    # cover all 9 iff they are disjoint, i.e. one MUB parallel class.
    assert all(len(set().union(*(set(affine_zero_lines[j]) for j in subset)))<9
       for k in (0,1,2) for subset in __import__('itertools').combinations(O12,k))
    three_site_covers=[list(subset) for subset in __import__('itertools').combinations(O12,3)
        if len(set().union(*(set(affine_zero_lines[j]) for j in subset)))==9]
    assert sorted(three_site_covers)==sorted(bases)
    assert all(abs2(dots(rays[25],rays[j]))/(3*dots(rays[j],rays[j])[0])==F(1,3) for j in O27)
    assert all(dots(rays[25],rays[j])==ZERO for j in O12)
    assert qmatrix_sum(P,O27)==mat_add(mat_scaled(I,F(6)),mat_scaled(p25,F(3)))
    assert qmatrix_sum(P,O12)==mat_scaled(subspace,F(4))
    # 27 outer rays + just one orthonormal qutrit MUB basis make a 30-element POVM.
    for b in bases:
        target=mat_add(mat_scaled(qmatrix_sum(P,O27),F(1,9)),
                       mat_scaled(qmatrix_sum(P,b),F(1,3)))
        assert target==I
    # Rank/IC verified in six split fields, then the physical frame numerics.
    ranks=[]
    for p in L.PRIMES:
        mats=[]
        for v,vc in L.all_witting_rays(p):
            norm=sum(int(a)*int(b) for a,b in zip(v,vc))%p
            mats.append(np.array(L.outer(v,vc,p),dtype=np.int64).reshape(4,4)*pow(norm,-1,p)%p)
        vals=[]
        for b in bases:
            r=L.modular_rank([mats[i].ravel().tolist() for i in O27+b],p)
            vals.append(r);assert r==16
        ranks.append(dict(prime=p,all_four_30_effect_choices_rank=vals))
    cv=lambda q:complex(float(q[0])-float(q[1])/2,float(q[1])*np.sqrt(3)/2)
    complex_rays=np.array([[cv(z) for z in v] for v in rays]);complex_rays/=np.linalg.norm(complex_rays,axis=1)[:,None]
    stats=[]
    for name,choice,weights in [('39-effect',O27+O12,[1/9]*27+[1/12]*12)]+[
         ('30-effect-basis-'+str(k),O27+b,[1/9]*27+[1/3]*3) for k,b in enumerate(bases)]:
        V=np.array([np.sqrt(w)*complex_rays[j].conj() for j,w in zip(choice,weights)])
        assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-12
        q=np.array([w*np.outer(complex_rays[j],complex_rays[j].conj()).reshape(16) for j,w in zip(choice,weights)])
        Fop=q.conj().T@q
        eig=np.linalg.eigvalsh(Fop)
        assert eig.min()>1e-12
        stats.append(dict(name=name,number_of_outcomes=len(choice),frame_eigenvalues=np.round(eig,12).tolist(),
                  frame_condition_number=float(eig.max()/eig.min()),
                  Naimark_isometry_max_error=float(np.max(abs(V.conj().T@V-np.eye(4))))))
    return dict(status='PASS_EXACT_40_WITTING_QUTRIT_SIC_MUB_AND_30_EFFECT_IC_POVM',
      fixed_ray=25,universal_ray_orbit=O27,blocked_qutrit_MUB_basis_partition=bases,
      H27_nine_center_fibers=fibers,
      Hesse_affine_plane_MUB_zero_lines={str(k):v for k,v in affine_zero_lines.items()},
      minimum_extra_blocked_orbit_sites_if_all27_positive=3,
      all_minimal_three_site_positive_supports=three_site_covers,
      minimum_support_proof='The nine projected SIC operators form a linearly independent basis of 3x3 Hermitians. In its dual expansion, a blocked MUB projector has coefficient +1/3 at each of six nonorthogonal SIC rays and -1/3 at its three orthogonal rays. Q pairing fixes total blocked weights to 1. If a SIC point belongs to no chosen zero-line, its three outer-ray weights sum to zero. Positive outer weights require the chosen zero-lines cover all nine SIC points. At least three lines are needed; three cover all nine iff disjoint, namely one of four MUB bases.',
      exact_qutrit_MUB_cross_basis_squared_overlap='1/3',
      exact_nine_SIC_projected_squared_overlap='1/4',
      qutrit_SIC_projected_fiber_multiplicity=3,
      exact_projector_sum_27='6I+3P25',
      exact_projector_sum_each_blocked_triple='I-P25',
      reduced_positive_POVM='27 effects P_j/9 plus 3 effects P_k/3 chosen from any blocked MUB triple; sum I4',
      previous_effect_count=39,reduced_effect_count=30,
      reduction_fraction=9/39,
      six_prime_rank_certificates=ranks,
      Naimark_isometry_and_superoperator_spectra=stats,
      novelty_boundary='Specific exact Witting 1+12+3x9 decomposition and 30-effect IC Naimark measurement. Qutrit SICs and MUBs are established mathematical objects, not inventions. This 30-effect choice is NOT proven globally minimal.',
      physics_boundary='Single-photon mathematical POVM only; an actual 30-output passive network and its calibration/loss were not constructed or measured.')


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],d['blocked_qutrit_MUB_basis_partition'])
    print([(x['name'],round(x['frame_condition_number'],2)) for x in d['Naimark_isometry_and_superoperator_spectra']])
if __name__=='__main__':main()
