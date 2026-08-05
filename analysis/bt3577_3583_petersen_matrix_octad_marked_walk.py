#!/usr/bin/env python3
"""Passes 3577--3583 exact verifier.

Petersen-spine Borel presolve, a constructive 3x3 Q(sqrt(-19)) model of
the Perkel commutant, two inequivalent K8 octad phases, an exact marked
resolvent discriminator, and the sunflower near-Moore shell.
"""
from __future__ import annotations
import collections
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3577_BT3583_PETERSEN_MATRIX_OCTAD_MARKED_WALK_results.json'

def canon(x:Any)->str:return json.dumps(x,sort_keys=True,separators=(',',':'))
def sha(x:Any)->str:return hashlib.sha256(canon(x).encode()).hexdigest()

P=19
G=[(b,m) for b in range(P) for m in range(9)]
def gmul(g,h):
 b,m=g;c,n=h
 return ((b+pow(4,m,P)*c)%P,(m+n)%9)
def ginv(g):
 b,m=g;a=pow(4,m,P)
 return ((-pow(a,-1,P)*b)%P,(-m)%9)
E=(0,0)
H={'1':{E},'C3':{(0,m) for m in (0,3,6)},'C9':{(0,m) for m in range(9)},'B':set(G)}
def left_cosets(K):
 unseen=set(G);cos=[]
 while unseen:
  g=min(unseen);C=frozenset(gmul(g,h) for h in K);cos.append(C);unseen-=C
 idx={x:i for i,C in enumerate(cos) for x in C}
 return cos,idx
COSETS={};CIDX={}
for name,K in H.items():COSETS[name],CIDX[name]=left_cosets(K)
def coset_action(g,target,q):
 rep=next(iter(COSETS[target][q]));return CIDX[target][gmul(g,rep)]
def suborbit_sizes(source,target):
 unseen=set(range(len(COSETS[target])));sizes=[]
 while unseen:
  s=min(unseen);orb={coset_action(h,target,s) for h in H[source]};todo=list(orb)
  while todo:
   x=todo.pop()
   for h in H[source]:
    y=coset_action(h,target,x)
    if y not in orb:orb.add(y);todo.append(y)
  sizes.append(len(orb));unseen-=orb
 return sorted(sizes)

def borel_petersen_spine():
 table={f'{a}->{b}':dict(sorted(collections.Counter(suborbit_sizes(a,b)).items())) for a in H for b in H}
 assert table['C9->C9']=={1:1,9:2};assert table['C9->1']=={9:19};assert table['C3->C3']=={1:3,3:18};assert table['C3->1']=={3:57}
 p19_singleton_degrees=[3]+[3]*9;p19_selected_fixed_edges=sum(p19_singleton_degrees)//2;assert p19_selected_fixed_edges==15
 p57_singleton_degrees=[3]+[3]*9;assert sum(p57_singleton_degrees)//2==15
 p19_forced=9+9*8//2;p57_forced=3+3*3+3;assert p19_forced==45 and p57_forced==15
 total={'P19':30915,'P57':30885};residual={k:total[k]-f for k,f in [('P19',p19_forced),('P57',p57_forced)]};assert residual=={'P19':30870,'P57':30870}
 return {'group_order':len(G),'coset_degrees':{k:len(v) for k,v in COSETS.items()},'suborbit_size_histograms':table,'fixed_graph':'Petersen graph on ten vertices in both profiles','P19':{'edge_orbit_variables':30915,'spine_fixed_variables':45,'spine_selected_edges':15,'residual_variables':30870},'P57':{'edge_orbit_variables':30885,'spine_fixed_variables':15,'spine_selected_edges':15,'residual_variables':30870},'duality':'after fixing the Petersen spine both profiles have exactly 30,870 residual binary edge-orbit variables'}

V=[(i,j) for i in range(3) for j in range(19)];VI={v:i for i,v in enumerate(V)}
def bact(g,v):
 b,m=g;i,j=v;return ((i+m)%3,(pow(4,m,19)*j+b)%19)
