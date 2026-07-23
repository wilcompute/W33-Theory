#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass607_johnson_clique_pi1.json'

def free_reduce(word):
    stack=[]
    for x in word:
        if stack and stack[-1]==-x: stack.pop()
        else: stack.append(x)
    return tuple(stack)

def inverse_word(word): return tuple(-x for x in reversed(word))

def presentation():
    vertices=list(itertools.combinations(range(8),3))
    edges=[]; adj=[[] for _ in vertices]
    for i,A in enumerate(vertices):
        for j in range(i+1,len(vertices)):
            if len(set(A)&set(vertices[j]))==2:
                edges.append((i,j));adj[i].append(j);adj[j].append(i)
    edge_set=set(edges)
    parent=[None]*len(vertices); parent[0]=-1; q=collections.deque([0]); tree=set()
    while q:
        i=q.popleft()
        for j in sorted(adj[i]):
            if parent[j] is None:
                parent[j]=i; tree.add(tuple(sorted((i,j)))); q.append(j)
    non_tree=[e for e in edges if e not in tree]; gid={e:k+1 for k,e in enumerate(non_tree)}
    def letter(a,b):
        e=tuple(sorted((a,b)))
        if e in tree:return None
        return gid[e] if a<b else -gid[e]
    triangles=[]; relators=[]
    for i,j,k in itertools.combinations(range(len(vertices)),3):
        if (i,j) in edge_set and (i,k) in edge_set and (j,k) in edge_set:
            triangles.append((i,j,k))
            w=free_reduce(x for x in (letter(i,j),letter(j,k),letter(k,i)) if x is not None)
            if w:relators.append(w)
    return vertices,edges,tree,non_tree,triangles,relators

def tietze_eliminate(relators,ngens):
    rels=list(relators); active=set(range(1,ngens+1)); transcript=[]; histogram=[]
    while True:
        found=None
        for ri,w in enumerate(rels):
            counts=collections.Counter(abs(x) for x in w)
            for g in sorted(counts):
                if counts[g]==1 and g in active:
                    found=(ri,g);break
            if found:break
        if found is None:break
        ri,g=found; w=rels[ri]; p=next(i for i,x in enumerate(w) if abs(x)==g); x=w[p]
        A=w[:p];B=w[p+1:]
        rhs=free_reduce(inverse_word(A)+inverse_word(B)) if x==g else free_reduce(B+A)
        transcript.append((g,w,rhs))
        active.remove(g); new=[]
        for sj,u in enumerate(rels):
            if sj==ri:continue
            v=[]
            for z in u:
                if abs(z)!=g:v.append(z)
                elif z==g:v.extend(rhs)
                else:v.extend(inverse_word(rhs))
            v=free_reduce(v)
            if v:new.append(v)
        rels=new
        if len(transcript)%25==0 or not active:
            histogram.append({'eliminated':len(transcript),'active_generators':len(active),'relators':len(rels),'max_relator_length':max(map(len,rels),default=0)})
    h=hashlib.sha256()
    for g,w,rhs in transcript:h.update(repr((g,w,rhs)).encode())
    return active,rels,transcript,h.hexdigest(),histogram

def payload():
    V,E,T,N,tri,rels=presentation();active,left,seq,digest,hist=tietze_eliminate(rels,len(N))
    star_cliques=collections.Counter();top_cliques=collections.Counter()
    for t in tri:
        sets=[set(V[i]) for i in t];inter=set.intersection(*sets);union=set.union(*sets)
        if len(inter)==2:star_cliques[tuple(sorted(inter))]+=1
        elif len(union)==4:top_cliques[tuple(sorted(union))]+=1
    checks={
      'Johnson_vertices56_edges420':len(V)==56 and len(E)==420,
      'spanning_tree55_generators365':len(T)==55 and len(N)==365,
      'clique_triangles840':len(tri)==840,
      'triangle_geometry_560_star_280_top':sum(star_cliques.values())==560 and sum(top_cliques.values())==280,
      'all365_generators_eliminated':len(seq)==365 and not active,
      'all_relators_eliminated':left==[],
      'tietze_relators_never_exceed_length3':max(x['max_relator_length'] for x in hist)==3,
      'deterministic_transcript_hash':digest=='a1ea002c8fa703cb9daa001575feecd68e540f5d51095236d832b75670077529',
    }
    return {'schema':'w33.pass607.johnson_clique_pi1.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'complex':{'name':'clique complex of J(8,3)','vertices':len(V),'edges':len(E),'triangles':len(tri),'star_triangles':sum(star_cliques.values()),'top_triangles':sum(top_cliques.values())},
      'presentation':{'tree_edges':len(T),'initial_generators':len(N),'initial_nontrivial_relators':len(rels),'eliminations':len(seq),'remaining_generators':len(active),'remaining_relators':len(left),'transcript_sha256':digest,'progress':hist},
      'theorem':'The clique complex of J(8,3) is simply connected. A deterministic sequence of 365 elementary Tietze eliminations removes every free generator and every triangle relator from the spanning-tree edge presentation.',
      'flat_connection_consequence':'For every discrete group G, every triangle-flat G-valued connection on J(8,3) is gauge equivalent to the trivial connection. In particular, no finite perfect S5 quotient survives the triangle relations.',
      'checks':checks,'boundary':'This proves pi_1=1 for the full clique complex using all 840 triangle 2-cells. It does not say that arbitrary curved Pass-594 connections are gauge trivial.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 607 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'eliminations':p['presentation']['eliminations']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
