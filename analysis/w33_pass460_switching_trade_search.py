#!/usr/bin/env python3
"""Pass 460: search for switching/trade mechanisms behind the genuine q=5 collision."""
from __future__ import annotations
import argparse,json,itertools
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass460_switching_trade_search.json'
Q=5
LEFT=(0,3,4,1,1,0,2,0,1,1,2,2)
RIGHT=(0,2,3,0,2,2,4,1,0,3,3,2)

def setup():
 q=Q;elems=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)];idx={g:i for i,g in enumerate(elems)}
 vecs=[(a,b) for a in range(q) for b in range(q) if (a,b)!=(0,0)];pairs=[];used=set()
 for v in vecs:
  nv=(-v[0]%q,-v[1]%q);key=tuple(sorted((v,nv)))
  if key not in used:used.add(key);pairs.append(key)
 def mul(g,h):return ((g[0]+h[0])%q,(g[1]+h[1])%q,(g[2]+h[2]-g[0]*h[1]+h[0]*g[1])%q)
 def graph(offs):
  S=[]
  for (v,nv),c in zip(pairs,offs):S += [(v[0],v[1],c),(nv[0],nv[1],-c%q)]
  A=np.zeros((125,125),dtype=np.int8)
  for i,g in enumerate(elems):
   for s in S:A[i,idx[mul(g,s)]]=1
  return A
 ab=[(a,b) for a in range(q) for b in range(q)];abidx={v:i for i,v in enumerate(ab)};omega=np.exp(2j*np.pi/q)
 def blocks(offs):
  f={}
  for (v,nv),c in zip(pairs,offs):f[v]=c;f[nv]=-c%q
  out=[]
  for t in range(1,q):
   M=np.zeros((q*q,q*q),complex)
   for i,(a,b) in enumerate(ab):
    for (x,y),z in f.items():M[i,abidx[((a+x)%q,(b+y)%q)]]=omega**((t*(z-a*y+x*b))%q)
   out.append(M)
  return out
 def spec_key(offs):
  vals=[]
  for B in blocks(offs):vals.extend(np.linalg.eigvalsh(B))
  return tuple(np.round(sorted(vals),7))
 return elems,idx,pairs,graph,spec_key

