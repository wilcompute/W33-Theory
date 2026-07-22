#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,multiprocessing as mp,pickle
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass551_z9_fourier_transfer import cp_from_trits,META,BIDX,ALPHAS
from w33_pass554_z9_minimal_memory_automaton import canonical_projective,build_rows as build_base_rows

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass559_z9_radial_quadratic_automaton.json'
BASE_CACHE=ROOT/'data'/'pass554_rows_cache.pkl'
EXT_CACHE=ROOT/'data'/'pass559_extended_rows_cache.pkl'

def minimal_unlabelled_automaton(rows):
    n=len(rows);labels=[None]*n;definitions=[None]*n
    terminal=sorted(set(rows[-1].values()),key=str);mp={x:i for i,x in enumerate(terminal)}
    labels[-1]={p:mp[cp] for p,cp in rows[-1].items()};definitions[-1]=terminal
    for k in range(n-2,-1,-1):
        sig={}
        for p,cp in rows[k].items():
            child=tuple(sorted(Counter(labels[k+1][p+(a,)] for a in range(3)).items()))
            sig[p]=(cp,child)
        vals=sorted(set(sig.values()),key=str);mp={x:i for i,x in enumerate(vals)}
        labels[k]={p:mp[v] for p,v in sig.items()};definitions[k]=vals
    return labels,definitions

def automaton_summary(rows,labels):
    out=[]
    for k in range(len(rows)):
        counts=Counter(labels[k].values());bycp=defaultdict(set)
        for p,cp in rows[k].items():bycp[cp].add(labels[k][p])
        out.append({'active_packets':k,'sections':len(rows[k]),'charpolys':len(set(rows[k].values())),'minimal_markov_states':len(counts),'state_class_size_histogram':dict(sorted(Counter(counts.values()).items())),'charpoly_split_count_histogram':dict(sorted(Counter(len(v) for v in bycp.values()).items()))})
    return out

def closure(rows,labels):
    out=[]
    for k in range(len(rows)-1):
        seen={};ok=True
        for p,state in labels[k].items():
            child=tuple(sorted(Counter(labels[k+1][p+(a,)] for a in range(3)).items()))
            if state in seen and seen[state]!=child:ok=False
            seen[state]=child
        out.append(ok)
    return out

def section_trits_extended(params,k):
    constants=params[:4]
    amps=list(params[4:4+min(k,4)])+[0]*max(0,4-min(k,4))
    deep=params[8] if k>=5 else 0
    quad=params[9] if k>=6 else 0
    out=[]
    for b,u,primitive in META:
        i=BIDX[b]
        if not primitive:
            out.append(deep)
            continue
        ell=(ALPHAS[i][0]*u[0]+ALPHAS[i][1]*u[1])%3
        out.append((constants[i]+amps[i]*ell+quad*ell*ell)%3)
    return tuple(out)

def _worker(arg):
    k,p=arg
    return p,cp_from_trits(section_trits_extended(p,k))

def build_layer(k,workers=5):
    params=list(itertools.product(range(3),repeat=4+k))
    keys=sorted({canonical_projective(p) for p in params})
    if workers<=1:
        cache=dict(_worker((k,p)) for p in keys)
    else:
        with mp.Pool(processes=workers) as pool:
            cache=dict(pool.imap_unordered(_worker,((k,p) for p in keys),chunksize=16))
    return {p:cache[canonical_projective(p)] for p in params}

def sparse_rank(rows,p=1000003):
    piv={}
    for row in rows:
        r={k:v%p for k,v in row.items() if v%p}
        while r:
            j=min(r)
            if j not in piv:
                inv=pow(r[j],-1,p)
                r={k:(v*inv)%p for k,v in r.items() if (v*inv)%p}
                piv[j]=r
                break
            q=r[j];pr=piv[j]
            for k,v in pr.items():
                nv=(r.get(k,0)-q*v)%p
                if nv:r[k]=nv
                elif k in r:del r[k]
    return len(piv)

def transition_sparse(prev,cur):
    pc=sorted(set(prev.values()),key=str);cc=sorted(set(cur.values()),key=str);ci={x:i for i,x in enumerate(cc)}
    aggregate={x:Counter() for x in pc};signatures=defaultdict(set);children=defaultdict(list)
    for p,x in cur.items():children[p[:-1]].append(x)
    for par,ch in children.items():
        parent_cp=prev[par];aggregate[parent_cp].update(ch);signatures[parent_cp].add(tuple(sorted(Counter(ch).values())))
    sparse=[{ci[k]:v for k,v in aggregate[x].items()} for x in pc]
    rank=sparse_rank(sparse)
    return {'parent_states':len(pc),'child_states':len(cc),'rank':rank,'rank_certificate_prime':1000003,'full_row_rank':rank==len(pc),'nonzero_entries':sum(len(r) for r in sparse),'spectral_markov':all(len(v)==1 for v in signatures.values()),'ambiguous_parent_spectra':sum(len(v)>1 for v in signatures.values()),'row_sum_histogram':dict(sorted(Counter(sum(r.values()) for r in sparse).items()))}

