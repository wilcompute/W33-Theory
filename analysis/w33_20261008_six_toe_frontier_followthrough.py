#!/usr/bin/env python3
"""Six exact/controlled physics-interface tests on W33.

Scientific status: graph/Poisson/charge theorems and *supplied* phenomenological
models, not a derived 4D action, observed Yukawa spectrum, or heterotic vacuum.
"""
from __future__ import annotations
import itertools
import json
import math
import sys
from collections import Counter, deque
from fractions import Fraction as Q
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_dual_27_electrical_transport import build_graphs

OUTPUT=ROOT/"data"/"w33_20261008_six_toe_frontier_followthrough.json"


def spectral_projectors(a):
    vals=(8,2,-1,-4)
    e=np.eye(len(a),dtype=np.int64)
    pieces={}
    for v in vals:
        n=e.copy()
        den=1
        for w in vals:
            if w != v:
                n=n@(a-w*e)
                den*=v-w
        assert np.array_equal(n@n,den*n)
        assert np.array_equal(n@a,v*n)
        pieces[v]=(n,den)
    assert all(sum(Q(int(pieces[v][0][i,j]),pieces[v][1]) for v in vals)==(i==j)
               for i in range(27) for j in range(27))
    return pieces


def coherent_frontier():
    out={}
    for name,a in build_graphs().items():
        proj=spectral_projectors(a)
        mean=np.zeros((27,27),dtype=object)
        t=.43
        u=np.zeros((27,27),dtype=complex)
        for i in range(27):
            for j in range(27):
                mean[i,j]=sum(Q(int(num[i,j]*num[i,j]),den*den)
                              for num,den in proj.values())
        for eigenvalue,(num,den) in proj.items():
            u += np.exp(-1j*t*eigenvalue)*(num/den)
        assert np.max(np.abs(u.conj().T@u-np.eye(27)))<1e-12
        probs=np.abs(u)**2
        assert np.max(abs(probs.sum(axis=0)-1))<1e-12
        mixhist=Counter(str(mean[i,j]) for i in range(27) for j in range(i+1,27))
        # Szegedy coherent lift of the stochastic map P=A/8.
        # V|i> = |i> (x) sum_j sqrt(Pij)|j> is an isometry.
        edges=np.argwhere(a>0)
        assert len(edges)==216
        psi=np.zeros((27,27),float)
        psi[a>0]=1/np.sqrt(216)
        def refl(x):
            c=np.einsum('ij,ij->i',x,a)/np.sqrt(8)
            projection=(c[:,None]*a)/np.sqrt(8)
            return 2*projection-x
        def step(x):
            return refl(refl(x).T).T  # R S R S variant, still unitary
        x=np.random.default_rng(13).normal(size=(27,27))
        assert abs(np.linalg.norm(refl(x))-np.linalg.norm(x))<1e-11
        assert abs(np.linalg.norm(step(x))-np.linalg.norm(x))<1e-11
        assert np.max(abs(step(psi)-psi))<1e-12
        off=[probs[i,j] for i in range(27) for j in range(i+1,27)]
        out[name]={
            "spectrum": {"8":1,"2":12,"-1":8,"-4":6},
            "hamiltonian":"H=A, U(t)=exp(-i t A), t=0.43 dimensionless supplied",
            "unitarity_error_max":float(np.max(np.abs(u.conj().T@u-np.eye(27)))),
            "instantaneous_offdiagonal_prob_min":float(min(off)),
            "instantaneous_offdiagonal_prob_max":float(max(off)),
            "instantaneous_offdiagonal_prob_classes_rounded12":dict(sorted(Counter(str(round(x,12)) for x in off).items())),
            "exact_infinite_time_average_offdiag":dict(sorted(mixhist.items(),key=lambda kv:Q(kv[0]))),
            "stationary_szegedy_state":"uniform superposition of 216 directed edges",
            "szegedy_unitary_norm_check":True,
            "loss_survival_example_gamma_0p1_at_t_0p43":float(np.exp(-.1*t)),
        }
    assert out["point_far_H27"]["exact_infinite_time_average_offdiag"]!=out["line_transverse_null"]["exact_infinite_time_average_offdiag"]
    return out