def gm_switch(A,X):
 X=sorted(X);n=len(A);Xs=set(X);Y=[i for i in range(n) if i not in Xs];m=len(X)
 if m%2:return None
 degX=A[np.ix_(X,X)].sum(1)
 if len(set(map(int,degX)))!=1:return None
 cnt=A[np.ix_(Y,X)].sum(1)
 if not set(map(int,cnt)).issubset({0,m//2,m}):return None
 B=A.copy()
 for row,y in enumerate(Y):
  if int(cnt[row])==m//2:
   B[y,X]=1-B[y,X];B[X,y]=B[y,X]
 return B

def seidel_switch(A,X):
 X=sorted(X);Xs=set(X);Y=[i for i in range(len(A)) if i not in Xs];B=A.copy();B[np.ix_(X,Y)]=1-B[np.ix_(X,Y)];B[np.ix_(Y,X)]=B[np.ix_(X,Y)].T;return B

def fibonacci_word(n):
 s='1'
 while len(s)<n:s=''.join('10' if c=='1' else '1' for c in s)
 return s[:n]

def candidate_vertex_sets(elems,idx):
 q=Q;cands=[]
 fibers={(a,b):{idx[(a,b,c)] for c in range(q)} for a in range(q) for b in range(q)}
 for u,v in itertools.combinations(fibers,2):cands.append(('two_fibers',tuple(sorted(fibers[u]|fibers[v]))))
 lines=[];seen=set()
 for v in [(a,b) for a in range(q) for b in range(q) if (a,b)!=(0,0)]:
  L=frozenset(((t*v[0])%q,(t*v[1])%q) for t in range(q))
  if L not in seen:seen.add(L);lines.append(L)
 for li,L in enumerate(lines):
  remaining=set(fibers);cosets=[]
  while remaining:
   u=min(remaining);C=frozenset(((u[0]+x[0])%q,(u[1]+x[1])%q) for x in L);remaining-=set(C);cosets.append(C)
  for i,j in itertools.combinations(range(5),2):
   X=set()
   for u in cosets[i]|cosets[j]:X|=fibers[u]
   cands.append((f'abelian_coset_pair_L{li}',tuple(sorted(X))))
 for c,d in itertools.combinations(range(q),2):cands.append(('central_slices',tuple(sorted(idx[g] for g in elems if g[2] in (c,d)))))
 w=fibonacci_word(25)
 points=sorted(fibers)
 for sh in range(25):
  bits=w[sh:]+w[:sh]
  for symbol,name in [('0','fibonacci_zero_fibers'),('1','fibonacci_one_fibers')]:
   sel=[points[i] for i,b in enumerate(bits) if b==symbol]
   X=set()
   for u in sel:X|=fibers[u]
   cands.append((name,tuple(sorted(X))))
 out=[];seenX=set()
 for kind,X in cands:
  if X not in seenX:seenX.add(X);out.append((kind,X))
 return out

def build_payload():
 elems,idx,pairs,graph,spec_key=setup();A0=graph(LEFT);A1=graph(RIGHT);target=spec_key(RIGHT)
 delta=tuple((b-a)%Q for a,b in zip(LEFT,RIGHT));support=[i for i,d in enumerate(delta) if d]
 cospectral=[]
 for mask in range(1<<len(support)):
  offs=list(LEFT)
  for j,pos in enumerate(support):
   if mask>>j&1:offs[pos]=(offs[pos]+delta[pos])%Q
  if spec_key(tuple(offs))==target:cospectral.append({'mask':mask,'weight':mask.bit_count(),'offsets':offs})
 mind=min(((a['mask']^b['mask']).bit_count() for i,a in enumerate(cospectral) for b in cospectral[i+1:]),default=None)
 profile=Counter(x['weight'] for x in cospectral)
 candidates=candidate_vertex_sets(elems,idx);gm_valid=0;gm_spectral=0;gm_iso=[];seidel_regular=0;seidel_spectral=0;seidel_iso=[];kind_counts=Counter(k for k,_ in candidates)
 G1=nx.from_numpy_array(A1)
 for kind,X in candidates:
  B=gm_switch(A0,X)
  if B is not None:
   gm_valid+=1
   if np.allclose(np.linalg.eigvalsh(B.astype(float)),np.linalg.eigvalsh(A1.astype(float)),atol=1e-7):
    gm_spectral+=1
    if nx.is_isomorphic(nx.from_numpy_array(B),G1):gm_iso.append({'kind':kind,'size':len(X)})
  S=seidel_switch(A0,X)
  if len(set(map(int,S.sum(1))))==1:
   seidel_regular+=1
   if np.allclose(np.linalg.eigvalsh(S.astype(float)),np.linalg.eigvalsh(A1.astype(float)),atol=1e-7):
    seidel_spectral+=1
    if nx.is_isomorphic(nx.from_numpy_array(S),G1):seidel_iso.append({'kind':kind,'size':len(X)})
 x=sp.symbols('x')
 nonlinear=sp.Poly(x**10-120*x**8-15*x**7+4220*x**6+792*x**5-37925*x**4+4955*x**3+96910*x**2-39730*x-209,x)
 golden_gcd_hits=[]
 for n in range(3,501):
  g=sp.gcd(nonlinear,sp.Poly(x**4-(n-2)*x**2+1,x))
  if g.degree()>0:golden_gcd_hits.append({'n':n,'gcd':str(g.as_expr())})
 golden_audit={
  'collision_factor_degree':nonlinear.degree(),
  'collision_factor_irreducible_over_Q':bool(nonlinear.is_irreducible),
  'collision_factor_reciprocal':nonlinear.all_coeffs()==list(reversed(nonlinear.all_coeffs())),
  'golden_quartic_family_range':'x^4-(n-2)x^2+1, 3<=n<=500',
  'nontrivial_gcd_hits':golden_gcd_hits,
 }
 checks={
  'delta_support_ten':len(support)==10,
  'all_1024_phase_subtrades_searched':2**len(support)==1024,
  'source_and_target_are_only_phase_subtrade_hits':len(cospectral)==2 and sorted(x['weight'] for x in cospectral)==[0,10],
  'no_local_quartet_trade':not any(x['weight']==4 for x in cospectral),
  'natural_switching_families_exhausted':len(candidates)>=400,
  'no_natural_GM_switch_to_target':not gm_iso,
  'no_natural_Seidel_switch_to_target':not seidel_iso,
  'golden_quartic_family_does_not_factor_collision':bool(nonlinear.is_irreducible) and not golden_gcd_hits and not golden_audit['collision_factor_reciprocal'],
 }
 return {
  'schema':'w33.pass460.switching_trade_search.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'offset_delta':list(delta),'changed_direction_indices':support,'phase_subtrade_hits':cospectral,
  'minimum_hamming_distance_between_hits':mind,'hit_weight_profile':{str(k):v for k,v in sorted(profile.items())},
  'candidate_vertex_sets':len(candidates),'candidate_kind_counts':dict(kind_counts),
  'godsil_mckay':{'valid_switching_sets':gm_valid,'cospectral_with_target':gm_spectral,'isomorphic_to_target':gm_iso},
  'seidel':{'regular_outputs':seidel_regular,'cospectral_with_target':seidel_spectral,'isomorphic_to_target':seidel_iso},
  'golden_quartic_audit':golden_audit,
  'headline':'The collision is a global ten-direction phase trade: among all 2^10 partial applications of its exact offset difference, only the two endpoints are cospectral. No natural central-fiber, maximal-abelian-coset, central-slice, or Fibonacci/Beatty-mask Godsil-McKay or Seidel switch generates the target.',
  'document_connection':'The Fibonacci-word upload motivated the aperiodic fiber masks, and the fifth-root spin-foam upload motivated a four-leg F-move search. Both mechanisms are falsified in these natural forms: there is no weight-4 phase trade and no tested Fibonacci-mask switching set reaching the collision.',
  'boundary':'This is an exhaustive search inside the exact ten-coordinate phase cube and the listed natural vertex-set families, not a proof that no switching description exists in any enlarged coherent configuration.',
  'checks':checks,
 }
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 460 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'phase_hits':len(p['phase_subtrade_hits']),'candidates':p['candidate_vertex_sets'],'gm':p['godsil_mckay'],'seidel':p['seidel']}))
 return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
