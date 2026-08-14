#!/usr/bin/env python3
"""Pass5205: exact diagnostic wall for q=5 chamber leader 36.

Pass5200 closes leader 35 with C_35=65. Edge deletion gives the raw m=36
adjacent-pair cap 68. The edge-type relaxation has no feasible N1=68 profile,
so N1<=67.

This producer applies the complete Pass5200 stack profile-by-profile:
  * exact q=5 Delsarte pair optimization conditioned by P4<=N3 and P5<=2N4;
  * edge-type N112;
  * local P4 and sharp P5 lower bounds;
  * both valid cubic parity minorants, taking their maximum;
  * the degree-edge-type full-apartment cap from Pass5199.

The method closes N1<=53 and N1>=65, but leaves the contiguous window
54<=N1<=64.  The best uniform integer lower bounds on that window are

  584,551,531,542,553,574,535,556,567,579,590.

Thus the Pass5198--5200 full-apartment correction has reached a genuine
leader-36 wall.  The failure is not hidden in one isolated profile: eleven
adjacent-pair layers survive.  Pass5185's full cut-coset inequality and the
Pass5201--5203 P-footprint quotient are therefore the two natural independent
next constraints.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5173_q5_leader31_sharp_p5_extension import p5_sharp
from analysis.w33_pass5183_q5_leader33_p5_n4_coupling import pair_coupled
from analysis.w33_pass5199_q5_leader35_edgetype_full_apartment_correction import (
    edge_type_solutions,p5_upper_from_edge_types)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5205_Q5_LEADER36_FULL_APARTMENT_WALL.json'


def row(m,W,prev,p):
    minsum=max(2,W-prev+2)
    n112,_=edge_type_n112_floor(*p,minsum);p4,_=p4_relaxed(*p,minsum)
    if n112 is None or p4 is None:return None
    p5=p5_sharp(p4,p[0],p[1])
    z=pair_coupled(m,W,p4,(p5+1)//2)
    if z is None:return None
    _,dist,_,pair_lb=z;s3=25*n112+10*p4+3*p5
    es=list(edge_type_solutions(*p,minsum));assert es
    p5up=max(p5_upper_from_edge_types(e) for e in es);a8=p5up//8
    ordinary=ceil_frac(Fraction(pair_lb)+Fraction(6,7)*s3)
    corrected=ceil_frac(Fraction(pair_lb)+Fraction(36,35)*s3-Fraction(48,5)*a8)
    return {'degree_counts':list(p),'N112_lower':n112,'P4_lower':p4,
      'P5_lower':p5,'conditioned_distance_counts':list(dist),
      'pair_weight_lower_bound':pair_lb,'S3_lower':s3,
      'P5_edge_type_upper':p5up,'A8_upper':a8,
      'ordinary_integer_lower_bound':ordinary,'corrected_integer_lower_bound':corrected,
      'combined_integer_lower_bound':max(ordinary,corrected)}

def main():
    m=36;prev=65;raw=prev*m//(m-2);assert raw==68
    assert all(edge_type_n112_floor(*p,5)[0] is None for p in profiles(m,68))
    cap=67
    expected={46:1949,47:1767,48:1583,49:1434,50:1284,51:1100,52:950,53:768,
      54:584,55:551,56:531,57:542,58:553,59:574,60:535,61:556,62:567,63:579,
      64:590,65:643,66:1544,67:2907}
    layers={}
    for W,E in expected.items():
        rows=[x for p in profiles(m,W) if (x:=row(m,W,prev,p)) is not None]
        assert rows
        lb=min(x['combined_integer_lower_bound'] for x in rows);assert lb==E,(W,lb,E)
        layers[str(W)]={'uniform_lower_bound':lb,'profiles':rows}
    open_window={str(W):layers[str(W)]['uniform_lower_bound'] for W in range(54,65)}
    deficits={str(W):626-open_window[str(W)] for W in range(54,65)}
    assert all(layers[str(W)]['uniform_lower_bound']>=625 for W in list(range(46,54))+[65,66,67])
    assert all(v<625 for v in open_window.values())

    critical={}
    for W in range(54,65):
        b=min(layers[str(W)]['profiles'],key=lambda x:x['combined_integer_lower_bound'])
        critical[str(W)]={k:b[k] for k in ('degree_counts','N112_lower','P4_lower','P5_lower',
          'conditioned_distance_counts','pair_weight_lower_bound','S3_lower','P5_edge_type_upper',
          'A8_upper','ordinary_integer_lower_bound','corrected_integer_lower_bound',
          'combined_integer_lower_bound')}

    out={'pass':5205,'status':'EXACT_Q5_LEADER36_FULL_APARTMENT_METHOD_WALL',
      'q':5,'leader_size_diagnostic':36,'target_distance':625,
      'previous_adjacent_pair_cap':prev,'raw_deletion_cap':raw,'relaxed_adjacent_pair_cap':cap,
      'safe_layers':{str(W):expected[W] for W in list(range(46,54))+[65,66,67]},
      'open_adjacent_pair_window':open_window,'units_needed_to_reach_strict_626':deficits,
      'critical_profiles':critical,
      'conclusion':'The complete Pass5200 cubic/full-apartment relaxation does not close leader 36. Its unresolved window is exactly N1=54..64; all lower tested layers and N1=65..67 are above target, while N1=68 is locally infeasible.',
      'next_constraints':'Use the full Pass5185 cut-coset inequalities on multi-vertex shores to reject or sharpen the listed critical selected-degree profiles; independently use the Pass5201--5203 P-footprint quotient/minimum-distance problem to bypass leader recursion.',
      'boundary':'This is a rigorous diagnostic of the current relaxation, not a q5 distance advance. Strict counterexamples are proved only to require leader >=36 by Pass5200. No claim about leader 36, d=625, or the equality shell is made.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
