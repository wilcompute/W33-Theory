"""Compile the declared R9 target ISA to qutrit Clifford+T with clean workspace.
Basis: F, X, S=diag(1,1,omega), SUM, T=diag(1,zeta,zeta^-1).
Exact modular phase identities; numerical coherent simulation checks convention.
"""
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np
import w33_native_qutrit_seed_frontier as prior
from w33_reversible_observation_experiments import ternary_gates,apply_ternary


def inverse(gates):return [(k,c,t,-p) for k,c,t,p in reversed(gates)]


def phase_parity(wires,power):
    target=wires[-1];compute=[('SUM',w,target,1) for w in wires[:-1]]
    return compute+[('T',None,target,power)]+inverse(compute)


def product_shift(a,b,target,power=1):
    # 2[(a+b+c)^3-(a+b)^3-(a+c)^3-(b+c)^3+a^3+b^3+c^3] = 3abc mod 9.
    out=[('F',None,target,1)]
    for size in (1,2,3):
        for subset in combinations((a,b,target),size):out+=phase_parity(subset,2*power*(-1 if size==2 else 1))
    return out+[('F',None,target,-1)]


def equality_shift(control,target,power=1):
    a,level=control
    out=[('X',None,a,-level),('F',None,target,1),('T',None,target,7*power)]
    for s in (1,-1):
        out += [('SUM',a,target,s),('T',None,target,-2*power),('SUM',a,target,-s)]
    return out+[('F',None,target,-1),('X',None,a,level)]


def controlled_r9(control,target,power,flag,scratch):
    # Compute f=delta(control,level), then z=f*target into clean scratch.
    compute=equality_shift(control,flag)+product_shift(flag,target,scratch)
    return compute+[('T',None,scratch,power),('S',None,scratch,power)]+inverse(compute)


def compile_target(gates,wires):
    out=[]
    for kind,control,target,power in gates:
        if kind=='F':out.append((kind,None,target,power))
        elif kind=='X':out+=equality_shift(control,target,power)
        elif kind=='R9':out+=controlled_r9(control,target,power,wires,wires+1)
        else:raise ValueError('unsupported target instruction')
    return out,wires+2


def simulate(psi,gates):
    psi=psi.copy();ii=np.arange(len(psi));digits={}
    def digit(w):
        if w not in digits:digits[w]=ii//3**w%3
        return digits[w]
    F=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
    for kind,control,target,power in gates:
        d=digit(target)
        if kind in ('T','S'):
            exponent=d**3 if kind=='T' else 3*(d==2)
            psi*=np.exp(2j*np.pi*((power*exponent)%9)/9)
        elif kind in ('X','SUM'):
            shift=power if kind=='X' else power*digit(control)
            dest=ii+(((d+shift)%3)-d)*3**target
            out=np.empty_like(psi);out[dest]=psi;psi=out
        elif kind=='F':
            base=ii[d==0];ids=base[:,None]+np.arange(3)*3**target
            mat=F if power==1 else F.conj().T
            psi[ids]=psi[ids]@mat.T
        else:raise ValueError(kind)
    return psi


def audit():
    for a,b,c in product(range(3),repeat=3):
        cubic=2*((a+b+c)**3-(a+b)**3-(a+c)**3-(b+c)**3+a**3+b**3+c**3)
        assert (cubic-3*a*b*c)%9==0
    for a,b in product(range(3),repeat=2):
        assert (7*b**3-2*(b+a)**3-2*(b-a)**3-3*(a==0)*b)%9==0
    worst=0.;checks=0
    for level,power in product(range(3),(1,-1)):
        circuit=controlled_r9((0,level),1,power,2,3)
        for i in range(9):
            psi=np.zeros(81,complex);psi[i]=1
            expected=psi.copy();expected[i]*=np.exp(2j*np.pi*power*(i//3)*(i%3==level)/9)
            worst=max(worst,float(np.max(abs(simulate(psi,circuit)-expected))));checks+=1
    gates,wires=ternary_gates(3,1);native=prior.compile_gates(gates);compiled,total=compile_target(native,wires)
    rng=np.random.default_rng(33511);original=rng.normal(size=3**wires)+1j*rng.normal(size=3**wires);original/=np.linalg.norm(original)
    psi=np.zeros(3**total,complex);psi[:len(original)]=original
    expected=np.zeros_like(psi);perm=np.array([apply_ternary(i,gates) for i in range(len(original))]);expected[perm]=original
    error=float(np.max(abs(simulate(psi,compiled)-expected)))
    assert worst<1e-11 and error<1e-11
    bad=controlled_r9((0,0),1,1,2,3);bad=[g for g in bad if g[0]!='S']
    psi=np.zeros(81,complex);psi[6]=1
    assert abs(simulate(psi,bad)[6]-np.exp(4j*np.pi/9))>0.1
    return dict(status='PASS',basis=['F','X','S','SUM','T'],gate_count=len(compiled),
        t_power_gates=sum(g[0]=='T' for g in compiled),unit_t_or_inverse_count=sum(min(g[3]%9,(-g[3])%9) for g in compiled if g[0]=='T'),
        qutrits=total,additional_clean_ancillas=2,controlled_r9_basis_checks=checks,max_r9_error=worst,
        coherent_full_eraser_error=error,mutation_rejections=1,compiled_gates=compiled,
        scope='Exact logical Clifford+T decomposition on clean-ancilla input subspace; ancillas returned clean. No measured fault tolerance, threshold, or optimal gate count claim.',
        prior='w33_native_qutrit_seed_frontier.py; controlled-qutrit synthesis prior art arXiv:2204.00552')

if __name__=='__main__':
    result=audit();Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='compiled_gates'},indent=2))
