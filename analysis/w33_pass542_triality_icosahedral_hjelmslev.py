#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data'/'w33_pass542_triality_icosahedral_hjelmslev.json'
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A,v):return tuple(sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A)))
def tr(A):return [list(x) for x in zip(*A)]
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def cp(v,m):return min(v,((-v[0])%m,(-v[1])%m))
def AC(m):return sorted({cp(v,m) for v in itertools.product(range(m),repeat=2) if v!=(0,0)})
def det(g,m):a,b,c,d=g;return (a*d-b*c)%m
def mats(m,D):return [g for g in itertools.product(range(m),repeat=4) if det(g,m) in D]
def act(g,v,m):a,b,c,d=g;return ((a*v[0]+b*v[1])%m,(c*v[0]+d*v[1])%m)
def pimage(M,C,m):
 I={v:i for i,v in enumerate(C)};return {tuple(I[cp(act(g,v,m),m)] for v in C) for g in M}
def pc(p,q):return tuple(p[q[i]] for i in range(len(p)))
def po(p):
 e=tuple(range(len(p)));x=e
 for k in range(1,100):
  x=pc(p,x)
  if x==e:return k
 raise AssertionError
def leg(a,p):
 a%=p
 return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
def om(u,v,m):return (u[0]*v[1]-u[1]*v[0])%m
def RG(C,p,s):
 G=nx.Graph();G.add_nodes_from(range(len(C)))
 for i,u in enumerate(C):
  for j in range(i+1,len(C)):
   if leg(om(u,C[j],p),p)==s:G.add_edge(i,j)
 return G
def allcycles(G):
 out=set();n=len(G)
 def can(a):
  V=[]
  for s in (a,list(reversed(a))):
   for i in range(len(s)):V.append(tuple(s[i:]+s[:i]))
  return min(V)
 for z in range(n):
  def dfs(a):
   for y in G[a[-1]]:
    if y==z and len(a)>=3:out.add(can(a))
    elif y not in a and len(a)<n:dfs(a+[y])
  dfs([z])
 return sorted(out)
def prod(a,p):
 r=1
 for x in a:r=r*x%p
 return r
def section_actions(p):
 C=AC(p);I={v:i for i,v in enumerate(C)};A=[]
 for a,b,c,d in mats(p,{1}):
  gi=(d%p,(-b)%p,(-c)%p,a%p);P=[];E=[]
  for r in C:
   w=act(gi,r,p);q=cp(w,p);P.append(I[q]);E.append(1 if w==q else -1)
  A.append((P,E))
 return C,A
def orb(s,A,p):return {tuple(E[i]*s[P[i]]%p for i in range(len(s))) for P,E in A}
def partA(ch):
 V=set()
 for i in range(4):
  for s in(-1,1):x=[Q(0)]*4;x[i]=Q(s);V.add(tuple(x))
 S=[set(),set()]
 for a in itertools.product((-1,1),repeat=4):S[sum(x<0 for x in a)%2].add(tuple(Q(x,2) for x in a))
 T=[[Q(x,2) for x in r] for r in [[1,1,1,-1],[1,1,-1,1],[1,-1,1,1],[1,-1,-1,-1]]]
 C,A=section_actions(3); O={s for s in itertools.product(range(3),repeat=4) if sum(x!=0 for x in s)==1};P={s for s in itertools.product((1,2),repeat=4) if prod(s,3)==1};M={s for s in itertools.product((1,2),repeat=4) if prod(s,3)==2}
 ch.update(T_orthogonal=mm(tr(T),T)==eye(4),T_order3=mm(mm(T,T),T)==eye(4),T_cycles=({mv(T,x) for x in V}==S[0] and {mv(T,x) for x in S[0]}==S[1] and {mv(T,x) for x in S[1]}==V),three_8sets=len(V)==len(S[0])==len(S[1])==8,orbit_8v=orb(next(iter(O)),A,3)==O,orbit_8sp=orb(next(iter(P)),A,3)==P,orbit_8sm=orb(next(iter(M)),A,3)==M)
 return {'classes':C,'sets':{'8v':8,'8s+':8,'8s-':8},'T':[[str(x) for x in r] for r in T],'cycle':['8v','8s+','8s-','8v']}
