"""Register networks, shortest conjugation templates, and uncalibrated noise sweeps.
Run directly; --write exports the three-front certificate. Prior: w33_reye_sector_control.
"""
from collections import deque, Counter
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
import w33_reye_sector_control as c


def shortest_proof():
    # Each edge is conjugation by one AVAILABLE pi/4 Pauli pulse.
    proof={w:None for w in sorted(c.BASE+c.EXTRA)}; dist={w:0 for w in proof}
    todo=deque(proof)
    while todo:
        b=todo.popleft()
        for a in sorted(c.BASE+c.EXTRA):
            if c.anticommutes(a,b):
                w=c.xor(a,b)
                if w not in proof:
                    proof[w]=(a,b);dist[w]=dist[b]+1;todo.append(w)
    assert len(proof)==63
    # Bellman lower bound and a decreasing-distance path certify shortestness.
    for b in proof:
        for a in c.BASE+c.EXTRA:
            if c.anticommutes(a,b):assert abs(dist[b]-dist[c.xor(a,b)])<=1
    return proof,dist


def simplify(program):
    out=[]
    for w,t in program:
        if out and out[-1][0]==w:
            t+=out.pop()[1]
        if abs(t)>1e-14:out.append((w,t))
    return out


def unitary(program):
    U=c.EYE.copy()
    for w,t in program:U=U@c.rotation(w,t)
    return U


def compiler_audit():
    proof,dist=shortest_proof();old=c.closure(c.BASE+c.EXTRA);rows=[]
    for w in sorted(proof):
        p=simplify(c.pulses(w,np.pi/7,proof));before=c.pulses(w,np.pi/7,old)
        assert len(p)==2*dist[w]+1 and len(p)<=len(before)
        assert np.max(np.abs(unitary(p)-c.rotation(w,np.pi/7)))<1e-13
        rows.append({'word':w,'old_pulses':len(before),'new_pulses':len(p),'conjugation_distance':dist[w]})
    for a in proof:
        for b in proof:
            if c.anticommutes(a,b):
                assert 2*dist[c.xor(a,b)]+1 <= 2*(2*dist[a]+1)+(2*dist[b]+1)
    return {'status':'PASS','rows':rows,'old_total':sum(r['old_pulses'] for r in rows),
            'new_total':sum(r['new_pulses'] for r in rows),'max_pulses':max(r['new_pulses'] for r in rows),
            'distance_histogram':dict(Counter(dist.values())),
            'optimality_scope':'Shortest native-conjugation template, also minimal in the recursive conjugation grammar by all-pair cost inequalities. Arbitrary pulse identities or cancellations may improve further.'}


def one_word(n,q,axis):return 'I'*q+axis+'I'*(n-q-1)
def kron_word(w):
    M=np.array([[1]],complex)
    for x in w:M=np.kron(M,c.SINGLE[x])
    return M


def network_compile(registers,control,target):
    """CNOT along a chain of 3-qubit tiles using only first-qubit ZZ ports.

    Swap endpoints to adjacent positions in a connected qubit graph, perform
    adjacent CNOT, undo swaps. Return chronological *logical* operations.
    Local tile operations lower through the prior pulse compiler. Cross-tile
    CNOT lowers to local Hadamards and a ZZ port rotation.
    """
    n=3*registers
    if not all(type(x) is int for x in (registers,control,target)) or registers<1 or not 0<=control<n or not 0<=target<n or control==target:raise ValueError('invalid register operands')
    edges={(3*r,3*r+j) for r in range(registers) for j in (1,2)}
    edges|={(3*r,3*(r+1)) for r in range(registers-1)}
    adj={i:[] for i in range(n)}
    for a,b in sorted(edges):adj[a].append(b);adj[b].append(a)
    paths={control:[control]};todo=deque([control])
    while target not in paths:
        a=todo.popleft()
        for b in adj[a]:
            if b not in paths:paths[b]=paths[a]+[b];todo.append(b)
    path=paths[target];swaps=list(zip(path[:-2],path[1:-1]));program=[]
    for a,b in swaps:program.extend([(a,b),(b,a),(a,b)])
    program.append((path[-2],path[-1]))
    for a,b in reversed(swaps):program.extend([(a,b),(b,a),(a,b)])
    return program


