#!/usr/bin/env python3
"""Pass 1351: literal projective layers and minimal resolution prefixes.

This works in the actual basic algebra e H(F_p) e cut from the frozen
26-dimensional Hecke multiplication tensor.  It does not infer module data
from the associated-graded quiver presentation.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass1330_1334_modular_triality_cycle_atlas as old
import w33_pass1345_1349_support as support

OUT=DATA/'w33_pass1351_projective_resolutions.json'
REQUESTED_DEPTH=10
MAX_COVER_DIMENSION=768


def rref(rows,p,ncols):
    A=[[int(x)%p for x in row] for row in rows]
    m=len(A); r=0; piv=[]
    for c in range(ncols):
        q=next((i for i in range(r,m) if A[i][c]),None)
        if q is None: continue
        A[r],A[q]=A[q],A[r]
        inv=pow(A[r][c],-1,p); A[r]=[(inv*x)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]; A[i]=[(A[i][j]-z*A[r][j])%p for j in range(ncols)]
        piv.append(c); r+=1
        if r==m: break
    return A[:r],piv


def span(rows,p,ncols): return rref(rows,p,ncols)[0]


def nullspace(rows,p,ncols):
    R,piv=rref(rows,p,ncols); free=[i for i in range(ncols) if i not in piv]; out=[]
    for f in free:
        v=[0]*ncols; v[f]=1
        for i,c in enumerate(piv): v[c]=(-R[i][f])%p
        out.append(v)
    return out


def complement(super_rows,sub_rows,p,ncols):
    B=span(sub_rows,p,ncols); answer=[]; r=len(B)
    for v in span(super_rows,p,ncols):
        C=span(B+[v],p,ncols)
        if len(C)>r: answer.append(v); B=C; r+=1
    return answer


def add_vectors(vectors,coeffs,p):
    if not vectors: return []
    out=[0]*len(vectors[0])
    for c,v in zip(coeffs,vectors):
        if c%p: out=[(a+c*b)%p for a,b in zip(out,v)]
    return out


def coords(vector,basis,p):
    if not basis:
        assert not any(int(x)%p for x in vector); return []
    return support.solve_field([list(x) for x in zip(*basis)],[int(x)%p for x in vector],p)


class BasicAlgebra:
    def __init__(self,p):
        self.p=p
        lifts=support.orthogonal_primitive_lifts(p)
        seen=set(); self.labels=[]; self.ambient_idempotents=[]
        for label,e,component,_ in lifts:
            if component not in seen:
                seen.add(component); self.labels.append(label); self.ambient_idempotents.append(e)
        total=[0]*26
        for e in self.ambient_idempotents: total=[(a+b)%p for a,b in zip(total,e)]
        self.ambient_identity=total
        sandwiched=[support.mul(support.mul(total,b,p),total,p) for b in support.BASIS]
        self.ambient_basis=old.span(sandwiched,p)
        self.dim=len(self.ambient_basis)
        self.basis=[[int(i==j) for i in range(self.dim)] for j in range(self.dim)]
        self.idempotents=[coords(e,self.ambient_basis,p) for e in self.ambient_idempotents]
        assert add_vectors(self.idempotents,[1]*len(self.idempotents),p)==coords(total,self.ambient_basis,p)
        self.mult=[]
        for x in self.ambient_basis:
            row=[]
            for y in self.ambient_basis:
                row.append(coords(support.mul(x,y,p),self.ambient_basis,p))
            self.mult.append(row)
        radical=old.span(support.quotient_record(p)['radical_basis'],p)
        self.radical=old.span([coords(support.mul(support.mul(total,r,p),total,p),self.ambient_basis,p) for r in radical],p)
        self.projectives=[old.span([self.mul(e,b) for b in self.basis],p) for e in self.idempotents]

    def mul(self,x,y):
        p=self.p; out=[0]*self.dim
        for i,a in enumerate(x):
            if not a%p: continue
            for j,b in enumerate(y):
                if not b%p: continue
                for k,c in enumerate(self.mult[i][j]): out[k]=(out[k]+a*b*c)%p
        return out


class FreeModule:
    def __init__(self,A,types):
        self.A=A; self.types=list(types); self.offsets=[]; self.dim=0
        for t in self.types:
            self.offsets.append(self.dim); self.dim+=len(A.projectives[t])

    def right_mul(self,v,a):
        A=self.A; p=A.p; out=[0]*self.dim
        for s,t in enumerate(self.types):
            P=A.projectives[t]; off=self.offsets[s]; coeff=v[off:off+len(P)]
            if not any(coeff): continue
            x=add_vectors(P,coeff,p); y=A.mul(x,a); yc=coords(y,P,p)
            for i,c in enumerate(yc): out[off+i]=(out[off+i]+c)%p
        return out

    def project_vertex(self,v,j): return self.right_mul(v,self.A.idempotents[j])


def module_rad(F,M):
    return span([F.right_mul(m,r) for m in M for r in F.A.radical],F.A.p,F.dim)


def vertex_dimensions(F,M):
    return [len(span([F.project_vertex(m,j) for m in M],F.A.p,F.dim)) for j in range(len(F.A.idempotents))]


def top_generators(F,M):
    A=F.A; p=A.p; MJ=module_rad(F,M); gens=[]; types=[]
    for j in range(len(A.idempotents)):
        Mj=span([F.project_vertex(m,j) for m in M],p,F.dim)
        Nj=span([F.project_vertex(m,j) for m in MJ],p,F.dim)
        for g in complement(Mj,Nj,p,F.dim): gens.append(g); types.append(j)
    assert len(span(MJ+gens,p,F.dim))==len(span(M,p,F.dim))
    return gens,types


def projective_cover_from_generators(F,M,gens,types):
    p=F.A.p; P=FreeModule(F.A,types); images=[]
    for s,t in enumerate(types):
        for a in F.A.projectives[t]: images.append(F.right_mul(gens[s],a))
    matrix=[list(row) for row in zip(*images)] if images else [[] for _ in range(F.dim)]
    kernel=nullspace(matrix,p,P.dim) if P.dim else []
    assert len(span(images,p,F.dim))==len(span(M,p,F.dim))
    return P,span(kernel,p,P.dim)


def full_basis(F): return [[int(i==j) for i in range(F.dim)] for j in range(F.dim)]


def socle_closure(F,S):
    """Return {m in F: m*J subset S}."""
    p=F.A.p; n=F.dim; S=span(S,p,n)
    Q=complement(full_basis(F),S,p,n); combined=S+Q
    product_columns=[]
    for basis_vector in full_basis(F):
        col=[]
        for r in F.A.radical:
            c=coords(F.right_mul(basis_vector,r),combined,p); col+=c[len(S):]
        product_columns.append(col)
    equations=[list(row) for row in zip(*product_columns)] if product_columns and product_columns[0] else []
    return span(nullspace(equations,p,n),p,n)


def projective_layers(A,i):
    F=FreeModule(A,[i]); current=full_basis(F); radical=[]
    while current:
        nxt=module_rad(F,current); a=vertex_dimensions(F,current); b=vertex_dimensions(F,nxt)
        radical.append([x-y for x,y in zip(a,b)]); current=nxt
    socle=[]; current=[]
    while len(current)<F.dim:
        nxt=socle_closure(F,current); a=vertex_dimensions(F,nxt); b=vertex_dimensions(F,current)
        socle.append([x-y for x,y in zip(a,b)]); current=nxt
    return radical,socle


def module_sha(rows,p,ncols):
    canonical=span(rows,p,ncols)
    raw=';'.join(','.join(map(str,row)) for row in canonical).encode()
    return hashlib.sha256(raw).hexdigest()


def resolution(A,i,steps=REQUESTED_DEPTH,max_cover_dimension=MAX_COVER_DIMENSION):
    F=FreeModule(A,[i]); M=module_rad(F,full_basis(F)); records=[]
    records.append({'syzygy':0,'module_dimension':1,'cover_multiplicities':[int(j==i) for j in range(len(A.labels))],'cover_dimension':F.dim,'next_syzygy_dimension':len(M)})
    for n in range(1,steps+1):
        rec={'syzygy':n,'module_dimension':len(M),'ambient_projective_types':F.types,'module_sha256':module_sha(M,A.p,F.dim)}
        if not M:
            rec['projective']=True; records.append(rec); break
        gens,types=top_generators(F,M); counts=Counter(types); cover_dimension=sum(len(A.projectives[t]) for t in types)
        rec['cover_multiplicities']=[counts.get(j,0) for j in range(len(A.labels))]; rec['cover_dimension']=cover_dimension
        if cover_dimension>max_cover_dimension:
            rec['kernel_not_materialized']='exact cover exceeds declared dimension ceiling'; rec['dimension_ceiling']=max_cover_dimension; records.append(rec); break
        P,K=projective_cover_from_generators(F,M,gens,types); rec['next_syzygy_dimension']=len(K)
        records.append(rec); F,M=P,K
    return records


def main(write=True):
    canonical=json.loads((DATA/'w33_pass1345_modular_basic_algebras.json').read_text())
    previous=json.loads((DATA/'w33_pass1351_projective_layers.json').read_text())
    records={}
    for p in (2,3,5):
        A=BasicAlgebra(p); key=str(p); expected=canonical['records'][key]
        assert A.dim==expected['basic_algebra_dimension']
        assert A.labels==expected['quiver_and_associated_graded_relations']['vertices']
        assert [len(x) for x in A.projectives]==[sum(row) for row in expected['cartan_matrix']]
        radical=[]; socle=[]
        for i in range(len(A.labels)):
            r,s=projective_layers(A,i); radical.append(r); socle.append(s)
        assert radical==previous['records'][key]['radical_layers']; assert socle==previous['records'][key]['socle_layers']
        resolutions=[resolution(A,i) for i in range(len(A.labels))]
        records[key]={'vertices':A.labels,'basic_algebra_dimension':A.dim,'radical_dimension':len(A.radical),'projective_dimensions':[len(x) for x in A.projectives],'radical_layers':radical,'socle_layers':socle,'minimal_projective_resolution_prefixes':resolutions,'requested_resolution_depth':REQUESTED_DEPTH,'max_cover_dimension':MAX_COVER_DIMENSION,'computed_resolution_depths':[len(x)-1 for x in resolutions]}
    result={'schema':'w33.pass1351.literal_projective_resolutions.v2','status':'PASS','boundary':'Computed in the actual basic algebra e H(F_p) e from the frozen 26-dimensional multiplication tensor, not from the associated-graded presentation. Every stored cover and kernel is exact. A prefix stops before kernel construction when the next exact projective cover exceeds the declared dimension ceiling; no unproved periodic or infinite continuation is asserted.','records':records,'checks':{'actual_basic_algebra_used':True,'previous_radical_layers_reproduced':True,'previous_socle_layers_reproduced':True,'minimal_covers_computed_from_module_tops':True,'growth_boundary_explicit':True}}
    if write: OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','requested_depth':REQUESTED_DEPTH,'max_cover_dimension':MAX_COVER_DIMENSION,'computed_depths':{p:r['computed_resolution_depths'] for p,r in records.items()}},indent=2)); return result

if __name__=='__main__': main()
