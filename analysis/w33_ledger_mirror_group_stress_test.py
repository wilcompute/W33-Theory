#!/usr/bin/env python3
"""Exact finite mirror-group stress test for the Ledger/W33 bridge.

This is a geometric analogue of the Ledger slogan "mirrors generate symmetry".
It does NOT identify these anti-symplectic involutions with Tomita modular
conjugations. It asks the finite group-theoretic question that W33 can answer
exactly: close a PSp(4,3)-conjugacy class of anti-symplectic involutions.

Result: the mirror class has 540 elements; eight mirrors generate order 51840;
even mirror products generate exactly PSp(4,3), order 25920.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
MOD=3

def canon(v):
    v=tuple(x%MOD for x in v)
    for a in v:
        if a:
            inv=1 if a==1 else 2
            return tuple((inv*x)%MOD for x in v)
    raise ValueError("zero vector")
def symp(u,v): return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%MOD
POINTS=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
INDEX={p:i for i,p in enumerate(POINTS)}
ID=tuple(range(40))
def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def invperm(a):
    b=[0]*len(a)
    for i,j in enumerate(a): b[j]=i
    return tuple(b)
def transvection(v):
    out=[]
    for x in POINTS:
        w=symp(x,v); y=tuple((x[i]+w*v[i])%3 for i in range(4))
        out.append(INDEX[canon(y)])
    return tuple(out)
def base_mirror_perm():
    return tuple(INDEX[canon((x[0],x[1],(-x[2])%3,(-x[3])%3))] for x in POINTS)
def closure(gens,limit=60000):
    seen={ID}; stack=[ID]
    while stack:
        g=stack.pop()
        for h in gens:
            z=compose(h,g)
            if z not in seen:
                seen.add(z); stack.append(z)
                if len(seen)>limit: raise RuntimeError("group exceeded limit")
    return seen
def greedy_psp_generators():
    selected=[]; indices=[]; group={ID}; growth=[]
    for i,t in enumerate([transvection(v) for v in POINTS]):
        trial=closure(selected+[t],30000)
        if len(trial)>len(group):
            selected.append(t); indices.append(i); group=trial; growth.append(len(group))
        if len(group)==25920: break
    return selected,indices,group,growth
def main():
    edges=sum(symp(POINTS[i],POINTS[j])==0 for i in range(40) for j in range(i+1,40))
    R=base_mirror_perm()
    psp_gens,psp_indices,psp,psp_growth=greedy_psp_generators()
    mirrors={compose(compose(g,R),invperm(g)) for g in psp}
    mg=[]; G={ID}; growth=[]
    for m in sorted(mirrors):
        trial=closure(mg+[m],60000)
        if len(trial)>len(G): mg.append(m); G=trial; growth.append(len(G))
        if len(G)==51840: break
    even=closure([compose(a,b) for a in mg for b in mg],30000)
    fixed={sum(m[i]==i for i in range(40)) for m in mirrors}
    centralizer=len(psp)//len(mirrors)
    checks={
      "w33_points_40":len(POINTS)==40,"w33_edges_240":edges==240,
      "base_mirror_involution":compose(R,R)==ID,"psp_order_25920":len(psp)==25920,
      "psp_five_transvection_generators":len(psp_gens)==5,"mirror_class_540":len(mirrors)==540,
      "mirror_class_all_involutions":all(compose(m,m)==ID for m in mirrors),
      "mirror_fixed_points_uniform_8":fixed=={8},"mirror_centralizer_48":centralizer==48,
      "mirrors_generate_51840":len(G)==51840,"mirror_generators_needed_8":len(mg)==8,
      "even_mirror_products_generate_25920":len(even)==25920,
      "even_group_equals_psp":even==psp,"index_two":len(G)==2*len(even)}
    checks={k:bool(v) for k,v in checks.items()}; assert all(checks.values()),checks
    out={"schema":"w33.ledger.mirror-group-stress.v1","status":"PASS_GEOMETRIC_MIRROR_DOUBLE_COVER",
      "w33":{"points":40,"edges":240},
      "base_mirror":{"matrix":"diag(1,1,-1,-1) over F3","identity":"R^T Omega R = -Omega, R^2=I","projective_fixed_points":8},
      "psp":{"order":len(psp),"generator_point_indices":psp_indices,
             "generator_projective_vectors":[list(POINTS[i]) for i in psp_indices],"greedy_growth":psp_growth},
      "mirror_conjugacy_class":{"size":len(mirrors),"centralizer_order_in_psp":centralizer,"fixed_point_counts":sorted(fixed)},
      "mirror_generated_group":{"order":len(G),"greedy_mirror_generator_count":len(mg),"growth":growth,
                                "identification":"PGSp(4,3)=PSp(4,3):2, same order as W(E6)"},
      "even_mirror_products":{"order":len(even),"equals_psp_permutation_group":True,"identification":"PSp(4,3)"},
      "boundary":["These are exact anti-symplectic geometric mirrors of the W33 carrier.",
                  "No equality with Tomita-Takesaki modular conjugations J_A is claimed here.",
                  "Odd mirrors extend the symplectic group and even mirror products recover its orientation-preserving core."],
      "checks":checks}
    p=Path("data/PART_LEDGER_MIRROR_GROUP_STRESS_TEST.json"); p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); print(json.dumps(out,indent=2,sort_keys=True)); return out
if __name__=="__main__": main()
