#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,defaultdict,deque
from fractions import Fraction as F
from pathlib import Path
from w33_pass571_twisted_walsh_representation import G,I,compose,dual,apply,A
from w33_pass568_572_q5_common import charpoly_prime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass576_exact_walsh_central_idempotents.json'

# Q(sqrt(5),i), basis 1,s,i,is with s^2=5 and i^2=-1.
def K(a=0,b=0,c=0,d=0):return (F(a),F(b),F(c),F(d))
ZERO=K();ONE=K(1);II=K(0,0,1);SQ=K(0,1)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def scale(q,x):return tuple(F(q)*a for a in x)
def mul(x,y):
 a,b,c,d=x;e,f,g,h=y
 re0=a*e+5*b*f-c*g-5*d*h
 re1=a*f+b*e-c*h-d*g
 im0=a*g+5*b*h+c*e+5*d*f
 im1=a*h+b*g+c*f+d*e
 return (re0,re1,im0,im1)
def conj(x):a,b,c,d=x;return (a,b,-c,-d)
def eq0(x):return x==ZERO
def fmtq(q):return str(q.numerator) if q.denominator==1 else f'{q.numerator}/{q.denominator}'
def fmt(x):
 names=('','sqrt(5)','i','i*sqrt(5)');parts=[]
 for q,n in zip(x,names):
  if not q:continue
  atom=fmtq(abs(q))+(('*'+n) if n and abs(q)!=1 else n if n else '')
  if n and abs(q)==1:atom=n
  parts.append(('-' if q<0 else '+')+atom)
 if not parts:return '0'
 s=''.join(parts);return s[1:] if s[0]=='+' else s

def powK(x,n):
 y=ONE
 while n:
  if n&1:y=mul(y,x)
  x=mul(x,x);n//=2
 return y

def tables():
 idx={g:i for i,g in enumerate(G)};mulT=[[idx[compose(g,h)] for h in G] for g in G];iid=idx[I]
 inv=[]
 for i in range(40):inv.append(next(j for j in range(40) if mulT[i][j]==iid and mulT[j][i]==iid))
 def order(i):
  x=iid
  for n in range(1,41):
   x=mulT[i][x]
   if x==iid:return n
  raise AssertionError
 center=[i for i in range(40) if all(mulT[i][j]==mulT[j][i] for j in range(40))]
 comm={mulT[mulT[mulT[a][b]][inv[a]]][inv[b]] for a in range(40) for b in range(40)}
 derived=set([iid]);front=list(comm)
 while front:
  x=front.pop()
  if x in derived:continue
  derived.add(x)
  for y in list(derived):front.extend((mulT[x][y],mulT[y][x]))
 r=next(i for i in derived if order(i)==5);z=next(i for i in center if order(i)==4)
 s=next(i for i in range(40) if order(i)==2 and mulT[mulT[s if False else i][r]][i]==inv[r])
 for cand in range(40):
  if order(cand)==2 and mulT[mulT[cand][r]][cand]==inv[r]:
   coords={}
   for k,e,a in itertools.product(range(4),range(2),range(5)):
    x=iid
    for _ in range(k):x=mulT[z][x]
    if e:x=mulT[s if False else cand][x]
    for _ in range(a):x=mulT[r][x]
    coords[(a,e,k)]=x
   if len(set(coords.values()))==40:s=cand;break
 coords={};reverse={}
 for k,e,a in itertools.product(range(4),range(2),range(5)):
  x=iid
  for _ in range(k):x=mulT[z][x]
  if e:x=mulT[s][x]
  for _ in range(a):x=mulT[r][x]
  coords[(a,e,k)]=x;reverse[x]=(a,e,k)
 return idx,mulT,inv,order,center,derived,r,s,z,coords,reverse

def dihedral_trace(j,a):
 a=(j*a)%5
 if a==0:return K(2)
 if a in (1,4):return K(F(-1,2),F(1,2))
 return K(F(-1,2),F(-1,2))

def character_rows(reverse):
 rows=[]
 for eps in (1,-1):
  for m in range(4):
   vals=[]
   for g in range(40):
    a,e,k=reverse[g];vals.append(scale(eps**e,powK(II,m*k)))
   rows.append({'name':f'chi_{eps:+d}_{m}','degree':1,'values':vals})
 for j in (1,2):
  for m in range(4):
   vals=[]
   for g in range(40):
    a,e,k=reverse[g];vals.append(ZERO if e else mul(powK(II,m*k),dihedral_trace(j,a)))
   rows.append({'name':f'rho_{j}_{m}','degree':2,'values':vals})
 return rows

def conv(x,y,mulT):
 out=[ZERO for _ in range(40)]
 for a,xa in enumerate(x):
  if eq0(xa):continue
  for b,yb in enumerate(y):
   if not eq0(yb):out[mulT[a][b]]=add(out[mulT[a][b]],mul(xa,yb))
 return out

def idempotents(chars,inv,mulT,iid):
 E=[]
 for ch in chars:E.append([scale(F(ch['degree'],40),ch['values'][inv[g]]) for g in range(40)])
 idem=all(conv(e,e,mulT)==e for e in E)
 orth=all(all(eq0(x) for x in conv(E[i],E[j],mulT)) for i in range(16) for j in range(i))
 total=[ZERO]*40
 for e in E:total=[add(x,y) for x,y in zip(total,e)]
 identity=[ZERO]*40;identity[iid]=ONE
 return E,idem,orth,total==identity

