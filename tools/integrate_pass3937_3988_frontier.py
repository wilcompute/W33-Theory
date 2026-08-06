#!/usr/bin/env python3
"""Reconcile Passes 3937-3956 and replay the pending 3973-3988 registrations.

This metadata-only tool never modifies protected docs/index.html.
"""
from __future__ import annotations
import json
from pathlib import Path
from integrate_pass3973_3980_frontier import integrate as integrate_3973

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'data/w33_current_frontier_manifest_v1.json'
OUR_TEX='analysis/BT3937_BT3956_rho200_poset_monster_octonion_universal_photon_insert'
OUR_SECTION={'kind':'id','token':'bt3937-3956-rho200-poset-photon','source':'analysis/BT3937_BT3956_rho200_poset_monster_octonion_universal_photon_index_insert.html'}
OUR_PAGE={'token':'passes-3937-3956-rho200-local-algebra-photon-null-processor','source':'docs/rho200-local-algebra-photon-null-processor.html'}
TEX_3981='analysis/BT3981_BT3988_five_front_three_photon_closure_insert'
SECTION_3981={'kind':'id','token':'bt3981-3988-five-front-photon-closure','source':'analysis/BT3981_BT3988_five_front_three_photon_closure_index_insert.html'}
PAGE_3981={'token':'passes-3981-3988-five-front-photon-closure','source':'docs/five-front-photon-closure.html'}

def insert_before(items,value,predicate):
    if value in items:return False
    index=next((i for i,x in enumerate(items) if predicate(x)),len(items))
    items.insert(index,value);return True

def upsert_before(items,value,key,predicate):
    matches=[i for i,x in enumerate(items) if x[key]==value[key]]
    changed=False
    for i in reversed(matches):
        if items[i]!=value or len(matches)>1:
            del items[i];changed=True
    if not any(x==value for x in items):
        index=next((i for i,x in enumerate(items) if predicate(x)),len(items))
        items.insert(index,value);changed=True
    return changed

def add_unique(items,value,key=None):
    if key is None:
        if value in items:return False
    else:
        matches=[x for x in items if x[key]==value[key]]
        if matches:
            if matches!=[value]:raise ValueError((matches,value))
            return False
    items.append(value);return True

def main():
    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    changes={}
    changes['our_input']=insert_before(cfg['required_ordered_inputs'],OUR_TEX,lambda x:'BT3957_' in x)
    changes['our_section']=upsert_before(cfg['public_sections'],OUR_SECTION,'token',lambda x:x['token'].startswith('bt3957-'))
    changes['our_page']=upsert_before(cfg['standalone_public_pages'],OUR_PAGE,'token',lambda x:x['token'].startswith('passes-3957-'))
    CONFIG.write_text(json.dumps(cfg,separators=(',',':'))+'\n',encoding='utf-8')

    result_3973=integrate_3973(CONFIG)

    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    changes['input_3981']=add_unique(cfg['required_ordered_inputs'],TEX_3981)
    changes['section_3981']=add_unique(cfg['public_sections'],SECTION_3981,'token')
    changes['page_3981']=add_unique(cfg['standalone_public_pages'],PAGE_3981,'token')
    CONFIG.write_text(json.dumps(cfg,separators=(',',':'))+'\n',encoding='utf-8')

    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    required=cfg['required_ordered_inputs']
    assert required.index(OUR_TEX)<required.index('analysis/BT3957_BT3964_exact_algebra_mesh_code_photon_insert')
    assert required.index('analysis/BT3973_BT3980_combined_extremal_mesh_photon_tensor_insert')<required.index(TEX_3981)
    assert len(required)==len(set(required))
    print(json.dumps({'status':'PASS','changed':changes,'pass3973':result_3973['changed'],'protected_index_modified':False},sort_keys=True))

if __name__=='__main__':main()
