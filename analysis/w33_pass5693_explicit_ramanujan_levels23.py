#!/usr/bin/env python3
"""Pass5693: explicit W33 Ramanujan 2-lift levels two and three.

Pass5683 gave one explicit 160-vertex Ramanujan 2-lift and MSS gives existence of
an infinite tower. Here we continue constructively without an exponential signing
search. At each new 4-regular bipartite graph:

  1. deterministically factor the edges into four perfect matchings;
  2. test the six unions of two matchings as locally balanced signings;
  3. quotient the complementary-signing gauge and choose a canonical representative;
  4. choose the canonical class with smallest signed spectral radius;
  5. form the corresponding 2-lift.

Complementary signings sigma and -sigma are switching-equivalent on a bipartite
base (switch one bipartition). Their signed spectra agree exactly, but numerical
eigensolvers can differ at roundoff and previously let a floating tie choose either
representative. Because the next matching factorization depends on vertex labels,
that harmless first-level gauge choice changed later deterministic numerics. We now
fix the complement gauge by using representatives (0,1),(0,2),(0,3) and sorting
spectral classes only after rounding away eigensolver noise.

Important contract: the Pass5683 NEG indices refer to levi()'s producer order, so
that base edge order is preserved exactly. Newly generated lift edges are sorted.
"""
from __future__ import annotations
import collections,itertools,json,math
from pathlib import Path
import numpy as np
import w33_pass5683_balanced_ramanujan_levi_lifts as p5683
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5693_EXPLICIT_RAMANUJAN_LEVELS23.json'
RAM=2*math.sqrt(3)

def lift_edges(E,n,neg_idx):
    neg=set(neg_idx);out=[]
    for ei,(u,v) in enumerate(E):
      flip=1 if ei in neg else 0
      for sh in (0,1):
        a=u+sh*n;b=v+(sh^flip)*n
        if a>b:a,b=b,a
        out.append((a,b))
    return sorted(out)

def bipartition(E,n):
    adj=[[] for _ in range(n)]
    for u,v in E:adj[u].append(v);adj[v].append(u)
    col=[None]*n
    for s in range(n):
      if col[s] is not None:continue
      col[s]=0;q=collections.deque([s])
      while q:
        u=q.popleft()
        for v in sorted(adj[u]):
          if col[v] is None:col[v]=1-col[u];q.append(v)
          else:assert col[v]!=col[u]
    X=sorted(i for i,c in enumerate(col) if c==0);Y={i for i,c in enumerate(col) if c==1}
    assert len(X)==len(Y)==n//2
    return X,Y

def perfect_matching(E,n):
    X,Y=bipartition(E,n);adj={u:[] for u in X}
    for a,b in E:
      u,v=(b,a) if a in Y else (a,b);adj[u].append(v)
    for u in X:adj[u].sort()
    mt={}
    def dfs(u,seen):
      for v in adj[u]:
        if v in seen:continue
        seen.add(v)
        if v not in mt or dfs(mt[v],seen):mt[v]=u;return True
      return False
    for u in X:assert dfs(u,set())
    M={tuple(sorted((u,v))) for v,u in mt.items()};assert len(M)==n//2
    return M

def factor4(E,n):
    rem=set(E);M=[]
    for _ in range(4):
      m=perfect_matching(sorted(rem),n);M.append(m);rem-=m
    assert not rem
    return M

def signed_adj(E,n,neg):
    neg=set(neg);A=np.zeros((n,n),float)
    for i,(u,v) in enumerate(E):
      s=-1 if i in neg else 1;A[u,v]=A[v,u]=s
    return A

def unsigned_adj(E,n):return signed_adj(E,n,[])

def components(E,n):
    adj=[[] for _ in range(n)]
    for u,v in E:adj[u].append(v);adj[v].append(u)
    seen=set();sizes=[]
    for s in range(n):
      if s in seen:continue
      q=[s];seen.add(s);m=0
      while q:
        u=q.pop();m+=1
        for v in adj[u]:
          if v not in seen:seen.add(v);q.append(v)
      sizes.append(m)
    return sorted(sizes,reverse=True)

