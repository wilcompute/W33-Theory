#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass595_johnson_triangle_curvature.json'
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def closure(gens):
 I=tuple(range(len(gens[0])));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def sylow(B):
 B=tuple(sorted(B));S=set()
 for tail in itertools.permutations(B[1:]):S.add(closure((cyc(8,(B[0],)+tail),)))
 return tuple(sorted(S,key=lambda H:sorted(H)))
def conj(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def transport(A,B):
 A=set(A);B=set(B);a=next(iter(A-B));b=next(iter(B-A));outside=sorted(set(range(8))-(A|B));return comp(trans(8,a,b),trans(8,outside[0],outside[1]))
def ctype(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=p[j]
  out.append(n)
 return tuple(sorted(out,reverse=True))
def payload():
 triples=list(itertools.combinations(range(8),3));fib={A:sylow(set(range(8))-set(A)) for A in triples};adj=[[] for _ in triples]
 for i,A in enumerate(triples):
  for j in range(i+1,len(triples)):
   B=triples[j]
   if len(set(A)&set(B))==2:
    g=transport(A,B);adj[i].append((j,g));adj[j].append((i,g))
 def fmap(A,B,g):
  idx={P:i for i,P in enumerate(fib[B])};return tuple(idx[conj(g,P)] for P in fib[A])
 def pc(q,p):return tuple(q[p[i]] for i in range(6))
 path=[None]*56;path[0]=tuple(range(6));Q=deque([0])
 while Q:
  i=Q.popleft();A=triples[i]
  for j,g in adj[i]:
   if path[j] is None:path[j]=pc(fmap(A,triples[j],g),path[i]);Q.append(j)
 counts=Counter();incident=[Counter() for _ in triples]
 for i,A in enumerate(triples):
  ed={j:g for j,g in adj[i]}
  for j,k in itertools.combinations(sorted(ed),2):
   if not(i<j<k) or len(set(triples[j])&set(triples[k]))!=2:continue
   gjk=next(g for x,g in adj[j] if x==k);gki=next(g for x,g in adj[k] if x==i)
   local=pc(fmap(triples[k],A,gki),pc(fmap(triples[j],triples[k],gjk),fmap(A,triples[j],ed[j])))
   h=pc(inv(path[i]),pc(local,path[i]));sets=[set(triples[x]) for x in (i,j,k)];kind='tetrahedral' if (len(set.intersection(*sets)),len(set.union(*sets)))==(1,4) else 'top';key=(kind,ctype(h));counts[key]+=1
   for v in (i,j,k):incident[v][key]+=1
 meta={('top',(1,1,1,1,1,1)):('flat_identity',1,6),('top',(2,2,1,1)):('top_double_transposition',2,2),('top',(3,3)):('top_order_three',3,0),('tetrahedral',(2,2,2)):('tetrahedral_fixed_point_free_involution',2,0)}
 rows=[]
 for key,(label,order,fixed) in meta.items():
  n=counts[key];rows.append({'triangle_type':key[0],'fibre_cycle_type':list(key[1]),'holonomy_label':label,'holonomy_order':order,'count':n,'count_per_base_vertex_global':n//56,'incident_count_histogram':dict(sorted(Counter(c[key] for c in incident).items())),'permutation_character':fixed,'augmentation_character':fixed-1,'augmentation_wilson_contribution':n*(fixed-1)})
 total=sum(r['count'] for r in rows);aug=sum(r['augmentation_wilson_contribution'] for r in rows);perm=sum(r['count']*r['permutation_character'] for r in rows)
 lav=[sum(n*(meta[k][2]-1) for k,n in c.items()) for c in incident];lpv=[sum(n*meta[k][2] for k,n in c.items()) for c in incident]
 expected=Counter({('top',(1,1,1,1,1,1)):112,('top',(2,2,1,1)):112,('top',(3,3)):336,('tetrahedral',(2,2,2)):280})
 checks={'johnson_vertices56':len(triples)==56,'johnson_degree15':{len(x) for x in adj}=={15},'triangle_total840':total==840,'triangle_factorization56x15':total==56*15,'top_triangles560':sum(v for (k,_),v in counts.items() if k=='top')==560,'tetrahedral_triangles280':sum(v for (k,_),v in counts.items() if k=='tetrahedral')==280,'four_class_census_exact':counts==expected,'tetrahedral_holonomy_fixed_point_free_involutions':counts[('tetrahedral',(2,2,2))]==280,'top_holonomy_orders123':{r['holonomy_order'] for r in rows if r['triangle_type']=='top'}=={1,2,3},'incident_triangle_count45':{sum(c.values()) for c in incident}=={45},'tetrahedral_incidence15':{c[('tetrahedral',(2,2,2))] for c in incident}=={15},'top_incidence30':{sum(v for (k,_),v in c.items() if k=='top') for c in incident}=={30},'augmentation_wilson_sum56':aug==56,'average_local_augmentation3':sum(lav)==56*3,'gauss_bonnet_incidence':sum(lav)==3*aug,'permutation_wilson_sum896':perm==896,'permutation_split840_plus56':perm==total+aug,'average_local_permutation48':sum(lpv)==56*48}
 return {'schema':'w33.pass595.johnson_triangle_curvature.v1','status':'PASS' if all(checks.values()) else 'FAIL','base':{'graph':'Johnson graph J(8,3)','vertices':56,'degree':15,'triangles':total,'triangle_types':{'top':560,'tetrahedral':280}},'connection':{'source':'Pass 594 six-pentagon Singer connection','fibre':'six Sylow-5 subgroups / P1(F5)','holonomy_group':'S5 in its exceptional degree-six action','gauge_invariance':'Cycle types, orders, fixed-point counts, character values, and global totals are invariant under vertex-wise gauge conjugation.'},'holonomy_census':rows,'wilson_curvature':{'augmentation_character_rule':'chi_aug(g)=#Fix_6(g)-1','global_augmentation_wilson_sum':aug,'global_identity':'112*5 + 112*1 - 336 - 280 = 56','local_incident_augmentation_trace_histogram':dict(sorted(Counter(lav).items())),'average_local_incident_augmentation_trace':sum(lav)//56,'discrete_gauss_bonnet_identity':'(1/3) times the sum of the 56 incident-vertex traces equals 56','permutation_character_sum':perm,'permutation_identity':'896 = 840 base triangles + 56 augmentation curvature','local_incident_permutation_trace_histogram':dict(sorted(Counter(lpv).items())),'average_local_incident_permutation_trace':sum(lpv)//56},'interpretation':'The two Johnson triangle geometries separate holonomy sharply: every tetrahedral triangle is a fixed-point-free involution, while top triangles split 1:1:3 into identity, double-transposition, and order-three classes. In the five-dimensional augmentation fibre the integrated Wilson trace equals the 56 base vertices.','boundary':'This is a finite Wilson/Gauss-Bonnet identity for the stated Pass-594 connection, not a continuum curvature theorem or a canonical 56-to-40 W33 identification. The canonical least-outside edge rule is not vertex-transitive, so only the integrated and averaged trace laws are asserted.','checks':checks}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'triangles':p['base']['triangles'],'augmentation_wilson_sum':p['wilson_curvature']['global_augmentation_wilson_sum']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
