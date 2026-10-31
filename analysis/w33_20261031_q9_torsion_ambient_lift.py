#!/usr/bin/env python3
"""Lift the actual q=9 icosa orbit's order-five graph automorphism to PGammaSp(4,9).

Certifies the source line incidence, induced action on 240 points, and an
explicit invertible GF(9) semilinear transformation if one exists.
"""
import itertools,json,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from symmetric_fast import fast_build
from symmetric_even_sets_gf import setup

OUT=ROOT/"data/w33_20261031_q9_torsion_ambient_lift.json"
def build():
    points,lines=fast_build(9)
    info=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())
    selected=info["results"][0]["chosen"]
    auto=json.loads((ROOT/"data/w33_20261031_torsion_order5_probe.json").read_text())["order5_mapping"]
    assert len(auto)==len(selected)==48 and sorted(auto)==list(range(48))
    cover={}
    for i,j in enumerate(selected):
        for p in lines[j]:cover.setdefault(p,[]).append(i)
    assert len(cover)==240 and all(len(v)==2 for v in cover.values())
    by_pair={tuple(sorted(v)):p for p,v in cover.items()}
    assert len(by_pair)==240
    mapped={}
    for p,pair in cover.items():
        new=tuple(sorted(auto[i] for i in pair))
        assert new in by_pair
        mapped[p]=by_pair[new]
    assert len(set(mapped.values()))==240
    F,add,mul,inv,neg=setup(9)
    def linear_rank(rows):
        v=[list(x) for x in rows];n=4;r=0
        for j in range(n):
            t=next((k for k in range(r,len(v)) if v[k][j]!=0),None)
            if t is None:continue
            v[r],v[t]=v[t],v[r];a=inv[v[r][j]]
            v[r]=[mul[a][x] for x in v[r]]
            for k in range(len(v)):
                if k!=r and v[k][j]:
                    a=v[k][j];v[k]=[add[v[k][z]][neg[mul[a][v[r][z]]]] for z in range(n)]
            r+=1
        return r
    basis=[]
    for p in sorted(cover):
        if linear_rank([points[z] for z in basis]+[points[p]])>len(basis):
            basis.append(p)
            if len(basis)==4:break
    assert len(basis)==4
    def inverse(M):
        a=[list(M[i])+[int(i==j) for j in range(4)] for i in range(4)]
        for k in range(4):
            r=next(i for i in range(k,4) if a[i][k]);a[k],a[r]=a[r],a[k]
            d=inv[a[k][k]]
            a[k]=[mul[d][z] for z in a[k]]
            for j in range(4):
                if j!=k and a[j][k]:
                    d=a[j][k]
                    a[j]=[add[a[j][l]][neg[mul[d][a[k][l]]]]for l in range(8)]
        return [r[4:] for r in a]
    def mm(A,B):
        return [[sum_f(mul[A[i][k]][B[k][j]] for k in range(4)) for j in range(len(B[0]))] for i in range(len(A))]
    def sum_f(a):
        z=0
        for t in a:z=add[z][t]
        return z
    def norm(x):
        a=inv[next(z for z in x if z)]
        return tuple(mul[a][z] for z in x)
    image={p:tuple(points[q]) for p,q in mapped.items()}
    basisimages=[image[p] for p in basis]
    attempts=0
    result=None
    for power in (1,3):
        B=[[pow(points[p][r],power) if power==1 else None for p in basis]for r in range(4)]
        # GF(9) third-power Frobenius must use multiplication table, NOT integer pow.
        def frob(x):return x if power==1 else mul[mul[x][x]][x]
        B=[[frob(points[p][r]) for p in basis] for r in range(4)]
        Binv=inverse(B)
        Y=[[image[p][r] for p in basis]for r in range(4)]
        for ds in itertools.product(F[1:],repeat=3):
            attempts+=1
            d=(1,)+ds
            M=mm([[mul[Y[i][j]][d[j]] for j in range(4)]for i in range(4)],Binv)
            def apply(p):
                x=[frob(v) for v in points[p]]
                return norm([sum_f(mul[M[i][k]][x[k]] for k in range(4)) for i in range(4)])
            if any(apply(p)!=image[p] for p in list(sorted(mapped))[:8]):continue
            if all(apply(p)==image[p] for p in mapped):
                result={"matrix_GF9":M,"field_frobenius_power":power,
                        "projective_points_certified":240,
                        "four_basis_point_ids":basis,
                        "generator_order":5,
                        "all_selected_line_images_certified":all(
                           {mapped[p] for p in lines[selected[i]]}
                           ==set(lines[selected[auto[i]]])
                           for i in range(48))}
                break
        if result is not None:break
    if result:
        M=result["matrix_GF9"];power=result["field_frobenius_power"]
        def frob(x):return x if power==1 else mul[mul[x][x]][x]
        def image_vector(v):
            x=[frob(t) for t in v]
            return norm([sum_f(mul[M[i][k]][x[k]] for k in range(4)) for i in range(4)])
        def alternating(u,v):
            return sum_f([mul[u[0]][v[2]],mul[u[1]][v[3]],
               neg[mul[u[2]][v[0]]],neg[mul[u[3]][v[1]]]])
        ee=[[int(i==j)for j in range(4)]for i in range(4)]
        scaled=alternating(image_vector(ee[0]),image_vector(ee[2]))
        # image_vector() is projectively normalized: for the form use raw M columns.
        columns=[[M[i][j] for i in range(4)]for j in range(4)]
        mu=alternating(columns[0],columns[2])
        assert mu!=0
        for i in range(4):
            for j in range(4):
                target=mul[mu][alternating(ee[i],ee[j])]
                assert alternating(columns[i],columns[j])==target
        pid={tuple(p):j for j,p in enumerate(points)}
        fullmap=[pid[image_vector(v)] for v in points]
        assert len(set(fullmap))==820
        lid={frozenset(line) for line in lines}
        assert all(frozenset(fullmap[p] for p in line) in lid for line in lines)
        mm5=[[int(i==j) for j in range(4)] for i in range(4)]
        for _ in range(5):mm5=mm(mm5,M)
        assert all(mm5[i][j]==0 for i in range(4) for j in range(4) if i!=j)
        assert len({mm5[i][i] for i in range(4)})==1 and mm5[0][0]!=0
        result.update({"symplectic_similitude_multiplier_GF9":mu,
           "all_projective_points_permuted":820,
           "all_isotropic_lines_permuted":820,
           "fifth_power_scalar_GF9":mm5[0][0],
           "full_ambient_PGSp_certificate":True})
    return {"status":"PASS_GF9_AMBIENT_SEMILINEAR_LIFT" if result else "NO_SEMILINEAR_LIFT_FOUND",
            "search_attempts":attempts,"point_map":result,
            "scope":"A lift, if found, identifies this order-five torsion action with a genuine ambient GF(9) collineation. No physics is inferred. If absent it exposes an abstract-graph automorphism not detected by the searched semilinear class."}
if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":d["status"],"attempts":d["search_attempts"],"lift":d["point_map"]}))
