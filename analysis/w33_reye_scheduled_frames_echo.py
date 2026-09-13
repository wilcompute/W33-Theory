"""Shared-port scheduling, Clifford IR, echoed BB1 and quartic frame selection.
Prior: w33_reye_network_robust_frames and Schur sixteen-line fibre certificate.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import product
import json
import numpy as np
from scipy.linalg import expm
import w33_reye_network_robust_frames as p
c=p.c;e=p.e


def schedule(operations):
    """Deterministic earliest-start list schedule preserving per-qubit input order.
    Each operation declares positive integer duration and exclusive extra resources.
    Shared-qubit dependencies retain the serial unitary; port order is selectable.
    """
    rows=[];last={}
    for i,o in enumerate(operations):
        a,b=o['edge'];dt=o['duration']
        if a==b or min(a,b)<0 or type(dt) is not int or dt<1:raise ValueError('invalid operation')
        deps={last[q] for q in (a,b) if q in last}
        rows.append({**o,'id':i,'deps':sorted(deps),'resources':sorted(set(o.get('ports',[]))|{f'q:{a}',f'q:{b}'})})
        last[a]=last[b]=i
    pending=set(range(len(rows)));done={};calendar={}
    while pending:
        choices=[]
        for i in sorted(pending):
            r=rows[i]
            if any(j not in done for j in r['deps']):continue
            start=max((done[j]['end'] for j in r['deps']),default=0)
            while True:
                overlap=[end for resource in r['resources'] for begin,end in calendar.get(resource,[])
                         if start<end and start+r['duration']>begin]
                if not overlap:break
                start=max(overlap)
            choices.append((start,i))
        start,i=min(choices);r={**rows[i],'start':start,'end':start+rows[i]['duration']}
        done[i]=r;pending.remove(i)
        for resource in r['resources']:calendar.setdefault(resource,[]).append((r['start'],r['end']))
    return [done[i] for i in sorted(done)]


def schedule_audit():
    ops=[]
    # Two disjoint routed register operations: independent qubits, shared drive buses.
    for offset in (0,6):
        for a,b in e.network_compile(2,2,5):
            a+=offset;b+=offset
            ports=sorted({f'bus:{(a//3)%2}',f'bus:{(b//3)%2}'}) if a//3!=b//3 else []
            ops.append({'edge':[a,b],'duration':1,'ports':ports})
    rows=schedule(ops)
    for i,r in enumerate(rows):
        for j in r['deps']:assert rows[j]['end']<=r['start']
        for s in rows[i+1:]:
            if set(r['resources'])&set(s['resources']):assert r['end']<=s['start'] or s['end']<=r['start']
    # Full permutation, not only dependency bookkeeping.
    serial=np.arange(4096);parallel=serial.copy()
    for o in ops:serial=e.cnot_permutation(12,*o['edge'])[serial]
    for o in sorted(rows,key=lambda r:(r['start'],r['id'])):parallel=e.cnot_permutation(12,*o['edge'])[parallel]
    assert np.array_equal(serial,parallel)
    assert max(r['end'] for r in rows)<len(ops)
    # Extra port conflict despite disjoint qubits is enforced.
    collision=schedule([{'edge':[0,1],'duration':3,'ports':['shared']},{'edge':[2,3],'duration':2,'ports':['shared']}])
    assert collision[1]['start']==3
    return {'serial_duration':len(ops),'scheduled_duration':max(r['end'] for r in rows),'schedule':rows,
      'scope':'Exclusive declared port and qubit resources, integer durations, dependency-preserving list heuristic. No optimal makespan, analog overlap or calibrated bandwidth claim.'}


def conjugate_quarter(a,w,turns):
    sign=1
    for _ in range(turns%4):
        if c.anticommutes(a,w):
            v=c.xor(a,w);M=-1j*c.MATS[a]@c.MATS[w]
            s=1 if np.array_equal(M,c.MATS[v]) else -1
            assert np.array_equal(M,s*c.MATS[v]);w=v;sign*=s
    return w,sign


def frame_compile(program):
    """Product order U = product(non-Clifford rotations) * terminal Clifford.
    Frame words retained exactly, including scalar phase in their pulse realization.
    """
    frame=[];out=[]
    for w,t in program:
        t=F(t)
        if (4*t).denominator==1:frame.append((w,t));continue
        sign=1
        for a,q in reversed(frame):
            w,s=conjugate_quarter(a,w,int(4*q));sign*=s
        out.append((w,sign*t))
    return p.commute_reduce(out),p.commute_reduce(frame)


def frame_audit():
    proof,_=e.shortest_proof();program=[]
    for w in sorted(proof):program += [(v,F(t/np.pi).limit_denominator(10000)) for v,t in c.pulses(w,np.pi/7,proof)]
    rotations,frame=frame_compile(program)
    U=lambda prog:e.unitary([(w,float(t)*np.pi) for w,t in prog])
    err=float(np.max(abs(U(program)-U(rotations)@U(frame))));assert err<1e-12
    assert len(rotations)==63
    # Lower transformed nonnative rotations back to the actual native alphabet.
    lower=[]
    for w,t in rotations:lower+=c.pulses(w,float(t)*np.pi,proof)
    lower += [(w,float(t)*np.pi) for w,t in frame]
    assert np.max(abs(e.unitary(lower)-U(program)))<1e-12
    rng=np.random.default_rng(24063)
    for _ in range(60):
        prog=[(c.WORDS[int(rng.integers(1,64))],F(int(rng.integers(-3,4)),int(rng.choice([4,7])))) for _ in range(24)]
        ro,fr=frame_compile(prog);assert np.max(abs(U(prog)-U(ro)@U(fr)))<1e-12
    sandwich=[('ZII',F(1,4)),('XII',F(1,7)),('ZII',F(-1,4)),('YII',F(-1,7))]
    ro,fr=frame_compile(sandwich)
    assert len(p.commute_reduce(sandwich))==4 and not ro and not fr
    assert np.max(abs(U(sandwich)-c.EYE))<1e-12
    lower_reduced=p.commute_reduce([(w,F(t/np.pi).limit_denominator(10000)) for w,t in lower])
    assert np.max(abs(U(lower_reduced)-U(program)))<1e-12
    return {'clifford_sandwich_before':4,'clifford_sandwich_after':0,'relowered_after_commuting':len(lower_reduced),
       'input_native_pulses':len(program),'rotation_ir_count':len(rotations),'terminal_frame_pulses':len(frame),
       'relowered_native_pulses':len(lower),'matrix_error':err,'random_matrix_checks':60,
       'scope':'Exact phase-retaining Clifford IR factoring. Abstract rotations are not free native gates; relowering cost reported. Prior: PCOAST and arXiv:1903.12456.'}


def echo_audit():
    theta=np.pi/4;phi=np.arccos(-theta/(2*np.pi));rows=[]
    for eps,cross in ((.03,.01),(-.03,.01),(.1,.02),(.03,-.01)):
        metrics={k:[] for k in ('base','bb1','echo4','echo16')}
        for axis,s,t in product('XYZ',(-1,1),(-1,1)):
            Q=(c.EYE+s*c.MATS['IZI'])@(c.EYE+t*c.MATS['IIX'])/4
            P=c.MATS[axis+'II']@Q;R=c.MATS[{'X':'Y','Y':'Z','Z':'X'}[axis]+'II']@Q
            E=c.MATS['IZI'];C=c.MATS['IXI']
            assert np.max(abs(E@P@E-P))<1e-14 and np.array_equal(E@C@E,-C)
            tilted=lambda f:np.cos(f)*P+np.sin(f)*R
            bb=[(P,theta/2),(tilted(phi),np.pi/2),(tilted(3*phi),np.pi),(tilted(phi),np.pi/2),(P,theta/2)]
            ideal=expm(-1j*theta*P)
            for name,N in [('base',0),('bb1',0),('echo4',4),('echo16',16)]:
                U=c.EYE.copy()
                for H,dt in ([(P,theta)] if name=='base' else bb):
                    if not N:V=expm(-1j*dt*((1+eps)*H+cross*C))
                    else:
                        # Physical E echo pulses ideal/instantaneous. Two per cycle,
                        # implemented by R_Z2(pi/2) with the pair's scalar phase corrected.
                        A=expm(-1j*(dt/(4*N))*((1+eps)*H+cross*C))
                        B=expm(-1j*(dt/(2*N))*((1+eps)*H+cross*C))
                        V=np.linalg.matrix_power(A@E@B@E@A,N)
                    U=V@U
                fid=(abs(np.trace(ideal.conj().T@U))**2/8+1)/9
                leak=max(0.,float(np.linalg.eigvalsh(Q@U.conj().T@(c.EYE-Q)@U@Q)[-1]))
                metrics[name].append((float(1-fid),leak))
        row={'amplitude':eps,'crosstalk':cross,**{k:{'worst_infidelity':max(x[0] for x in v),'worst_leakage':max(x[1] for x in v)} for k,v in metrics.items()}}
        assert row['echo16']['worst_infidelity']<row['base']['worst_infidelity']/100
        assert row['echo16']['worst_leakage']<row['echo4']['worst_leakage']/100
        rows.append(row)
    return {'rows':rows,'settings_per_row':12,'echo_pulses_per_bb1':{'echo4':40,'echo16':160},
      'proof':'E=Z2 commutes with the selected control and anticommutes with X2 crosstalk. Symmetric echo cycling removes the mean crosstalk; finite-cycle residuals are checked with full matrices.',
      'boundary':'Ideal instantaneous error-free Z2 echoes and simultaneous phased sector controls; BB1 duration remains ninefold excluding echoes. No finite-bandwidth echo, detuning, Markov-dephasing or hardware robustness claim.'}


def quartic_audit():
    import sympy as s
    import w33_schur_cross_kernel_matrices as k
    import w33_schur176_sixteen_line_fibre_structure as f
    data=json.loads(Path(p.__file__).with_suffix('.json').read_text())['normalizer']['frame_maps']
    raw=json.loads(Path(k.__file__).with_suffix('.json').read_text())
    S=s.Matrix([[s.sympify(x) for x in row] for row in raw['conjugator_to_pauli']])
    x,y=s.symbols('x y');u,v=S*s.Matrix([x,y])
    # Work in the Pauli chart to avoid expanding complicated conjugator inverses.
    poly=s.Poly(s.expand(f.phi(u,v)),x,y);h=s.Poly(s.expand(f.hess(u,v)),x,y)
    phi=s.expand(poly.as_expr()/poly.coeff_monomial(x**4));hh=s.expand(h.as_expr()/h.coeff_monomial(x**4))
    def multiplier(expr,T):
        U,V=T*s.Matrix([x,y]);new=s.Poly(s.expand(expr.subs({x:U,y:V},simultaneous=True)),x,y)
        old=s.Poly(expr,x,y);a=s.simplify(new.coeff_monomial(x**4)/old.coeff_monomial(x**4))
        return a if all(s.simplify(new.coeff_monomial(x**(4-j)*y**j)-a*old.coeff_monomial(x**(4-j)*y**j))==0 for j in range(5)) else None
    H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);D=s.diag(1,s.I);rows=[]
    for row in data:
        T=s.eye(2)
        for g in row['generator_word']:T=(H,D)[g]*T
        T=k.simp(T);a=multiplier(phi,T);b=multiplier(hh,T)
        if a is not None:
            assert b is not None and s.simplify(a*s.conjugate(a))==1
            chi=s.simplify(b/a);assert s.simplify(chi**3)==1
            rows.append({'word':row['generator_word'],'frame_permutation':row['permutation'],'quartic_multiplier':str(a),'hessian_character_after_phase_lift':str(chi),'scalar_lift_equation':'lambda^4 = 1/('+str(a)+')'})
    assert len(rows)==12
    counts=Counter(r['hessian_character_after_phase_lift'] for r in rows)
    assert sorted(counts.values())==[4,4,4]
    # Prior owns A4 and 48 lifts; this connects that result to concrete Clifford frames.
    return {'preserving_projective_frames':12,'rejected_projective_frames':12,'quartic_exact_scalar_lifts':48,'character_counts':dict(counts),'rows':rows,
      'boundary':'Preservation up to phase for projective frames; four scalar fourth-root corrections per frame give exact quartic preservation. Prior A4/48 theorem cited, not rediscovered. Only four projective frames preserve quartic and Hessian simultaneously after correction.'}


if __name__=='__main__':
    import sys
    out={'status':'PASS','schedule':schedule_audit(),'frames':frame_audit(),'echo':echo_audit(),'quartic':quartic_audit()}
    if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a not in ('rows','schedule')} if isinstance(v,dict) else v for k,v in out.items()},indent=2))
