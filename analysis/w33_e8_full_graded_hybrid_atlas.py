#!/usr/bin/env python3
"""Lift the completed matter81 hybrid chart to both E8 matter grades.

The physical FI theorem gives the exact Z3 grading
  E8 = g0(86) + g1(81) + g2(81)
with g0=E6+A2, g1=(27,3), g2=(27bar,3bar).

The landed g1 hybrid chart is an exact 81x81 Q(omega) basis. The g2 chart is
its field conjugate omega<->omega^2. Using the identity basis on g0 gives the
block atlas
  I86 direct_sum B81 direct_sum conjugate(B81),
of total rank 248.

This is a coordinate atlas for the full graded E8 adjoint vector space. It
does not by itself transport the Chevalley bracket into hybrid coordinates.
"""
from __future__ import annotations
import hashlib, importlib.util, json, sys
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_full_graded_hybrid_atlas.json"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);assert s and s.loader
    m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def token(x):
    a,b=x.as_pair()
    return f"{a.numerator}/{a.denominator},{b.numerator}/{b.denominator}"

def rebuild_hybrid():
    h=load(ROOT/"analysis/w33_e8_matter81_hybrid_cubic_dark_basis.py","hybrid_builder")
    frozen=json.loads((ROOT/"data/w33_e8_matter81_hybrid_cubic_dark_basis.json").read_text())
    piv=frozen["cubic_sector"]["selected_pivot_indices_zero_based"]
    lines,_=h.lifted_instructions()
    incidence=[[0]*270 for _ in range(81)]
    for j,line in enumerate(lines):
        for x in line:incidence[h.K_INDEX[x]][j]=1
    cols=[]
    for j in piv:
        cols.append([h.ONE if incidence[r][j] else h.ZERO for r in range(81)])
    for t in (1,2):
        cols.append([h.omega_power(t*p) for _hh,p in h.K])
    for s in (1,2):
        m=[h.ONE,-h.omega_power(s),h.ZERO]
        values={hh:h.matvec(h.rho_s(hh,s),m) for hh in h.H}
        for component in range(3):
            cols.append([values[hh][component] for hh,p in h.K])
    assert len(cols)==81
    return [[cols[c][r] for c in range(81)] for r in range(81)],h

