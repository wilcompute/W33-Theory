"""Authenticated redundant arithmetic: logical value P-N, with P,N monotone.

Trusted genesis P>=N and verified transitions preserve nonnegativity. Equality
of canonical roots supplies the zero test. This is a primitive adapter, not a
replacement for the universal guest ABI or an exactly-once owner.
"""
from dataclasses import dataclass, replace, asdict
import json
from pathlib import Path
from itertools import product
import w33_counter_zipper_microcode as micro
from w33_authenticated_counter_machine import BitStore, genesis, State, layout_for
from w33_typed_universal_microvm import Program, Instruction, Carrier, digest
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress

PROGRAM=Program((Instruction('INC',0,0),Instruction('INC',1,1)),name='monotone-difference')
FIBRE=FibreProductAddress(7,2,5)

@dataclass(frozen=True)
class Pair:
    roots: tuple[str,str]
    generation: int
    session: str
    history: str
    @property
    def identity(self):return digest(asdict(self))


def initial(value,memory,session='difference-counter'):
    base=genesis(PROGRAM,memory,(value,0),session=session)
    return Pair(base.roots,0,base.session,digest({'initial':base.roots,'session':base.session}))


def base_for(pair,op):
    if op not in ('INC','DEC'):raise ValueError('unknown operation')
    return State(PROGRAM.image_id,digest(layout_for(PROGRAM)),pair.session,
                 Carrier.CIRCUIT_ST81.value,pair.roots,0 if op=='INC' else 1)


def prove(pair,op,memory):
    base=base_for(pair,op)
    if op=='DEC' and pair.roots[0]==pair.roots[1]:return ()
    control=micro.start(PROGRAM,base,FIBRE)
    out=[]
    while control.phase!='DONE':
        receipt=micro.prove_tick(PROGRAM,control,memory)
        control,writes=micro.verify_tick(PROGRAM,control,receipt)
        for node in writes:memory.put(node)
        out.append(receipt)
    return tuple(out)


def verify_step(pair,op,receipts):
    """No store or integer decoder; pair must be an admitted trusted pre-state."""
    base=base_for(pair,op)
    zero=op=='DEC' and pair.roots[0]==pair.roots[1]
    writes=[]
    if zero:
        if receipts:raise ValueError('zero decrement must not execute an inner increment')
        roots=pair.roots
    else:
        control=micro.start(PROGRAM,base,FIBRE)
        for receipt in receipts:
            control,nodes=micro.verify_tick(PROGRAM,control,receipt)
            writes.extend(nodes)
        if control.phase!='DONE':raise ValueError('incomplete inner execution')
        roots=micro.committed(PROGRAM,control).roots
    history=digest({'parent':pair.identity,'op':op,'roots':roots})
    return Pair(roots,pair.generation+1,pair.session,history),tuple(writes),max(1,len(receipts))


def inspect(pair,memory):
    p,n=map(memory.decode,pair.roots)
    return p,n,p-n


def run(start,ops):
    memory=BitStore()
    state=initial(start,memory)
    expected=start
    ticks=writes=up=down=zero=0
    for op in ops:
        receipts=prove(state,op,memory)
        # Verification only consumes roots and proof nodes.
        state,nodes,t=verify_step(state,op,receipts)
        for node in nodes:memory.put(node)
        if op=='INC':expected+=1;up+=1
        elif expected:expected-=1;down+=1
        else:zero+=1
        ticks+=t;writes+=len(nodes)
        p,n,value=inspect(state,memory)
        assert value==expected and p>=n
        assert (state.roots[0]==state.roots[1])==(expected==0)
        assert ticks==zero+5*(up+down)+2*start.bit_count()-2*p.bit_count()-2*n.bit_count()
    return dict(initial=start,operations=len(ops),final_value=expected,ticks=ticks,
                writes=writes,physical_positive=p,physical_negative=n,
                distinct_retained_nodes=len(memory.nodes))


def verify():
    paths=0
    for start in range(5):
        for ops in product(('INC','DEC'),repeat=6):
            run(start,ops);paths+=1
    cycles=[run((1<<k)-1,('INC','DEC')*128) for k in (4,16,64)]
    for k,row in zip((4,16,64),cycles):row['prior_binary_ticks']=128*(4*k+6)
    # Rejection controls: truncated, wrong-counter and corrupted proofs.
    mem=BitStore();state=initial(7,mem)
    inc=prove(state,'INC',mem)
    rejected=0
    for op,proof in [('INC',inc[:-1]),('DEC',inc)]:
        try:verify_step(state,op,proof)
        except ValueError:rejected+=1
        else:raise AssertionError('bad proof accepted')
    first=inc[0]
    bad=replace(first,after=replace(first.after,result=first.before.cursor))
    try:verify_step(state,'INC',(bad,)+inc[1:])
    except ValueError:rejected+=1
    else:raise AssertionError('changed transition accepted')
    zero=initial(0,mem)
    try:verify_step(zero,'DEC',prove(zero,'INC',mem))
    except ValueError:rejected+=1
    else:raise AssertionError('nonempty zero proof accepted')
    return dict(schema='w33.monotone-difference-counter.v1',status='PASS',
                paths=paths,cycles=cycles,negative_controls=rejected,
                law='T=Z+5(U+D)+2s(P0)+2s(N0)-2s(Pf)-2s(Nf)',
                boundary='Trusted nonnegative genesis, canonical roots and collision-resistant hashing; arithmetic microtick accounting excludes wrapper hashes; storage grows with execution history; guest ABI and owner integration open')

if __name__=='__main__':
    row=verify()
    Path(__file__).with_name('w33_monotone_difference_counter_certificate.json').write_text(json.dumps(row,indent=2,sort_keys=True)+'\n')
    print(json.dumps(row,indent=2))
