from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import json,hashlib,sys
p=Path(sys.argv[1]);raw=p.read_bytes();lines=raw.decode('ascii').splitlines()
assert len(lines)==28
def decode(t):
 n=ord(t[0])-63;assert n==40
 bits=[(ord(c)-63>>b)&1 for c in t[1:] for b in range(5,-1,-1)]
 A=[0]*n;z=0
 for j in range(1,n):
  for i in range(j):
   if bits[z]:A[i]|=1<<j;A[j]|=1<<i
   z+=1
 assert z==780 and all(x.bit_count()==12 for x in A)
 assert all((A[i]&A[j]).bit_count()==(2 if A[i]>>j&1 else 4) for i in range(n) for j in range(i+1,n))
 return A
def basis(rows):
 p={}
 for x in rows:
  while x:
   b=x.bit_length()-1
   if b not in p:p[b]=x;break
   x^=p[b]
 return p
def remainder(x,b):
 while x:
  k=x.bit_length()-1
  if k not in b:break
  x^=b[k]
 return x
def kth(A):
 count=0
 for i in range(40):
  for j in range(i+1,40):
   if not A[i]>>j&1:continue
   co=A[i]&A[j]
   a=(co&-co).bit_length()-1;b=co.bit_length()-1
   count+=A[a]>>b&1
 assert count%6==0
 return count//6
def exact_small_distance(A,b):
 n=40
 # Single-, double-, triple-coordinate syndrome tables.
 D=[]
 for k in range(4):
  dic=defaultdict(list)
  for cs in combinations(range(n),k):
   support=sum(1<<i for i in cs)
   syndrome=0
   for i in cs:syndrome^=A[i]
   dic[syndrome].append(support)
  D.append(dic)
 # Work in ascending total weight. A codeword x with |x|<=6
 # decomposes into disjoint r- and s-subsets with r,s<=3.
 checks=[(0,1),(1,1),(1,2),(2,2),(2,3),(3,3)]
 for r,s in checks:
  for syndrome,rs in D[r].items():
   ss=D[s].get(syndrome,[])
   if not ss:continue
   for a in rs:
    for z in ss:
     if a&z:continue
     word=a^z
     if not word:continue
     if remainder(word,b):return r+s,word
 return None,None
out=[]
for ix,t in enumerate(lines):
 A=decode(t);b=basis(A)
 d,w=exact_small_distance(A,b)
 out.append(dict(graph6_catalog_index=ix,rank2=len(b),logical_qubits=40-2*len(b),K4=kth(A),distance_leq6=d, witness_support=([j for j in range(40) if w>>j&1] if w else None)))
print('sha256',hashlib.sha256(raw).hexdigest())
print('ranks',dict(sorted(Counter(z['rank2'] for z in out).items())))
print('K4_40',[(z['graph6_catalog_index'],z['rank2']) for z in out if z['K4']==40])
print('distances_through6',dict(sorted(Counter(str(z['distance_leq6']) for z in out).items())))
print('logical_by_distance',sorted(Counter((z['logical_qubits'],z['distance_leq6']) for z in out).items(),key=str))
print('w33',out[27])
print('dual',out[26])
print('complete',json.dumps(out,separators=(',',':')))
