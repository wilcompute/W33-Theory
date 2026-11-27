"""Split finite quadratic module M2(F_p), q=det/p; independent general-prime checks."""
from itertools import product
from collections import Counter
import json

def rank1(u,v,p):
    return tuple(a*b%p for a in u for b in v)

def det(x,p):
    return (x[0]*x[3]-x[1]*x[2])%p

def gramrank_mod(a,p):
    a=[list(row) for row in a]; rank=0
    for j in range(len(a[0])):
        k=next((i for i in range(rank,len(a)) if a[i][j]%p),None)
        if k is None: continue
        a[k],a[rank]=a[rank],a[k]
        c=pow(a[rank][j]%p,-1,p); a[rank]=[x*c%p for x in a[rank]]
        for i in range(rank+1,len(a)):
            c=a[i][j]%p
            if c: a[i]=[(x-c*y)%p for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def verify(p):
    V=list(product(range(p),repeat=2)); P=[(1,j) for j in range(p)]+[(0,1)]; n=p+1
    L=[{rank1(u,v,p) for v in V} for u in P]+[{rank1(u,v,p) for u in V} for v in P]
    null={x for x in product(range(p),repeat=4) if det(x,p)==0}; z=(0,)*4
    assert len(null)==1+(p-1)*n*n and set.union(*L)==null
    assert all(len(c)==p*p for c in L)
    H=[[len(a&b) for b in L] for a in L]
    assert all(H[i][j]==(p*p if i==j else 1 if i//n==j//n else p) for i in range(2*n) for j in range(2*n))
    assert gramrank_mod(H,1000003)==2*p+1
    X=set(product(range(p),repeat=4)); sizes=[]
    while X:
        start=X.pop(); orbit={start}; todo=[start]
        while todo:
            a,b,c,d=todo.pop()
            for y in [(c,d,-a%p,-b%p),(a,b,(c+a)%p,(d+b)%p)]:
                if y not in orbit: orbit.add(y); todo.append(y); X.remove(y)
        sizes.append(len(orbit))
    expected=Counter({1:1,p*p-1:p+1,p*(p*p-1):p-1})
    assert Counter(sizes)==expected and len(sizes)==2*p+1
    assert sum(sizes)==p**4
    return {'p':p,'planes':len(L),'null_vectors':len(null),'fixed_dim':len(sizes),'orbit_sizes':dict(Counter(sizes)),'gram_rank_lower_bound_mod_1000003':2*p+1,'gram_eigenvalues':[f'{2*(p+1)}/{p}',f'{p*p-1}/{p*p}','0'],'multiplicities':[1,2*p,1]}

def higher_genus(p,g):
    d=2*g; basis=[tuple(int(i==j) for i in range(d)) for j in range(d)]
    dirs=basis+[tuple((a+b)%p for a,b in zip(basis[i],basis[i+1])) for i in range(g-1)]
    def form(a,b): return sum(a[i]*b[g+i]-a[g+i]*b[i] for i in range(g))%p
    def tr(x,v):
        c=form(x,v); return tuple((a+c*b)%p for a,b in zip(x,v))
    X=set(product(range(p),repeat=2*d)); sizes=[]
    while X:
        start=X.pop(); todo=[start]; orbit={start}
        while todo:
            x=todo.pop(); a,b=x[:d],x[d:]
            for v in dirs:
                y=tr(a,v)+tr(b,v)
                if y not in orbit: orbit.add(y); todo.append(y); X.remove(y)
        sizes.append(len(orbit))
    expected=Counter([1]+[p**d-1]*(p+1)+[(p**d-1)*p**(d-1)]*(p-1)+([(p**d-1)*(p**(d-1)-p)] if g>=2 else []))
    assert Counter(sizes)==expected
    assert len(sizes)==2*p+1+(g>=2)
    n=p+1
    H=[[(p*p if i==j else 1 if i//n==j//n else p)**g for j in range(2*n)] for i in range(2*n)]
    assert gramrank_mod(H,1000003)==len(sizes)
    return {'p':p,'genus':g,'orbit_sizes':dict(Counter(sizes)),'fixed_dim':len(sizes),'boundary_tensor_rank':len(sizes)}

if __name__=='__main__': print(json.dumps({'prime_checks':[verify(p) for p in [2,3,5,7,11,13]],'higher_genus':[higher_genus(p,g) for p,g in [(2,1),(2,2),(2,3),(3,1),(3,2)]]},indent=2))
