#!/usr/bin/env python3
"""Transport the canonical signed E6 cubic into the current K/hybrid matter chart.

The historical combined SU(3)+E6 gauge solve is still source-locked in
extracted_v13.  After its phase gauge, the g1 x g1 -> g2 root bracket is

    [e_(i,a), e_(j,b)] = d_{ijk} epsilon_{abc} ebar_(k,c),

where {i,j,k} is one of the 45 E6 cubic triads.

Pass1103 gives the exact e6id -> H27 normal-form address:
    i -> (u0,u1,z).
This is the same H27 normal form used by the current K=H27 x C3 address chart.
Thus the old signed cubic can be transported objectwise to the current 81-root
carrier without guessing a new graph isomorphism.

The current 73+8 hybrid basis B is invertible.  Consequently the complete
hybrid structure tensor is represented exactly (without materializing a dense
81^3 array) by

    T_hyb = conjugate(B)^(-1) o T_root o (B tensor B).

This file verifies the complete sparse root tensor and the exact change-of-basis
ingredients.  It also distinguishes two tangent statements:

* for any single ROOT-BASIS background v, D_v(x)=[v,x] has rank 20;
* the span of the images of all 81 such Jacobians is all 81 dimensions of g2.

Therefore, after charge conjugation and the already-frozen minimal 81-state
compiler, the Jacobian FAMILY collectively reaches every one of the 54
symmetry-retyped target slots.  No claim is made that one background has
rank 54.
"""
from __future__ import annotations
import importlib.util, itertools, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e6_cubic_hybrid81_transport.json"
ARCH=ROOT/"extracted_v13/W33-Theory-master/artifacts"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def eps3(a,b,c):
    if len({a,b,c})<3:return 0
    inv=sum(1 for i,j in ((a,b),(a,c),(b,c)) if i>j)
    return -1 if inv%2 else 1

