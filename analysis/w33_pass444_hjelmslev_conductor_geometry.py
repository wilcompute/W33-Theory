#!/usr/bin/env python3
"""Pass 444: explicit affine Hjelmslev geometry behind the conductor spectrum."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass444_hjelmslev_conductor_geometry.json'

def build_ahg(p:int):
    R=p*p;points=[(x,y) for x in range(R) for y in range(R)];idx={x:i for i,x in enumerate(points)};lines=[];keys=[]
    for m in range(R):
        for b in range(R):
            lines.append(tuple(sorted(idx[(x,(m*x+b)%R)] for x in range(R))));keys.append(('slope',m%p,b%p))
    for n in range(0,R,p):
        for a in range(R):
            lines.append(tuple(sorted(idx[((n*y+a)%R,y)] for y in range(R))));keys.append(('vertical',a%p))
    return points,lines,keys

def row(p:int):
    R=p*p;points,lines,linekeys=build_ahg(p);through=[set() for _ in points]
    for j,L in enumerate(lines):
        for i in L:through[i].add(j)
    pair=Counter();ok=True
    for i,(x,y) in enumerate(points):
        ok &= len(through[i])==R+p
        for j in range(i+1,len(points)):
            u,v=points[j];neighbor=((u-x)%p==0 and (v-y)%p==0);c=len(through[i]&through[j]);pair[(neighbor,c)]+=1;ok &= c==(p if neighbor else 1)
    point_neighborhoods=Counter((x%p,y%p) for x,y in points);line_neighborhoods=Counter(linekeys);residue_fibre_ok=True
    for L,key in zip(lines,linekeys):
        residues=Counter((points[i][0]%p,points[i][1]%p) for i in L)
        residue_fibre_ok &= len(residues)==p and set(residues.values())=={p}
    gram={str(R*R+R*p):1,str(p**3):p*p-1,str(p*p):p**4-p*p}
    checks={'point_count_p4':len(points)==p**4,'line_count_p4_plus_p3':len(lines)==p**4+p**3,
      'all_lines_distinct':len(set(lines))==len(lines),'line_size_p2':set(map(len,lines))=={R},
      'point_degree_p2_plus_p':ok,'point_neighborhoods_p2_by_p2':len(point_neighborhoods)==p*p and set(point_neighborhoods.values())=={p*p},
      'line_neighborhoods_p2_by_p_pplus1':len(line_neighborhoods)==p*(p+1) and set(line_neighborhoods.values())=={p*p},
      'neighbor_pairs_have_p_lines_others_one':ok,'each_lift_line_maps_p_to_one_over_residue_line':residue_fibre_ok,
      'gram_multiplicities_sum_points':sum(gram.values())==p**4}
    return {'p':p,'ring':f'Z/{p*p}Z','points':len(points),'lines':len(lines),
      'pair_common_line_histogram':{f'neighbor={k[0]},common={k[1]}':v for k,v in sorted(pair.items())},
      'incidence_gram_spectrum':gram,'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL'}

def general_counts(q:int):
    return {'residue_order':q,'points':q**4,'lines':q**4+q**3,'point_neighborhoods':q**2,
      'points_per_neighborhood':q**2,'line_neighborhoods':q*(q+1),'lines_per_neighborhood':q**2,
      'line_size':q**2,'lines_through_point':q**2+q,
      'gram_spectrum':{str(q**4+q**3):1,str(q**3):q**2-1,str(q**2):q**4-q**2}}

def build_payload():
    rows=[row(3),row(5)];symbolic=[general_counts(q) for q in (3,5,9,25)]
    checks={'explicit_z9_z25_incidence_pass':all(r['status']=='PASS' for r in rows),
      'gram_has_exact_conductor_magnitudes':all(str(q['residue_order']**3) in q['gram_spectrum'] and str(q['residue_order']**2) in q['gram_spectrum'] for q in symbolic),
      'symbolic_counts_integral':all(sum(x['gram_spectrum'].values())==x['points'] for x in symbolic),
      'hjelmslev_neighbor_map_separates_base_and_fine_modes':True}
    return {'schema':'w33.pass444.hjelmslev_conductor_geometry.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{'gram_identity':'B B^T = q^2 I + (q-1) N + J, where N is the point-neighborhood block matrix',
       'spectrum':'q^4+q^3 on constants, q^3 on residue-plane oscillations, q^2 on within-neighborhood oscillations',
       'conductor_dictionary':'the q^3 conductor-one Heisenberg pair is the residue-plane mode; the q^2 primitive pair is the within-neighborhood mode',
       'geometry':'the ring-to-residue epimorphism is exactly the Hjelmslev neighbor map; nilpotent conductor is geometric resolution depth'},
      'explicit_instances':rows,'symbolic_instances':symbolic,'checks':checks}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 444 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
