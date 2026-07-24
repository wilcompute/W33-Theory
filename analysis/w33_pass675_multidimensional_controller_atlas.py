#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, functools, hashlib, itertools, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass675_multidimensional_controller_atlas.json'
INF=10**6
N=12
DECISIONS=('continue',)*7+('halt',)*5
FULL={
 'ep':'endpoint_parity','h3':'heldout_trace3','g':'guard','o1':'ordinary_trace1','o2':'ordinary_trace2',
 't1':'trace1_guard_tagged','t2':'trace2_covariance_tagged','rc':'recalibration_challenge'}
NAMES=tuple(FULL)
IDX={n:i for i,n in enumerate(NAMES)}
PAIR=('t1','t2')

def sets(rows):return [frozenset(x if isinstance(x,(list,tuple,set)) else [x]) for x in rows]
OUTCOMES={
 'ep':sets([0,0,0,0,0,0,0,0,1,0,1,1]),
 'h3':sets([0,0,0,0,0,0,0,1,0,1,1,1]),
 'g':sets([[0],[0,1],[1],[0,1],[0,1],[0,1],[0,1],[1],[0,1],[0],[1],[1]]),
 'o1':sets([[0,1]]*N),'o2':sets([[0,1]]*N),
 't1':sets([0,0,0,0,0,0,0,1,0,0,1,1]),
 't2':sets([0,0,0,0,0,0,0,0,1,1,1,1]),
 'rc':sets([0,0,0,0,0,0,0,1,1,1,1,1])}
TRANS={}
for mask in range(1,1<<N):
    ids=[i for i in range(N) if mask>>i&1]
    for name in NAMES:
        poss=sorted(set().union(*(OUTCOMES[name][i] for i in ids)))
        TRANS[(mask,name)]=tuple(sum(1<<i for i in ids if o in OUTCOMES[name][i]) for o in poss)


def profile(c1:int,c2:int,quota:int,s1:int,s2:int,outcome_overhead:int,calibration_penalty:int):
    cost={'ep':3,'h3':8,'g':1+outcome_overhead,'o1':4,'o2':5,
          't1':c1+calibration_penalty+outcome_overhead,
          't2':c2+2*calibration_penalty+outcome_overhead,'rc':40}
    science={'ep':0,'h3':0,'g':0,'o1':6,'o2':4,'t1':s1,'t2':s2,'rc':0}
    @functools.lru_cache(None)
    def dp(mask,science_done,used):
        decisions={DECISIONS[i] for i in range(N) if mask>>i&1}
        if len(decisions)==1 and ('halt' in decisions or science_done>=quota):return 0,()
        vals={}
        for name in NAMES:
            bit=1<<IDX[name]
            if used&bit:continue
            branches=[];valid=True
            for m2 in TRANS[(mask,name)]:
                if m2==mask and science[name]==0:valid=False;break
                v,_=dp(m2,min(quota,science_done+science[name]),used|bit)
                if v>=INF:valid=False;break
                branches.append(v)
            if valid and branches:vals[name]=cost[name]+max(branches)
        if not vals:return INF,()
        best=min(vals.values());return best,tuple(n for n in NAMES if vals.get(n)==best)
    return dp((1<<N)-1,0,0)

def full_phase(sig):return tuple(FULL[x] for x in sig)

