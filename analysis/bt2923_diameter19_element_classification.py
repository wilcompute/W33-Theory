#!/usr/bin/env python3
"""Pass 2923: algebraic census of the 188 directed-diameter-19 ISA elements."""
from __future__ import annotations
import json
from collections import Counter, deque
from itertools import product
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT2923_DIAMETER19_ELEMENT_CLASSIFICATION_results.json'
LIN={
 'F_p':((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)),
 'CX_pf':((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1)),
 'CX_fp':((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,2,0,1)),
 'Z_p':((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)),}
TRANS={'F_p':(0,0,0,0),'CX_pf':(0,0,0,0),'CX_fp':(0,0,0,0),'Z_p':(0,1,0,0)}
IDENT=tuple(tuple(1 if i==j else 0 for j in range(4)) for i in range(4));ZERO=(0,0,0,0)
NAMES=('F_p','CX_pf','CX_fp','Z_p')

def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(4))%3 for j in range(4)) for i in range(4))
def mv(a,v):return tuple(sum(a[i][k]*v[k] for k in range(4))%3 for i in range(4))
def add(a,b):return tuple((x+y)%3 for x,y in zip(a,b))
def neg(a):return tuple((-x)%3 for x in a)
def enumerate_sp():
 order=[IDENT];idx={IDENT:0};q=deque([IDENT]);for_mats=[LIN['F_p'],LIN['CX_pf'],LIN['CX_fp']]
 while q:
  m=q.popleft()
  for g in for_mats:
   p=mul(g,m)
   if p not in idx:idx[p]=len(order);order.append(p);q.append(p)
 assert len(order)==51840
 return order,idx

def matrix_order(m,maxn=200):
 p=IDENT
 for n in range(1,maxn+1):
  p=mul(m,p)
  if p==IDENT:return n
 raise AssertionError('matrix order bound')
def affine_order(m,t,maxn=500):
 A=IDENT;a=ZERO
 for n in range(1,maxn+1):
  A,a=mul(m,A),add(mv(m,a),t)
  if A==IDENT and a==ZERO:return n
 raise AssertionError('affine order bound')
def fixed_count(m,t,states):return sum(add(mv(m,x),t)==x for x in states)
def charpoly_mod3(m):
 x=sp.Symbol('x');coeff=sp.Matrix(m).charpoly(x).all_coeffs();return tuple(int(c)%3 for c in coeff)
def inv_matrix(m):
 o=matrix_order(m);p=IDENT
 for _ in range(o-1):p=mul(m,p)
 assert mul(m,p)==IDENT
 return p

def main():
 sp_list,sp_index=enumerate_sp();states=list(product(range(3),repeat=4));t_index={t:i for i,t in enumerate(states)}
 NT=81;N=len(sp_list)*NT;sp_perm={};t_map={}
 for name in NAMES:
  A,a=LIN[name],TRANS[name]
  sp_perm[name]=np.array([sp_index[mul(A,M)] for M in sp_list],dtype=np.int32)
  t_map[name]=np.array([t_index[add(mv(A,t),a)] for t in states],dtype=np.int16)
 depth=np.full(N,255,dtype=np.uint8);start=sp_index[IDENT]*NT+t_index[ZERO];depth[start]=0
 frontier=np.array([start],dtype=np.int64);profile=[1];d=0
 while frontier.size:
  d+=1;candidates=[]
  for name in NAMES:
   s=sp_perm[name][frontier//NT];tt=t_map[name][frontier%NT];candidates.append(s.astype(np.int64)*NT+tt)
  cand=np.unique(np.concatenate(candidates));cand=cand[depth[cand]==255]
  if cand.size==0:d-=1;break
  depth[cand]=d;profile.append(int(cand.size));frontier=cand
 assert d==19 and int((depth==19).sum())==188 and int((depth!=255).sum())==N
 shell=np.flatnonzero(depth==19);records=[]
 for element in shell:
  mi,ti=divmod(int(element),NT);m=sp_list[mi];t=states[ti]
  mo=matrix_order(m);ao=affine_order(m,t);fc=fixed_count(m,t,states);cp=charpoly_mod3(m)
  invm=inv_matrix(m);invt=neg(mv(invm,t));inv_id=sp_index[invm]*NT+t_index[invt]
  records.append({'element_index':int(element),'matrix_index':mi,'translation':list(t),'translation_weight':sum(x!=0 for x in t),
       'trace_mod3':sum(m[i][i] for i in range(4))%3,'charpoly_mod3':list(cp),'matrix_order':mo,'affine_order':ao,
       'fixed_frame_count':fc,'inverse_directed_depth':int(depth[inv_id]),'linear_part':[list(row) for row in m]})
 def hist(field):return {str(k):v for k,v in sorted(Counter(r[field] for r in records).items(),key=lambda kv:str(kv[0]))}
 cp_hist={}
 for r in records:
  key=''.join(map(str,r['charpoly_mod3']));cp_hist[key]=cp_hist.get(key,0)+1
 profiles=Counter((r['affine_order'],r['matrix_order'],tuple(r['charpoly_mod3']),r['fixed_frame_count'],r['translation_weight']) for r in records)
 checks={'group_order_4199040':N==4199040,'diameter_19':d==19,'hardest_count_188':len(records)==188,
         'all_orders_finite':all(r['affine_order']>0 for r in records),'profile_partition':sum(profiles.values())==188}
 assert all(checks.values())
 out={'schema':'w33.pass2923.diameter19_element_classification.v1','status':'COMPLETE_EXACT','check_count':len(checks),'checks':checks,
      'shell_size':188,'ball_new_counts':profile,
      'histograms':{'affine_order':hist('affine_order'),'matrix_order':hist('matrix_order'),'fixed_frame_count':hist('fixed_frame_count'),
        'translation_weight':hist('translation_weight'),'trace_mod3':hist('trace_mod3'),'inverse_directed_depth':hist('inverse_directed_depth'),'charpoly_mod3':cp_hist},
      'algebraic_profile_count':len(profiles),
      'algebraic_profiles':[{'affine_order':k[0],'matrix_order':k[1],'charpoly_mod3':list(k[2]),'fixed_frame_count':k[3],
          'translation_weight':k[4],'multiplicity':v} for k,v in sorted(profiles.items())],
      'records':records,
      'headline':'The 188 hardest compiler transformations are classified by exact affine order, linear characteristic polynomial, fixed-frame count, translation weight, and inverse depth.',
      'claim_boundary':'This is an algebraic census of the directed-diameter shell, not yet a proof that each profile is a conjugacy class.'}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print('PASS',checks);print('affine orders',out['histograms']['affine_order']);print('fixed frames',out['histograms']['fixed_frame_count'])
 print('inverse depths',out['histograms']['inverse_directed_depth']);print('profiles',len(profiles))
if __name__=='__main__':main()
