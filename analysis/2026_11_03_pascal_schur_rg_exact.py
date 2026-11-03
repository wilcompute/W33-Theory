#!/usr/bin/env python3
"""Exact three-port Schur reduction of the mod-3 Pascal lattice graph.

Six Lucas blocks with unit inter-block bonds induce a rational conductance
renormalization. The 15/7 limit is the known SG3 resistance multiplier; this
file certifies its application to the *specified* triangular-cell graph.
"""
from __future__ import annotations
from pathlib import Path
import json
import sympy as sy

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_pascal_schur_rg_exact.json"

def lucas(n,k):
    while n or k:
        if k%3>n%3:return False
        n//=3;k//=3
    return True

def block_bridges():
    # The 3x3 block layout has exactly six allowed high ternary digits.
    N=3
    sites={(r,k) for r in range(3*N) for k in range(r+1) if lucas(r,k)}
    corners={(0,0):"A",(N-1,0):"B",(N-1,N-1):"C"}
    bridges=[]
    for r,k in sorted(sites):
        u=(r,k)
        for v in ((r+1,k),(r+1,k+1),(r,k+1)):
            if v not in sites:continue
            high_u=(u[0]//N,u[1]//N)
            high_v=(v[0]//N,v[1]//N)
            if high_u==high_v:continue
            low_u=(u[0]%N,u[1]%N)
            low_v=(v[0]%N,v[1]%N)
            assert low_u in corners and low_v in corners,(u,v)
            bridges.append(((high_u,corners[low_u]),(high_v,corners[low_v])))
    assert len(bridges)==9
    return bridges

def exact_reduction():
    c=sy.symbols("c",positive=True)
    blocks=[(a,b) for a in range(3) for b in range(a+1)]
    ports=[(block,label) for block in blocks for label in "ABC"]
    flip=lambda z:((z[0][0],z[0][0]-z[0][1]),
                   {"A":"A","B":"C","C":"B"}[z[1]])
    orbits={}
    for z in ports:
        if z in orbits:continue
        ident=len(set(orbits.values()))
        for x in (z,flip(z)):orbits[x]=ident
    groups={j:[z for z in ports if orbits[z]==j]
            for j in sorted(set(orbits.values()))}
    assert len(groups)==10
    weighted=[]
    for b in blocks:
        for a,z in (("A","B"),("A","C"),("B","C")):
            weighted.append(((b,a),(b,z),c))
    weighted += [(u,v,sy.S.One) for u,v in block_bridges()]
    # Reflect through axis top -> midpoint of base; top potential 1,
    # both bottom corners grounded. Other 8 orbit voltages are unknown.
    top=((0,0),"A");lower_left=((2,0),"B");lower_right=((2,2),"C")
    assert orbits[lower_left]==orbits[lower_right]
    high=orbits[top];low=orbits[lower_left]
    unknown=[j for j in groups if j not in (high,low)]
    assert len(unknown)==8
    mat=sy.zeros(8);rhs=sy.zeros(8,1)
    for i,orbit in enumerate(unknown):
        rep=groups[orbit][0]
        for u,v,g in weighted:
            if rep not in (u,v):continue
            other=v if u==rep else u
            dest=orbits[other]
            if dest==orbit:continue
            mat[i,i]+=g
            if dest in unknown:
                mat[i,unknown.index(dest)]-=g
            elif dest==high:
                rhs[i]+=g
            else:assert dest==low
    sol=mat.inv(method="DM")*rhs
    V={high:sy.S.One,low:sy.S.Zero,
       **{j:sy.factor(sol[i]) for i,j in enumerate(unknown)}}
    current=sy.factor(sum(g*(1-V[orbits[v if u==top else u]])
        for u,v,g in weighted if u==top or v==top))
    target=2*c*(9*c+7)/(15*c*c+31*c+15)
    assert sy.factor(current-target)==0
    cnext=sy.factor(current/2)
    expected=c*(9*c+7)/(15*c*c+31*c+15)
    assert sy.factor(cnext-expected)==0
    return dict(port_count=18,reflected_orbits=10,unknown_orbits=8,
                interblock_unit_edges=len(block_bridges()),
                outer_triangle_effective_conductance=str(cnext),
                current_from_top_with_bottom_pair_grounded=str(current),
                symbolic_schur_reduction_exact=True)

def base_c1():
    # Compute the first 6-site graph's three-port response with exact Q.
    sites=sorted((r,k) for r in range(3) for k in range(r+1) if lucas(r,k))
    ids={z:i for i,z in enumerate(sites)}
    L=sy.zeros(len(sites))
    for r,k in sites:
        u=(r,k)
        for v in ((r+1,k),(r+1,k+1),(r,k+1)):
            if v not in ids:continue
            i=ids[u];j=ids[v]
            L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
    top=ids[(0,0)]
    bottom={ids[(2,0)],ids[(2,2)]}
    unknown=[i for i in range(len(sites)) if i not in bottom|{top}]
    potentials=sy.zeros(len(sites),1)
    potentials[top]=1
    M=L.extract(unknown,unknown)
    b=-(L.extract(unknown,[top])*sy.ones(1,1))
    ans=M.inv()*b
    for i,x in zip(unknown,ans):potentials[i]=x
    current=(L*potentials)[top]
    assert current==sy.Rational(6,5)
    return sy.Rational(3,5)

def run():
    derived=exact_reduction()
    c=base_c1()
    series=[]
    for n in range(1,7):
        R=sy.Rational(2,3)/c
        series.append(dict(level=n,conductance_exact=str(c),
            resistance_exact=str(R),resistance_float=float(R)))
        c=sy.cancel(c*(9*c+7)/(15*c*c+31*c+15))
    ratios=[series[j]["resistance_float"]/series[j-1]["resistance_float"]
        for j in range(1,len(series))]
    # Strict positivity and c_next<c for c>0: denominator-(9c+7)
    # is 15c²+22c+8>0. Limit cannot be positive since every
    # positive candidate fixed point would violate c_next<c.
    x=sy.symbols('x')
    assert sy.expand((15*x**2+31*x+15)-(9*x+7)-(15*x**2+22*x+8))==0
    result=dict(status="PASS_EXACT_THREE_PORT_SCHUR_REDUCTION",
        exact_reduction=derived,initial_conductance="3/5",
        exact_series=series,observed_ratios=ratios,
        exact_recursion="c_(n+1)=c_n*(9*c_n+7)/(15*c_n^2+31*c_n+15)",
        rigorous_asymptotic="For c_n>0, c_(n+1)/c_n<1, so c_n decreases to the only nonnegative fixed point 0. Thus R_(n+1)/R_n=c_n/c_(n+1) tends to 15/7.",
        graph_proof="Lucas digit support: in barycentric coordinates (i,j,h) with i+j+h=3^n-1, each base-3 digit triple sums to 2. There are six choices per digit, invariant under S3. Six depth-(n-1) blocks have 9 unit connecting edges (3 in each triangular direction), all joining block corners. Each block reduces by its S3-invariant three-port Dirichlet response to a triangle with edge conductance c_n. Exact rational Schur reduction of the 18-port gluing circuit gives the recurrence.",
        existing_prior_art="The SG3 resistance scaling 15/7 is established in fractal electrical-network literature; the present particular cell-neighbor recursion and W33 no-go juxtaposition are this project-specific audit, not proof of priority.",
        dimensional_boundary="The RG factor 15/7 and the Pascal spatial magnification 3 determine relative scaling; neither defines an absolute meter or Einstein action.",
        literature=["https://doi.org/10.1016/0016-0032(89)90047-1",
                    "https://doi.org/10.1109/ICICES.2013.6508276"])
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS exact Schur recurrence",result["exact_recursion"],flush=True)
    print("PASS rational resistances",[(z["level"],z["resistance_exact"]) for z in series],flush=True)
    return result
if __name__=="__main__":run()
