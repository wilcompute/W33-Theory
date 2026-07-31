#!/usr/bin/env python3
"""Pass 1534: exact affine geometry of the certified four-cover packing."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data'/'w33_pass1511_1515_cover_resolution_frontiers.json'
def certificate()->dict:
 src=json.loads(SOURCE.read_text());pack=src['pass1513_disjointness_graph_and_four_packing']['packing'];res=src['pass1515_residual_integrality_gap']
 X=np.zeros((540,4),dtype=np.int64)
 for j,c in enumerate(pack):X[c,j]=1
 Y9=9*X-np.ones((540,4),dtype=np.int64)
 gram=Y9.T@Y9;expected=np.full((4,4),-540,dtype=np.int64);np.fill_diagonal(expected,4320)
 used=X.sum(axis=1);s=Y9.sum(axis=1)
 yfrac45=-s;expected_fraction=np.where(used==1,-5,4)
 checks={
  'upstream_four_packing_exact':src['checks']['pass1513_four_packing_exact'],
  'upstream_pairwise_disjoint':src['checks']['pass1513_four_packing_pairwise_disjoint'],
  'four_sets_size_60':all(len(c)==60 for c in pack),
  'packing_disjoint_literal':np.array_equal(X.T@X,60*np.eye(4,dtype=np.int64)),
  'centered_gram_exact':np.array_equal(gram,expected),
  'covered_frames_240':int(used.sum())==240,
  'residual_frames_300':int((used==0).sum())==300,
  'fractional_projection_coordinates':np.array_equal(yfrac45,expected_fraction),
  'fractional_projection_norm_16_over_3':int(yfrac45@yfrac45)==10800,
  'upstream_uniform_fractional_cover':src['checks']['pass1515_uniform_fractional_cover'],
  'upstream_no_fifth_integral_cover':src['checks']['pass1515_no_fifth_integral_cover'],
 }
 checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
 return {
  'schema':'w33.pass1534.four_packing_simplex.v1','status':'PASS',
  'theorem':'The certified four-packing is a regular centered-cover 3-simplex. Its residual uniform 1/5 layer is exactly the orthogonal projection required of any fifth cover, but the remaining norm-48 integral shell is empty.',
  'gram':{'unscaled':'diag 160/3, off-diagonal -20/3','scaled_by_81':gram.tolist()},
  'projection':{'formula':'y_frac=-(1/5)(y_1+y_2+y_3+y_4)','norm_squared':'16/3','coordinates':'-1/9 on the 240 used frames and 4/45 on the 300 residual frames'},
  'integral_shell':{'candidate_formula':'y_5=y_frac+z','orthogonality':'z perpendicular to span(y_1,...,y_4)','required_norm_squared':48,
    'residual_coordinates':'z=4/5 on 60 selected residual frames and -1/5 on the other 240 residual frames','existence':False,
    'exhaustive_search_nodes':res['integral_search']['nodes'],'trace_sha256':res['integral_search']['trace_sha256']},
  'checks':checks,
  'boundary':'This empties the affine shell over this particular four-packing. It does not prove that every four-packing is blocked or that chi(H)>9.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--check',action='store_true');a=ap.parse_args();r=certificate();t=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(t)
 if not a.check or not a.output:print(t,end='')
if __name__=='__main__':main()
