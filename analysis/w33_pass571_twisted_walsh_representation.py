#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass568_572_q5_common import classes,cp,charpoly_prime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass571_twisted_walsh_representation.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)

def signed_actions():
 C=classes(5);idx={v:i for i,v in enumerate(C)};actions=set()
 for a,b,c,d in itertools.product(range(5),repeat=4):
  det=(a*d-b*c)%5
  if det not in (1,4):continue
  perm=[None]*12;flip=0;ok=True
  for i,v in enumerate(C):
   w=((a*v[0]+b*v[1])%5,(c*v[0]+d*v[1])%5);can=cp(w,5);j=idx[can];sgn=1 if w==can else 4
   if A[i]*A[i]%5!=A[j]*A[j]%5:ok=False;break
   ratio=sgn*A[i]*pow(A[j],-1,5)%5;perm[j]=i
   if ratio==4:flip|=1<<j
  if ok:actions.add((tuple(perm),flip))
 return tuple(sorted(actions))
G=signed_actions();I=next(g for g in G if g[0]==tuple(range(12)) and g[1]==0)
def apply(x,g):p,f=g;return sum(((x>>p[j])&1)<<j for j in range(12))^f
def compose(g,h):
 z=apply(apply(0,h),g);imgs=[apply(apply(1<<i,h),g)^z for i in range(12)];perm=[]
 for j in range(12):perm.append(next(i for i in range(12) if (imgs[i]>>j)&1))
 return (tuple(perm),z)
def dual(w,g):
 p,f=g;wp=sum(((w>>p[j])&1)<<j for j in range(12));phase=-1 if (wp&f).bit_count()%2 else 1
 return wp,phase

def group_tables():
 idx={g:i for i,g in enumerate(G)};mul=np.empty((40,40),dtype=np.int16)
 for i,g in enumerate(G):
  for j,h in enumerate(G):mul[i,j]=idx[compose(g,h)]
 iid=idx[I];invs=[]
 for i in range(40):invs.append(next(j for j in range(40) if mul[i,j]==iid and mul[j,i]==iid))
 def order_i(i):
  x=iid
  for n in range(1,100):
   x=int(mul[i,x])
   if x==iid:return n
  raise AssertionError
 unseen=set(range(40));cls=[]
 while unseen:
  i=next(iter(unseen));C={int(mul[mul[h,i],invs[h]]) for h in range(40)};unseen-=C;cls.append(sorted(C))
 cls.sort(key=lambda C:(0 if iid in C else 1,len(C),order_i(C[0]),C[0]))
 return idx,mul,invs,cls,order_i

def irreducible_characters(mul,invs,cls,order_i):
 r=len(cls);Ms=[]
 for Ai in cls:
  M=np.zeros((r,r),dtype=float)
  for bj,Bj in enumerate(cls):
   cnt=Counter(int(mul[x,y]) for x in Ai for y in Bj)
   for ck,Ck in enumerate(cls):
    vals={cnt[z] for z in Ck};assert len(vals)==1;M[ck,bj]=next(iter(vals))
  Ms.append(M)
 combo=sum((np.sqrt(i+2)+np.pi/(i+3))*M for i,M in enumerate(Ms))
 vals,V=np.linalg.eig(combo);chars=[]
 for col in range(r):
  v=V[:,col];den=np.vdot(v,v);lams=np.array([np.vdot(v,M@v)/den for M in Ms])
  d=np.sqrt(40/sum(abs(lams[i])**2/len(cls[i]) for i in range(r)))
  chi=np.array([d*lams[i]/len(cls[i]) for i in range(r)])
  chars.append((int(round(d)),chi))
 chars.sort(key=lambda x:(x[0],tuple(np.round(x[1].real,6)),tuple(np.round(x[1].imag,6))))
 return chars

def decompose_character(psi,chars,cls):
 out=[]
 for d,chi in chars:
  m=sum(len(cls[i])*psi[i]*np.conj(chi[i]) for i in range(len(cls)))/40
  assert abs(m.imag)<1e-6 and abs(m.real-round(m.real))<1e-6
  out.append(int(round(m.real)))
 return tuple(out)

def frequency_orbits():
 unseen=set(range(4096));orbits=[]
 while unseen:
  w0=min(unseen);O={w0};q=deque([w0])
  while q:
   w=q.popleft()
   for g in G:
    u,_=dual(w,g)
    if u not in O:O.add(u);q.append(u)
  unseen-=O;orbits.append(tuple(sorted(O)))
 return tuple(orbits)

