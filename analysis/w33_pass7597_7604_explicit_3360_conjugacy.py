#!/usr/bin/env python3
"""Pass7597-7604: literal point-by-point conjugacy between the ATLAS 3360 action
of O8+(3):S4 and the independently reconstructed E8/3E8 D4 triality graph.

This closes the remaining 'same standard carrier' gap: the script downloads the
canonical ATLAS degree-3360 generators, reconstructs their unique degree-80
triality orbital graph, rebuilds the E8 point/+generator/-generator graph, and
finds an explicit color-preserving graph isomorphism by individualization /
1-dimensional Weisfeiler-Leman refinement.  The full 3360-entry map is emitted.
"""
from __future__ import annotations
import argparse,hashlib,itertools,json,re,time,urllib.request
from collections import Counter,deque
from pathlib import Path
import sys
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E

URLS=[
 'https://brauer.maths.qmul.ac.uk/Atlas/clas/O8p3/gap/O8p3S4G2-p3360B0.g1',
 'https://brauer.maths.qmul.ac.uk/Atlas/clas/O8p3/gap/O8p3S4G2-p3360B0.g2']
OUT=ROOT/'data/PART_W33_PASS7597_7604_EXPLICIT_3360_CONJUGACY.json'
N=3360

def load(url,cache):
    cache.mkdir(parents=True,exist_ok=True);p=cache/Path(url).name
    if not p.exists():
        with urllib.request.urlopen(url,timeout=60) as r:p.write_bytes(r.read())
    b=p.read_bytes();return b,hashlib.sha256(b).hexdigest()
def parse_cycles(raw):
    text=raw.decode('ascii');p=list(range(N))
    for m in re.finditer(r'\((\s*\d+(?:[\s,]+\d+)+\s*)\)',text):
        cyc=[int(x)-1 for x in re.findall(r'\d+',m.group(1))]
        for a,b in zip(cyc,cyc[1:]+cyc[:1]):p[a]=b
    assert sorted(p)==list(range(N));return tuple(p)
def inv(p):
    q=[0]*N
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def edgecode(a,b):
    if a>b:a,b=b,a
    return a*N+b
def edgepair(z):return divmod(z,N)
def edge_orbit(seed_edges,gens):
    S={edgecode(a,b) for a,b in seed_edges};q=deque(S)
    while q:
        z=q.popleft();a,b=edgepair(z)
        for g in gens:
            w=edgecode(g[a],g[b])
            if w not in S:S.add(w);q.append(w)
    return S
def adjacency(edges):
    A=[set() for _ in range(N)]
    for z in edges:
        a,b=edgepair(z);A[a].add(b);A[b].add(a)
    return A
def triangles(A,edges):return sum(len(A[a]&A[b]) for a,b in map(edgepair,edges))//3

def atlas_graph(perms):
    G=PermutationGroup([Permutation(list(p)) for p in perms]);assert int(G.order())==118852315545600
    stab=G.stabilizer(0);subs=sorted([sorted(int(x) for x in o) for o in stab.orbits()],key=len)
    eighty=[o for o in subs if len(o)==80];assert eighty
    good=[];gens=perms+[inv(p) for p in perms]
    for o in eighty:
        edges=edge_orbit([(0,w) for w in o],gens)
        if len(edges)!=N*80//2:continue
        A=adjacency(edges)
        if {len(x) for x in A}!={80}:continue
        if triangles(A,edges)==582400:good.append((edges,A))
    assert len(good)==1,('degree-80 triality orbital not unique',len(good),[len(o) for o in subs])
    return good[0][0],good[0][1],[len(o) for o in subs]

def e8_graph():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();plus=[i for i,x in enumerate(parity) if x==0];minus=[i for i,x in enumerate(parity) if x==1]
    pp={v:i for i,v in enumerate(plus)};pm={v:i for i,v in enumerate(minus)};masks=[sum(1<<x for x in L) for L in leaves]
    edges=set()
    for j,v in enumerate(plus):
        b=1120+j
        for a in leaves[v]:edges.add(edgecode(a,b))
    for j,v in enumerate(minus):
        b=2240+j
        for a in leaves[v]:edges.add(edgecode(a,b))
    for v in plus:
        a=1120+pp[v]
        for w in minus:
            if (masks[v]&masks[w]).bit_count()==13:edges.add(edgecode(a,2240+pm[w]))
    assert len(edges)==N*80//2;A=adjacency(edges);assert {len(x) for x in A}=={80};assert triangles(A,edges)==582400
    return edges,A,[0]*1120+[1]*1120+[2]*1120

