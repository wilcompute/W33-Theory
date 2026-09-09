"""Device-neutral two-qutrit compilation and bounded fresh-seed allocation.
Reuses w33_reversible_observation_experiments; no physical gate claim.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import numpy as np
from w33_reversible_observation_experiments import ternary_gates, apply_ternary, errors, measurement_readiness
from w33_carry_timing_information import trace
from w33_computation_resource_frontiers import entropy


def compile_gates(gates):
    out=[]
    def cv(control,target,power):
        out.extend([('F',None,target,1),('R9',control,target,power),('F',None,target,-1)])
    for controls,target,power in gates:
        if len(controls)==1:out.append(('X',controls[0],target,power));continue
        if len(controls)!=2:raise ValueError('one or two controls required')
        a,b=controls
        cv(a,target,power)
        for s in (1,2):
            out.append(('X',a,b[0],s))
            cv(b,target,-power)
            out.append(('X',a,b[0],-s))
            cv(b,target,power)
    return out


def simulate(psi,gates):
    psi=psi.copy();indices=np.arange(len(psi));omega=np.exp(2j*np.pi/3)
    fourier=omega**np.outer(np.arange(3),np.arange(3))/np.sqrt(3)
    for kind,control,target,power in gates:
        base=indices[indices//3**target%3==0]
        if control is not None:base=base[base//3**control[0]%3==control[1]]
        ids=base[:,None]+np.arange(3)*3**target
        if kind=='F':mat=fourier if power==1 else fourier.conj().T
        elif kind=='R9':mat=np.diag(np.exp(2j*np.pi*np.arange(3)*power/9))
        elif kind=='X':mat=np.roll(np.eye(3),power,axis=0)
        else:raise ValueError(kind)
        psi[ids]=psi[ids]@mat.T
    return psi


def compilation_audit():
    worst=0.;checked=0
    for a,b,power in product(range(3),range(3),(1,-1)):
        gates=[(((0,a),(1,b)),2,power)]
        native=compile_gates(gates)
        for i in range(27):
            psi=np.eye(27,dtype=complex)[:,i];expected=np.zeros(27);expected[apply_ternary(i,gates)]=1
            worst=max(worst,float(np.max(abs(simulate(psi,native)-expected))));checked+=1
    gates,wires=ternary_gates(3,1);native=compile_gates(gates)
    rng=np.random.default_rng(33519);psi=rng.normal(size=3**wires)+1j*rng.normal(size=3**wires);psi/=np.linalg.norm(psi)
    perm=np.array([apply_ternary(i,gates) for i in range(len(psi))]);expected=np.empty_like(psi);expected[perm]=psi
    error=float(np.max(abs(simulate(psi,native)-expected)))
    assert worst<1e-12 and error<1e-12
    assert np.max(abs(simulate(psi,native[:-1])-expected))>1e-3
    return dict(basis='F, F-dagger; equality-controlled X and R9=diag(exp(2 pi i k/9))',
        native_gates=native,gate_count=len(native),two_qutrit_gates=sum(g[1] is not None for g in native),
        qutrits=wires,gadget_basis_checks=checked,max_gadget_error=worst,arbitrary_coherent_state_error=error,
        mutation_rejections=1,boundary='Declared logical target basis; no pulse calibration or gate optimality claim')


def seed_frontier():
    rows=[]
    for mask in range(16):
        positions=[j for j in range(4) if mask>>j&1];K=4**len(positions);marginal=Counter();conditional=0
        for x in range(8):
            local=Counter()
            for seed in range(K):
                noise=dict(zip(positions,errors(seed,len(positions))))
                local[tuple(t+noise.get(j,0) for j,t in enumerate(trace(x,4)))]+=1
            marginal.update(local);conditional+=entropy(Fraction(v,K) for v in local.values())/8
        leakage=entropy(Fraction(v,8*K) for v in marginal.values())-conditional
        rows.append(dict(mask=mask,positions=positions,retained_seed_bits=2*len(positions),information_bits=leakage,
                         seed_entropy_given_final_counter_and_record_bits=len(positions)/2))
    frontier=[]
    for budget in range(0,9,2):
        eligible=[r for r in rows if r['retained_seed_bits']<=budget];best=min(r['information_bits'] for r in eligible)
        frontier.append(dict(budget_bits=budget,minimum_information_bits=best,optimal_masks=[r['mask'] for r in eligible if abs(r['information_bits']-best)<1e-12]))
    assert abs(frontier[0]['minimum_information_bits']-3)<1e-12
    return dict(policies=rows,frontier=frontier,scope='All 16 fixed subsets of four observations; uniform three-bit input; independent two-bit seeds; entropies evaluated numerically from exact counts')

if __name__=='__main__':
    result=dict(status='PASS',compilation=compilation_audit(),seed_allocation=seed_frontier(),physical=measurement_readiness())
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('compilation','seed_allocation')},indent=2))
    print(result['compilation']['gate_count'],result['seed_allocation']['frontier'])
