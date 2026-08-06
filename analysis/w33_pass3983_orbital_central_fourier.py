#!/usr/bin/env python3
"""Pass 3983: primitive central idempotents and character table in the literal 48-orbital basis."""
from __future__ import annotations
import base64, hashlib, json, zlib
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]

def unpack_tensor():
    manifest=json.loads((ROOT/'data/PART_3973_3980_EXTREMAL_MESH_PHOTON_TENSOR_manifest.json').read_text())
    path=ROOT/manifest['rank48_tensor']['path']
    raw=zlib.decompress(base64.b64decode(path.read_text(encoding='ascii').strip()))
    assert hashlib.sha256(raw).hexdigest()==manifest['rank48_tensor']['json_sha256']
    return json.loads(raw)

def normalize_entries(tensor):
    raw=tensor['tensor_entries']; out=[]
    for e in raw:
        if isinstance(e,dict):
            def pick(*names):
                for n in names:
                    if n in e: return e[n]
                raise KeyError((names,e))
            i=pick('i','left','a','r'); j=pick('j','right','b','s'); k=pick('k','output','c','t'); v=pick('p','value','coefficient','n')
        else:
            if len(e)!=4: raise ValueError(e)
            i,j,k,v=e
        out.append((int(i),int(j),int(k),sp.Rational(v)))
    return out

def frac(x):
    x=sp.Rational(x); return str(x.p) if x.q==1 else f'{x.p}/{x.q}'

def canonical_sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    tensor=unpack_tensor(); entries=normalize_entries(tensor); n=48
    L=[sp.zeros(n,n) for _ in range(n)]
    for i,j,k,v in entries: L[i][k,j]+=v
    # Identity vector u satisfies sum_i u_i L_i=I.
    rows=[]; rhs=[]
    for r in range(n):
        for c in range(n):
            rows.append([L[i][r,c] for i in range(n)]); rhs.append(1 if r==c else 0)
    A=sp.Matrix(rows); b=sp.Matrix(rhs)
    sol=sp.linsolve((A,b)); identity=sp.Matrix(list(next(iter(sol))))
    assert sum((identity[i]*L[i] for i in range(n)),sp.zeros(n,n))==sp.eye(n)
    # Center equations: x*e_j=e_j*x.
    C=[]
    lookup={(i,j,k):v for i,j,k,v in entries}
    for j in range(n):
        for k in range(n):
            C.append([lookup.get((i,j,k),0)-lookup.get((j,i,k),0) for i in range(n)])
    center=sp.Matrix(C).nullspace(); assert len(center)==7
    # Search a small separating central element.
    eigen=None; zvec=None; Lz=None
    coefficient_trials=[
      [1,2,4,8,16,32,64],[1,3,9,27,81,243,729],
      [2,5,11,23,47,97,197],[1,-2,4,-8,16,-32,64]
    ]
    for coeffs in coefficient_trials:
        z=sum((sp.Integer(a)*v for a,v in zip(coeffs,center)),sp.zeros(n,1))
        M=sum((z[i]*L[i] for i in range(n)),sp.zeros(n,n))
        ev=M.eigenvals()
        if len(ev)==7 and all(x.is_Rational for x in ev):
            mults=sorted(int(m) for m in ev.values())
            if mults==[1,1,4,4,4,9,25]: eigen=ev; zvec=z; Lz=M; break
    assert eigen is not None
    idempotents=[]; chars=[]
    eigenvalues=sorted(eigen,key=lambda x:(int(eigen[x]),sp.Rational(x)))
    for lam in eigenvalues:
        P=sp.eye(n)
        for mu in eigenvalues:
            if mu!=lam: P=(P*(Lz-mu*sp.eye(n)))/(lam-mu)
        P=sp.simplify(P)
        e=sp.simplify(P*identity)
        Le=sum((e[i]*L[i] for i in range(n)),sp.zeros(n,n))
        assert Le==P and P*P==P
        rank=int(P.rank()); d=int(sp.sqrt(rank)); assert d*d==rank
        support=[i for i,x in enumerate(e) if x]
        row=[]
        for i in range(n): row.append(sp.simplify(sp.trace(L[i]*P)/d))
        idempotents.append({'eigenvalue':frac(lam),'regular_rank':rank,'simple_degree':d,
          'support_size':len(support),'coefficients':[[i,frac(e[i])] for i in support]})
        chars.append([frac(x) for x in row])
    # Orthogonal completeness.
    Es=[]
    for item in idempotents:
        e=sp.zeros(n,1)
        for i,x in item['coefficients']: e[i]=sp.Rational(x)
        Es.append(sum((e[i]*L[i] for i in range(n)),sp.zeros(n,n)))
    assert sum(Es,sp.zeros(n,n))==sp.eye(n)
    for i in range(7):
        for j in range(7): assert Es[i]*Es[j]==(Es[i] if i==j else sp.zeros(n,n))
    payload={'schema':'w33.pass3983.orbital_central_fourier.v1','status':'PASS',
      'relations':n,'tensor_nonzeros':len(entries),'center_dimension':len(center),
      'simple_degrees':[x['simple_degree'] for x in idempotents],
      'primitive_central_idempotents':idempotents,'irreducible_character_table':chars,
      'identity_coefficients':[[i,frac(identity[i])] for i in range(n) if identity[i]],
      'boundary':'Exact rational central Fourier transform in the literal orbital basis. This is not a complete classification of all combinatorial fusion schemes.'}
    payload['character_table_sha256']=canonical_sha(chars)
    payload['idempotent_sha256']=canonical_sha(idempotents)
    (ROOT/'data/PART_3983_ORBITAL_CENTRAL_FOURIER.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print('PASS_ORBITAL_CENTRAL_FOURIER',payload['simple_degrees'],payload['character_table_sha256'])
if __name__=='__main__': main()
