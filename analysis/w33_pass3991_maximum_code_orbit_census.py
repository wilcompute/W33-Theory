#!/usr/bin/env python3
"""Pass 3991: exact maximum-code orbit census in the fixed [36,6,16] parent problem."""
from __future__ import annotations
import hashlib, itertools, json, time
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = 57

def bits(x,n=6): return [(x>>i)&1 for i in range(n)]
def qform(x):
    b=bits(x)
    return (b[0]*b[1]+b[2]*b[3]+b[4]*b[5]+b[4]+b[5])&1
def beta(x,y): return qform(x^y)^qform(x)^qform(y)

def gf2_basis(values):
    piv={}
    for value in values:
        x=int(value)
        while x:
            p=x.bit_length()-1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p]=x
                for pp in list(piv):
                    if pp!=p and ((piv[pp]>>p)&1):
                        piv[pp] ^= x
                break
    return [piv[p] for p in sorted(piv,reverse=True)]

def build_graph():
    nonsingular=[x for x in range(1,64) if qform(x)]
    assert len(nonsingular)==36
    parent=[]
    for label in range(64):
        w=0
        for i,x in enumerate(nonsingular):
            if beta(label,x):
                w |= 1<<i
        parent.append(w)
    base=gf2_basis(parent)
    assert len(base)==6
    words=[]
    for support in itertools.combinations(range(36),4):
        w=sum(1<<i for i in support)
        if all(((w&b).bit_count()&1)==0 for b in base):
            words.append(w)
    assert len(words)==945
    adj=[0]*len(words)
    for i,wi in enumerate(words):
        for j in range(i+1,len(words)):
            if ((wi&words[j]).bit_count()&1)==0:
                adj[i] |= 1<<j
                adj[j] |= 1<<i
    assert set(x.bit_count() for x in adj)=={624}
    return nonsingular,words,adj

def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))

def coordinate_generators(nonsingular):
    index={x:i for i,x in enumerate(nonsingular)}
    out=[]
    for v in nonsingular:
        p=[]
        for x in nonsingular:
            y=x ^ (v if beta(x,v) else 0)
            assert qform(y)==1
            p.append(index[y])
        out.append(tuple(p))
    return out

def generate_group(gens):
    ident=tuple(range(len(gens[0])))
    seen={ident}; queue=deque([ident])
    while queue:
        h=queue.popleft()
        for g in gens:
            x=compose(g,h)
            if x not in seen:
                seen.add(x); queue.append(x)
    return seen

def permute_word(w,p):
    out=0
    while w:
        b=w&-w; i=b.bit_length()-1
        out |= 1<<p[i]
        w ^= b
    return out

def induced_word_generators(words,coord_gens):
    index={w:i for i,w in enumerate(words)}
    return [tuple(index[permute_word(w,p)] for w in words) for p in coord_gens]

def orbit_point(start,gens):
    seen={start}; queue=deque([start])
    while queue:
        x=queue.popleft()
        for g in gens:
            y=g[x]
            if y not in seen:
                seen.add(y); queue.append(y)
    return seen

def color_sort(P,adj):
    order=[]; bounds=[]; color=0; U=P
    while U:
        color+=1; Q=U
        while Q:
            bit=Q&-Q; v=bit.bit_length()-1
            U ^= bit
            Q &= ~bit
            Q &= ~adj[v]
            order.append(v); bounds.append(color)
    return order,bounds

def enumerate_with_anchor(anchor,adj,orbit135,target=TARGET):
    solutions=[]; nodes=0
    def expand(clique,P):
        nonlocal nodes
        nodes+=1
        if len(clique)==target:
            solutions.append(tuple(sorted(clique)))
            return
        if P.bit_count()<target-len(clique):
            return
        order,bounds=color_sort(P,adj)
        for idx in range(len(order)-1,-1,-1):
            if len(clique)+bounds[idx]<target:
                return
            v=order[idx]; bit=1<<v
            if not (P&bit):
                continue
            expand(clique+[v],P&adj[v])
            P ^= bit
            if P.bit_count()<target-len(clique):
                return
    expand([anchor],adj[anchor])
    return solutions,nodes

def orbit_clique(start,gens):
    start=tuple(sorted(start))
    seen={start}; queue=deque([start])
    while queue:
        c=queue.popleft()
        for g in gens:
            y=tuple(sorted(g[i] for i in c))
            if y not in seen:
                seen.add(y); queue.append(y)
    return seen

