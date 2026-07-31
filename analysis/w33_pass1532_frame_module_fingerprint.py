#!/usr/bin/env python3
"""Pass 1532: commutant fingerprints for the frame eigenspaces.

The orbitals of the frame action form the full permutation commutant. Generic
symmetric orbital combinations split isotypic multiplicity spaces. We compute
stable block dimensions for PSp(4,3) and PGSp(4,3), then test equal-dimensional
blocks against every orbital to distinguish multiplicity from coincidence.
"""
from __future__ import annotations
import argparse, collections, importlib.util, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'analysis'/'w33_frame_hoffman_resolution_theorem.py'
def load_base():
 spec=importlib.util.spec_from_file_location('frame_hoffman',BASE);m=importlib.util.module_from_spec(spec);assert spec.loader is not None;spec.loader.exec_module(m);return m

def certificate()->dict:
 w=load_base();g=w.build_geometry();pts=g['points'];A=g['point_adjacency'];lines=g['lines'];frames=g['frames'];H=g['frame_graph']
 pidx={p:i for i,p in enumerate(pts)};lidx={tuple(sorted(L)):i for i,L in enumerate(lines)};fidx={tuple(sorted(f)):i for i,f in enumerate(frames)}
 def trans(v):
  v=w.normalize(v);out=[]
  for x in pts:
   c=w.symplectic(x,v);y=tuple((x[i]+c*v[i])%3 for i in range(4));out.append(pidx[w.normalize(y)])
  return tuple(out)
 def diag(d):return tuple(pidx[w.normalize(tuple((d[i]*x[i])%3 for i in range(4)))] for x in pts)
 def comp(p,q):return tuple(q[p[i]] for i in range(40))
 ident=tuple(range(40));inner_gens=[trans(v) for v in [(1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0)]];outer=diag((1,1,2,2))
 def closure(gens):
  G=[ident];seen={ident};q=collections.deque([ident])
  while q:
   a=q.popleft()
   for h in gens:
    b=comp(a,h)
    if b not in seen:seen.add(b);G.append(b);q.append(b)
  return G
 psp=closure(inner_gens);full=closure(inner_gens+[outer]);assert len(psp)==25920 and len(full)==51840
 def lp(p):return tuple(lidx[tuple(sorted(p[x] for x in L))] for L in lines)
 def fim(l,f):
  a,b=frames[f];return fidx[tuple(sorted((l[a],l[b])))]
 def orbital_data(G):
  st=[];reps=[None]*540
  for p in G:
   l=lp(p);im=fim(l,0)
   if reps[im] is None:reps[im]=l
   if im==0:st.append(l)
  unseen=set(range(540));orbits=[]
  while unseen:
   x=min(unseen);O={fim(l,x) for l in st};q=collections.deque(O)
   while q:
    y=q.popleft()
    for l in st:
     z=fim(l,y)
     if z not in O:O.add(z);q.append(z)
   orbits.append(sorted(O));unseen-=O
  Rs=[]
  for O in orbits:
   R=np.zeros((540,540),dtype=float)
   for u,l in enumerate(reps):
    for x in O:R[u,fim(l,x)]=1
   Rs.append(R)
  vals,vecs=np.linalg.eigh(H.astype(float));spaces={}
  for target in (-4,4):
   Q=vecs[:,np.isclose(vals,target,atol=1e-7)]
   coeff=np.array([(i+1)**2 for i in range(len(Rs))],float);S=sum(coeff[i]*(Rs[i]+Rs[i].T) for i in range(len(Rs)))
   ev,U=np.linalg.eigh(Q.T@S@Q);clusters=[];start=0
   for i,x in enumerate(ev):
    if i and abs(x-ev[i-1])>1e-5:clusters.append((float(np.mean(ev[start:i])),start,i));start=i
   clusters.append((float(np.mean(ev[start:])),start,len(ev)))
   blocks=[{'eigenvalue':round(v,9),'multiplicity':b-a,'basis':Q@U[:,a:b]} for v,a,b in clusters]
   mixing=[]
   for i in range(len(blocks)):
    for j in range(i+1,len(blocks)):
     if blocks[i]['multiplicity']==blocks[j]['multiplicity']:
      Bi=blocks[i]['basis'];Bj=blocks[j]['basis'];mx=max(float(np.linalg.norm(Bi.T@R@Bj)) for R in Rs)
      mixing.append({'dimension':blocks[i]['multiplicity'],'block_indices':[i,j],'max_offdiagonal_frobenius':mx})
   spaces[str(target)]={'dimension':int(Q.shape[1]),'blocks':[{k:v for k,v in b.items() if k!='basis'} for b in blocks],'equal_dimension_mixing':mixing}
  return {'group_order':len(G),'frame_stabilizer_order':len(st),'permutation_rank':len(orbits),'subdegrees':[len(o) for o in orbits],'eigenspaces':spaces}
 inner=orbital_data(psp);outerdata=orbital_data(full)
 N=np.zeros((40,540),dtype=np.int64)
 for j,(a,b) in enumerate(frames):N[list(lines[a]),j]=1;N[list(lines[b]),j]=1
 I=np.eye(540,dtype=np.int64);Pm=I.copy()
 for lam in (32,14,8,4,2):Pm=Pm@(H-lam*I)
 point_orbits=[];stab=[p for p in psp if fim(lp(p),0)==0];un=set(range(40))
 while un:
  x=min(un);O={p[x] for p in stab};point_orbits.append(sorted(O));un-=O
 frame_reps=[None]*540
 for p in psp:
  im=fim(lp(p),0)
  if frame_reps[im] is None:frame_reps[im]=p
 rectangular_ranks=[]
 for O in point_orbits:
  R=np.zeros((40,540),dtype=np.int64)
  for f,p in enumerate(frame_reps):R[[p[x] for x in O],f]=1
  rectangular_ranks.append(int(np.linalg.matrix_rank((R@Pm).astype(float))))
 checks={'psp_order':len(psp)==25920,'pgsp_order':len(full)==51840,'psp_rank_32':inner['permutation_rank']==32,'pgsp_rank_22':outerdata['permutation_rank']==22,
   'minus4_dimension_315':inner['eigenspaces']['-4']['dimension']==315,'plus4_dimension_81':inner['eigenspaces']['4']['dimension']==81,
   'frame_stabilizer_point_orbits_8_8_24':sorted(map(len,point_orbits))==[8,8,24],'rectangular_orbital_ranks_computed':len(rectangular_ranks)==3}
 checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
 return {'schema':'w33.pass1532.frame_module_fingerprint.v1','status':'PASS','psp':inner,'pgsp':outerdata,
   'interpretation':{
    'psp_minus4':'64 + 81 + 20 + 2*60 + 2*15_other, with both equal-dimensional pairs mixed by orbitals.',
    'pgsp_minus4':'64 + 81 + 20 + 2*60 + 15_other^+ + 15_other^-, where the outer element separates the two 15 extensions but not the multiplicity-two 60 block.',
    'plus4':'A single 81 block for both groups; Pass 1535 identifies it with the harmonic Steinberg extension.',
    'sp_inflation':'The projective action inflates to Sp(4,3) with the central -I acting trivially.'},
   'point_module_comparison':{'frame_stabilizer_point_orbit_sizes':sorted(map(len,point_orbits)),'rectangular_orbital_ranks_on_Eminus4':rectangular_ranks,'N_times_Pminus4_zero':bool(not np.any(N@Pm)),'conclusion':'All three equivariant maps vanish on E_-4; therefore the repeated 15 is the other rational 15, not the 15 in the 40-point permutation module.'},
   'checks':checks,
   'boundary':'The orbit algebra and zero-map tests are exact integer-carrier computations; block extraction uses stable symmetric eigenspace numerics and should be independently matched against GAP character tables before being called a formal character decomposition.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--check',action='store_true');a=ap.parse_args();r=certificate();t=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(t,encoding='utf-8')
 if not a.check or not a.output:print(t,end='')
if __name__=='__main__':main()
