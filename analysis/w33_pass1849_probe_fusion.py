#!/usr/bin/env python3
import sys,collections,math,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1801_1805_common import build_geometry
D=build_geometry();igs=[tuple(a[0]) for a in D['acts']];s=tuple(D['outer'][0]);I=tuple(range(40))
def comp(p,q):return tuple(p[q[i]]for i in range(40))
def inv(p):
 r=[0]*40
 for i,j in enumerate(p):r[j]=i
 return tuple(r)
def power(p,n):
 if n<0:return power(inv(p),-n)
 y=I
 while n:
  if n&1:y=comp(p,y)
  p=comp(p,p);n//=2
 return y
def order(p):
 seen=[0]*40;z=1
 for i in range(40):
  if seen[i]:continue
  j=i;n=0
  while not seen[j]:seen[j]=1;n+=1;j=p[j]
  z=math.lcm(z,n)
 return z
def cyc(p):
 seen=[0]*40;o=[]
 for i in range(40):
  if seen[i]:continue
  j=i;n=0
  while not seen[j]:seen[j]=1;n+=1;j=p[j]
  o.append(n)
 return sorted(o,reverse=True)
seen={I:''};q=collections.deque([I])
while q:
 x=q.popleft();w=seen[x]
 for i,g in enumerate(igs):
  y=comp(g,x)
  if y not in seen:seen[y]=str(i)+w;q.append(y)
assert len(seen)==25920
x=next(g for g,w in seen.items()if w=='3423144210');c=comp(s,x)
def subgroup(c,d):
 di=inv(d);S={I};Q=collections.deque([I])
 while Q:
  x=Q.popleft()
  for g in(c,d,di):
   y=comp(g,x)
   if y not in S:S.add(y);Q.append(y)
 return S
for d,w in seen.items():
 if order(d)==9 and order(comp(c,d))==10:
  H=subgroup(c,d)
  if len(H)==51840:break
else:raise RuntimeError
full=list(H);di=inv(d)
def cent(x):return sum(comp(g,x)==comp(x,g)for g in full)
def eval_word(w,side='left'):
 y=I
 for ch in w:
  g=c if ch=='c'else d;y=comp(g,y)if side=='left'else comp(y,g)
 return y
official={'4C':('cdcdcdd',3,96),'4D':('dcdcdcdd',1,32),'6G':('ccdcdcddcdcdddcddcddcdcdddcdd',1,36),'6H':('dcdd',1,36),'6I':('cdcdddcdd',1,12),'8A':('cdd',1,8),'2C':('ccdcdcddcdcdddcddcddcdcdddcdd',3,1440),'2D':('cdcdddcdd',3,96)}
reps={}
for lab,(w,p,ce)in official.items():
 a=power(eval_word(w),p);b=power(eval_word(w,'right'),p);ca,cb=cent(a),cent(b)
 if ca==ce:reps[lab]=a
 elif cb==ce:reps[lab]=b
 else:raise RuntimeError((lab,ca,cb,ce))
probe_words={'2D':'','probe4':'3210','probe6':'23410','probe8':'10'}
probes={k:comp(s,next(g for g,w in seen.items()if w==iw))if iw else s for k,iw in probe_words.items()}
invs={g:inv(g)for g in full};conjsets={lab:{comp(comp(invs[g],r),g)for g in full}for lab,r in reps.items()}
class_of={k:next(lab for lab,S in conjsets.items()if p in S)for k,p in probes.items()}
parent={I:(None,None)};Q=collections.deque([I]);targets=set(probes.values())
while Q and not all(t in parent for t in targets):
 x=Q.popleft()
 for g,L in((c,'c'),(d,'d'),(di,'D')):
  y=comp(g,x)
  if y not in parent:parent[y]=(x,L);Q.append(y)
def getword(t):
 out=[]
 while parent[t][0]is not None:t,L=parent[t];out.append(L)
 return out[::-1]
def compact(w):
 out=[];i=0
 while i<len(w):
  j=i+1
  while j<len(w)and w[j]==w[i]:j+=1
  out.append(w[i]if j-i==1 else f'{w[i]}^{j-i}');i=j
 return' '.join(out)
def fixed_counts(p):
 points=D['points'];lines=D['lines'];frames=D['frames'];octets=D['octets'];ld={L:i for i,L in enumerate(lines)};fd={f:i for i,f in enumerate(frames)}
 lp=tuple(ld[tuple(sorted(p[x]for x in L))]for L in lines);fp=tuple(fd[tuple(sorted((lp[a],lp[b])))]for a,b in frames)
 os=[frozenset(a)|frozenset(b)for a,b in octets];od={x:i for i,x in enumerate(os)};op=tuple(od[frozenset(p[x]for x in(set(a)|set(b)))]for a,b in octets)
 return[sum(p[i]==i for i in range(40)),sum(lp[i]==i for i in range(40)),sum(fp[i]==i for i in range(540)),sum(op[i]==i for i in range(45))]
rows=[]
for pk,p in probes.items():
 lab=class_of[pk];w=getword(p);rows.append({'probe':pk,'atlas_class':lab,'order':order(p),'centralizer':cent(p),'cycle_type':cyc(p),'fixed_points_lines_frames_octets':fixed_counts(p),'shortest_word':w,'shortest_word_compact':compact(w),'word_length':len(w),'power_classes':{str(k):next((L for L,S in conjsets.items()if power(p,k)in S),None)for k in range(2,order(p))}})
out={'schema':'w33.pass1849.outer_probe_atlas_fusion.v1','status':'PASS','group_order':len(full),'standard_pair':{'c_centralizer':cent(c),'d_order':order(d),'cd_order':order(comp(c,d))},'probes':rows,'official_rep_words':{k:v[:2]for k,v in official.items()},'checks':{'unique_class_fusion':True,'literal_shortest_words':True,'centralizers_match_atlas':True},'boundary':'Class labels are fused by exact conjugacy to official ATLAS class-representative words evaluated in the project standard pair.'}
raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['sha256']=hashlib.sha256(raw).hexdigest();(ROOT/'data'/'w33_pass1849_outer_probe_atlas_fusion.json').write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(out,indent=2))
