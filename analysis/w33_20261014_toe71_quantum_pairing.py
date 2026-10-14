"""TOE71: automorphism-invariant 3-state vertex pairing quantum Hamiltonian.

Full Hilbert dimension 3^80; exact cycle-count potential and democratic
local transitions define an invariant finite quantum model, not gravity.
Exact 160 single flips + 4*C(80,2) double flips; four-vertex (3^4=81)
Galerkin sectors are small, deliberately symmetry-breaking controls.
"""
from pathlib import Path
from collections import Counter
import itertools,json,sys
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons,COVER

def geometry():
    ed,adj,cycles=octagons()
    owner={e:i for i,c in enumerate(COVER) for e in cycles[c]}
    assert len(owner)==160
    choices=[];initial=[]
    for v in range(80):
        a,b,c,d=sorted(e for neighbor,e,sg in adj[v])
        opts=(((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c)))
        expected={frozenset((x,y)) for x,y in itertools.combinations((a,b,c,d),2)
                  if owner[x]==owner[y]}
        z=next(i for i,op in enumerate(opts)
               if {frozenset(x) for x in op}==expected)
        initial.append(z);choices.append(opts)
    return ed,adj,choices,initial

def loop_count(config,ed,adj,choices):
    route={}
    for v,k in enumerate(config):
        for a,b in choices[v][k]:
            route[v,a]=b;route[v,b]=a
    seen=set();directed=0
    for v in range(80):
        for n,e,s in adj[v]:
            if (v,e) in seen:continue
            directed+=1;u=v;incoming=e
            while (u,incoming) not in seen:
                seen.add((u,incoming))
                outgoing=route[u,incoming]
                a,b=ed[outgoing]
                u=b if a==u else a;incoming=outgoing
    assert len(seen)==320 and directed%2==0
    return directed//2

def certificate():
    ed,adj,choices,initial=geometry()
    assert loop_count(initial,ed,adj,choices)==20
    single=Counter();pair=Counter();ground_pair=[]
    for v in range(80):
        for z in range(3):
            if z==initial[v]:continue
            state=initial.copy();state[v]=z
            single[loop_count(state,ed,adj,choices)]+=1
    assert single=={19:160}
    for a,b in itertools.combinations(range(80),2):
        for i in range(3):
            if i==initial[a]:continue
            for j in range(3):
                if j==initial[b]:continue
                state=initial.copy();state[a]=i;state[b]=j
                N=loop_count(state,ed,adj,choices)
                pair[N]+=1
                if N==20:ground_pair.append((a,b,i,j))
    assert pair=={18:12628,19:6,20:6}
    assert len(ground_pair)==6
    # Explicit small quantum Galerkin sectors of
    # H = -J Nloops -t sum_v sum_{a!=b}|a><b|_v.
    # The full model is invariant under graph automorphisms because both
    # loop count and the complete-graph onsite flip matrix are invariant
    # under any relabelling of the three pairings at each site.
    sectors=[]
    active=(0,40,4,1)
    for n in (2,3,4):
        touched=active[:n]
        states=list(itertools.product(range(3),repeat=n))
        counts=[]
        for z in states:
            state=initial.copy()
            for v,j in zip(touched,z):state[v]=j
            counts.append(loop_count(state,ed,adj,choices))
        for t in (.05,.2,.5):
            H=np.diag(-np.asarray(counts,dtype=float))
            for i,z in enumerate(states):
                for j,y in enumerate(states):
                    if sum(a!=b for a,b in zip(z,y))==1:H[i,j]=-t
            val,vec=eigh(H)
            avg=float(np.dot(np.asarray(counts),vec[:,0]**2))
            sectors.append({"active_vertices":list(touched),"states":len(states),
              "t_over_J":t,"ground_energy_over_J":float(val[0]),
              "first_gap_over_J":float(val[1]-val[0]),
              "ground_expected_loops":avg})
    target=next(s for s in sectors if s["states"]==81 and s["t_over_J"]==.2)
    assert abs(target["ground_energy_over_J"]+20.35959179422655)<1e-9
    return {
      "status":"PASS_TOE71_PAIRING_QUANTUM_TUNNELING",
      "native_degree_four_vertices":80,"state_choices_per_vertex":3,
      "full_model_Hilbert_dimension":"3^80",
      "classical_exact_cover_loops":20,
      "all_single_vertex_alternatives":160,
      "single_vertex_new_loop_counts":{str(k):v for k,v in single.items()},
      "all_two_vertex_alternatives":12640,
      "two_vertex_new_loop_counts":{str(k):v for k,v in pair.items()},
      "two_vertex_new_twenty_loop_configurations":[list(x) for x in ground_pair],
      "universal_second_order_diagonal_shift_of_each_twenty_loop_cover":"-160*t^2/J, prior to diagonalizing the degenerate 20-loop manifold",
      "automorphism_invariant_full_hamiltonian":"H=-J*N_loops-t*sum_v sum_{a!=b}|a><b|_v, J>0, t>=0",
      "restricted_quantum_sectors":sectors,
      "qualification":"4 selected active vertices are NOT symmetry invariant; their small exact eigenspectra are controls, not the 3^80 full quantum spectrum or emergence of spacetime. Full Hamiltonian symmetry is exact by graph combinatorics."
    }
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe71_quantum_pairing.json").write_text(
      json.dumps(c,indent=2)+"\n",encoding="utf-8")
    print(c["status"],c["two_vertex_new_loop_counts"])
