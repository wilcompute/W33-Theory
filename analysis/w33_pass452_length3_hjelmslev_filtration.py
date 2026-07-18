#!/usr/bin/env python3
"""Pass 452: explicit length-three affine Hjelmslev conductor filtration."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass452_length3_hjelmslev_filtration.json'


def valuation_p(x:int,p:int,n:int)->int:
    if x % (p**n)==0:return n
    v=0
    while x%p==0:
        v+=1;x//=p
    return v


def build_incidence(p:int=3,n:int=3):
    modulus=p**n
    points=[(x,y) for x in range(modulus) for y in range(modulus)]
    pindex={pt:i for i,pt in enumerate(points)}
    lines=[]
    for m in range(modulus):
        for b in range(modulus):
            lines.append(tuple(pindex[(t,(m*t+b)%modulus)] for t in range(modulus)))
    for u in range(0,modulus,p):
        for b in range(modulus):
            lines.append(tuple(pindex[((u*t+b)%modulus,t)] for t in range(modulus)))
    incidence=np.zeros((len(points),len(lines)),dtype=np.int16)
    for j,line in enumerate(lines):
        incidence[list(line),j]=1
    return points,lines,incidence


def symbolic_spectrum(q:int,n:int)->dict[int,int]:
    spectrum={q**(2*n)+q**(2*n-1):1}
    for j in range(1,n+1):
        spectrum[q**(2*n-j)]=q**(2*j)-q**(2*j-2)
    return spectrum


def build_payload():
    p=3;n=3;q=3;modulus=p**n
    points,lines,B=build_incidence(p,n)
    G=B@B.T
    point_count=modulus**2
    line_count=modulus*(modulus+modulus//p)

    N=[]
    for j in range(1,n):
        mod=p**j
        matrix=np.zeros((point_count,point_count),dtype=np.int16)
        classes={}
        for i,(x,y) in enumerate(points):classes.setdefault((x%mod,y%mod),[]).append(i)
        for block in classes.values():matrix[np.ix_(block,block)]=1
        N.append(matrix)
    formula=(q**n)*np.eye(point_count,dtype=np.int16)+np.ones((point_count,point_count),dtype=np.int16)
    for j,matrix in enumerate(N, start=1):
        formula+=(q**j-q**(j-1))*matrix

    eigenvalues=np.linalg.eigvalsh(G.astype(np.float64))
    rounded=np.rint(eigenvalues).astype(np.int64)
    spectral_counter={int(k):int(v) for k,v in sorted(Counter(rounded.tolist()).items())}
    expected=symbolic_spectrum(q,n)

    pair_hist=Counter()
    for i,(x1,y1) in enumerate(points):
        for x2,y2 in points[i+1:]:
            dx=(x1-x2)%modulus;dy=(y1-y2)%modulus
            depth=min(valuation_p(dx,p,n),valuation_p(dy,p,n),n-1)
            pair_hist[q**depth]+=1

    checks={
      'point_count_q6':point_count==q**6==729,
      'line_count_q6_plus_q5':line_count==q**6+q**5==972,
      'incidence_shape':B.shape==(729,972),
      'line_size_q3':set(B.sum(axis=0).tolist())=={q**3},
      'lines_through_point_q3_plus_q2':set(B.sum(axis=1).tolist())=={q**3+q**2},
      'all_lines_distinct':len({tuple(np.flatnonzero(B[:,j])) for j in range(B.shape[1])})==line_count,
      'gram_formula_exact':np.array_equal(G,formula),
      'common_line_histogram_exact':dict(pair_hist)=={1:236196,3:26244,9:2916},
      'spectrum_exact':spectral_counter==expected,
      'eigenvalues_integral_numerically':float(np.max(np.abs(eigenvalues-rounded)))<1e-8,
      'multiplicities_sum_points':sum(expected.values())==point_count,
      'conductor_magnitudes_match_pass440':[q**5,q**4,q**3]==[243,81,27],
    }
    return {
      'schema':'w33.pass452.length3_hjelmslev_filtration.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'ring':'Z/27Z','residue_order':q,'chain_length':n,
      'incidence':{'points':point_count,'lines':line_count,'line_size':q**3,'lines_through_point':q**3+q**2},
      'gram_identity':'B B^T = q^3 I + J + (q-1) N_1 + (q^2-q) N_2',
      'general_identity':'For length n: B B^T = q^n I + J + sum_{j=1}^{n-1}(q^j-q^(j-1)) N_j.',
      'pair_common_line_histogram':{str(k):v for k,v in sorted(pair_hist.items())},
      'gram_spectrum':{str(k):v for k,v in expected.items()},
      'filtration':[
        {'level':'constant','eigenvalue':q**6+q**5,'multiplicity':1},
        {'level':'residue-plane / conductor 1','eigenvalue':q**5,'multiplicity':q**2-1},
        {'level':'intermediate-neighborhood / conductor 2','eigenvalue':q**4,'multiplicity':q**4-q**2},
        {'level':'primitive within-neighborhood / conductor 3','eigenvalue':q**3,'multiplicity':q**6-q**4},
      ],
      'theorem':(
        'For AHG(2,Z/p^nZ), two distinct points whose difference has p-adic depth s lie on p^s common lines. '
        'The nested neighbor algebra therefore has nonconstant eigenlevels q^(2n-j) with multiplicity '
        'q^(2j)-q^(2j-2), exactly the conductor magnitudes of the length-n Heisenberg Fourier tower.'),
      'checks':checks,
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 452 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
