#!/usr/bin/env python3
"""Fail-closed aggregate verifier for Passes 2300--2305.

This verifier checks every frozen mathematical certificate, the complete semantic
hash set, the manuscript hooks, the reviewed RTL/formal harness, and namespace
ownership. Runtime Icarus/Yosys metrics are deliberately excluded until a
separate toolchain certificate records a completed runner job.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERTS={
 'data/w33_pass2300_ree_tits_divisible_code.json':'dc6a1b4262e96210af832d098a4140f58e022bea979b7cdf3c030246dbf956e9',
 'data/w33_pass2301_complete_quadratic_hom_bases.json':'26eab93605eeb603e3a899c2ecda2a39e268c65e3286b86dce9449f0540b8c43',
 'data/w33_pass2302_q7_q11_extended_weil_outer_inversion.json':'d850de3ddaad56765d692fcdba838e2e05bd13340da0194f56c7996807b651a7',
 'data/w33_pass2304_known_q27_symplectic_spread_spectra.json':'559653e8cd1b32f70596a0b334cae02abc4426c694146beaac4ca96970239b72'}

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 checks={}
 for path,h in CERTS.items():
  d=json.loads((ROOT/path).read_text())
  checks[path]=d['sha256_without_hash_field']==h==digest(d) and all(d['checks'].values())
 for p in range(2300,2306):
  d=json.loads((ROOT/f'data/w33_pass_namespace_registry_v2.d/{p}.json').read_text())
  checks[f'namespace_{p}']=d['pass']==p and d['owner']=='five_frontier_execution_ree_hom_weil_rtl_nonregular'
 insert='\\input{analysis/BT2305_five_frontiers_insert}'
 checks['w33_hook']=insert in (ROOT/'w33_paper.tex').read_text()
 checks['holonet_hook']=insert in (ROOT/'photonic_holonet.tex').read_text()
 rtl=(ROOT/'rtl/w33_pass2303_packed_toolchain.sv').read_text()
 formal=(ROOT/'formal/w33_pass2303_formal.sv').read_text()
 tb=(ROOT/'tests/rtl/w33_pass2303_tb.sv').read_text()
 checks['rtl_carry_widened']="{1'b0,phase_in}+{1'b0,step12}" in rtl
 checks['formal_carry_widened']="{1'b0,u}+{1'b0,v}" in formal
 checks['kernel_constants_sized']=".step4(2'd2)" in formal and ".step6(3'd3)" in formal
 checks['reserved_expect_absent']='expect ' not in tb and 'expected_phase' in tb
 checks['formal_mixer_identity']='assert($signed(y2[i*12 +: 12])==rhs)' in formal
 checks['formal_phase_law']='assert(p2==pc)' in formal and 'assert(pk==phase0)' in formal
 assert all(checks.values()),{k:v for k,v in checks.items() if not v}
 payload={'status':'PASS_FROZEN_MATH_AND_REVIEWED_HARDWARE_HARNESS',
  'semantic_hashes':CERTS,'checks':checks,
  'boundary':'This verifier does not claim Icarus, SAT or FPGA synthesis completion. Those claims require the separate Pass-2303 hardware-run certificate.'}
 payload['aggregate_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 print(json.dumps(payload,indent=2,sort_keys=True));return payload
if __name__=='__main__':main()
