"""Two-register INC/DECJZ/HALT guest adapter over four monotone roots.
Pure proof verification; consumption authorization remains an owner obligation.
"""
from dataclasses import dataclass,asdict,replace
from pathlib import Path
from itertools import product
import json
import w33_monotone_difference_counter as primitive
import w33_authenticated_counter_machine as binary
from w33_typed_universal_microvm import Program,Instruction,digest,GEOMETRY,instruction_portal

@dataclass(frozen=True)
class Guest:
    image:str
    pairs:tuple
    pc:int=0
    steps:int=0
    portal:int=0
    halted:bool=False
    history:str='genesis'
    @property
    def identity(self):return digest(asdict(self))

@dataclass(frozen=True)
class Receipt:
    parent:str
    proof:tuple
    after:Guest


def genesis(program,memory,values,session):
    if len(values)!=2 or not session:raise ValueError('two counters and session required')
    return Guest(program.image_id,tuple(primitive.initial(v,memory,session+':'+str(j)) for j,v in enumerate(values)))


def transition(program,state,proof):
    if state.image!=program.image_id or state.halted or not 0<=state.pc<len(program.instructions):raise ValueError('inactive or foreign guest')
    ins=program.instructions[state.pc];pairs=list(state.pairs);writes=();ticks=1;pc=state.pc
    if ins.op=='HALT':
        if proof:raise ValueError('HALT has no arithmetic proof')
    else:
        r=ins.register;zero=pairs[r].roots[0]==pairs[r].roots[1]
        pairs[r],writes,ticks=primitive.verify_step(pairs[r],'INC' if ins.op=='INC' else 'DEC',proof)
        pc=ins.zero_target if ins.op=='DECJZ' and zero else ins.target
    portal=instruction_portal(state.pc,ins,program.image_id)
    route=GEOMETRY.route(state.portal,portal)
    after=Guest(state.image,tuple(pairs),pc,state.steps+1,portal,ins.op=='HALT',digest({'parent':state.identity,'pc':pc,'route':route,'pairs':[p.identity for p in pairs]}))
    return after,writes,ticks,route


def prove(program,state,memory):
    if state.image!=program.image_id or state.halted:raise ValueError('inactive or foreign guest')
    ins=program.instructions[state.pc]
    proof=() if ins.op=='HALT' else primitive.prove(state.pairs[ins.register],'INC' if ins.op=='INC' else 'DEC',memory)
    return Receipt(state.identity,proof,transition(program,state,proof)[0])


def verify(program,expected,receipt):
    if receipt.parent!=expected.identity:raise ValueError('foreign or stale parent')
    result=transition(program,expected,receipt.proof)
    if result[0]!=receipt.after:raise ValueError('forged guest transition')
    return result


def audit():
    programs=[Program((Instruction('DECJZ',0,1,2),Instruction('INC',1,0),Instruction('HALT')),name='transfer'),
              Program((Instruction('DECJZ',1,1,2),Instruction('INC',0,0),Instruction('HALT')),name='reverse-transfer'),
              Program((Instruction('INC',0,1),Instruction('DECJZ',0,2,3),Instruction('DECJZ',1,0,3),Instruction('HALT')),name='mixed')]
    steps=0
    for program,values in product(programs,product(range(5),repeat=2)):
        memory=binary.BitStore();reference_memory=binary.BitStore()
        state=genesis(program,memory,values,'audit');reference=binary.genesis(program,reference_memory,values,session='audit')
        for _ in range(100):
            receipt=prove(program,state,memory);state,writes,_,_=verify(program,state,receipt)
            for node in writes:memory.put(node)
            reference,nodes=binary.verify_step(program,reference,binary.prove_step(program,reference,reference_memory))
            for node in nodes:reference_memory.put(node)
            assert tuple(primitive.inspect(p,memory)[2] for p in state.pairs)==tuple(reference_memory.decode(r) for r in reference.roots)
            assert (state.pc,state.steps,state.halted,state.portal)==(reference.pc,reference.steps,reference.halted,reference.portal)
            steps+=1
            if state.halted:break
        else:raise AssertionError('test guest did not halt')
    p=programs[0];memory=binary.BitStore();state=genesis(p,memory,(7,2),'negative');receipt=prove(p,state,memory)
    bad=[(p,state,replace(receipt,parent='foreign')),(programs[1],state,receipt),
         (p,state,replace(receipt,proof=receipt.proof[:-1])),(p,state,replace(receipt,after=replace(receipt.after,pc=2))),
         (p,state,replace(receipt,after=replace(receipt.after,pairs=tuple(reversed(receipt.after.pairs))))),
         (p,receipt.after,receipt)]
    for program,expected,r in bad:
        try:verify(program,expected,r)
        except ValueError:pass
        else:raise AssertionError('mutation accepted')
    return dict(status='PASS',programs=3,input_pairs_per_program=25,verified_guest_steps=steps,negative_controls=len(bad),
        refinement='Each INC or nonzero DECJZ increments the corresponding P or N; root equality selects zero branch; HALT preserves both pairs. Thus P-N matches the existing two-counter ISA by induction.',
        boundary='Trusted canonical nonnegative genesis and collision-resistant hashes; abstract unbounded memory; no new physical universality or exactly-once owner integration claim')

if __name__=='__main__':
    row=audit();Path(__file__).with_suffix('.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row,indent=2))
