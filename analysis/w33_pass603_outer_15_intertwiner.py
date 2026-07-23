#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass603_outer_15_intertwiner.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def perm_matrix(p):
 M=sp.zeros(len(p))
 for i,j in enumerate(p):M[j,i]=1
 return M

def payload():
 X=range(6);duads=tuple(itertools.combinations(X,2));did={frozenset(d):i for i,d in enumerate(duads)}
 synthemes=[]
 for P in itertools.combinations(duads,3):
  if len(set().union(*map(set,P)))==6:synthemes.append(frozenset(did[frozenset(d)] for d in P))
 synthemes=tuple(sorted(set(synthemes),key=lambda s:tuple(sorted(s))))
 totals=[]
 for C in itertools.combinations(range(15),5):
  if sorted(d for s in C for d in synthemes[s])==list(range(15)):totals.append(frozenset(C))
 totals=tuple(totals);tid={T:i for i,T in enumerate(totals)}
 M=sp.zeros(15)
 for s,S in enumerate(synthemes):
  for d in S:M[d,s]=1
 B=sp.zeros(6,15)
 for d,(a,b) in enumerate(duads):B[a,d]=B[b,d]=1
 T=sp.zeros(6,15)
 for i,U in enumerate(totals):
  for s in U:T[i,s]=1
 J=sp.ones(15);P1=J/15;C=B-sp.ones(6,15)/3;Q=C.T*(C*C.T).pinv()*C;P9=sp.eye(15)-P1-Q
 D=T-sp.ones(6,15)/3;Qout=D.T*(D*D.T).pinv()*D;P9out=sp.eye(15)-P1-Qout
 syn_to_outer=[]
 for s in range(15):syn_to_outer.append(did[frozenset(i for i,U in enumerate(totals) if s in U)])
 def act_syntheme(g,s):
  image=frozenset(did[frozenset((g[duads[d][0]],g[duads[d][1]]))] for d in synthemes[s]);return synthemes.index(image)
 def outer(g):return tuple(tid[frozenset(act_syntheme(g,s) for s in U)] for U in totals)
 def act_duad(g,d):
  a,b=duads[d];return did[frozenset((g[a],g[b]))]
 gens=[trans(6,i,i+1) for i in range(5)];outer_weld=True;intertwines=True
 for g in gens:
  ds=tuple(act_duad(g,d) for d in range(15));ss=tuple(act_syntheme(g,s) for s in range(15));og=outer(g);od=tuple(act_duad(og,d) for d in range(15))
  outer_weld &= all(syn_to_outer[ss[s]]==od[syn_to_outer[s]] for s in range(15));intertwines &= perm_matrix(ds)*M==M*perm_matrix(ss)
 checks={
  'duads_synthemes_15_totals6':len(duads)==15 and len(synthemes)==15 and len(totals)==6,
  'syntheme_is_outer_duad_bijection':sorted(syn_to_outer)==list(range(15)),
  'outer_twist_weld_on_generators':outer_weld,
  'incidence_intertwines_on_generators':intertwines,
  'projector_dimensions_1_5_9':P1.rank()==1 and Q.rank()==5 and P9.rank()==9,
  'outer_projector_dimensions_1_5prime_9':P1.rank()==1 and Qout.rank()==5 and P9out.rank()==9,
  'incidence_rank10':M.rank()==10,
  'five_packet_is_kernel':M.T*Q==sp.zeros(15),
  'one_and_nine_packets_intertwine':M.T*P1==P1*M.T and M.T*P9==P9out*M.T,
  'singular_square_identity':M*M.T==9*P1+4*P9 and M.T*M==9*P1+4*P9out,
 }
 return {'schema':'w33.pass603.outer_15_intertwiner.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'objects':{'duads':15,'synthemes':15,'synthematic_totals':6,'syntheme_to_outer_duad':syn_to_outer},
  'decomposition':{'natural_duad_module':'1 + 5 + 9','outer_twisted_duad_module':'1 + 5-prime + 9','projector_ranks':{'trivial':1,'natural_five':5,'common_nine':9,'outer_five_prime':5},'incidence_rank':M.rank()},
  'intertwiner':{'matrix':'15x15 duad-syntheme incidence matrix','kernel':'natural 5-dimensional point packet','image':'outer trivial plus outer 9-dimensional packet','MMt':'9 P1 + 4 P9','MtM':'9 P1 + 4 P9_outer','singular_values':'3 on the singlet, 2 on the common nine, 0 on the natural five'},
  'theorem':'The S6 outer automorphism transforms the canonical duad decomposition 15=1+5+9 into 15=1+5-prime+9. The duad-syntheme incidence matrix is an exact rank-10 intertwiner fixing the 1+9 sector while annihilating the natural 5.',
  'checks':checks,'boundary':'There is a second canonical packet basis, but no canonical invertible 15-dimensional intertwiner: the outer automorphism exchanges inequivalent five-dimensional sectors. The exact common bridge has rank ten.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 603 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'rank':p['decomposition']['incidence_rank']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
