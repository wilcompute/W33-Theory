#!/usr/bin/env python3
"""Pass 2309: reconstruct the complete four-orbit signature quotient and verify a nine-type witness.

This verifier does not require the large compressed 720-vector payload. It rebuilds
W(3,3), the 45 intrinsic K4,4 octets, and the 25,920-element PSp octet action in the
Pass-1601 coordinate order. Four representatives are identified by the exact
Pass-1822 orbit sizes, value histograms, and K4,4,4 anchor-cell patterns. Their
orbits contain 720 vectors. A literal nine-vector witness is then checked.
"""
from __future__ import annotations
import collections,hashlib,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass2309_signature_resolution_reconstruction.json'
EXPECTED='d9207bad35f30741d6dfabea0b1888d17249dc063deb317ccc113a639f9ac52a'
Q=3
REPRESENTATIVES=[[4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,4,1,1,1,1,1,1,0,2,4,1,1,1,1,1,1,4,0,2,1,1,1,1,1,1,2,4,0],[1,3,1,1,0,1,1,3,1,1,1,3,0,1,1,1,3,1,1,1,1,1,4,1,1,1,1,3,1,1,1,1,3,0,1,1,1,1,0,3,1,1,1,1,3],[2,1,1,1,1,3,1,1,1,1,1,1,1,1,3,2,1,1,1,3,1,1,1,1,2,1,1,1,1,1,3,1,1,1,2,1,1,1,1,1,1,1,1,1,4],[1,1,1,2,2,2,1,1,1,1,1,1,4,1,1,1,1,1,1,1,2,1,2,1,2,1,1,1,1,2,1,2,1,2,1,1,1,1,2,1,2,1,2,1,1]]
PATTERNS=[[0,2,4],[0,3,3],[1,2,3],[2,2,2]]
EXPECTED_ORBIT_SIZES=[270,135,270,45]
WITNESS=[{'signature_index':130,'class_label':0,'signature':[1,1,1,1,1,1,1,4,1,0,2,4,1,1,1,1,1,1,1,1,1,2,4,0,1,1,1,4,0,2,1,1,1,1,1,1,1,1,1,1,1,1,0,2,4]},{'signature_index':174,'class_label':0,'signature':[1,1,1,1,1,1,4,0,2,1,4,1,1,1,1,1,1,1,1,1,2,0,1,1,1,4,1,1,1,0,4,1,1,1,2,1,1,1,4,2,1,1,1,0,1]},{'signature_index':209,'class_label':2,'signature':[1,1,1,1,1,3,1,2,1,2,1,1,3,1,1,1,1,1,1,1,3,1,1,2,1,1,1,1,2,1,1,3,1,1,1,1,1,1,1,1,1,1,4,1,1]},{'signature_index':253,'class_label':0,'signature':[1,1,1,1,4,1,1,1,1,1,1,1,0,2,4,1,1,1,1,1,1,4,0,2,1,1,1,1,1,1,1,1,1,0,2,4,2,4,0,1,1,1,1,1,1]},{'signature_index':374,'class_label':3,'signature':[1,1,2,2,1,1,1,2,1,2,1,1,1,1,2,2,1,1,2,1,1,1,1,2,1,1,2,1,4,1,1,1,1,1,1,1,1,1,2,2,1,1,2,1,1]},{'signature_index':389,'class_label':1,'signature':[1,1,3,1,1,0,1,1,3,3,1,1,1,1,0,1,3,1,1,4,1,1,1,1,1,1,1,1,1,3,0,1,1,3,1,1,3,1,1,1,1,3,1,1,0]},{'signature_index':554,'class_label':3,'signature':[1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,2,2,2,1,1,1,1,1,1,2,2,2,1,1,1,1,1,1,2,2,2,1,1,1]},{'signature_index':616,'class_label':2,'signature':[2,1,1,3,1,1,1,1,1,1,1,1,3,1,1,2,1,1,1,1,1,1,1,1,4,1,1,1,1,3,1,1,1,1,2,1,1,1,1,1,3,1,1,1,2]},{'signature_index':657,'class_label':1,'signature':[3,1,1,1,1,3,1,0,1,1,0,1,1,3,1,1,1,3,3,1,1,0,1,1,1,1,3,1,1,0,1,1,3,3,1,1,1,1,1,1,1,1,1,4,1]}]
def csha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def normalize(v):
 w=tuple(int(x)%Q for x in v)
 for x in w:
  if x:
   z=pow(x,-1,Q);return tuple((z*y)%Q for y in w)
 raise ValueError
