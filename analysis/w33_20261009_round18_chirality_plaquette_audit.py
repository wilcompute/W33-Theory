"""Native W33 girth-eight holonomy, orientation-sensitive trace, and
finite-size time-reversal obstruction. Frustrated plaquette potential is
a CONSTRUCTED toy action, not an induced microphysical TOE mechanism.
"""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261009_round17_interaction_trace_certificate as old
from w33_20261008_5state_ritz import geometry
P=1000003
def cycles_touching(edges,edge_id):
    adj=[[] for _ in range(80)]
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    p,l=edges[edge_id]
    cycles=set()
    def walk(path):
        if len(path)==8:
            if path[-1] in adj[p]:
                cycle=tuple(path) # p,l,...,node7,p (8 edges)
                # canonical dihedral cyclic representation
                rot=[tuple(cycle[i:]+cycle[:i]) for i in range(8)]
                rev=cycle[::-1]
                rot.extend(tuple(rev[i:]+rev[:i]) for i in range(8))
                cycles.add(min(rot))
            return
        for next in adj[path[-1]]:
            if next!=p and next not in path:walk(path+[next])
    walk([p,l])
    return cycles

def zz_mul(x,y,p=P):
    a,b=x;c,d=y
    return ((a@c-b@d)%p,(a@d+b@c)%p)
def deriv_trace(edges,rep,sign=1,n=8,slot=0):
    old.MOD=P
    aa,bb=old.phased_adj(edges,rep)
    bb=(bb*sign)%P
    X=(aa,bb)
    ident=(np.eye(80,dtype=np.int64),np.zeros((80,80),dtype=np.int64))
    power=ident
    for _ in range(n-1):power=zz_mul(power,X)
    f=rep[slot];a,b=edges[f];u=int(aa[a,b]);v=int(bb[a,b])
    dR=np.zeros((80,80),dtype=np.int64);dI=np.zeros((80,80),dtype=np.int64)
    dR[a,b]=dR[b,a]=(-v)%P
    dI[a,b]=u;dI[b,a]=(-u)%P
    r,i=zz_mul(power,(dR,dI))
    assert int(np.trace(i)%P)==0
    return int(n*np.trace(r)%P)

def main():
    edges,*_=geometry()
    reps=json.loads((ROOT/"data/w33_20261009_PSp_orbits_isotropic_triplets.json").read_text())['orbits']
    counts=[len(cycles_touching(edges,j)) for j in range(len(edges))]
    assert len(edges)==160 and len(set(counts))==1 and counts[0]>0
    total=sum(counts)//8
    # Paths of lengths<8 cannot be incidence cycles of a generalized quadrangle.
    oriented=[]
    for rep in reps:
        r=rep['representative']
        plus=[deriv_trace(edges,r,1,8,k) for k in range(3)]
        minus=[deriv_trace(edges,r,-1,8,k) for k in range(3)]
        assert all((x+y)%P==0 for x,y in zip(plus,minus)),(plus,minus)
        oriented.append(dict(rep=r,first_even_moment=8,phase_current_mod_p=plus,reverse=minus))
    assert any(any(x["phase_current_mod_p"]) for x in oriented)
    # Place a single physical oriented edge phase phi, freeze all other edges.
    # Each elementary 8-cycle touching the edge carries +/-phi.
    # F(phi)=K*g*cos(2phi), g>0: two minima +/-pi/2, both positive curvature.
    K=counts[0]
    result=dict(status="PASS",graph_vertices=80,graph_edges=len(edges),
        edge_cycle8_incidence_distribution=sorted(set(counts)),unique_8cycles=total,
        all_edge_counts_equal=True,prime=P,cycle_derived_currents=oriented,
        signed_flux_current="d Tr A(phi)^8 / d phi_e is odd under simultaneous phase reversal and nonzero at rational phases. Gauge-orientation convention needed for sign.",
        autonomous_toy_plaquette_energy=f"F(phi)={K}*g*cos(2phi), g>0, for one unfrozen edge phase",
        degenerate_minima=["+pi/2","-pi/2"],hessian_minimum=f"{4*K}*g",
        time_reversal_nogo="An exact T-symmetric finite Hamiltonian cannot uniquely select a nonzero T-odd current in a nondegenerate T-invariant ground state; a symmetry-breaking preparation, environment, or thermodynamic limit is necessary.",
        scope="Native 8-cycles; one active-edge flux while all other gauge links are frozen is an engineered toy action. No field equations, optical experiment, or spontaneous quantum T-breaking demonstrated.")
    out=ROOT/'data/w33_20261009_round18_chirality_plaquette_audit.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print("CYCLES",K,total,"CURRENTS",[v['phase_current_mod_p'] for v in oriented])
if __name__=='__main__':main()
