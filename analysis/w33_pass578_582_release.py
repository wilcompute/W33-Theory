#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass578_582_residual_colored_johnson_completion_continuous_release.json'
FILES={
 '578_helper':ROOT/'data'/'w33_pass578_fixed_locus_monomial_search.json',
 '578':ROOT/'data'/'w33_pass578_residual_collision_symmetry.json',
 '579':ROOT/'data'/'w33_pass579_colored_600cell_module.json',
 '580':ROOT/'data'/'w33_pass580_singer_johnson_fusion.json',
 '581':ROOT/'data'/'w33_pass581_cyclotomic_completion_formal.json',
 '582':ROOT/'data'/'w33_pass582_continuous_bellman_enclosure.json',
}

def payload():
 raw={k:f.read_bytes() for k,f in FILES.items()};p={k:json.loads(v) for k,v in raw.items()}
 checks={
  'all_owner_certificates_pass':all(x['status']=='PASS' for x in p.values()),
  'owner_check_total66':sum(sum(x['checks'].values()) for x in p.values())==66,
  'natural_global_symmetry_exactly_C3':p['578']['natural_global_search']['global_projective_maps']==3,
  'fixed_locus_projective_S3':p['578']['fixed_locus_S3']['projective_group_order']==6,
  'twenty_two_exceptional_triples_closed':p['578']['fixed_locus_S3']['size3_S3_orbits']==22,
  'residual_excess_reduced_to44191':p['578']['combined_partial_quotient']['residual_collision_excess']==44191,
  'five_snub_octahedral_colorings':p['579']['snub_octahedral_colorings']['count']==5,
  'colored_module_matches_3J3_plus_3J1':p['579']['module_bridge']['F3_Jordan_type']=={'J1':3,'J2':0,'J3':3},
  'apex_adds_thirteenth_singlet':p['579']['module_bridge']['with_apex']=={'J1':4,'J2':0,'J3':3},
  'four_symmetric_singer_fusions':len(p['580']['fusions'])==4,
  'Singer_quotient_is_J83':p['580']['imprimitivity']['identification']=='Johnson association scheme J(8,3)',
  'Singer_quotient_56_K6':p['580']['imprimitivity']['components']==56 and p['580']['imprimitivity']['component_size']==6,
  'Krein_parameters_nonnegative':p['580']['scheme']['krein']['all_nonnegative'],
  'Terwilliger_dimension38_center6':p['580']['terwilliger_J83_basepoint']['dimension']==38 and p['580']['terwilliger_J83_basepoint']['center_dimension']==6,
  'residue_quotient_F5':p['581']['algebra']['residue_quotient']=='O_5/(lambda) ~= F_5',
  'native_adic_completion_defined':p['581']['algebra']['completion']=='AdicCompletion (lambda) O_5',
  'continuous_Blackwell_marginals_exact':all(all(x['quartic_marginal_error']<1e-14 and x['orientation_marginal_error']<1e-14 for x in r['blackwell_marginals']) for r in p['582']['profiles'].values()),
  'strict_one_step_regions_all_profiles':all(r['strict_L1_neighborhood_radius']>0 for r in p['582']['profiles'].values()),
 }
 custody={k:{'path':str(FILES[k].relative_to(ROOT)),'sha256':hashlib.sha256(raw[k]).hexdigest(),'check_count':sum(p[k]['checks'].values())} for k in FILES}
 return {
  'schema':'w33.pass578_582.residual_colored_johnson_completion_continuous.release.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'owner_check_total':sum(x['check_count'] for x in custody.values()),'owner_custody':custody,
  'headline':{
   '578':'The natural global symmetry is exactly C3; an S3 enhancement on its fixed locus closes 22 of 23 exceptional triples and reduces residual orbit excess to 44,191.',
   '579':'Five colored 600-cell icosahedra realize the packet module on eight yellow faces plus four opposite-face pairs, with Jordan type 3J3+3J1 and an apex singlet.',
   '580':'The rank-nine Singer scheme has four symmetric fusions and a canonical quotient Johnson scheme J(8,3) on 56 six-cliques.',
   '581':'Lean source identifies O5/(lambda) with F5 and defines the native lambda-adic completion.',
   '582':'Continuous joint actions Blackwell-dominate quartic marginals and have explicit strict one-step L1 advantage neighborhoods around the uniform prior.',
  },
  'release_checks':checks,
  'boundary':'Exact for the stated natural relabeling and monomial symmetry searches, colored 600-cell face object, Singer association scheme, native Lean source scaffold, and declared readout model. No arbitrary nonlinear collision-group classification, full A4 packet intertwiner, objectwise E6 identification, completed DVR/field theorem, or strict infinite-horizon continuous Bayes theorem is claimed.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Passes 578-582 release certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['release_checks'].values()),'total':len(p['release_checks']),'owners':p['owner_check_total']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