def function_rank():
    funcs=[]
    for j in range(4):
        funcs.append(tuple(1 if primitive and BIDX[b]==j else 0 for b,u,primitive in META))
    for j in range(4):
        funcs.append(tuple(((ALPHAS[j][0]*u[0]+ALPHAS[j][1]*u[1])%3) if primitive and BIDX[b]==j else 0 for b,u,primitive in META))
    funcs.append(tuple(0 if primitive else 1 for b,u,primitive in META))
    funcs.append(tuple((((ALPHAS[BIDX[b]][0]*u[0]+ALPHAS[BIDX[b]][1]*u[1])%3)**2)%3 if primitive else 0 for b,u,primitive in META))
    A=[list(f) for f in funcs];rank=0
    for col in range(len(META)):
        piv=next((i for i in range(rank,len(A)) if A[i][col]%3),None)
        if piv is None:continue
        A[rank],A[piv]=A[piv],A[rank]
        iv=pow(A[rank][col]%3,-1,3);A[rank]=[(x*iv)%3 for x in A[rank]]
        for i in range(len(A)):
            if i!=rank and A[i][col]%3:
                q=A[i][col]%3;A[i]=[(x-q*y)%3 for x,y in zip(A[i],A[rank])]
        rank+=1
    return rank,funcs

def payload(rows):
    layers=[];trans=[]
    for k,r in enumerate(rows):
        c=Counter(r.values())
        layers.append({'active_packets':k,'parameters':4+k,'sections':len(r),'distinct_charpolys':len(c),'multiplicity_histogram':dict(sorted(Counter(c.values()).items()))})
        if k:trans.append(transition_sparse(rows[k-1],r))
    labels,defs=minimal_unlabelled_automaton(rows);summary=automaton_summary(rows,labels);closed=closure(rows,labels)
    rank,funcs=function_rank()
    old=pickle.loads(BASE_CACHE.read_bytes())
    old_face=all(rows[4][p]==old[4][p] for p in old[4])
    old_terminal_by_cp={cp:i for i,cp in enumerate(sorted(set(old[4].values()),key=str))}
    ext_by_old=defaultdict(set)
    for p,cp in old[4].items():ext_by_old[old_terminal_by_cp[cp]].add(labels[4][p])
    split_hist=Counter(len(v) for v in ext_by_old.values())
    deep_test=section_trits_extended((0,)*8+(1,),5)
    quad_test=section_trits_extended((0,)*9+(1,),6)
    checks={
      'layer_sizes_through_59049':[x['sections'] for x in layers]==[81,243,729,2187,6561,19683,59049],
      'ten_packet_functions_independent':rank==10,
      'enumerated_space_is_F3_power10':layers[-1]['sections']==3**rank,
      'deep_packet_activates_all_four_anchors':all(deep_test[i]==1 for i,x in enumerate(META) if not x[2]),
      'quadratic_packet_zero_one_on_primitive_lifts':set(quad_test[i] for i,x in enumerate(META) if x[2])=={0,1},
      'old_affine_family_is_exact_zero_face':old_face,
      'all_six_transfers_full_row_rank':all(x['full_row_rank'] for x in trans),
      'minimal_future_closure_all_layers':all(closed),
      'extended_terminal_states_equal_image':summary[-1]['minimal_markov_states']==layers[-1]['distinct_charpolys'],
      'old_terminal_automaton_refines_in_extended_future':sum(split_hist.values())==921 and max(split_hist)>1,
      'projective_parameter_pair_bound':summary[-1]['minimal_markov_states']<=1+(3**10-1)//2,
    }
    return {
      'schema':'w33.pass559.z9_radial_quadratic_automaton.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'family':{'definition':'The four affine fibre functions c_b+a_b ell_b(u) are augmented by one PGL-symmetric radial deep-anchor trit d and one common quadratic packet q ell_b(u)^2 on every primitive fibre.','basis_dimension':rank,'parameter_space':'F3^10','deep_anchor_packet':'d on all four nonprimitive anchor classes','quadratic_packet':'q*ell_b(u)^2 on all 36 primitive lifts'},
      'layers':layers,'transfers':trans,
      'minimal_future_automaton':{'layers':summary,'closure':closed,'definition':'Backward unlabelled Myhill-Nerode refinement over the ordered affine, radial-anchor, and quadratic packets.'},
      'embedding_of_pass554':{'zero_face_exact':old_face,'old_terminal_states':921,'extended_state_splits_per_old_terminal_histogram':dict(sorted(split_hist.items())),'conclusion':'The 6,561-section Pass-554 family embeds exactly as d=q=0. Its terminal polynomial quotient is generally refined once radial and quadratic futures are admitted, so the old 921-state endpoint is a face, not a closed subautomaton.'},
      'checks':checks,
      'boundary':'Exact for the ten-dimensional structured packet space F3^10 (59,049 sections). It enlarges the affine family by symmetry-selected radial and quadratic modes but remains a tiny, explicitly declared slice of the full 9^40 section space.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--workers',type=int,default=5);ap.add_argument('--extended-cache',type=Path,default=EXT_CACHE);a=ap.parse_args()
    if BASE_CACHE.exists():base=pickle.loads(BASE_CACHE.read_bytes())
    else:
        base=build_base_rows();BASE_CACHE.write_bytes(pickle.dumps(base,protocol=5))
    if a.extended_cache.exists():ext=pickle.loads(a.extended_cache.read_bytes())
    else:
        ext=[build_layer(5,a.workers),build_layer(6,a.workers)]
        a.extended_cache.write_bytes(pickle.dumps(ext,protocol=5))
    rows=base+ext;p=payload(rows);s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 559 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'final_image':p['layers'][-1]['distinct_charpolys'],'final_states':p['minimal_future_automaton']['layers'][-1]['minimal_markov_states']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