def main(write=True):
    hmod=load(ROOT/"analysis/w33_e8_matter81_hybrid_cubic_dark_basis.py","hybrid_cubic_parent")
    fwmod=load(ROOT/"analysis/w33_pass1103_hesse_firewall_cubic_transport.py","firewall_transport_parent")

    canonical=json.loads((ARCH/"canonical_su3_gauge_and_cubic.json").read_text())
    archived=json.loads((ARCH/"e8_g1g1_couplings_cubic_firewall.json").read_text())
    hybrid=json.loads((ROOT/"data/w33_e8_matter81_hybrid_cubic_dark_basis.json").read_text())
    minimal=json.loads((ROOT/"data/w33_minimal_symmetry_changing_81_compiler.json").read_text())

    assert canonical["status"]=="ok"
    assert archived["status"]=="ok"
    assert archived["counts"]["nonzero_g1g1_brackets"]==810
    assert archived["counts"]["firewall_bad_couplings"]==162
    assert hybrid["hybrid_basis"]["rank"]==81
    assert minimal["compiler"]["symmetry_changing_coordinates"]==54

    d={tuple(sorted(x["triple"])):int(x["sign"]) for x in canonical["solution"]["d_triples"]}
    assert len(d)==45
    sign_hist=Counter(d.values())
    assert sign_hist==Counter({-1:23,1:22})

    # Exact e6id -> H27 address in the SAME Z^a X^b omega^c normal form.
    e6_to_h={int(i):(int(u[0]),int(u[1]),int(z)) for i,(u,z) in fwmod.E6_TO_UZ.items()}
    h_to_e6={h:i for i,h in e6_to_h.items()}
    assert len(e6_to_h)==len(h_to_e6)==27

    # Compare, but do NOT identify, the two 45-line gauges.  Pass1103's
    # e6id->H27 object map exactly locks the bad-nine central fibers, while the
    # newer five-direction right-coset chart uses a different anchored gauge.
    H=tuple(itertools.product(range(3),repeat=3)); ID=(0,0,0)
    def right_cosets_H(subgroup):
        unseen=set(H); out=[]
        while unseen:
            g=min(unseen)
            C=frozenset(hmod.hmul(g,x) for x in subgroup)
            out.append(C); unseen-=C
        return out
    current_lines=set()
    for _name,g in hmod.DIRECTIONS:
        S=frozenset((ID,g,hmod.hmul(g,g)))
        cs=right_cosets_H(S); assert len(cs)==9
        for C in cs: current_lines.add(tuple(sorted(h_to_e6[x] for x in C)))
    canonical_lines=set(d)
    assert len(current_lines)==len(canonical_lines)==45
    gauge_overlap=current_lines & canonical_lines
    bad_triads={tuple(sorted(x)) for x in fwmod.FIBER_SIGNS}
    assert len(gauge_overlap)==10
    assert bad_triads <= gauge_overlap and len(bad_triads)==9

    # Root-coordinate canonical bracket, with external phase p identified with
    # the canonical SU(3) basis index in this anchored qutrit gauge.
    keys=[(h,p) for h in H for p in range(3)]
    index={x:i for i,x in enumerate(keys)}
    out_hist=Counter(); in_degree=Counter(); nonzero=0; bad=0
    bad_triads={tuple(sorted(x)) for x in fwmod.FIBER_SIGNS}
    records=[]
    for aa in range(81):
        h1,p=keys[aa]
        i=h_to_e6[h1]
        for bb in range(aa+1,81):
            h2,q=keys[bb]; j=h_to_e6[h2]
            if i==j or p==q: continue
            third=None
            for tri in d:
                if i in tri and j in tri:
                    third=next(k for k in tri if k not in (i,j)); break
            if third is None: continue
            r=3-p-q
            if r not in (0,1,2): continue
            coeff=d[tuple(sorted((i,j,third)))]*eps3(p,q,r)
            assert coeff in (-1,1)
            out=index[(e6_to_h[third],r)]
            nonzero+=1; out_hist[out]+=1; in_degree[aa]+=1; in_degree[bb]+=1
            if tuple(sorted((i,j,third))) in bad_triads:bad+=1
            records.append((aa,bb,out,coeff))

    assert nonzero==810
    assert bad==162
    assert len(out_hist)==81 and set(out_hist.values())=={10}
    assert len(in_degree)==81 and set(in_degree.values())=={20}

    # Every root-basis Jacobian has 20 distinct output roots, hence rank 20.
    root_background_ranks=[]
    collective=set()
    for a in range(81):
        outs={o for i,j,o,c in records if i==a or j==a}
        root_background_ranks.append(len(outs)); collective|=outs
    assert set(root_background_ranks)=={20}
    assert len(collective)==81

    out={
      "schema":"w33.e6_cubic_hybrid81_transport.v1",
      "status":"PASS_CANONICAL_SIGNED_E6_CUBIC_TRANSPORTS_OBJECTWISE_TO_HYBRID81_AND_COLLECTIVE_JACOBIANS_SPAN_G2",
      "headline":"The actual source-locked 45-term signed E6 cubic is transported objectwise into the current H27/K-labelled matter carrier. In the canonical SU(3) phase gauge its root bracket has exactly 810 nonzero unordered g1xg1 channels, 162 on the nine firewall fibers, every g1 root has degree 20, and every g2 root occurs as ten outputs. The Pass1103 object gauge and the newer five-direction address gauge are not conflated: their 45-line sets overlap in only ten triads, while all nine firewall central fibers agree. The complete 73+8 hybrid tensor is the exact conjugation Bbar^-1 T_root (B tensor B).",
      "source_locks":{
        "canonical_cubic_path":"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json",
        "canonical_cubic_blob_sha":"3bcc9cdcd572627efe675e1fad4b32b3fe48f649",
        "archived_g1g1_path":"extracted_v13/W33-Theory-master/artifacts/e8_g1g1_couplings_cubic_firewall.json",
        "archived_g1g1_blob_sha":"e5baf485428856a438df04a12b3a6e4d3a2ba5f7",
        "current_H27_bridge":"analysis/w33_pass1103_hesse_firewall_cubic_transport.py"
      },
      "gauge_comparison":{
        "pass1103_e6id_to_H27_object_map_bijective":True,
        "canonical_cubic_triads":45,
        "newer_address_right_coset_lines":45,
        "line_set_overlap":10,
        "all_nine_firewall_center_fibers_in_overlap":True,
        "full_45_line_gauge_identity":False,
        "interpretation":"Object labels transport exactly, but the two independently anchored 45-line incidence gauges must not be identified without an additional automorphism/intertwiner."
      },
      "root_tensor":{
        "formula":"[e_(i,a),e_(j,b)] = d_ijk epsilon_abc ebar_(k,c)",
        "signed_E6_triads":45,
        "d_sign_distribution":{"plus":22,"minus":23},
        "nonzero_unordered_channels":810,
        "firewall_bad_channels":162,
        "input_degree_each":20,
        "output_multiplicity_each":10,
        "root_output_span_dimension":81
      },
      "hybrid_tensor":{
        "g1_basis":"B81 = 73 cubic pivots + 8 Fourier/magic modes",
        "g2_basis":"conjugate(B81)",
        "complete_factorized_formula":"T_hyb = conjugate(B81)^(-1) o T_root o (B81 tensor B81)",
        "materialized_dense_81_cubed":False,
        "reason":"the factorized exact tensor is complete and avoids a redundant dense 531441-entry artifact",
        "basis_rank_g1":81,
        "basis_rank_g2":81
      },
      "jacobian":{
        "definition":"D_v(x)=[v,x]: g1 -> g2",
        "root_basis_background_rank_set":[20],
        "collective_image_span_dimension":81,
        "collectively_reaches_all_54_retyped_slots":True,
        "single_root_background_rank54":False,
        "single_generic_background_rank":"not established in this certificate"
      },
      "boundary":"This closes the exact tensor transport and the collective tangent-span question. It does not prove that one physical vacuum/background realizes rank 54, nor supply a Hamiltonian coupling strength, VEV, mass, scattering amplitude, or fault-tolerant implementation.",
      "parents":[
        "data/w33_e8_matter81_hybrid_cubic_dark_basis.json",
        "data/w33_minimal_symmetry_changing_81_compiler.json",
        "data/w33_h27_cubic_representation_transducer.json"
      ],
      "checks":{
        "canonical_45_triads_loaded":True,
        "e6id_to_current_H27_is_bijective":True,
        "canonical_vs_current_line_overlap10":True,\n        "bad9_center_fibers_match_exactly":True,\n        "full_45_line_gauge_identity_not_claimed":True,
        "root_channels_810":True,
        "firewall_channels_162":True,
        "every_input_degree20":True,
        "every_output_multiplicity10":True,
        "collective_jacobian_span81":True,
        "hybrid_change_of_basis_invertible":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__": print(json.dumps(main(True),indent=2))
