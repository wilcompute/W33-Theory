#!/usr/bin/env python3
"""Pass5608: identify the old s12/Golay projective weight-12 shell.

The old s12 corpus projectivizes the 728 nonzero ternary Golay words to the 364
points of a projective 5-space-sized shell, with weight distribution 132+220+12.
This pass asks the decisive action-level question: is that final 12-set the new
576 Reye/Latin/F4 12-set?

Answer: no. Rebuild the ATLAS natural M12 generators, transport them into the
repo Golay coordinates through the Steiner S(5,6,12) design, find the required
monomial sign lifts, and induce their action on the twelve projective weight-12
Golay lines. The generated image has order 95040 and orbital sizes 12,132: it
is the natural 2-transitive M12 12-point action, not the rank-3 order-576 action.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from collections import deque
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5608_S12_GOLAY_WEIGHT12_M12_ACTION.json'
GEN=[
[1,0,0,0,0,0,0,1,1,1,1,1],
[0,1,0,0,0,0,1,0,1,2,2,1],
[0,0,1,0,0,0,1,1,0,1,2,2],
[0,0,0,1,0,0,1,2,1,0,1,2],
[0,0,0,0,1,0,1,2,2,1,0,1],
[0,0,0,0,0,1,1,1,2,2,1,0],
]

def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return tuple(q)
def perm_from_cycles(n,cycles):
    p=list(range(n))
    for cyc1 in cycles:
      cyc=[x-1 for x in cyc1]
      for a,b in zip(cyc,cyc[1:]+cyc[:1]): p[a]=b
    return tuple(p)
def codewords():
    out=[]
    for c in itertools.product(range(3),repeat=6):
      w=[]
      for j in range(12): w.append(sum(c[i]*GEN[i][j] for i in range(6))%3)
      out.append(tuple(w))
    return out
def subset_orbit(seed,gens):
    seen={tuple(sorted(seed))}; stack=list(seen)
    while stack:
      S=stack.pop()
      for g in gens:
        T=tuple(sorted(g[i] for i in S))
        if T not in seen: seen.add(T); stack.append(T)
    return seen
def incidence_graph(hexads,prefix):
    G=nx.Graph()
    for i in range(12): G.add_node((prefix,'p',i),kind='p')
    for b,H in enumerate(hexads):
      bn=(prefix,'b',b); G.add_node(bn,kind='b')
      for i in H: G.add_edge((prefix,'p',i),bn)
    return G
def act_perm(w,p):
    out=[0]*12
    for i,j in enumerate(p): out[j]=w[i]
    return tuple(out)
def act_monomial(w,p,s):
    x=act_perm(w,p); return tuple(s[i]*x[i]%3 for i in range(12))
def canon(w):
    z=tuple(2*x%3 for x in w); return min(tuple(w),z)
def find_sign(p,rows,code_set):
    for mask in range(1<<12):
      s=tuple(2 if (mask>>i)&1 else 1 for i in range(12))
      if all(act_monomial(r,p,s) in code_set for r in rows): return s
    raise AssertionError('no monomial sign lift')
def closure(gens):
    e=tuple(range(len(gens[0]))); allgens=list(gens)+[inv(g) for g in gens]
    seen={e}; dq=deque([e])
    while dq:
      x=dq.popleft()
      for g in allgens:
        y=compose(g,x)
        if y not in seen: seen.add(y); dq.append(y)
    return seen
def orbital_sizes(G,n):
    seen=set(); ans=[]
    for i in range(n):
      for j in range(n):
        if (i,j) in seen: continue
        o={(g[i],g[j]) for g in G}; seen|=o; ans.append(len(o))
    return sorted(ans)

def main():
    code=codewords(); C=set(code); assert len(C)==729
    wd={w:sum(x!=0 for x in w) for w in code}
    proj={canon(w) for w in code if any(w)}
    pweights={d:sum(1 for w in proj if sum(x!=0 for x in w)==d) for d in (6,9,12)}
    assert pweights=={6:132,9:220,12:12}

    b11=perm_from_cycles(12,[[1,4],[3,10],[5,11],[6,12]])
    b21=perm_from_cycles(12,[[1,8,9],[2,3,4],[5,12,11],[6,10,7]])
    gens=[b11,b21,inv(b11),inv(b21)]
    hexA=None
    for S in itertools.combinations(range(12),6):
      o=subset_orbit(S,gens)
      if len(o)==132: hexA=sorted(o); break
    assert hexA is not None
    hexC=sorted({tuple(i for i,x in enumerate(w) if x) for w in code if wd[w]==6})
    GA=incidence_graph(hexA,'A'); GC=incidence_graph(hexC,'C')
    GM=nx.algorithms.isomorphism.GraphMatcher(GA,GC,node_match=lambda a,b:a['kind']==b['kind'])
    assert GM.is_isomorphic(); mp=GM.mapping
    pi=tuple(mp[('A','p',i)][2] for i in range(12)); ipi=inv(pi)
    conj=lambda g: compose(pi,compose(g,ipi))
    c11,c21=conj(b11),conj(b21)
    rows=[tuple(r) for r in GEN]
    s11=find_sign(c11,rows,C); s21=find_sign(c21,rows,C)
    shell=sorted(w for w in proj if sum(x!=0 for x in w)==12); si={w:i for i,w in enumerate(shell)}
    def induced(p,s): return tuple(si[canon(act_monomial(w,p,s))] for w in shell)
    g11,g21=induced(c11,s11),induced(c21,s21)
    G12=closure([g11,g21])
    assert len(G12)==95040
    orbs=orbital_sizes(G12,12); assert orbs==[12,132]
    out={
      'pass':5608,'status':'WEIGHT12_SHELL_IS_NATURAL_M12_ACTION_NOT_REYE576',
      'projective_Golay_shell_size':len(proj),'projective_weight_distribution':pweights,
      'weight12_projective_lines':12,
      'atlas_to_repo_coordinate_map':list(pi),
      'monomial_sign_lift_b11':list(s11),'monomial_sign_lift_b21':list(s21),
      'induced_weight12_generators':[list(g11),list(g21)],
      'induced_group_order':len(G12),'orbital_sizes':orbs,
      'comparison':{'M12_order':95040,'Reye_Latin_F4_order':576,'Reye_Latin_F4_orbitals':[12,36,96]},
      'theorem':'The distinguished 12 projective weight-12 ternary Golay lines carry the natural 2-transitive M12 degree-12 action. They are not the recent rank-3 Reye/Latin/F4 12-point action.',
      'group_theory_firewall':'ATLAS lists the maximal subgroups of M12; none has order divisible by 576, so M12 has no subgroup of order 576. The non-identification is structural, not merely different measured generators.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
