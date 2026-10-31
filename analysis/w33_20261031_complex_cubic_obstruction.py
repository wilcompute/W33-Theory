"""Arbitrary C* monomial phases cannot descend the native cubic action.

Perfect point stabilizers trivialize monomial phases on the 16 orbit up to
diagonal gauge. Nine exact multiplicative equations then give 1=-1.
"""
import json,pathlib,itertools,sys
import numpy as np,sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_signed_cubic_lift import solve2

def constraints(generators,coefficients):
    rows=[];rhs=[];descriptions=[]
    for j,g in enumerate(generators):
        vectors={}
        for v in range(1,11):
            records=[]
            for t,c in coefficients.items():
                if v not in t or 0 in t:continue
                r=[0]*16
                for i in t:
                    if i>=11:r[i-11]+=1;r[g[i]-11]-=1
                b=int(c!=coefficients[tuple(sorted(g[i]for i in t))]);records.append((r,b,t))
            assert len(records)==4
            r0,b0,t0=records[0];vectors[v]=(r0,b0,t0)
            for r,b,t in records[1:]:
                rows.append([a-c for a,c in zip(r,r0)]);rhs.append((b0-b)%2)
                descriptions.append(dict(kind='same_vector',generator=j,left=t,right=t0))
        for t,c in coefficients.items():
            if 0 not in t:continue
            v,w=[i for i in t if i];r,b,tv=vectors[v];u,a,tw=vectors[w]
            bt=int(c!=coefficients[tuple(sorted(g[i]for i in t))])
            rows.append([x+y for x,y in zip(r,u)]);rhs.append((bt-b-a)%2)
            descriptions.append(dict(kind='singlet',generator=j,triple=t,vector_terms=[tv,tw]))
    return rows,rhs,descriptions

def perfect_subgroup(H,mul,inv,identity):
    def close(gens):
        seen={identity};queue=[identity]
        for x in queue:
            for g in gens:
                y=mul(g,x)
                if y not in seen:seen.add(y);queue.append(y)
        return seen
    gens=[];span={identity}
    for h in H:
        if h not in span:gens.append(h);span=close(gens)
        if len(span)==len(H):break
    comm=[mul(mul(mul(a,b),inv(a)),inv(b))for a in gens for b in gens]
    normal={mul(mul(h,c),inv(h))for h in H for c in comm}
    derived=close(normal)
    assert len(derived)==len(H)
    return dict(order=len(H),derived_order=len(derived),generators=[list(g)for g in gens])

def group_controls(perms,matrices):
    identity=tuple(range(27));mul=lambda p,q:tuple(p[q[i]]for i in range(27));inv=lambda p:tuple(p.index(i)for i in range(27))
    seen={identity};queue=[identity]
    for p in queue:
        for g in perms:
            q=mul(g,p)
            if q not in seen:seen.add(q);queue.append(q)
    assert len(seen)==960
    whole=perfect_subgroup(queue,mul,inv,identity)
    stab=perfect_subgroup([p for p in queue if p[11]==11],mul,inv,identity);assert stab['order']==60
    J=np.block([[np.zeros((2,2),int),np.eye(2,dtype=int)],[-np.eye(2,dtype=int),np.zeros((2,2),int)]])
    key=lambda M:tuple(map(int,M.flat));I=key(np.eye(4,dtype=int));mg=[np.array(M,dtype=int)for M in matrices]
    products={I:identity};todo=[I]
    for a in todo:
        for G,g in zip(mg,perms):
            b=key(G@np.array(a).reshape(4,4)%5);p=mul(g,products[a])
            if b not in products:products[b]=p;todo.append(b)
            else:assert products[b]==p
    mm=lambda a,b:key(np.array(a).reshape(4,4)@np.array(b).reshape(4,4)%5)
    mi=lambda a:key(-J@np.array(a).reshape(4,4).T@J%5)
    assert len(todo)==1920
    binary=perfect_subgroup([a for a in todo if products[a][11]==11],mm,mi,I);assert binary['order']==120
    return dict(projective_perfect=whole,spinor_point_stabilizer_perfect=stab,
        covering_spinor_point_stabilizer_perfect=binary)

