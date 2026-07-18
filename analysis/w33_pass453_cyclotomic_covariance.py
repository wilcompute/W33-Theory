#!/usr/bin/env python3
"""Pass 453: cyclotomic covariance explains the q=5 sqrt(5) coefficient atlas.

For an inverse-closed section c and nonzero central character t, the central
Fourier block B_t has entries in Q(zeta_q), and sigma_a(zeta_q)=zeta_q^a sends
B_t to B_{a t}.  Hermiticity identifies t with -t, so coefficient Galois
orbits are indexed by F_q^*/{+-1}.  At q=5 that orbit has size two and its
field is Q(zeta_5)^+=Q(sqrt(5)); at q=7 it has size three and field
discriminant 49.
"""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.polys.numberfields import round_two

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass453_cyclotomic_covariance.json'

def setup(q:int):
    vecs=[(a,b) for a in range(q) for b in range(q) if (a,b)!=(0,0)]
    pairs=[];used=set()
    for v in vecs:
        nv=(-v[0]%q,-v[1]%q);key=tuple(sorted((v,nv)))
        if key not in used:used.add(key);pairs.append(key)
    ab=[(a,b) for a in range(q) for b in range(q)];idx={v:i for i,v in enumerate(ab)}
    omega=np.exp(2j*np.pi/q)
    def block(offsets,t):
        f={}
        for (v,nv),c in zip(pairs,offsets):f[v]=c;f[nv]=-c%q
        M=np.zeros((q*q,q*q),complex)
        for i,(a,b) in enumerate(ab):
            for (x,y),z in f.items():
                M[i,idx[((a+x)%q,(b+y)%q)]]=omega**((t*(z-a*y+x*b))%q)
        return M
    return pairs,block

def trace_orbit(q:int,seed:int):
    pairs,block=setup(q);r=random.Random(seed)
    offsets=tuple(r.randrange(q) for _ in pairs)
    reps=tuple(range(1,(q-1)//2+1))
    raw=[];hermitian=[];minus=[]
    for t in reps:
        B=block(offsets,t)
        raw.append(float(np.trace(np.linalg.matrix_power(B,3)).real/q))
        hermitian.append(bool(np.allclose(B,B.conj().T,atol=1e-10)))
        minus.append(bool(np.allclose(np.linalg.eigvalsh(B),np.linalg.eigvalsh(block(offsets,q-t)),atol=1e-9)))
    coeff=np.poly(raw);icoeff=[int(round(v)) for v in coeff]
    err=float(max(abs(coeff-np.array(icoeff))))
    x=sp.symbols('x');P=sp.Poly(sum(icoeff[i]*x**(len(icoeff)-1-i) for i in range(len(icoeff))),x)
    order,disc=round_two(P)
    return {
      'q':q,'seed':seed,'offsets':list(offsets),'central_character_representatives':list(reps),
      'normalized_trace_cube_conjugates':raw,'minimal_polynomial':str(P.as_expr()),
      'polynomial_discriminant':int(P.discriminant()),'number_field_discriminant':int(disc),
      'integer_recovery_error':err,'all_blocks_hermitian':all(hermitian),
      't_and_minus_t_spectra_equal':all(minus),'polynomial_irreducible':bool(P.is_irreducible),
    }

def build_payload():
    q5=trace_orbit(5,458);q7=trace_orbit(7,460)
    checks={
      'q5_orbit_degree_two':len(q5['central_character_representatives'])==2,
      'q5_field_discriminant_5':q5['number_field_discriminant']==5,
      'q5_polynomial_is_quadratic':q5['minimal_polynomial']=='x**2 + 105*x - 4275',
      'q7_orbit_degree_three':len(q7['central_character_representatives'])==3,
      'q7_field_discriminant_49':q7['number_field_discriminant']==49,
      'q7_polynomial_is_cubic':q7['minimal_polynomial']=='x**3 + 987*x**2 + 274302*x + 22569057',
      'all_blocks_hermitian':q5['all_blocks_hermitian'] and q7['all_blocks_hermitian'],
      'minus_character_identification':q5['t_and_minus_t_spectra_equal'] and q7['t_and_minus_t_spectra_equal'],
      'integer_recovery_stable':max(q5['integer_recovery_error'],q7['integer_recovery_error'])<1e-5,
    }
    return {
      'schema':'w33.pass453.cyclotomic_covariance.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'galois_law':'sigma_a(B_t(c)) = B_(a t)(c); inverse closure gives Spec(B_t)=Spec(B_-t)',
      'coefficient_field_theorem':(
        'The coefficient Galois orbit of a central Fourier block is controlled by F_q^*/{+-1}. '
        'For q=5 its only nontrivial real coefficient field is Q(zeta_5+zeta_5^-1)=Q(sqrt(5)); '
        'for q=7 the corresponding field is the real cubic cyclotomic field of discriminant 49.'),
      'q5':q5,'q7':q7,
      'resolution':(
        'Pass 447\'s square-root-five atlas is forced for the quadratic coefficient pairs it detects; '
        'it is not evidence by itself for a universal golden-ratio dynamics. The q=3 curved sqrt(5) '
        'factor has a different origin: an internal characteristic-polynomial discriminant.'),
      'boundary':(
        'Cyclotomic covariance controls block coefficients and their Galois conjugacy, not every individual '
        'eigenvalue. Higher-degree internal eigenvalue extensions occur, as the Pass 449 degree-4 and degree-8 factors show.'),
      'checks':checks,
    }
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 453 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
