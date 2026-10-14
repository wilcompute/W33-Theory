"""TOE78: exact commutative 6-dimensional native orbital adjacency algebra
and 27=1+4+4+6+6+6 decomposition under H27 semidirect D8.

This supplies the 6D E6 root-like eigenspace (lambda -5) of the
27-line cubic surface graph from actual W33 octagon addresses.
No identification with physical Weyl fermions or E6 gauge dynamics.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate as native

def certificate():
    g=native()
    assert g["induced_faithful_permutation_group_order"]==216
    orbits=g["unordered_pair_orbit_edges"]
    assert len(orbits)==5
    assert [len(x) for x in orbits]==[27,54,54,108,108]
    I=np.eye(27,dtype=np.int64)
    adjacency=[]
    for pairs in orbits:
        A=np.zeros((27,27),dtype=np.int64)
        for u,v in pairs:
            assert 0<=u<v<27
            A[u,v]=A[v,u]=1
        assert np.all(np.diag(A)==0)
        adjacency.append(A)
    assert np.array_equal(sum(adjacency),np.ones((27,27),dtype=np.int64)-I)
    assert [int(A[0].sum()) for A in adjacency]==[2,4,4,8,8]
    for A,B in itertools.combinations(adjacency,2):
        assert not np.any(A@B-B@A)
    # Association-scheme structure constants from exact integer
    # multiplication, constant on each unordered pair orbital.
    mats=[I]+adjacency
    structure=np.zeros((6,6,6),dtype=np.int64)
    for i,A in enumerate(mats):
        for j,B in enumerate(mats):
            P=A@B
            coeff=[int(P[0,0])]
            for orb in orbits:coeff.append(int(P[orb[0][0],orb[0][1]]))
            reconstructed=sum(k*M for k,M in zip(coeff,mats))
            assert np.array_equal(P,reconstructed)
            structure[i,j,:]=coeff
    assert np.array_equal(structure,np.transpose(structure,(1,0,2)))
    T=sum(w*A for w,A in zip((1,3,9,27,81),adjacency))
    eig,vec=np.linalg.eigh(T.astype(float))
    groups=[]
    for i,e in enumerate(eig):
        if not groups or abs(e-groups[-1]["value"])>1e-6:
            groups.append({"value":float(e),"columns":[i]})
        else:groups[-1]["columns"].append(i)
    dims=sorted(len(t["columns"]) for t in groups)
    # The rank-six commutative algebra makes the induced 27-dimensional
    # permutation representation multiplicity-free.
    assert len(groups)==6 and dims==[1,4,4,6,6,6],dims
    # Central H27 C3 projects exactly onto 9-dimensional subspace
    # of scalar central character 1; it is 1+4+4 of these six sectors.
    center=g["normal_H27_center_generator_27"]
    assert len(center)==27 and sorted(center)==list(range(27))
    Z=np.zeros((27,27),dtype=np.int64)
    for i,j in enumerate(center):Z[j,i]=1
    assert np.array_equal(Z@Z@Z,I) and not np.array_equal(Z,I)
    P0=(I+Z+Z@Z)/3.
    assert abs(np.trace(P0)-9)<1e-10
    GQ=adjacency[0]+adjacency[1]+adjacency[2]
    eiggq=np.linalg.eigvalsh(GQ)
    assert np.max(abs(eiggq-np.sort(np.array([-5.]*6+[1.]*20+[10.]))))<1e-9
    specs=[]
    for grp in groups:
        ids=grp["columns"]
        V=vec[:,ids]
        chi0=float(np.trace(V.T@P0@V))
        gamma=float(np.trace(V.T@GQ@V)/len(ids))
        assert abs(chi0-round(chi0))<1e-7
        assert min(abs(gamma-v) for v in (10.,1.,-5.))<1e-8
        center_rank=int(round(chi0))
        assert center_rank in (0,len(ids))
        specs.append({
          "dimension":len(ids),
          "generic_orbital_operator_eigenvalue":grp["value"],
          "H27_center_character_trivial":center_rank==len(ids),
          "GQ24_cubic_surface_eigenvalue":int(round(gamma))
        })
    assert sum(row["dimension"] for row in specs)==27
    assert sum(x["dimension"] for x in specs if x["H27_center_character_trivial"])==9
    assert sorted(x["dimension"] for x in specs if x["H27_center_character_trivial"])==[1,4,4]
    assert sorted(x["dimension"] for x in specs if not x["H27_center_character_trivial"])==[6,6,6]
    assert [x["dimension"] for x in specs if x["GQ24_cubic_surface_eigenvalue"]==-5]==[6]
    assert [x["dimension"] for x in specs if x["GQ24_cubic_surface_eigenvalue"]==10]==[1]
    return {
      "status":"PASS_TOE78_W33_OCTAGON_6_SECTOR_ASSOCIATION_SCHEME",
      "native_octagon_addresses":27,
      "acting_native_group":"H27 semidirect D8, order 216",
      "undirected_pair_orbital_valencies":[2,4,4,8,8],
      "rank_of_commutative_orbital_adjacency_algebra":6,
      "all_five_orbital_matrices_pairwise_commute_exactly":True,
      "integer_association_scheme_structure_constants":structure.tolist(),
      "multiplicity_free_27_representation_dimensions":[1,4,4,6,6,6],
      "H27_center_trivial_isotypic_total_dimension":9,
      "nontrivial_H27_center_isotypic_total_dimension":18,
      "GQ_27_line_spectrum":{"10":1,"1":20,"-5":6},
      "six_irreducible_symmetry_sector_controls":specs,
      "exact_e6_six_dimensional_submodule":"The -5 eigenspace of the 27-line incidence graph is 6D and is precisely one irreducible symmetry sector of the native 216 group. This is the standard 6D E6 reflection spectral sector at the abstract 27-line graph level; no physical 4D spin representation follows.",
      "physics_scope":"Every real symmetric 216-invariant linear operator on these 27 native octagon addresses is a real combination of I and five orbital matrices. This is a complete five-coupling symmetry-compatible static single-particle adjacency ansatz, not a 4D quantum field theory, a physical mass spectrum or an E6 Higgs mechanism.",
      "proof":"All 351 unordered pairs partition into five 216-group orbits of sizes 27,54,54,108,108. Each adjacency matrix is invariant and symmetric. Their products remain group-invariant, and the fixed-space is exactly their six-dimensional span with I; hence all products commute and have integer structure constants, verified by exhaustive 27x27 integer multiplication. A generic integer orbital combination has six distinct eigenspaces of dimensions 1,4,4,6,6,6. The central C3 projection and GQ adjacency classify the six sectors exactly at integer-rank level."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe78_octagon_bose_mesner.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["multiplicity_free_27_representation_dimensions"])
    print("SECTORS",[(s["dimension"],s["H27_center_character_trivial"],s["GQ24_cubic_surface_eigenvalue"]) for s in c["six_irreducible_symmetry_sector_controls"]])