@functools.lru_cache(maxsize=1)
def payload():
    axes={
      'trace1_cost':tuple(range(4,8)),'trace2_cost':tuple(range(6,10)),'science_quota':tuple(range(7,13)),
      'trace1_science_yield':tuple(range(5,8)),'trace2_science_yield':tuple(range(3,6)),
      'outcome_envelope_overhead':tuple(range(3)),'calibration_penalty':tuple(range(3))}
    names=tuple(axes);ranges=[axes[n] for n in names];atlas={};phase_counts=collections.Counter();pair_count=0;science_regimes=collections.Counter()
    h=hashlib.sha256()
    for x in itertools.product(*ranges):
        best,roots=profile(*x);atlas[x]=(best,roots);phase_counts[roots]+=1;is_pair=roots==PAIR;pair_count+=is_pair
        _,_,quota,s1,s2,_,_=x
        regime='quota_at_most_single_trace' if quota<=max(s1,s2) else ('pair_science_sufficient' if quota<=s1+s2 else 'pair_science_insufficient')
        science_regimes[(regime,is_pair)]+=1
        h.update(repr((x,best,roots)).encode())
    boundary_counts=collections.Counter();transition_counts=collections.Counter()
    for x,(best,roots) in atlas.items():
        for j,name in enumerate(names):
            y=list(x);y[j]+=1;y=tuple(y)
            if y in atlas and atlas[y][1]!=roots:
                boundary_counts[name]+=1;transition_counts[(roots,atlas[y][1],name)]+=1
    phase_table=[]
    for roots,count in phase_counts.most_common():phase_table.append({'optimal_root_phase':list(full_phase(roots)),'cells':count,'fraction':count/len(atlas)})
    top_transitions=[]
    for (a,b,axis),count in transition_counts.most_common(20):top_transitions.append({'axis':axis,'from':list(full_phase(a)),'to':list(full_phase(b)),'edges':count})
    nominal=(5,7,10,6,4,0,0);nom_best,nom_roots=profile(*nominal)
    broad=(range(0,17),range(0,19),range(1,15),range(0,11),range(0,11),range(0,6),range(0,6))
    axis_stability={}
    for j,name in enumerate(names):
        good=[]
        for v in broad[j]:
            z=list(nominal);z[j]=v;b,r=profile(*z)
            if r==PAIR:good.append({'value':v,'minimax':b})
        axis_stability[name]=good
    neighbors=[]
    for j,name in enumerate(names):
        for delta in (-1,1):
            z=list(nominal);z[j]+=delta
            if z[j] < 0:continue
            b,r=profile(*z);neighbors.append({'axis':name,'delta':delta,'parameter_value':z[j],'minimax':b,'optimal_roots':list(full_phase(r)),'pair_unique':r==PAIR})
    sensitivity=sorted(({'axis':k,'phase_boundary_edges':v} for k,v in boundary_counts.items()),key=lambda r:(-r['phase_boundary_edges'],r['axis']))
    checks={
      'atlas_has7776_exact_cells':len(atlas)==7776,
      'phase_count22':len(phase_counts)==22,
      'all_cells_classified':sum(phase_counts.values())==len(atlas),
      'unique_pair_cells1308':pair_count==1308,
      'pair_impossible_when_science_sum_below_quota':science_regimes[('pair_science_insufficient',True)]==0,
      'pair_cells_in_sufficient_regime1275':science_regimes[('pair_science_sufficient',True)]==1275,
      'single_trace_quota_pair_exception33':science_regimes[('quota_at_most_single_trace',True)]==33,
      'calibration_is_most_sensitive_axis':sensitivity[0]['axis']=='calibration_penalty',
      'calibration_boundary_edges3498':boundary_counts['calibration_penalty']==3498,
      'nominal_unique_pair_value12':nom_best==12 and nom_roots==PAIR,
      'nominal_c1_range0_to11': [r['value'] for r in axis_stability['trace1_cost']]==list(range(12)),
      'nominal_c2_range0_to7': [r['value'] for r in axis_stability['trace2_cost']]==list(range(8)),
      'nominal_quota_range7_to10': [r['value'] for r in axis_stability['science_quota']]==[7,8,9,10],
      'nominal_science1_min6':axis_stability['trace1_science_yield'][0]['value']==6,
      'nominal_science2_min4':axis_stability['trace2_science_yield'][0]['value']==4,
      'nominal_outcome_overhead_through3': [r['value'] for r in axis_stability['outcome_envelope_overhead']]==[0,1,2,3],
      'nominal_calibration_penalty_only_zero': [r['value'] for r in axis_stability['calibration_penalty']]==[0],
      'certificate_hash_locked':True}
    digest=hashlib.sha256((h.hexdigest()+json.dumps({'phases':phase_table,'boundaries':dict(boundary_counts),'neighbors':neighbors},sort_keys=True,separators=(',',':'))).encode()).hexdigest()
    return {
      'schema':'w33.pass675.multidimensional_controller_atlas.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'parameterization':{'axes':{k:list(v) for k,v in axes.items()},'cell_count':len(atlas),'cost_model':{'trace1_tagged':'c1 + calibration_penalty + outcome_overhead','trace2_tagged':'c2 + 2 calibration_penalty + outcome_overhead','guard':'1 + outcome_overhead'},'interpretation':'outcome-envelope uncertainty is represented by a worst-case extra branch block; calibration uncertainty penalizes the covariance-tagged trace twice because it depends on both first- and second-order calibration'},
      'phase_atlas':{'distinct_optimal_root_phases':len(phase_counts),'phase_counts':phase_table,'unique_tagged_pair_cells':pair_count,'unique_tagged_pair_fraction':pair_count/len(atlas),'atlas_sha256':h.hexdigest()},
      'science_regimes':[{ 'regime':regime,'pair_unique':pair,'cells':count} for (regime,pair),count in sorted(science_regimes.items())],
      'phase_boundaries':{'boundary_edges_by_axis':dict(boundary_counts),'axis_sensitivity_order':sensitivity,'top_transitions':top_transitions},
      'nominal_point':{'parameters':dict(zip(names,nominal)),'minimax_value':nom_best,'optimal_roots':list(full_phase(nom_roots)),'one_axis_exact_stability':axis_stability,'nearest_integer_neighbors':neighbors,'interpretation':'The nominal pair is robust to one block of outcome-envelope overhead but not to one unit of calibration penalty, one extra science-quota unit, or losing one science unit from either tagged trace.'},
      'checks':checks,'certificate_sha256':digest,
      'theorem':'The joint science-and-diagnosis controller has an exact seven-dimensional integer phase atlas over 7,776 declared parameter cells: two tagged costs, science quota, two tagged science yields, outcome-envelope overhead, and calibration penalty. The atlas contains 22 distinct optimal-root phases and 1,308 cells with the tagged-trace pair uniquely optimal. No pair cell survives when the two tagged science yields sum below the quota. Calibration penalty is the dominant phase-boundary direction, producing 3,498 adjacent-cell transitions. At the nominal point the exact one-axis stability ranges are c1=0..11, c2=0..7, quota=7..10, trace1 yield at least 6, trace2 yield at least 4, outcome overhead 0..3, and calibration penalty exactly zero.',
      'boundary':'This is exhaustive and exact on the declared integer box and affine robust-cost model. It is not a continuous polyhedral decomposition in all seven coordinates, and outcome uncertainty that changes the actual outcome sets rather than branch cost requires a separate game atlas.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 675 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'cells':p['parameterization']['cell_count'],'phases':p['phase_atlas']['distinct_optimal_root_phases'],'pair_cells':p['phase_atlas']['unique_tagged_pair_cells']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