def cnot_permutation(n,a,b):
    return np.array([x ^ (1<<(n-1-b)) if x & (1<<(n-1-a)) else x for x in range(2**n)])


def lower_network(registers, control, target):
    """Return product-order physical Pauli pulses and an explicit global phase."""
    proof,_=shortest_proof();n=3*registers;out=[];phase=0.0
    def emit(support, theta):
        tiles={q//3 for q in support}
        if len(tiles)==1:
            tile=next(iter(tiles));word=['I']*3
            for q,axis in support.items():word[q%3]=axis
            for w,t in c.pulses(''.join(word),theta,proof):
                out.append(('I'*(3*tile)+w+'I'*(n-3*tile-3),t))
        else:
            assert len(support)==2 and all(q%3==0 and axis=='Z' for q,axis in support.items())
            word=['I']*n
            for q,axis in support.items():word[q]=axis
            out.append((''.join(word),theta))
    for a,b in reversed(network_compile(registers,control,target)):
        # H = i RY(pi/4) RZ(pi/2); CZ has phase exp(-i*pi/4).
        phase+=3*np.pi/4
        emit({b:'Y'},np.pi/4);emit({b:'Z'},np.pi/2)
        emit({a:'Z'},-np.pi/4);emit({b:'Z'},-np.pi/4)
        emit({a:'Z',b:'Z'},np.pi/4)
        emit({b:'Y'},np.pi/4);emit({b:'Z'},np.pi/2)
    return out,phase


def network_audit():
    # Exact basis permutations imply arbitrary coherent correctness (all phases 1).
    examples=[]
    for r in (1,2,3):
        n=3*r
        for a in range(n):
            for b in range(n):
                if a==b:continue
                program=network_compile(r,a,b);v=np.arange(2**n)
                for q,t in program:v=cnot_permutation(n,q,t)[v]
                assert np.array_equal(v,cnot_permutation(n,a,b))
        examples.append({'registers':r,'all_ordered_pairs':n*(n-1),'max_adjacent_cnot_count':max(len(network_compile(r,a,b)) for a in range(n) for b in range(n) if a!=b)})
    # Physical port identity CZ = exp(-i*pi/4) R_Za(-pi/4) R_Zb(-pi/4) R_ZZ(pi/4).
    Z=np.kron(c.SINGLE['Z'],c.SINGLE['I']);W=np.kron(c.SINGLE['I'],c.SINGLE['Z']);I=np.eye(4)
    R=lambda P,t:np.cos(t)*I-1j*np.sin(t)*P
    cz=np.exp(-1j*np.pi/4)*R(Z,-np.pi/4)@R(W,-np.pi/4)@R(Z@W,np.pi/4)
    assert np.max(np.abs(cz-np.diag([1,1,1,-1])))<1e-14
    H=(c.SINGLE['X']+c.SINGLE['Z'])/np.sqrt(2);H2=np.kron(c.SINGLE['I'],H)
    assert np.max(np.abs(H2@cz@H2-np.eye(4)[:,cnot_permutation(2,0,1)]))<1e-14
    # Bell pair across ports, witnessed by reduced purity 1/2.
    psi=H2@cz@H2@np.kron(H,c.SINGLE['I'])@np.array([1,0,0,0]);rho=psi.reshape(2,2)@psi.reshape(2,2).conj().T
    assert abs(np.trace(rho@rho)-.5)<1e-14
    physical,phase=lower_network(2,2,5)
    U=np.eye(64,dtype=complex)
    for w,t in physical:
        P=kron_word(w);U=U@(np.cos(t)*np.eye(64)-1j*np.sin(t)*P)
    U*=np.exp(1j*phase)
    physical_error=float(np.max(np.abs(U-np.eye(64)[:,cnot_permutation(6,2,5)])))
    assert physical_error<1e-12
    return {'status':'PASS','physical_example_pulse_count':len(physical),
            'physical_example_full_matrix_error':physical_error,'routing_checks':examples,'port':'one independently switchable Z(first) tensor Z(first) interaction per neighbouring tile pair',
            'cnot_port_rotation_angle':'pi/4','per_cnot_phase_correction':'exp(-i*pi/4)',
            'bell_reduced_purity':float(np.trace(rho@rho).real),
            'proof':'Connected tile chain plus exact local SU(8) controls yields arbitrary one-qubit gates and routed CNOTs on every finite number of tiles.',
            'boundary':'Logical scalable circuit architecture under supplied coupling and local-control assumptions; no physical scalability, fault tolerance, or unbounded storage proof.'}


def noisy_channel(program,eps,detuning,crosstalk,dephase_rate):
    # Unit Rabi angular rate; time=abs(angle). Static coherent error is shared
    # across pulses. Markov dephasing on Z2 has p=(1-exp(-2 gamma t))/2.
    K=[c.EYE.copy()]
    for w,t in reversed(program): # chronological execution of product-order list
        H=np.sign(t)*(1+eps)*c.MATS[w]+detuning*c.MATS['IZI']+crosstalk*c.MATS['IXI']
        U=expm(-1j*abs(t)*H);p=(1-np.exp(-2*dephase_rate*abs(t)))/2
        A=[np.sqrt(1-p)*U,np.sqrt(p)*c.MATS['IZI']@U]
        K=[a@k for a in A for k in K]
    return K


def noise_audit():
    rows=[]
    params=[(0,0,0,0),(.001,0,0,0),(.01,0,0,0),(.05,0,0,0),(0,.01,0,0),(0,0,.01,0),(0,0,.05,0),(0,0,0,.01),(.01,.01,.01,.01)]
    for eps,det,cross,gamma in params:
        fidelities=[];leakages=[]
        for axis,s,t in product('XYZ',(-1,1),(-1,1)):
            program=c.sector_pulses(axis,s,t,np.pi/4);ideal=unitary(program)
            K=noisy_channel(program,eps,det,cross,gamma)
            assert np.max(np.abs(sum(k.conj().T@k for k in K)-c.EYE))<1e-12
            Fe=sum(abs(np.trace(ideal.conj().T@k))**2 for k in K)/64
            Q=(c.EYE+s*c.MATS['IZI'])@(c.EYE+t*c.MATS['IIX'])/4
            L=Q@sum(k.conj().T@(c.EYE-Q)@k for k in K)@Q
            leakage=max(0,float(np.linalg.eigvalsh(L)[-1].real))
            fidelities.append(float((8*Fe+1)/9));leakages.append(leakage)
        rows.append({'amplitude_fraction':eps,'detuning_over_rabi':det,'crosstalk_over_rabi':cross,'dephasing_rate_over_rabi':gamma,'minimum_average_gate_fidelity':min(fidelities),'maximum_sector_leakage':max(leakages)})
    assert rows[0]['minimum_average_gate_fidelity']>1-1e-13
    assert rows[6]['maximum_sector_leakage']>rows[5]['maximum_sector_leakage']>0
    assert rows[7]['minimum_average_gate_fidelity']<1 and rows[7]['maximum_sector_leakage']<1e-12
    return {'status':'PASS','rows':rows,'models':'Static amplitude/detuning/crosstalk errors plus independent Markov Z2 dephasing; normalized Rabi rate one.',
            'interpretation':'Sector leakage alone misses coherence loss: dephasing can preserve sectors and damage the coherent gate.',
            'boundary':'Synthetic parameter sweep, no measured calibration, error threshold, or device performance claim.'}


if __name__=='__main__':
    import sys
    result={'schema':'w33.reye-control-extensions.v1','compiler':compiler_audit(),'network':network_audit(),'noise':noise_audit(),'status':'PASS'}
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{x:v for x,v in r.items() if x not in ('rows',)} if isinstance(r,dict) else r for k,r in result.items()},indent=2))
