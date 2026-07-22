#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,pickle
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass551_z9_fourier_transfer import cp_from_trits,section_trits,transition

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass554_z9_minimal_memory_automaton.json'
SELECTED_FORMS={1:(0,0,1,1,0),2:(0,0,1,0,0,0),3:(0,0,0,1,0,0,0)}

def neg3(p):return tuple((-x)%3 for x in p)
def canonical_projective(p):return min(p,neg3(p))

def build_rows():
    rows=[]
    for k in range(5):
        cache={};r={}
        for p in itertools.product(range(3),repeat=4+k):
            key=canonical_projective(p)
            if key not in cache:cache[key]=cp_from_trits(section_trits(key,k))
            r[p]=cache[key]
        rows.append(r)
    return rows

def profile(rows,k,p):
    ch=[rows[k+1][p+(a,)] for a in range(3)]
    return tuple(sorted(Counter(ch).values()))

def projective_forms(n):
    for a in itertools.product(range(3),repeat=n):
        if not any(a):continue
        j=next(i for i,x in enumerate(a) if x)
        if a[j]==1:yield a

def eval_form(a,p):return sum(x*y for x,y in zip(a,p))%3

def one_trit_forms(rows,k):
    P=list(rows[k]);cps={x:i for i,x in enumerate(sorted(set(rows[k].values()),key=str))};profs={x:i for i,x in enumerate(sorted({profile(rows,k,p) for p in P},key=str))}
    C=[cps[rows[k][p]] for p in P];R=[profs[profile(rows,k,p)] for p in P];hits=[]
    for a in projective_forms(4+k):
        seen={};ok=True
        for p,c,r in zip(P,C,R):
            key=(c,eval_form(a,p))
            if key in seen and seen[key]!=r:ok=False;break
            seen[key]=r
        if ok:hits.append(a)
    return hits

def minimal_unlabelled_automaton(rows):
    labels=[None]*5;definitions=[None]*5
    terminal=sorted(set(rows[4].values()),key=str);mp={x:i for i,x in enumerate(terminal)}
    labels[4]={p:mp[cp] for p,cp in rows[4].items()};definitions[4]=terminal
    for k in range(3,-1,-1):
        sig={}
        for p,cp in rows[k].items():
            child=tuple(sorted(Counter(labels[k+1][p+(a,)] for a in range(3)).items()))
            sig[p]=(cp,child)
        values=sorted(set(sig.values()),key=str);mp={x:i for i,x in enumerate(values)}
        labels[k]={p:mp[s] for p,s in sig.items()};definitions[k]=values
    return labels,definitions

def automaton_summary(rows,labels):
    out=[]
    for k in range(5):
        counts=Counter(labels[k].values());bycp=defaultdict(set)
        for p,cp in rows[k].items():bycp[cp].add(labels[k][p])
        out.append({'active_packets':k,'sections':len(rows[k]),'charpolys':len(set(rows[k].values())),'minimal_markov_states':len(counts),'state_class_size_histogram':dict(sorted(Counter(counts.values()).items())),'charpoly_split_count_histogram':dict(sorted(Counter(len(v) for v in bycp.values()).items()))})
    return out

def closure(rows,labels):
    result=[]
    for k in range(4):
        seen={};ok=True
        for p,s in labels[k].items():
            ch=tuple(sorted(Counter(labels[k+1][p+(a,)] for a in range(3)).items()))
            if s in seen and seen[s]!=ch:ok=False
            seen[s]=ch
        result.append(ok)
    return result

def payload(rows):
    layers=[];trans=[]
    for k,r in enumerate(rows):
        c=Counter(r.values());layers.append({'active_packets':k,'sections':len(r),'distinct_charpolys':len(c),'multiplicity_histogram':dict(sorted(Counter(c.values()).items()))})
        if k:trans.append(transition(rows[k-1],r))
    local=[]
    for k in (1,2,3):
        hits=one_trit_forms(rows,k);sel=SELECTED_FORMS[k]
        local.append({'parent_layer':k,'new_packet':k+1,'ambiguous_parent_spectra_without_memory':trans[k]['ambiguous_parent_spectra'],'minimal_memory_alphabet':3,'selected_linear_form':sel,'selected_expression':{1:'c2+c3',2:'c2',3:'c3'}[k],'working_projective_linear_forms':len(hits),'selected_form_works':sel in hits})
    labels,defs=minimal_unlabelled_automaton(rows);summary=automaton_summary(rows,labels);closed=closure(rows,labels)
    checks={
      'layer_sizes_through_6561':[x['sections'] for x in layers]==[81,243,729,2187,6561],
      'image_growth_13_26_96_336_921':[x['distinct_charpolys'] for x in layers]==[13,26,96,336,921],
      'all_four_aggregate_transfers_full_row_rank':all(x['full_row_rank'] for x in trans),
      'exactly_three_coarse_ambiguities_each_later_transfer':[x['ambiguous_parent_spectra'] for x in trans]==[0,3,3,3],
      'one_trit_is_locally_sufficient':all(x['selected_form_works'] for x in local),
      'one_trit_is_locally_minimal':all(x['ambiguous_parent_spectra_without_memory']>0 and x['minimal_memory_alphabet']==3 for x in local),
      'working_form_counts_3_9_27':[x['working_projective_linear_forms'] for x in local]==[3,9,27],
      'minimal_state_counts_41_122_365_1081_921':[x['minimal_markov_states'] for x in summary]==[41,122,365,1081,921],
      'markov_closure_all_layers':all(closed),
      'projective_pair_structure_first_three':all(summary[k]['state_class_size_histogram']==({1:1,2:(3**(4+k)-1)//2}) for k in range(3)),
      'fourth_prefix_has_thirteen_quartets':summary[3]['state_class_size_histogram']=={1:1,2:1067,4:13},
      'final_fibre_multiplicities_exact':layers[4]['multiplicity_histogram']=={1:1,2:3,4:3,6:751,8:1,12:155,24:7},
    }
    return {
      'schema':'w33.pass554.z9_minimal_memory_automaton.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'layers':layers,'aggregate_transfers':trans,'local_one_trit_repairs':local,
      'minimal_future_automaton':{'definition':'Backward Myhill-Nerode refinement for the unlabelled three-amplitude packet transfer: terminal states are exact characteristic polynomials; a prefix state is (current polynomial, multiset of child states).','layers':summary,'closure':closed,'minimality':'Any output-preserving weighted Markov quotient must separate two prefixes with different child-state multisets, so the backward refinement is the coarsest possible future-complete quotient.'},
      'conclusion':'One trit repairs each local multiplicity-profile ambiguity, but complete future Markov closure retains a projective Fourier-history state. The fourth packet produces 921 exact characteristic polynomials from 6,561 sections.',
      'checks':checks,
      'boundary':'The automaton is minimal for the ordered four-packet affine family with the three amplitude values treated as an unlabelled transfer multiset. It does not classify the full 9^40 section space.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--cached-rows',type=Path);a=ap.parse_args()
    rows=pickle.loads(a.cached_rows.read_bytes()) if a.cached_rows else build_rows();p=payload(rows);s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 554 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'final_image':p['layers'][-1]['distinct_charpolys']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
