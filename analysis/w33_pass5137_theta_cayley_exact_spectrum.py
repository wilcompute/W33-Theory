#!/usr/bin/env python3
"""Pass5137: exact spectrum/representation certificate for the U(q) theta Cayley graph.

No floating diagonalization is used.  For q=2,3,4,5 we build the Cayley
operator A on the regular U(q)-module.  A square-free integer polynomial P is
verified to satisfy P(A) delta_e=0; left-translation invariance then gives
P(A)=0.  Exact closed-walk moments trace(A^k)=|U|(A^k)_{e,e} determine the
multiplicities uniquely among the distinct roots of P.

The all-q linear-character sector follows directly from U/[U,U] ~= F_q^2:
the two simple-root subgroup sums are q-1 on a trivial additive character and
-1 otherwise, while the two higher-root subgroup sums are always q-1.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm,I4
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5137_THETA_CAYLEY_EXACT_SPECTRUM.json'

def pmul(a,b):
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
      for j,y in enumerate(b):z[i+j]+=x*y
    return z

def annihilator(linears,quads):
    p=[1]
    for r in linears:p=pmul(p,[-r,1])
    for b,c in quads:p=pmul(p,[c,b,1])
    return p

def qpower_sum(b,c,k):
    # roots of x^2+b x+c: sum roots=-b, product=c
    if k==0:return 2
    if k==1:return -b
    a0,a1=2,-b
    for _ in range(2,k+1):a0,a1=a1,(-b)*a1-c*a0
    return a1

def expected_moment(spec,k):
    z=sum(m*(r**k) for r,m in spec['linear_mult'].items())
    for key,m in spec['quad_mult'].items():
        b,c=map(int,key.split(','));z+=m*qpower_sum(b,c,k)
    return z

def apply(v,U,conn,F,idx):
    out=[0]*len(U)
    for i,x in enumerate(v):
        if not x:continue
        g=U[i]
        for h in conn:out[idx[mm(g,h,F)]]+=x
    return out

def anchor(q,spec):
    U,H,F=roots(q);idx={g:i for i,g in enumerate(U)};e=idx[I4()]
    conn=[]
    for h in H:
      for z in h:
        if z!=I4():conn.append(z)
    assert len(conn)==4*(q-1)
    p=annihilator(sorted(spec['linear_mult']),[tuple(map(int,k.split(','))) for k in spec['quad_mult']])
    deg=len(p)-1
    powers=[];v=[0]*len(U);v[e]=1
    for k in range(deg+1):
        powers.append(v)
        if k<deg:v=apply(v,U,conn,F,idx)
    residual=[0]*len(U)
    for k,c in enumerate(p):
        if c:
            vk=powers[k]
            for i,x in enumerate(vk):residual[i]+=c*x
    assert not any(residual)
    traces=[]
    for k in range(deg):
        tr=len(U)*powers[k][e]
        ex=expected_moment(spec,k)
        assert tr==ex,(q,k,tr,ex)
        traces.append(tr)
    dim=sum(spec['linear_mult'].values())+2*sum(spec['quad_mult'].values())
    assert dim==q**4
    return {'q':q,'vertices':q**4,'degree':4*(q-1),'annihilator_coefficients_low_to_high':p,
            'annihilator_degree':deg,'annihilator_delta_residual_l1':0,
            'trace_moments_0_to_degree_minus_1':traces,
            'linear_eigenvalue_multiplicities':{str(k):v for k,v in sorted(spec['linear_mult'].items())},
            'quadratic_factor_multiplicities':spec['quad_mult']}

def main():
    specs={
      2:{'linear_mult':{-4:1,-2:2,0:2,2:2,4:1},'quad_mult':{'0,-2':4}},
      3:{'linear_mult':{-4:12,-1:18,2:10,5:4,8:1},'quad_mult':{'2,-2':6,'-4,1':6,'-1,-8':6}},
      4:{'linear_mult':{-4:72,0:84,2:24,4:9,6:24,8:6,12:1},'quad_mult':{'0,-8':18}},
      5:{'linear_mult':{-4:220,1:140,6:16,11:8,16:1},'quad_mult':{'-2,-14':40,'-2,-4':40,'-7,-4':20,'-12,31':20}}
    }
    A={str(q):anchor(q,specs[q]) for q in (2,3,4,5)}
    linear={'eigenvalues':['4(q-1)','3q-4','2q-4'],
            'multiplicities':['1','2(q-1)','(q-1)^2'],
            'dimension':'q^2',
            'proof':'U/[U,U] is F_q^2. Higher-root subgroup sums act by q-1 on every linear character; each simple-root sum acts by q-1 for the trivial additive character and -1 otherwise.'}
    out={'pass':5137,'status':'THEOREM_ALL_Q_LINEAR_SECTOR_PLUS_EXACT_FULL_Q2_Q3_Q4_Q5_SPECTRA',
         'all_q_linear_character_sector':linear,'anchors':A,
         'method':'For each anchor, square-free P(A) delta_e=0 implies P(A)=0 by left translations. Since A is real symmetric, it is diagonalizable with eigenvalues among the distinct roots of P. Exact traces through degree(P)-1 agree with the displayed multiplicities, which are unique by the Vandermonde system.',
         'spectral_gap_anchor_pattern':'At q=2,3,4,5 the second eigenvalue is 3q-4, so the adjacency spectral gap is q.',
         'boundary':'The full all-q nonlinear spectrum and the all-q proof that no nonlinear eigenvalue exceeds 3q-4 remain open; only the q^2-dimensional linear sector is proved uniformly.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
