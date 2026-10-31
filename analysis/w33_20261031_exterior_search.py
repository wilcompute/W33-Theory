"""Exact normalized prime-field exterior-arc matching search. See the five-front report for proof of exhaustive normalization."""
import sys,time,itertools,json,pathlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
if hasattr(sys.stdout,'reconfigure'):
 sys.stdout.reconfigure(encoding='utf-8',errors='replace')
def solve(q,square=False,limit=90,backend='conic'):
 if q<3 or q%2==0 or any(q%d==0 for d in range(3,int(q**.5)+1,2)):
  raise ValueError('This producer accepts odd prime fields only')
 t0=time.monotonic();target=(q+1)//2;I=q
 pairs=list(itertools.combinations(range(q+1),2));lookup={p:i for i,p in enumerate(pairs)}
 P=np.array([(2*a%q,1,0) if b==I else (a*b%q,(a+b)*pow(2,-1,q)%q,1) for a,b in pairs],dtype=np.int64)
 n=len(P);x,y,z=P.T;squares={a*a%q for a in range(1,q)};chi=np.array([0]+[1 if a in squares else -1 for a in range(1,q)])
 def bits(mask):return int.from_bytes(np.packbits(mask,bitorder='little').tobytes(),'little')
 adj=[]
 for row,(a,b,c) in enumerate(P):
  if backend=='conic':
   aa=(b*z-c*y)%q;bb=(c*x-a*z)%q;cc=(a*y-b*x)%q
   disc=(bb*bb-4*aa*cc)%q
  elif backend=='cross_ratio':
   # Independent homogeneous P1 formula: quadratic character of the four
   # determinants in the numerator and denominator of the cross-ratio.
   u,v=pairs[row];C=np.array([s for s,t in pairs]);D=np.array([t for s,t in pairs])
   def df(s,A):
    if s==I:return np.where(A==I,0,1)
    return np.where(A==I,-1,s-A)%q
   disc=df(u,C)*df(v,D)%q*df(u,D)%q*df(v,C)%q
  else:raise ValueError('unknown predicate backend')
  adj.append(bits(chi[disc]==(1 if square else -1)))
 incident=[0]*(q+1)
 for j,(a,b) in enumerate(pairs):incident[a]|=1<<j;incident[b]|=1<<j
 allpoints=(1<<(q+1))-1;linecache={};nodes=0;maxdepth=0;witness=None
 def linemask(i,j):
  a,b,c=map(int,np.cross(P[i],P[j])%q);u=next(v for v in (a,b,c) if v);inv=pow(u,-1,q);key=tuple(v*inv%q for v in (a,b,c))
  if key not in linecache:
   linecache[key]=bits((key[0]*x+key[1]*y+key[2]*z)%q==0)
  return linecache[key]
 def bt(chosen,free,allowed):
  nonlocal nodes,maxdepth,witness
  nodes+=1;maxdepth=max(maxdepth,len(chosen))
  if nodes%1024==0 and time.monotonic()-t0>limit:raise TimeoutError
  if not free:witness=list(chosen);return True
  options=None
  for a in range(q+1):
   if free>>a&1:
    cand=allowed&incident[a];count=cand.bit_count()
    if count==0:return False
    if options is None or count<options.bit_count():options=cand
  while options:
   bit=options&-options;options-=bit;j=bit.bit_length()-1;a,b=pairs[j]
   nextallowed=allowed&adj[j]
   for i in chosen:
    nextallowed&=~linemask(i,j)
   if bt(chosen+[j],free&~((1<<a)|(1<<b)),nextallowed):return True
  return False
 start=lookup[(0,I)]
 try:
  found=bt([start],allpoints&~((1<<I)|1),adj[start]);status='found' if found else 'none_complete'
 except TimeoutError:status='timeout'
 import hashlib
 rec=dict(q=q,family='square' if square else 'nonsquare',status=status,nodes=nodes,max_depth=maxdepth,seconds=round(time.monotonic()-t0,3),backend=backend,
          compatibility_sha256=hashlib.sha256(b''.join(a.to_bytes((n+7)//8,'little') for a in adj)).hexdigest(),
          normalized_first_pair=[0,'inf'],matching=[['inf' if a==I else a,'inf' if b==I else b] for a,b in (pairs[j] for j in witness)] if witness else None)
 return rec
if __name__=='__main__':
 out=[]
 for q in [int(a) for a in sys.argv[1:] if a.isdigit()]:
  row=solve(q,square='--square' in sys.argv,limit=600,backend='cross_ratio' if '--cross-ratio' in sys.argv else 'conic');out.append(row);print(json.dumps(row),flush=True)
  (ROOT/'data'/('w33_20261031_exterior_search'+('_square' if '--square' in sys.argv else '')+('_cross_ratio' if '--cross-ratio' in sys.argv else '')+'.json')).write_text(json.dumps(out,indent=2))
