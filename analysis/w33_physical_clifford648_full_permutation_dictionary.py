#!/usr/bin/env python3
"""Materialize all 648 elements of the physical one-qutrit Clifford normalizer
as explicit W33 point-stabilizer permutations.

The physical external-A2 H27 uses normal form Z^a X^b z^c with ZX=zXZ.
Pass1054 chooses a Heisenberg basis x,y,zp with xp*yp=yp*xp*zp and constructs
a split complement L ~= SL(2,3).

To match the quotient basis used by the physical Clifford bridge, choose
    X_phys -> x,
    Z_phys -> y,
    z_phys -> zp^-1.
For physical coordinates (a,b,c) in Z^a X^b z^c, reordering gives the exact
Pass1054 normal coordinates
    phi_H(a,b,c) = (b, a, -a*b-c) mod 3.
This is checked as a homomorphism on all 27^2 products.

For each of the 24 SL(2,3) matrices, use the unique element of Pass1054's
chosen complement having that quotient matrix.  This fixes the lift gauge.
Then every physical abstract normal form
    (a,b,c; M)
maps to one explicit source permutation on the 40 W33 points and one affine
permutation on the 27 Heisenberg states.

All 648^2 products are checked and a SHA256 digest of the full multiplication
index table is serialized.
"""
from __future__ import annotations
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path: sys.path.insert(0,str(ROOT/"analysis"))
OUT=ROOT/"data/w33_physical_clifford648_full_permutation_dictionary.json"

from w33_pass1054_1059_core import build_w33_bundle, cycle_partition, permutation_images

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def sorted_elements(group,degree=40):
    return sorted(group.generate_schreier_sims(),key=lambda e:tuple(permutation_images(e,degree)))

def commutator(left,right): return left**-1*right**-1*left*right

def mm(A,B):
    return tuple(sum(A[2*r+k]*B[2*k+c] for k in range(2))%3 for r in range(2) for c in range(2))

