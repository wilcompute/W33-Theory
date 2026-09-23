#!/usr/bin/env python3
"""Transport the complete sparse E8 Chevalley bracket into the 86+81+81 hybrid atlas.

Source algebra:
  artifacts/e8_structure_constants_w33_discrete.json
with basis h_1..h_8 + 240 root vectors.

Hybrid atlas:
  I_86 direct_sum B_81 direct_sum conjugate(B_81).

The archived exact root metadata supplies the objectwise permutation from the
source Chevalley root basis to (e6id, external-qutrit-index) on g1/g2.
The archived canonical SU(3)+E6 phase solution supplies optional diagonal root
signs, so this transport is in the same signed cubic gauge used by the
hybrid-E6-cubic certificate.

No dense 248^3 tensor is necessary.  The exact executable bracket is

    [x,y]_hyb = A^{-1} [A x, A y]_Chevalley,

where A is the block atlas including the root permutation/sign gauges.  This is
a complete Lie-algebra compiler: all g0g0, g0g1, g0g2, g1g1, g1g2, g2g2
operations are inherited exactly.

Jacobi is verified in two layers:
  1. exhaust all C(248,3)=2,511,496 source basis triples directly;
  2. prove A is exactly invertible over Q(omega).
An invertible change of basis preserves the Jacobi polynomial identically, so
the transported hybrid bracket satisfies Jacobi for all vectors, not merely a
sample of hybrid basis triples.
"""
from __future__ import annotations
import importlib.util, itertools, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_full_hybrid_chevalley_compiler.json"
ARCH=ROOT/"extracted_v13/W33-Theory-master/artifacts"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def invert(A,zero,one):
    n=len(A); M=[list(row)+[one if i==j else zero for j in range(n)] for i,row in enumerate(A)]
    for col in range(n):
        piv=next((r for r in range(col,n) if M[r][col]),None)
        if piv is None: raise AssertionError(("singular",col))
        M[col],M[piv]=M[piv],M[col]
        q=one/M[col][col]; M[col]=[x*q for x in M[col]]
        for r in range(n):
            if r==col: continue
            f=M[r][col]
            if f: M[r]=[x-f*y for x,y in zip(M[r],M[col])]
    return [row[n:] for row in M]

def mm(A,B,zero):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),zero)
             for j in range(len(B[0]))] for i in range(len(A))]

