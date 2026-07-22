#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass568_572_singer_hjelmslev_residue_walsh_chernoff_release.json'
FILES={n:ROOT/'data'/f for n,f in {
568:'w33_pass568_singer_intersection_design.json',
569:'w33_pass569_z9_coupled_affine_radial_quadratic.json',
570:'w33_pass570_cyclotomic_residue_formal.json',
571:'w33_pass571_twisted_walsh_representation.json',
572:'w33_pass572_analytic_sequential_bound.json'}.items()}

def payload():
 raw={n:f.read_bytes() for n,f in FILES.items()};p={n:json.loads(raw[n]) for n in FILES}
 w=p[568]['families']['Witting_fixed_16_line_stabilizer']['intersection_signature_census']
 final=p[569]['layers'][-1]
 checks={
  'all_owner_certificates_pass':all(x['status']=='PASS' for x in p.values()),
  'singer_conjugates336':p[568]['ambient']['Singer_normalizer_conjugates']==336,
  'witting_intersection_census_240_72_24':sorted(w.values())==[24,72,240],
  'witting_orbits10':p[568]['incidence_summary']['witting_orbit_count']==10,
  'point_plane_duality_exact':p[568]['incidence_summary']['duality_point_plane_census_equal'],
  'hjelmslev_dimension13':p[569]['family']['parameter_space']=='F3^13',
  'hjelmslev_sections_3pow13':final['sections']==3**13,
  'hjelmslev_exact_image221451':final['distinct_charpolys']==221451,
  'hjelmslev_not_near_injective':final['projective_injectivity_ratio']<0.3,
  'residue_map_formalized':p[570]['checks']['all_theorem_names_present'],
  'completion_boundary_explicit':len(p[570]['remaining_completion_obligations'])==4,
  'walsh_irreducible_degrees_exact':p[571]['checks']['irreducible_degrees_eight1_eight2'],
  'walsh_full_multiplicities_104_204':p[571]['checks']['full_rep_multiplicities_104_204'],
  'six_character_formula_signatures':p[571]['checks']['six_formula_signatures'],
  'chernoff_orientation_bottleneck':p[572]['checks']['joint_bottleneck_is_orientation_pair'],
  'coarse_bound_negative_result_locked':p[572]['checks']['coarse_union_bound_does_not_certify_empirical_gain'],
 }
 custody={n:{'path':str(FILES[n].relative_to(ROOT)),'sha256':hashlib.sha256(raw[n]).hexdigest(),'check_count':len(p[n]['checks'])} for n in FILES}
 return {
  'schema':'w33.pass568_572.singer_hjelmslev_residue_walsh_chernoff.release.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'headline':{
   'singer':'The 336 Singer normalizers form a 10-orbit incidence design under the Witting order-48 stabilizer; intersections are 240 trivial, 72 C2, and 24 C4.',
   'hjelmslev':'The exact F3^13 family has 1,594,323 sections and 221,451 characteristic polynomials; after sign reduction the injectivity ratio is 0.2778, so near-injectivity fails.',
   'residue':'Lean now contains the native reduction map O5 -> F5, surjectivity, and uniformizer-kernel containment, while completion obligations remain explicit.',
   'walsh':'The 4096-dimensional signed Walsh representation is 104 copies of each of eight 1D irreps plus 204 copies of each of eight 2D irreps; six fibre formula signatures result.',
   'chernoff':'The exact cost-aware Chernoff LP is orientation-pair dominated; its coarse union bound is 13-14% looser than the staged bound and therefore cannot certify the Monte Carlo gain.'
  },
  'owner_check_total':sum(len(p[n]['checks']) for n in p),'owner_custody':custody,'release_checks':checks,
  'boundary':'Exact for the declared GL(4,2) subgroup families, the structured F3^13 Hjelmslev module, the native residue-map scaffold, the fixed q=5 Walsh representation, and the stated Chernoff model. No full W(3,3) subgroup embedding, full 9^40 image, completed Q5(zeta5), or measured hardware theorem is claimed.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 568-572 release certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'owner_checks':p['owner_check_total'],'release_checks':sum(p['release_checks'].values()),'release_total':len(p['release_checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
