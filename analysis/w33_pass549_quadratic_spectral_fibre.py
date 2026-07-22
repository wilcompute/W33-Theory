#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
from w33_pass543_547_common import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass549_quadratic_spectral_fibre.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)
LINEAR_EQS=(0x1a4,0x28c,0x4c4,0x894)
BASIS=(0x001,0x002,0x07c,0x0f8,0x120,0x3d0,0x440,0xf80)

def from_y(y):
    x=0
    for i,b in enumerate(BASIS):
        if (y>>i)&1:x^=b
    return x

def target_set():
    target=charpoly_prime(5,A)[0];S=[]
    for mask in range(1<<12):
        offs=tuple(a*(4 if (mask>>i)&1 else 1)%5 for i,a in enumerate(A))
        if charpoly_prime(5,offs)[0][4]==target[4]:S.append(mask)
    return set(S),target

def anf(ind):
    a=list(ind)
    for i in range(12):
        for mask in range(1<<12):
            if (mask>>i)&1:a[mask]^=a[mask^(1<<i)]
    return a

def payload():
    S,target=target_set();L={x for x in range(1<<12) if all(((x&e).bit_count()&1)==0 for e in LINEAR_EQS)}
    Y={y for y in range(256) if from_y(y) in S}
    core=[]
    for y3 in (0,1):
      for y4 in (0,1):
       for y5 in (0,1):
        for y6 in (0,1):
         if y4*(1^y3)==0 and y3*y5==0 and y6*(1^y5)==0:core.append((y3,y4,y5,y6))
    predicted={from_y(y) for y in range(256) if (((y>>4)&1)*(1^((y>>3)&1))==0 and ((y>>3)&1)*((y>>5)&1)==0 and ((y>>6)&1)*(1^((y>>5)&1))==0)}
    indicator=[1 if x in S else 0 for x in range(1<<12)];aa=anf(indicator)
    anf_hist=Counter(mask.bit_count() for mask,x in enumerate(aa) if x)
    checks={
      'target_80':len(S)==80,
      'four_linear_equations_rank4':len(L)==256 and all(x in L for x in S),
      'basis_spans_linear_hull':len({from_y(y) for y in range(256)})==256 and {from_y(y) for y in range(256)}==L,
      'quadratic_three_equation_model_exact':predicted==S,
      'five_parallel_four_cubes':len(core)==5 and len(predicted)==5*16,
      'not_linear':any((x^y) not in S for x in S for y in S),
      'complement_closed':all((x^0xfff) in S for x in S),
      'indicator_anf_degree8':max(anf_hist)==8,
      'e4_level_set_exact':all(charpoly_prime(5,tuple(a*(4 if (x>>i)&1 else 1)%5 for i,a in enumerate(A)))[0][4]==target[4] for x in S),
    }
    return {
      'schema':'w33.pass549.quadratic_spectral_fibre.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'ambient_coordinates':{
        'bit_order':'x_0,...,x_11; bit 1 multiplies the corresponding fixed magnitude by -1 mod 5',
        'linear_equations_0_based':[[2,5,7,8],[2,3,7,9],[2,6,7,10],[2,4,7,11]],
        'linear_hull_dimension':8,
        'basis_masks_hex':[hex(x) for x in BASIS]
      },
      'quadratic_model':{
        'quotient_coordinates':'x=sum_i y_i*basis_i over F2',
        'equations':['y4*(1+y3)=0','y3*y5=0','y6*(1+y5)=0'],
        'free_coordinates':['y0','y1','y2','y7'],
        'core_patterns_y3_y4_y5_y6':core,
        'structure':'F2^4 times a five-point quadratic core; equivalently a union of five parallel affine 4-cubes.',
        'size':len(predicted)
      },
      'boolean_indicator':{'anf_terms':sum(aa),'anf_degree_histogram':dict(sorted(anf_hist.items())),'note':'The full indicator has degree 8, although its zero-locus description needs only four linear and three quadratic equations.'},
      'spectral_definition':{'quartic_coefficient':target[4],'statement':'The same set is exactly the level set e4=e4(target), so the quadratic Boolean model and quartic cyclotomic invariant define one identical 80-word fibre.'},
      'checks':checks,
      'boundary':'The coordinate model depends on the fixed Pass-540 magnitude frame; its cardinality and spectral meaning are intrinsic under the magnitude stabilizer.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 549 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
