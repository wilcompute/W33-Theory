"""Exact arithmetic enclosures of infinite-flux patch ground energies.

TOE71--73 own related complement/interface bounds on another native patch.
Here positive test vectors certify the finite block, closing a numerical premise
left open in that earlier gap estimate. No spectral-gap bound is claimed here.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import json,sys
import numpy as np
import sympy as s
from scipy.sparse import coo_matrix
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_20261027_microscopic_response_and_lifts as old
ROOT=Path(__file__).resolve().parents[1]


def integer_operator(d,L,g='1'):
    g=F(g);C,B,keys=old.lifted_patch(d)
    G=s.Matrix(C@C.T);states=list(product(range(-L,L+1),repeat=d));idx={x:i for i,x in enumerate(states)}
    raw=json.loads((ROOT/'data/w33_20261027_five_front_followthrough.json').read_text())
    harmonics=defaultdict(F)
    for rec in raw['compact_metric_completion']['harmonics']:
        q=tuple(rec['q'][:d])
        if not any(q):continue
        if next(x for x in q if x)<0:q=tuple(-x for x in q)
        harmonics[q]+=F(rec['weight'])
    hop={q:w/(2*g*g)for q,w in harmonics.items()};constant=sum(harmonics.values())/(g*g)
    den=lcm(*(x.denominator for x in list(hop.values())+[g*g/2,constant]))
    hopping={q:int(v*den)for q,v in hop.items()}
    rr=[];cc=[];vv=[];outside=defaultdict(int);cols=np.zeros(len(states),np.int64)
    for i,m in enumerate(states):
        e=np.array(m,dtype=int)@C
        diag=g*g*int(e@e)/2+constant
        rr.append(i);cc.append(i);vv.append(int(diag*den))
        for q,w in hopping.items():
            for sign in (-1,1):
                target=tuple(a+sign*b for a,b in zip(m,q));j=idx.get(target)
                if j is None:outside[target]+=w;cols[i]+=w
                else:rr.append(i);cc.append(j);vv.append(-w)
    A=coo_matrix((vv,(rr,cc)),shape=(len(states),len(states)),dtype=np.int64).tocsr()
    assert (A-A.T).nnz==0
    beta2=F(int(max(cols))*max(outside.values()),den*den)
    diag_inverse=max(G.inv()[i,i]for i in range(d))
    # For any omitted integer m, some |m_i|>=L+1 and
    # m^T G m >= m_i^2/(G^-1)_ii by Cauchy--Schwarz in the G inner product.
    c=s.Rational(g.numerator,g.denominator)**2*s.Rational((L+1)**2,2)/diag_inverse
    return A,den,beta2,c,states


def positive_vector_certificate(A,den):
    evals,vec=eigsh(A.astype(float)/den,k=1,which='SA',tol=1e-12,v0=np.ones(A.shape[0]))
    # Tiny Ritz-vector tails need relative accuracy, which an absolute residual
    # does not supply. Positive Jacobi iterations repair these tails without
    # subtractive cancellation. They still only propose a certificate vector.
    diagonal=A.diagonal().astype(float)/den
    off=(diags(A.diagonal(),dtype=np.int64)-A).astype(float)/den
    proposal=np.abs(vec[:,0])+1e-100
    shift=min(float(evals[0]),float(min(diagonal))-.01)
    for _ in range(80):
        proposal=(off@proposal)/(diagonal-shift)
        proposal/=max(proposal)
    # Floating Ritz computation only proposes a vector. Exact integers below
    # independently certify its quality, even if the eigensolver were wrong.
    psi=[max(1,int(float(x)*10**60))for x in proposal]
    Hpsi=[]
    for i in range(len(psi)):
        Hpsi.append(sum(int(A.data[j])*psi[int(A.indices[j])]for j in range(A.indptr[i],A.indptr[i+1])))
    ratios=[F(h,den*x)for h,x in zip(Hpsi,psi)]
    lower=min(ratios);upper=F(sum(x*h for x,h in zip(psi,Hpsi)),den*sum(x*x for x in psi))
    assert lower<=upper
    return lower,upper,psi,dict(proposed_Ritz_energy=float(evals[0]),
                               exact_min_positive_vector_ratio=str(lower),
                               exact_Rayleigh_quotient=str(upper),
                               finite_block_interval_width=float(upper-lower))


def bound(d=6,L=1,g='1',include_vector=True):
    A,den,beta2,c,states=integer_operator(d,L,g)
    lower,upper,psi,record=positive_vector_certificate(A,den)
    a=s.Rational(lower.numerator,lower.denominator);b2=s.Rational(beta2.numerator,beta2.denominator)
    full_lower=(a+c-s.sqrt((c-a)**2+4*b2))/2
    assert full_lower<=a and float(full_lower)<=float(upper)
    out=dict(loops=d,cutoff=L,g=g,dimension=len(states),
             integer_Hamiltonian_denominator=den,
             finite_block_certificate=record,
             complement_lower_bound_exact=str(c),interface_norm_squared_upper_exact=str(beta2),
             infinite_ground_lower_exact=str(full_lower),infinite_ground_upper_exact=str(upper),
             infinite_ground_interval=[float(full_lower),float(upper)],
             interval_width=float(s.Rational(upper.numerator,upper.denominator)-full_lower),
             proof='P H P >= a from a strictly positive integer vector and the weighted graph-Laplacian identity. Q H Q >= c because V>=0 and each omitted m has a coordinate outside the cutoff. ||PHQ||^2 <= max_abs_row_sum*max_abs_column_sum. The2x2 block comparison gives the displayed exact algebraic lower endpoint; the exact finite-vector Rayleigh quotient gives the variational upper endpoint.',
             scope='Rigorous infinite-electric-flux ground-energy enclosure for this finite geometric patch and supplied potential. Exact arithmetic does not certify a physical mass gap, infinite spatial volume, continuum, or confinement.')
    if include_vector:out['strictly_positive_integer_test_vector']=list(map(str,psi))
    return out


def run():
    return dict(schema='native_positive_vector_and_complement_ground_bounds_v1',
                prior_owner='analysis/2026-10-14_toe72_five_fronts.md and toe73_gauge_static_dipole.py: other-patch complement/interface method; finite-P gap premise remained numerical there.',
                controls=[bound(3,L,'1')for L in (2,3)]+[bound(6,L,'1')for L in (1,2)])


if __name__=='__main__':
    result=run();out=ROOT/'data/w33_20261027_certified_rotor_bounds.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([dict(loops=x['loops'],cutoff=x['cutoff'],interval=x['infinite_ground_interval'],finite_width=x['finite_block_certificate']['finite_block_interval_width'])for x in result['controls']],indent=2))
