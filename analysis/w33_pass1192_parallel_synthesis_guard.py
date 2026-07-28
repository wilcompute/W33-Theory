#!/usr/bin/env python3
"""Pass 1192: fail-closed guard for active parallel synthesis surfaces."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1192_parallel_synthesis_guard.json'
ACTIVE=[
 'analysis/w33_pass1158_kernel_residual_1952.py','analysis/w33_pass1160_we6_character_bridge.py',
 'analysis/w33_pass1161_propagator_determinant_product.py','analysis/w33_pass1162_corpus_full_sync.py',
 'PASS1158_1162_BREAKTHROUGH_RELEASE.md','analysis/w33_pass1163_sp43_stabilizer_precompute.py',
 'analysis/w33_pass1164_1920_module_identification.py','analysis/w33_pass1166_ihara_zeta_degree10.py',
 'analysis/w33_pass1167_40pt_carrier_decomposition.py','PASS1163_1167_EXECUTION_RELEASE.md',
 'analysis/w33_pass1168_sym3_decomposition.py','analysis/w33_pass1169_sp43_432_orbit_source.py',
 'analysis/w33_pass1170_meataxe_kernel_plan.py','analysis/w33_pass1171_needs_tag_fix.py',
 'analysis/w33_pass1172_ihara_zeta_degree20.py','PASS1168_1172_EXECUTION_RELEASE.md',
 'analysis/w33_pass1173_clebsch_gordan_sym3.py','analysis/w33_pass1174_d5_adjoint_image.py',
 'analysis/w33_pass1175_meataxe_gf7_simulation.py','analysis/w33_pass1176_manuscript_amendment.py',
 'analysis/w33_pass1177_ihara_zeta_degree30.py','PASS1173_1177_EXECUTION_RELEASE.md',
 'analysis/w33_pass1178_sym3_v24_plethysm_search.py','analysis/w33_pass1179_d5_image_split_checker.py',
 'analysis/w33_pass1180_meataxe_kernel_manifest.py','analysis/w33_pass1181_manuscript_inline_patch_plan.py',
 'analysis/w33_pass1182_ihara_degree40_scaffold.py','PASS1178_1182_EXECUTION_RELEASE.md',
 'analysis/w33_pass1183_sym3_v24_fingerprint_table.py','analysis/w33_pass1184_d5_image_verdict_memo.py',
 'analysis/w33_pass1185_meataxe_handoff_bundle.py','analysis/w33_pass1186_manuscript_patch_queue.py',
 'analysis/w33_pass1187_ihara_degree40_worklist.py','PASS1183_1187_EXECUTION_RELEASE.md',
]
BAD={
 'we6_order_25920':re.compile(r'\|W\(E6\)\|\s*=\s*25920|W\(E6\).{0,40}order\s*[:=]\s*25920',re.I|re.S),
 'ihara_degree_not_minus_one':re.compile(r'(?:Ihara|det\(I-uB\)).{0,300}\+\s*12u\^2',re.I|re.S),
 'bad_character_tail':re.compile(r'120.{0,30}160.{0,30}216.{0,30}240.{0,30}270.{0,30}360',re.S),
 'false_we6_sp_quotient':re.compile(r'2-to-1 map\s+W\(E6\).{0,60}Sp\(4,3\)|W\(E6\).{0,80}central (?:cover|extension).{0,40}Sp\(4,3\)',re.I|re.S),
 'impossible_s5_central_quotient':re.compile(r'S5\s*/\s*(?:\{[^}]*[+-][^}]*\}|Z/?2)',re.I),
 'd5_adjoint_promoted':re.compile(r"['\"]d5_adjoint_identified['\"]\s*:\s*True|image\s+(?:is|=)\s+(?:the\s+)?D5 adjoint",re.I),
 'fake_tensor_irreducibility':re.compile(r'V_?24\s*(?:x|tensor|\*)\s*V_?15\s*=\s*V_?360|v24_x_v15_is_V360',re.I),
 'fake_meataxe_execution':re.compile(r"['\"]simulation_performed['\"]\s*:\s*True|exact decomposition pending MeatAxe",re.I),
 'maschke_absolute':re.compile(r'all W\(E6\) irreps are absolutely irreducible over GF\(7\).{0,80}(?:by|because of|from) Maschke',re.I|re.S),
 'wrong_isotropic_count':re.compile(r'isotropic_points_sp43\s*=\s*16|#\s*isotropic points:\s*16',re.I),
}
def main():
    records=[]
    for rel in ACTIVE:
        path=ROOT/rel
        if not path.exists():records.append({'path':rel,'matches':['MISSING_ACTIVE_SURFACE']});continue
        text=path.read_text(encoding='utf-8',errors='replace')
        records.append({'path':rel,'matches':[name for name,pat in BAD.items() if pat.search(text)]})
    violations=[r for r in records if r['matches']]
    result={'schema':'w33.pass1192.parallel_synthesis_guard.v1','status':'PASS' if not violations else 'FAIL',
      'active_surfaces':records,'violations':violations,
      'canonical_facts':{'PSp(4,3)_order':25920,'Sp(4,3)_order':51840,'W(E6)_order':51840,
       'extension_types':'central cover versus outer split extension','Ihara_quadratic_coefficient':11,
       'kernel_residual':'exact Pass-1135 decomposition; dimension 1952; commutant 1109',
       'cubic_image':'1+20+24','point_module':'rank-three 1+24+15'}}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+'\n')
    if violations:raise RuntimeError(json.dumps(violations,indent=2))
    print('PASS 1192 active parallel synthesis surfaces clean');return result
if __name__=='__main__':main()