def support_sha(clique,words):
    return hashlib.sha256(
        "\n".join(f"{words[i]:09x}" for i in sorted(clique)).encode()
    ).hexdigest()

def main():
    started=time.time()
    nonsingular,words,adj=build_graph()
    cgens=coordinate_generators(nonsingular)
    group=generate_group(cgens)
    assert len(group)==51840
    wgens=induced_word_generators(words,cgens)
    orbit_a=orbit_point(0,wgens)
    unseen=set(range(945))-orbit_a
    orbit_b=orbit_point(next(iter(unseen)),wgens)
    vertex_orbits=sorted([orbit_a,orbit_b],key=len)
    assert [len(x) for x in vertex_orbits]==[135,810]
    orbit135,orbit810=vertex_orbits
    anchor=min(orbit135)
    solutions,nodes=enumerate_with_anchor(anchor,adj,orbit135)
    composition=Counter(len(set(c)&orbit135) for c in solutions)
    assert composition==Counter({3:12,15:45})
    total_by_composition={
        str(r): 135*count//r for r,count in sorted(composition.items())
    }
    assert total_by_composition=={"3":540,"15":405}
    reps={}
    c3=next(c for c in solutions if len(set(c)&orbit135)==3)
    o3=orbit_clique(c3,wgens)
    assert len(o3)==540
    reps["orbit_540"]=c3
    c15a=next(c for c in solutions if len(set(c)&orbit135)==15)
    o15a=orbit_clique(c15a,wgens)
    assert len(o15a)==270
    c15b=next(c for c in solutions if len(set(c)&orbit135)==15 and c not in o15a)
    o15b=orbit_clique(c15b,wgens)
    assert len(o15b)==135
    assert not (o3&o15a or o3&o15b or o15a&o15b)
    anchored_partition=Counter()
    for c in solutions:
        if c in o3: anchored_partition["orbit_540"]+=1
        elif c in o15a: anchored_partition["orbit_270"]+=1
        elif c in o15b: anchored_partition["orbit_135"]+=1
        else: raise AssertionError("unclassified anchored maximum clique")
    assert anchored_partition==Counter({"orbit_540":12,"orbit_270":30,"orbit_135":15})
    orbit_records=[]
    for name,orb,rep in [
        ("orbit_540",o3,c3),("orbit_270",o15a,c15a),("orbit_135",o15b,c15b)
    ]:
        r=len(set(rep)&orbit135)
        orbit_records.append({
            "name":name,
            "orbit_size":len(orb),
            "parent_group_stabilizer_order":51840//len(orb),
            "vertex_orbit_composition":{"135_orbit":r,"810_orbit":57-r},
            "anchored_solutions":anchored_partition[name],
            "representative_support_sha256":support_sha(rep,words),
        })
    result={
        "schema":"w33.pass3991.maximum_code_orbit_census.v1",
        "status":"PASS_EXACT_THREE_MAXIMUM_CODE_ORBITS",
        "parent_group_order":51840,
        "compatibility_graph":{"vertices":945,"degree":624,"maximum_clique_size":57},
        "weight4_vertex_orbits":[135,810],
        "fixed_anchor":anchor,
        "anchored_maximum_cliques":len(solutions),
        "anchored_composition":dict(sorted(composition.items())),
        "search_nodes":nodes,
        "total_maximum_cliques":945,
        "total_by_135_orbit_composition":total_by_composition,
        "maximum_code_orbits":orbit_records,
        "correction":"The order-192 full coordinate stabilizer cannot be divided directly into the parent-group order. In the parent-preserving group the three maximum-code stabilizers have orders 96, 192, and 384.",
        "boundary":"Exact for maximum doubly-even self-orthogonal extensions in the fixed 945-vertex compatibility graph containing the fixed [36,6,16] parent. It does not classify length-36 codes outside this parent-extension problem.",
        "seconds":time.time()-started,
    }
    payload={k:v for k,v in result.items() if k!="seconds"}
    result["semantic_sha256"]=hashlib.sha256(
        json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
    ).hexdigest()
    out=ROOT/"data/PART_3991_MAXIMUM_CODE_ORBIT_CENSUS.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS_MAXIMUM_CODE_ORBITS",result["total_maximum_cliques"],
          [x["orbit_size"] for x in orbit_records],result["semantic_sha256"])
if __name__=="__main__":
    main()