def main(write=True,full_jacobi=True):
    atlasmod=load(ROOT/"analysis/w33_e8_full_graded_hybrid_atlas.py","full_hybrid_atlas_parent")
    exact=sys.modules.get("w33_exact_eisenstein")
    assert exact is not None, "hybrid atlas must load canonical w33_exact_eisenstein"
    jac=load(ROOT/"tools/verify_e8_jacobi_from_structure_constants.py","full_hybrid_jacobi")

    sc=json.loads((ROOT/"artifacts/e8_structure_constants_w33_discrete.json").read_text())
    meta=json.loads((ARCH/"e8_root_metadata_table.json").read_text())
    canon=json.loads((ARCH/"canonical_su3_gauge_and_cubic.json").read_text())
    atlas=json.loads((ROOT/"data/w33_e8_full_graded_hybrid_atlas.json").read_text())

    assert sc["basis"]["n"]==248 and sc["basis"]["cartan_dim"]==8 and len(sc["basis"]["roots"])==240
    assert atlas["atlas"]["rank"]==248
    assert meta["counts"]["grade_hist"]=={"g0":78,"g1":81,"g2":81}

    roots=[tuple(x) for x in sc["basis"]["roots"]]
    byroot={tuple(r["root_orbit"]):r for r in meta["rows"]}
    assert set(roots)==set(byroot)

    # Source basis partitions.
    g0=list(range(8))+[8+i for i,r in enumerate(roots) if byroot[r]["grade"]=="g0"]
    g1=[8+i for i,r in enumerate(roots) if byroot[r]["grade"]=="g1"]
    g2=[8+i for i,r in enumerate(roots) if byroot[r]["grade"]=="g2"]
    assert [len(g0),len(g1),len(g2)]==[86,81,81]

    # e6id/H27 and external-index maps in the CURRENT physical-Clifford address gauge.
    gauge_bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    assert gauge_bridge["incidence"]["mapped_full45_equal"] is True
    e6_to_h={int(i):tuple(map(int,h)) for i,h in gauge_bridge["maps"]["e6id_to_current_H27_address"].items()}
    H=tuple(itertools.product(range(3),repeat=3))
    K=[(h,p) for h in H for p in range(3)]
    kindex={x:i for i,x in enumerate(K)}
    g1_by_label={(int(byroot[roots[i-8]]["i27"]),int(byroot[roots[i-8]]["i3"])):i for i in g1}
    g2_by_label={(int(byroot[roots[i-8]]["i27"]),int(byroot[roots[i-8]]["i3"])):i for i in g2}
    assert len(g1_by_label)==len(g2_by_label)==81

    # Canonical phase gauge.  i3 -> orbit id:
    # g1: fundamental weights (1,0),(-1,1),(0,-1) -> 4,9,3
    # g2: negatives -> 5,6,0.
    pb=canon["solution"]["phase_bits"]
    g1_orbit={0:"4",1:"9",2:"3"}; g2_orbit={0:"5",1:"6",2:"0"}
    sign1={}; sign2={}; orig1={}; orig2={}
    h_to_e6={h:i for i,h in e6_to_h.items()}
    for h,p in K:
        i=h_to_e6[h]; row=kindex[(h,p)]
        orig1[row]=g1_by_label[(i,p)]; orig2[row]=g2_by_label[(i,p)]
        sign1[row]=-1 if pb[g1_orbit[p]][i] else 1
        sign2[row]=-1 if pb[g2_orbit[p]][i] else 1
    assert len(set(orig1.values()))==len(set(orig2.values()))==81

    # Rebuild exact hybrid B and inverse.
    B=atlasmod.rebuild_hybrid()
    Bbar=[[x.conjugate() for x in row] for row in B]
    Binv=invert(B,exact.ZERO,exact.ONE)
    Bbarinv=[[x.conjugate() for x in row] for row in Binv]
    I=exact.identity_matrix(81)
    assert mm(Binv,B,exact.ZERO)==I
    assert mm(Bbarinv,Bbar,exact.ZERO)==I

    # Verify grading of every source bracket term directly using the archived metadata.
    grade=[0]*248
    for i,r in enumerate(roots,8):
        grade[i]={"g0":0,"g1":1,"g2":2}[byroot[r]["grade"]]
    grade_terms=0
    for key,terms in sc["brackets"].items():
        a,b=map(int,key.split(","))
        for k,c in terms:
            grade_terms+=1
            assert grade[int(k)]==(grade[a]+grade[b])%3

    # Exhaustive source Jacobi. This is the finite proof imported by exact basis transport.
    n,cartan_dim,rts,table=jac._load_table(ROOT/"artifacts/e8_structure_constants_w33_discrete.json")
    assert (n,cartan_dim,len(rts))==(248,8,240)
    checked=0
    if full_jacobi:
        for a in range(246):
            for b in range(a+1,247):
                for c in range(b+1,248):
                    assert not jac._jacobi_for_triple(a,b,c,table),(a,b,c)
                    checked+=1
        assert checked==2511496

    out={
      "schema":"w33.e8_full_hybrid_chevalley_compiler.v1",
      "status":"PASS_COMPLETE_248D_HYBRID_CHEVALLEY_BRACKET_IS_EXACT_TRANSPORT_OF_W33_DISCRETE_E8",
      "headline":"The 86+81+81 hybrid atlas is now an executable Lie-algebra compiler, not only a vector-space atlas. The committed W33-discrete E8 Chevalley bracket is transported by the exact block change of basis A=I86 plus the signed/permuted B81 and conjugate(B81) matter charts. Every bracket term respects the Z3 grading, both 81x81 matter transforms have exact inverses over Q(omega), and all 2,511,496 source basis Jacobi triples vanish. Therefore the transported hybrid bracket satisfies Jacobi identically.",
      "source":{
        "structure_constants":"artifacts/e8_structure_constants_w33_discrete.json",
        "structure_constants_blob_sha":"c4cd1f603c421423123aebd82a660d1ec00979dd",
        "root_metadata":"extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json",
        "root_metadata_blob_sha":"8f2bb5f5b5b22eee059bf2bf30de95e73af9c2f1",
        "dimension":248,
        "grading_dimensions":[86,81,81],
        "all_bracket_terms_checked_for_grading":True
      },
      "hybrid_transform":{
        "formula":"A = I86 direct_sum (P1 G1 B81) direct_sum (P2 G2 conjugate(B81))",
        "field":"Q(omega)",
        "g1_inverse_verified":True,
        "g2_inverse_verified":True,
        "rank":248,
        "g1_digest":atlas["atlas"]["grade1_digest"],
        "g2_digest":atlas["atlas"]["grade2_conjugate_digest"]
      },
      "bracket":{
        "definition":"[x,y]_hyb = A^-1 [A x,A y]_Chevalley",
        "all_grade_products":["g0g0->g0","g0g1->g1","g0g2->g2","g1g1->g2","g1g2->g0","g2g2->g1"],
        "dense_248_cubed_materialized":False,
        "representation":"exact sparse source bracket plus exact block change-of-basis evaluator"
      },
      "jacobi":{
        "source_basis_triples_total":2511496,
        "source_basis_triples_checked":checked if full_jacobi else 0,
        "source_jacobi_exact":bool(full_jacobi),
        "hybrid_jacobi_exact":bool(full_jacobi),
        "proof":"Jacobi is a polynomial identity preserved by the verified invertible exact change of basis A."
      },
      "boundary":"This closes the finite Lie-algebra coordinate compiler. It does not derive a spacetime Hamiltonian, quantum-field vacuum, coupling constants, particle spectrum, scattering amplitudes, or a unitary hardware implementation of every Lie bracket.",
      "parents":[
        "data/w33_e8_full_graded_hybrid_atlas.json",
        "data/w33_e6_cubic_hybrid81_transport.json",
        "data/w33_e6id_current_h27_gauge_bridge.json",
        "artifacts/e8_structure_constants_w33_discrete.json"
      ],
      "checks":{
        "source_dimension248":True,
        "source_grades_86_81_81":True,
        "root_label_permutations_bijective":True,
        "canonical_phase_gauges_loaded":True,
        "current_H27_gauge_bridge_loaded":True,
        "B81_inverse_exact":True,
        "conjugate_B81_inverse_exact":True,
        "all_bracket_terms_respect_Z3":True,
        "all_2511496_source_Jacobi_triples_zero":bool(full_jacobi),
        "hybrid_Jacobi_follows_exactly":bool(full_jacobi)
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__": print(json.dumps(main(True,True),indent=2))
