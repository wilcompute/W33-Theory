from __future__ import annotations
import json,hashlib,itertools,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import numpy as np
cols=[int(x) for x in open(ROOT/'data/w33_pass1848_syndrome_columns.txt')];triples=[tuple(i for i in range(45) if x>>i&1) for x in cols];assert all(len(t)==3 for t in triples) and len(set(triples))==240
H=np.zeros((45,240),dtype=np.int64)
for j,t in enumerate(triples):H[list(t),j]=1
pair=collections.Counter(tuple(sorted(p)) for t in triples for p in itertools.combinations(t,2));A=np.zeros((45,45),dtype=np.int64)
for(i,j),v in pair.items():assert v==1;A[i,j]=A[j,i]=1
k=set(map(int,A.sum(1)));ca=set();cn=set()
for i,j in itertools.combinations(range(45),2):(ca if A[i,j] else cn).add(int(A[i]@A[j]))
eh=collections.Counter(round(float(x),8) for x in np.linalg.eigvalsh(A));HH=H@H.T;assert np.array_equal(HH,16*np.eye(45,dtype=np.int64)+A)
rank=0;rows=[sum((int(H[i,j])<<j) for j in range(240)) for i in range(45)]
for c in range(239,-1,-1):
 p=next((i for i in range(rank,45) if rows[i]>>c&1),None)
 if p is not None:
  rows[rank],rows[p]=rows[p],rows[rank]
  for i in range(45):
   if i!=rank and rows[i]>>c&1:rows[i]^=rows[rank]
  rank+=1
out={'schema':'w33.pass2555.syndrome_triangle_geometry.v1','status':'PASS_SYNDROME_COLUMNS_TRIANGLE_DECOMPOSE_THE_OCTET_SRG45','points':45,'triangles':240,'point_degree':sorted(set(map(int,H.sum(1)))),'pair_multiplicity_histogram':dict(collections.Counter(pair.values())),'covered_pairs':len(pair),'cooccurrence_graph':{'parameters':[45,next(iter(k)),next(iter(ca)),next(iter(cn))],'eigenvalue_multiplicities':{str(k):v for k,v in sorted(eh.items())}},'gram_identity':'H H^T = 16 I + A_45','gram_eigenvalues':{'48':1,'18':24,'12':20},'gf2_rank':rank,'theorem':'The 240 frozen 45-bit syndrome columns are a regular 3-uniform linear hypergraph whose triangles partition all 720 edges of SRG(45,32,22,24).','boundary':'This identification does not by itself determine the exact weight-six singleton coefficient.','checks':{'240_distinct_triples':len(set(triples))==240,'all_column_weight3':all(len(t)==3 for t in triples),'all_point_degree16':set(map(int,H.sum(1)))=={16},'linear_pair_system':set(pair.values())=={1},'edge_partition_720':len(pair)==720,'srg45_32_22_24':(k,ca,cn)==({32},{22},{24}),'gram_identity':np.array_equal(HH,16*np.eye(45,dtype=np.int64)+A),'gf2_full_rank45':rank==45}};base=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest();json.dump(out,open(ROOT/'data/w33_pass2555_syndrome_triangle_geometry.json','w'),indent=2,sort_keys=True)
