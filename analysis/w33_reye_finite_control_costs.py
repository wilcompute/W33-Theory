"""Finite echo errors, native-cost template search and noise-aware scheduling.
Imports the declared Reye controls. All device/noise quantities are synthetic.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
import w33_reye_scheduled_frames_echo as prev
p=prev.p;c=prev.c;e=prev.e


def finite_echo_audit():
    theta=np.pi/4;phi=np.arccos(-theta/(2*np.pi));rows=[]
    # Pulse speed relative to sector Rabi rate; imperfect echoes have their own error.
    for speed,echo_error in [(10,0),(100,0),(100,.001),(100,.01),(1000,.001)]:
        outcomes={n:[] for n in (0,1,4,16)}
        for axis,s,t in product('XYZ',(-1,1),(-1,1)):
            Q=(c.EYE+s*c.MATS['IZI'])@(c.EYE+t*c.MATS['IIX'])/4
            H=c.MATS[axis+'II']@Q;R=c.MATS[{'X':'Y','Y':'Z','Z':'X'}[axis]+'II']@Q
            C=c.MATS['IXI'];Z=c.MATS['IZI'];eps=.03;cross=.01
            seq=[(H,theta/2),(np.cos(phi)*H+np.sin(phi)*R,np.pi/2),
                 (np.cos(3*phi)*H+np.sin(3*phi)*R,np.pi),(np.cos(phi)*H+np.sin(phi)*R,np.pi/2),(H,theta/2)]
            ideal=expm(-1j*theta*H)
            for N in outcomes:
                U=c.EYE.copy();duration=0
                for A,dt in seq:
                    if N==0:V=expm(-1j*dt*((1+eps)*A+cross*C));duration+=dt
                    else:
                        E=expm(-1j*(np.pi/(2*speed))*(speed*(1+echo_error)*Z+cross*C))
                        B=expm(-1j*(dt/(4*N))*((1+eps)*A+cross*C))
                        D=expm(-1j*(dt/(2*N))*((1+eps)*A+cross*C))
                        V=np.linalg.matrix_power(-B@E@D@E@B,N) # correct known pair phase
                        duration+=dt+N*np.pi/speed
                    U=V@U
                inf=float(1-(abs(np.trace(ideal.conj().T@U))**2/8+1)/9)
                leak=max(0.,float(np.linalg.eigvalsh(Q@U.conj().T@(c.EYE-Q)@U@Q)[-1]))
                outcomes[N].append((inf,leak,duration))
        scores={str(N):{'infidelity':max(x[0] for x in v),'leakage':max(x[1] for x in v),'duration':v[0][2]} for N,v in outcomes.items()}
        winner=min(scores,key=lambda N:scores[N]['infidelity'])
        rows.append({'echo_speed':speed,'echo_fractional_error':echo_error,'scores':scores,'best_tested_cycles':int(winner)})
    assert any(r['best_tested_cycles']!=16 for r in rows)
    return {'rows':rows,'boundary':'Finite square echoes include continuous X2 crosstalk during each echo and independent amplitude error. Sector drive is off during echoes; no Markov noise or measured hardware parameters. Best only among tested counts.'}


def native_cost_audit():
    proof,dist=e.shortest_proof();native=sorted(c.BASE+c.EXTRA)
    @lru_cache(None)
    def templates(w,t):
        if w in native:return (((w,t),),)
        out=[]
        for a in native:
            b=c.xor(a,w)
            if not c.anticommutes(a,w) or dist[b]!=dist[w]-1:continue
            sign=1 if np.array_equal(-1j*c.MATS[a]@c.MATS[b],c.MATS[w]) else -1
            for mid in templates(b,sign*t):out.append(((a,F(1,4)),)+mid+((a,F(-1,4)),))
        return tuple(out[:32])
    baseline=[];beam=[[]]
    for w in sorted(proof):
        baseline.extend((v,F(t/np.pi).limit_denominator(10000)) for v,t in c.pulses(w,np.pi/7,proof))
        candidates={tuple(p.commute_reduce(old+list(new))) for old in beam for new in templates(w,F(1,7))}
        beam=[list(x) for x in sorted(candidates,key=lambda a:(len(a),a))[:16]]
    before=p.commute_reduce(baseline);best=min(beam+[before],key=len)
    U=lambda seq:e.unitary([(w,float(t)*np.pi) for w,t in seq])
    error=float(np.max(abs(U(best)-U(baseline))))
    assert error<1e-12 and all(w in native for w,t in best) and len(best)<=len(before)
    return {'baseline_native_pulses':len(before),'optimized_native_pulses':len(best),'matrix_error':error,
      'program':[[w,str(t)] for w,t in best],'template_cap':32,'beam_width':16,
      'boundary':'Native-cost beam search over alternative shortest conjugation frames with exact rational merges. No global optimum claim; all emitted words are declared native controls.'}


def noise_schedule_audit():
    # Four commuting disjoint CNOT jobs; pairs share hard ports, other pairs
    # have a calibrated-in-principle soft crosstalk penalty when overlapping.
    jobs=[{'edge':[0,1],'port':'a'},{'edge':[2,3],'port':'a'},
          {'edge':[4,5],'port':'b'},{'edge':[6,7],'port':'b'}]
    schedules=[]
    for starts in product(range(4),repeat=4):
        if min(starts)!=0 or starts[0]==starts[1] or starts[2]==starts[3]:continue
        makespan=max(starts)+1
        overlap=sum(starts[i]==starts[j] for i in (0,1) for j in (2,3))
        schedules.append((makespan,overlap,starts))
    rows=[]
    # Markov phase-flip parity: q=(1-exp(-2 L))/2, where L is additive exposure.
    # idle cost here is total time across eight memory qubits; overhead modeled.
    for memory_rate,cross_rate in [(0.001,0.1),(.1,.001),(.01,.04)]:
        score=lambda r:8*memory_rate*r[0]+cross_rate*r[1]
        winner=min(schedules,key=lambda r:(score(r),r));fast=min(schedules)
        L=score(winner);q=float(-np.expm1(-2*L)/2)
        rows.append({'memory_rate':memory_rate,'overlap_rate':cross_rate,'starts':winner[2],
          'duration':winner[0],'overlaps':winner[1],'dephasing_exposure':L,'phase_flip_probability':q,
          'fastest_duration':fast[0],'fastest_exposure':score(fast)})
        # Every schedule realizes the same full permutation.
        v=np.arange(256);ref=v.copy()
        for job in jobs:ref=e.cnot_permutation(8,*job['edge'])[ref]
        for i in sorted(range(4),key=lambda i:winner[2][i]):v=e.cnot_permutation(8,*jobs[i]['edge'])[v]
        assert np.array_equal(v,ref)
    assert rows[0]['duration']>rows[0]['fastest_duration']
    assert rows[1]['duration']==rows[1]['fastest_duration']
    return {'candidate_schedules':len(schedules),'rows':rows,
      'boundary':'Exhaustive bounded four-job model with hard ports and additive Markov dephasing exposure. Synthetic rates, not a general many-qubit error model or hardware optimum.'}


if __name__=='__main__':
    import sys
    out={'status':'PASS','finite_echo':finite_echo_audit(),'native_cost':native_cost_audit(),'noise_schedule':noise_schedule_audit()}
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a!='program'} if isinstance(v,dict) else v for k,v in out.items()},indent=2))