def levi_graph():
    pts, lines=projective_points_and_lines()
    graph=nx.Graph()
    graph.add_nodes_from(range(80))
    index={p:i for i,p in enumerate(pts)}
    for li,line in enumerate(lines):
        for p in line:
            graph.add_edge(index[p],40+li)
    assert graph.number_of_edges()==160 and nx.is_connected(graph)
    return graph


def find_eight_cycle(g):
    root=0
    def visit(path):
        curr=path[-1]
        if len(path)==8:
            return path if root in g[curr] else None
        for nxt in sorted(g[curr]):
            if nxt not in path:
                ans=visit(path+[nxt])
                if ans is not None:return ans
        return None
    cyc=visit([root])
    assert cyc is not None and len(cyc)==8
    return cyc


def add_modular_basis(mat,basis,p):
    vec=(mat%p).reshape(-1).tolist()
    for pivot,v in basis:
        if vec[pivot]:
            c=vec[pivot]
            vec=[(a-c*b)%p for a,b in zip(vec,v)]
    for k,x in enumerate(vec):
        if x:
            inv=pow(x,-1,p)
            vec=[(v*inv)%p for v in vec]
            basis.append((k,vec))
            basis.sort(key=lambda x:x[0])
            return True
    return False


def rational_eight_cycle_closure_dimension():
    """Exact Q Gaussian elimination of all commutator words on C8."""
    n=8
    generators=[]
    for i in range(n):
        j=(i+1)%n
        a=np.zeros(n,dtype=object)
        b=np.zeros(n,dtype=object)
        a[i]=a[j]=1
        b[i]=1
        b[j]=-1
        generators.append(np.outer(a,b))
    basis=[]
    def add(mat):
        v=[Q(int(x)) for x in mat.reshape(-1)]
        for pivot,row in basis:
            c=v[pivot]
            if c:
                v=[x-c*y for x,y in zip(v,row)]
        pivot=next((i for i,x in enumerate(v) if x),None)
        if pivot is None:return False
        denom=v[pivot]
        basis.append((pivot,[x/denom for x in v]))
        basis.sort(key=lambda x:x[0])
        return True
    found=[]
    for gen in generators:
        if add(gen):found.append(gen)
    for x in found:
        for gen in generators:
            comm=x@gen-gen@x
            if add(comm):found.append(comm)
    return len(found)


def lie_frontier():
    g=levi_graph()
    cycle=find_eight_cycle(g)
    n=8;p=101
    gen=[]
    for k in range(n):
        j=(k+1)%n
        left=np.zeros(n,dtype=np.int64)
        right=np.zeros(n,dtype=np.int64)
        left[k]=left[j]=1
        right[k]=1;right[j]=-1
        gen.append(np.outer(left,right))
    ones=np.ones(n,dtype=np.int64)
    signs=np.array([1 if cycle[i]<40 else -1 for i in range(n)])
    assert signs.sum()==0
    mats=[];basis=[]
    for x in gen:
        if add_modular_basis(x,basis,p): mats.append(x%p)
    initial=len(mats)
    for x in mats:
        for b in gen:
            br=(x@b-b@x)%p
            if add_modular_basis(br,basis,p):
                assert np.array_equal(br@ones%p,np.zeros(n,dtype=np.int64))
                assert np.array_equal(signs@br%p,np.zeros(n,dtype=np.int64))
                assert np.trace(br)%p==0
                mats.append(br)
            if len(mats)>60:raise AssertionError("Lie closure unexpectedly large")
    assert all(np.all(x@ones%p==0) and np.all(signs@x%p==0)
               and np.trace(x)%p==0 for x in mats)
    # Exact codimension count: M 1=0 and signs^T M=0 impose 2n-1
    # independent constraints. Trace=0 adds one: max dim n^2-2n.
    ceiling=n*n-2*n
    assert len(mats)<=ceiling
    characteristic_zero_dim=rational_eight_cycle_closure_dimension()
    assert characteristic_zero_dim==len(mats)==34
    return {
        "characteristic_zero_lie_dimension":characteristic_zero_dim,
        "w33_levi_vertices":80,
        "w33_levi_edges":160,
        "explicit_induced_8_cycle":cycle,
        "cycle_nearest_edge_generators":initial,
        "cycle_lie_closure_dimension_mod_101":len(mats),
        "maximal_dimension_given_two_annihilators_and_trace":ceiling,
        "common_right_null_vector":"all-ones",
        "common_left_null_covector":"point/line alternating signs",
        "strict_nearest_neighbor_closure":len(mats)==initial,
        "claim_scope":"local induced C8, not a 4D hypersurface deformation algebra",
    }


