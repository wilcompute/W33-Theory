#!/usr/bin/env python3
"""Pass 2300: complete q=27 Ree--Tits hyperplane spectrum and divisible code.

Default mode verifies the frozen exact certificate.  ``--full`` reconstructs the
GF(27) ovoid, enumerates every one of the 551,881 projective hyperplanes in
chunks, classifies their polar type, and recomputes the complete spectrum.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2300_ree_tits_divisible_code.json'

def coeff(a): return a%3,(a//3)%3,(a//9)%3
def enc(c): return c[0]%3+3*(c[1]%3)+9*(c[2]%3)
def add0(a,b):
    A,B=coeff(a),coeff(b)
    return enc(((A[0]+B[0])%3,(A[1]+B[1])%3,(A[2]+B[2])%3))
def neg0(a):
    A=coeff(a); return enc(((-A[0])%3,(-A[1])%3,(-A[2])%3))
def mul0(a,b):
    A,B=coeff(a),coeff(b); c=[0]*5
    for i,x in enumerate(A):
        for j,y in enumerate(B): c[i+j]=(c[i+j]+x*y)%3
    for k in (4,3):
        x=c[k]%3; c[k]=0
        c[k-2]=(c[k-2]+x)%3
        c[k-3]=(c[k-3]+2*x)%3
    return enc(c[:3])
ADD=np.array([[add0(a,b) for b in range(27)] for a in range(27)],dtype=np.uint8)
NEG=np.array([neg0(a) for a in range(27)],dtype=np.uint8)
MUL=np.array([[mul0(a,b) for b in range(27)] for a in range(27)],dtype=np.uint8)
def powf(a,n):
    r=1
    while n:
        if n&1:r=int(MUL[r,a])
        a=int(MUL[a,a]);n//=2
    return r
INV=np.array([0]+[powf(a,25) for a in range(1,27)],dtype=np.uint8)

def ree(x,y): return int(NEG[int(ADD[powf(x,21),powf(y,9)])])
def ovoid_points():
    pts=[(0,0,0,0,1)]
    for x in range(27):
        for y in range(27):
            g=ree(x,y)
            pts.append((1,x,y,int(NEG[g]),int(NEG[int(ADD[int(MUL[x,g]),int(MUL[y,y])])])))
    assert len(pts)==730
    return np.array(pts,dtype=np.uint8)

def projective_hyperplanes():
    rows=[]
    for pivot in range(5):
        for tail in itertools.product(range(27),repeat=4-pivot):
            rows.append((0,)*pivot+(1,)+tail)
    A=np.array(rows,dtype=np.uint8)
    assert A.shape==(551881,5)
    return A

def qpolar(a):
    x=(int(a[4]),int(NEG[a[3]]),int(MUL[a[2],INV[2]]),int(NEG[a[1]]),int(a[0]))
    return int(ADD[int(MUL[x[0],x[4]]),
                   int(ADD[int(NEG[int(MUL[x[1],x[3]])]),int(MUL[x[2],x[2]])])])

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def moments(weight_enum):
    q,k,n=27,5,730
    A={int(w):int(c) for w,c in weight_enum.items()}
    m=[sum(math.prod(range(w-j+1,w+1))*c for w,c in A.items()) for j in (1,2,3)]
    rhs=[(q-1)**j*q**(k-j)*math.prod(range(n-j+1,n+1)) for j in (1,2,3)]
    return m,rhs

def build_full(chunk=4096):
    P=ovoid_points(); H=projective_hyperplanes()
    spectrum=Counter();typed=defaultdict(Counter)
    squares={int(MUL[a,a]) for a in range(1,27)}
    for lo in range(0,len(H),chunk):
        A=H[lo:lo+chunk]
        z=np.zeros((len(A),len(P)),dtype=np.uint8)
        for j in range(5):
            z=ADD[z,MUL[A[:,j,None],P[None,:,j]]]
        sizes=np.count_nonzero(z==0,axis=1)
        for a,s in zip(A,sizes):
            spectrum[int(s)]+=1
            qv=qpolar(a)
            typ='singular' if qv==0 else ('square_anisotropic' if qv in squares else 'nonsquare_anisotropic_regular_sections')
            typed[typ][int(s)]+=1
    weight={str(730-s):26*c for s,c in spectrum.items()}
    weight=dict(sorted(weight.items(),key=lambda x:int(x[0])))
    m,rhs=moments(weight)
    checks={
      'spectrum_sums_to_all_hyperplanes':sum(spectrum.values())==551881,
      'typed_spectra_sum_to_all_hyperplanes':sum(sum(h.values()) for h in typed.values())==551881,
      'all_sections_one_mod_9':all(s%9==1 for s in spectrum),
      'code_size_q5':1+sum(weight.values())==27**5,
      'first_pless_factorial_moment':m[0]==rhs[0],
      'second_pless_factorial_moment':m[1]==rhs[1],
      'third_pless_factorial_moment':m[2]==rhs[2],
      'exactly_9_divisible':math.gcd(*(int(w) for w in weight))==9}
    assert all(checks.values())
    out={
      'schema':'w33.pass2300.ree_tits_divisible_code.v1',
      'status':'PASS_COMPLETE_Q27_REE_TITS_HYPERPLANE_SPECTRUM_AND_9_DIVISIBLE_CODE',
      'field':'GF(27)=F3[t]/(t^3+2t+1)','ovoid_size':730,'projective_hyperplanes':551881,
      'complete_hyperplane_intersection_spectrum':{str(k):v for k,v in sorted(spectrum.items())},
      'hyperplane_types':{t:{str(k):v for k,v in sorted(h.items())} for t,h in sorted(typed.items())},
      'projective_code':{'parameters':'[730,5]_27','size':27**5,
        'nonzero_weight_enumerator':weight,'weight_gcd':9,
        'divisibility':'9-divisible but not 27-divisible',
        'explanation':'Every hyperplane intersection has size 730-w, so 9-divisible code weights are equivalent to section sizes congruent to 1 modulo 9.'},
      'checks':checks,
      'theorem':'The q=27 Ree--Tits ovoid has complete hyperplane spectrum 1^730, 10^4563, 19^96174, 28^408294, 37^36504, 46^4914, 55^702. Its projective [730,5]_27 code has seven nonzero weights and is exactly 9-divisible.',
      'boundaries':['This is an exhaustive q=27 theorem for the specified Ree--Tits coordinate ovoid.',
        'The general theorem for arbitrary Q(4,q) ovoids guarantees intersection 1 modulo the characteristic p; the stronger modulo 9 property is not promoted universally here.',
        'The Ree--Tits construction, projective-code correspondence, and general ovoid intersection theorem retain literature ownership.']}
    out['sha256_without_hash_field']=digest(out);return out

def verify_frozen(d):
    assert d['sha256_without_hash_field']==digest(d)
    assert all(d['checks'].values())
    m,rhs=moments(d['projective_code']['nonzero_weight_enumerator'])
    assert m==rhs
    assert sum(d['complete_hyperplane_intersection_spectrum'].values())==551881
    assert all(int(s)%9==1 for s in d['complete_hyperplane_intersection_spectrum'])
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true')
    ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true')
    a=ap.parse_args()
    out=build_full() if a.full else verify_frozen(json.loads(CERT.read_text()))
    if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