def main(write=True):
    physical=json.loads((ROOT/"data/w33_physical_a2_clifford648_w33_stabilizer_bridge.json").read_text())
    assert physical["status"]=="PASS_PHYSICAL_A2_H27_NORMALIZER_EQUALS_W33_CLIFFORD648_AT_QUOTIENT_ACTION_LEVEL"

    bundle=build_w33_bundle(); stabilizer=bundle.point_stabilizer
    elements=sorted_elements(stabilizer)
    center=stabilizer.center(); center_elements=set(center.generate_schreier_sims())

    # Reproduce Pass1054's deterministic normal H27 selection.
    normal_27=None
    for element in elements:
        if element.is_identity or element in center_elements or element.order()!=3: continue
        candidate=stabilizer.normal_closure(PermutationGroup([element]))
        if candidate.order()==27:
            normal_27=candidate; break
    assert normal_27 is not None
    normal_elements=sorted_elements(normal_27); normal_set=set(normal_elements)

    gens=None
    for x in normal_elements:
        if x.is_identity or x in center_elements: continue
        for y in normal_elements:
            if y.is_identity or y in center_elements: continue
            z=commutator(x,y)
            if not z.is_identity and z in center_elements and PermutationGroup([x,y]).order()==27:
                gens=(x,y,z); break
        if gens: break
    assert gens is not None
    x,y,zp=gens

    coordinate_of={}
    element_at=[None]*27
    for u,v,w in itertools.product(range(3),repeat=3):
        e=x**u*y**v*zp**w
        coordinate_of[e]=(u,v,w)
        element_at[9*u+3*v+w]=e
    assert len(coordinate_of)==27
    ordered_normal=list(element_at)
    normal_index={e:i for i,e in enumerate(ordered_normal)}

    sylow_two=stabilizer.sylow_subgroup(2)
    complement=None
    for element in elements:
        if element.order()!=3 or element in normal_set: continue
        candidate=PermutationGroup(list(sylow_two.generators)+[element])
        if candidate.order()==24 and len(set(candidate.generate_schreier_sims())&normal_set)==1:
            complement=candidate; break
    assert complement is not None
    complement_elements=sorted_elements(complement)
    assert len(complement_elements)==24

    decomposition={}
    for n in normal_elements:
        for l in complement_elements:
            e=n*l
            assert e not in decomposition
            decomposition[e]=(n,l)
    assert len(decomposition)==648

    def affine_image(element):
        n,l=decomposition[element]
        return Permutation([normal_index[n*l*state*l**-1] for state in ordered_normal])

    # Matrix -> unique chosen complement lift.
    matrix_to_lift={}
    matrix_offsets={}
    for l in complement_elements:
        cx=coordinate_of[l*x*l**-1]
        cy=coordinate_of[l*y*l**-1]
        M=(cx[0],cy[0],cx[1],cy[1])
        assert (M[0]*M[3]-M[1]*M[2])%3==1
        assert M not in matrix_to_lift
        matrix_to_lift[M]=l
        matrix_offsets[M]=(cx[2],cy[2])
    assert len(matrix_to_lift)==24

    # Physical H27 -> Pass1054 H27 exact homomorphism.
    def hmul(g,h):
        a,b,c=g; A,B,C=h
        return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
    H=list(itertools.product(range(3),repeat=3))
    def phi_coord(g):
        a,b,c=g
        return (b%3,a%3,(-a*b-c)%3)
    assert all(phi_coord(hmul(g,h))==hmul(phi_coord(g),phi_coord(h)) for g in H for h in H)
    def phi_elem(g):
        u,v,w=phi_coord(g)
        return x**u*y**v*zp**w

    matrices=sorted(matrix_to_lift)
    records=[]
    element_to_index={}
    for h in H:
        for M in matrices:
            e=phi_elem(h)*matrix_to_lift[M]
            idx=len(records)
            assert e not in element_to_index
            element_to_index[e]=idx
            records.append({
              "index":idx,
              "physical_H27_ZXz":[*h],
              "SL23_matrix_row_major":[*M],
              "chosen_lift_central_offsets_on_pass_x_y":[*matrix_offsets[M]],
              "W33_permutation_on_40":permutation_images(e,40),
              "affine_permutation_on_H27_27":permutation_images(affine_image(e),27),
              "order":int(e.order()),
              "cycle_partition_on_40":list(cycle_partition(e,40)),
            })
    assert len(records)==len(element_to_index)==648
    assert set(element_to_index)==set(elements)

    # Entire multiplication table as indices; verify closure and hash table.
    table=[]
    for e1 in [next(e for e,i in element_to_index.items() if i==k) for k in range(648)]:
        row=[]
        for e2 in [next(e for e,i in element_to_index.items() if i==k) for k in range(648)]:
            p=e1*e2
            assert p in element_to_index
            row.append(element_to_index[p])
        table.append(row)
    flat=",".join(str(x) for row in table for x in row).encode()
    digest="sha256:"+hashlib.sha256(flat).hexdigest()

    # Identity and generator labels.
    identity_idx=element_to_index[Permutation(list(range(40)))]
    F=(0,2,1,0); P=(1,0,1,1)
    assert F in matrix_to_lift and P in matrix_to_lift
    F_idx=element_to_index[matrix_to_lift[F]]
    P_idx=element_to_index[matrix_to_lift[P]]
    X_idx=element_to_index[phi_elem((0,1,0))]
    Z_idx=element_to_index[phi_elem((1,0,0))]
    z_idx=element_to_index[phi_elem((0,0,1))]

    out={
      "schema":"w33.physical_clifford648_full_permutation_dictionary.v1",
      "status":"PASS_ALL_648_PHYSICAL_QUTRIT_CLIFFORD_ELEMENTS_MAPPED_TO_W33_STABILIZER_PERMUTATIONS",
      "headline":"All 648 normal forms of the physical external-A2 qutrit Clifford/Hessian group are now mapped to explicit permutations in the selected W33 point stabilizer. The physical H27 identification X->x, Z->y, z_phys->z_pass^-1 is an exact homomorphism; each SL(2,3) matrix uses the unique element of Pass1054's chosen split complement, fixing the lift gauge. The resulting 648 source permutations exhaust the stabilizer, their affine degree-27 images are serialized, and all 648^2 products were checked.",
      "lift_gauge":{
        "physical_H27_normal_form":"Z^a X^b z^c",
        "Pass1054_normal_form":"x^u y^v zp^w",
        "generator_map":{"X_phys":"x","Z_phys":"y","z_phys":"zp^-1"},
        "coordinate_map":"(a,b,c) -> (b,a,-a*b-c) mod3",
        "SL23_lift_choice":"unique element of Pass1054's deterministic split complement with the requested quotient matrix"
      },
      "orders":{"H27":27,"SL23":24,"normalizer":648},
      "distinguished_indices":{"identity":identity_idx,"X":X_idx,"Z":Z_idx,"central_z":z_idx,"Fourier_lift":F_idx,"quadratic_phase_lift":P_idx},
      "Fourier_matrix":[*F],
      "quadratic_phase_matrix":[*P],
      "full_multiplication_table_shape":[648,648],
      "full_multiplication_table_digest":digest,
      "records":records,
      "checks":{
        "physical_H27_map_is_homomorphism_all_27_squared":True,
        "24_unique_split_lifts":True,
        "648_normal_forms_bijective":True,
        "source_permutations_exhaust_W33_point_stabilizer":True,
        "all_648_squared_products_checked":True,
        "affine_permutations_serialized":True
      },
      "boundary":"This is an exact finite group-element dictionary in a fixed split-complement gauge. It is not a unique complex 3x3 matrix gauge, and no hardware interpretation follows."
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","orders","distinguished_indices","full_multiplication_table_digest","checks")},indent=2))
    return out

if __name__=="__main__": main(True)
