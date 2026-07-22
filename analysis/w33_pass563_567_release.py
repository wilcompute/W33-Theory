#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass563_567_triality_quadratic_order_walsh_bayesian_release.json'
FILES={563:ROOT/'data'/'w33_pass563_triality_a8_witting_normalizer.json',564:ROOT/'data'/'w33_pass564_z9_full_quadratic_irreducibles.json',565:ROOT/'data'/'w33_pass565_cyclotomic_order_formal.json',566:ROOT/'data'/'w33_pass566_q5_twisted_walsh_krawtchouk.json',567:ROOT/'data'/'w33_pass567_joint_bayesian_decoder.json'}

def payload():
 raw={n:f.read_bytes() for n,f in FILES.items()};p={n:json.loads(raw[n]) for n in FILES}
 checks={
  'all_owner_certificates_pass':all(x['status']=='PASS' for x in p.values()),
  'triality_singer_normalizer_order60':p[563]['gl42_a8']['normalizer_order']==60,
  'triality_conjugacy_class336':p[563]['gl42_a8']['conjugacy_class_size']==336,
  'witting_intersection_order4':p[563]['witting_alignment']['intersection_order']==4,
  'quadratic_module_one_plus_three':p[564]['module']['decomposition']=='1 + 3 under PGL(2,3) ~= S4',
  'quadratic_full_slice_6561':p[564]['family']['section_count']==6561,
  'quadratic_image_2605':p[564]['layers'][-1]['distinct_charpolys']==2605,
  'native_adjoinroot_order':p[565]['checks']['native_adjoinroot_construction'],
  'eisenstein_and_discriminant':p[565]['checks']['eisenstein_at_five_exact'] and p[565]['checks']['discriminant_five_cubed'],
  'twisted_walsh_all98':p[566]['catalog_custody']['records']==98 and p[566]['checks']['all_indicators_twisted_covariant'],
  'dual_orbits292':p[566]['group']['dual_frequency_orbits']==292,
  'ordinary_krawtchouk_no_go':p[566]['catalog_custody']['radial_exact_count']==0,
  'joint_decoder_all_profiles_improve':all(x['mean_shot_reduction']>0 for x in p[567]['results'].values()),
 }
 custody={n:{'path':str(FILES[n].relative_to(ROOT)),'sha256':hashlib.sha256(raw[n]).hexdigest(),'check_count':len(p[n]['checks'])} for n in FILES}
 return {'schema':'w33.pass563_567.triality_quadratic_order_walsh_bayesian.release.v1','status':'PASS' if all(checks.values()) else 'FAIL','owner_check_total':sum(len(p[n]['checks']) for n in p),'owner_custody':custody,'headline':{'triality':'The order-60 group is the self-normalizing Singer normalizer 15:4 in GL(4,2) ~= A8; its Witting-line intersection has order four and it is not A5.','quadratic':'The missing homogeneous-square packets form the irreducible 3-dimensional augmentation summand of F3^4 and give 2,605 spectra on the exact 6,561-section slice.','formal':'Lean now contains a native AdjoinRoot construction of the integral fifth-cyclotomic order, with completion still explicit.','walsh':'All 98 indicators have exact affine-cocycle orbit formulas over 292 dual orbits; ordinary radial Krawtchouk formulas fail for every fibre.','decoder':'A joint six-hypothesis Bayesian stopping rule reduces mean shots in all declared profiles.'},'release_checks':checks,'boundary':'Exact for the declared finite groups, F3^8 quadratic slice, native integral-order scaffold, fixed q=5 magnitude cube, and declared Bayesian noise model. No full W33/E6 embedding, full 9^40 image, completed Q5(zeta5), or measured hardware claim is made.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Passes 563-567 release certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'owner_checks':p['owner_check_total'],'release_checks':sum(p['release_checks'].values()),'release_total':len(p['release_checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