def best_two_matching_signing(E,n):
    mats=factor4(E,n);ei={e:i for i,e in enumerate(E)};rows=[]
    for a,b in itertools.combinations(range(4),2):
      neg={ei[e] for e in mats[a]|mats[b]}
      rho=float(np.max(np.abs(np.linalg.eigvalsh(signed_adj(E,n,neg)))))
      rows.append((rho,a,b,neg))
    D={(a,b):rho for rho,a,b,_ in rows}
    for x,y in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]:
      assert abs(D[x]-D[y])<1e-8
    canonical=[r for r in rows if (r[1],r[2]) in {(0,1),(0,2),(0,3)}]
    canonical.sort(key=lambda z:(round(z[0],10),z[1],z[2]))
    rows.sort(key=lambda z:(round(z[0],10),z[1],z[2]))
    return canonical[0],rows

def graph_metrics(E,n):
    ev=np.linalg.eigvalsh(unsigned_adj(E,n));non=[abs(x) for x in ev if abs(abs(x)-4)>1e-7]
    rho=float(max(non));gap=4-rho;distinct=[]
    for x in ev:
      if not distinct or abs(x-distinct[-1])>1e-7:distinct.append(float(x))
    return {'vertices':n,'edges':len(E),'nontrivial_radius':rho,'laplacian_gap':gap,'distinct_eigenvalues':len(distinct)}

def main():
    E0=p5683.levi();neg0=set(p5683.NEG);assert len(E0)==160 and len(neg0)==80
    E1=lift_edges(E0,80,neg0);assert components(E1,160)==[160]
    best1,all1=best_two_matching_signing(E1,160);rho1,a1,b1,neg1=best1
    assert (a1,b1)==(0,1) and len(neg1)==160 and rho1<RAM
    E2=lift_edges(E1,160,neg1);assert components(E2,320)==[320]
    best2,all2=best_two_matching_signing(E2,320);rho2,a2,b2,neg2=best2
    assert (a2,b2)==(0,1) and len(neg2)==320 and rho2<RAM
    E3=lift_edges(E2,320,neg2);assert components(E3,640)==[640]
    for E,n,neg in [(E1,160,neg1),(E2,320,neg2)]:
      d=np.zeros(n,dtype=int)
      for i in neg:
        u,v=E[i];d[u]+=1;d[v]+=1
      assert set(d)=={2}
    levels=[graph_metrics(E0,80),graph_metrics(E1,160),graph_metrics(E2,320),graph_metrics(E3,640)]
    assert all(x['nontrivial_radius']<RAM+1e-8 for x in levels)
    out={
      'pass':5693,'status':'EXPLICIT_RAMANUJAN_W33_2LIFT_LEVELS_320_AND_640_CONSTRUCTED__COMPLEMENT_GAUGE_FIXED',
      'ramanujan_bound':RAM,
      'producer_order_contract':'Pass5683 NEG is applied to levi() in its original line-major order; only derived lift edge lists are sorted.',
      'complement_gauge_contract':'For the four matching colors, 01~23, 02~13, 03~12 by sign complementation/switching. Canonical representatives are 01,02,03; spectral sorting rounds to 1e-10 before lexical tie-break.',
      'construction':'At each new 4-regular bipartite graph, deterministic four-perfect-matching factorization followed by exhaustive choice among the three complementary-signing switching classes.',
      'level1_to_level2_signing':{'parent_vertices':160,'negative_edges':len(neg1),'negative_degree_each_vertex':2,'matching_colors':[a1,b1],'signed_radius':rho1,'all_six_signed_radii':[float(x[0]) for x in all1]},
      'level2_to_level3_signing':{'parent_vertices':320,'negative_edges':len(neg2),'negative_degree_each_vertex':2,'matching_colors':[a2,b2],'signed_radius':rho2,'all_six_signed_radii':[float(x[0]) for x in all2]},
      'explicit_levels':levels,
      'conclusion':'The W33 Levi root has an explicit connected Ramanujan tower at 80,160,320 and 640 vertices under a deterministic switching-gauge convention. The complement gauge must be fixed before recursive labeling-dependent searches are reproducible.',
      'recursion_boundary':'The perfect-matching factorization still depends on deterministic graph ordering and the three switching classes are permuted by color relabeling. No automorphism-canonical or all-level recursive signing theorem is claimed.',
      'physics_boundary':'These are expander refinements of an internal graph carrier, not a physical spacetime discretization or continuum-limit proof.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
