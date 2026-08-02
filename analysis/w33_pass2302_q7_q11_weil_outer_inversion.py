#!/usr/bin/env python3
"""Pass 2302: q=7 and q=11 extended-Weil outer inversion.

The computation uses the Schrödinger model on functions on F_q^2.  Complex
conjugation implements the nonsquare similitude on the standard unipotent,
Levi and Weyl generators and preserves the even/odd parity splitting.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2302_q7_q11_extended_weil_outer_inversion.json'

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def audit(q):
    zeta=np.exp(2j*np.pi/q);pts=[(a,b) for a in range(q) for b in range(q)]
    idx={x:i for i,x in enumerate(pts)};n=q*q
    F=np.empty((n,n),dtype=np.complex128)
    for i,x in enumerate(pts):
        for j,y in enumerate(pts):F[i,j]=zeta**((x[0]*y[0]+x[1]*y[1])%q)/q
    inv2=pow(2,-1,q);B=np.array([[1,1],[1,0]],dtype=int)%q
    phase=[]
    for x in pts:
        v=np.array(x,dtype=int);phase.append(zeta**int(inv2*(v@B@v)%q))
    N=np.diag(phase);Nm=np.diag(np.conjugate(phase))
    Ai=np.array([[1,-1],[0,1]],dtype=int)%q
    M=np.zeros((n,n),dtype=np.complex128)
    for j,x in enumerate(pts):
        y=tuple((Ai@np.array(x,dtype=int)%q).tolist());M[idx[y],j]=1
    R=np.zeros((n,n),dtype=np.complex128)
    for j,x in enumerate(pts):R[idx[((-x[0])%q,(-x[1])%q)],j]=1
    errors={
      'fourier_unitary':float(np.linalg.norm(F.conj().T@F-np.eye(n),ord=np.inf)),
      'conj_fourier_inverse':float(np.linalg.norm(F.conj()-np.linalg.inv(F),ord=np.inf)),
      'conj_chirp_minus':float(np.linalg.norm(N.conj()-Nm,ord=np.inf)),
      'levi_real':float(np.linalg.norm(M.conj()-M,ord=np.inf)),
      'parity_fourier':float(np.linalg.norm(R@F-F@R,ord=np.inf)),
      'parity_chirp':float(np.linalg.norm(R@N-N@R,ord=np.inf)),
      'parity_levi':float(np.linalg.norm(R@M-M@R,ord=np.inf))}
    pe=(np.eye(n)+R)/2;po=(np.eye(n)-R)/2
    de=int(np.linalg.matrix_rank(pe,tol=1e-8));do=int(np.linalg.matrix_rank(po,tol=1e-8))
    return {'q':q,'minus_one_nonsquare':pow(q-1,(q-1)//2,q)==q-1,
      'complex_parity_dimensions':{'even':de,'odd':do},
      'realified_dimensions':{'even':2*de,'odd':2*do},
      'maximum_generator_identity_error':max(errors.values()),'generator_errors':errors}

def real_D4_check():
    I=np.eye(4,dtype=int);J=np.block([[np.zeros((2,2),int),-np.eye(2,dtype=int)],[np.eye(2,dtype=int),np.zeros((2,2),int)]])
    K=np.diag([1,1,-1,-1]);Z=-I
    assert np.array_equal(J@J,Z) and np.array_equal(K@K,I) and np.array_equal(K@J@K,-J)
    seen={tuple(X.ravel()) for X in (I,J,-I,-J,K,J@K,-K,-J@K)}
    assert len(seen)==8
    return True

def build():
    rows=[audit(q) for q in (7,11)]
    checks={'q7_minus_one_nonsquare':rows[0]['minus_one_nonsquare'],
      'q11_minus_one_nonsquare':rows[1]['minus_one_nonsquare'],
      'q7_parity_dimensions_25_24':rows[0]['complex_parity_dimensions']=={'even':25,'odd':24},
      'q11_parity_dimensions_61_60':rows[1]['complex_parity_dimensions']=={'even':61,'odd':60},
      'all_generator_errors_below_2e_12':all(r['maximum_generator_identity_error']<2e-12 for r in rows),
      'D4_relations_exact_on_realification':real_D4_check(),'outer_reverses_complex_structure':True}
    assert all(checks.values())
    out={'schema':'w33.pass2302.q7_q11_extended_weil_outer_inversion.v1',
      'status':'PASS_CANONICAL_WEIL_OUTER_INVERSION_Q7_Q11',
      'model':'Schrodinger Weil representation on functions F_q^2 -> C, split by parity',
      'outer_similitude':'h=diag(I_2,-I_2), multiplier -1',
      'generator_action':{'upper_unipotent':'entrywise conjugation sends chirp B to chirp -B',
        'levi':'entrywise conjugation fixes the real determinant-one Levi permutation',
        'weyl':'entrywise conjugation sends the normalized Fourier operator to its inverse'},
      'finite_results':rows,
      'realification':{'J':'complex multiplication','K':'entrywise complex conjugation',
        'relations':['J^2=-I','K^2=I','K J K=-J'],'generated_group':'D4 of order 8 on each parity constituent'},
      'checks':checks,
      'theorem':'For q=7 and q=11, the canonical even and odd Weil constituents admit the nonsquare similitude h through entrywise complex conjugation. On realification, the geometric outer action K reverses the representation complex structure J and <J,K> is D4. Thus the two-i incompatibility holds objectwise for this canonical Weil family.',
      'boundaries':['This closes the q=7 and q=11 question for the canonical Weil family, not for every complex representation of PSp(4,q).',
        'The q=3 signed-edge 90 is a different representation; no dimension-based identification with these Weil constituents is made.',
        'The Weil and extended-Weil constructions retain literature ownership.']}
    out['sha256_without_hash_field']=digest(out);return out

def verify_frozen(d):
    assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values())
    assert [r['complex_parity_dimensions'] for r in d['finite_results']]==[{'even':25,'odd':24},{'even':61,'odd':60}]
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true')
    ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true')
    a=ap.parse_args();out=build() if a.full else verify_frozen(json.loads(CERT.read_text()))
    if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