def flag_frontier():
    g=levi_graph()
    flags=list(sorted(tuple(sorted(x)) for x in g.edges()))
    fg=nx.line_graph(g)
    assert fg.number_of_nodes()==160 and fg.number_of_edges()==480
    assert set(dict(fg.degree()).values())=={6}
    connected=nx.is_connected(fg)
    edge_connectivity=nx.edge_connectivity(fg)
    assert connected and edge_connectivity==6
    # Ferromagnetic H=-J sum_(xy) s_x s_y. Ground states all +- only.
    # A cut edge incurs +2J relative to a uniform state.
    # Smallest defect: a minimum nonempty cut.
    return {
        "flag_states":len(flags),
        "flag_graph_edges":fg.number_of_edges(),
        "degree":6,
        "minimum_domain_wall_cut_edges":edge_connectivity,
        "minimum_domain_wall_energy_over_J":2*edge_connectivity,
        "ferromagnetic_ground_state_count":2,
        "spontaneous_sign_selection":False,
        "qualifier":"supplied graph-Ising action, no spacetime domain wall dynamics",
    }


Z6={"Q":0,"Uc":1,"Dc":5,"L":4,"Ec":1,"Nc":3,"Hu":5,"Hd":1,"Sminus2":0}
OPS={
    "up_yukawa":("Q","Uc","Hu"),
    "down_yukawa":("Q","Dc","Hd"),
    "charged_lepton_yukawa":("L","Ec","Hd"),
    "neutrino_yukawa":("L","Nc","Hu"),
    "mu":("Hu","Hd"),
    "majorana":("Nc","Nc"),
    "weinberg":("L","L","Hu","Hu"),
    "majorana_with_Sminus2":("Nc","Nc","Sminus2"),
    "bilinear_LHu":("L","Hu"),
    "UDD":("Uc","Dc","Dc"),
    "QLD":("Q","L","Dc"),
    "LLE":("L","L","Ec"),
    "QQQL":("Q","Q","Q","L"),
    "UUDE":("Uc","Uc","Dc","Ec")
}
ALLOW={"up_yukawa","down_yukawa","charged_lepton_yukawa",
       "neutrino_yukawa","mu","majorana","weinberg","majorana_with_Sminus2"}
VETO=set(OPS)-ALLOW


def p6_frontier():
    charges={k:sum(Z6[x] for x in v)%6 for k,v in OPS.items()}
    assert all(charges[x]==0 for x in ALLOW)
    assert all(charges[x]!=0 for x in VETO)
    # Only a *necessary* integer modular check, not a full discrete
    # Green-Schwarz, gravitational or worldsheet anomaly certificate.
    su3=sum(3*(2*Z6["Q"]+Z6["Uc"]+Z6["Dc"]) for _ in range(1))
    su2=3*(3*Z6["Q"]+Z6["L"])+Z6["Hu"]+Z6["Hd"]
    gr=3*(6*Z6["Q"]+3*Z6["Uc"]+3*Z6["Dc"]+2*Z6["L"]+Z6["Ec"]+Z6["Nc"])+2*(Z6["Hu"]+Z6["Hd"])
    assert all(a%6==0 for a in (su3,su2,gr))
    # Construct consistency search across N=2,...,6. Parameterize using
    # yukawas, neutrino Yukawa, mu, Majorana and test 6 dangerous operators.
    counts={}
    samples={}
    for n in range(2,7):
        candidates=[]
        for q,l,hu,nc in itertools.product(range(n),repeat=4):
            hd=(-hu)%n
            uc=(-q-hu)%n
            dc=(-q+hu)%n
            ec=(-l+hu)%n
            if (l+nc+hu)%n or (2*nc)%n:continue
            c={"Q":q,"L":l,"Hu":hu,"Hd":hd,"Uc":uc,"Dc":dc,"Ec":ec,"Nc":nc}
            if all(sum(c[x] for x in OPS[o])%n for o in VETO):
                candidates.append(c)
        counts[str(n)]=len(candidates)
        if candidates:samples[str(n)]=candidates[0]
    assert counts["6"]>0
    return {
        "known_proton_hexality_Z6":Z6,
        "operator_Z6_residues":charges,
        "allowed_operators":sorted(ALLOW),
        "vetoed_operators":sorted(VETO),
        "mixed_mod6_necessary_sums":{"SU3":su3,"SU2":su2,"gravitational":gr},
        "charge_filter_candidate_counts_N2_to_N6":counts,
        "Sminus2_preserves_Z6_if_vev":True,
        "Nc_vev_breaks_Z6_to_Z3":True,
        "scope":"operator-level candidate filters only; no compactification constructed or discrete anomaly sufficiency certified",
    }