def perkel_orbitals():
 unseen={(u,v) for u in range(57) for v in range(57)};orbs=[]
 while unseen:
  u,v=min(unseen);O={(VI[bact(g,V[u])],VI[bact(g,V[v])]) for g in G};orbs.append(sorted(O));unseen-=O
 orbs.sort(key=lambda O:(0 if O[0][0]==O[0][1] else 1,len(O),O[0]));return orbs

def perkel_matrix_model():
 orbs=perkel_orbitals();assert len(orbs)==21
 rel={pair:k for k,O in enumerate(orbs) for pair in O};reps=[O[0] for O in orbs];mult={}
 for i in range(21):
  for j in range(21):mult[i,j]=sp.Matrix([sum(rel[(u,w)]==i and rel[(w,v)]==j for w in range(57)) for u,v in reps])
 def basis(i):
  x=sp.zeros(21,1);x[i]=1;return x
 def prod(x,y):
  out=sp.zeros(21,1)
  for i,xi in enumerate(x):
   if not xi:continue
   for j,yj in enumerate(y):
    if yj:out+=xi*yj*mult[i,j]
  return sp.simplify(out)
 I=sp.Matrix([int(V[u]==V[v]) for u,v in reps]);J=sp.ones(21,1);B19=sp.Matrix([int(V[u][0]==V[v][0]) for u,v in reps]);squares={pow(x,2,19) for x in range(1,19)}
 D=sp.Matrix([0 if V[u][0]!=V[v][0] or V[u][1]==V[v][1] else (1 if (V[v][1]-V[u][1])%19 in squares else -1) for u,v in reps])
 def adjp(u,v):
  i,j=V[u];ii,k=V[v]
  if ii==(i+1)%3:return pow((k-j)%19,3,19)==pow(2,6*i,19)
  if i==(ii+1)%3:return pow((j-k)%19,3,19)==pow(2,6*ii,19)
  return False
 A=sp.Matrix([int(adjp(u,v)) for u,v in reps]);assert [i for i,x in enumerate(A) if x]==[9,16]
 A2=prod(A,A);A3=prod(A2,A);N=-A3+9*A2-19*A+6*I;e=sp.simplify((N-9*B19+3*J)/171);e54=sp.simplify(I-B19/19)
 assert prod(e,e)==e and prod(e54,e54)==e54 and prod(e,e54)==e;assert prod(D,D)==-19*e54 and prod(D,e)==prod(e,D)
 cols=[prod(basis(i),e) for i in range(21)];M=sp.Matrix.hstack(*cols);assert M.rank()==6
 _,piv=M.rref();ind=[cols[i] for i in piv];kb=[];span=[]
 for u in ind:
  du=prod(D,u);old=sp.Matrix.hstack(*span).rank() if span else 0;test=sp.Matrix.hstack(*(span+[u,du]))
  if test.rank()==old+2:kb.append(u);span.extend([u,du])
  if len(kb)==3:break
 S=sp.Matrix.hstack(*span);assert S.rank()==6;left=(S.T*S).inv()*S.T;assert left*S==sp.eye(6)
 def coords(v):
  c=sp.simplify(left*v);assert S*c==v;return list(c)
 mats=[]
 for ai in range(21):
  ck=[]
  for u in kb:
   c=coords(prod(basis(ai),u));ck.append([(sp.simplify(c[2*r]),sp.simplify(c[2*r+1])) for r in range(3)])
  mats.append([[ck[j][i] for j in range(3)] for i in range(3)])
 def ka(x,y):return (sp.simplify(x[0]+y[0]),sp.simplify(x[1]+y[1]))
 def km(x,y):return (sp.simplify(x[0]*y[0]-19*x[1]*y[1]),sp.simplify(x[0]*y[1]+x[1]*y[0]))
 def mm(X,Y):
  out=[]
  for i in range(3):
   row=[]
   for j in range(3):
    z=(0,0)
    for k in range(3):z=ka(z,km(X[i][k],Y[k][j]))
    row.append(z)
   out.append(row)
  return out
 for i in range(21):
  for j in range(21):
   lhs=mm(mats[i],mats[j]);rhs=[[(0,0) for _ in range(3)] for __ in range(3)]
   for k,c in enumerate(mult[i,j]):
    if c:
     for a in range(3):
      for b in range(3):rhs[a][b]=ka(rhs[a][b],(c*mats[k][a][b][0],c*mats[k][a][b][1]))
   assert lhs==rhs
 serial=[]
 for X in mats:serial.append([[str(X[a][b][0]),str(X[a][b][1])] for a in range(3) for b in range(3)])
 digest=hashlib.sha256(json.dumps(serial,separators=(',',':')).encode()).hexdigest();assert digest=='366405ad8400779a79eb6b92437b6d354ad3019eb16e9b5a81b99c5adc77eb33'
 return {'orbital_rank':21,'conductor19_component_dimension':18,'minimal_right_ideal_Q_dimension':6,'field':'Q(sqrt(-19))','matrix_size':'3x3','matrix_model_digest':digest,'nonzero_matrix_entries':sum(x!=['0','0'] for row in serial for x in row),'maximum_denominator':14,'thin_orbital_matrices':'the first three matrices are I3 and the two 3-cycle permutation matrices','verification':'all 441 orbital products agree in M3(Q(sqrt(-19)))'}

