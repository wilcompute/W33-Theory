#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass598_s6_outer_automorphism.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def closure(gens):
 I=tuple(range(len(gens[0])));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def cycle_type(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=p[j]
  out.append(n)
 return tuple(sorted(out,reverse=True))

def payload():
 X=range(6);duads=tuple(itertools.combinations(X,2));did={frozenset(d):i for i,d in enumerate(duads)}
 synthemes=[]
 for P in itertools.combinations(duads,3):
  if len(set().union(*map(set,P)))==6:synthemes.append(frozenset(did[frozenset(d)] for d in P))
 synthemes=tuple(sorted(set(synthemes),key=lambda s:tuple(sorted(s))))
 totals=[]
 for C in itertools.combinations(range(15),5):
  words=[d for s in C for d in synthemes[s]]
  if sorted(words)==list(range(15)):totals.append(frozenset(C))
 totals=tuple(totals);tid={T:i for i,T in enumerate(totals)}
 def act_syntheme(g,s):
  ds=[]
  for di in synthemes[s]:
   a,b=duads[di];ds.append(did[frozenset((g[a],g[b]))])
  return synthemes.index(frozenset(ds))
 def outer(g):return tuple(tid[frozenset(act_syntheme(g,s) for s in T)] for T in totals)
 S6=list(itertools.permutations(X));image=frozenset(outer(g) for g in S6)
 t=trans(6,0,1);tt=comp(trans(6,0,1),comp(trans(6,2,3),trans(6,4,5)))
 S5=list(itertools.permutations(range(5)));subs=set()
 for tail in itertools.permutations((1,2,3,4)):subs.add(closure((cyc(5,(0,)+tail),)))
 subs=tuple(sorted(subs,key=lambda H:sorted(H)));sid={H:i for i,H in enumerate(subs)}
 def conj(g,H):
  gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
 singer=frozenset(tuple(sid[conj(g,H)] for H in subs) for g in S5)
 stabilizer=frozenset(outer(g) for g in S6 if g[5]==5)
 conjugator=None
 for c in itertools.permutations(range(6)):
  ci=inv(c)
  if frozenset(comp(comp(c,g),ci) for g in stabilizer)==singer:conjugator=c;break
 gens=[trans(6,i,i+1) for i in range(5)]
 hom_checks=all(outer(comp(g,h))==comp(outer(g),outer(h)) for g in gens for h in S6)
 checks={
  'duads15':len(duads)==15,
  'synthemes15':len(synthemes)==15,
  'synthematic_totals6':len(totals)==6,
  'outer_action_faithful_order720':len(image)==720,
  'generator_homomorphism_check':hom_checks,
  'transposition_maps_to_triple_transposition':cycle_type(outer(t))==(2,2,2),
  'triple_transposition_maps_to_transposition':cycle_type(outer(tt))==(2,1,1,1,1),
  'point_stabilizer_order120':len(stabilizer)==120,
  'Singer_S5_order120':len(singer)==120,
  'point_stabilizer_conjugate_to_Singer_fibre':conjugator is not None,
 }
 return {'schema':'w33.pass598.s6_outer_automorphism.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'classical_model':{'points':6,'duads':len(duads),'synthemes':len(synthemes),'synthematic_totals':len(totals),'totals':[sorted(T) for T in totals]},
  'outer_action':{'image_order':len(image),'transposition_image_cycle_type':list(cycle_type(outer(t))),'triple_transposition_image_cycle_type':list(cycle_type(outer(tt))),'proof_of_outerness':'Inner automorphisms preserve conjugacy classes, whereas this action exchanges the 2*1^4 and 2^3 involution classes.'},
  'Singer_weld':{'natural_point_stabilizer':'S5 fixing point 5','degree_six_action':'on six synthematic totals','Singer_action':'on six Sylow-5 pentagons','conjugating_permutation':list(conjugator) if conjugator else None,'identification':'The Pass-593/594 P1(F5) fibre is exactly the restriction of the classical outer S6 action to a point stabilizer.'},
  'theorem':'The six-pentagon Singer fibre is not merely analogous to the exceptional S5 action: it is explicitly conjugate to the point-stabilizer restriction of the duad-syntheme outer automorphism of S6.',
  'checks':checks,'boundary':'The conjugator depends on the chosen enumerations of totals and Sylow-5 subgroups. The conjugacy class of the degree-six action and the outer-automorphism conclusion are canonical.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 598 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'image_order':p['outer_action']['image_order']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