def type_coloring(A):
    # One chamber fixes the names of the three D4 triality types.  Incidence
    # propagation normally closes the entire connected building.
    a=0;b=next(iter(A[a]));c=next(iter(A[a]&A[b]));col=[-1]*N;col[a],col[b],col[c]=0,1,2
    changed=True
    while changed:
        changed=False
        for v in range(N):
            if col[v]>=0:continue
            s={col[w] for w in A[v] if col[w]>=0}
            if len(s)>=2:
                if len(s)!=2:raise AssertionError('not tripartite')
                col[v]=({0,1,2}-s).pop();changed=True
    if any(x<0 for x in col):
        raise AssertionError(f'type propagation stalled with {sum(x<0 for x in col)} uncolored vertices')
    assert Counter(col)=={0:1120,1:1120,2:1120}
    assert all(col[a]!=col[b] for a in range(N) for b in A[a])
    return col

def refine(A,B,la,lb):
    while True:
        def sigs(G,labs):
            return [(labs[v],tuple(sorted(Counter(labs[w] for w in G[v]).items()))) for v in range(N)]
        sa,sb=sigs(A,la),sigs(B,lb);un=sorted(set(sa)|set(sb),key=repr);code={s:i for i,s in enumerate(un)}
        na=[code[s] for s in sa];nb=[code[s] for s in sb]
        if Counter(na)!=Counter(nb):return None
        if na==la and nb==lb:return na,nb
        la,lb=na,nb

def explicit_iso(A,B,typesA,typesB,deadline):
    # Try all six triality type-name permutations.  Individualization/refinement
    # then chooses an explicit base.  The first successful branch is certified by
    # a complete edge check, so no canonicity is assumed.
    sys.setrecursionlimit(10000)
    def search(la,lb,nextmark):
        if time.monotonic()>deadline:raise TimeoutError('isomorphism search deadline')
        rr=refine(A,B,la,lb)
        if rr is None:return None
        la,lb=rr;cells=Counter(la)
        if max(cells.values())==1:
            pos={c:v for v,c in enumerate(lb)};f=[pos[c] for c in la]
            if all({f[w] for w in A[v]}==B[f[v]] for v in range(N)):return f
            return None
        labels=[c for c,n in cells.items() if n>1];c=min(labels,key=lambda x:cells[x]);av=next(v for v,x in enumerate(la) if x==c);cand=[v for v,x in enumerate(lb) if x==c]
        mark=max(max(la),max(lb))+1
        for bv in cand:
            nla=la.copy();nlb=lb.copy();nla[av]=mark;nlb[bv]=mark
            ans=search(nla,nlb,mark+1)
            if ans is not None:return ans
        return None
    for perm in itertools.permutations((0,1,2)):
        lb=[perm[x] for x in typesB]
        try:
            ans=search(typesA.copy(),lb,3)
        except TimeoutError:raise
        if ans is not None:return ans,perm
    return None,None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cache',type=Path,default=Path('.cache/atlas_o8p3_3360'));ap.add_argument('--seconds',type=int,default=900);args=ap.parse_args()
    blobs=[load(u,args.cache) for u in URLS];perms=[parse_cycles(x[0]) for x in blobs]
    ae,AA,subs=atlas_graph(perms);ee,EA,etypes=e8_graph();atypes=type_coloring(AA)
    f,tperm=explicit_iso(AA,EA,atypes,etypes,time.monotonic()+args.seconds);assert f is not None
    assert len(set(f))==N
    mapped={edgecode(f[a],f[b]) for a,b in map(edgepair,ae)};assert mapped==ee
    payload=','.join(map(str,f)).encode();out={'schema':'w33.pass7597_7604.explicit_3360_conjugacy.v1','status':'PASS','passes':'7597-7604','atlas_urls':URLS,'atlas_sha256':[x[1] for x in blobs],'atlas_subdegrees':subs,'vertices':3360,'edges':len(ae),'degree':80,'triangles':582400,'type_sizes':[1120,1120,1120],'triality_type_permutation':list(tperm),'atlas_to_e8_vertex_map':f,'map_sha256':hashlib.sha256(payload).hexdigest(),'theorem':'A literal 3360-entry graph isomorphism conjugates the canonical ATLAS O8+(3):S4 triality orbital graph to the independently reconstructed E8/3E8 point/+generator/-generator incidence graph. The previous external-name identification is therefore upgraded to an explicit coordinate identification.','claim_boundary':'Finite permutation/geometry theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','map_sha256':out['map_sha256'],'subdegrees':subs}))
if __name__=='__main__':main()