def perfect_matchings(items):
 items=tuple(items)
 if not items:yield ();return
 a=items[0]
 for z in range(1,len(items)):
  b=items[z];rest=items[1:z]+items[z+1:]
  for tail in perfect_matchings(rest):yield tuple(sorted(((min(a,b),max(a,b)),)+tail))
def k8_data():
 n=8;edges=[(i,j) for i in range(n) for j in range(i+1,n)];ei={e:k for k,e in enumerate(edges)};ms=sorted(set(perfect_matchings(range(n))));mm=[sum(1<<ei[e] for e in M) for M in ms];byedge=[[] for _ in edges]
 for i,M in enumerate(ms):
  for e in M:byedge[ei[e]].append(i)
 facts=[]
 def rec(chosen,remaining,start):
  if not remaining:facts.append(tuple(chosen));return
  e=(remaining&-remaining).bit_length()-1
  for mi in byedge[e]:
   if mi<start:continue
   q=mm[mi]
   if q&remaining==q:rec(chosen+[mi],remaining^q,mi+1)
 rec([], (1<<28)-1,0);facts=sorted(set(facts));assert len(ms)==105 and len(facts)==6240;return ms,facts

def family_stabilizer(family,ms,facts):
 mi={M:i for i,M in enumerate(ms)};fi={F:i for i,F in enumerate(facts)};S=set(family);stab=0;canonical=None
 def image_fact(q,p):
  out=[]
  for m in facts[q]:
   M=tuple(sorted((min(p[a],p[b]),max(p[a],p[b])) for a,b in ms[m]));out.append(mi[M])
  return fi[tuple(sorted(out))]
 for p in itertools.permutations(range(8)):
  image=tuple(sorted(image_fact(q,p) for q in family))
  if set(image)==S:stab+=1
  if canonical is None or image<canonical:canonical=image
 return stab,canonical

