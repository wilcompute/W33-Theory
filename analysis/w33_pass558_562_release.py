#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass558_562_triality_radial_localfield_noise_tensor_release.json'
FILES={558:ROOT/'data'/'w33_pass558_q5_triality_partition.json',559:ROOT/'data'/'w33_pass559_z9_radial_quadratic_automaton.json',560:ROOT/'data'/'w33_pass560_cyclotomic_uniformizer_formal.json',561:ROOT/'data'/'w33_pass561_noise_aware_orientation_latch.json',562:ROOT/'data'/'w33_pass562_q5_tensor_type_derivation.json'}

def payload():
    raw={n:f.read_bytes() for n,f in FILES.items()};p={n:json.loads(raw[n]) for n in FILES}
    checks={
      'all_owner_certificates_pass':all(x['status']=='PASS' for x in p.values()),
      'pg32_partition_exact':p[558]['checks']['quotient_is_pg32_nonzero_points'],
      'triality_s3_exact':p[558]['partition_stabilizer']['block_action']=='S3',
      'triality_group_order60':p[558]['partition_stabilizer']['order']==60,
      'z9_extended_sections_59049':p[559]['layers'][-1]['sections']==59049,
      'z9_extended_image_9266':p[559]['layers'][-1]['distinct_charpolys']==9266,
      'z9_projective_history_3281':p[559]['minimal_future_automaton']['layers'][4]['minimal_markov_states']==3281,
      'cyclotomic_ramification_formalized':p[560]['checks']['actual_cyclotomic_identity_formalized'],
      'uniformizer_value_theorem_present':p[560]['checks']['all_theorem_names_present'],
      'quartic_margin_3750':abs(p[561]['quartic_gate']['minimum_four_embedding_distance_squared']-3750)<1e-6,
      'adaptive_noise_selector':p[561]['checks']['hybrid_selector_is_pointwise_minimum'],
      'tensor_five_types_exact':p[562]['checks']['five_type_census_exact'],
      'tensor_walsh_geometry_lock':p[562]['checks']['walsh_translation_theorem_matches_geometry'],
    }
    summaries={
      'pass558':{'status':p[558]['status'],'group_order':p[558]['partition_stabilizer']['order'],'block_action':p[558]['partition_stabilizer']['block_action'],'kernel':p[558]['partition_stabilizer']['block_action_kernel'],'fibre_ids':p[558]['fibre_ids']},
      'pass559':{'status':p[559]['status'],'sections':p[559]['layers'][-1]['sections'],'image':p[559]['layers'][-1]['distinct_charpolys'],'state_counts':[x['minimal_markov_states'] for x in p[559]['minimal_future_automaton']['layers']]},
      'pass560':{'status':p[560]['status'],'lean_file':p[560]['lean_file'],'formalized':p[560]['formalized']},
      'pass561':{'status':p[561]['status'],'quartic_distance_squared':p[561]['quartic_gate']['minimum_four_embedding_distance_squared'],'selected_architectures':{k:v['selected_architecture'] for k,v in p[561]['orientation_profiles'].items()}},
      'pass562':{'status':p[562]['status'],'type_counts':p[562]['type_counts'],'transform_catalog_sha256':p[562]['transform_catalog_sha256']},
    }
    custody={str(n):{'path':str(FILES[n].relative_to(ROOT)),'sha256':hashlib.sha256(raw[n]).hexdigest(),'check_count':sum(p[n]['checks'].values())} for n in FILES}
    return {'schema':'w33.pass558_562.triality_radial_localfield_noise_tensor.release.v1','status':'PASS' if all(checks.values()) else 'FAIL','owner_check_total':sum(x['check_count'] for x in custody.values()),'headline':{'triality':'Three five-cube fibres partition PG(3,2); stabilizer C15 semidirect C4 acts as S3 with D10 kernel.','z9':'Radial and quadratic packets enlarge the exact image to 9,266 polynomials over 59,049 sections.','formal':'Lean proves the translated Phi5 identity, ramification factorization, and valuation-one consequence under standard valuation laws.','noise':'The optimal orientation architecture is contrast-adaptive, not universally direct or sequential.','tensor':'Walsh and Möbius transforms of invariant-tensor level sets derive all five fibre types.'},'owner_custody':custody,'summaries':summaries,'release_checks':checks,'boundary':'Exact for the fixed q=5 magnitude cube, the structured F3^10 Hjelmslev packet space, the stated stochastic readout model, and the formal algebraic interfaces. No full q=5 orbit classification, full 9^40 image, completed Q_5(zeta_5) construction, or measured hardware performance claim is made.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 558-562 release drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'owner_checks':p['owner_check_total'],'release_checks':sum(p['release_checks'].values()),'total_release_checks':len(p['release_checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
