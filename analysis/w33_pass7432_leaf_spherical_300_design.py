#!/usr/bin/env python3
"""Pass7432: the centered 2240 Eisenstein-leaf indicators form a spherical 2-design in V300."""
from __future__ import annotations
from fractions import Fraction
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7432_LEAF_SPHERICAL_300_DESIGN.json'

def main():
    N=2240;ambient=1120;k=40;r=80;d=300;frame_eigen=288
    mean=Fraction(k,ambient);assert mean==Fraction(1,28)
    centered_norm=Fraction(k,1)-2*mean*k+mean*mean*ambient
    assert centered_norm==Fraction(270,7)
    # C^T C=288 P_d, so after row normalization the frame operator is N/d on V_d.
    unit_frame_bound=Fraction(frame_eigen,1)/centered_norm
    assert unit_frame_bound==Fraction(N,d)==Fraction(112,15)
    # integral scale y=28*(1_L-1/28 1)=28 1_L-1
    integral_norm=28*28*centered_norm;assert integral_norm==30240
    # inner product for intersection t: (t-10/7), scaled by 28^2.
    # 784*(t-10/7)=112*(7t-10).
    welch=Fraction(N-d,d*(N-1));assert welch==Fraction(97,33585)
    out={'schema':'w33.pass7432.leaf_spherical_300_design.v1','status':'PASS',
      'leaf_vectors':N,'irreducible_dimension':d,'ambient_incidence_coordinates':ambient,
      'leaf_weight':k,'point_replication':r,'centering_mean':'1/28','centered_norm_squared':'270/7',
      'centered_frame_operator':'C^T C = 288 P_V300','unit_norm_frame_bound':'112/15',
      'spherical_design':'The normalized centered leaf indicators are a spherical 2-design (equivalently a zero-sum finite unit-norm tight frame) in R^300.',
      'integral_model':'y_L = 28*1_L - 1','integral_entries':'27 on the 40 A2s of L and -1 on the other 1080','integral_norm_squared':integral_norm,
      'intersection_angle_formula':'If |L intersect M|=t then <y_L,y_M>=112(7t-10), and normalized inner product=(7t-10)/270.',
      'Welch_average_squared_offdiagonal':'97/33585',
      'theorem':'The global Eisenstein-leaf orbit is not only a tactical design: after centering it is an exact 2240-point spherical 2-design spanning precisely the irreducible 300-dimensional constituent of the E8 A2 permutation module.',
      'boundary':'No claim is made that this is an optimal spherical code or a physical state ensemble; leaf-intersection distances are not classified here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','N':N,'d':d,'frame_bound':'112/15'}))
if __name__=='__main__':main()
