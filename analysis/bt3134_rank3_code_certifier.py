#!/usr/bin/env python3
"""Independent fail-closed certifier for six-qubit rank-three M36 codes.

This tool does not search the candidate space. It verifies candidate stabilizer generators
from an independent producer and refuses promotion unless every algebraic, first-order and
magic condition passes.
"""
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
I2=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Z=np.array([[1,0],[0,-1]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
LOCAL={(0,0):I2,(1,0):X,(0,1):Z,(1,1):Y}

def rank_f2(rows):
    a=[list(map(int,r)) for r in rows];rank=0
    for c in range(len(a[0]) if a else 0):
        p=next((i for i in range(rank,len(a)) if a[i][c]),None)
        if p is None:continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(len(a)):
            if i!=rank and a[i][c]:a[i]=[x^y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def symp(u,v,n=6):
    return sum(u[i]*v[n+i]+u[n+i]*v[i] for i in range(n))%2

def pauli_matrix(v,n=6):
    out=np.array([[1]],dtype=complex)
    for i in range(n):out=np.kron(out,LOCAL[(v[i],v[n+i])])
    return out

def m36_problem():
    m=np.array([0,1,-1,1],dtype=complex);m/=np.linalg.norm(m)
    basis=[m]+[np.eye(4,dtype=complex)[:,i] for i in range(4)]
    q,_=np.linalg.qr(np.column_stack(basis))
    if abs(np.vdot(q[:,0],m))<.99:raise RuntimeError('QR did not preserve clean vector')
    e=[q[:,i] for i in range(1,4)]
    clean=np.kron(np.kron(m,m),m)
    singles=[]
    for j in range(3):
        singles += [np.kron(np.kron(e[j],m),m),
                    np.kron(np.kron(m,e[j]),m),
                    np.kron(np.kron(m,m),e[j])]
    return clean,singles

def pauli_expectation(psi,v,n=6):
    x=v[:n];z=v[n:]
    xmask=sum(int(x[i])<<(n-1-i) for i in range(n))
    phase=(1j)**(sum(x[i]*z[i] for i in range(n))%4)
    ans=0j
    for b,a in enumerate(psi):
        parity=0
        for i in range(n):parity^=(z[i]&((b>>(n-1-i))&1))
        ans+=np.conj(psi[b^xmask])*phase*((-1)**parity)*a
    return ans

def certify(c):
    gens=[tuple(map(int,g['vector'])) for g in c['generators']]
    signs=[int(g.get('sign',1)) for g in c['generators']]
    reasons=[]
    if len(gens)!=3:reasons.append('need exactly three generators')
    if any(len(g)!=12 or any(x not in (0,1) for x in g) for g in gens):
        reasons.append('generators must be 12-bit binary symplectic vectors')
    if any(s not in (-1,1) for s in signs):reasons.append('signs must be +/-1')
    if reasons:return {'name':c.get('name','unnamed'),'accepted':False,'reasons':reasons}
    rk=rank_f2(gens)
    commute=all(symp(gens[i],gens[j])==0 for i in range(3) for j in range(i))
    if rk!=3:reasons.append(f'binary rank {rk}, need 3')
    if not commute:reasons.append('generators do not commute')
    P=np.eye(64,dtype=complex)
    for g,s in zip(gens,signs):P=P@(np.eye(64)+s*pauli_matrix(g))/2
    herm=float(np.max(np.abs(P-P.conj().T)))
    idem=float(np.max(np.abs(P@P-P)))
    trace=float(np.trace(P).real)
    clean,singles=m36_problem()
    killed=[float(np.linalg.norm(P@v)) for v in singles]
    success=float(np.vdot(clean,P@clean).real)
    if herm>1e-9:reasons.append('projector is not Hermitian')
    if idem>1e-9:reasons.append('projector is not idempotent')
    if abs(trace-8)>1e-8:reasons.append(f'projector rank/trace {trace}, need 8')
    if max(killed)>1e-8:reasons.append('range is not contained in single-error complement')
    if success<=1e-12:reasons.append('clean branch has zero success')
    stabilizer=None;unit_paulis=None
    if not reasons:
        psi=P@clean/math.sqrt(success);unit_paulis=0
        for v in itertools.product((0,1),repeat=12):
            if abs(abs(pauli_expectation(psi,v))-1)<1e-8:unit_paulis+=1
        stabilizer=(unit_paulis==64)
        if stabilizer:reasons.append('accepted clean output is a stabilizer state')
    return {'name':c.get('name','unnamed'),'accepted':not reasons,'reasons':reasons,
            'generator_rank':rk,'commuting':commute,'projector_trace':trace,
            'hermitian_error':herm,'idempotence_error':idem,
            'max_single_error_projection_norm':max(killed),
            'clean_success_probability':success,
            'unit_magnitude_pauli_expectations':unit_paulis,
            'accepted_clean_output_is_stabilizer':stabilizer}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--candidates',default='data/PART_BT3134_rank3_candidate_fixture.json')
    ap.add_argument('--output',default='data/PART_BT3134_RANK3_CODE_CERTIFIER_results.json')
    a=ap.parse_args();source=ROOT/a.candidates
    payload=json.loads(source.read_text())
    results=[certify(c) for c in payload.get('candidates',[])]
    if payload.get('expected')=='all_rejected' and any(r['accepted'] for r in results):
        raise SystemExit('negative control unexpectedly accepted')
    out={'schema':'w33.pass3134.rank3_code_certifier.v1',
         'source':str(source.relative_to(ROOT)),'candidate_count':len(results),
         'accepted_count':sum(r['accepted'] for r in results),'results':results,
         'boundary':'candidate certifier only; absence of accepted candidates is not a no-go theorem'}
    target=ROOT/a.output;target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
