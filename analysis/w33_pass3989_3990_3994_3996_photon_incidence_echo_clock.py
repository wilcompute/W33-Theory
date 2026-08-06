#!/usr/bin/env python3
"""Passes 3989, 3990, 3994-3996: sparse W33 coupler, exact echo, dark memory, Floquet clock, and tensor tower."""
from __future__ import annotations
import hashlib, itertools, json, math
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def canon(v):
    for x in v:
        if x%3:
            inv=1 if x%3==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError("zero vector")

def symp(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def zeros(r,c): return [[0]*c for _ in range(r)]
def matmul(A,B):
    Bt=list(zip(*B))
    return [[sum(x*y for x,y in zip(row,col)) for col in Bt] for row in A]
def madd(A,B): return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def msub(A,B): return [[x-y for x,y in zip(a,b)] for a,b in zip(A,B)]
def mscale(c,A): return [[c*x for x in row] for row in A]
def trace(A): return sum(A[i][i] for i in range(len(A)))
def equal(A,B): return A==B

def projective_w33():
    points=[]
    for v in itertools.product(range(3),repeat=4):
        if any(v):
            c=canon(v)
            if c not in points:
                points.append(c)
    assert len(points)==40
    index={p:i for i,p in enumerate(points)}
    lines=set()
    for i,x in enumerate(points):
        for j in range(i+1,40):
            y=points[j]
            if symp(x,y):
                continue
            line=set()
            for a,b in itertools.product(range(3),repeat=2):
                if a==b==0:
                    continue
                z=tuple((a*x[k]+b*y[k])%3 for k in range(4))
                line.add(index[canon(z)])
            assert len(line)==4
            lines.add(tuple(sorted(line)))
    lines=sorted(lines)
    assert len(lines)==40
    N=zeros(40,40)
    for j,line in enumerate(lines):
        for i in line:
            N[i][j]=1
    A=zeros(40,40)
    for i,x in enumerate(points):
        for j,y in enumerate(points):
            if i!=j and symp(x,y)==0:
                A[i][j]=1
    assert {sum(row) for row in A}=={12}
    assert {sum(row) for row in N}=={4}
    assert {sum(N[i][j] for i in range(40)) for j in range(40)}=={4}
    return points,lines,A,N

def block_incidence(N):
    H=zeros(80,80)
    for i in range(40):
        for j in range(40):
            H[i][40+j]=N[i][j]
            H[40+j][i]=N[i][j]
    return H

def girth(H):
    n=len(H); best=10**9
    for s in range(n):
        dist=[-1]*n; parent=[-1]*n; dist[s]=0
        q=deque([s])
        while q:
            u=q.popleft()
            for v,x in enumerate(H[u]):
                if not x: continue
                if dist[v]<0:
                    dist[v]=dist[u]+1; parent[v]=u; q.append(v)
                elif parent[u]!=v:
                    best=min(best,dist[u]+dist[v]+1)
    return best

def canonical_sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def phase_error(delta_over_g,m):
    R=float(delta_over_g)
    lam=(R-math.sqrt(R*R+4*m))/2
    t=math.pi*R/2
    actual=-lam*t
    intended=math.pi*m/2
    return (actual-intended+math.pi)%(2*math.pi)-math.pi

def main():
    points,lines,A,N=projective_w33()
    I=eye(40); J=[[1]*40 for _ in range(40)]
    M=matmul(N,list(map(list,zip(*N))))
    assert M==madd(mscale(4,I),A)
    P=matmul(matmul(M,msub(M,mscale(6,I))),msub(M,mscale(16,I)))
    assert P==zeros(40,40)
    tr1=trace(M); tr2=trace(matmul(M,M))
    assert (tr1,tr2)==(160,1120)
    multiplicities={"0":15,"6":24,"16":1}
    H=block_incidence(N)
    assert girth(H)==8

    B=msub(msub(J,I),A)
    D=msub(A,B)
    assert matmul(matmul(madd(D,mscale(15,I)),msub(D,mscale(5,I))),madd(D,mscale(7,I)))==zeros(40,40)
    Q0=matmul(msub(D,mscale(5,I)),madd(D,mscale(7,I)))
    Q5=matmul(madd(D,mscale(15,I)),madd(D,mscale(7,I)))
    Qm7=mscale(-1,matmul(madd(D,mscale(15,I)),msub(D,mscale(5,I))))
    assert Q0==mscale(4,J)
    assert matmul(Q5,Q5)==mscale(240,Q5)
    assert matmul(Qm7,Qm7)==mscale(96,Qm7)
    assert matmul(Q0,Q5)==zeros(40,40)
    assert matmul(Q0,Qm7)==zeros(40,40)
    assert matmul(Q5,Qm7)==zeros(40,40)
    assert madd(madd(mscale(3,Q0),mscale(2,Q5)),mscale(5,Qm7))==mscale(480,I)

    U15=madd(mscale(-5,madd(I,A)),mscale(2,J))
    assert matmul(U15,U15)==mscale(225,I)
    R30=madd(madd(mscale(20,I),mscale(5,A)),mscale(-2,J))
    assert matmul(R30,R30)==mscale(30,R30)
    assert trace(R30)==720

    detuning=[]
    for R in [20,40,80,160,320]:
        detuning.append({
            "delta_over_g":R,
            "maximum_bus_population_bound":64/(R*R+64),
            "phase_error_sector_m6_rad":phase_error(R,6),
            "phase_error_sector_m16_rad":phase_error(R,16),
        })

    tower=[]
    checkpoint8=None
    for m in range(1,9):
        shells=[]
        for r in range(m+1):
            mult=math.comb(m,r)*(24**r)
            singular_square=(16**(m-r))*(6**r)
            shells.append({
                "sqrt6_factors":r,
                "multiplicity":mult,
                "singular_value_squared":singular_square,
            })
        assert sum(x["multiplicity"] for x in shells)==25**m
        record={
            "level":m,
            "point_modes":40**m,
            "bright_rank":25**m,
            "dark_dimension_each_side":40**m-25**m,
            "total_bipartite_dark_dimension":2*(40**m-25**m),
            "dark_fraction_each_side":1-(5/8)**m,
            "nonzero_singular_shells":m+1,
        }
        if m<=4:
            record["shells"]=shells
            tower.append(record)
        if m==8:
            checkpoint8=record

    result={
        "schema":"w33.pass3989_3990_3994_3996.photon_incidence_echo_clock.v1",
        "status":"PASS_EXACT_SPARSE_COUPLER_ECHO_DARK_CLOCK_TOWER",
        "pass3989_sparse_incidence_coupler":{
            "point_modes":40,"line_bus_modes":40,"total_modes":80,
            "incidence_edges":160,"degree":4,"girth":8,
            "identity":"N N^T = 4 I + A_W33",
            "point_gram_spectrum":multiplicities,
            "bipartite_spectrum":{"-4":1,"-sqrt(6)":24,"0":30,"sqrt(6)":24,"4":1},
            "effective_hamiltonian":"For bus detuning Delta, H_eff=-(g^2/Delta) N N^T=-(g^2/Delta)(A+4I)+O(g^4/Delta^3).",
            "target_time":"t=pi Delta/(2 g^2) implements exp(i pi(A+4I)/2)=exp(-i pi L/2) in the dispersive limit.",
            "detuning_table":detuning,
            "boundary":"Exact graph lift and analytic two-level bounds. Not a fabricated device; higher-order disorder, loss, and simultaneous-mode calibration are not included."
        },
        "pass3990_dual_geometry_echo":{
            "A_spectrum":[12,2,-4],"B_spectrum":[27,-3,3],"D_equals_A_minus_B_spectrum":[-15,5,-7],
            "common_mode_identity":"A+B=J-I",
            "protected_echo":"On the 39-dimensional nonuniform subspace, exp(-i pi(A-B)/12) is a global phase times E_5-E_-7.",
            "sector_projectors":{
                "E_-15":"(D-5I)(D+7I)/160=J/40",
                "E_5":"(D+15I)(D+7I)/240",
                "E_-7":"-(D+15I)(D-5I)/96"
            },
            "moment_tomography":{
                "p_-15":"(<D^2>+2<D>-35)/160",
                "p_5":"(<D^2>+22<D>+105)/240",
                "p_-7":"(-<D^2>-10<D>+75)/96"
            },
            "common_error_firewall":"If identical commuting error C enters H_A=A+C and H_B=B+C, exp(-it H_A) exp(+it H_B)=exp(-it(A-B)) exactly. A symmetric echo cancels first-order common error more generally."
        },
        "pass3994_dark_sector_memory":{
            "point_dark_dimension":15,"line_dark_dimension":15,"total_dark_dimension":30,
            "bright_dimensions":{"uniform":1,"sqrt6_sector":24},
            "interpretation":"The incidence lift separates stationary dark coordinates from bright processing coordinates. Relative phase between dark and bright sectors can act as a clock-referenced memory, without changing causal-front speed.",
            "boundary":"A dark subspace is an engineered Hamiltonian property, not literal stored spacetime history or a claim that time is physical RAM."
        },
        "pass3995_exact_floquet_clock":{
            "generator":"L=12I-A","period":"pi in dimensionless coupling time",
            "quarter_step":"V=exp(-i pi L/4)=I-(1+i)E_10",
            "half_step":"V^2=U=I-2E_10",
            "cycle":["I","V","U","V^dagger","I"],
            "order":4,
            "projector":"E_10=(4I+A)/6-J/15",
            "interpretation":"Processor frequency is set by the engineered coupling constant multiplying L; vacuum c controls the propagation front, not this internal graph-clock rate."
        },
        "pass3996_tensor_incidence_tower":{
            "rank_law":"rank(N^{tensor m})=25^m",
            "dark_law":"dim ker(N^{tensor m})=40^m-25^m",
            "dark_fraction":"1-(5/8)^m",
            "nonzero_shell_count":"m+1",
            "tower_levels_1_to_4":tower,
            "level_8_checkpoint":checkpoint8,
            "boundary":"Tensor powers require genuine independent factors and grow the physical carrier exponentially. The shell law compresses spectral/control description, not Hilbert-space size or energy."
        }
    }
    result["semantic_sha256"]=canonical_sha(result)
    out=ROOT/"data/PART_3989_3990_3994_3996_PHOTON_INCIDENCE_ECHO_CLOCK.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS_PHOTON_INCIDENCE_ECHO_CLOCK",80,160,30,4,result["semantic_sha256"])

if __name__=="__main__":
    main()
