#!/usr/bin/env python3
"""Native W33 Jones ticks synthesize qutrit SWAP; anomalous 2D exchange loop.

This is an explicit supplied 2D Floquet SWAP drive (known construction),
not intrinsic W33 geometry, an anyon category or spacetime. The new connection
is certified full Sp(4,3) synthesis into native two-qutrit TLJ/Clifford ticks.
"""
from __future__ import annotations
import collections,json,itertools,math,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12055_microscopic_tick_model import PTS,PROJ,pauli,FORM,w as omega

OUT=ROOT/"data/w33_20261031_native_floquet_chiral_edge.json"
I4=np.eye(4,dtype=np.int64);I9=np.eye(9,dtype=complex)
PATH=json.loads((ROOT/"data/w33_20261031_native_tlj_metaplectic_chain.json").read_text())["concrete_Pauli_indices"]
assert len(PATH)==5

def matrices():
    # For U=I+(omega-1)(I-Pi_{v,0}), conjugation acts on
    # mod3 Pauli directions by x -> x - <x,v> v.
    g=[]
    for i in PATH:
        v=tuple(PTS[i])
        a=np.array(v,dtype=np.int64)
        f=np.array([v[2],v[3],-v[0],-v[1]],dtype=np.int64)
        g.append((I4-np.outer(a,f))%3)
    return g+[(I4+np.outer(np.array(PTS[i],dtype=np.int64),
        np.array([PTS[i][2],PTS[i][3],-PTS[i][0],-PTS[i][1]],dtype=np.int64)))%3
        for i in PATH]
def find_swap_word():
    moves=matrices()
    key=lambda M:tuple(map(int,M.ravel()))
    target=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],dtype=np.int64)
    start=key(I4)
    found={start:None};todo=collections.deque([I4])
    while todo:
        a=todo.popleft();k=key(a)
        for j,g in enumerate(moves):
            b=(g@a)%3;kb=key(b)
            if kb not in found:
                found[kb]=(k,j);todo.append(b)
    assert len(found)==51840 and key(target) in found
    word=[];q=key(target)
    while q!=start:
        prior,j=found[q];word.append(j);q=prior
    word=word[::-1]
    assert word==[0,1,0,3,7,3,6,2,5,1,9,8,7]
    test=I4.copy()
    for j in word:test=(moves[j]@test)%3
    assert np.array_equal(test,target)
    return word,len(found),target.tolist()
def synthesize():
    word,order,target=find_swap_word()
    ticks=[I9+(omega-1)*(I9-PROJ[i][0]) for i in PATH]
    def dagger(t):return t.conj().T
    gates=ticks+[dagger(t)for t in ticks]
    U=I9.copy()
    for j in word:U=gates[j]@U
    SWAP=np.zeros((9,9),dtype=complex)
    for a in range(3):
        for b in range(3):SWAP[b*3+a,a*3+b]=1
    phase=np.trace(SWAP.conj().T@U)/9
    assert abs(abs(phase)-1)<1e-12
    assert np.linalg.norm(U-phase*SWAP)<1e-11
    # The projective PSp word of length9 differs by central parity,
    # hence the FULL Sp double-cover comparison is mandatory.
    return dict(status="PASS_EXACT_NATIVE_13_TICK_SWAP",
        path_indices=PATH,
        path_Pauli_vectors=[list(PTS[i])for i in PATH],
        full_symplectic_group_order=order,
        shortest_word_with_directed_generators=word,
        number_ticks=len(word),
        gate_convention="0-4 native Clifford tick U_i; 5-9 U_(i-5)^dagger. Matrix words act right-to-left in time.",
        matrix_GF3=target,
        phase_re_im=[float(phase.real),float(phase.imag)],
        frobenius_unitary_error=float(np.linalg.norm(U-phase*SWAP)))
def drive(L,periodic=False):
    assert L>=4
    if periodic:assert L%2==0
    at={(x,y):(x,y) for x in range(L)for y in range(L)}
    widths=[]
    for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
        used=set();pairs=[]
        for x in range(L):
            for y in range(L):
                if (x+y)%2:continue
                bx,by=x+dx,y+dy
                if periodic:
                    bx%=L;by%=L
                if not 0<=bx<L or not 0<=by<L:continue
                p=(x,y);q=(bx,by)
                assert p not in used and q not in used
                used.add(p);used.add(q)
                at[p],at[q]=at[q],at[p]
                pairs.append([p,q])
        widths.append(len(pairs))
    movement={original:pos for pos,original in at.items()}
    assert len(set(movement.values()))==L*L
    if periodic:
        assert all(a==b for a,b in movement.items())
        return dict(L=L,periodic=True,per_stage_swap_pairs=widths,
            bulk_identity=True,edge_cycle_length=0)
    inside=lambda a:0<a[0]<L-1 and 0<a[1]<L-1
    assert all(movement[a]==a for a in movement if inside(a))
    moved={x for x,y in movement.items() if x!=y}
    assert len(moved)==2*L-1
    assert all(not inside(x) for x in moved)
    origin=min(moved);visited=[];p=origin
    while p not in visited:
        visited.append(p);p=movement[p]
    assert p==origin and len(visited)==len(moved)
    assert all(movement[x]==x for x in movement if x not in moved)
    return dict(L=L,periodic=False,per_stage_swap_pairs=widths,
        bulk_identity=True,edge_cycle_length=len(visited),
        stationary_boundary_rails=4*(L-1)-len(visited),
        edge_translation_orbit=[list(x)for x in visited],
        active_edge_GNVW_qutrit_index=3,
        active_edge_log_index=math.log(3))
def build():
    gate=synthesize()
    open_runs=[drive(L)for L in (4,5,6,7,8,9,12)]
    torus_runs=[drive(L,periodic=True)for L in (4,6,8,10)]
    assert all(x["edge_cycle_length"]==2*x["L"]-1 for x in open_runs)
    return {"schema":"w33.native_metaplectic_exchange_floquet.v1",
      "gate":gate,"open_square_runs":open_runs,"periodic_torus_controls":torus_runs,
      "status":"PASS_ANOMALOUS_CHIRAL_QUTRIT_EDGE_FROM_NATIVE_JONES_COMPILED_SWAP",
      "edge_index_reason":"A four-step two-dimensional exchange loop is identity in the torus bulk and on all interior open sites; its active open boundary rails translate by one site in one orientation. On a locally straight semi-infinite edge this is a 1D qutrit shift with GNVW index3, log index ln3. Inert edge rails carry index1.",
      "layer_depth_using_native_two_qutrit_ticks":4*13,
      "prior_art":"Standard four-step chiral Floquet SWAP/exchange drive, a 2D boundary anomaly. Native Clifford/Sp(4,3) 13-tick compile is concrete to this W33 projector carrier.",
      "physical_scope":"Supplied 2D square lattice, time-periodic four-step schedule and physical nearest-neighbor SWAP couplers; no W33-derived lattice, dynamical anomaly cancellation, physical chiral matter or graviton. Cannot be implemented as strictly 1D finite-depth unitary circuit."}
if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(d["status"],"word",d["gate"]["shortest_word_with_directed_generators"],
          "edge_orbit_lengths",[x["edge_cycle_length"]for x in d["open_square_runs"]])
