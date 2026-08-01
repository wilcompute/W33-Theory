#!/usr/bin/env python3
from __future__ import annotations
import sys,hashlib,json,base64,gzip,collections
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_pass1801_1805_common import build_geometry,build_bockstein
D=build_geometry(); B=build_bockstein(D); M=D['M']; J=B['J']; n=4860
rows=[]
for f in range(540): rows.append(sum(1<<(9*f+c) for c in range(9))|(1<<n))
inc=[np.flatnonzero(M[:,e]) for e in range(240)]
for e in range(240):
    for c in range(9): rows.append(sum(1<<(9*int(f)+c) for f in inc[e])|(1<<n))
for o in range(45):
    fs=np.flatnonzero(J[:,o]); assert len(fs)==72
    for c in range(9): rows.append(sum(1<<(9*int(f)+c) for f in fs))
for c,f in enumerate(inc[0]): rows.append((1<<(9*int(f)+c))|(1<<n))
assert len(rows)==3114
mask=(1<<n)-1; piv={}
for x in rows:
    while True:
        v=x&mask
        if not v:
            assert ((x>>n)&1)==0; break
        p=v.bit_length()-1
        if p in piv: x^=piv[p]
        else:
            for q in list(piv):
                if (piv[q]>>p)&1: piv[q]^=x
            piv[p]=x; break
for p in sorted(piv):
    x=piv[p]
    for q in [q for q in piv if q>p]:
        if (piv[q]>>p)&1: piv[q]^=x
for p,x in piv.items():
    assert ((x&mask)>>p)&1
    assert sum(((y&mask)>>p)&1 for q,y in piv.items() if q!=p)==0
rank=len(piv); assert rank==2349
sol=0
for p,x in piv.items():
    if (x>>n)&1: sol|=1<<p
assert all(((x&mask)&sol).bit_count()%2==((x>>n)&1) for x in rows)
X=np.fromiter(((sol>>i)&1 for i in range(n)),dtype=np.uint8,count=n).reshape(540,9)
frame=collections.Counter(map(int,X.sum(1))); edge=collections.Counter(map(int,(M.T@X).reshape(-1))); octet=collections.Counter(map(int,(J.T@X).reshape(-1)))
sol_bytes=sol.to_bytes((n+7)//8,'little')
sol_b64=base64.b64encode(gzip.compress(sol_bytes,mtime=0)).decode()
rref_hash=hashlib.sha256(('\n'.join(f'{p}:{piv[p]:x}' for p in sorted(piv))+'\n').encode()).hexdigest()
pivot_hash=hashlib.sha256(np.array(sorted(piv),dtype=np.uint16).tobytes()).hexdigest()
valid_frame=int(sum(v==1 for v in X.sum(1))); valid_edge=int(sum(v==1 for v in (M.T@X).reshape(-1))); valid_oct=int(sum(v==8 for v in (J.T@X).reshape(-1)))
res={'schema':'w33.pass1827.proof_producing_xor.v1','status':'PASS','variables':n,'equations':len(rows),'rank':rank,'nullity':n-rank,'consistent':True,'canonical_particular_solution':{'hamming_weight':sol.bit_count(),'gzip_base64':sol_b64,'raw_sha256':hashlib.sha256(sol_bytes).hexdigest()},'proof':{'pivot_count':rank,'pivot_columns_sha256':pivot_hash,'canonical_rref_sha256':rref_hash,'pivot_convention':'highest variable bit, exact GF(2), all pivot columns globally eliminated'},'integer_sum_histograms':{'frame':dict(sorted(frame.items())),'edge_color':dict(sorted(edge.items())),'octet_color':dict(sorted(octet.items()))},'exact_integer_rows_satisfied_by_xor_witness':{'frame_1':valid_frame,'of_frames':540,'edge_color_1':valid_edge,'of_edge_colors':2160,'octet_color_8':valid_oct,'of_octet_colors':405},'verdict':'The complete symmetry-fixed XOR system is satisfiable and has affine dimension 2511. This exact witness closes the XOR solve, but it is not a Hoffman resolution because parity permits odd/even sums other than 1/8. Therefore no SAT or UNSAT verdict for the nonlinear binary assignment is inferred.'}
raw=json.dumps(res,sort_keys=True,separators=(',',':')); res['sha256']=hashlib.sha256(raw.encode()).hexdigest()
assert res['sha256']=='1e40566ab1732fa0c518e773a44f61e0459c206a03b65a8d30f8c43c0cf7428a'
(ROOT/'data'/'w33_pass1827_xor_proof.json').write_text(json.dumps(res,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps(res,indent=2))
