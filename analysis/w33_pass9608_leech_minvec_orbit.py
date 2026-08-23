import sys, numpy as np
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt')))
G=-G0                      # the recovered form was negative definite
gens=load_flat(Path('analysis/_co0_G.txt'))
print('SIGN FIX: the recovered Gram was NEGATIVE definite; using -G.')
print('  diagonal now:',sorted(set(int(G[i,i]) for i in range(24))))
print('  minimum diagonal entry =',min(int(G[i,i]) for i in range(24)),'(Leech minimum is 4)')
print('  generators preserve -G too:',all(np.array_equal(g.T@G@g,G) for g in gens))
print('  (all earlier results are rank/symmetry statements mod p, invariant under a')
print('   global sign, so none of them change.)')
start=None
for i in range(24):
    if int(G[i,i])==4: start=np.eye(24,dtype=np.int64)[i]; break
print('  norm-4 basis vector found:',start is not None)
print()
print('GENERATING THE Co0 ORBIT')
inv=[np.rint(np.linalg.inv(g.astype(float))).astype(np.int64) for g in gens]
acts=[a for a in gens+inv]
seen={start.tobytes():1}; frontier=[start]
rounds=0
while frontier and rounds<80:
    rounds+=1
    F=np.array(frontier,dtype=np.int64); nf=[]
    for A in acts:
        Im=F@A.T
        for row in Im:
            k=row.tobytes()
            if k not in seen:
                seen[k]=1; nf.append(row)
    frontier=nf
print('  rounds:',rounds,'  orbit size:',len(seen))
V=np.frombuffer(b''.join(seen.keys()),dtype=np.int64).reshape(-1,24)
nrm=set(int(v@G@v) for v in V[:500])
print('  norms present (sample of 500):',sorted(nrm))
cls=set((v%2).tobytes() for v in V)
print('  distinct classes mod 2:',len(cls),'  ratio orbit/classes =',len(seen)/max(len(cls),1))
np.save('C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/minvec.npy',V)