def fwht(a):
 a=list(a);h=1
 while h<len(a):
  for i in range(0,len(a),2*h):
   for j in range(i,i+h):x,y=a[j],a[j+h];a[j],a[j+h]=x+y,x-y
  h*=2
 return a

def fibres():
 F=defaultdict(set)
 for m in range(4096):
  offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A));F[tuple(charpoly_prime(5,offs)[0])].add(m)
 return [frozenset(S) for _,S in sorted(F.items(),key=lambda kv:json.dumps(kv[0],separators=(',',':')))]

def payload():
 idx,mul,invs,cls,order_i=group_tables();chars=irreducible_characters(mul,invs,cls,order_i);degrees=[d for d,_ in chars]
 class_rows=[{'size':len(C),'element_order':order_i(C[0])} for C in cls]
 fullchar=[]
 for C in cls:
  g=G[C[0]];fullchar.append(sum(s for w in range(4096) for u,s in [dual(w,g)] if u==w))
 fullmult=decompose_character(fullchar,chars,cls)
 orbits=frequency_orbits();orbit_mult=[]
 for O in orbits:
  psi=[]
  for C in cls:
   g=G[C[0]];psi.append(sum(s for w in O for u,s in [dual(w,g)] if u==w))
  m=decompose_character(psi,chars,cls)
  assert sum(d*x for d,x in zip(degrees,m))==len(O);orbit_mult.append(m)
 rows=fibres();signatures=[]
 for S in rows:
  W=fwht([1 if x in S else 0 for x in range(4096)])
  active=[i for i,O in enumerate(orbits) if any(W[w]!=0 for w in O)]
  mult=tuple(sum(orbit_mult[i][j] for i in active) for j in range(len(chars)))
  signatures.append((len(S),len(active),sum(c!=0 for c in W),mult))
 sc=Counter(signatures)
 sigrows=[]
 for s,n in sorted(sc.items(),key=lambda kv:(kv[0][0],kv[0][1],kv[0][2],kv[0][3])):
  sigrows.append({'fibre_count':n,'fibre_size':s[0],'active_twisted_orbits':s[1],'nonzero_walsh_coefficients':s[2],'irreducible_multiplicities':s[3]})
 orbit_type_counts=Counter(orbit_mult)
 checks={
  'signed_group_order40':len(G)==40,
  'conjugacy_classes16':len(cls)==16,
  'irreducible_degrees_eight1_eight2':Counter(degrees)==Counter({1:8,2:8}),
  'sum_degree_squares40':sum(d*d for d in degrees)==40,
  'full_representation_dimension4096':sum(d*m for d,m in zip(degrees,fullmult))==4096,
  'full_rep_multiplicities_104_204':fullmult==(104,)*8+(204,)*8,
  'frequency_orbits292':len(orbits)==292,
  'orbit_modules_have15_decomposition_types':len(orbit_type_counts)==15,
  'exact_98_fibres':len(rows)==98,
  'six_formula_signatures':len(sc)==6,
  'formula_signature_counts_partition98':sum(sc.values())==98,
 }
 return {
  'schema':'w33.pass571.twisted_walsh_representation.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'group':{'order':40,'conjugacy_classes':class_rows,'irreducible_degrees':degrees,'identification_data':{'center_order':4,'derived_order':5,'abelianization_order':8}},
  'signed_walsh_representation':{'dimension':4096,'character_on_classes':fullchar,'irreducible_multiplicities':fullmult,'decomposition':'Each of the eight one-dimensional irreducibles occurs 104 times; each of the eight two-dimensional irreducibles occurs 204 times.'},
  'frequency_orbit_modules':{'orbits':len(orbits),'orbit_size_histogram':dict(sorted(Counter(map(len,orbits)).items())),'decomposition_type_count':len(orbit_type_counts),'decomposition_type_census':{str(k):v for k,v in sorted(orbit_type_counts.items(),key=str)}},
  'formula_signatures':sigrows,
  'conclusion':'The six Pass-566 formula signatures are exactly six sums of induced twisted-frequency orbit modules. Their multiplicity vectors in the 8 one-dimensional and 8 two-dimensional irreducibles replace digest-only classification by character-theoretic data.',
  'checks':checks,
  'boundary':'The decomposition is exact for the signed order-40 fixed-magnitude stabilizer and its 4096-dimensional Walsh representation. Numeric diagonalization is used only to recover the finite character table; every reported multiplicity is integer-checked by character orthogonality and dimension reconstruction.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 571 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'signatures':len(p['formula_signatures'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
