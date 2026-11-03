"""Exact real structures and two distinct circuit realizations of the bridge.

Clifford real-algebra classification and local equivalence to CNOT are prior
mathematics. This checks actual repo gamma/unitary matrices, and distinguishes
the two-qubit spinor gate from a four-qubit16-state basis permutation.
"""
import collections
import heapq
import itertools
import json
import pathlib
import sys

import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_toroidal_knight_clifford_bridge import matrices,adjoint_action,compose,IDENTITY


def antiunitaries(gens):
    rows=[]
    for g in gens:
        for r,c in itertools.product(range(4),repeat=2):
            row=[0]*16
            for k in range(4):row[r*4+k]+=s.conjugate(g[k,c]);row[k*4+c]-=g[r,k]
            rows.append(row)
    null=s.Matrix(rows).nullspace()
    if not null:return [],None
    assert len(null)==1
    B=s.Matrix(4,4,null[0]);norm=(B.conjugate().T*B)[0,0];B=s.simplify(B/s.sqrt(norm))
    square=B*B.conjugate();sign=1 if square==s.eye(4) else -1
    assert square==sign*s.eye(4)
    return [[str(x) for x in row] for row in B.tolist()],sign


def minimum_spinor_circuit(blades,target):
    I=s.eye(2);Hn=s.Matrix([[1,1],[1,-1]]);S=s.diag(1,s.I)
    cnot=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    cnrev=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
    specs=[('H0',s.kronecker_product(Hn,I),2,0),('H1',s.kronecker_product(I,Hn),2,0),
           ('S0',s.kronecker_product(S,I),1,0),('S1',s.kronecker_product(I,S),1,0),
           ('CX01',cnot,1,1),('CX10',cnrev,1,1)]
    actions=[adjoint_action(n,d,blades) for _,n,d,_ in specs]
    dist={IDENTITY:(0,0)};words={IDENTITY:[]};queue=[(0,0,IDENTITY)]
    while queue:
        ent,length,a=heapq.heappop(queue)
        if dist[a]!=(ent,length):continue
        if a==target:break
        for j,g in enumerate(actions):
            b=compose(g,a);cost=(ent+specs[j][3],length+1)
            if b not in dist or cost<dist[b]:
                dist[b]=cost;words[b]=words[a]+[j];heapq.heappush(queue,(*cost,b))
    assert dist[target][0]==1
    U=s.eye(4)
    for j in words[target]:U=specs[j][1]*U/s.sqrt(specs[j][2])
    N=s.eye(4)+s.I*blades[15]
    phase=s.simplify(N.conjugate().T*U/s.sqrt(2))
    assert phase==phase[0,0]*s.eye(4)
    return dict(word_in_application_order=[specs[j][0] for j in words[target]],CNOT_count=dist[target][0],
                total_gate_count=dist[target][1],phase_relative_to_native_U=str(phase[0,0]),
                optimality='0-1 weighted Clifford action search with lexicographic(CNOT count,total gates). The target is entangling, so local-only cost0 is impossible; the exhibited cost1 word attains the bound.')


def minimum_register_circuit():
    start=(1,2,4,8);target=tuple(15^(1<<i) for i in range(4))
    parent={start:None};todo=collections.deque([start]);ops=list(itertools.permutations(range(4),2))
    while todo:
        a=todo.popleft()
        if a==target:break
        for c,t in ops:
            b=list(a);b[t]^=b[c];b=tuple(b)
            if b not in parent:parent[b]=(a,(c,t));todo.append(b)
    path=[];x=target
    while parent[x] is not None:
        x,op=parent[x];path.append(op)
    path.reverse();assert len(parent)<=20160
    for mask in range(16):
        y=mask
        for c,t in path:
            if y>>c&1:y^=1<<t
        assert y==mask^(15 if mask.bit_count()%2 else 0)
    return dict(CNOT_word_in_application_order=path,minimum_CNOT_count=len(path),searched_GL4_states=len(parent),
                boundary='This circuit permutes computational basis states of four physical qubits. It is not the four-state spinor U, whose16 vertices label operators.')


def build():
    axes,blades,old,omega=matrices();N=s.eye(4)+s.I*blades[15]
    signatures=[]
    for p in range(5):
        gamma=[g if j<p else s.I*g for j,g in enumerate(axes[:4])]
        B,sign=antiunitaries(gamma)
        assert sign==(1 if p in [2,3] else -1)
        signatures.append(dict(p=p,q=4-p,J_square=sign,antiunitary_linear_part=B,
            minimum_real_module_dimension=4 if sign==1 else 8,
            real_algebra='Mat4(R)' if sign==1 else 'Mat2(H)'))
    old_B,old_sign=antiunitaries(old);new_B,new_sign=antiunitaries(old+[N])
    assert old_sign==-1 and new_B==[] and new_sign is None
    Y=s.Matrix([[0,-s.I],[s.I,0]])
    assert blades[15]==-s.kronecker_product(Y,Y)
    circuit=minimum_spinor_circuit(blades,adjoint_action(N,2,blades))
    register=minimum_register_circuit()
    # Realification is a supplied repair, not an unchanged Majorana4 module.
    swap=s.BlockMatrix([[s.zeros(4),s.eye(4)],[s.eye(4),s.zeros(4)]]).as_explicit()
    for U in old+[N/s.sqrt(2)]:
        V=s.diag(U,U.conjugate())
        assert swap*V.conjugate()==V*swap
    return dict(status='PASS_REAL_CLIFFORD_AND_EXACT_GATE_SYNTHESIS',signature_table=signatures,
        old_spinor_antiunitary_square=-1,enlarged_spinor_antiunitary_solution_dimension=0,
        old_antiunitary_linear_part=old_B,doubled_realification_complex_dimension=8,
        native_pseudoscalar='-Y tensor Y',native_unitary='exp(-i*pi*(Y tensor Y)/4)',
        spinor_circuit=circuit,four_qubit_register_circuit=register,
        boundary='Signature classification does not select a physical Lorentz signature. Cl(3,1) permits a real4-dimensional module, while Cl(1,3) is quaternionic in this convention; the full enlarged spinor gate group has no invariant antiunitary on C4. Circuit synthesis is ideal and all-to-all; no calibrated device, timing or noise performance is claimed.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_real_clifford_gate_synthesis.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['spinor_circuit'],d['four_qubit_register_circuit'],flush=True)
