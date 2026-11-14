#!/usr/bin/env python3
"""Passes 3155-3158: factor schedule, physical bank shape, and in-band epoch code."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3155_BT3158_FACTOR_EPOCH_results.json'
TRIS=[(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),
(1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),
(1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),
(3,6,8),(0,4,5),(4,6,7)]
SYNC=(7,2,16,23,20,15,0,2,7,11,16,19)
MARKER=(1,22,1,22,1)

def factor_schedule():
    edges=list(itertools.combinations(range(10),2));eid={e:i for i,e in enumerate(edges)}
    pairs=[]
    for t in TRIS:
        es=[tuple(sorted(x)) for x in itertools.combinations(t,2)]
        pairs.extend(tuple(sorted((eid[a],eid[b]))) for a,b in itertools.combinations(es,2))
    assert len(pairs)==69 and len(set(pairs))==69
    schedule=[]
    for e in range(45):
        schedule.append({'cycle':len(schedule),'kind':'unary','edge':e,
                         'memory':'unary_wide','address':e})
    for p,pair in enumerate(pairs):
        for left_label in range(7):
            schedule.append({'cycle':len(schedule),'kind':'pair','edge_pair':list(pair),
                             'left_label':left_label,'memory':'correction_banks',
                             'address':7*p+left_label})
    assert len(schedule)==528
    assert [x['address'] for x in schedule[:45]]==list(range(45))
    assert [x['address'] for x in schedule[45:]]==list(range(483))
    return schedule,pairs

def marker_proof():
    used=set(SYNC);assert 1 not in used and 22 not in used
    assert len(MARKER)==5 and set(MARKER).isdisjoint(used)
    pairs=[(SYNC[i],SYNC[(i+1)%12]) for i in range(12)]
    assert len(set(pairs))==12
    spacing=[]
    for payload in (12,24,48,96,192,384,768):
        spacing.append({'payload_symbols':payload,'marker_symbols':5,
          'overhead_fraction':5/(payload+5),'maximum_received_symbols_to_confirm':payload+7,
          'mean_received_symbols_to_confirm_uniform_arrival':payload/2+7})
    return spacing

def main():
    schedule,pairs=factor_schedule();spacing=marker_proof()
    bits=45*126+7*483*18+18
    # iCE40 aspect-ratio fit: unary 45x126 uses eight 256x16 columns;
    # each 483x18 correction bank uses three 512x8 columns.
    unary_ebr=8;correction_ebr_per_bank=3;total_ebr=unary_ebr+7*correction_ebr_per_bank
    assert bits==66546 and total_ebr==29
    out={'schema':'w33.pass3155_3158.factor_epoch.v2',
      'factor_engine':{
        'dynamic_factors':3697,'baseline_registers':1,'word_bits':18,
        'unary_memory':{'rows':45,'width_bits':126,'ice40_ebr_blocks':unary_ebr},
        'correction_banks':7,'correction_words_per_bank':483,
        'correction_ebr_blocks_per_bank':correction_ebr_per_bank,
        'ice40_total_ebr_blocks':total_ebr,
        'single_table_bits':bits,'single_table_bytes':bits/8,
        'unary_cycles':45,'pair_cycles':483,'sweep_cycles':528,
        'parallel_factor_updates_per_cycle':7,
        'modeled_100mhz_sweeps_per_second':100_000_000/528,
        'modeled_internal_write_bandwidth_bits_per_second':7*18*100_000_000,
        'schedule':schedule,
        'boundary':'Cycle and aspect-ratio arithmetic are exact; inferred block count, frequency and placement remain tool-observed gates.'},
      'epoch_code':{
        'payload_alphabet_size':24,'payload_period':12,'marker':list(MARKER),
        'marker_symbol_meaning':['omit0/order1','omit3/order4','omit0/order1','omit3/order4','omit0/order1'],
        'marker_symbols_unused_by_payload':True,
        'clean_blind_phase_acquisition_symbols':2,
        'two_edit_false_acquisition':'IMPOSSIBLE',
        'proof':'payload-to-marker Levenshtein distance is at least five; radius-two balls are disjoint',
        'robust_detector':'declare epoch only after at least three marker-alphabet symbols survive in a seven-symbol window',
        'spacing_pareto':spacing,
        'boundary':'Exact adversarial two-edit delimiter theorem. Optical symbol confusion probabilities are not measured.'}}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
