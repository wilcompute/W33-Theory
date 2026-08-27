#!/usr/bin/env python3
"""Pass10781-10788: H27 + fixed-theta stable repair of the C13:C3 bridge.

Pass10709 killed a direct C13:C3 extension of
  F2[V2] ~= H1(Levi H4;F2),
and Pass10773 identified the C3-local virtual defect
  [F2[V2]]-[H1] = 8*1 - 4*W2.

Two existing geometries realize the two terms canonically at C3 level:
* H27: the central-C3 trivial Fourier sector is K9; its augmentation / -1
  adjacency eigenspace is 8-dimensional and C3-trivial, hence 8*1.
* the h-fixed H(4) Levi graph is Theta5 with beta1=4, so
  H1(Theta5;F2) tensor W2 = 4*W2.

Let G=C13:C3 (order 39) and H=C3.  Inducing both local corrections to G gives
104-dimensional modules.  The Frobenius group has conjugacy classes
  1, four C13-classes of size 3, two order-3 classes of size 13.
The base virtual character delta=[F2[V2]]-[H1] is
  0 on 1 and all nontrivial C13 elements, 12 on both order-3 classes.
But
  Ind_H^G(8*1) - Ind_H^G(4*W2)
has exactly the same Brauer character.  Since |G| is odd, F2[G] is semisimple,
so the equality of Brauer characters proves the stable module isomorphism

 F2[V2] + Ind(4W2) ~= H1(H4) + Ind(8*1).

This repairs the normalizer bridge stably; it does NOT restore a direct
4096-dimensional isomorphism.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10781_10788_H27_THETA_STABLE_NORMALIZER_REPAIR.json'

def main():
    theta=json.loads((ROOT/'data/PART_W33_PASS10773_10780_NORMALIZER_FIXED_THETA_DEFECT.json').read_text())
    h27=json.loads((ROOT/'data/PART_W33_PASS10581_10588_H27_CENTRAL_C3_FOURIER.json').read_text())
    assert theta['fixed_Levi_subgraph']['beta1']==4
    assert h27['trivial_sector']['spectrum']=={'-1':8,'8':1}
    assert h27['sector_dimensions']==[9,9,9]

    # C3-local modules over F2.
    # W2 has Brauer character (2,-1,-1) on (1,h,h^2).
    one=(1,1,1);W2=(2,-1,-1)
    E8=tuple(8*x for x in one)       # H27 -1 / K9 augmentation sector
    thetaW=tuple(4*x for x in W2)    # H1(Theta5) tensor W2
    assert E8==(8,8,8) and thetaW==(8,-4,-4)
    local_delta=tuple(a-b for a,b in zip(E8,thetaW))
    assert local_delta==(0,12,12)

    # G=C13:C3.  Class order: 1; four nontrivial C13 classes; h-class; h^2-class.
    class_sizes=[1,3,3,3,3,13,13]
    assert sum(class_sizes)==39
    base_delta=[0,0,0,0,0,12,12]

    # Ind_H^G: degree multiplies by 13.  At a complement element exactly one
    # H-coset is fixed because H is self-normalizing in this Frobenius group;
    # at a nontrivial C13 element the induced character vanishes.
    ind_E8=[104,0,0,0,0,8,8]
    ind_thetaW=[104,0,0,0,0,-4,-4]
    correction=[a-b for a,b in zip(ind_E8,ind_thetaW)]
    assert correction==base_delta

    # Stable dimensions match: each induced correction has dimension 104.
    assert ind_E8[0]==ind_thetaW[0]==104
    total=4096+104
    assert total==4200

    out={
      'schema':'w33.pass10781_10788.h27_theta_stable_normalizer_repair.v1','status':'PASS','passes':'10781-10788',
      'group':{'G':'C13:C3','order':39,'H':'C3','index':13,'class_sizes':class_sizes,'Maschke_over_F2':True},
      'local_C3_corrections':{
        'H27_E_minus1':'8*1, the 8-dimensional augmentation/-1 sector of the trivial central Fourier block K9',
        'fixed_theta':'H1(Theta5;F2) tensor W2 = 4*W2',
        'difference_character':'8*1 - 4*W2 = (0,12,12) on (1,h,h^2)'},
      'base_virtual_character_on_G':{
        'classes':'1; four nontrivial C13 classes; h; h^2',
        'F2V2_minus_H1':[0,0,0,0,0,12,12]},
      'induced_corrections':{
        'Ind_H^G_H27_E8':ind_E8,
        'Ind_H^G_thetaW2':ind_thetaW,
        'difference':correction,
        'dimension_each':104},
      'stable_isomorphism':{
        'statement':'F2[V2] direct-sum Ind_C3^G(H1(Theta5) tensor W2) ~= H1(Levi H4;F2) direct-sum Ind_C3^G(E_-1(H27))',
        'dimension_each_side':total,
        'proved':True,
        'reason':'the two semisimple F2[G] modules have identical Brauer characters on all seven odd conjugacy classes'},
      'theorem':'The direct C13:C3 bridge fails, but it has an exact 104-dimensional stable repair assembled from two existing project geometries. The H27 trivial central sector supplies the missing 8-dimensional trivial module, while the fixed Theta5 cycle space supplies the four W2 copies. Inducing these corrections from C3 to C13:C3 cancels the full Brauer-character defect and yields a genuine stable F2[C13:C3]-module isomorphism.',
      'boundary':'Stable semisimple module equivalence only. It does not produce a direct 4096-dimensional normalizer intertwiner, and it does not yet extend through the order-2 part of C13:C6 where characteristic 2 destroys Maschke semisimplicity.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','stable_dimension':4200,'correction_dimension':104,'direct_bridge':False,'stable_bridge':True}))
if __name__=='__main__':main()
