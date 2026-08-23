"""Passes 9041-9052 -- Golay/tetracode glue bifurcation above A2^12.

Starting from the quotient-zero A2^12 root subsystem found in Pass 9029-9040 inside
N(E6^4), this verifier places N(E6^4) and N(A2^12) over the same A2^12
discriminant space and compares their ternary self-dual glue codes.

The result explains both the different Niemeier root systems and the E6 line shadow.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sympy import Matrix, zeros

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass9029_9040_root_shadow_trichotomy as rs  # noqa: E402

OUT = ROOT / "data" / "PART_W33_PASS9041_9052_GOLAY_TETRACODE_GLUE_BIFURCATION.json"


def rref_basis(a, p=3):
    a = np.array(a, dtype=np.int64) % p
    m,n=a.shape
    r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if int(a[i,c])%p),None)
        if piv is None:
            continue
        a[[r,piv]]=a[[piv,r]]
        a[r]=(a[r]*pow(int(a[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and a[i,c]%p:
                a[i]=(a[i]-a[i,c]*a[r])%p
        r+=1
        if r==m:
            break
    return a[:r]


def span_words(g):
    g=np.array(g,dtype=np.int64)%3
    return {
        tuple((np.array(c,dtype=np.int64)@g)%3)
        for c in itertools.product(range(3),repeat=g.shape[0])
    }


def weight_enum(words):
    return Counter(sum(int(x)!=0 for x in w) for w in words)


def build_e6_carrier():
    E6=rs.E6
    w=Matrix(np.loadtxt(ROOT/"analysis"/"_e6_ord9.txt",dtype=np.int64).tolist())
    b=Matrix(np.loadtxt(ROOT/"analysis"/"_niemeier_e6_4_basis.txt",dtype=np.int64).tolist())
    gram=Matrix(np.loadtxt(ROOT/"analysis"/"_niemeier_e6_4_gram.txt",dtype=np.int64).tolist())
    mz=E6*w*E6.inv()
    a=zeros(24)
    for k in range(4):
        a[6*k:6*k+6,6*k:6*k+6]=mz
    x=b.T.inv()*a*b.T
    h,j=rs.quotient_form(x,gram)
    return E6,b,gram,x,h,j


def zero_root_a2_basis(E6,b,gram,h):
    roots6=rs.e6_roots()
    binv=b.T.inv()
    g=np.array(gram.tolist(),dtype=np.int64)
    a2basis=[]
    block_root_counts=[]
    for comp in range(4):
        zr=[]
        for rv in roots6:
            amb=zeros(24,1)
            amb[6*comp:6*comp+6,0]=E6*Matrix(rv)
            z=binv*amb
            zv=np.array([int(v) for v in z],dtype=np.int64)
            if not ((h@(zv%3))%3).any():
                zr.append(zv)
        assert len(zr)==18

        adj={i:set() for i in range(18)}
        for i,u in enumerate(zr):
            for k,v in enumerate(zr[i+1:],i+1):
                if int(u@g@v)!=0:
                    adj[i].add(k); adj[k].add(i)
        seen=set(); comps=[]
        for i in range(18):
            if i in seen:
                continue
            todo=[i];seen.add(i);ids=[]
            while todo:
                u=todo.pop();ids.append(u)
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v);todo.append(v)
            comps.append(ids)
        assert sorted(map(len,comps))==[6,6,6]

        for ids in comps:
            rootset=[zr[i] for i in ids]
            target={tuple(v) for v in rootset}
            pair=None
            for aa,bb in itertools.permutations(rootset,2):
                if int(aa@g@bb)==-1:
                    gen={tuple(aa),tuple(-aa),tuple(bb),tuple(-bb),
                         tuple(aa+bb),tuple(-(aa+bb))}
                    if gen==target:
                        pair=(aa,bb)
                        break
            assert pair is not None
            a2basis.extend(pair)
        block_root_counts.append(len(zr))

    s=Matrix(np.column_stack(a2basis).tolist())
    assert abs(int(s.det()))==729
    ga2=s.T*gram*s
    target=Matrix.diag(*([rs.A2]*12))
    assert ga2==target
    return s,block_root_counts


def discr_symbol(pair):
    """A2*/A2 class in the simple-root basis: c*(2,1)/3 mod Z^2."""
    nums=[int(3*v)%3 for v in pair]
    for c in range(3):
        if nums==[(2*c)%3,c%3]:
            return c
    raise AssertionError(f"not in A2*: {pair} -> {nums}")


def e6_glue_code(s):
    t=s.inv()
    generators=[]
    for j in range(24):
        word=[]
        for k in range(12):
            word.append(discr_symbol([t[2*k,j],t[2*k+1,j]]))
        generators.append(word)
    g=rref_basis(np.array(generators,dtype=np.int64),3)
    assert g.shape==(6,12)
    assert not ((g@g.T)%3).any()
    words=span_words(g)
    assert len(words)==729
    return g,words


def local_weight3_split(words):
    w3=sorted(w for w in words if sum(int(x)!=0 for x in w)==3)
    assert len(w3)==8
    supports=Counter(tuple(i for i,x in enumerate(w) if x) for w in w3)
    assert sorted(supports.values())==[2,2,2,2]
    supp=sorted(supports)
    assert supp==[(0,1,2),(3,4,5),(6,7,8),(9,10,11)]

    us=[]
    for block in supp:
        w=next(w for w in w3 if tuple(i for i,x in enumerate(w) if x)==block)
        u=np.array([w[i] for i in block],dtype=np.int64)%3
        u=(u*pow(int(next(x for x in u if x)), -1, 3))%3
        us.append(u)

    U=np.zeros((4,12),dtype=np.int64)
    for b,u in enumerate(us):
        U[b,3*b:3*b+3]=u
    assert rs.rank_modp(U,3)==4
    uwords=span_words(U)
    assert len(uwords)==81

    block_maps=[]
    for u in us:
        local=[np.array(v,dtype=np.int64) for v in itertools.product(range(3),repeat=3)
               if int(np.dot(v,u))%3==0]
        v=next(x for x in local if any(x) and rs.rank_modp(np.vstack([u,x]),3)==2)
        m={}
        for a in range(3):
            for b in range(3):
                m[tuple((a*u+b*v)%3)]=b
        assert len(m)==9
        block_maps.append(m)

    qwords=set()
    for w in words:
        q=[]
        for b in range(4):
            tri=tuple(int(x) for x in w[3*b:3*b+3])
            assert tri in block_maps[b]
            q.append(block_maps[b][tri])
        qwords.add(tuple(q))
    qg=rref_basis(np.array(list(qwords),dtype=np.int64),3)
    assert qg.shape==(2,4)
    assert not ((qg@qg.T)%3).any()
    assert len(qwords)==9
    assert weight_enum(qwords)==Counter({3:8,0:1})
    return w3,supp,U,uwords,qg,qwords


def main():
    E6,b,gram,x,h,j=build_e6_carrier()
    s,block_root_counts=zero_root_a2_basis(E6,b,gram,h)
    g_e6,words_e6=e6_glue_code(s)
    we_e6=weight_enum(words_e6)
    assert we_e6==Counter({9:464,6:240,12:16,3:8,0:1})
    w3,supp,U,uwords,qg,qwords=local_weight3_split(words_e6)

    words_golay=rs.golay_codewords()
    we_golay=weight_enum(words_golay)
    assert we_golay==Counter({9:440,6:264,12:24,0:1})

    added=8*27
    assert 72+added==288

    out={
      "theorem":"A2^12 Glue-Code Bifurcation and E6 Line-Shadow Mechanism",
      "boundary":(
        "VERIFIED after choosing the quotient-zero A2^12 root subsystem inside N(E6^4). "
        "Relative to this common A2^12 root lattice, N(E6^4) is encoded by a self-dual "
        "ternary [12,6,3] glue code with exactly eight weight-3 words, while N(A2^12) "
        "uses the extended ternary Golay [12,6,6] code and has no weight-3 words. The "
        "eight E6-code weight-3 words occur as four +/- pairs on four disjoint triples. "
        "Their local span has dimension 4 and the residual quotient is the [4,2,3] "
        "tetracode. This explains 72 + 8*27 = 288 E6^4 roots and the 54-root fibre over "
        "each of the four W33 line points. No physics claim is made."
      ),
      "common_root_lattice":{
        "type":"A2^12","rank":24,"determinant":3**12,
        "index_in_each_unimodular_overlattice":729
      },
      "N(A2^12)_Golay_glue":{
        "parameters":"[12,6,6]_3","size":729,"self_dual":True,
        "weight_enumerator":{str(k):int(v) for k,v in sorted(we_golay.items())},
        "weight3_words":0,"root_effect":"no new norm-2 vectors; roots remain A2^12 (72)"
      },
      "N(E6^4)_relative_glue":{
        "parameters":"[12,6,3]_3","size":729,"self_dual":True,
        "generator_rref":g_e6.tolist(),
        "weight_enumerator":{str(k):int(v) for k,v in sorted(we_e6.items())},
        "weight3_words":8,
        "weight3_supports":[list(x) for x in supp],
        "local_extension_subcode":{"dimension":4,"size":81,
          "description":"four disjoint isotropic weight-3 glue lines, one A2^3 -> E6 extension per block"},
        "quotient_code":{"parameters":"[4,2,3]_3","size":9,"self_dual":True,
          "generator_rref":qg.tolist(),"weight_enumerator":{"0":1,"3":8},
          "identification":"tetracode"},
      },
      "root_count_explanation":{
        "base_A2^12_roots":72,
        "weight3_glue_words":8,
        "minimal_vectors_per_weight3_coset":27,
        "added_roots":216,
        "total":288,
        "per_W33_line_point":"two +/- weight-3 words * 27 roots = 54",
        "kernel_per_E6_block":"A2^3 has 18 roots"
      },
      "bridge_to_pass9029_9040":{
        "four_disjoint_weight3_supports":"the four visible W33 line channels",
        "E6_zero_root_system":"A2^12",
        "visible_E6_roots":"4 * 54 = 216"
      }
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
