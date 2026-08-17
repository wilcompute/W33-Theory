#!/usr/bin/env python3
"""Passes 5856--5862: binary Radon radicals and the full doily quadratic orbit.

This is a new exact packet after the collision-recovered M2(F2) frontier.
It proves:
  5856. Mod 2, the saturated point/heavy -> line Radon maps have image exactly
        the 5D radical of A3 tensor A3.  The 3D source radical maps to the
        single all-ones grid vector, with 2D kernel.  H^T instead has 2D image
        inside the heavy 3D radical and kills the point radical.
  5857. The 16 quadratic refinements of the determinant polar form split as
        10 hyperbolic grids and 6 elliptic ovoids.  Their Boolean chirps are
        Walsh eigenfunctions with eigenvalue +4 and -4 respectively.
  5858. The six ovoids pairwise meet in one doily point.  Each of the ten
        grids selects exactly nine of those fifteen pair-intersection points,
        and these nine edges form K3,3 on the six ovoid labels.  Hence the ten
        grids canonically become the ten unordered 3+3 partitions of six.
  5859. Sp4(2) has 720 elements and its action on the six ovoids is faithful,
        giving the explicit S6 permutation model.  The induced action on the
        ten grids agrees with the action on the ten 3+3 partitions.
  5860. Every pair of distinct grids meets in five points inducing K1 join 2K2:
        two isotropic lines through a unique center.  The 45 grid pairs are in
        bijection with the 15 doily points times the three unordered pairs of
        lines through that point.
  5861. The unit-difference L2(4) rook graph has the zero vertex's distance-2
        subconstituent equal to the 9 rank-one matrices, with induced graph
        L2(3)=SRG(9,4,1,2).  Its 72-element automorphism group is the determinant
        grid stabilizer from Pass5844.
  5862. Under the explicit Pass5825 product-coordinate relabeling, the three
        coordinates deleted in the [15,4,8] -> [12,4,6] simplex puncture become
        one of exactly two projective lines lying wholly in the six unit points.
        Those lines are non-isotropic for the doily symplectic form.

All statements are finite geometry/coding/Fourier facts.  No physical qubit,
particle, gauge-field, or continuum claim is made.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5856_5862_DOILY_QUADRATIC_ORBITS.json"

V2 = [(0, 0), (0, 1), (1, 0), (1, 1)]
NZ2 = [(1, 0), (0, 1), (1, 1)]
MATS = [tuple(x) for x in itertools.product((0, 1), repeat=4)]
ZERO = (0, 0, 0, 0)
BASIS4 = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]


def add(a,b): return tuple(x ^ y for x,y in zip(a,b))
def dot(a,b): return (a[0] & b[0]) ^ (a[1] & b[1])
def det(m): return (m[0] & m[3]) ^ (m[1] & m[2])
def mv(m,v): return ((m[0]&v[0])^(m[1]&v[1]), (m[2]&v[0])^(m[3]&v[1]))
def rmul(v,m): return ((v[0]&m[0])^(v[1]&m[2]), (v[0]&m[1])^(v[1]&m[3]))
def bdet(x,y): return det(add(x,y)) ^ det(x) ^ det(y)
def transpose(m): return (m[0],m[2],m[1],m[3])


def rank2(a):
    a=[list(map(lambda x:x&1,row)) for row in a]
    if not a: return 0
    r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        for i in range(len(a)):
            if i!=r and a[i][c]: a[i]=[x^y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r


def inv4(a):
    aug=[[a[i][j]&1 for j in range(4)]+[int(i==j) for j in range(4)] for i in range(4)]
    r=0
    for c in range(4):
        p=next(i for i in range(r,4) if aug[i][c])
        aug[r],aug[p]=aug[p],aug[r]
        for i in range(4):
            if i!=r and aug[i][c]: aug[i]=[x^y for x,y in zip(aug[i],aug[r])]
        r+=1
    return [row[4:] for row in aug]


def act4(a,v): return tuple(sum((a[i][j]&v[j]) for j in range(4))&1 for i in range(4))


def matmul4(a,b):
    return [[sum((a[i][k]&b[k][j]) for k in range(4))&1 for j in range(4)] for i in range(4)]


def connected_bipartition(edges):
    adj={i:set() for i in range(6)}
    for i,j in edges: adj[i].add(j); adj[j].add(i)
    col={0:0}; stack=[0]
    while stack:
        u=stack.pop()
        for v in adj[u]:
            if v not in col: col[v]=1-col[u]; stack.append(v)
            else: assert col[v]!=col[u]
    assert len(col)==6
    p0=tuple(sorted(i for i,c in col.items() if c==0))
    p1=tuple(sorted(i for i,c in col.items() if c==1))
    assert len(p0)==len(p1)==3
    return tuple(sorted((p0,p1)))


def main():
    # ---------- Reconstruct saturated Radon coordinate matrices ----------
    P=[(w,x) for w in NZ2 for x in V2]
    H=[(phi,psi) for phi in NZ2 for psi in V2]
    pidx={p:i for i,p in enumerate(P)}; hidx={h:i for i,h in enumerate(H)}; midx={m:i for i,m in enumerate(MATS)}
    R=[[int(mv(m,w)==x) for m in MATS] for w,x in P]
    Hinc=[[int((dot(phi,x)^dot(psi,w))==1) for phi,psi in H] for w,x in P]
    D=[[int(rmul(phi,m)==psi) for phi,psi in H] for m in MATS]

    PB=[]; HB=[]
    for w in NZ2:
        inds=[pidx[(w,x)] for x in V2]
        for i in range(3):
            z=[0]*12; z[inds[i]]=1; z[inds[3]]=-1; PB.append(z)
    for phi in NZ2:
        inds=[hidx[(phi,psi)] for psi in V2]
        for i in range(3):
            z=[0]*12; z[inds[i]]=1; z[inds[3]]=-1; HB.append(z)
    # columns, easier accessor
    PB=list(map(list,zip(*PB))); HB=list(map(list,zip(*HB)))

    L=[[0,1,1,0],[1,0,1,1],[0,1,1,1],[1,0,0,1]]
    Linv=inv4(L); C=[[Linv[j][i] for j in range(4)] for i in range(4)]
    qperm=[midx[act4(C,m)] for m in MATS]
    pair_idx={(a,b):midx[a+b] for a in V2 for b in V2}
    lcoords=[pair_idx[(V2[i],V2[j])] for i in range(3) for j in range(3)]
    pcoords=[]; hcoords=[]
    for w in NZ2: pcoords.extend(pidx[(w,V2[i])] for i in range(3))
    for phi in NZ2: hcoords.extend(hidx[(phi,V2[i])] for i in range(3))

    def mm(A,x): return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]
    def qvec(x):
        y=[0]*16
        for i,j in enumerate(qperm): y[j]=x[i]
        return y
    def line_coords(x): return [qvec(x)[i] for i in lcoords]
    def pcol(k): return [PB[i][k] for i in range(12)]
    def hcol(k): return [HB[i][k] for i in range(12)]
    RT=list(map(list,zip(*R))); HT=list(map(list,zip(*Hinc)))
    TR=[]; TD=[]; TH=[]
    for k in range(9):
        TR.append(line_coords(mm(RT,pcol(k))))
        TD.append(line_coords(mm(D,hcol(k))))
        TH.append([mm(HT,pcol(k))[i] for i in hcoords])
    # rows
    TR=list(map(list,zip(*TR))); TD=list(map(list,zip(*TD))); TH=list(map(list,zip(*TH)))
    TR2=[[x&1 for x in row] for row in TR]; TD2=[[x&1 for x in row] for row in TD]; TH2=[[x&1 for x in row] for row in TH]
    assert rank2(TR2)==rank2(TD2)==5 and rank2(TH2)==2

    prad=[]
    for b in range(3):
        v=[0]*9
        for i in range(3): v[3*b+i]=1
        prad.append(v)
    lrad=[]
    for j in range(3): lrad.append([int(k%3==j) for k in range(9)])
    for i in range(3): lrad.append([int(k//3==i) for k in range(9)])
    assert rank2(lrad)==5 and rank2(prad)==3
    # column spaces: rank([image | radical]) == radical rank means image is radical.
    imageTR=list(map(list,zip(*TR2))); imageTD=list(map(list,zip(*TD2))); imageTH=list(map(list,zip(*TH2)))
    assert rank2(list(map(list,zip(*(imageTR+lrad)))))==5
    assert rank2(list(map(list,zip(*(imageTD+lrad)))))==5
    assert rank2(list(map(list,zip(*(imageTH+prad)))))==3
    allones=[1]*9
    def apply(A,v): return [sum(A[i][j]*v[j] for j in range(9))&1 for i in range(9)]
    assert all(apply(TR2,v)==allones for v in prad)
    assert all(apply(TD2,v)==allones for v in prad)
    assert all(apply(TH2,v)==[0]*9 for v in prad)

    # ---------- Doily and all 16 quadratic refinements ----------
    nonzero=[x for x in MATS if x!=ZERO]
    rank1=[x for x in nonzero if det(x)==0]
    units=[x for x in nonzero if det(x)==1]
    refinements=[]
    for v in MATS:
        vals={x:det(x)^bdet(v,x) for x in MATS}
        z=frozenset(x for x in nonzero if vals[x]==0)
        refinements.append((v,vals,z))
    grids=[r for r in refinements if len(r[2])==9]
    ovoids=[r for r in refinements if len(r[2])==5]
    assert len(grids)==10 and len(ovoids)==6

    def walsh(vals,z): return sum(((-1)**vals[x]) * ((-1)**bdet(z,x)) for x in MATS)
    grid_eigs=set(); ovoid_eigs=set()
    for _,vals,_ in grids:
        ratios={walsh(vals,z)//((-1)**vals[z]) for z in MATS}; assert len(ratios)==1; grid_eigs |= ratios
    for _,vals,_ in ovoids:
        ratios={walsh(vals,z)//((-1)**vals[z]) for z in MATS}; assert len(ratios)==1; ovoid_eigs |= ratios
    assert grid_eigs=={4} and ovoid_eigs=={-4}

    # Six ovoids are the six 'letters'; pair intersections are 15 unique doily points.
    O=[o[2] for o in ovoids]
    pairpoint={}
    for i in range(6):
        for j in range(i+1,6):
            inter=O[i]&O[j]; assert len(inter)==1
            pairpoint[(i,j)]=next(iter(inter))
    assert len(set(pairpoint.values()))==15

    grid_partitions=[]
    for _,_,G in grids:
        e=[(i,j) for (i,j),p in pairpoint.items() if p in G]
        deg=[0]*6
        for i,j in e: deg[i]+=1;deg[j]+=1
        assert len(e)==9 and deg==[3]*6
        part=connected_bipartition(e)
        grid_partitions.append(part)
    assert len(set(grid_partitions))==10
    all_partitions=set()
    for A in itertools.combinations(range(6),3):
        B=tuple(sorted(set(range(6))-set(A)))
        all_partitions.add(tuple(sorted((tuple(A),B))))
    assert set(grid_partitions)==all_partitions and len(all_partitions)==10

    # ---------- Sp4(2) action: faithful S6 on ovoids, induced 10-grid action ----------
    gl4=[]; sp4=[]
    for bits in itertools.product((0,1), repeat=16):
        a=[list(bits[4*i:4*i+4]) for i in range(4)]
        if rank2(a)!=4: continue
        gl4.append(a)
        if all(bdet(act4(a,x),act4(a,y))==bdet(x,y) for x in BASIS4 for y in BASIS4): sp4.append(a)
    assert len(gl4)==20160 and len(sp4)==720
    Oidx={frozenset(s):i for i,s in enumerate(O)}
    Gsets=[g[2] for g in grids]; Gidx={frozenset(s):i for i,s in enumerate(Gsets)}
    ovoid_perms=[]; grid_perms=[]
    for a in sp4:
        po=[]; pg=[]
        for S in O:
            po.append(Oidx[frozenset(act4(a,x) for x in S)])
        for S in Gsets:
            pg.append(Gidx[frozenset(act4(a,x) for x in S)])
        ovoid_perms.append(tuple(po)); grid_perms.append(tuple(pg))
    assert len(set(ovoid_perms))==720
    assert len(set(grid_perms))==720
    # Equivariance of the 10-grid <-> 3+3-partition map.
    for po,pg in zip(ovoid_perms,grid_perms):
        for i,part in enumerate(grid_partitions):
            moved=tuple(sorted(tuple(sorted(po[x] for x in side)) for side in part))
            assert moved==grid_partitions[pg[i]]

    # ---------- Pairwise grid intersections are the 45 pointed two-line angles ----------
    doily_lines=set()
    for i,x in enumerate(nonzero):
        for y in nonzero[i+1:]:
            if bdet(x,y)==0:
                doily_lines.add(tuple(sorted((x,y,add(x,y)))))
    assert len(doily_lines)==15
    line_through={p:[] for p in nonzero}
    for line in doily_lines:
        for p in line: line_through[p].append(line)
    assert all(len(v)==3 for v in line_through.values())
    angle_sets={}
    for p,ls in line_through.items():
        for a,b in itertools.combinations(ls,2): angle_sets[frozenset(set(a)|set(b))]=(p,a,b)
    assert len(angle_sets)==45
    grid_intersections=[]
    for i in range(10):
        for j in range(i+1,10):
            S=frozenset(Gsets[i]&Gsets[j]); assert len(S)==5; assert S in angle_sets
            # induced collinearity graph = K1 join 2K2
            deg=sorted(sum(bdet(x,y)==0 for y in S if y!=x) for x in S)
            assert deg==[2,2,2,2,4]
            grid_intersections.append(S)
    assert len(set(grid_intersections))==45

    # ---------- Nested rook theorem: L2(4) -> L2(3) ----------
    def rook_edge(x,y): return x!=y and det(add(x,y))==1
    deg16=[sum(rook_edge(x,y) for y in MATS) for x in MATS]
    assert set(deg16)=={6}
    # zero neighbors are units; distance-two vertices are rank-one.
    assert {y for y in MATS if rook_edge(ZERO,y)}==set(units)
    # induced rank-one graph has SRG(9,4,1,2).
    rdeg={x:sum(rook_edge(x,y) for y in rank1) for x in rank1}
    assert set(rdeg.values())=={4}
    lam=[]; mu=[]
    for i,x in enumerate(rank1):
        for y in rank1[i+1:]:
            c=sum(rook_edge(x,z) and rook_edge(y,z) for z in rank1)
            (lam if rook_edge(x,y) else mu).append(c)
    assert set(lam)=={1} and set(mu)=={2}
    # determinant stabilizer restrictions to rank1 has exactly 72 permutations.
    qstab=[]
    for a in sp4:
        if all(det(act4(a,x))==det(x) for x in MATS): qstab.append(a)
    assert len(qstab)==72
    rindex={x:i for i,x in enumerate(rank1)}
    rperms={tuple(rindex[act4(a,x)] for x in rank1) for a in qstab}
    assert len(rperms)==72

    # ---------- Simplex puncture line becomes one of two unit-only projective lines ----------
    deleted_product=[(0,0,b[0],b[1]) for b in NZ2]
    deleted_matrix=[act4(Linv,x) for x in deleted_product]
    assert all(x in units for x in deleted_matrix)
    unit_lines=set()
    for i,x in enumerate(units):
        for y in units[i+1:]:
            z=add(x,y)
            if z in units: unit_lines.add(tuple(sorted((x,y,z))))
    assert len(unit_lines)==2
    deleted_line=tuple(sorted(deleted_matrix)); assert deleted_line in unit_lines
    for line in unit_lines:
        assert all(bdet(x,y)==1 for x,y in itertools.combinations(line,2))
        assert tuple(sorted(transpose(x) for x in line))==line

    out={
      "schema":"w33.pass5856_5862.doily_quadratic_orbits.v1","status":"PASS",
      "pass_5856_mod2_radon_radical_map":{
        "R_transpose_mod2_rank":5,"D_mod2_rank":5,"H_transpose_mod2_rank":2,
        "point_heavy_radical_dim":3,"line_radical_dim":5,
        "R_transpose_image":"exactly the 5D line radical","D_image":"exactly the 5D line radical",
        "point_radical_under_R_transpose":"all three generators map to the single 3x3 all-ones vector; restriction rank 1, kernel dimension 2",
        "point_radical_under_D":"same rank-1 all-ones image",
        "H_transpose_image":"2D subspace of the heavy 3D radical","point_radical_under_H_transpose":"zero",
        "deduction":"mod 2, all saturated Radon information lands in degenerate lattice radicals; it does not descend to the nondegenerate quotient"
      },
      "pass_5857_quadratic_refinement_bent_orbits":{
        "quadratic_refinements":16,"hyperbolic_grid_forms":10,"elliptic_ovoid_forms":6,
        "hyperbolic_nonzero_zeros":9,"elliptic_nonzero_zeros":5,
        "Walsh_eigenvalue_hyperbolic":4,"Walsh_eigenvalue_elliptic":-4,
        "deduction":"the 10+6 hyperplane split is exactly the +/- bent-Walsh sign split for the 16 refinements of one symplectic polar form"
      },
      "pass_5858_ovoid_grid_partition_model":{
        "ovoids":6,"pairwise_ovoid_intersection_size":1,"pair_intersection_points":15,
        "grids":10,"edges_selected_per_grid_on_six_ovoids":9,"induced_graph":"K3,3",
        "partitions_realized":"all 10 unordered 3+3 partitions of six ovoid labels",
        "deduction":"the classical S6 3+3-partition model of the ten doily grids is reconstructed internally from ovoid intersections"
      },
      "pass_5859_explicit_S6_action":{
        "Sp4_2_order":720,"distinct_permutations_on_six_ovoids":720,"distinct_permutations_on_ten_grids":720,
        "deduction":"the ovoid action is faithful and identifies Sp4(2) with S6; the ten-grid action is exactly the induced S6 action on unordered 3+3 partitions"
      },
      "pass_5860_grid_pair_angle_bijection":{
        "grid_pairs":45,"distinct_five_point_intersections":45,"intersection_size":5,
        "induced_intersection_graph":"K1 join 2K2 (two doily lines through one center)",
        "doily_angles":"15 points x C(3 lines through point,2) = 45",
        "deduction":"edges of K10 on the ten grids are canonically the pointed unordered two-line angles of the doily"
      },
      "pass_5861_nested_rook_subconstituent":{
        "ambient":"unit-difference Cayley graph L2(4)=SRG(16,6,2,2)",
        "zero_neighbors":"six units","zero_distance2":"nine rank-one matrices",
        "rank_one_induced_graph":"L2(3)=SRG(9,4,1,2)",
        "determinant_grid_stabilizer_order":72,"distinct_rank_one_permutations":72,
        "deduction":"the doily 3x3 determinant grid is literally the distance-2 subconstituent of the 4x4 rook graph at zero, and its full 72 symmetry is the zero/determinant stabilizer"
      },
      "pass_5862_simplex_puncture_unit_line":{
        "unit_points":6,"projective_lines_wholly_in_units":2,"deleted_coordinates":3,
        "deleted_line_maps_to_one_unit_line":True,"unit_lines_are_nonisotropic":True,"transpose_fixes_each_unit_line_setwise":True,
        "deduction":"the [15,4,8] -> [12,4,6] puncture deletes a non-isotropic 3-point line lying wholly in the six-point complement of the determinant grid"
      },
      "boundary":"Exact finite geometry, binary lattice, coding and Fourier statements. The W(3,2) model is an abstract two-qubit Pauli incidence geometry; no q=5 physical-state, particle, gauge-field or continuum identification is asserted."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
