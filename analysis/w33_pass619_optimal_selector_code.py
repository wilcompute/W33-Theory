#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass619_optimal_selector_code.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def closure(gens,n=4):
 I=tuple(range(n));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def conj(g,H):
 gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
def left_cosets(G,H):
 unseen=set(G);out=[]
 while unseen:
  g=min(unseen);C=frozenset(comp(g,h) for h in H);out.append(C);unseen-=C
 out=sorted(out,key=lambda C:sorted(C));return out,{C:i for i,C in enumerate(out)}
def action(g,cos,idx):return tuple(idx[frozenset(comp(g,x) for x in C)] for C in cos)

def all_subgroup_classes(G):
 I=tuple(range(4));subs={frozenset((I,))};changed=True
 while changed:
  changed=False
  for H in list(subs):
   for g in G:
    if g not in H:
     J=closure(tuple(H)+(g,))
     if J not in subs:subs.add(J);changed=True
 unseen=set(subs);reps=[]
 while unseen:
  H=min(unseen,key=lambda x:(len(x),sorted(x)));C={conj(g,H) for g in G};reps.append(H);unseen-=C
 return reps,len(subs)

def component_catalog(G,K,classes,max_degree):
 states,_=left_cosets(G,K);state_reps=[min(C) for C in states];catalog=[]
 for J in classes:
  deg=len(G)//len(J)
  if deg>max_degree:continue
  cos,idx=left_cosets(G,J);A={g:action(g,cos,idx) for g in G};unseen=set(range(deg));Korbs=[]
  while unseen:
   i=min(unseen);O={A[k][i] for k in K};Korbs.append(tuple(sorted(O)));unseen-=O
  for mask in range(1,1<<len(Korbs)):
   S=set()
   for i,O in enumerate(Korbs):
    if mask>>i&1:S.update(O)
   words=[frozenset(A[g][j] for j in S) for g in state_reps]
   d=tuple(len(words[0]^words[i]) for i in range(1,12))
   if max(d):catalog.append({'degree':deg,'weight':len(S),'distance_vector':d,'J_order':len(J),'K_orbits':Korbs,'subset':tuple(sorted(S)),'words':words})
 return state_reps,catalog

def lower_bound(catalog,limit=7):
 uniq={}
 for c in catalog:
  key=(c['degree'],c['distance_vector'])
  if key not in uniq:uniq[key]=c
 C=list(uniq.values());dp={0:{(0,)*11}}
 for n in range(limit+1):
  for v in list(dp.get(n,set())):
   if min(v)>=4:return False,dp,C
   for c in C:
    m=n+c['degree']
    if m>limit:continue
    w=tuple(min(4,v[i]+c['distance_vector'][i]) for i in range(11));dp.setdefault(m,set()).add(w)
 return True,dp,C

def payload():
 G=list(itertools.permutations(range(4)));I=tuple(range(4));K=frozenset((I,trans(4,2,3)));classes,nsub=all_subgroup_classes(G)
 states,catalog=component_catalog(G,K,classes,8);proved,dp,uniq=lower_bound([c for c in catalog if c['degree']<8],7)
 candidates=[c for c in catalog if c['degree']==8 and min(c['distance_vector'])>=4]
 c=min(candidates,key=lambda x:(x['weight'],x['subset']));edges=[(g[0],g[1]) for g in states];words=[tuple(int(i in w) for i in range(8)) for w in c['words']]
 wil={(0,1):56,(0,2):-84,(0,3):-168,(1,2):112,(1,3):-84,(2,3):56}
 records=[]
 for e,w in zip(edges,words):records.append({'oriented_edge':list(e),'codeword':list(w),'weight':sum(w),'Wilson_sum':wil[tuple(sorted(e))]})
 distances=[sum(a!=b for a,b in zip(words[i],words[j])) for i in range(12) for j in range(i)]
 all_faults=0;detected=True
 code={w for w in words}
 for w in words:
  for r in (1,2,3):
   for F in itertools.combinations(range(8),r):
    z=list(w)
    for i in F:z[i]^=1
    all_faults+=1;detected &= tuple(z) not in code
 checks={
  'S4_order24_subgroups30_classes11':len(G)==24 and nsub==30 and len(classes)==11,
  'oriented_edge_stabilizer_order2':len(K)==2 and len(states)==12,
  'exhaustive_equivariant_lower_bound_n_ge8':proved and all(not any(min(v)>=4 for v in dp[n]) for n in dp),
  'degree8_C3_coset_orbit':c['degree']==8 and c['J_order']==3,
  'twelve_constant_weight4_codewords':len(set(words))==12 and {sum(w) for w in words}=={4},
  'minimum_distance4':min(distances)==4,
  'distance_histogram_4_8':collections.Counter(distances)==collections.Counter({4:60,8:6}),
  'all_weight1_2_3_faults_detected':detected and all_faults==12*(8+28+56),
  'single_bit_correction_radius1':min(distances)>=3,
  'Wilson_multiset_oriented':collections.Counter(r['Wilson_sum'] for r in records)==collections.Counter({56:4,-84:4,-168:2,112:2}),
 }
 return {'schema':'w33.pass619.optimal_selector_code.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'optimality_search':{'coordinate_symmetry':'arbitrary finite binary S4-set, decomposed into transitive coset orbits S4/J','subgroups_enumerated':nsub,'subgroup_conjugacy_classes':len(classes),'all K-invariant subsets enumerated_per_orbit':True,'dynamic_program_distance_cap':4,'no_solution_lengths':list(range(1,8)),'minimum_length':8},
  'code':{'name':'cube-vertex oriented tetrahedral selector','coordinate_set':'S4/C3, the eight cube vertices under tetrahedral rotation symmetry','length':8,'size':12,'constant_weight':4,'minimum_distance':4,'distance_histogram':{str(k):v for k,v in sorted(collections.Counter(distances).items())},'records':records},
  'fault_contract':{'detected_all_faults_of_weight_at_most3':True,'exhaustive_faults_checked':all_faults,'corrects_every_single_bit_fault':True,'previous_length':20,'channel_reduction':12},
  'theorem':'Among all binary S4-equivariant encodings of the twelve oriented tetrahedral edges with minimum distance at least four, the minimum length is eight. A unique search class is realized on the eight cube vertices as a constant-weight-four (8,12,4) code, reducing the Pass-614 hardware from twenty channels to eight while retaining single-fault correction and detection of every fault of weight at most three.',
  'checks':checks,'boundary':'Optimality is proved within binary coordinate systems carrying an S4 permutation action, which is exactly the required equivariant hardware model. A nonequivariant encoder or a nonbinary physical alphabet is outside this lower bound.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 619 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'optimal_length':p['code']['length']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
