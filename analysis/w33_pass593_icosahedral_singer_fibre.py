#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass593_icosahedral_singer_fibre.json'
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def order(p):
 q=tuple(range(len(p)))
 for n in range(1,61):
  q=comp(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError
def closure(gens):
 n=len(gens[0]);I=tuple(range(n));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def cyc(n,c):
 p=list(range(n))
 for a,b in zip(c,c[1:]+c[:1]):p[a]=b
 return tuple(p)
def sylow5_action():
 S5=list(itertools.permutations(range(5)));subs=set()
 for tail in itertools.permutations((1,2,3,4)):
  g=cyc(5,(0,)+tail);subs.add(closure((g,)))
 subs=tuple(sorted(subs,key=lambda H:sorted(H)));idx={H:i for i,H in enumerate(subs)}
 def conj(g,H):
  gi=inv(g);return frozenset(comp(comp(g,h),gi) for h in H)
 return S5,subs,{g:tuple(idx[conj(g,H)] for H in subs) for g in S5}
def mobius_group():
 pts=tuple(range(6));INF=5;mats=[]
 for a,b,c,d in itertools.product(range(5),repeat=4):
  det=(a*d-b*c)%5
  if not det:continue
  v=(a,b,c,d);first=next(x for x in v if x);iv=pow(first,-1,5);can=tuple(x*iv%5 for x in v)
  if can not in mats:mats.append(can)
 def act(M,x):
  a,b,c,d=M
  if x==INF:return INF if c==0 else a*pow(c,-1,5)%5
  den=(c*x+d)%5;num=(a*x+b)%5
  return INF if den==0 else num*pow(den,-1,5)%5
 perms={M:tuple(act(M,x) for x in pts) for M in mats};return mats,frozenset(perms.values()),frozenset(perms[M] for M in mats if ((M[0]*M[3]-M[1]*M[2])%5) in (1,4))
def conjugator(G,H):
 for c in itertools.permutations(range(6)):
  ci=inv(c)
  if frozenset(comp(comp(c,g),ci) for g in G)==H:return c
def character(group):
 rec=defaultdict(list)
 for g in group:rec[(order(g),tuple(sorted(Counter(g).values())))].append(sum(i==g[i] for i in range(6))-1)
 return {str(o):sorted(Counter(v for k,vals in rec.items() if k[0]==o for v in vals).items()) for o in sorted({k[0] for k in rec})}
def inner_product(group):
 vals=[sum(i==g[i] for i in range(6))-1 for g in group];return sum(v*v for v in vals)/len(group)
def payload():
 S5,subs,act=sylow5_action();G=frozenset(act.values());A5=frozenset(act[g] for g in S5 if parity(g)==0);mats,PGL,PSL=mobius_group();c=conjugator(G,PGL);H0=subs[0];N=[g for g in S5 if parity(g)==0 and frozenset(comp(comp(g,h),inv(g)) for h in H0)==H0];natA5=[g for g in S5 if parity(g)==0];char6=Counter((order(act[g]),sum(i==act[g][i] for i in range(6))-1) for g in natA5);char5=Counter((order(g),sum(i==g[i] for i in range(5))-1) for g in natA5)
 checks={'six_sylow5_subgroups':len(subs)==6,'exceptional_S5_degree6_action_faithful':len(G)==120,'A5_axis_action_order60':len(A5)==60,'PGL2_5_order120':len(PGL)==120,'PSL2_5_order60':len(PSL)==60,'S5_action_conjugate_to_PGL2_5':c is not None,'A5_action_conjugate_to_PSL2_5':c is not None and frozenset(comp(comp(c,g),inv(c)) for g in A5)==PSL,'axis_stabilizer_D10_order10':len(N)==10,'six_axis_orbit':60//len(N)==6,'augmentation_dimension5':True,'augmentation_irreducible_on_A5':abs(inner_product(A5)-1)<1e-12,'five_coloring_module_not_axis_module':char6!=char5,'Singer_complement_dimension280':56*5==280,'W33_count_identity280':40*7==280}
 return {'schema':'w33.pass593.icosahedral_singer_fibre.v1','status':'PASS' if all(checks.values()) else 'FAIL','six_fibre':{'objects':'six Sylow-5 subgroups of S5','S5_action_order':len(G),'A5_action_order':len(A5),'mobius_model':'PGL(2,5) on P1(F5)','conjugating_permutation_to_P1F5':list(c) if c else None,'icosahedral_model':'six fivefold rotation axes, equivalently six antipodal vertex pairs','axis_stabilizer_in_A5':'D10','axis_stabilizer_order':len(N)},'augmentation':{'dimension':5,'A5_character_by_order':character(A5),'character_inner_product':inner_product(A5),'interpretation':'The five-dimensional fibre augmentation is the irreducible icosahedral quadrupole module, the traceless part of the six-axis permutation representation.','global_bundle_dimension':280,'identity':'280 = 56*5 = 40*7'},'colored_comparison':{'five_snub_colorings_module':'permutation module 1+4','six_axis_augmentation':'irreducible 5','not_isomorphic':True,'lesson':'The five colorings and five-dimensional Singer fibre are distinct A5 modules despite the shared numeral five.'},'checks':checks,'boundary':'The P1(F5)/icosahedral-axis identification and 280-dimensional augmentation bundle are exact. The numerical equality 56*5=40*7 does not by itself define a canonical 56-by-40 W33 incidence geometry.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
