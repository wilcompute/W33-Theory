#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
LINE='\\input{analysis/BT4105_BT4112_carrier_reference_netlist_decoder_turing_bonkers_insert}%'
text=MANIFEST.read_text()
assert text.count(LINE)==1, f'expected exactly one frontier entry, found {text.count(LINE)}'
assert text.index('BT4097_BT4104_manybody_gauge_horizon_rg_engine_insert') < text.index('BT4105_BT4112_carrier_reference_netlist_decoder_turing_bonkers_insert')
for rel in [
 'analysis/BT4105_BT4112_carrier_reference_netlist_decoder_turing_bonkers_insert.tex',
 'data/PART_4105_4112_CARRIER_REFERENCE_NETLIST_DECODER_TURING_BONKERS.json',
 'data/w33_pass_namespace_registry_v2.d/4105-4112.json']:
    assert (ROOT/rel).is_file(), rel
print('PASS_FRONTIER_4105_4112')