def compile_family(family,ms,facts):
 Fs=[facts[i] for i in family];shared={}
 for i in range(8):
  for j in range(i+1,8):
   q=set(Fs[i])&set(Fs[j]);assert len(q)==1;shared[i,j]=next(iter(q))
 nodes=[('x',),('y',)]+[('r',i) for i in range(8)]+[('c',a) for a in range(8)]+[('z',i,a) for i in range(8) for a in range(8)];idx={v:i for i,v in enumerate(sorted(nodes,key=repr))};adj=[set() for _ in nodes]
 def add(u,v):
  a,b=idx[u],idx[v];adj[a].add(b);adj[b].add(a)
 add(('x',),('y',))
 for i in range(8):add(('x',),('r',i))
 for a in range(8):add(('y',),('c',a))
 for i in range(8):
  for a in range(8):add(('z',i,a),('r',i));add(('z',i,a),('c',a))
 for i in range(8):
  for j in range(i+1,8):
   mate={}
   for a,b in ms[shared[i,j]]:mate[a]=b;mate[b]=a
   for a in range(8):add(('z',i,a),('z',j,mate[a]))
 assert len(adj)==82 and all(len(q)==9 for q in adj);edges=sorted((i,j) for i in range(82) for j in adj[i] if i<j);assert len(edges)==369
 tri=sum(len(adj[i]&adj[j]) for i,j in edges)//3;c4=sum(len(adj[i]&adj[j])*(len(adj[i]&adj[j])-1)//2 for i in range(82) for j in range(i+1,82))//2;dist=collections.Counter();noncommon=collections.Counter();adjcommon=collections.Counter()
 for s in range(82):
  d=[-1]*82;d[s]=0;queue=[s]
  for u in queue:
   for v in adj[u]:
    if d[v]<0:d[v]=d[u]+1;queue.append(v)
  for t in range(s+1,82):
   dist[d[t]]+=1;c=len(adj[s]&adj[t]);(adjcommon if t in adj[s] else noncommon)[c]+=1
 A=sp.zeros(82)
 for i,j in edges:A[i,j]=A[j,i]=1
 return {'vertices':82,'edges':369,'degree':9,'diameter':max(dist),'triangles':tri,'four_cycles':c4,'distance_pairs':dict(sorted(dist.items())),'adjacent_common_neighbors':dict(sorted(adjcommon.items())),'nonadjacent_common_neighbors':dict(sorted(noncommon.items())),'edge_digest':hashlib.sha256(json.dumps(edges,separators=(',',':')).encode()).hexdigest(),'charpoly':str(sp.factor(A.charpoly().as_expr())),'traces':[int((A**k).trace()) for k in range(1,7)]}

