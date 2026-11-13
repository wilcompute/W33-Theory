#!/usr/bin/env python3
"""Exact non-flat compact-E6 lattice gauge field on F3^3 sites.

Each link is an integer signed permutation exp(pi/2 K) from the
36 cubic-preserving root packets. Independent noncommuting root
rotations generate a non-identity compact E6 Wilson plaquette.
Build 2187x729 covariant finite-difference operator D; verify
L=D^T D gauge covariance, positive kinetic energy, sitewise signed
cubic, and gauge-invariant Wilson holonomy under nonconstant site
gauge transformations.

Nonzero curvature is real mathematically but SU(8) matter,
Lorentz metric, and Yang-Mills action not derived.
"""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
import json,sys
import numpy as np
from scipy import sparse
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_E6_compact_nonflat_Wilson_lattice_gauge.json"

def exact_cubic(N,x):
    return sum(int(s)*int(x[i])*int(x[j])*int(x[k]) for (i,j,k),s in N.items())

def check_signed_permutation(U,N):
    assert np.array_equal(U@U.T,np.eye(27,dtype=np.int64))
    assert set(np.abs(U).sum(0))=={1}
    assert set(np.abs(U).sum(1))=={1}
    p=np.argmax(np.abs(U),axis=0)
    im={}
    for t,sgn in N.items():
        mapped=tuple(sorted(int(p[i]) for i in t))
        factors=np.prod([int(U[p[i],i]) for i in t])
        assert mapped not in im
        im[mapped]=int(sgn)*int(factors)
    assert im==N
    return True

def root_links():
    _,N,_,_,roots=R.load()
    packets,Ks=R.pack_roots(roots)
    I=np.eye(27,dtype=np.int64)
    link=[I+K+K@K for K in Ks]
    for i in (0,1,2):check_signed_permutation(link[i],N)
    for i,j in combinations(range(36),2):
        W=link[i]@link[j]@link[i].T@link[j].T
        if not np.array_equal(W,I):
            return N,link[i],link[j],link[(j+1)%36],[i,j,(j+1)%36],W
    raise AssertionError("All finite compact rotations commute?")

def build_derivative(U_by_site,V):
    # row edge=(h,a,k), result field[destination,k] -
    # sum_l U_{h,a}[k,l]*field[h,l].
    rows=[];cols=[];vals=[]
    dirs=[(1,0,0),(0,1,0),(0,0,1)]
    for h,coord in enumerate(V):
        for a,delta in enumerate(dirs):
            destination=G.VID[tuple((coord[k]+delta[k])%3 for k in range(3))]
            link=U_by_site[h,a]
            for m in range(27):
                r=(h*3+a)*27+m
                rows.append(r);cols.append(destination*27+m);vals.append(1)
                for n in np.flatnonzero(link[m]):
                    rows.append(r);cols.append(h*27+int(n));vals.append(-int(link[m,n]))
    return sparse.coo_matrix((vals,(rows,cols)),shape=(2187,729),dtype=np.int64).tocsr()