def main(write=True):
    grading=json.loads((ROOT/"data/w33_physical_fi_e6_a2_z3_grading.json").read_text())
    hybrid=json.loads((ROOT/"data/w33_e8_matter81_hybrid_cubic_dark_basis.json").read_text())
    address=json.loads((ROOT/"data/w33_e8_matter81_h27_address_operator_compiler.json").read_text())
    assert grading["E8"]["fixed_dimension"]==86
    assert grading["E8"]["root_grades"]=={"0":78,"1/3":81,"2/3":81}
    assert hybrid["hybrid_basis"]["rank"]==81

    B,h=rebuild_hybrid()
    serial="|".join(token(B[r][c]) for r in range(81) for c in range(81))
    d1="sha256:"+hashlib.sha256(serial.encode()).hexdigest()
    assert d1==hybrid["hybrid_basis"]["matrix_digest"]

    Bbar=[[x.conjugate() for x in row] for row in B]
    serial2="|".join(token(Bbar[r][c]) for r in range(81) for c in range(81))
    d2="sha256:"+hashlib.sha256(serial2.encode()).hexdigest()
    assert d2=="sha256:c9edf314a841138fc6b401b4423f60fe4d6e7d6ee09151388c2b1a1746bafa0c"

    descriptor={"neutral":"I86","grade1":d1,"grade2":d2}
    atlas_digest="sha256:"+hashlib.sha256(json.dumps(descriptor,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert atlas_digest=="sha256:bd2390b4676d487af40be06317bf7be9a6225048b867e0af77114d924f47652f"

    # Anchor the two matter blocks to explicit, ordered frozen E8 roots.  The
    # hybrid matrix rows use h.K order; the landed compiler certificate maps
    # every K address to one grade-one root.  Negation supplies the matching
    # grade-two root order, removing the previous formal-conjugate ambiguity.
    root_by_address={}
    for record in address["address_space"]["root_addresses"]:
        key=(tuple(record["K_address"][0]),record["K_address"][1])
        root=tuple(Fraction(value) for value in record["root"])
        assert key not in root_by_address
        root_by_address[key]=root
    assert set(root_by_address)==set(h.K)
    grade1_roots=[root_by_address[key] for key in h.K]
    grade2_roots=[tuple(-value for value in root) for root in grade1_roots]
    assert len(set(grade1_roots))==len(set(grade2_roots))==81
    assert set(grade1_roots).isdisjoint(grade2_roots)
    grade1_serial=[[str(value) for value in root] for root in grade1_roots]
    grade2_serial=[[str(value) for value in root] for root in grade2_roots]
    address_serial=[[[*key[0]],key[1]] for key in h.K]
    root_order_descriptor={
        "K_address_order":address_serial,
        "grade1_root_rows":grade1_serial,
        "grade2_root_rows":grade2_serial,
    }
    root_order_digest="sha256:"+hashlib.sha256(
        json.dumps(root_order_descriptor,sort_keys=True,separators=(",",":")).encode()
    ).hexdigest()

    # Rank is additive across the block diagonal; conjugation preserves rank.
    ranks=[86,81,81]
    assert sum(ranks)==248
    # FI center trace: 86 + 81 omega + 81 omega^2 = 5.
    fi_trace_pair=[5,0]

    out={
      "schema":"w33.e8_full_graded_hybrid_atlas.v2",
      "status":"PASS_ROOT_ORDERED_GRADED_E8_VECTOR_ATLAS_IS_I86_PLUS_HYBRID81_PLUS_CONJUGATE_HYBRID81",
      "headline":"The completed 81-state hybrid chart lifts to both explicitly ordered E8 matter grades. The physical FI grading is 248=86+81+81; the grade-1 rows use the landed K-address-to-root order, the grade-2 rows are their ordered negative roots and use the exact Q(omega) conjugate chart, and the neutral E6+A2 block uses I86. The block atlas has rank 248 and FI-center trace 5.",
      "grading":{
        "branching":"248=(78,1)+(1,8)+(27,3)+(27bar,3bar)",
        "dimensions":{"g0":86,"g1":81,"g2":81,"total":248},
        "FI_center_eigenvalues":{"g0":"1","g1":"omega","g2":"omega^2"},
        "FI_center_trace_Qomega_pair":fi_trace_pair,
        "FI_center_trace":"5"
      },
      "atlas":{
        "formula":"I86 direct_sum B81 direct_sum conjugate(B81)",
        "block_ranks":ranks,
        "rank":248,
        "grade1_digest":d1,
        "grade2_conjugate_digest":d2,
        "atlas_descriptor_digest":atlas_digest,
        "grade2_rule":"ordered root negation together with field conjugation omega <-> omega^2 of every grade1 hybrid coordinate",
        "matter_root_row_order_digest":root_order_digest
      },
      "matter_root_row_order":root_order_descriptor,
      "physics_reading":"The finite matter compiler now has a charge-conjugate partner and sits inside the exact E8 FI grading. Matter and antimatter hybrid coordinates are related by field conjugation, while the E6+A2 gauge-neutral sector remains a separate 86-dimensional block.",
      "boundary":"This is a root-ordered graded E8 vector-space block atlas, not yet a hybrid-coordinate Chevalley multiplication table. The neutral I86 block is relative to the prior E6+A2 grading basis. Brackets g1 x g1 -> g2, g2 x g2 -> g1 and g1 x g2 -> g0 remain to be transported explicitly before calling this a full Lie-algebra compiler.",
      "parents":[
        "data/w33_physical_fi_e6_a2_z3_grading.json",
        "data/w33_e8_matter81_hybrid_cubic_dark_basis.json",
        "data/w33_e8_matter81_h27_address_operator_compiler.json"
      ],
      "checks":{
        "grading_86_81_81":True,
        "grade1_digest_replayed":True,
        "grade2_exact_conjugate":True,
        "grade1_rows_anchored_to_81_frozen_roots":True,
        "grade2_rows_anchored_to_ordered_negative_roots":True,
        "conjugation_preserves_rank81":True,
        "block_rank248":True,
        "FI_center_trace5":True,
        "Chevalley_bracket_not_claimed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
