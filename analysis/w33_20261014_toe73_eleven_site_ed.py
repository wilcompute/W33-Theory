"""TOE73 static native 11-site two-octagon exact spinless fermion many-body ED.

Full C(11,5)=462 number-conserving Fock sector, all 12 native edges,
two independent fundamental chord Z2 holonomies and repulsive nearest-
neighbor density interaction. This is NOT a dynamically gauged model.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch

def make_hamiltonian(p,twists,V,number=5):
    edges=p["p_ed"];chords=p["chords"];N=len(p["nodes"])
    states=[bits for bits in range(1<<N) if bits.bit_count()==number]
    idx={bits:i for i,bits in enumerate(states)}
    nn=len(states)
    occ=np.asarray([[(bits>>j)&1 for j in range(N)] for bits in states],float)
    interaction=np.asarray([
        sum((o[a]-.5)*(o[b]-.5) for a,b in edges) for o in occ])
    rows=list(range(nn));cols=list(range(nn));data=list(V*interaction)
    for i,bits in enumerate(states):
        for edge,(a,b) in enumerate(edges):
            if int(occ[i,a])==int(occ[i,b]):continue
            target=bits^(1<<a)^(1<<b)
            phase=-1 if edge in chords and twists[chords.index(edge)] else 1
            parity=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
            rows.append(i);cols.append(idx[target]);data.append(-phase*parity)
    H=coo_matrix((data,(rows,cols)),shape=(nn,nn)).tocsr()
    assert (H-H.T).nnz==0
    return H,occ,interaction

def trial(p,twists,V):
    H,occ,inter=make_hamiltonian(p,twists,V)
    eig,u=eigsh(H,k=3,which="SA",tol=1e-11,maxiter=12000)
    order=np.argsort(eig);e=eig[order];psi=u[:,order[0]]
    norm=float(np.linalg.norm(H@psi-e[0]*psi))
    assert norm<1e-7
    prob=psi**2
    # Finite-size density correlations are appropriate, unlike claims
    # of spontaneous order in an eleven-site quantum eigenstate.
    mean=np.asarray(prob@occ)
    star=np.asarray([1 if val else -1 for val in p["background"]],float)
    ordervar=(occ-.5)@star
    M=float(prob@ordervar)
    M2=float(prob@(ordervar**2))
    conn=float(np.mean([prob@(occ[:,a]*occ[:,b])-mean[a]*mean[b]
                        for a,b in p["p_ed"]]))
    return {
        "flipped_chord_Z2_twists":list(twists),"V":V,
        "dimension":H.shape[0],
        "E0":float(e[0]),"E1":float(e[1]),"E2":float(e[2]),
        "same_N_first_excitation_gap":float(e[1]-e[0]),
        "staggered_density_mean":M,
        "staggered_density_second_moment":M2,
        "average_native_edge_connected_density":conn,
        "max_ground_Ritz_residual":norm}

def certificate():
    p=patch()
    choices=list(itertools.product((0,1),repeat=2))
    interactions=(0.0,0.2,1.0,4.0)
    scans=[]
    for V in interactions:
        rows=[trial(p,twists,V) for twists in choices]
        winner=min(range(4),key=lambda j:rows[j]["E0"])
        assert all(r["dimension"]==462 and r["max_ground_Ritz_residual"]<1e-7 for r in rows)
        scans.append({"V":V,"sectors":rows,
                      "lowest_energy_chord_twists":list(choices[winner]),
                      "ground_energy_spread_over_four_Z2_sectors":
                          max(r["E0"] for r in rows)-min(r["E0"] for r in rows)})
    return {
      "status":"PASS_TOE73_NATIVE_ELEVEN_SITE_EXACT_INTERACTION",
      "native_sites":11,"native_edges":12,
      "fermion_count":5,"canonical_Fock_dimension":462,
      "independent_Z2_fundamental_chords":2,
      "chord_positions_in_native_patch":list(p["chords"]),
      "tested_V":list(interactions),
      "four_flux_corners":list(map(list,choices)),
      "scan":scans,
      "comparison_scope":"Full same-N many-body exact diagonalization (sparse lowest eigenpairs) of static Z2 sectors with spinless nearest-neighbor repulsion. This extends TOE72 8-site 70-state exact study. It is NOT the dynamical Gauss-constrained gauge model, a thermodynamic phase, or a proof of W33 physical 3pi flux selection."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe73_eleven_site_interaction.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],[(z["V"],z["lowest_energy_chord_twists"],
         z["ground_energy_spread_over_four_Z2_sectors"]) for z in c["scan"]])