def verify(d):
    old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    perms=[g['permutation']for g in old['signed_generators']];co={tuple(r['triple']):r['coefficient']for r in old['coefficient_rows']}
    rows,rhs,desc=constraints(perms,co);total=[0]*16;exponent=0
    for term in d['multiplicative_contradiction']:
        i=term['constraint_index'];k=term['integer_power']
        assert term['description']==json.loads(json.dumps(desc[i]))
        assert term['exponents']==rows[i]and term['rhs_sign_exponent']==rhs[i]
        total=[a+k*b for a,b in zip(total,rows[i])];exponent+=k*rhs[i]
    assert not any(total)and exponent%2==1
    return True

def build():
    old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text());pg=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text())
    perms=[g['permutation']for g in old['signed_generators']];co={tuple(r['triple']):r['coefficient']for r in old['coefficient_rows']}
    controls=group_controls(perms,pg['symplectic_matrix_generators'])
    rows,rhs,desc=constraints(perms,co);A=s.Matrix(rows);b=s.Matrix(rhs);vectors=[];witness=None
    for z in A.T.nullspace():
        z=z*s.ilcm(*[s.denom(x)for x in z]);z=z/s.igcd(*[int(x)for x in z]);vectors.append(z)
        if int((z.T*b)[0])%2:witness=z;break
    if witness is None:
        # Saturate the rational nullspace lattice at2. Individually primitive
        # basis vectors need not span the full integer relation lattice.
        V=s.Matrix.hstack(*vectors);values=[int((z.T*b)[0])for z in vectors]
        assert all(v%2==0 for v in values)
        eq=[(sum((int(V[i,j])%2)<<j for j in range(V.cols)),0)for i in range(V.rows)]
        eq.append((sum(((v//2)%2)<<j for j,v in enumerate(values)),1))
        comb=solve2(eq,V.cols);assert comb is not None
        witness=V*s.Matrix(comb)/2
    assert all(s.denom(x)==1 for x in witness)and A.T*witness==s.zeros(16,1)and int((witness.T*b)[0])%2
    certificate=[dict(constraint_index=i,integer_power=int(k),exponents=rows[i],rhs_sign_exponent=rhs[i],description=desc[i])for i,k in enumerate(witness)if k]
    d=dict(status='PROVED_NO_ARBITRARY_COMPLEX_MONOMIAL_DESCENT',group_controls=controls,
        constraint_shape=[210,16],multiplicative_contradiction=certificate,
        gauge_argument='For a transitive monomial representation, phases restricted to a point stabilizer form a1D character. The60-element stabilizer on the16 orbit is perfect, so its character is trivial; choosing orbit-transversal basis scalings gauges every spinor action to an unsigned permutation. The whole960 group is perfect, so the fixed singlet acts trivially. Eliminating vector-coordinate phases leaves the published multiplicative equations in16 nonzero diagonal gauge coordinates.',
        covering_argument='The corresponding120-element point stabilizer in the actual1920 cover is also perfect. Its central -I therefore acts trivially on all spinor coordinates in any such monomial representation. Cubic invariance and the singlet action force it trivial on1+10 too. Any covering representation would factor through the already excluded960 action.',
        conclusion='No assignment of arbitrary nonzero complex monomial phases realizes either the unsigned960 action or its actual1920 cover as a linear symmetry of the native45-term cubic. The nine selected equations multiply to1=-1.',
        prior='Extends the real-sign-only obstructions of w33_20261031_signed_cubic_lift.py. Monomial induction and point-stabilizer characters are standard representation theory.',
        boundary='Specific prescribed27-coordinate permutation action. Does not exclude a different carrier, nonmonomial embedding, larger common extension, or the already constructed30720 signed lift; no physical E6 or Yukawa no-go asserted.')
    verify(json.loads(json.dumps(d)));return d

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_complex_cubic_obstruction.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],len(d['multiplicative_contradiction']))
