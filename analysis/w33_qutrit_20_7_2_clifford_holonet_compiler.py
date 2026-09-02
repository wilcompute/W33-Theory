#!/usr/bin/env python3
"""Compile the sparse [[20,7,2]]_3 symplectic embedding into an explicit
qutrit linear-Clifford encoder and a Holonet packet-level schedule.

For the sparse A,B witness with A B^T=I_20, choose 220 rows C spanning ker(B).
Then F=[A;C] lies in GL(240,3), satisfies F B^T=[I_20;0], and therefore the
first 20 rows of F^{-T} are exactly B.  The reversible qutrit basis map

    U_F |x> = |x F>

thus sends the first 20 input Pauli-X/Z generators to A/B.  We synthesize F by
GF(3) column Gauss-Jordan into SWAP, SCALE2, and SUM_ALPHA Clifford gates.

The Holonet lowering packs non-conflicting Clifford macros into the existing
16-slot, 72-tick packet body. Each occupied slot is represented by the verified
controller word LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX. This is packet-level
microcode/refinement evidence, not calibrated optical pulse timing.
"""
from __future__ import annotations
import hashlib, json
import numpy as np

import w33_qutrit_20_7_2_symplectic_embedding as base
import w33_qutrit_20_7_2_sparse_symplectic as sparse


def sparse_witness():
    hx,hz,h,targets,A0=sparse.build_base()
    A,_=sparse.rank_preserving_descent(A0,h)
    B,_=sparse.right_inverse(A)
    return hx,hz,h,targets,A,B


def build_full_linear(A,B):
    kerB=base.nullspace(B)
    if len(kerB)!=220: raise RuntimeError('expected dim ker(B)=220')
    F=np.vstack([A,kerB])%3
    if base.rank(F)!=240: raise RuntimeError('A plus ker(B) did not form a basis')
    Finv=base.inv(F)
    if not np.array_equal(F[:20],A): raise RuntimeError('A prefix lost')
    if not np.array_equal(Finv.T[:20]%3,B%3): raise RuntimeError('dual Z prefix is not B')
    return F


def reduce_columns_to_identity(F):
    M=np.array(F,dtype=np.int64)%3; n=M.shape[0]; ops=[]
    for r in range(n):
        c=next((j for j in range(r,n) if M[r,j]%3),None)
        if c is None: raise RuntimeError(f'no column pivot for row {r}')
        if c!=r:
            M[:,[r,c]]=M[:,[c,r]]; ops.append({'gate':'SWAP','a':r,'b':c})
        if M[r,r]==2:
            M[:,r]=(2*M[:,r])%3; ops.append({'gate':'SCALE2','wire':r})
        for j in range(n):
            if j==r or M[r,j]==0: continue
            alpha=(-int(M[r,j]))%3
            M[:,j]=(M[:,j]+alpha*M[:,r])%3
            ops.append({'gate':'SUM_ALPHA','control':r,'target':j,'alpha':alpha})
    if not np.array_equal(M,np.eye(n,dtype=np.int64)): raise RuntimeError('column elimination did not reach identity')
    # F E1...Ek=I, hence build F by inverse operations in reverse order.
    build=[]
    for op in reversed(ops):
        if op['gate']=='SUM_ALPHA': build.append({**op,'alpha':(-op['alpha'])%3})
        else: build.append(dict(op))
    return build,ops


def apply_right_ops(n,ops):
    M=np.eye(n,dtype=np.int64)
    for op in ops:
        if op['gate']=='SWAP': M[:,[op['a'],op['b']]]=M[:,[op['b'],op['a']]]
        elif op['gate']=='SCALE2': M[:,op['wire']]=(2*M[:,op['wire']])%3
        else: M[:,op['target']]=(M[:,op['target']]+op['alpha']*M[:,op['control']])%3
    return M%3


def wires(op):
    if op['gate']=='SWAP': return {op['a'],op['b']}
    if op['gate']=='SCALE2': return {op['wire']}
    return {op['control'],op['target']}


def pack_microframes(gates):
    frames=[]
    for gi,g in enumerate(gates):
        placed=False
        gw=wires(g)
        for f in frames:
            if len(f['slots'])<16 and not (gw & f['used']):
                f['slots'].append((gi,g)); f['used']|=gw; placed=True; break
        if not placed: frames.append({'slots':[(gi,g)],'used':set(gw)})
    out=[]
    for fi,f in enumerate(frames):
        slots=[]
        for slot,(gi,g) in enumerate(f['slots']):
            slots.append({'slot':slot,'gate_index':gi,'gate':g,'ticks':[
                {'tick':fi*72+3*slot,'op':'LOAD_FLAG','wires':sorted(wires(g))},
                {'tick':fi*72+3*slot+1,'op':'FLIP_Q6_AXIS','clifford_macro':g['gate']},
                {'tick':fi*72+3*slot+2,'op':'LATCH_VERTEX','wires':sorted(wires(g))},
            ]})
        out.append({'microframe':fi,'start_tick':fi*72,'body_ticks':[fi*72,fi*72+47],'epilogue_ticks':[fi*72+48,fi*72+71],'slots':slots})
    return out


def digest_matrix(a): return 'sha256:'+hashlib.sha256(bytes(int(x) for x in a.flatten())).hexdigest()


def verify():
    hx,hz,h,targets,A,B=sparse_witness()
    F=build_full_linear(A,B)
    gates,_=reduce_columns_to_identity(F)
    replay=apply_right_ops(240,gates)
    frames=pack_microframes(gates)
    counts={k:sum(g['gate']==k for g in gates) for k in ('SUM_ALPHA','SCALE2','SWAP')}
    checks={
      'full_linear_map_rank_240':base.rank(F)==240,
      'data_X_prefix_is_A':np.array_equal(F[:20],A),
      'data_Z_prefix_is_B':np.array_equal(base.inv(F).T[:20]%3,B),
      'circuit_replays_exact_F':np.array_equal(replay,F),
      'symplectic_data_embedding':np.array_equal((A@B.T)%3,np.eye(20,dtype=np.int64)),
      'packet_slots_at_most_16':all(len(f['slots'])<=16 for f in frames),
      'packet_slots_wire_disjoint':all(len(set(w for s in f['slots'] for w in wires(s['gate'])))==sum(len(wires(s['gate'])) for s in f['slots']) for f in frames),
      'three_phase_word_exact':all([t['op'] for s in f['slots'] for t in s['ticks']]==['LOAD_FLAG','FLIP_Q6_AXIS','LATCH_VERTEX']*len(f['slots']) for f in frames),
    }
    return {
      'schema':'w33.qutrit-20-7-2-clifford-holonet-compiler.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'checks':checks,
      'linear_encoder':{'F_sha256':digest_matrix(F),'A_sha256':digest_matrix(A),'B_sha256':digest_matrix(B),'gate_count':len(gates),'gate_counts':counts},
      'packet_schedule':{'microframes':len(frames),'packet_ticks':72*len(frames),'body_capacity_per_frame':16,'frames':frames},
      'theorem':'The algebraic A/B Pauli embedding extends to an explicit 240-qutrit linear Clifford encoder U_F, synthesized exactly into ternary SUM, SCALE2 and SWAP generators.',
      'boundary':'The packet lowering proves a finite compiler/refinement contract only. It does not assign calibrated optical pulses, physical two-qutrit error rates, decoder latency, or a fault-tolerance threshold.'
    }

if __name__=='__main__':
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
