"""Exact 81-choose-3 W33 voltage optimization and full-symmetry obstruction.

Builds upon the independently implemented native 80-vertex Levi graph
and its integer Laplacian polynomial. No spacetime dynamics are asserted.
"""
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W


def optimize():
    G,points,lines=W.levi()
    tree=nx.bfs_tree(G,source=0).to_undirected()
    edges=sorted(tuple(sorted(e)) for e in G.edges())
    tedges={tuple(sorted(e)) for e in tree.edges()}
    chords=sorted(set(edges)-tedges)
    assert len(chords)==81 and len(edges)==160
    edgeidx={e:i for i,e in enumerate(edges)}
    B=np.zeros((80,160),dtype=np.int64)
    for i,(a,b) in enumerate(edges):
        B[a,i]=1
        B[b,i]=-1
    L=B@B.T
    H= -L@L@L+20*(L@L)-138*L+376*np.eye(80,dtype=np.int64)
    assert np.array_equal(L@H,320*np.eye(80,dtype=np.int64)-4*np.ones((80,80),dtype=np.int64))
    C=B[:,[edgeidx[e] for e in chords]]
    gram320=320*np.eye(81,dtype=np.int64)-C.T@H@C
    assert set(np.diag(gram320))=={162}
    off=Counter(int(gram320[i,j]) for i in range(81) for j in range(i+1,81))
    assert off=={2:1620,-6:1134,18:324,-54:162}
    best=None
    minima=[]
    freq=Counter()
    for i,j,k in itertools.combinations(range(81),3):
        vals=[int(gram320[i,j]),int(gram320[i,k]),int(gram320[j,k])]
        score=sum(v*v for v in vals)
        freq[score]+=1
        if best is None or score<best:
            best=score
            minima=[(i,j,k)]
        elif score==best:
            minima.append((i,j,k))
    assert sum(freq.values())==math.comb(81,3)==85320
    assert best==12 and len(minima)==10152
    idx=minima[0]
    assert idx==(0,4,8)
    selected=[chords[i] for i in idx]
    assert selected==[(1,45),(2,50),(3,55)]
    A=gram320[np.ix_(idx,idx)]
    assert np.array_equal(A,np.array([[162,2,2],[2,162,2],[2,2,162]]))
    # K = A/320 = 1/160*[81 1 1;1 81 1;1 1 81].
    # D=K/80 = above matrix /12800 with eigenvalues 80,80,83.
    eig=np.linalg.eigvalsh(A)
    assert np.max(abs(eig-np.array([160,160,166])))<1e-12
    voltage={e:(0,0,0) for e in edges}
    for i,e in enumerate(selected):
        voltage[e]=tuple(int(i==j) for j in range(3))
    # Reuse Bloch solver, which depends only on edge phase assignments.
    errs=[]
    for eps in (.25,.125,.0625):
        theta=np.array([1.,-.5,.6])*eps
        low=W.bloch_lowest(edges,voltage,theta)
        quad=float(theta@A@theta/25600)
        errs.append(dict(epsilon=eps,lowest_band=low,quadratic=quad,
                         relative_error=abs(low/quad-1)))
    assert errs[-1]["relative_error"]<.001
    return dict(chords=chords,selected=selected,indices=list(idx),
                total_triplets=sum(freq.values()),min_score=best,
                min_triplet_count=len(minima),
                off_diagonal_Gram320_counts={str(k):v for k,v in sorted(off.items())},
                score_histogram={str(k):v for k,v in sorted(freq.items())},
                K_numerator_160=[[81,1,1],[1,81,1],[1,1,81]],
                D_numerator_12800=[[81,1,1],[1,81,1],[1,1,81]],
                D_eigen_numerators_12800=[80,80,83],
                anisotropy_condition_ratio=83/80,
                bloch_checks=errs), G,points,lines,edges,B


def transvection_certificate(G,points,lines,edges,B):
    pidx={p:i for i,p in enumerate(points)}
    lidx={l:i for i,l in enumerate(lines)}
    eidx={e:i for i,e in enumerate(edges)}
    perms=[]
    for v in points:
        pm={i:pidx[W.projective(tuple((x[j]+W.symplectic(x,v)*v[j])%3
                                     for j in range(4)))]
            for i,x in enumerate(points)}
        lm={i:lidx[tuple(sorted(pm[k] for k in line))]
            for i,line in enumerate(lines)}
        perm=[eidx[tuple(sorted((pm[a],40+lm[b-40])))] for a,b in edges]
        assert len(set(perm))==160
        perms.append(perm)
    seen={0}; queue=[0]
    for a in queue:
        for perm in perms:
            b=perm[a]
            if b not in seen:
                seen.add(b);queue.append(b)
    assert len(seen)==160
    # Every oriented edge is point->line. The unique 1-cochain fixed by a
    # flag-transitive automorphism group is constant; it is exact.
    potential=np.array([1]*40+[0]*40,dtype=np.int64)
    assert np.array_equal(B.T@potential,np.ones(160,dtype=np.int64))
    # PSp(4,3) simple order25920. Finite GL(3,Z) subgroups inject after
    # reduction mod3 (torsion-free principal level3 congruence subgroup);
    # GL(3,F3) order11232 <25920. No nontrivial deck rank3 action exists.
    psp_order=(3**4*(3**2-1)*(3**4-1))//2
    gl3_f3=(3**3-1)*(3**3-3)*(3**3-3**2)
    assert (psp_order,gl3_f3)==(25920,11232)
    return dict(projective_symplectic_order=psp_order,
                GL3_F3_order=gl3_f3,
                checked_symplectic_transvections=len(perms),
                flag_orbit_size=len(seen),
                flag_transitive=True,
                invariant_point_to_line_edge_cochain="constant=vertex_coboundary",
                rational_H1_full_group_invariants=0,
                rank3_deck_representation="necessarily trivial, by PSp(4,3) simplicity and torsion-free level-3 principal congruence kernel",
                obstruction="A connected Z^3-periodic Levi cover with nonzero deck winding cannot preserve full PSp(4,3) symmetry with an integral linear deck action. A physical three-dimensional selector must break that symmetry or abandon this class of covers.",
                caveat="Does not exclude other W33-derived spacetime models with different fibers, graph refinements, nonlinear actions, or different symmetry realizations.")


def run():
    a,G,p,l,e,B=optimize()
    b=transvection_certificate(G,p,l,e,B)
    out=dict(status="PASS",optimization=a,symmetry=b,
             scope="Exact optimization among 3 SINGLE fundamental BFS chord voltages; no global optimum among all integer 1-cochains or physical uniqueness claim.",
             prior="analysis/toe_20261118_W33_triperiodic_Levi_homogenization.py")
    target=ROOT/"data/toe_20261118_isotropic_Levi_symmetry_no_go.json"
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS 85320 triples; 10152 minima; D eigen 80,80,83 /12800; full PSp cannot preserve rank3 deck")
    return out

if __name__=="__main__":
    run()