def partB(ch):
 out={}
 for p,rot,full,name in [(3,12,24,'tetrahedron'),(5,60,120,'icosahedron')]:
  C=AC(p);SL=mats(p,{1});D=set(range(1,p)) if p==3 else {x for x in range(1,p) if leg(x,p)==1};R=pimage(SL,C,p);F=pimage(mats(p,D),C,p)
  ch[f'p{p}_rot']=len(R)==rot;ch[f'p{p}_full']=len(F)==full
  row={'classes':len(C),'rotation_image':len(R),'extended_image':len(F),'name':name,'orders':dict(Counter(po(x) for x in R))}
  if p==5:
   G,H=RG(C,5,1),RG(C,5,-1);opp={i:[j for j in range(12) if j!=i and om(C[i],C[j],5)==0][0] for i in range(12)};aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter());Qm=mats(5,{2,3})[0];q=next(iter(pimage([Qm],C,5)))
   ch.update(ico=nx.is_isomorphic(G,nx.icosahedral_graph()),ico2=nx.is_isomorphic(H,nx.icosahedral_graph()),valencies=all(G.degree(i)==H.degree(i)==5 and opp[opp[i]]==i for i in G),links=all(nx.is_isomorphic(G.subgraph(list(G[i])),nx.cycle_graph(5)) for i in G),full_aut=aut==len(F)==120 and all(all(G.has_edge(x[u],x[v]) for u,v in G.edges()) for x in F),swap=all(G.has_edge(i,j)==H.has_edge(q[i],q[j]) for i in G for j in G if i<j))
   row.update(edges=30,triangles=sum(nx.triangles(G).values())//3,scheme=[1,5,5],automorphisms=aut)
  out[f'p{p}']=row
 return out
def partC(ch):
 C=AC(5);G=RG(C,5,1);A=(1,1,2,2,2,3,3,2,3,2,3,2);B=(1,1,2,2,3,3,3,3,2,3,2,2);sqA=tuple(x*x%5 for x in A);sqB=tuple(x*x%5 for x in B);r=tuple(y*pow(x,-1,5)%5 for x,y in zip(A,B));sw=[i for i,x in enumerate(r) if x==4];CA=Counter();CB=Counter();cy=allcycles(G)
 for z in cy:
  a=b=1
  for i,j in zip(z,z[1:]+z[:1]):w=om(C[i],C[j],5);a=a*A[i]*A[j]*w%5;b=b*B[i]*B[j]*w%5
  if len(z)%2:a=min(a,-a%5);b=min(b,-b%5)
  CA[(len(z),a)]+=1;CB[(len(z),b)]+=1
 EA=Counter(A[i]*A[j]%5 for i,j in G.edges());EB=Counter(B[i]*B[j]%5 for i,j in G.edges())
 ch.update(squares=sqA==sqB,signword=set(r)<={1,4},five_switch=len(sw)==5,product_flip=prod(B,5)==-prod(A,5)%5,cycles_blind=CA==CB,edge_separates=EA!=EB)
 return {'A':A,'B':B,'squares':sqA,'ratio':r,'switched':sw,'products':[prod(A,5),prod(B,5)],'cycles':len(cy),'cycle_lengths':dict(Counter(map(len,cy))),'edge_profiles':[dict(EA),dict(EB)]}
def mul(g,h,m):a,b,c,d=g;e,f,k,l=h;return ((a*e+b*k)%m,(a*f+b*l)%m,(c*e+d*k)%m,(c*f+d*l)%m)
def red9(v):return (cp((v[0]%3,v[1]%3),3),'primitive') if v[0]%3 or v[1]%3 else (cp((v[0]//3%3,v[1]//3%3),3),'deep')
def partD(ch):
 A9,A3=AC(9),AC(3);fib={x:{'primitive':[],'deep':[]} for x in A3}
 for v in A9:b,s=red9(v);fib[b][s].append(v)
 S9,S3=mats(9,{1}),mats(3,{1});K=[g for g in S9 if tuple(x%3 for x in g)==(1,0,0,1)];I={v:i for i,v in enumerate(A9)};P=[tuple(I[cp(act(g,v,9),9)] for v in A9) for g in K];rows=[]
 for b in A3:
  Qs={I[v] for v in fib[b]['primitive']};z=I[fib[b]['deep'][0]];rows.append({'base':b,'primitive':len(Qs),'orbit':len({p[next(iter(Qs))] for p in P}),'deep_fixed':all(p[z]==z for p in P)})
 BI={v:i for i,v in enumerate(A3)};Qp={tuple(BI[cp(act(tuple(x%3 for x in g),v,3),3)] for v in A3) for g in S9};od=Counter(po(x) for x in Qp)
 ab=all(mul(g,h,9)==mul(h,g,9) for g in K for h in K);ex=all(mul(mul(g,g,9),g,9)==(1,0,0,1) for g in K)
 ch.update(A9_40=len(A9)==40,fibres=all(len(x['primitive'])==9 and len(x['deep'])==1 for x in fib.values()),SL9_648=len(S9)==648,kernel27=len(K)==27,kernel_C3cubed=ab and ex,kernel_transitive=all(x['orbit']==9 for x in rows),deep_fixed=all(x['deep_fixed'] for x in rows),quotient_A4=len(Qp)==12 and od==Counter({3:8,2:3,1:1}),exact_sequence=len(K)*len(S3)==len(S9))
 return {'classes':40,'fibres':rows,'kernel':'C3^3','orders':[27,648,24],'quotient_orders':dict(od)}
def rec(a,b,n):
 S=[3,0,2*a]
 for m in range(3,n+1):S.append(a*S[m-2]+b*S[m-3])
 return S
def v3(n):
 if n==0:return 999
 v=0
 while n%3==0:n//=3;v+=1
 return v
def partE(ch):
 V,H,A=rec(1,0,120),rec(4,3,120),rec(3,1,120);ev=range(2,121,2);o1=range(7,121,6);o35=[m for m in range(3,121,2) if m%6 in(3,5)]
 ch.update(trace_even=all(v3(V[m])==0 for m in ev),trace_spin=all(v3(H[m])==1 for m in o1),trace_aux=all(v3(A[m])==1 for m in o35),triality_not_all_odd=any(v3(H[m])>1 for m in o35))
 return {'8v':'all even','8s':'odd 1 mod 6','aux':'odd 3,5 mod 6'}
def payload():
 c={};A=partA(c);B=partB(c);C=partC(c);D=partD(c);E=partE(c);return {'schema':'w33.pass542.triality_icosahedral_hjelmslev.v1','status':'PASS' if all(c.values()) else 'FAIL','triality':A,'polyhedral':B,'odd_switch':C,'z9_bundle':D,'trace_boundary':E,'checks':c,'boundary':'finite exact; no q5 image classification or physical claim'}
def main():
 a=argparse.ArgumentParser();a.add_argument('--check',action='store_true');a.add_argument('--output',type=Path,default=OUT);x=a.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if x.check:
  if not x.output.exists() or x.output.read_text()!=s:raise SystemExit('Pass 542 certificate drift')
 else:x.output.parent.mkdir(parents=True,exist_ok=True);x.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())