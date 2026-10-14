"""TOE72 exact 70-state W33 native-octagon repulsion vs unrestricted HF.

Actual 8-cycle carries one of the TOE67 marked nonzero Z2 fluxes.
Exact fixed N=4 many-body sparse/dense diagonalization (70 Slater
basis determinants) and sitewise HF on EXACT SAME 8-site graph.
The two gaps are distinct observables: canonical many-body excitation
vs HF one-body particle-hole eigenvalue gap. Finite symmetry unbroken.
"""
from pathlib import Path
import itertools,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons,windings

def matrices():
    ed,adj,cycles=octagons()
    marker=dict(windings(cycles,ed))
    cycle_id=next(i for i,w in sorted(marker.items()) if w==(1,0,0))
    assert cycle_id==111
    cycle=cycles[cycle_id]
    vertices=sorted({v for e in cycle for v in ed[e]})
    assert len(vertices)==8
    idx={v:i for i,v in enumerate(vertices)}
    links=[(idx[ed[e][0]],idx[ed[e][1]],-1 if e in (59,93,139) else 1)
           for e in cycle]
    A=np.zeros((8,8));H0=np.zeros((8,8))
    for a,b,phase in links:
        A[a,b]=A[b,a]=1
        H0[a,b]=H0[b,a]=-phase
    assert np.all(A.sum(axis=0)==2)
    fock=[x for x in range(256) if x.bit_count()==4]
    lookup={x:i for i,x in enumerate(fock)}
    stagger=np.array([1 if v<40 else -1 for v in vertices])
    free=np.zeros((70,70));pairenergy=np.zeros(70);M=np.zeros(70)
    for i,bits in enumerate(fock):
        occ=np.array([(bits>>j)&1 for j in range(8)])
        M[i]=stagger@(occ-.5)
        for a,b,phase in links:
            pairenergy[i]+=(occ[a]-.5)*(occ[b]-.5)
            if occ[a]==occ[b]:continue
            dest=bits^(1<<a)^(1<<b)
            parity=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
            free[i,lookup[dest]]+=-phase*parity
    assert np.allclose(free,free.T)
    assert np.prod([z for _,_,z in links])==-1
    return vertices,cycle,links,H0,A,stagger,free,pairenergy,M

def exact(V,free,inter,M):
    eig,u=np.linalg.eigh(free+np.diag(V*inter))
    prob=u[:,0]**2
    return {"V":V,"many_body_ground_energy":float(eig[0]),
      "exact_fixed_N_first_gap":float(eig[1]-eig[0]),
      "exact_staggered_mean":float(M@prob),
      "exact_staggered_second_moment":float((M*M)@prob),
      "exact_abs_staggered_moment":float(abs(M)@prob),
      "ground_eigen_residual":float(np.linalg.norm(
          (free+np.diag(V*inter))@u[:,0]-eig[0]*u[:,0]))}

def hf(V,links,H0,A,stagger,seed=.2):
    eig,u=np.linalg.eigh(H0+np.diag(seed*stagger))
    rho=u[:,:4]@u[:,:4].T
    for step in range(1000):
        d=np.diag(rho)-.5
        H=H0+V*np.diag(A@d)-V*A*rho
        eig,u=np.linalg.eigh(H)
        nr=u[:,:4]@u[:,:4].T
        residual=float(np.max(abs(nr-rho)))
        if residual<1e-11:
            rho=nr;break
        rho=.45*nr+.55*rho
    assert residual<1e-11
    d=np.diag(rho)-.5
    energy=float(np.trace(H0@rho)+V*sum(
        d[a]*d[b]-rho[a,b]**2 for a,b,_ in links))
    return {"HF_variational_energy":energy,
      "HF_one_particle_hole_gap":float(eig[4]-eig[3]),
      "HF_staggered_mean":float(stagger@d),
      "fixed_point_max_residual":residual,
      "HF_iterations":step+1}

def certificate():
    vertices,cycle,links,H0,A,stagger,free,inter,M=matrices()
    rows=[]
    for V in (.2,.5,1.,2.,4.,8.):
        a=exact(V,free,inter,M)
        b=hf(V,links,H0,A,stagger)
        assert a["many_body_ground_energy"]<=b["HF_variational_energy"]+1e-9
        assert abs(a["exact_staggered_mean"])<1e-10
        assert a["ground_eigen_residual"]<1e-11
        rows.append({**a,**b})
    assert abs(rows[3]["exact_fixed_N_first_gap"]-1.045348690185)<1e-10
    assert abs(rows[3]["HF_one_particle_hole_gap"]-2.96310871745998)<1e-8
    assert rows[-1]["exact_fixed_N_first_gap"]<.13
    assert rows[-1]["HF_one_particle_hole_gap"]>15
    assert all(rows[i+1]["exact_staggered_second_moment"]>
               rows[i]["exact_staggered_second_moment"] for i in range(5))
    return {
      "status":"PASS_TOE72_EXACT_NATIVE_INTERACTION_VS_HF",
      "native_octagon_id":111,
      "native_vertex_indices":vertices,
      "native_edge_indices":list(cycle),
      "native_deck_winding":[1,0,0],
      "edge_sign_product_pi":-1,
      "spinless_fermions":4,
      "fixed_particle_many_body_dimension":70,
      "Hamiltonian":"H=-sum_native_edges (s_e c_i^dagger c_j+h.c.) + V sum_edges(n_i-1/2)(n_j-1/2)",
      "comparison":"Exact N=4 many-body first excitation gap vs HF one-body occupied-unoccupied eigenvalue gap; distinct quantities used only to assess mean-field gap inference.",
      "runs":rows,
      "key_caveat":"Exact unique finite octagon ground preserves sublattice-exchange symmetry and <M>=0; increasing <M^2> indicates enhanced fluctuations, not proven thermodynamic spontaneous ordering. Mean-field HF broken branch at large V overstates the first exact excitation gap; these are finite-size physics controls, not 80-site interacting theory."
    }

if __name__=="__main__":
    o=certificate()
    (ROOT/"data/w33_20261014_toe72_exact_interacting_octagon.json").write_text(json.dumps(o,indent=2)+"\n")
    print(o["status"],o["runs"][-1]["exact_fixed_N_first_gap"])
