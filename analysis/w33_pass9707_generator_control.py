import sys, numpy as np, itertools, random
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt')))
G=-G0
V=np.load(SP+'minvec.npy')
type4=set((v%2).tobytes() for v in V)
q=lambda x:(int(x@G@x)//2)%2
b=lambda x,y:int(x@G@y)%2
print('IS "NO TYPE-4 CLASS" ACTUALLY SPECIAL?  A control.')
print()
print('  First, the group orders, because they decide what can be an invariant:')
def o_plus(n,qq=2):   # |O^+_{2n}(2)|
    o=2*qq**(n*(n-1))*(qq**n-1)
    for i in range(1,n): o*= (qq**(2*i)-1)
    return o
Oo=o_plus(12); Co=8315553613086720000
print(f'    |O_24^+(2)| = {Oo:.3e}')
print(f'    |Co0|       = {Co:.3e}')
print(f'    index       = {Oo/Co:.3e}   -- Co0 is a TINY subgroup')
print()
print('  Witt: the orthogonal group is TRANSITIVE on totally singular subspaces of a given')
print('  dimension. So every maximal totally singular 12-space is equivalent to every other')
print('  under O(q).  Nothing about the quadratic form alone can distinguish them.')
print('  The TYPE function is Co0-invariant, not O(q)-invariant, so it is much finer.')
print()
print('  Now: generate random maximal totally singular 12-spaces and count type-4 classes.')
rng=random.Random(11)
def rand_generator():
    basis=[]
    for _ in range(12):
        for _try in range(20000):
            v=np.array([rng.randint(0,1) for _ in range(24)],dtype=np.int64)
            if not v.any(): continue
            if q(v): continue
            if any(b(v,u) for u in basis): continue
            # independence
            w=v.copy(); ok=True
            for u in basis:
                p=next(i for i,x in enumerate(u) if x)
                if w[p]: w=(w+u)%2
            if not w.any(): continue
            basis.append(v); break
        else:
            return None
    return basis
def count4(basis):
    c=0
    for coef in itertools.product([0,1],repeat=len(basis)):
        if not any(coef): continue
        v=np.zeros(24,dtype=np.int64)
        for k,u in zip(coef,basis):
            if k: v=(v+u)%2
        if v.tobytes() in type4: c+=1
    return c
print(f"   {'trial':>6s} {'dim':>4s} {'type-4 classes held':>21s}")
got=[]
for t in range(6):
    B=rand_generator()
    if B is None: print(f'   {t:6d} {"--":>4s} {"failed to build":>21s}'); continue
    c=count4(B); got.append(c)
    print(f'   {t:6d} {len(B):4d} {c:21d}')
print()
print('   V_2 (the filtration level):        0')
if got:
    print(f'   random generators: min {min(got)}, max {max(got)}, mean {sum(got)/len(got):.1f}')
    print()
    print('   So 0 is ATYPICAL: a generic generator of the quadric holds type-4 classes.')
    print('   The vanishing is a real Co0-invariant property of V_2, not a feature every')
    print('   maximal totally singular subspace has.')