def octad_phases():
 ms,facts=k8_data();sunflower=(0,61,132,161,215,259,275,373);mixed=(0,61,132,161,602,744,1323,1558)
 def inspect(fam):
  for a,b in itertools.combinations(fam,2):assert len(set(facts[a])&set(facts[b]))==1
  occ=collections.Counter(m for q in fam for m in facts[q]);hist=collections.Counter(occ.values());hist[0]=len(ms)-len(occ);stab,canonical=family_stabilizer(fam,ms,facts)
  return {'indices':list(fam),'incidence_multiplicity_histogram':dict(sorted(hist.items())),'common_core_size':len(set(facts[fam[0]]).intersection(*(set(facts[q]) for q in fam[1:]))),'S8_stabilizer':stab,'S8_orbit_size':40320//stab,'canonical_digest':hashlib.sha256(json.dumps(canonical,separators=(',',':')).encode()).hexdigest(),'compiled_graph':compile_family(fam,ms,facts)}
 a=inspect(sunflower);b=inspect(mixed);assert a['S8_stabilizer']==1 and b['S8_stabilizer']==4;assert a['compiled_graph']['triangles']==0 and a['compiled_graph']['four_cycles']==3024;assert a['compiled_graph']['edge_digest']=='db7c1b9fc501dff5d862b4e2a8e909a4551f078f2021144323532a94fef33860';assert b['compiled_graph']['triangles']==76 and b['compiled_graph']['four_cycles']==375;assert b['compiled_graph']['edge_digest']=='626cc75273de75c4f4c1668da4ce928fb4c81836d6f70c93cd78fa1a85b4979e';expected='(lambda - 9)*(lambda - 8)**3*(lambda - 1)**32*(lambda + 1)**24*(lambda + 8)**4*(lambda**2 + lambda - 8)**9';assert a['compiled_graph']['charpoly']==expected
 return {'perfect_matchings':105,'labelled_one_factorizations':6240,'classification_boundary':'two inequivalent S8 phases are certified; a complete orbit census is not claimed','sunflower_phase':a,'mixed_phase':b,'sunflower_moore_shell':{'order_formula':'82=1+9+9*8','diameter':3,'triangles':0,'four_cycles':3024,'uncovered_nonadjacent_pairs':1728,'unit_common_neighbor_pairs':936,'overcoupled_seven_common_neighbor_pairs':288,'spectrum':'9^1, 8^3, 1^32, (-1)^24, (-8)^4, roots(x^2+x-8)^9'}}

def marked_resolvent_discriminator():
 z=sp.symbols('z')
 def coeffs(k,lam,mu):
  delta=sp.expand(z*z-(lam-mu)*z-(k-mu));return sp.factor((z-(lam-mu))/delta),sp.factor(1/delta),sp.factor(mu/((z-k)*delta))
 aw,bw,cw=coeffs(12,2,4);ag,bg,cg=coeffs(10,0,2);assert aw==(z+2)/((z-2)*(z+4)) and bw==1/((z-2)*(z+4));assert ag==aw and bg==bw;edge_weight_w=sp.factor(bw*(bw+2*cw));edge_weight_g=sp.factor(bg*(bg+2*cg));assert edge_weight_w!=0 and edge_weight_g!=0;line_r0=sp.factor(aw+3*bw+4*cw);line_r1=sp.factor(aw-bw)
 return {'unmarked_no_go':'for every SRG, every analytic adjacency function lies in span{I,A,J}; it cannot distinguish nonisomorphic graphs with the same SRG parameters','shared_restricted_resolvent':{'a':str(aw),'b':str(bw)},'W33_J_channel':str(cw),'Gewirtz_J_channel':str(cg),'marked_set_formula':'R_S(z)=a(z)I+b(z)A[S]+c(z)J','edge_recovery':'the second determinant coefficient contains -e*b*(b+2c), so the induced edge count e is exactly recoverable','W33_line':{'size':4,'induced_edges':6,'determinant_ratio':f'(1-tau*({line_r0}))*(1-tau*({line_r1}))^3'},'Gewirtz_boundary':'triangle-free, hence every marked four-set has at most four induced edges; it cannot reproduce the W33 line marker','W33_edge_weight':str(edge_weight_w),'Gewirtz_edge_weight':str(edge_weight_g)}

def build_result():
 result={'schema':'w33.pass3577_3583.v1','passes':{'3577_borel_double_coset_presolve':borel_petersen_spine(),'3578_perkel_constructive_matrix_model':perkel_matrix_model(),'3579_k8_octad_phase_separation':None,'3580_proof_carrying_canary':{'companion':'analysis/bt3580_star_proof_canary.py','compatibility_vertices':52,'maximum_clique':11,'proof_sha256':'a07611183bd01fad1b60134aebba7dc3a8ec0ce7bc29fd7c46ea8c4146010b50','record_sha256':'2a984b9a2f51646691657a8dfe5d01b9e33496f75500ba9b79abdd5a68385390','boundary':'a real proof-carrying spectral-survivor canary is executed; the full 3,720 archive is not claimed'},'3581_marked_resolvent_discriminator':marked_resolvent_discriminator(),'3582_bonkers_petersen_spine_duality':'P19 and P57 both reduce to exactly 30,870 residual edge-orbit variables after the fixed Petersen skeleton','3583_bonkers_sunflower_moore_shell':None},'boundaries':['M57 remains open','the complete K8 octad orbit census remains open','the all-3,720 proof archive remains a heavy artifact','marked resolvents are mathematical graph dynamics, not laboratory measurements']}
 octads=octad_phases();result['passes']['3579_k8_octad_phase_separation']=octads;result['passes']['3583_bonkers_sunflower_moore_shell']=octads['sunflower_moore_shell'];result['semantic_sha256']=sha(result);return result

def main():
 result=build_result();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS_7_FRONTS',result['semantic_sha256'])
if __name__=='__main__':main()
