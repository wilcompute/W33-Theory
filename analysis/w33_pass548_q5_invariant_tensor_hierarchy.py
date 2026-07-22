#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
from w33_pass543_547_common import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass548_q5_invariant_tensor_hierarchy.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)

def fwht(a):
    a=list(a);h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):
                x,y=a[j],a[j+h];a[j]=x+y;a[j+h]=x-y
        h*=2
    return a

def all_rows():
    rows=[]
    for mask in range(1<<12):
        offs=tuple(a*(4 if (mask>>i)&1 else 1)%5 for i,a in enumerate(A))
        rows.append(tuple(charpoly_prime(5,offs)[0]))
    return rows

def payload():
    rows=all_rows();target=rows[0]
    prefix_counts={k:len({cp[2:k+1] for cp in rows}) for k in range(2,6)}
    coefficient_counts={k:len({cp[k] for cp in rows}) for k in range(2,6)}
    fibre_hist={k:dict(sorted(Counter(Counter(cp[2:k+1] for cp in rows).values()).items())) for k in range(2,6)}
    target_fibres={k:sum(cp[k]==target[k] for cp in rows) for k in range(2,6)}
    target_prefix={k:sum(cp[2:k+1]==target[2:k+1] for cp in rows) for k in range(2,6)}
    walsh={}
    for k in range(2,6):
        hist=Counter()
        for coord in range(4):
            W=fwht([cp[k][coord] for cp in rows])
            for mask,x in enumerate(W):
                if x:hist[mask.bit_count()]+=1
        walsh[k]=dict(sorted(hist.items()))
    checks={
      'all_4096_sections':len(rows)==4096,
      'exact_98_charpolys':len(set(rows))==98,
      'hierarchy_1_10_87_98':prefix_counts=={2:1,3:10,4:87,5:98},
      'e4_target_is_80':target_fibres[4]==80,
      'e3_target_is_400':target_fibres[3]==400,
      'e5_target_is_80':target_fibres[5]==80,
      'quartic_first_isolates_target':target_prefix[3]==400 and target_prefix[4]==80 and target_prefix[5]==80,
      'global_complement_even_walsh':all(all(d%2==0 for d in walsh[k]) for k in range(2,6)),
      'degree_bounds_0_2_4_4':max(walsh[2])==0 and max(walsh[3])==2 and max(walsh[4])==4 and max(walsh[5])==4,
      'quadratic_coefficient_constant':coefficient_counts[2]==1,
    }
    return {
      'schema':'w33.pass548.q5_invariant_tensor_hierarchy.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'fixed_magnitude_cube':{'sections':4096,'exact_characteristic_polynomials':len(set(rows))},
      'tensor_hierarchy':{
        'prefix_class_counts':prefix_counts,
        'single_coefficient_value_counts':coefficient_counts,
        'prefix_fibre_size_histograms':fibre_hist,
        'target_single_coefficient_fibres':target_fibres,
        'target_prefix_fibres':target_prefix,
        'walsh_support_by_tensor_order':walsh,
        'interpretation':'e2 is constant; e3 is quadratic in the sign variables and gives 10 classes; e4 adds quartic contractions and gives 87 classes; e5 completes the 98-class spectral image but has no odd Walsh degree because global complement is invisible.'
      },
      'target':{'charpoly':target,'conclusion':'The quartic characteristic coefficient e4 alone has the exact 80-word Pass-540 spectral fibre as its level set.'},
      'checks':checks,
      'boundary':'Exact for the fixed Pass-540 magnitude profile. It is not the full 2,034,735-orbit q=5 image.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 548 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
