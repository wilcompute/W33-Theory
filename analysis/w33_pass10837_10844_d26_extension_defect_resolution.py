#!/usr/bin/env python3
"""Pass10837-10844: resolve the order-2 defect as a D26 extension-class obstruction.

Earlier exact data:
* C13 acts freely on V2\{0}: 315 nonzero vector cycles plus zero, so the
  C13-fixed part of the permutation module F2[V2] has dimension 316.
* k=n^3 is an involution inverting C13.  It fixes 64 vectors of V2.
* On the H(4) Levi graph k fixes 21 points,25 lines,45 flags and this fixed
  subgraph is a tree.
* The full k-invariant dimensions are 2080 on F2[V2] and 2048 on H1.

The 64 fixed vectors consist of zero plus one fixed point in each k-stable
nonzero C13 orbit.  Hence k fixes 63 of the 315 nonzero C13 cycles.  On the
316-dimensional C13-fixed permutation sector this gives

    1^64 + J2^126,

where J2 is the two-dimensional regular/Jordan F2[C2]-module.

On the C13 quotient Levi graph there are 210 vertices and 525 edges.  The
induced k action has the same 46 fixed vertices and45 fixed edges, so the
further quotient has

    V=(210+46)/2=128, E=(525+45)/2=285, beta1=158.

Because the fixed subgraph is a tree, invariant-chain elimination gives the
same fixed dimension 158 on H1 of the quotient.  Since this sector itself has
dimension316, it is exactly J2^158.

The complementary nontrivial C13-isotypic sector is W12^315 on both sides.
Here inversion is the degree-six Frobenius on F_{2^12} because 2^6=-1 mod13.
By nonabelian Hilbert 90, every semilinear involution A sigma with
A sigma(A)=1 is conjugate to sigma, even with multiplicity.  Thus the D26
extension of W12^315 is unique up to module isomorphism.  The entire D26 defect
therefore lies in the trivial C13 sector.

Minimal stable repair:

 F2[V2] + J2^32  ~=  H1(Levi H4;F2) + 1^64

as F2[D26]-modules, with C13 acting trivially on both correction modules.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10837_10844_D26_EXTENSION_DEFECT_RESOLUTION.json'

def ordmod(a,n):
    x=1
    for k in range(1,n+1):
        x=x*a%n
        if x==1:return k
    raise RuntimeError

def main():
    # Existing exact counts from Pass10789 and Pass10501.
    dim=4096; c13_fixed=316; nontriv_dim=dim-c13_fixed
    assert nontriv_dim==3780==315*12
    assert ordmod(2,13)==12 and pow(2,6,13)==12  # inversion = Frobenius^6

    # V2 permutation module under k.
    k_fixed_vectors=64
    stable_nonzero_c13_cycles=k_fixed_vectors-1
    assert stable_nonzero_c13_cycles==63
    paired_nonzero_c13_cycles=(315-stable_nonzero_c13_cycles)//2
    assert paired_nonzero_c13_cycles==126
    v_trivial_blocks=64
    v_jordan_blocks=126
    assert v_trivial_blocks+2*v_jordan_blocks==316
    assert v_trivial_blocks+v_jordan_blocks==190

    # H4/C13 quotient followed by k.
    qV,qE=210,525
    fixed_vertices=21+25; fixed_edges=45
    assert (fixed_vertices,fixed_edges)==(46,45)
    kkV=(qV+fixed_vertices)//2; kkE=(qE+fixed_edges)//2
    assert (kkV,kkE)==(128,285)
    h_c13_k_fixed=kkE-kkV+1
    assert h_c13_k_fixed==158
    h_trivial_blocks=0
    h_jordan_blocks=158
    assert h_trivial_blocks+2*h_jordan_blocks==316

    # The complementary W12^315 sectors already have equal C2 fixed dimension.
    full_v_k=2080; full_h_k=2048
    v_nontriv_k=full_v_k-(v_trivial_blocks+v_jordan_blocks)
    h_nontriv_k=full_h_k-h_c13_k_fixed
    assert v_nontriv_k==h_nontriv_k==1890==315*6

    # Stable repair dimensions and block counts.
    # Add 32 regular J2 blocks to V2 side; add 64 trivial blocks to H1 side.
    lhs_dim=dim+32*2; rhs_dim=dim+64
    assert lhs_dim==rhs_dim==4160
    assert v_trivial_blocks==64
    assert v_jordan_blocks+32==h_jordan_blocks

    out={
      'schema':'w33.pass10837_10844.d26_extension_defect_resolution.v1','status':'PASS','passes':'10837-10844',
      'group':{'D26':'C13:C2 with inversion','characteristic':2,'inversion_as_Frobenius':'2^6 = -1 mod 13','ord_13_2':12},
      'C13_fixed_sector':{
        'dimension':316,
        'F2V2_C2_decomposition':'1^64 + J2^126',
        'F2V2_k_fixed_dimension':190,
        'stable_nonzero_C13_cycles':63,
        'paired_nonzero_C13_cycle_pairs':126,
        'H1_C2_decomposition':'J2^158',
        'H1_k_fixed_dimension':158,
        'quotient_graph':{'vertices':210,'edges':525,'k_fixed_vertices':46,'k_fixed_edges':45,'k_quotient_vertices':128,'k_quotient_edges':285,'beta1':158}},
      'nontrivial_C13_sector':{
        'module':'W12^315','dimension':3780,'k_fixed_dimension_each_side':1890,
        'uniqueness_reason':'inversion is Frobenius^6 on F_{2^12}; nonabelian Hilbert 90 conjugates every semilinear involution A sigma with A sigma(A)=1 to sigma, including multiplicity 315'},
      'minimal_stable_repair':{
        'statement':'F2[V2] direct-sum J2^32 ~= H1(Levi H4;F2) direct-sum 1^64 as F2[D26]-modules',
        'corrections_C13_trivial':True,'dimension_each_side':4160,
        'meaning':'the 32-number counts missing nonsplit extensions, not a missing 32-dimensional simple carrier'},
      'theorem':'The characteristic-2 order-two obstruction is completely localized in the 316-dimensional C13-fixed sector. F2[V2] has 64 split trivial states plus126 Jordan blocks, whereas hexagon homology has158 Jordan blocks and no split trivial states. The W12^315 sector already has the unique compatible D26 semilinear extension. Hence the exact defect is 32 missing nonsplit extensions and admits the displayed minimal stable repair.',
      'boundary':'All counting and C2-module decompositions are exact from existing certificates. Uniqueness of the nontrivial D26 extension uses standard nonabelian Hilbert 90 for GL_315(F_{2^12}) under the degree-two fixed-field involution.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','trivial_sector':['1^64+J2^126','J2^158'],'repair':'V2+J2^32 ~= H1+1^64'}))
if __name__=='__main__':main()
