#!/usr/bin/env python3
"""A constructive 27-history x 27-internal-mode covariant clock bundle.

Proof-of-principle F3^3 covariant transport with variable local cubics;
NOT a derivation of gauge dynamics. Separately test a conventional
4-spinor Wilson lattice Dirac dispersion and its fermion-doubling tradeoff.
"""
import json,sys,itertools
from pathlib import Path
import numpy as np
import sympy as sp
from scipy import sparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_gauge_covariant_729_clock_wilson_dirac.json"

def group_action():
    _,terms,D,mapi,roots=R.load()
    edges,Ks=R.pack_roots(roots)
    null={(i,j) for i in range(27) for j in range(i+1,27) if D[i,j]}
    pos=next(i for i,packet in enumerate(edges)
             if sum((a,b) not in null for a,b,z in packet)==3)
    K=Ks[pos]
    hcoords={i:tuple(G.V[int(h)]) for i,h in enumerate(mapi)}
    ids={v:i for i,v in hcoords.items()}
    assert len(ids)==27
    def add(a,b):return tuple((x+y)%3 for x,y in zip(a,b))
    zero=(0,0,0)
    def permutation(a):
        P=np.zeros((27,27),dtype=np.int8)
        for i,x in hcoords.items():
            P[ids[add(x,a)],i]=1
        return P
    allP={x:permutation(x) for x in G.V}
    I=np.eye(27,dtype=np.int64)
    assert all(np.array_equal(p.T@p,I) for p in allP.values())
    Ksites={a:allP[a]@K@allP[a].T for a in G.V}
    for a in G.V:
        for b in [(1,0,0),(0,1,0),(0,0,1)]:
            assert np.array_equal(allP[b]@Ksites[a]@allP[b].T,Ksites[add(a,b)])
    # 27 sections over 27 history sites -> 729D real bundle
    Sblocks=sparse.block_diag([sparse.csr_matrix(Ksites[a]) for a in G.V],format="csr")
    assert Sblocks.shape==(729,729)
    permutations={}
    for a in [(1,0,0),(0,1,0),(0,0,1)]:
        rows=[];cols=[];vals=[]
        for h,site in enumerate(G.V):
            hprime=G.VID[add(site,a)]
            Pa=allP[a]
            out,inpt=Pa.nonzero()
            for i,j in zip(out,inpt):
                rows.append(27*hprime+int(i))
                cols.append(27*h+int(j))
                vals.append(1)
        S=sparse.coo_matrix((vals,(rows,cols)),shape=(729,729),dtype=np.int64).tocsr()
        assert (S.T@S-sparse.eye(729,format="csr")).nnz==0
        assert (S@Sblocks-Sblocks@S).nnz==0
        assert (S@S@S-sparse.eye(729,format="csr")).nnz==0
        permutations[str(a)]={"sparse_permutation_nnz":S.nnz,
            "commutator_with_bundle_clock_nnz":(S@Sblocks-Sblocks@S).nnz}
    # Each transported fiber's invariant is N_h(y)=N(P_h.T y);
    # K_h=P_h K P_h.T preserves N_h by exact polynomial invariance.
    return {
      "status":"PASS_EXPLICIT_729D_LIFTED_TRANSLATION_COVARIANT_CLOCK",
      "history_sites":27,"internal_real_modes_per_site":27,"total_real_modes":729,
      "base_clock_packet_index":pos,
      "base_clock_rank":int(np.linalg.matrix_rank(K)),
      "base_signed_cubic_invariant":"N(x) signed 45 triads",
      "fiber_cubic_transport":"N_h(y)=N(P_h.T y), with P_h translation permutation of 27 E6 mode labels",
      "transport":"T_a: |h,y> maps to |h+a,P_a y>",
      "covariant_clock":"K_bundle=direct_sum_h(P_h K P_h.T)",
      "K_bundle_sparse_nnz":Sblocks.nnz,
      "translation_controls":permutations,
      "fiber_cubic_not_same_fixed_polynomial":True,
      "base_cubic_fixed_translation_no_go_not_evaded":True,
      "interpretation":"The lifted transport commutes with the on-site clock because each fiber transports its cubic. This construction is a mathematically consistent but gauge-trivial pure relabeling and does not restore invariance of one fixed global N under the old 27 history permutations."
    }

def wilson_dirac():
    sx=sp.Matrix([[0,1],[1,0]])
    sy=sp.Matrix([[0,-sp.I],[sp.I,0]])
    sz=sp.diag(1,-1)
    I2=sp.eye(2);I4=sp.eye(4)
    alpha=[sp.kronecker_product(sx,z) for z in (sx,sy,sz)]
    beta=sp.kronecker_product(sz,I2)
    gammas=alpha+[beta]
    for i in range(4):
        for j in range(4):
            anti=gammas[i]*gammas[j]+gammas[j]*gammas[i]
            assert anti==(2*I4 if i==j else sp.zeros(4))
    s=sp.symbols("s1 s2 s3",real=True)
    c=sp.symbols("c1 c2 c3",real=True)
    mass,r=sp.symbols("m r",real=True)
    mw=mass+r*sum(1-z for z in c)
    H=sum((z*a for z,a in zip(s,alpha)),sp.zeros(4))+mw*beta
    energy2=sum(z*z for z in s)+mw*mw
    assert sp.simplify(H*H-energy2*I4)==sp.zeros(4)
    corners=[]
    for choice in itertools.product((0,1),repeat=3):
        cos=[1 if x==0 else -1 for x in choice]
        doublers=sum(choice)
        e2=energy2.subs({s[0]:0,s[1]:0,s[2]:0,c[0]:cos[0],c[1]:cos[1],c[2]:cos[2],mass:0,r:1})
        assert e2==4*doublers**2
        corners.append({"pi_coordinate_count":doublers,"corner":list(choice),"wilson_gap_energy":2*doublers})
    assert sum(x["wilson_gap_energy"]==0 for x in corners)==1
    return {"status":"PASS_GAUGE_COVARIANCE_DOES_NOT_DERIVE_DIRAC",
            "Clifford_alpha_beta":"4x4 conventional complex Dirac alpha1,alpha2,alpha3 and beta",
            "all_gamma_anticommutations_verified":16,
            "squared_energy":"sum_i sin(k_i)^2 + [m+r sum_i(1-cos k_i)]^2",
            "naive_massless_species_at_brillouin_corners":8,
            "wilson_massless_species_at_r_1_m_0":1,
            "seven_lifted_species_gaps":[x["wilson_gap_energy"] for x in corners if x["wilson_gap_energy"]>0],
            "wilson_explicit_chiral_symmetry_breaking":True,
            "selection_warning":"The 4-spinor Clifford matrices, integer lattice lifts, Wilson term, and scale parameter r are external design inputs, not derived from the finite W33/E6/H27 data. The finite 27-site torus has momenta only 0 and +/-2pi/3, so no controlled low-k continuum without a sequence of enlarging lattices."}

def main():
    q=group_action()
    w=wilson_dirac()
    o={"schema":"toe.20261113.gauge_lift_and_wilson.v1","bundle":q,"continuum":w}
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"bundle":q["status"],"block_nonzeros":q["K_bundle_sparse_nnz"],"translation_checks":q["translation_controls"],"lattice":w["status"]},indent=2),flush=True)
    return o
if __name__=="__main__":main()
