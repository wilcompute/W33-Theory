#!/usr/bin/env python3
"""Actual W33 40-point A5 subgroup + 25 Reye grid isometric intertwiner.

Previous repo Pass999 PROVES two conjugacy classes of A5 in PSp4(3)
both with W33 point orbits 20+20. Here reconstructs an actual group
and canonical 5-point quotient from five A4 subgroups, then labels
BOTH genuine 20-orbit W33 carriers by the 20 ordered pairs (i,j).
Construct F: 25 packet amplitude -> 40 W33 point-LABEL amplitudes:
 F|i,j>=|i,j;orbit0> when i!=j;
 F|i,i>=1/2 sum_{j!=i}|i,j;orbit1>.
Prove F†F=I, all 60 A5 intertwiners exact. Quantify whether the
injected image is invariant under full W33 adjacency (generally no).
Cannot be a physical 4D Witting Hilbert isometry or full H4 action.
"""
from __future__ import annotations
import collections,itertools,json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass999_a5_double_class_census as prior
OUT=ROOT/"data/toe_20261104_actual_a5_w33_25_to40_intertwiner.json"
def conj(g,h):
    return prior.conjugate(g,h)
def main():
    data=prior.core_objects()
    points=data["points"]; H0,H1=data["A5_classes"]
    records=[]
    for classindex,H in enumerate((H0,H1)):
        H=sorted(H)
        order3=[g for g in H if prior.order_of(g)==3]
        asub=set()
        for a in order3:
            for b in order3:
                grp=prior.subgroup_closure((a,b),cap=12)
                if grp is not None and len(grp)==12 and prior.a5_profile(grp)=={1:1,2:3,3:8}:
                    asub.add(grp)
        assert len(asub)==5,("A4 count",len(asub))
        asub=sorted(asub,key=lambda z:tuple(sorted(z)))
        idx={q:i for i,q in enumerate(asub)}
        g5={}
        for g in H:
            p=tuple(idx[frozenset(conj(g,h) for h in a4)] for a4 in asub)
            assert len(set(p))==5
            g5[g]=p
        assert len(set(g5.values()))==60
        # Genuine 40 W33 points -> two A5 orbits of size20.
        remaining=set(range(40));orbits=[]
        while remaining:
            v=min(remaining);O={g[v] for g in H}
            assert len(O)==20
            remaining-=O;orbits.append(sorted(O))
        assert len(orbits)==2
        # Label each W33 20-point orbit by ordered 5-label pairs,
        # stabilizer of ordered pair(0,1) is one order3 subgroup.
        C3={g for g in H if g5[g][0]==0 and g5[g][1]==1}
        assert len(C3)==3
        mapped=[]
        allpairs=[(i,j) for i in range(5) for j in range(5) if i!=j]
        for orbit in orbits:
            candidates=[v for v in orbit if all(g[v]==v for g in C3)]
            assert len(candidates)==2,(classindex,candidates)
            seed=min(candidates)
            m={}
            for (i,j) in allpairs:
                images={g[seed] for g in H if g5[g][0]==i and g5[g][1]==j}
                assert len(images)==1
                m[(i,j)]=next(iter(images))
            assert set(m.values())==set(orbit)
            mapped.append(m)
        labels=list(itertools.product(range(5),repeat=2))
        F=np.zeros((40,25),dtype=np.float64)
        for j,(i,k) in enumerate(labels):
            if i!=k:F[mapped[0][i,k],j]=1.
            else:
                for t in range(5):
                    if t!=i:F[mapped[1][i,t],j]=.5
        assert np.array_equal(F.T@F,np.eye(25))
        # Explicit real representations permuting packet site labels
        # and W33 point labels. Source is only diagonal A5.
        lidx={v:j for j,v in enumerate(labels)}
        for g in H:
            p5=g5[g]
            perm25=np.array([lidx[p5[i],p5[j]] for i,j in labels])
            assert np.max(abs(F[np.ix_(list(g),perm25)]-F))<1e-12
            # F[g(target), g(source)] = F[target,source] equivalent.
        # Graph adjacency on EXACT W33 40 points
        A=np.zeros((40,40),dtype=np.int64)
        for u,v in data["edges"]:A[u,v]=A[v,u]=1
        assert np.all(A.sum(axis=1)==12)
        P=F@F.T
        comm=A@P-P@A
        rank_comm=int(np.linalg.matrix_rank(comm,tol=1e-9))
        leak=float(np.linalg.norm((np.eye(40)-P)@A@F,ord="fro")**2)
        # Reduced adjacency B=F† A F is NOT a genuine W33
        # adjacency or automorphism-equivariant FULL-H4 action.
        B=F.T@A@F
        assert np.max(abs(B-B.T))<1e-12
        assert np.max(abs(B-np.round(B*4)/4))<1e-12
        v1=np.linalg.eigvalsh(B)
        row_summary=collections.Counter(str(round(float(x),4)) for x in np.diag(B))
        records.append(dict(A5_conjugacy_class_index=classindex,
          actual_W33_point_orbits=[len(x) for x in orbits],
          exact_A4_overgroups_giving_five_labels=len(asub),
          ordered_pair_stabilizer_C3_order=len(C3),
          packet25_labels_to_genuine_W33_vertices={
            str(i)+","+str(j):mapped[0][i,j] for i,j in allpairs},
          second20_orbit_packet_diagonal_image={
            str(i):[mapped[1][i,j] for j in range(5) if i!=j] for i in range(5)},
          intertwiner_matrix_40x25=F.tolist(),
          isometry_rank=int(np.linalg.matrix_rank(F)),
          all_60_diagonal_A5_grouplaw_checks=True,
          compressed_W33_adjacency_diagonal_histogram=dict(row_summary),
          compressed_W33_adjacency_eigenvalues=[float(x) for x in v1],
          W33_adjacency_projection_commutator_rank=rank_comm,
          W33_adjacency_projection_commutator_squared_frobenius=float(np.sum(comm**2)),
          W33_adjacency_leakage_squared_frobenius=leak,
          full_W33_adjacency_invariant_subspace=bool(leak<1e-10),
          actual_A5_classes_proved_by_existing_repo=2))
    assert len(records)==2
    result=dict(status="PASS_ACTUAL_W33_A5_25_TO40_PACKET_INTERTWINER_BOTH_CLASSES",
      W33_full_point_graph_Aut_order=51840,
      previous_full_H4_packet_to_W33_graph_Aut_image_at_most2=True,
      reduced_diagonal_A5_subgroup_order=60,
      W33_A5_subgroup_classes_tested=2,
      source_25_packet_A5_orbits=[5,20],
      target_W33_point_A5_orbits=[20,20],
      source_A5_character_on_classes={"id":25,"order2":1,"order3":4,"order5":0},
      target_A5_character_on_classes={"id":40,"order2":0,"order3":4,"order5":0},
      transitive_five_set_A5_character={"id":5,"order2":1,"order3":2,"order5":0},
      transitive_twenty_set_A5_character={"id":20,"order2":0,"order3":2,"order5":0},
      source_rep_complex_irrep_multiplicities={"1":2,"3":1,"3prime":1,"4":3,"5":1},
      target_rep_complex_irrep_multiplicities={"1":2,"3":2,"3prime":2,"4":4,"5":2},
      diagonal_A5_equivariant_isometric_25_to40_exists=True,
      diagonal_A5_equivariant_deterministic_set_map_25_to40_exists=False,
      why_no_set_map="The diagonal packet (i,i) has A4 point-stabilizer order12. A W33 20-orbit point has C3 stabilizer order3. An A5-set map would force A4 subset C3, impossible.",
      both_W33_class_certificates=records,
      limiting_statement="This is an A5-equivariant isometric linear map on a 40-dimensional point-LABEL module, not a four-dimensional quantum Witting Hilbert isometry; FULL-H4 graph equivariance is impossible. Test the actual W33 adjacency leakage, which can refute invariance as a W33 dynamics subspace.",
      prior_art="Repo Pass999 enumerated two A5 classes and 20+20 point orbits; here explicit coset coordinatizations, full 60-element matrices and 40x25 intertwiner are newly computed.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],[(x["W33_adjacency_projection_commutator_rank"],x["W33_adjacency_leakage_squared_frobenius"]) for x in records],flush=True)
    return result
if __name__=="__main__":main()