def main():
    N,Ux,Uy,Uz,which,W=root_links()
    assert not np.array_equal(W,np.eye(27,dtype=np.int64))
    assert check_signed_permutation(W,N)
    V=[tuple(map(int,v)) for v in G.V]
    assert len(V)==27
    link=np.stack([[Ux,Uy,Uz] for _ in V],axis=0)
    D=build_derivative(link,V)
    assert D.nnz==4374,D.nnz
    L=D.T@D
    assert (L-L.T).nnz==0
    seed=np.random.default_rng(2026111308)
    psi=seed.integers(-2,3,size=729,dtype=np.int64)
    energy=int((D@psi)@(D@psi))
    assert int(psi@(L@psi))==energy>=0
    # Gauge by site-dependent products of cubic-preserving rotations.
    Q={}
    for h,t in enumerate(V):
        q=np.linalg.matrix_power(Ux,t[0]) @ np.linalg.matrix_power(Uy,t[1]) @ np.linalg.matrix_power(Uz,t[2])
        assert np.array_equal(q@q.T,np.eye(27,dtype=np.int64))
        Q[h]=q
    new=np.empty_like(link)
    dirs=((1,0,0),(0,1,0),(0,0,1))
    for h,t in enumerate(V):
        for a,delta in enumerate(dirs):
            dest=G.VID[tuple((t[k]+delta[k])%3 for k in range(3))]
            new[h,a]=Q[dest]@link[h,a]@Q[h].T
    Dp=build_derivative(new,V)
    QQ=sparse.block_diag([sparse.csr_matrix(Q[h]) for h in range(27)],format="csr")
    assert (QQ.T@QQ-sparse.eye(729,format="csr")).nnz==0
    Lp=Dp.T@Dp
    # The operator transforms by conjugation under compact local gauge.
    assert (Lp-QQ@L@QQ.T).nnz==0
    psip=QQ@psi
    assert int(psip@(Lp@psip))==energy
    orig_N=[exact_cubic(N,psi[h*27:(h+1)*27]) for h in range(27)]
    after_N=[exact_cubic(N,psip[h*27:(h+1)*27]) for h in range(27)]
    assert orig_N==after_N
    # Wilson holonomy around a 0-1 plaquette, orientation:
    # h->h+x->h+x+y->h+y->h:
    # W=U_y(h)^-1 U_x(h+y)^-1 U_y(h+x) U_x(h).
    def plaq(links,h):
        t=V[h]
        dx=G.VID[((t[0]+1)%3,t[1],t[2])]
        dy=G.VID[(t[0],(t[1]+1)%3,t[2])]
        return links[h,1].T@links[dy,0].T@links[dx,1]@links[h,0]
    ordinary=plaq(link,0)
    transformed=plaq(new,0)
    assert np.array_equal(transformed,Q[0]@ordinary@Q[0].T)
    assert not np.array_equal(ordinary,np.eye(27,dtype=np.int64))
    assert int(np.trace(ordinary))==int(np.trace(transformed))
    Gsec=nx.Graph();Gsec.add_nodes_from(range(27))
    for t in N:Gsec.add_edges_from(combinations(t,2))
    allsec=list(nx.find_cliques(nx.complement(Gsec)))
    ph=np.argmax(np.abs(ordinary),axis=0)
    fixed={}
    for size in (5,6):
        ss=[tuple(sorted(x)) for x in allsec if len(x)==size]
        fixed[str(size)]=sum(tuple(sorted(int(ph[i]) for i in s))==s for s in ss)
    out={
       "status":"PASS_EXACT_NONFLAT_COMPACT_E6_CUBIC_GAUGE_WILSON_PLAQUETTE",
       "source_root_packet_ids":which,
       "history_sites":27,"internal_real_modes":27,"total_real_lattice_modes":729,
       "directed_lattice_edges":81,"covariant_derivative_size":[2187,729],
       "covariant_derivative_nonzeros":D.nnz,
       "Wilson_loop_trace":int(np.trace(ordinary)),
       "Wilson_loop_is_not_identity":True,
       "Wilson_loop_nonidentity_moved_coordinates":int(27-np.trace(np.abs(ordinary))),
       "Wilson_loop_matrix_order":next(k for k in range(1,101) if np.array_equal(np.linalg.matrix_power(ordinary,k),np.eye(27,dtype=np.int64))),
       "fixed_maximal_sections_by_Wilson_loop":fixed,
       "gauge_group":"the compact real orthogonal stabilizer of canonical signed 45-term E6 cubic",
       "lattice_kinetic_energy":energy,
       "sitewise_cubic_invariance":True,
       "entire_729_laplacian_gauge_covariance_exact_integer":True,
       "nonflat_plaquette_gauge_conjugacy_exact":True,
       "positive_semidefinite_laplacian":"L=D^T D over Z by construction",
       "physical_scope":"Non-flat compact lattice gauge background and exact gauge-invariant matter energy, with link variables externally selected. No dynamical derivation of a Yang-Mills gauge action, Lorentz invariance, Standard Model chirality, or gravitational equations.",
       "section_relevance":"A nontrivial holonomy might preserve only some 5/6-dimensional cubic-null coordinate sections, a finite gauge-vacuum selection constraint; not proof of physical vacuum."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","source_root_packet_ids","Wilson_loop_trace","Wilson_loop_matrix_order","fixed_maximal_sections_by_Wilson_loop","lattice_kinetic_energy"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