def kinetic_inverse_sqrt(k):
    w,v=np.linalg.eigh(k)
    assert min(w)>0
    return (v*(w**-.5))@v.conj().T


def mixing_observables(yu,yd):
    l_u=np.linalg.eigh(yu@yu.conj().T)[1]
    l_d=np.linalg.eigh(yd@yd.conj().T)[1]
    v=l_u.conj().T@l_d
    j=float(np.imag(v[0,0]*v[1,1]*np.conj(v[0,1]*v[1,0])))
    mu=sorted(np.linalg.svd(yu,compute_uv=False))
    md=sorted(np.linalg.svd(yd,compute_uv=False))
    return {"up_masses":mu,"down_masses":md,"Jarlskog":j}


def flavor_frontier():
    # These holomorphic matrices and metrics are *supplied controls*.
    yu=np.diag([.5,.2,.05]).astype(complex)
    yd=np.array([[.08,.02j,.003],[.015,.04,.007j],[.001,.01,.03]],complex)
    kq=np.diag([1.,4.,9.]);ku=np.diag([2.,1.,3.]);kd=np.diag([1.,2.,4.])
    def normalize(a,b,c):
        return kinetic_inverse_sqrt(a)@yu@kinetic_inverse_sqrt(b),kinetic_inverse_sqrt(a)@yd@kinetic_inverse_sqrt(c)
    canonical=mixing_observables(*normalize(kq,ku,kd))
    naive=mixing_observables(yu,yd)
    assert abs(canonical["Jarlskog"]-naive["Jarlskog"])>1e-7
    rng=np.random.default_rng(20261008)
    zz=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    q,r=np.linalg.qr(zz)
    q=q@np.diag(np.exp(-1j*np.angle(np.diag(r))))
    yl,dl=normalize(kq,ku,kd)
    yl2=kinetic_inverse_sqrt(q@kq@q.conj().T)@(q@yu)@kinetic_inverse_sqrt(ku)
    dl2=kinetic_inverse_sqrt(q@kq@q.conj().T)@(q@yd)@kinetic_inverse_sqrt(kd)
    rotated=mixing_observables(yl2,dl2)
    assert np.allclose(rotated["up_masses"],canonical["up_masses"],atol=1e-12)
    assert np.allclose(rotated["down_masses"],canonical["down_masses"],atol=1e-12)
    assert abs(rotated["Jarlskog"]-canonical["Jarlskog"])<1e-12
    # A single certified holomorphic coefficient cannot by itself give
    # nonzero rank-3 masses. Invertible metrics preserve rank.
    only_cert=np.diag([.5,0.,0.])
    assert np.linalg.matrix_rank(kinetic_inverse_sqrt(kq)@only_cert@kinetic_inverse_sqrt(ku))==1
    g1,g2,g3=.357,.65,1.16
    def beta(_scale,y):
        return y*(4.5*y*y-(17/12)*g1*g1-2.25*g2*g2-8*g3*g3)/(16*np.pi*np.pi)
    sol=solve_ivp(beta,[np.log(173.),np.log(1000.)],[.94],rtol=1e-11,atol=1e-12)
    assert sol.success
    return {
        "supplied_Yu":yu.real.tolist(),
        "supplied_Yd_real":yd.real.tolist(),
        "supplied_Yd_imag":yd.imag.tolist(),
        "supplied_kinetic_diagonal":{"Q":[1,4,9],"U":[2,1,3],"D":[1,2,4]},
        "bare_example":naive,
        "canonically_normalized_example":canonical,
        "unitary_left_frame_invariance_error_J":abs(rotated["Jarlskog"]-canonical["Jarlskog"]),
        "single_certified_entry_rank_after_invertible_normalization":1,
        "toy_1loop_top_beta_fixed_gauge":{"mu_initial_GeV":173,"mu_final_GeV":1000,
              "y_initial":.94,"y_final":float(sol.y[0,-1]),
              "supplied_fixed_gauge_couplings":[g1,g2,g3]},
        "not_a_physical_prediction":"kinetic metrics, holomorphic textures and gauge parameters supplied; no actual Ricci-flat/HYM solution",
    }


