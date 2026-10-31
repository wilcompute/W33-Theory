#!/usr/bin/env python3
"""Native W33 two-qutrit Temperley-Lieb-Jones q=e^(i pi/6) realization.

Physical boundary: finite Clifford braid representation, NOT physical anyons,
not a topologically protected device and not braiding-universal.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import networkx as nx
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12055_microscopic_tick_model import PROJ, PTS, ADJ, w as omega, pauli

OUT=ROOT/"data/w33_20261031_native_tlj_metaplectic_chain.json"

def frob(X): return float(np.linalg.norm(X))
def build():
    I=np.eye(9,dtype=complex); delta=math.sqrt(3)
    projectors=np.array([PROJ[p][0] for p in range(40)])
    projective_controls={"noncommuting_pairs":0,"commuting_pairs":0}
    for i in range(40):
        assert frob(projectors[i]@projectors[i]-projectors[i])<1e-12
        assert abs(np.trace(projectors[i])-3)<1e-12
        for j in range(i+1,40):
            P,Q=projectors[[i,j]]
            if ADJ[i,j]:
                projective_controls["commuting_pairs"]+=1
                assert frob(P@Q-Q@P)<1e-12
            else:
                projective_controls["noncommuting_pairs"]+=1
                assert frob(P@Q@P-P/3)<1e-12
                assert frob(Q@P@Q-Q/3)<1e-12
    assert projective_controls=={"noncommuting_pairs":540,"commuting_pairs":240}
    # Induced path in the noncommutation graph; distant generators commute.
    def seek(path,depth):
        if len(path)==depth:return path
        for j in range(40):
            if j in path or ADJ[path[-1],j]:continue
            if all(ADJ[j,k] for k in path[:-1]):
                result=seek(path+[j],depth)
                if result:return result
        return None
    path=seek([0],5)
    assert path is not None and len(path)==5
    e=[delta*projectors[i] for i in path]
    for k in range(5):assert frob(e[k]@e[k]-delta*e[k])<1e-12
    for k in range(4):
        assert frob(e[k]@e[k+1]@e[k]-e[k])<1e-12
        assert frob(e[k+1]@e[k]@e[k+1]-e[k+1])<1e-12
    for i in range(5):
        for j in range(i+2,5):
            assert frob(e[i]@e[j]-e[j]@e[i])<1e-12
    theta=math.pi/6
    qinteger=lambda n:math.sin(n*theta)/math.sin(theta)
    # f_m is Jones-Wenzl projector in the TL algebra of m strands.
    f=I.copy()
    jw=[]
    for n in range(1,5):
        f=f-(qinteger(n)/qinteger(n+1))*f@e[n-1]@f
        assert frob(f@f-f)<1e-11
        jw.append({"strands":n+1,"rank":int(np.linalg.matrix_rank(f,tol=1e-8)),
                   "trace_real":float(np.trace(f).real),"idempotence_error":frob(f@f-f)})
    assert [q["rank"] for q in jw]==[6,3,1,0]
    assert frob(f)<1e-11
    A=np.exp(1j*5*math.pi/12)
    assert abs(delta + A**2+A**-2)<1e-12
    braid=[A*I+e[i]/A for i in range(5)]
    braid_point_actions=[]
    for i,R in enumerate(braid):
        assert frob(R.conj().T@R-I)<1e-12
        tick=I+(omega-1)*(I-projectors[path[i]])
        assert frob(R-np.exp(-1j*math.pi/4)*tick)<1e-12
        assert frob(tick@tick@tick-I)<1e-12
        action=[]
        for v in PTS:
            Y=R@pauli(v)@R.conj().T
            found=None
            for j,w in enumerate(PTS):
                U=pauli(w)
                c=np.trace(U.conj().T@Y)/9
                if abs(abs(c)-1)<1e-11 and frob(Y-c*U)<1e-10:
                    found=j;break
                c=np.trace(U@Y)/9
                if abs(abs(c)-1)<1e-11 and frob(Y-c*U.conj().T)<1e-10:
                    found=j;break
            assert found is not None
            action.append(found)
        assert sorted(action)==list(range(40))
        braid_point_actions.append(tuple(action))
    for i in range(4): assert frob(braid[i]@braid[i+1]@braid[i]-braid[i+1]@braid[i]@braid[i+1])<1e-11
    for i in range(5):
        for j in range(i+2,5):
            assert frob(braid[i]@braid[j]-braid[j]@braid[i])<1e-11
    # Chern/anyon caveat: finite 9D Clifford image has no intrinsic anyon
    # fusion spaces or locality-protected winding. No universality by braids.
    G=nx.from_numpy_array(ADJ)
    C=nx.complement(G)
    maximal= list(nx.find_cliques(C))
    lengths={}
    for cl in maximal: lengths[str(len(cl))]=lengths.get(str(len(cl)),0)+1
    assert lengths=={"4":90,"7":2880}
    witness=max(maximal,key=len)
    assert len(witness)==7 and all(ADJ[i,j]==0 for i,j in itertools.combinations(witness,2))
    # Exhaust every ordered induced P5 of the noncommutation graph.
    # Consecutive projectors obey TL Jones triples; distant ones commute.
    def enumerate_paths(length):
        result=[]
        def visit(seq):
            if len(seq)==length:result.append(tuple(seq));return
            for nxt in range(40):
                if nxt in seq or ADJ[seq[-1],nxt]:continue
                if all(ADJ[k,nxt] for k in seq[:-1]):visit(seq+[nxt])
        for start in range(40):visit([start])
        return result
    four=enumerate_paths(4)
    five=enumerate_paths(5)
    six=enumerate_paths(6)
    assert (len(four),len(five),len(six))==(25920,25920,0)
    # Projective symplectic transvections: their action is *not* a
    # numerical coincidence with the number of braid chains.
    from w33_pass12055_microscopic_tick_model import FORM
    idx={tuple(v):j for j,v in enumerate(PTS)}
    def norm(v):
        a=next(x for x in v if x)
        return tuple((x*pow(int(a),-1,3))%3 for x in v)
    def transvection(v):
        return tuple(idx[norm(tuple((x[k]+FORM(x,v)*v[k])%3 for k in range(4)))]
                     for x in PTS)
    tvectors=[tuple(PTS[i]) for i in path]  # the SAME five native braid directions generate PSp(4,3)
    gens=[transvection(v) for v in tvectors]
    assert all(act==g or act==tuple(g.index(i) for i in range(40))
               for act,g in zip(braid_point_actions,gens))
    assert all(all(ADJ[i,j]==ADJ[g[i],g[j]] for i in range(40) for j in range(40))
               for g in gens)
    orbit={tuple(path)};todo=[tuple(path)]
    for seq in todo:
        for g in gens:
            new=tuple(g[i] for i in seq)
            if new not in orbit:orbit.add(new);todo.append(new)
    assert len(orbit)==len(five)==25920 and orbit==set(five)
    # An actual entangling two-qutrit Jones braid: X tensor X.
    cross=PTS.index((1,1,0,0))
    Pcross=projectors[cross]
    Rcross=I+(omega-1)*(I-Pcross)
    product_basis=np.zeros(9,dtype=complex);product_basis[0]=1
    state=(Rcross@product_basis).reshape(3,3)
    schmidt=np.linalg.svd(state,compute_uv=False)
    assert np.max(abs(schmidt**2-np.ones(3)/3))<1e-12
    rho=state@state.conj().T
    assert frob(rho-np.eye(3)/3)<1e-12
    return {"status":"PASS_NATIVE_9D_TEMPERLEY_LIEB_JONES_BRAID",
      "maximally_entangling_native_braid":{"Pauli_direction":[1,1,0,0],
         "input":"|0> tensor |0>", "Schmidt_probabilities":[float(x*x)for x in schmidt],
         "von_Neumann_entropy_nats":math.log(3),
         "gate":"Jones R is the native order-three Clifford tick up to global phase, here controlled by the X tensor X eigenprojector",
         "physical_limit":"Ideal two-qutrit register gate, not a protected anyonic fusion process"},
      "ordered_TL5_paths":{"length4":len(four),"length5":len(five),"length6":len(six),
          "projective_symplectic_orbit_size":len(orbit),
          "regular_PSp43_torsor":True,
          "transvection_generator_vectors":[list(v) for v in tvectors],
          "proof_method":"Exact enumerated induced-path census plus transvection BFS on actual 40 projective F3^4 directions"},
      "projector_pairs":projective_controls,
      "concrete_Pauli_indices":path,"concrete_Pauli_coordinates":[list(PTS[i]) for i in path],
      "TL":"e_i=sqrt(3) Pi_i, e_i^2=sqrt(3)e_i; e_i e_(i+1) e_i=e_i; distant generators commute",
      "root_of_unity":"q=exp(i pi/6), quantum loop dimension 2cos(pi/6)=sqrt(3), SU(2)_4 Jones parameter",
      "JW_projectors":jw,"level4_truncation":"f5=0 in this explicit 9D *-representation",
      "braid_formula":"R_i=A I + A^-1 e_i, A=exp(5 pi i/12); R_i=exp(-i pi/4)[I+(omega-1)(I-Pi_i)]",
      "projective_braid_image":"Exactly within native two-qutrit Clifford tick gates, hence no dense-braiding universality.",
      "full_40_point_Pauli_conjugacy_verified":True,
      "native_tick_count":120,
      "spatial_graph_packing":{"maximum_pairwise_noncommuting_Pauli_directions":7,
          "number_maximal_independent_sets_7":2880,
          "number_maximal_independent_sets_4":90,
          "complete_maximal_set_census":True,
          "witness_7":[int(x) for x in witness]},
      "spatial_interpretation":"Above the existing K=3J/2 noncommuting-bond preference threshold, any 7-site complete spatial graph can saturate all bonds using seven noncommuting directions; no 8-site complete graph can. This is a finite frustration/packing bound, not a vacuum derivation.",
      "novelty_boundary":"Temperley-Lieb/Jones and metaplectic SU2_4 are established mathematics; earlier repo already discussed these topics numerically. The specific canonical native 9D 120-projector chain, exact gate identification, braid and f5 controls, and packing census are this reproducible bridge. No anyon material or topological hardware."}

if __name__=="__main__":
    d=build()
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":d["status"],"path":d["concrete_Pauli_indices"],
       "JW_ranks":[r["rank"] for r in d["JW_projectors"]],
       "independence":d["spatial_graph_packing"]["maximum_pairwise_noncommuting_Pauli_directions"]}))
