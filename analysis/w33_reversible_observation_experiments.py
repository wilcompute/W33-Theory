"""Reversible noise seeds, coherent ternary erasure, seed reuse and padding.

No physical measurements are generated. The separate measurement reader accepts
recorded work/internal-energy data; its built-in fixture is explicitly synthetic.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import product
from math import log2,isclose,sqrt
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
from w33_carry_timing_information import trace
from w33_computation_resource_frontiers import entropy,carry


def errors(seed,length,reuse=False):
    values=[]
    for j in range(length):
        z=(seed>>(0 if reuse else 2*j))&3
        values.append(2*((z&1)+(z>>1)-1))
    return tuple(values)


def observed(x,seed,length,reuse=False):
    return tuple(t+e for t,e in zip(trace(x,length),errors(seed,length,reuse)))


def channel(n,m,reuse=False):
    N,L=1<<n,1<<m
    K=4 if reuse else 4**L
    marginal=Counter()
    hs=[]
    difference=Counter()
    for x in range(N):
        local=Counter(observed(x,s,L,reuse) for s in range(K))
        hs.append(entropy(F(v,K) for v in local.values()))
        marginal.update(local)
        # Timing differences cancel a common additive seed exactly.
        if reuse:
            ds={tuple(v-z[0] for v in z) for z in local}
            assert len(ds)==1
            difference[next(iter(ds))]+=1
    ho=entropy(F(v,N*K) for v in marginal.values())
    conditional=sum(hs)/N
    return dict(input_information_bits=ho-conditional,record_entropy_bits=ho,
                conditional_record_entropy_bits=conditional,seed_register_bits=2 if reuse else 2*L,
                timing_difference_information_bits=entropy(F(v,N) for v in difference.values()) if reuse else None)


def noise_seed_witness(n=3,m=1):
    N,L=1<<n,1<<m
    K=4**L
    width=4*L
    checked=0
    for y in range(2*N):
        for s in range(K):
            # Total extension; valid Y satisfy L <= Y < N+L.
            x=(y-L)%N
            z=observed(x,s,L)
            assert all(0<=v<16 for v in z)
            code=sum(v<<(4*j) for j,v in enumerate(z))
            for r in range(1<<width):
                out=r^code
                assert out^code==r
                checked+=1
            assert code^code==0
    row=channel(n,m)
    assert isclose(row['conditional_record_entropy_bits'],1.5*L)
    # A two-bit seed maps to {-2,0,2}; the zero error has two preimages.
    seed_given_error=2-entropy((F(1,4),F(1,2),F(1,4)))
    return dict(n=n,m=m,permutation_states_checked=checked,
                seed_bits=2*L,noise_entropy_bits=1.5*L,
                seed_entropy_given_final_counter_and_record_bits=L*seed_given_error,
                record_entropy_given_final_counter_and_seed_bits=0,
                scope='Total XOR permutation retains the seed; resetting the seed is a separate operation')


def ternary_gates(n,m):
    if not 0<=m<n:raise ValueError('need 0 <= m < n')
    d=n-m
    r0=n+1;a0=r0+n
    compute=[]
    for j in range(d):
        controls=((m,0),) if j==0 else ((a0+j-1,1),(m+j,0))
        compute.append((controls,a0+j,1))
    erase=[]
    for j in range(m):
        for value in (1,2):erase.append((((j,value),),r0+j,-value))
    for j in range(d):erase.append((((a0+j,1),),r0+m+j,-1))
    uncompute=[(c,t,-a) for c,t,a in reversed(compute)]
    return compute+erase+uncompute,a0+d


def apply_ternary(index,gates):
    for controls,target,shift in gates:
        if all(index//3**wire%3==v for wire,v in controls):
            old=index//3**target%3
            index+=(((old+shift)%3)-old)*3**target
    return index


def ternary_record(x,n,m):
    k=carry(x//3**m,3)
    return x%3**m+sum(3**(m+j) for j in range(k))


def ternary_witness(n=3,m=1):
    gates,wires=ternary_gates(n,m)
    dimension=3**wires
    perm=np.array([apply_ternary(i,gates) for i in range(dimension)])
    assert len(set(perm))==dimension
    inverse=[(c,t,-a) for c,t,a in reversed(gates)]
    assert all(apply_ternary(int(perm[i]),inverse)==i for i in range(dimension))
    N,L=3**n,3**m
    # A complex coherent superposition, not a probability histogram.
    psi=np.zeros(dimension,dtype=complex)
    expected=np.zeros_like(psi)
    for x in range(N):
        y=x+L;r=ternary_record(x,n,m)
        phase=np.exp(2j*np.pi*x/N)/sqrt(N)
        psi[y+r*3**(n+1)]=phase
        expected[y]=phase
    out=np.empty_like(psi);out[perm]=psi
    error=float(np.max(abs(out-expected)))
    assert error<1e-12 and isclose(float(np.vdot(out,out).real),1,abs_tol=1e-12)
    # Gate mutation must leave some record/ancilla uncleared.
    damaged=gates[:-1]
    assert any(apply_ternary(x+L+ternary_record(x,n,m)*3**(n+1),damaged)!=x+L for x in range(N))
    return dict(n=n,m=m,qutrits=wires,dimension=dimension,gates=gates,
                coherent_state_error=error,record_trits=n,clean_ancillas=n-m,
                gate_basis='one- or two-equality-controlled qutrit shifts; explicit total basis permutations',
                boundary='Coherent state-vector simulation, not physical gates or a Clifford+T decomposition')


def reuse_witness():
    rows=[]
    for m in range(3):
        independent=channel(3,m,False)
        reused=channel(3,m,True)
        rows.append(dict(m=m,independent=independent,reused=reused))
    assert isclose(rows[0]['independent']['input_information_bits'],rows[0]['reused']['input_information_bits'])
    return rows


def padding_witness(n=4):
    N=1<<n
    counts=Counter(trace(x,1)[0] for x in range(N))
    values=sorted(counts)
    rows=[]
    for cuts in product((False,True),repeat=len(values)-1):
        groups=[];g=[]
        for i,t in enumerate(values):
            g.append(t)
            if i==len(values)-1 or cuts[i]:groups.append(g);g=[]
        mapping={t:max(g) for g in groups for t in g}
        emitted=Counter()
        delay=F(0)
        for t,c in counts.items():
            emitted[mapping[t]]+=c
            delay+=F(c,N)*(mapping[t]-t)
        info=entropy(F(c,N) for c in emitted.values())
        rows.append(dict(delay=delay,information=info,mapping=mapping))
    front=[r for r in rows if not any(s['delay']<=r['delay'] and s['information']<=r['information']+1e-12 and
            (s['delay']<r['delay'] or s['information']<r['information']-1e-12) for s in rows)]
    zero=[r for r in front if abs(r['information'])<1e-12]
    assert len(zero)==1 and zero[0]['delay']==F(49,8)
    return dict(n=n,policies_checked=len(rows),pareto=[dict(expected_added_ticks=str(r['delay']),
                information_bits=r['information'],mapping=r['mapping']) for r in sorted(front,key=lambda z:z['delay'])],
                scope='All contiguous deterministic upward-padding partitions of this single-instruction timing alphabet; not all randomized policies')


def analyze_work(samples):
    """Paired physical quantities in SI; positive heat means heat to the bath."""
    groups=defaultdict(list)
    for row in samples:
        if row['protocol'] not in ('with_side_information','without_side_information'):
            raise ValueError('unknown protocol')
        t=float(row['temperature_kelvin']);w=float(row['work_joules']);du=float(row['delta_internal_energy_joules'])
        if not np.isfinite([t,w,du]).all() or t<=0:raise ValueError('invalid physical sample')
        groups[row['protocol']].append((w-du)/(1.380649e-23*t))
    if set(groups)!={'with_side_information','without_side_information'}:raise ValueError('both controls required')
    out={}
    for label,values in groups.items():
        if len(values)<2:raise ValueError('need repeated cycles per protocol')
        out[label]=dict(cycles=len(values),mean_heat_over_kBT=float(np.mean(values)),
                        standard_error=float(np.std(values,ddof=1)/sqrt(len(values))))
    return out


def read_measurement(csv_path,metadata_path):
    meta=json.loads(Path(metadata_path).read_text())
    for key in ('device_id','calibration_reference','raw_source_reference','source_class'):
        if not meta.get(key):raise ValueError('missing measurement provenance: '+key)
    if meta['source_class']!='hardware-measured':raise ValueError('physical admission requires hardware-measured source')
    raw=Path(csv_path).read_bytes()
    with Path(csv_path).open(newline='') as f:samples=list(csv.DictReader(f))
    return dict(status='MEASURED_INPUT_ANALYZED',metadata=meta,sha256=hashlib.sha256(raw).hexdigest(),
                analysis=analyze_work(samples),boundary='Provenance is supplied by experimenter; analysis does not independently authenticate the instrument')


def measurement_readiness():
    root=Path('/sys/class/powercap')
    counters=sorted(str(p) for p in root.glob('**/energy_uj')) if root.exists() else []
    # Synthetic arithmetic control, never promoted to physical evidence.
    kbT=1.380649e-23*300
    fixture=[dict(protocol=label,temperature_kelvin=300,work_joules=v*kbT,
                  delta_internal_energy_joules=0) for label,vals in
             [('with_side_information',(0.1,0.3)),('without_side_information',(0.7,0.9))] for v in vals]
    check=analyze_work(fixture)
    assert isclose(check['with_side_information']['mean_heat_over_kBT'],0.2)
    assert isclose(check['without_side_information']['mean_heat_over_kBT'],0.8)
    from tempfile import TemporaryDirectory
    rejections=0
    with TemporaryDirectory() as directory:
        data=Path(directory)/'cycles.csv'
        data.write_text('protocol,temperature_kelvin,work_joules,delta_internal_energy_joules\n')
        meta=Path(directory)/'provenance.json'
        for record in ({},dict(device_id='fixture',calibration_reference='fixture',
                             raw_source_reference='fixture',source_class='synthetic')):
            meta.write_text(json.dumps(record))
            try:read_measurement(data,meta)
            except ValueError:rejections+=1
            else:raise AssertionError('nonphysical input admitted')
    assert rejections==2
    return dict(status='BLOCKED_NO_PHYSICAL_DATA',powercap_energy_counters=counters,
                physical_admission_negative_controls=rejections,
                analyzer_fixture_source_class='synthetic-unit-check',
                required_csv_columns=['protocol','temperature_kelvin','work_joules','delta_internal_energy_joules'],
                required_metadata=['device_id','calibration_reference','raw_source_reference','source_class'],
                boundary='No reset-work samples collected; synthetic fixture is excluded from physical results')


def verify():
    return dict(schema='w33.reversible-observation-experiments.v1',logical_status='PASS',
                reversible_seeds=noise_seed_witness(),ternary=ternary_witness(),
                seed_reuse=reuse_witness(),padding=padding_witness(),physical=measurement_readiness())

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--measurements');ap.add_argument('--metadata')
    args=ap.parse_args()
    if args.measurements:
        if not args.metadata:ap.error('--metadata is required with --measurements')
        print(json.dumps(read_measurement(args.measurements,args.metadata),indent=2))
    else:
        row=verify()
        Path(__file__).with_name('w33_reversible_observation_certificate.json').write_text(json.dumps(row,indent=2,sort_keys=True)+'\n')
        print(json.dumps(row,indent=2))
