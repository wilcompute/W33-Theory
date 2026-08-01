#!/usr/bin/env python3
"""Fail-closed verifier for Passes 1907--1911."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
FILES={
1907:'w33_pass1907_u6_exact_shard_and_resource.json',
1908:'w33_pass1908_complete_mixed_trivariate_certificate_v2.json',
1909:'w33_pass1909_complete_s6_subgroup_phase_poset_certificate.json',
1910:'w33_pass1910_gaussian_lines_sigma_phase_cuts.json',
1911:'w33_pass1911_stabilizer_weighted_primitive_holonomy.json'}
def chash(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 d={p:json.loads((DATA/f).read_text()) for p,f in FILES.items()};checks=[]
 def add(name,x):checks.append((name,bool(x)))
 for p in FILES:add(f'{p}_canonical_hash',chash(d[p])==d[p]['sha256_without_hash_field'])
 a=d[1907];add('1907_status',a['status']=='PASS_WITH_GLOBAL_U6_RUNTIME_BOUNDARY');add('1907_pilot_records',a['completed_exact_pilot_shard']['records']==2190670);add('1907_pilot_groups',a['completed_exact_pilot_shard']['syndrome_groups']==1830866);add('1907_pilot_nonlower_singletons',a['completed_exact_pilot_shard']['nonlower_singletons_within_shard']==1349896);add('1907_chart_bytes',a['external_memory_ledger']['chart_records_16byte_sort_bytes']==99687752752);add('1907_bitmap_bytes',a['external_memory_ledger']['external_partner_bitmap_bytes']==778810569);add('1907_weight12_edges',a['global_exact_inputs']['weight12_disjoint_collision_edges']==412008338280);add('1907_internal_checks',all(a['checks'].values()))
 b=d[1908];add('1908_payload_file_hash',b['full_payload']['uncompressed_file_sha256']=='c59d2621a5909476d02c220d6348d21e54654c90ca6e24ab62b15909be9a02f8');add('1908_payload_enumerator_hash',b['full_payload']['enumerator_sha256_without_hash_field']=='6806257aff50237fe5c49a7b4cfb5b8254df36dcd24c1fe949e1dbefdcd30042');add('1908_payload_sparse_count',b['full_payload']['sparse_histogram_entries']==7355);add('1908_status',b['status']=='PASS');add('1908_words',b['words']==2**45);add('1908_bins',b['nonzero_bins']==7355);add('1908_histogram_hash',b['histogram_sha256']=='88ebaaa26631c25df99336e1aba3ca38c2973e9fa2da7de9d5e036e27c67e936');add('1908_internal_checks',all(b['checks'].values()));add('1908_complement_C2xC2',b['complement_subcode']['structure']=='C2 x C2');add('1908_generator_partition',len(b['complement_subcode']['phase40']['generator_rows'])==30 and len(b['complement_subcode']['residual_pair200']['generator_rows'])==15);add('1908_sparse_count',b['full_payload']['sparse_histogram_entries']==7355);add('1908_phase_marginal_symmetric',b['marginals']['phase']==list(reversed(b['marginals']['phase'])))
 c=d[1909];add('1909_status',c['status']=='PASS');add('1909_subgroup_classes',c['subgroup_class_count']==56);add('1909_j24_count',c['counts']['j24']==26);add('1909_j90_count',c['counts']['j90']==22);add('1909_j114_count',c['counts']['j114']==12);add('1909_paired_count',c['counts']['pairedV9']==56);add('1909_so3_relation','so(3)' in c['j_reconciliation']['relation']);add('1909_not_quaternionic',c['j_reconciliation']['quaternionic'] is False);s6=c['named_classes']['S6'];add('1909_s6_obstructed',not s6['j24'] and not s6['j90'] and not s6['j114']);a6=c['named_classes']['A6'];add('1909_a6_90_phase',a6['j90'])
 e=d[1910];add('1910_status',e['status']=='PASS');add('1910_kg',e['gaussian_projective_layer']['line_graph']=='KG(6,2)=SRG(15,6,1,3)');add('1910_oriented_vectors','60 minimal vectors' in e['gaussian_projective_layer']['oriented_lift']);add('1910_internal_checks',all(e['checks'].values()));add('1910_false_bound_excluded',e['spread_K10_audit']['forbidden_inference'].startswith('The mean 5'));add('1910_13_not_proved',e['spread_K10_audit']['upper_13_proved'] is False);add('1910_fixed_cut','Phi(c)=0' in e['sound_cut_schema']['fixed_color_equality'])
 f=d[1911];add('1911_status',f['status']=='PASS');add('1911_dimensions90',sum(f['sector_dimensions'])==90);add('1911_v9_dimensions36',sum(f['v9_shared_channel']['sector_dimensions'])==36);add('1911_complement54',sum(f['hashimoto_complement']['sector_dimensions'])==54);add('1911_internal_checks',all(f['checks'].values()));add('1911_carrier_boundary','cannot distinguish A24 from A90' in f['carrier_separation_theorem'])
 failed=[n for n,x in checks if not x]
 if failed:raise AssertionError(failed)
 print(f'PASS {len(checks)}/{len(checks)}')
 return len(checks)
if __name__=='__main__':main()
