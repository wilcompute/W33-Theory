#!/usr/bin/env python3
"""Exact ambient lifting audit of three *previously selected* automorphisms.

The order-2/3 maps were found abstractly by a graph matcher. Nothing here
assumes that they generate A5 or even lift to the ambient polar geometry.
"""
import itertools,json,sys
from pathlib import Path
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from symmetric_fast import fast_build
from symmetric_even_sets_gf import setup
OUT=ROOT/"data/w33_20261031_same_subgroup_ambient_lift_audit.json"

def build():
    points,lines=fast_build(9)
    selected=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())["results"][0]["chosen"]
    old=json.loads((ROOT/"data/w33_20261031_torsion_order5_probe.json").read_text())
    F,add,mul,inv,neg=setup(9)
    sumf=lambda xs:__import__("functools").reduce(lambda a,b:add[a][b],xs,0)
    def fm(x,p):return x if p==1 else mul[mul[x][x]][x]
    def norm(x):
        z=inv[next(z for z in x if z)]
        return tuple(mul[z][y] for y in x)
    def det_inverse(A):
        w=[A[i][:]+[int(i==j)for j in range(4)]for i in range(4)]
        for col in range(4):
            k=next((r for r in range(col,4)if w[r][col]),None)
            if k is None:return None
            w[col],w[k]=w[k],w[col]
            invpivot=inv[w[col][col]]
            w[col]=[mul[invpivot][z]for z in w[col]]
            for row in range(4):
                if row!=col and w[row][col]:
                    a=w[row][col]
                    w[row]=[add[w[row][j]][neg[mul[a][w[col][j]]]]for j in range(8)]
        return [v[4:]for v in w]
    def product(A,B):
        return [[sumf(mul[A[i][k]][B[k][j]]for k in range(4))for j in range(len(B[0]))]for i in range(len(A))]
    def polar(u,v):
        return sumf([mul[u[0]][v[2]],mul[u[1]][v[3]],neg[mul[u[2]][v[0]]],neg[mul[u[3]][v[1]]]])
    cover={}
    for i,j in enumerate(selected):
        for p in lines[j]:cover.setdefault(p,[]).append(i)
    assert len(cover)==240 and all(len(v)==2 for v in cover.values())
    bypair={tuple(sorted(v)):p for p,v in cover.items()}
    assert len(bypair)==240
    basis=[]
    def rank(rows):
        z=[list(row)for row in rows];r=0
        for j in range(4):
            k=next((k for k in range(r,len(z))if z[k][j]),None)
            if k is None:continue
            z[r],z[k]=z[k],z[r]
            a=inv[z[r][j]];z[r]=[mul[a][t]for t in z[r]]
            for k in range(len(z)):
                if k!=r and z[k][j]:
                    a=z[k][j]
                    z[k]=[add[z[k][i]][neg[mul[a][z[r][i]]]]for i in range(4)]
            r+=1
        return r
    for p in sorted(cover):
        if rank([points[b]for b in basis]+[points[p]])>len(basis):basis.append(p)
        if len(basis)==4:break
    assert len(basis)==4
    point_index={tuple(x):j for j,x in enumerate(points)}
    all_lines={frozenset(x)for x in lines}
    checks={}
    certified={}
    for order in (2,3,5):
        g=old["other_orders"][str(order)]["mapping"]
        assert sorted(g)==list(range(48))
        mapped={p:bypair[tuple(sorted(g[i]for i in pair))]for p,pair in cover.items()}
        y=[points[mapped[p]]for p in basis]
        answer=None;trials=0
        for power in (1,3):
            col=[[fm(points[p][i],power)for p in basis]for i in range(4)]
            ci=det_inverse(col)
            if ci is None:continue
            for ds in itertools.product(F[1:],repeat=3):
                trials+=1
                scales=(1,)+ds
                m=product([[mul[y[j][i]][scales[j]]for j in range(4)]for i in range(4)],ci)
                def image(v):
                    x=[fm(t,power)for t in v]
                    return norm([sumf(mul[m[i][k]][x[k]]for k in range(4))for i in range(4)])
                if any(image(points[p])!=tuple(points[mapped[p]])for p in list(sorted(mapped))[:12]):continue
                if any(image(points[p])!=tuple(points[q])for p,q in mapped.items()):continue
                cols=[[m[i][j]for i in range(4)]for j in range(4)]
                ee=[[int(i==j)for i in range(4)]for j in range(4)]
                mu=polar(cols[0],cols[2])
                if not mu or any(polar(cols[i],cols[j])!=mul[mu][polar(ee[i],ee[j])]
                         for i in range(4)for j in range(4)):continue
                full=[point_index[image(v)]for v in points]
                if len(set(full))!=820 or not all(frozenset(full[p]for p in ln)in all_lines for ln in lines):continue
                Mpower=[[int(i==j)for j in range(4)]for i in range(4)]
                for _ in range(order):Mpower=product(Mpower,m)
                if power==1:
                    scalar=Mpower[0][0]
                    assert scalar and all(Mpower[i][j]==(scalar if i==j else 0)for i in range(4)for j in range(4))
                else:scalar=None
                answer={"matrix_GF9":m,"frobenius_exponent":power,"multiplier_GF9":mu,
                        "certified_all_820_points":True,"certified_all_820_lines":True,
                        "projective_order":order,"scalar_power_when_linear":scalar}
                certified[order]=g
                break
            if answer:break
        checks[str(order)]={"status":"LIFT_FOUND" if answer else "NO_LIFT_FOUND_IN_PGAMMASP_SEARCH",
                            "attempts":trials,"lift":answer}
    if len(certified)>1:
        perms=[Permutation(certified[o])for o in sorted(certified)]
        group=PermutationGroup(perms)
        order=int(group.order())
        checks["generated_graph_group_order"]=order
        checks["generators_certified"]=sorted(certified)
        checks["equal_to_A5_order60"]=(order==60)
    return {"status":"PASS_EXACT_PROJECTIVE_SEMILINEAR_LIFT_AUDIT",
       "coordinate_encoding":"GF9 from symmetric_even_sets_gf.setup(9)",
       "line_set_indices":selected,"basis_projective_point_ids":basis,
       "lifts":checks,
       "boundary":"Independent order2/3 graph automorphisms need not belong to same A5 subgroup as previously fixed order5 element; full A5 module is not asserted."}

if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2)+"\n")
    print(json.dumps({"lifts":{o:(v.get("status")if isinstance(v,dict)else v)for o,v in d["lifts"].items()}}))
