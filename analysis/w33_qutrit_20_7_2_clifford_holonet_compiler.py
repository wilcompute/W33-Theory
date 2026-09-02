#!/usr/bin/env python3
"""Compile the exact support-optimized [[20,7,2]]_3 symplectic embedding into
an explicit qutrit linear-Clifford encoder and a Holonet packet-level schedule.

The A/B input is supplied by the deterministic CP-SAT optimizer: A is exact
minimum support within its displayed fixed-minor class and B is exact minimum
support for that optimized A. Choose 220 rows C spanning ker(B), so
F=[A;C] lies in GL(240,3), F B^T=[I_20;0], and the first 20 rows of F^{-T} are
B. The reversible qutrit basis map U_F|x>=|xF> realizes A/B on the first twenty
input Pauli generators.

GF(3) column Gauss-Jordan synthesizes F into SWAP, SCALE2, and SUM_ALPHA
Cliffords. Non-conflicting macros are packed into the existing 16-slot, 72-tick
Holonet body while preserving each wire's gate order, with
LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX refinement.
"""
from __future__ import annotations
import hashlib, json
import numpy as np

import w33_qutrit_20_7_2_symplectic_embedding as base
import w33_qutrit_20_7_2_cpsat_support_optimizer as cpopt


def optimized_witness():
    hx,hz,h,targets,A0,A,B,fixed,arec,brec=cpopt.optimized_witness()
    return hx,hz,h,targets,A,B,{'fixed_minor':fixed,'A_records':arec,'B_records':brec}


def build_full_linear(A,B):
    kerB=base.nullspace(B)
    if len(kerB)!=220: raise RuntimeError('expected dim ker(B)=220')
    F=np.vstack([A,kerB])%3
    if base.rank(F)!=240: raise RuntimeError('A plus ker(B) did not form a basis')
    Finv=base.inv(F)
    if not np.array_equal(F[:20],A): raise RuntimeError('A prefix lost')
    if not np.array_equal(Finv.T[:20]%3,B%3): raise RuntimeError('dual Z prefix is not B')
    return F,Finv


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
    build=[]
    for op in reversed(ops):
        if op['gate']=='SUM_ALPHA': build.append({**op,'alpha':(-op['alpha'])%3})
        else: build.append(dict(op))
    return build


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
    # Preserve the circuit's partial order.  For every wire, a later gate must
    # be placed strictly after the frame containing the previous gate on that
    # wire.  Gates on disjoint wires commute and may share a frame.
    frames=[]; last_frame={}; assignment={}
    for gi,g in enumerate(gates):
        gw=wires(g)
        earliest=max((last_frame.get(w,-1)+1 for w in gw),default=0)
        fi=earliest
        while True:
            while len(frames)<=fi: frames.append({'slots':[],'used':set()})
            f=frames[fi]
            if len(f['slots'])<16 and not (gw & f['used']):
                f['slots'].append((gi,g)); f['used']|=gw; assignment[gi]=fi
                for w in gw: last_frame[w]=fi
                break
            fi+=1
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
    return out,assignment


def per_wire_order_ok(gates,assignment):
    last={}
    for gi,g in enumerate(gates):
        fi=assignment[gi]
        for w in wires(g):
            if w in last and fi<=last[w]: return False
            last[w]=fi
    return True


def digest_matrix(a): return 'sha256:'+hashlib.sha256(bytes(int(x) for x in a.flatten())).hexdigest()
def digest_json(v): return 'sha256:'+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def verify():
    hx,hz,h,targets,A,B,opt=optimized_witness()
    F,Finv=build_full_linear(A,B)
    gates=reduce_columns_to_identity(F)
    replay=apply_right_ops(240,gates)
    frames,assignment=pack_microframes(gates)
    counts={k:int(sum(g['gate']==k for g in gates)) for k in ('SUM_ALPHA','SCALE2','SWAP')}
    checks={
      'full_linear_map_rank_240':base.rank(F)==240,
      'data_X_prefix_is_A':np.array_equal(F[:20],A),
      'data_Z_prefix_is_B':np.array_equal(Finv.T[:20]%3,B),
      'circuit_replays_exact_F':np.array_equal(replay,F),
      'symplectic_data_embedding':np.array_equal((A@B.T)%3,np.eye(20,dtype=np.int64)),
      'packet_slots_at_most_16':all(len(f['slots'])<=16 for f in frames),
      'packet_slots_wire_disjoint':all(len(set(w for s in f['slots'] for w in wires(s['gate'])))==sum(len(wires(s['gate'])) for s in f['slots']) for f in frames),
      'per_wire_gate_order_preserved':per_wire_order_ok(gates,assignment),
      'three_phase_word_exact':all([t['op'] for s in f['slots'] for t in s['ticks']]==['LOAD_FLAG','FLIP_Q6_AXIS','LATCH_VERTEX']*len(f['slots']) for f in frames),
    }
    checks={k:bool(v) for k,v in checks.items()}
    schedule_digest=digest_json(frames)
    sample=frames[:2]+(frames[-2:] if len(frames)>2 else [])
    return {
      'schema':'w33.qutrit-20-7-2-clifford-holonet-compiler.v3',
      'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'optimizer':{'class':'CP_SAT_FIXED_MINOR_A_PLUS_EXACT_B','fixed_minor_columns_0_indexed':opt['fixed_minor']},
      'linear_encoder':{'F_sha256':digest_matrix(F),'A_sha256':digest_matrix(A),'B_sha256':digest_matrix(B),'gate_count':int(len(gates)),'gate_counts':counts},
      'packet_schedule':{'sha256':schedule_digest,'microframes':int(len(frames)),'packet_ticks':int(72*len(frames)),'body_capacity_per_frame':16,'per_wire_order':'STRICT','sample_frames':sample},
      'theorem':'The exact support-optimized A/B Pauli embedding extends to an explicit 240-qutrit linear Clifford encoder U_F, synthesized exactly into ternary SUM, SCALE2 and SWAP generators and packetized without reordering any wire-local gate sequence.',
      'boundary':'The packet lowering proves a finite compiler/refinement contract only. It does not assign calibrated optical pulses, physical two-qutrit error rates, decoder latency, or a fault-tolerance threshold.'
    }

if __name__=='__main__':
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
