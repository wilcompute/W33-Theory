#!/usr/bin/env python3
"""Pass 422: optimal enumerative telemetry plus bounded-memory protection."""
from __future__ import annotations
import argparse,json,math
from collections import Counter
from pathlib import Path
import numpy as np

from w33_pass410_414_common import certificate,write_json
from w33_pass417_divisor_cycle_hybrid_decoder import PairIndex,partitions,canonical_divisor,fibre_counts,EDGES

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass422_telemetry_coding_theorem.json'

def type_multiplicity(pos:tuple[int,...],neg:tuple[int,...],n:int=27)->int:
    cp,cn=Counter(pos),Counter(neg);r,s=len(pos),len(neg)
    ans=math.factorial(n)//math.factorial(n-r-s)
    for x in cp.values(): ans//=math.factorial(x)
    for x in cn.values(): ans//=math.factorial(x)
    return ans

def hamming_systematic(k:int)->tuple[np.ndarray,np.ndarray]:
    r=1
    while 2**r < k+r+1:r+=1
    units=[1<<i for i in range(r)]
    data=[x for x in range(1,2**r) if x not in units][:k]
    H=np.zeros((r,k+r),dtype=np.uint8)
    for j,x in enumerate(data+units):
        for i in range(r):H[i,j]=(x>>i)&1
    P=H[:,:k]
    return H,P

def encode(bits:list[int],P:np.ndarray)->list[int]:
    m=np.array(bits,dtype=np.uint8);par=(P@m)%2
    return [int(x) for x in np.r_[m,par]]

def erasure_recover(code:list[int|None],H:np.ndarray)->list[int]:
    known=np.array([0 if x is None else x for x in code],dtype=np.uint8)
    er=[i for i,x in enumerate(code) if x is None]
    if not er:return known.tolist()
    rhs=(H@known)%2;M=H[:,er].copy();
    # binary Gaussian elimination for a unique erased solution
    aug=np.c_[M,rhs].astype(np.uint8);row=0;piv=[]
    for col in range(len(er)):
        pick=next((i for i in range(row,len(aug)) if aug[i,col]),None)
        if pick is None:continue
        aug[[row,pick]]=aug[[pick,row]]
        for i in range(len(aug)):
            if i!=row and aug[i,col]:aug[i]^=aug[row]
        piv.append(col);row+=1
    if len(piv)<len(er):raise ValueError('erasure pattern not recoverable')
    sol=np.zeros(len(er),dtype=np.uint8)
    for i,col in enumerate(piv):sol[col]=aug[i,-1]
    out=known.copy()
    for j,v in zip(er,sol):out[j]=v
    return out.tolist()

def build_payload()->dict:
    pi=PairIndex();rows=[]
    for w in range(4):
      for pos in partitions(w):
       for neg in partitions(w):
        c=fibre_counts(canonical_divisor(pos,neg),pi);m=type_multiplicity(pos,neg)
        rows.append({'weight':w,'positive':list(pos),'negative':list(neg),'divisor_multiplicity':m,**c})
    total_u=sum(r['divisor_multiplicity']*r['unordered_cumulative'] for r in rows)
    total_o=sum(r['divisor_multiplicity']*r['ordered_cumulative'] for r in rows)
    avg_u=sum(r['divisor_multiplicity']*r['unordered_cumulative']*(math.ceil(math.log2(r['unordered_cumulative'])) if r['unordered_cumulative']>1 else 0) for r in rows)/total_u
    ent_u=sum(r['divisor_multiplicity']*r['unordered_cumulative']*(math.log2(r['unordered_cumulative']) if r['unordered_cumulative']>1 else 0) for r in rows)/total_u
    avg_o=sum(r['divisor_multiplicity']*r['ordered_cumulative']*(math.ceil(math.log2(r['ordered_cumulative'])) if r['ordered_cumulative']>1 else 0) for r in rows)/total_o
    ent_o=sum(r['divisor_multiplicity']*r['ordered_cumulative']*(math.log2(r['ordered_cumulative']) if r['ordered_cumulative']>1 else 0) for r in rows)/total_o

    code_rows=[];all_ok=True
    for k in (13,16):
        H,P=hamming_systematic(k);n=H.shape[1]
        sample=[(7*i+3)%2 for i in range(k)];cw=encode(sample,P)
        one=True;two=True
        for i in range(n):
            x=cw.copy();x[i]=None;one &= erasure_recover(x,H)==cw
        for i in range(n):
          for j in range(i+1,n):
            x=cw.copy();x[i]=x[j]=None;two &= erasure_recover(x,H)==cw
        # all single-bit syndromes are distinct and nonzero => d>=3
        synd={tuple(H[:,i]) for i in range(n)}
        d3=len(synd)==n and tuple([0]*H.shape[0]) not in synd
        all_ok &= one and two and d3
        code_rows.append({'source_bits':k,'protected_bits':n,'parity_bits':n-k,'minimum_distance':3,'single_bit_error_correctable':True,'two_known_erasures_recoverable':two,'fits_bytes':math.ceil(n/8),'parity_check_columns':[int(sum(int(H[b,j])<<b for b in range(H.shape[0]))) for j in range(n)]})

    hist=Counter()
    for r in rows:
        s=r['unordered_cumulative'];bits=0 if s<=1 else math.ceil(math.log2(s));hist[bits]+=r['divisor_multiplicity']*s
    checks={
      'unordered_source_cardinality':total_u==sum(math.comb(len(EDGES)+w-1,w) for w in range(4)),
      'ordered_source_cardinality':total_o==sum(len(EDGES)**w for w in range(4)),
      'worst_unordered_13_bits':max(math.ceil(math.log2(r['unordered_cumulative'])) for r in rows)==13,
      'worst_ordered_16_bits':max(math.ceil(math.log2(r['ordered_cumulative'])) for r in rows)==16,
      'adaptive_unordered_average_below_four':avg_u<4,
      'adaptive_ordered_average_below_seven':avg_o<7,
      'all_shortened_hamming_checks':all_ok,
      'unordered_protected_frame_18_bits':code_rows[0]['protected_bits']==18,
      'ordered_protected_frame_21_bits':code_rows[1]['protected_bits']==21,
    };checks={k:bool(v) for k,v in checks.items()}
    payload={'schema':'w33.pass422.telemetry_coding_theorem.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
       'side_information_code':'given the measured divisor, encode only the lexicographic rank inside its exact history fibre',
       'worst_case':'13 bits unordered and 16 bits time ordered are information-theoretically optimal through weight three',
       'adaptive_gain':f'uniform-over-histories average fixed-rank length is {avg_u:.6f} unordered and {avg_o:.6f} ordered bits',
       'robust_frames':'shortened binary Hamming frames [18,13,3] and [21,16,3] correct one serialized bit error or any two known erasures',
       'memory':'both protected packets fit in three bytes',
       'boundary':'the channel model covers serialized bit flips and known erasures; analog timing estimation remains a front-end problem'},
      'source_statistics':{'unordered_histories':total_u,'ordered_histories':total_o,'unordered_average_bits':round(avg_u,12),'unordered_conditional_entropy':round(ent_u,12),'ordered_average_bits':round(avg_o,12),'ordered_conditional_entropy':round(ent_o,12),'unordered_length_histogram':{str(k):v for k,v in sorted(hist.items())}},
      'protected_codes':code_rows,'divisor_types':rows,'checks':checks}
    payload['certificate_sha256']=certificate(payload);return payload

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();t=json.dumps(p,indent=2,sort_keys=True)+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=t:raise SystemExit('Pass 422 certificate drift')
 else:write_json(a.output,p)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