def sixth_discrimination():
    # Contrast earlier entanglement-breaking 2-step channel, depolarizing
    # measurement noise and photon loss. This is a bound for a *known*
    # tested pair, not an unknown-label classifier.
    raw=Q(1,64)
    eta=Q(1,10)
    conditional_gap=(1-eta)*raw
    delta=.05
    shots=math.ceil(2*math.log(2/delta)/float(conditional_gap)**2)
    gamma=.1;t=.43
    survival=math.exp(-gamma*t)
    shots_unconditional=math.ceil(shots/survival**2)
    return {"two_step_known_pair_gap_no_noise":str(raw),
            "depolarizing_eta":str(eta),
            "conditional_detection_gap":str(conditional_gap),
            "Hoeffding_two_sided_error_target":delta,
            "sufficient_shots_per_known_pair_no_loss":shots,
            "sufficient_pre_loss_trials_conservative":shots_unconditional,
            "assumptions":"known discriminating pair, independent trials, exact engineered graph transition, symmetric readout noise and uniform survival"}


def transport_duality_frontier():
    """Seventh: cross-tab classical Green resistance with quantum mixing."""
    from w33_20261008_dual_27_electrical_transport import bfs_distances
    out={}
    for name,a in build_graphs().items():
        L=8*np.eye(27,dtype=np.int64)-a
        numerator=13*(L@L@L)-315*(L@L)+2070*L
        projectors=spectral_projectors(a)
        pairs=Counter()
        for i in range(27):
            dist=bfs_distances(a,i)
            for j in range(i+1,27):
                resistance=Q(int(numerator[i,i]+numerator[j,j]-2*numerator[i,j]),23328)
                qmix=sum(Q(int(num[i,j]*num[i,j]),den*den)
                         for num,den in projectors.values())
                pairs[(dist[j],str(resistance),str(qmix))]+=1
        out[name]=[
            {"distance":k[0],"resistance":k[1],"coherent_time_mean":k[2],"unordered_pairs":cnt}
            for k,cnt in sorted(pairs.items())]
        assert sum(x["unordered_pairs"] for x in out[name])==351
    vals=out["point_far_H27"]
    distant=next(x for x in vals if x["distance"]==3)
    two=next(x for x in vals if x["distance"]==2)
    coherent_ratio=Q(distant["coherent_time_mean"])/Q(two["coherent_time_mean"])
    assert coherent_ratio==Q(220,13)
    return {"cross_tabulation":out,
            "point_d3_to_d2_time_mean_ratio":str(coherent_ratio),
            "scope":"effective resistance is classical, time-averaged mixing is unitary; neither identifies physical conductances"}


def build():
    return {
      "scope":"exact finite constructions and supplied toy actions; no complete TOE",
      "coherent_quantum_walk":coherent_frontier(),
      "local_constraint_lie_algebra":lie_frontier(),
      "chirality_flag_domain_walls":flag_frontier(),
      "heterotic_proton_hexality_filter":p6_frontier(),
      "kinetic_normalization_flavor":flavor_frontier(),
      "operational_shot_budget":sixth_discrimination(),
      "classical_quantum_transport_cross_tab":transport_duality_frontier()
    }


def main():
    a=build()
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(a,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for k,v in a.items():
        if k!="scope":print("FRONT",k,json.dumps(v,sort_keys=True))
    print("SIX_FRONTIERS_SUCCESS")
    return a

if __name__=="__main__":
    main()