def symplectic(u,v):return (u[0]*v[3]-u[3]*v[0]+u[1]*v[2]-u[2]*v[1])%Q
def geometry():
 points=sorted({normalize(v) for v in itertools.product(range(Q),repeat=4) if any(v)});pidx={p:i for i,p in enumerate(points)}
 A=np.zeros((40,40),dtype=np.int64)
 for i,u in enumerate(points):
  for j in range(i+1,40):
   if symplectic(u,points[j])==0:A[i,j]=A[j,i]=1
 edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]];eidx={e:i for i,e in enumerate(edges)}
 octets=[];seen=set()
 for left in itertools.combinations(range(40),4):
  if any(A[a,b] for a,b in itertools.combinations(left,2)):continue
  right=tuple(v for v in range(40) if all(A[v,u] for u in left))
  if len(right)!=4 or any(A[a,b] for a,b in itertools.combinations(right,2)):continue
  key=tuple(sorted((tuple(left),tuple(right))))
  if key in seen:continue
  seen.add(key);octets.append((tuple(left),tuple(right)))
 K=np.zeros((45,240),dtype=np.int64)
 for r,(left,right) in enumerate(octets):
  for a in left:
   for b in right:K[r,eidx[tuple(sorted((a,b)))]]=1
 gram=K@K.T;np.fill_diagonal(gram,0);return points,pidx,A,edges,octets,(gram==1).astype(np.int64)
def transvection(points,pidx,v):
 v=normalize(v);out=[]
 for x in points:
  c=symplectic(x,v);y=tuple((x[i]+c*v[i])%3 for i in range(4));out.append(pidx[normalize(y)])
 return tuple(out)
def closure(gens):
 I=tuple(range(len(gens[0])));G=[I];seen={I};q=collections.deque([I])
 while q:
  a=q.popleft()
  for g in gens:
   b=tuple(g[a[i]] for i in range(len(a)))
   if b not in seen:seen.add(b);G.append(b);q.append(b)
 return G
def act(v,p):
 w=[0]*len(v)
 for i,j in enumerate(p):w[j]=int(v[i])
 return tuple(w)
def cells(A,a):
 non=[j for j in range(45) if j!=a and A[a,j]==0];unseen=set(non);out=[]
 while unseen:
  s=min(unseen);C={s};stack=[s]
  while stack:
   x=stack.pop()
   for y in list(unseen):
    if y!=x and A[x,y]==0 and y not in C:C.add(y);stack.append(y)
  unseen-=C;out.append(sorted(C))
 return sorted(out)
def anchors(A,t,p):
 out=[]
 for a,x in enumerate(t):
  if x!=4:continue
  cc=cells(A,a);vals=[]
  for c in cc:
   z=sorted({int(t[j]) for j in c});vals.append(z[0] if len(z)==1 else None)
  if None not in vals and sorted(vals)==sorted(p):out.append({'anchor':a,'cells':cc,'cell_values':vals})
 return out