def full_walsh_character():
 out=[]
 for g in G:out.append(sum(s for w in range(4096) for u,s in [dual(w,g)] if u==w))
 return out

def inner_mult(psi,ch):
 z=ZERO
 for g in range(40):z=add(z,scale(psi[g],conj(ch['values'][g])))
 z=scale(F(1,40),z);assert z[1:]==(F(0),F(0),F(0)) and z[0].denominator==1
 return int(z[0])

def frequency_orbits():
 unseen=set(range(4096));out=[]
 while unseen:
  w0=min(unseen);O={w0};q=deque([w0])
  while q:
   w=q.popleft()
   for g in G:
    u,_=dual(w,g)
    if u not in O:O.add(u);q.append(u)
  unseen-=O;out.append(tuple(sorted(O)))
 return out

def fwht(a):
 a=list(a);h=1
 while h<len(a):
  for i in range(0,len(a),2*h):
   for j in range(i,i+h):x,y=a[j],a[j+h];a[j],a[j+h]=x+y,x-y
  h*=2
 return a

def fibres():
 FIB=defaultdict(set)
 for m in range(4096):
  offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A));FIB[tuple(charpoly_prime(5,offs)[0])].add(m)
 return [frozenset(S) for _,S in sorted(FIB.items(),key=lambda kv:json.dumps(kv[0],separators=(',',':')))]

def payload():
 idx,mulT,inv,order,center,derived,r,s,z,coords,reverse=tables();iid=idx[I];chars=character_rows(reverse);E,idem,orth,sumone=idempotents(chars,inv,mulT,iid)
 fullpsi=full_walsh_character();fullmult=tuple(inner_mult(fullpsi,ch) for ch in chars);ranks=tuple(ch['degree']*m for ch,m in zip(chars,fullmult))
 orbits=frequency_orbits();om=[]
 for O in orbits:
  psi=[]
  for g in G:psi.append(sum(ph for w in O for u,ph in [dual(w,g)] if u==w))
  m=tuple(inner_mult(psi,ch) for ch in chars);assert sum(ch['degree']*x for ch,x in zip(chars,m))==len(O);om.append(m)
 sigs=[]
 for S in fibres():
  W=fwht([1 if x in S else 0 for x in range(4096)]);active=[i for i,O in enumerate(orbits) if any(W[w] for w in O)]
  mult=tuple(sum(om[i][j] for i in active) for j in range(16));sigs.append((len(S),len(active),sum(c!=0 for c in W),mult))
 sc=Counter(sigs)
 checks={
  'group_order40':len(G)==40,
  'exact_identification_D10_times_C4':len(center)==4 and len(derived)==5 and len(reverse)==40 and order(r)==5 and order(s)==2 and order(z)==4,
  'sixteen_symbolic_characters':len(chars)==16 and Counter(c['degree'] for c in chars)==Counter({1:8,2:8}),
  'character_degree_squares40':sum(c['degree']**2 for c in chars)==40,
  'central_idempotents_idempotent':idem,
  'central_idempotents_pairwise_orthogonal':orth,
  'central_idempotents_sum_identity':sumone,
  'full_projector_ranks_exact':ranks==(104,)*8+(408,)*8,
  'frequency_orbits292':len(orbits)==292,
  'six_exact_fibre_signatures':len(sc)==6 and sum(sc.values())==98,
 }
 idrows=[]
 for ch,e,rankv in zip(chars,E,ranks):
  support=sum(not eq0(x) for x in e);idrows.append({'name':ch['name'],'degree':ch['degree'],'rank_in_Walsh4096':rankv,'support':support,'identity_coefficient':fmt(e[iid])})
 sigrows=[]
 for key,n in sorted(sc.items(),key=lambda kv:kv[0]):sigrows.append({'fibre_count':n,'fibre_size':key[0],'active_orbits':key[1],'nonzero_walsh':key[2],'exact_irreducible_multiplicities':key[3]})
 return {
  'schema':'w33.pass576.exact_walsh_central_idempotents.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'group':{'identification':'D10 x C4','presentation':'r^5=s^2=z^4=1, srs=r^-1, z central','generator_indices':{'r':r,'s':s,'z':z},'center_order':len(center),'derived_order':len(derived),'coordinate_bijection_size':len(reverse)},
  'character_field':'Q(i,sqrt(5))','characters':[{'name':c['name'],'degree':c['degree']} for c in chars],
  'primitive_central_idempotents':idrows,
  'signed_Walsh_representation':{'dimension':4096,'multiplicities':fullmult,'projector_ranks':ranks,'decomposition':'Eight one-dimensional characters occur with multiplicity 104; eight two-dimensional characters occur with multiplicity 204, hence central-projector rank 408.'},
  'formula_signatures':sigrows,
  'checks':checks,
  'boundary':'All character values, group-algebra convolutions, central idempotents, and multiplicities are exact in Q(i,sqrt(5)); no floating-point eigendecomposition is used.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 576 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'signatures':len(p['formula_signatures'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
