#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,multiprocessing as mp
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass543_547_common import Cyc9,classes,cp,mat_sub,traces,charpoly_from_traces

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass564_z9_full_quadratic_irreducibles.json'
C=Cyc9();A9,A3=classes(9),classes(3);BIDX={b:i for i,b in enumerate(A3)}
ALPHAS=((1,0),(0,1),(1,1),(1,2))

def oriented(v):
 r=(v[0]%3,v[1]%3);q=cp(r,3)
 return v if r==q else ((-v[0])%9,(-v[1])%9)
def reduction_meta(v):
 if v[0]%3 or v[1]%3:
  w=oriented(v);b=(w[0]%3,w[1]%3);u=((w[0]-b[0])//3%3,(w[1]-b[1])//3%3);return b,u,True
 w=(v[0]//3%3,v[1]//3%3);return cp(w,3),(0,0),False
META=[reduction_meta(v) for v in A9]

def pair_deltas():
 out=[];E=range(9)
 for a,b in A9:
  vals=[]
  for c in (0,3,6):
   M=[[C.zero() for _ in E] for _ in E]
   for aa,bb,cc in ((a,b,c),((-a)%9,(-b)%9,(-c)%9)):
    for x in E:
     z=(cc+2*x*bb+aa*bb)%9;j=(x+aa)%9
     M[j][x]=C.add(M[j][x],C.from_exp(z))
   vals.append(M)
  out.append([mat_sub(vals[i],vals[0],C) for i in range(3)])
 return out
PD=pair_deltas();Z=C.zero();CP_CACHE={}

def cp_from_trits(vals):
 vals=tuple(vals);neg=tuple((-x)%3 for x in vals);key=min(vals,neg)
 if key in CP_CACHE:return CP_CACHE[key]
 D=[[Z for _ in range(9)] for _ in range(9)]
 for i,v in enumerate(vals):
  if v:
   M=PD[i][v]
   for r in range(9):
    for s in range(9):D[r][s]=C.add(D[r][s],M[r][s])
 out=tuple(charpoly_from_traces(traces(D,9,C),C));CP_CACHE[key]=out;return out

def section(constants,qvec):
 out=[]
 for b,u,primitive in META:
  if not primitive:out.append(0);continue
  i=BIDX[b];ell=(ALPHAS[i][0]*u[0]+ALPHAS[i][1]*u[1])%3
  out.append((constants[i]+qvec[i]*ell*ell)%3)
 return tuple(out)

def addv(a,b):return tuple((x+y)%3 for x,y in zip(a,b))
def smul(k,a):return tuple(k*x%3 for x in a)
def span(gens):
 s={(0,0,0,0)}
 for g in gens:s|={addv(x,smul(k,g)) for x in tuple(s) for k in range(3)}
 return frozenset(s)
def rank(gens):
 A=[list(x) for x in gens];r=0
 for c in range(4):
  p=next((i for i in range(r,len(A)) if A[i][c]%3),None)
  if p is None:continue
  A[r],A[p]=A[p],A[r];iv=pow(A[r][c]%3,-1,3);A[r]=[iv*x%3 for x in A[r]]
  for i in range(len(A)):
   if i!=r and A[i][c]%3:
    q=A[i][c]%3;A[i]=[(x-q*y)%3 for x,y in zip(A[i],A[r])]
  r+=1
 return r
def permute(v,p):return tuple(v[p[i]] for i in range(4))
S4=tuple(itertools.permutations(range(4)))

def transition(prev,cur):
 signatures=defaultdict(set);children=defaultdict(list)
 for p,x in cur.items():children[p[:-1]].append(x)
 for par,ch in children.items():signatures[prev[par]].add(tuple(sorted(Counter(ch).items(),key=str)))
 return {'parent_charpolys':len(set(prev.values())),'child_charpolys':len(set(cur.values())),'spectral_markov':all(len(v)==1 for v in signatures.values()),'ambiguous_parent_spectra':sum(len(v)>1 for v in signatures.values())}

PACKET_BASIS=((1,1,1,1),(1,2,0,0),(0,1,2,0),(0,0,1,2))
def _cp_param_worker(params):
 constants=params[:4];q=(0,0,0,0)
 for a,b in zip(params[4:],PACKET_BASIS):q=addv(q,smul(a,b))
 return cp_from_trits(section(constants,q))

def payload():
 one=(1,1,1,1);aug_basis=((1,2,0,0),(0,1,2,0),(0,0,1,2));aug=span(aug_basis);const=span((one,))
 orbit_span_dims=[]
 for v in aug:
  if v!=(0,0,0,0):orbit_span_dims.append(rank(tuple(permute(v,p) for p in S4)))
 augmentation_irreducible=all(d==3 for d in orbit_span_dims)
 packet_basis=(one,)+aug_basis
 full_params=list(itertools.product(range(3),repeat=8))
 def canon_param(p):
  n=tuple((-x)%3 for x in p);return min(p,n)
 reps=sorted({canon_param(p) for p in full_params})
 with mp.Pool(processes=8) as pool:
  vals=pool.map(_cp_param_worker,reps,chunksize=16)
 cpmap=dict(zip(reps,vals))
 rows=[]
 for k in range(5):
  row={}
  for params in itertools.product(range(3),repeat=4+k):
   full=params+(0,)*(4-k)
   row[params]=cpmap[canon_param(full)]
  rows.append(row)
 layers=[]
 for k,r in enumerate(rows):
  c=Counter(r.values());layers.append({'active_quadratic_packets':k,'sections':len(r),'distinct_charpolys':len(c),'multiplicity_histogram':dict(sorted(Counter(c.values()).items()))})
 trans=[transition(rows[k-1],rows[k]) for k in range(1,5)]
 qvecs=list(itertools.product(range(3),repeat=4));seen=set();orbits=[]
 for q in qvecs:
  if q in seen:continue
  O={permute(q,p) for p in S4}|{smul(2,permute(q,p)) for p in S4}
  seen|=O;orbits.append(O)
 checks={
  'four_fibres_nine_primitive_lifts':all(sum(1 for b,_,p in META if p and b==base)==9 for base in A3),
  'quadratic_coefficient_module_dimension4':rank(packet_basis)==4,
  'permutation_module_splits_trivial_plus_augmentation':len(const)==3 and len(aug)==27 and const&aug=={(0,0,0,0)} and len({addv(x,y) for x in const for y in aug})==81,
  'augmentation_dimension3':rank(aug_basis)==3,
  'augmentation_irreducible_over_F3':augmentation_irreducible,
  'layer_sizes_exact':[x['sections'] for x in layers]==[81,243,729,2187,6561],
  'full_quadratic_slice_F3_power8':layers[-1]['sections']==3**8,
  'all_layers_nontrivial_image_growth':all(layers[i]['distinct_charpolys']<layers[i+1]['distinct_charpolys'] for i in range(4)),
  'full_module_contains_common_packet_face':all(rows[1][p]==rows[-1][p+(0,0,0)] for p in rows[1]),
  'projective_S4_orbit_partition':sum(len(o) for o in orbits)==81 and len(set().union(*orbits))==81,
 }
 return {
  'schema':'w33.pass564.z9_full_quadratic_irreducibles.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'module':{'coefficient_space':'F3^4 on the four primitive Hjelmslev fibres','decomposition':'1 + 3 under PGL(2,3) ~= S4','trivial_packet':one,'augmentation_basis':aug_basis,'augmentation_irreducible':augmentation_irreducible,'projective_orbit_count':len(orbits),'projective_orbit_sizes':sorted(len(o) for o in orbits)},
  'family':{'definition':'f_b(u)=c_b+q_b ell_b(u)^2 with c,q in F3^4; deep anchors are zero. The first quadratic packet is the common diagonal q_b=q, and the remaining three packets span the irreducible augmentation module sum q_b=0.','parameter_space':'F3^8','section_count':3**8},
  'layers':layers,'transfers':trans,
  'conclusion':'The common quadratic packet of Pass 559 is exactly the trivial summand of the four-fibre quadratic coefficient module. The remaining modes form one irreducible 3-dimensional S4 module and produce the exact final image recorded here.',
  'checks':checks,
  'boundary':'Exact for the full homogeneous-square coefficient module on the four primitive fibres with arbitrary fibre constants. Cross-products between different Hjelmslev fibres and the full 9^40 section space are not included.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 564 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'image':p['layers'][-1]['distinct_charpolys']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
