#!/usr/bin/env python3
"""Reconstruct the 36/45 cubic-surface carriers from W(E6) involutions.

Independent classical verifier.  We use the Picard lattice of a cubic surface
with basis H,E1,...,E6 and intersection form diag(1,-1^6).  The 27 (-1)-curve
classes are E_i, H-E_i-E_j, and 2H-sum_{j!=i}E_j.  Six simple root
reflections generate W(E6) on these 27 lines.

Exact results.
  * |W(E6)| = 51840 and its determinant/sign kernel has order 25920.
  * The 891 nonidentity involutions split into four line-action signatures,
    of sizes 36,270,540,45, matching involution degrees 1,2,3,4.
  * Every one of the 36 reflections moves exactly the 12-line support of one
    double-six, and every double-six occurs once.
  * Every one of the 540 odd degree-3 involutions fixes exactly three cubic
    lines; those three form a tritangent.  Every tritangent has exactly 12 such
    involutions above it: 540 = 45*12.
  * Let F_T be the 12-element degree-3 involution fibre over a tritangent T,
    and r_D the reflection corresponding to double-six D.  Then

          |T cap D| = 0  iff  #{w in F_T : wr_D=r_Dw} = 4,
          |T cap D| = 2  iff  #{w in F_T : wr_D=r_Dw} = 0.

    Thus the W(E6) group law reconstructs the full 45x36 tritangent/double-six
    disjointness matrix: 540 disjoint pairs and 1080 two-line intersections.

This closes an independent loop with Pass 4659, which reconstructed the same
45x36 incidence from the W33 internal 27/36 carrier and obtained exactly the
same 0^540,2^1080 census.

Literature boundary: the involution degree census 1,36,270,540,45 is classical
(Carter; see also Dolgachev--Duncan, "Lines on cubic surfaces, Witt invariants
and Stiefel-Whitney classes", Section 3.2).  The objectwise double-six support,
12-to-1 tritangent fibre, and commutation reconstruction are the computations
certified here.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_e6_involution_reconstructs_double_six_tritangent.json"

# Picard intersection form in coordinates H,E1,...,E6.
Q = (1,-1,-1,-1,-1,-1,-1)


def dot(x,y):
    return sum(Q[i]*x[i]*y[i] for i in range(7))


def add(x,y,k=1):
    return tuple(x[i]+k*y[i] for i in range(7))


def compose(p,q):
    """Apply p, then q."""
    return tuple(q[p[i]] for i in range(len(p)))


def line_classes():
    out=[]; names=[]
    for i in range(6):
        v=[0]*7; v[1+i]=1; out.append(tuple(v)); names.append(f"E{i+1}")
    for i,j in itertools.combinations(range(6),2):
        v=[0]*7; v[0]=1; v[1+i]=-1; v[1+j]=-1
        out.append(tuple(v)); names.append(f"L{i+1}{j+1}")
    for i in range(6):
        v=[0]*7; v[0]=2
        for j in range(6):
            if j!=i: v[1+j]=-1
        out.append(tuple(v)); names.append(f"Q{i+1}")
    return out,names


def simple_roots():
    rr=[]
    for i in range(5):
        v=[0]*7; v[1+i]=1; v[2+i]=-1; rr.append(tuple(v))
    v=[0]*7; v[0]=1; v[1]=v[2]=v[3]=-1; rr.append(tuple(v))
    return rr


def build_weyl(lines):
    idx={v:i for i,v in enumerate(lines)}
    gens=[]
    for a in simple_roots():
        assert dot(a,a)==-2
        p=[]
        for x in lines:
            y=add(x,a,dot(x,a))  # s_a(x)=x+(x.a)a for a^2=-2
            p.append(idx[y])
        gens.append(tuple(p))
    ident=tuple(range(27)); sign={ident:1}; q=deque([ident])
    while q:
        x=q.popleft()
        for g in gens:
            z=compose(x,g); s=-sign[x]
            if z not in sign:
                sign[z]=s; q.append(z)
            else:
                assert sign[z]==s
    assert len(sign)==51840 and Counter(sign.values())==Counter({1:25920,-1:25920})
    return gens,sign


def carriers(lines):
    meet=[[0]*27 for _ in range(27)]
    for i,j in itertools.combinations(range(27),2):
        z=dot(lines[i],lines[j]); assert z in (0,1); meet[i][j]=meet[j][i]=z
    tri=[frozenset(c) for c in itertools.combinations(range(27),3)
         if meet[c[0]][c[1]] and meet[c[0]][c[2]] and meet[c[1]][c[2]]]
    assert len(tri)==45 and Counter(i for t in tri for i in t)==Counter({i:5 for i in range(27)})

    sixers=[]
    for c in itertools.combinations(range(27),6):
        if all(meet[i][j]==0 for i,j in itertools.combinations(c,2)):
            sixers.append(frozenset(c))
    assert len(sixers)==72
    double=[]; used=set()
    for i,S in enumerate(sixers):
        if i in used: continue
        cand=[]
        for j,T in enumerate(sixers):
            if j==i or S&T: continue
            if all(sum(meet[a][b] for b in T)==5 for a in S) and all(sum(meet[a][b] for a in S)==5 for b in T):
                cand.append(j)
        assert len(cand)==1
        j=cand[0]; used.update((i,j)); double.append(frozenset((S,sixers[j])))
    assert len(double)==36
    return meet,set(tri),set(double)


def act_set(S,p):
    return frozenset(p[i] for i in S)


def act_double(D,p):
    return frozenset(act_set(S,p) for S in D)


def main(write=True):
    lines,names=line_classes(); K=(-3,1,1,1,1,1,1)
    assert len(lines)==27 and all(dot(x,x)==-1 and dot(K,x)==-1 for x in lines)
    meet,tritangents,double_sixes=carriers(lines)
    gens,W=build_weyl(lines); ident=tuple(range(27))

    inv=[]
    for p,sgn in W.items():
        if p==ident or compose(p,p)!=ident: continue
        fixed_lines=sum(p[i]==i for i in range(27))
        fixed_tri=sum(act_set(t,p)==t for t in tritangents)
        fixed_ds=sum(act_double(d,p)==d for d in double_sixes)
        pointwise_tri=sum(all(p[i]==i for i in t) for t in tritangents)
        inv.append((sgn,fixed_lines,fixed_tri,fixed_ds,pointwise_tri,p))
    sig=Counter(x[:5] for x in inv)
    expected=Counter({
        (-1,15,15,16,15):36,
        ( 1, 7, 5, 8, 3):270,
        (-1, 3, 7, 4, 1):540,
        ( 1, 3,13,12, 1):45,
    })
    assert sig==expected and len(inv)==891

    # Degree-1 reflections <-> double-sixes by moved 12-line support.
    ds_by_support={frozenset().union(*D):D for D in double_sixes}; assert len(ds_by_support)==36
    reflections=[p for s,f,*_,p in inv if s==-1 and f==15]
    moved={p:frozenset(i for i in range(27) if p[i]!=i) for p in reflections}
    assert len(reflections)==36 and len(set(moved.values()))==36
    assert set(moved.values())==set(ds_by_support)
    refl_by_ds={S:p for p,S in moved.items()}

    # Degree-3 odd involutions -> tritangents by their pointwise fixed triple.
    degree3=[p for s,f,*_,p in inv if s==-1 and f==3]
    fibres=defaultdict(list)
    for p in degree3:
        T=frozenset(i for i in range(27) if p[i]==i)
        assert T in tritangents
        fibres[T].append(p)
    assert len(fibres)==45 and {len(v) for v in fibres.values()}=={12}

    # The commutation rule alone reconstructs the Pass-4659 45x36 cross-incidence.
    cross=Counter(); commuting=Counter()
    for T,F in fibres.items():
        for S,r in refl_by_ds.items():
            z=len(T&S); assert z in (0,2)
            c=sum(compose(w,r)==compose(r,w) for w in F)
            cross[z]+=1; commuting[(z,c)]+=1
            if z==0: assert c==4
            else: assert c==0
    assert cross==Counter({2:1080,0:540})
    assert commuting==Counter({(2,0):1080,(0,4):540})

    out={
      "schema":"w33.e6_involution_reconstructs_double_six_tritangent.v1",
      "status":"PASS",
      "headline":"The involution theory of W(E6) reconstructs the cubic 36/45 carriers and their cross-incidence. The 36 reflections move exactly the 36 double-six supports. The 540 odd degree-3 involutions fix tritangents in 45 fibres of size 12. A tritangent is disjoint from a double-six iff the corresponding reflection commutes with exactly four of the twelve degree-3 involutions above that tritangent; two-line intersections commute with none. The resulting census is 0^540 + 2^1080, exactly the independent Pass-4659 incidence matrix.",
      "weyl_group":{"order":len(W),"sign_kernel":25920,"generators":6},
      "classical_carriers":{"lines":27,"double_sixes":36,"tritangents":45,"sixers":72},
      "involution_signatures":{
        "degree1":{"class_size":36,"sign":-1,"fixed_lines":15,"fixed_tritangents":15,"fixed_double_sixes":16},
        "degree2":{"class_size":270,"sign":1,"fixed_lines":7,"fixed_tritangents":5,"fixed_double_sixes":8},
        "degree3":{"class_size":540,"sign":-1,"fixed_lines":3,"fixed_tritangents":7,"fixed_double_sixes":4},
        "degree4":{"class_size":45,"sign":1,"fixed_lines":3,"fixed_tritangents":13,"fixed_double_sixes":12}
      },
      "reflection_double_six_bridge":{"reflections":36,"moved_lines_each":12,"bijection_to_double_sixes":True},
      "degree3_tritangent_bridge":{"degree3_involutions":540,"tritangent_fibres":45,"fibre_size":12,"fixed_lines_form_tritangent":True},
      "group_law_cross_incidence":{"rule_disjoint":"exactly 4 of the 12 fibre involutions commute with r_D","rule_two_line":"0 of the 12 commute with r_D","disjoint_pairs":540,"two_line_pairs":1080,"identity":"45*36=540+1080"},
      "repo_crosscheck":"Pass4659 independently reconstructs T^T R = 2(J-D), with triangle/double-six line-intersection census 0^540,2^1080.",
      "literature":[
        "Carter, Conjugacy classes in the Weyl group",
        "Dolgachev-Duncan, Lines on cubic surfaces, Witt invariants and Stiefel-Whitney classes, Sec. 3.2: E6 involution degrees 0..4 with counts 1,36,270,540,45",
        "Classical cubic-surface geometry: 27 lines, 36 double-sixes, 45 tritangents"
      ],
      "boundary":"Exact finite Weyl-group/cubic-surface theorem. The identification with W33/Suzuki carriers uses separately certified equivariant intertwiners; no physical E6 gauge field or dynamical involution is inferred.",
      "checks":{"W_E6_51840":True,"involution_census":True,"reflection_double_six_bijection":True,"degree3_12_to_1_tritangent_cover":True,"commutation_recovers_45x36_incidence":True}
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2)); return out


if __name__=="__main__": main(True)
