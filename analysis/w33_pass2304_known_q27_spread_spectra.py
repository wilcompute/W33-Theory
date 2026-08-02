#!/usr/bin/env python3
"""Pass 2304: complete q=27 spectra for four standard spread families.

The frozen certificate records exhaustive enumeration of every projective
hyperplane for the regular, Kantor, Thas--Payne and Ree--Tits coordinate ovoids.
Use ``--full`` to rebuild all four 551,881-hyperplane censuses.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from w33_pass2300_ree_tits_divisible_code import ADD,NEG,MUL,INV,powf,projective_hyperplanes,qpolar

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2304_known_q27_symplectic_spread_spectra.json'
N=3

def fadd(*xs):
    z=0
    for x in xs:z=int(ADD[z,int(x)])
    return z
def fneg(x):return int(NEG[int(x)])
def fmul(x,y):return int(MUL[int(x),int(y)])

def functions():
    ni=int(INV[N])
    return {
      'regular':lambda x,y:fneg(fmul(N,x)),
      'kantor':lambda x,y:fneg(fmul(N,powf(x,3))),
      'thas_payne':lambda x,y:fneg(fadd(fmul(N,x),powf(fmul(ni,x),3),powf(y,9))),
      'ree_tits':lambda x,y:fneg(fadd(powf(x,21),powf(y,9)))}

def ovoid(g):
    pts=[(0,0,0,0,1)]
    for x in range(27):
        for y in range(27):
            z=g(x,y)
            pts.append((1,x,y,fneg(z),fneg(fadd(fmul(x,z),fmul(y,y)))))
    assert len(set(pts))==730
    return np.array(pts,dtype=np.uint8)

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def moments(weight_enum,k):
    q,n=27,730;A={int(w):int(c) for w,c in weight_enum.items()}
    m=[sum(math.prod(range(w-j+1,w+1))*c for w,c in A.items()) for j in (1,2,3)]
    rhs=[(q-1)**j*q**(k-j)*math.prod(range(n-j+1,n+1)) for j in (1,2,3)]
    return m,rhs

def census(P,H,chunk=4096):
    spectrum=Counter();typed=defaultdict(Counter)
    squares={int(MUL[a,a]) for a in range(1,27)}
    for lo in range(0,len(H),chunk):
        A=H[lo:lo+chunk]
        z=np.zeros((len(A),len(P)),dtype=np.uint8)
        for j in range(5):z=ADD[z,MUL[A[:,j,None],P[None,:,j]]]
        sizes=np.count_nonzero(z==0,axis=1)
        for a,s in zip(A,sizes):
            spectrum[int(s)]+=1
            qv=qpolar(a)
            typ='singular' if qv==0 else ('square_anisotropic' if qv in squares else 'nonsquare_anisotropic_regular_sections')
            typed[typ][int(s)]+=1
    kernel_projective=spectrum.get(730,0)
    dim=4 if kernel_projective else 5
    divisor=27 if kernel_projective else 1
    weight={str(730-s):26*c//divisor for s,c in spectrum.items() if s!=730}
    weight=dict(sorted(weight.items(),key=lambda x:int(x[0])))
    return {
      'typed_hyperplane_spectrum':{t:{str(k):v for k,v in sorted(h.items())} for t,h in sorted(typed.items())},
      'complete_hyperplane_spectrum':{str(k):v for k,v in sorted(spectrum.items())},
      'regular_spread_intersection_spectrum':{str(k):v for k,v in sorted(typed['nonsquare_anisotropic_regular_sections'].items())},
      'projective_code':{'parameters':f'[730,{dim}]_27','dimension':dim,'nonzero_weight_enumerator':weight,
        'weight_gcd':math.gcd(*(int(w) for w in weight)),
        'divisibility':f"{math.gcd(*(int(w) for w in weight))}-divisible"}}

def build_full():
    H=projective_hyperplanes()
    rows={name:census(ovoid(g),H) for name,g in functions().items()}
    checks={
      'every_family_has_730_ovoid_points':all(len(ovoid(g))==730 for g in functions().values()),
      'every_typed_spectrum_sums_551881':all(sum(sum(h.values()) for h in r['typed_hyperplane_spectrum'].values())==551881 for r in rows.values()),
      'every_complete_spectrum_one_mod_9':all(all(int(s)%9==1 for s in r['complete_hyperplane_spectrum']) for r in rows.values()),
      'all_code_sizes_match_dimensions':all(1+sum(r['projective_code']['nonzero_weight_enumerator'].values())==27**r['projective_code']['dimension'] for r in rows.values()),
      'four_weight_enumerators_distinct':len({json.dumps(r['projective_code']['nonzero_weight_enumerator'],sort_keys=True) for r in rows.values()})==4,
      'regular_27_divisible':rows['regular']['projective_code']['weight_gcd']==27,
      'three_nonregular_exactly_9_divisible':all(rows[x]['projective_code']['weight_gcd']==9 for x in ('kantor','thas_payne','ree_tits'))}
    assert all(checks.values())
    out={'schema':'w33.pass2304.known_q27_symplectic_spread_spectra.v1',
      'status':'PASS_COMPLETE_KNOWN_Q27_FAMILY_SPECTRA',
      'field':'GF(27)=F3[t]/(t^3+2t+1)',
      'families':{'regular':{'formula':'g(x,y)=-n x','n':'t, a nonsquare'},
        'kantor':{'formula':'g(x,y)=-n x^3','n':'t, a nonsquare'},
        'thas_payne':{'formula':'g(x,y)=-n x-(n^{-1}x)^3-y^9','n':'t, a nonsquare'},
        'ree_tits':{'formula':'g(x,y)=-x^21-y^9'}},
      'complete_results':rows,
      'comparison':{'all_four_hyperplane_sections_one_mod_9':True,
        'regular_code_exact_divisibility':27,
        'nonregular_code_exact_divisibility':{'kantor':9,'thas_payne':9,'ree_tits':9},
        'numbers_of_regular_intersection_values':{x:len(r['regular_spread_intersection_spectrum']) for x,r in rows.items()},
        'known_base_intersections':{'regular_kantor':82,'regular_thas_payne':28,'regular_ree_tits':28,'kantor_ree_tits':28,'thas_payne_ree_tits':244}},
      'checks':checks,
      'theorem':'For the four standard q=27 symplectic-spread coordinate families regular, Kantor, Thas--Payne and Ree--Tits, every hyperplane section is 1 modulo 9, but their complete spectra and projective weight enumerators are pairwise distinct. The regular elliptic section spans a hyperplane and gives a 27-divisible [730,4]_27 code; the three nonregular ovoids span PG(4,27) and give exactly 9-divisible [730,5]_27 codes.',
      'boundaries':['This is an exhaustive classification within four named coordinate families at q=27, not a classification of all symplectic spreads.',
        'The universal ovoid theorem supplies only the weaker 1 modulo 3 congruence; the common 1 modulo 9 property of these four families is recorded as a finite theorem and a broader conjectural direction.',
        'The regular, Kantor, Thas--Payne and Ree--Tits constructions retain literature ownership.']}
    out['sha256_without_hash_field']=digest(out);return out

def verify_frozen(d):
    assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values())
    for r in d['complete_results'].values():
        assert sum(r['complete_hyperplane_spectrum'].values())==551881
        assert all(int(s)%9==1 for s in r['complete_hyperplane_spectrum'])
        m,rhs=moments(r['projective_code']['nonzero_weight_enumerator'],r['projective_code']['dimension']);assert m==rhs
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true')
    ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true')
    a=ap.parse_args();out=build_full() if a.full else verify_frozen(json.loads(CERT.read_text()))
    if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