def build():
 points,pidx,A,edges,octets,A45=geometry();oidx={tuple(map(tuple,o)):i for i,o in enumerate(np.array(octets,dtype=np.int16).tolist())}
 pgens=[transvection(points,pidx,v) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))];ogens=[]
 for p in pgens:
  op=[]
  for left,right in octets:
   key=tuple(sorted((tuple(sorted(p[x] for x in left)),tuple(sorted(p[x] for x in right)))));op.append(oidx[key])
  ogens.append(tuple(op))
 G=closure(ogens);orbits=[{act(r,p) for p in G} for r in REPRESENTATIVES];allset=set().union(*orbits);allsigs=sorted([list(v) for v in allset])
 cinv=[]
 for k,(r,O,p) in enumerate(zip(REPRESENTATIVES,orbits,PATTERNS)):
  cinv.append({'class_label':k,'orbit_size':len(O),'stabilizer_order':25920//len(O),'histogram':{str(a):b for a,b in sorted(collections.Counter(r).items())},'anchor_pattern':p,'matching_anchor_witnesses':anchors(A45,r,p),'representative':r,'orbit_sha256':csha(sorted([list(v) for v in O]))})
 selected=[dict(w) for w in WITNESS];orbitsets=[set(O) for O in orbits];sumvec=np.sum([z['signature'] for z in selected],axis=0).astype(int).tolist()
 checks={'w33_srg_40_12_2_4':len(points)==40 and len(edges)==240 and set(map(int,A.sum(1)))=={12},'octet_srg_45_32_22_24':len(octets)==45 and set(map(int,A45.sum(1)))=={32},'psp_order_25920':len(G)==25920,'class_orbit_sizes_270_135_270_45':[len(O) for O in orbits]==EXPECTED_ORBIT_SIZES,'class_orbits_disjoint':sum(map(len,orbits))==len(allset),'complete_signature_count_720':len(allsigs)==720,'all_signatures_sum_60':all(sum(v)==60 for v in allsigs),'all_signatures_satisfy_linear_equation':all(np.array_equal((A45+4*np.eye(45,dtype=int))@np.array(v,dtype=int),np.full(45,48)) for v in allsigs),'anchor_patterns_match_frozen_classes':all(x['matching_anchor_witnesses'] for x in cinv),'nine_witness_signatures_are_distinct':len({tuple(x['signature']) for x in selected})==9,'witness_membership_in_complete_set':all(x['signature'] in allsigs for x in selected),'witness_class_labels_correct':all(tuple(x['signature']) in orbitsets[x['class_label']] for x in selected),'witness_sum_is_12_all_45':sumvec==[12]*45}
 d={'schema':'w33.pass2309.signature_resolution_reconstruction.v1','status':'PASS_SIGNATURE_QUOTIENT_FEASIBLE_WITNESS','sources':{'geometry_producer':'analysis/w33_frame_hoffman_resolution_theorem.py','octet_producer':'analysis/w33_pass1601_1605_integral_frame_cokernel.py','frozen_signature_certificate':'data/w33_pass1821_1825_complete_cover_signature.json','frozen_signature_sha256':'5c3e60271e6108b8df1537b59416b008f3cd4d40cf7a14a5f1b1d90150cc3304','reconstruction_basis':'The frozen certificate classifies the complete signature set into four PSp orbits of sizes 270,135,270,45 with histograms and anchor-cell patterns (0,2,4),(0,3,3),(1,2,3),(2,2,2).'},'geometry':{'w33_points':40,'w33_edges':240,'octets':45,'octet_graph_parameters':[45,32,22,24],'psp_octet_action_order':25920,'psp_octet_action_sha256':csha(sorted([list(p) for p in G])),'linear_signature_equation':'(A45+4I)t=48*1'},'reconstruction':{'class_orbits':cinv,'orbit_sizes':[len(O) for O in orbits],'total_signatures':len(allsigs),'signature_set_sha256_in_pass1601_octet_order':csha(allsigs),'coordinate_statement':'This is a coordinate-conjugate reconstruction of the frozen four-orbit signature set. Feasibility of a uniform coordinate sum is invariant under the common octet relabeling.'},'witness':{'signature_count':9,'distinct_signature_count':len({tuple(x['signature']) for x in selected}),'class_multiplicities':{str(k):sum(x['class_label']==k for x in selected) for k in range(4)},'selected_signatures':selected,'coordinate_sum':sumvec,'target':[12]*45,'witness_sha256':csha(selected)},'checks':checks,'theorem':'The complete 720-type nonlinear octet-signature quotient admits nine distinct globally realizable signature vectors whose coordinatewise sum is 12*1_45.','boundary':'This removes the Pass-1825 nonlinear-signature obstruction but does not construct nine pairwise frame-disjoint exact covers. The next exact problem is a fibered lift from each selected signature type to its cover realizations with all 540 frames used once.'}
 assert all(checks.values());d['sha256_without_hash_field']=csha(d);return d
def main():
 d=build();assert d['sha256_without_hash_field']==EXPECTED;assert d==json.loads(OUT.read_text());print(json.dumps({'status':d['status'],'certificate':EXPECTED,'class_multiplicities':d['witness']['class_multiplicities'],'selected':9},sort_keys=True))
if __name__=='__main__':main()
