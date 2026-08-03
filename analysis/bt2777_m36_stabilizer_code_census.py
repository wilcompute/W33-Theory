#!/usr/bin/env python3
"""Pass 2777: exhaustive [[4,2]] binary-stabilizer projection census for two M36 copies."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from bt2777_2781_core import *
ROOT=Path(__file__).resolve().parents[1];SQ3=sp.sqrt(3);p=sp.symbols('p',real=True)
def all_isotropic_rank2():
    vecs=[bvec(i,4) for i in range(1,256)];out=set()
    for i,u in enumerate(vecs):
        for v in vecs[i+1:]:
            if not bsymp(u,v,4):out.add(tuple(sorted((u,v,bxor(u,v)))))
    assert len(out)==5355;return sorted(out)
def span(basis):
    out={(0,)*8}
    for b in basis:out|={bxor(x,b) for x in tuple(out)}
    return out
def extend_iso(s1,s2):
    basis=[s1,s2];S=span(basis)
    for v in [bvec(i,4) for i in range(1,256)]:
        if v not in S and all(not bsymp(v,b,4) for b in basis):
            basis.append(v);S=span(basis)
            if len(basis)==4:return basis[2],basis[3]
    raise AssertionError
PAULI4={bvec(i,4):hermitian_pauli(bvec(i,4),4) for i in range(256)}
def syndrome_bases(sub):
    s1,s2,_=sub;l1,l2=extend_iso(s1,s2);Ps=[PAULI4[x] for x in (s1,s2,l1,l2)];H=Ps[0]+2*Ps[1]+4*Ps[2]+8*Ps[3];_,V=np.linalg.eigh(H);labels=[tuple(1 if np.real(np.vdot(V[:,j],P@V[:,j]))>0 else -1 for P in Ps) for j in range(16)];out={}
    for e1,e2 in itertools.product((1,-1),repeat=2):out[(e1,e2)]=np.column_stack([V[:,labels.index((e1,e2,z1,z2))] for z1,z2 in itertools.product((1,-1),repeat=2)])
    return out
_EXACT_CACHE={}
def exact(x):
    key=round(float(x),11)
    if abs(key)<1e-10:return sp.Integer(0)
    if key not in _EXACT_CACHE:_EXACT_CACHE[key]=sp.nsimplify(key,[SQ3],tolerance=1e-8,full=False)
    return _EXACT_CACHE[key]
def bernstein_power_to_coeff(a):
    a=list(a)+[0]*(4-len(a));a0,a1,a2,a3=a[:4];return [a0,a0+a1/3,a0+2*a1/3+a2/3,a0+a1+a2+a3]
def subdivide_bernstein(b):
    levels=[list(b)]
    while len(levels[-1])>1:levels.append([(levels[-1][i]+levels[-1][i+1])/2 for i in range(len(levels[-1])-1)])
    return [levels[i][0] for i in range(4)],[levels[3-i][i] for i in range(4)]
def nonpositive_bernstein(b,depth=0):
    if all(sp.simplify(x)<=0 for x in b):return True
    if depth>=18:return False
    l,r=subdivide_bernstein(b);return nonpositive_bernstein(l,depth+1) and nonpositive_bernstein(r,depth+1)
def certify_poly(dcoef,pmax):return nonpositive_bernstein(bernstein_power_to_coeff([sp.simplify(dcoef[i]*pmax**i) for i in range(4)]))
def ray_expect(S,R):return np.real(np.einsum('ij,ji->i',R.conj().T@S,R))
def census(psi,fstab,rays,subs):
    A=np.outer(psi,psi.conj());B=np.eye(4)/4-A;coeff=[np.kron(A,A),np.kron(A,B)+np.kron(B,A),np.kron(B,B)];R=np.column_stack(rays);pmax=sp.nsimplify(4*(1-fstab)/3,[SQ3]);closure=certified=identical=0;profiles=Counter();worst=None
    for sub in subs:
        for syndrome,V in syndrome_bases(sub).items():
            S=[V.conj().T@C@V for C in coeff];qf=[float(np.trace(x).real) for x in S]
            if qf[0]<1e-12:continue
            nums=np.stack([ray_expect(x,R) for x in S],axis=1);targets=np.where(nums[:,0]/qf[0]>1-1e-8)[0]
            if not len(targets):continue
            q=[exact(x) for x in qf]
            for ti in targets:
                closure+=1;n=[exact(x) for x in nums[ti]];d=[sp.Integer(0)]*4
                for i in range(3):d[i]+=n[i]-q[i]
                for i in range(3):d[i+1]+=sp.Rational(3,4)*q[i]
                d=[sp.simplify(x) for x in d]
                if all(x==0 for x in d):identical+=1;certified+=1;profiles['identical_fidelity']+=1;continue
                if not certify_poly(d,pmax):raise AssertionError((fstab,sub,syndrome,ti,d,pmax))
                certified+=1;lead=next(i for i,x in enumerate(d) if x!=0);profiles[f'first_negative_order_{lead}']+=1;val=sp.N(sum(d[i]*(pmax/2)**i for i in range(4)),30)
                if worst is None or val>worst[0]:worst=(val,d)
    assert closure==certified
    return {'nearest_stabilizer_fidelity_exact':str(fstab),'magic_witness_p_max_exact':str(pmax),'codes':5355,'syndromes_per_code':4,'m36_closed_branches':closure,'certified_nonimproving_branches':certified,'fidelity_identical_branches':identical,'polynomial_profiles':dict(profiles),'best_nontrivial_midpoint_difference':str(worst[0]) if worst else None,'best_nontrivial_difference_polynomial':str(sp.Poly(sum(worst[1][i]*p**i for i in range(4)),p).as_expr()) if worst else None}
def fanout_formula(k):
    ds=(4-p)/12;dd=p/4;F=sp.simplify((ds**k+2*(1-p)**k/3**k)/(3*ds**k+dd**k));return {'copies':k,'success_probability':str(sp.factor(3*ds**k+dd**k)),'output_fidelity':str(sp.factor(F)),'difference_from_input':str(sp.factor(F-(1-sp.Rational(3,4)*p)))}
def main():
    rays,_,groups=m36_grade_data();subs=all_isotropic_rank2();exact_f={8:(2+SQ3)/6,24:(5+2*SQ3)/12,4:sp.Rational(3,4)};rows=[]
    for _,ids in sorted(groups.items(),key=lambda kv:len(kv[1])):
        size=len(ids);row=census(rays[ids[0]],exact_f[size],rays,subs);row['grade']={8:'deep',24:'mid',4:'shallow'}[size];row['grade_size']=size;rows.append(row)
    out={'schema':'w33.pass2777.m36_4_2_stabilizer_census.v1','status':'EXACT_FINITE_NO_GO','search_space':{'input':'two identical depolarized M36 resources','protocols':'all binary [[4,2]] stabilizer projectors, all four syndromes, arbitrary logical Clifford absorbed by M36 orbit','isotropic_rank2_codes':5355,'branches':21420},'rows':rows,'natural_fanout_recurrences':[fanout_formula(k) for k in range(2,7)],'result':'No M36-closed [[4,2]] stabilizer-projection branch strictly improves depolarizing fidelity anywhere inside its grade-specific magic-witness interval. Deep-grade branches include fidelity-preserving fixed maps, but none distill.','boundary':'This closes the complete two-copy [[4,2]] stabilizer-projection family. It does not exclude larger block codes, nonidentical inputs, catalytic resources, adaptive multi-round protocols, or non-stabilizer-assisted schemes.'}
    path=ROOT/'data/PART_BT2777_M36_4_2_STABILIZER_CENSUS.json';path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');summary={k:out[k] for k in ('schema','status','search_space','result','rows','boundary')};(ROOT/'data/PART_BT2777_M36_4_2_STABILIZER_CENSUS_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print('wrote',path)
if __name__=='__main__':main()
