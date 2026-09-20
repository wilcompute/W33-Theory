"""Integral handle transport and metric-dependent harmonic storage on the Lutz surface.
Prior: w33_genus_six_execution; Hodge method is classical (BT994 and DEC).
"""
from pathlib import Path
from collections import defaultdict, deque
import json, hashlib, os, tempfile
import numpy as np
import sympy as s
from w33_genus_six_execution import orient, incidence, validate_surface, HandleVM, integral
from w33_k12_genus_polarization import darboux
ROOT=Path(__file__).resolve().parents[1]


def chains(faces):
    reference=tuple(faces[0]); faces=orient(faces)
    first=faces[0]
    if reference not in [first,first[1:]+first[:1],first[2:]+first[:2]]:
        faces=[(f[0],f[2],f[1]) for f in faces]
    topo=validate_surface(faces)
    vertices=sorted({v for f in faces for v in f}); vi={v:i for i,v in enumerate(vertices)}
    edges=sorted(incidence(faces)); ei={e:i for i,e in enumerate(edges)}
    d1=s.zeros(len(vertices),len(edges)); d2=s.zeros(len(edges),len(faces))
    adj=defaultdict(list)
    for j,(a,b) in enumerate(edges):
        d1[vi[a],j]=-1;d1[vi[b],j]=1;adj[a].append((b,j));adj[b].append((a,j))
    for j,f in enumerate(faces):
        for a,b in zip(f,f[1:]+f[:1]):d2[ei[tuple(sorted((a,b)))],j]=1 if a<b else -1
    paths={vertices[0]:s.zeros(len(edges),1)};queue=deque(paths);tree=[]
    while queue:
        a=queue.popleft()
        for b,e in adj[a]:
            if b not in paths:
                paths[b]=paths[a].copy();paths[b][e]+=1 if a<b else -1;tree.append(e);queue.append(b)
    chords=[e for e in range(len(edges)) if e not in tree]
    C=s.zeros(len(edges),len(chords))
    for j,e in enumerate(chords):
        a,b=edges[e];C[:,j]=paths[a]-paths[b];C[e,j]+=1
    ef=incidence(faces);dual=defaultdict(list)
    for e in chords:
        (a,_),(b,_)=ef[edges[e]];dual[a].append((b,e));dual[b].append((a,e))
    seen={0};queue=deque([0]);cotree=[]
    while queue:
        a=queue.popleft()
        for b,e in dual[a]:
            if b not in seen:seen.add(b);queue.append(b);cotree.append(e)
    free=[e for e in chords if e not in cotree];cols=list(range(1,len(faces)))
    R=d2.extract(cotree,cols);assert abs(R.det())==1
    H=s.zeros(len(free),len(edges))
    for j,e in enumerate(free):H[j,e]=1
    correction=-d2.extract(free,cols)*R.inv()
    for i in range(len(free)):
        for j,e in enumerate(cotree):H[i,e]=correction[i,j]
    C=C[:,[chords.index(e) for e in free]]
    cup=s.zeros(len(free))
    for f in faces:
        a,b,c=sorted(f);sign=1 if tuple(f) in [(a,b,c),(b,c,a),(c,a,b)] else -1
        cup+=sign*H[:,ei[(a,b)]]*H[:,ei[(b,c)]].T
    assert d1*C==s.zeros(len(vertices),len(free)) and H*C==s.eye(len(free))
    assert H*d2==s.zeros(len(free),len(faces)) and cup.T==-cup and cup.det()==1
    return faces,edges,d1,d2,H,C,-cup.inv()


def hodge_audit():
    prior=json.loads((ROOT/'analysis/w33_genus_six_execution.json').read_text())['surface']
    d1=s.Matrix(prior['d1']);d2=s.Matrix(prior['d2']);C=s.Matrix(prior['lattice_to_cycles'])
    # Exact cycle representative of minimum Euclidean edge norm in each H1 class.
    B=d2[:,1:];P=s.eye(66)-B*(B.T*B).inv()*B.T;Q=P*C
    assert d1*Q==s.zeros(12) and d2.T*Q==s.zeros(44,12)
    assert s.Matrix(prior['homology_projection'])*Q==s.Matrix(prior['homology_projection'])*C
    assert Q.rank()==12
    projector=Q*(Q.T*Q).inv()*Q.T
    assert projector**2==projector and projector.T==projector
    L=d1.T*d1+d2*d2.T;assert L*projector==s.zeros(66)
    # A second positive edge metric changes representatives, but not periods/classes.
    M=s.diag(*[1+i%3 for i in range(66)])
    Q2=(s.eye(66)-B*(B.T*M*B).inv()*B.T*M)*C
    assert d2.T*M*Q2==s.zeros(44,12) and d1*Q2==s.zeros(12)
    assert s.Matrix(prior['homology_projection'])*(Q2-Q)==s.zeros(12)
    assert Q2!=Q
    z=s.Symbol('lambda');poly=(d2.T*d2).charpoly(z).as_expr()
    rest=s.cancel(poly/(z*(z*z-4*z+2)**2));assert rest.is_polynomial(z)
    intervals=s.Poly(rest,z).intervals(eps=s.Rational(1,10**8))
    assert all(a>s.Rational(586,1000) for (a,b),multiplicity in intervals)
    assert d1*d1.T==12*s.eye(12)-s.ones(12)
    # Projection rejects exact and coexact corruption, but cannot reject harmonic errors.
    assert projector*d1.T==s.zeros(66,12) and projector*d2==s.zeros(66,44)
    assert projector*Q[:,0]==Q[:,0]
    lam=np.linalg.eigvalsh(np.array(L,dtype=float));gap=float(min(x for x in lam if x>1e-8))
    def rational(A):return [[str(x) for x in A.row(i)] for i in range(A.rows)]
    return {'harmonic_dimension':12,'positive_combinatorial_gap':gap,'exact_gap':'2-sqrt(2)',
            'face_laplacian_characteristic_polynomial':str(s.factor(poly)),
            'exact_and_coexact_errors_rejected_harmonic_errors_survive':True,
            'harmonic_lattice_cycles':rational(Q),'harmonic_gram':rational(Q.T*Q),
            'second_metric_changes_representatives_not_classes':True,
            'scope':'Declared discrete inner products; no induced smooth conformal structure or physical mass'}


class DurableSurface:
    def __init__(self,faces,cycles,state):
        self.faces=faces;self.cycles=s.Matrix(cycles);self.state=list(state);self.receipts=[];self.check()
    def check(self):
        _,_,d1,_,H,_,K=chains(self.faces);n=len(self.state)
        assert n==self.cycles.cols==H.rows and d1*self.cycles==s.zeros(d1.rows,n)
        assert (H*self.cycles).det() in (-1,1)
        assert (H*self.cycles).T*K*(H*self.cycles)==s.diag(*([s.Matrix([[0,1],[-1,0]])]*(n//2)))
    def allocate(self):
        oldfaces,oldedges,_,_,_,_,_=chains(self.faces);oldC=self.cycles.copy();oldstate=list(self.state)
        vm=HandleVM(self.faces);vm.allocate()
        reference=oldfaces[1]
        shared=next(f for f in vm.faces if set(f)==set(reference))
        if tuple(reference) not in [tuple(shared),tuple(shared[1:]+shared[:1]),tuple(shared[2:]+shared[:2])]:
            vm.faces=[(f[0],f[2],f[1]) for f in vm.faces]
        newfaces,edges,d1,d2,H,C,K=chains(vm.faces)
        I=s.zeros(len(edges),len(oldedges));lookup={e:i for i,e in enumerate(edges)}
        for i,e in enumerate(oldedges):I[lookup[e],i]=1
        transported=I*oldC;A=H*transported;O=A.T*K*A
        assert O==s.diag(*([s.Matrix([[0,1],[-1,0]])]*(len(oldstate)//2)))
        candidates=C-transported*O.inv()*A.T*K
        pair=None
        for i in range(candidates.cols):
            for j in range(i+1,candidates.cols):
                u,v=candidates[:,i],candidates[:,j];p=((H*u).T*K*(H*v))[0]
                if abs(p)==1:pair=(u,v*p);break
            if pair:break
        assert pair is not None
        self.faces=newfaces;self.cycles=transported.row_join(pair[0]).row_join(pair[1]);self.state += [0,0]
        self.receipts.append({'faces':oldfaces,'cycles':integral(oldC),'state':oldstate})
        self.check()
    def free(self):
        if not self.receipts or any(self.state[-2:]):raise ValueError('missing receipt or live handle')
        r=self.receipts.pop();self.faces=r['faces'];self.cycles=s.Matrix(r['cycles']);self.state=self.state[:-2];self.check()
    def save(self,path):
        self.check();payload={'faces':self.faces,'cycles':integral(self.cycles),'state':self.state,'receipts':self.receipts}
        raw=json.dumps(payload,sort_keys=True,separators=(',',':'));envelope={'sha256':hashlib.sha256(raw.encode()).hexdigest(),'payload':payload}
        path=Path(path);temporary=path.with_suffix('.pending')
        with temporary.open('w') as f:json.dump(envelope,f);f.flush();os.fsync(f.fileno())
        os.replace(temporary,path)
        fd=os.open(path.parent,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
    @classmethod
    def recover(cls,path):
        e=json.loads(Path(path).read_text());r=e['payload'];raw=json.dumps(r,sort_keys=True,separators=(',',':'))
        if hashlib.sha256(raw.encode()).hexdigest()!=e['sha256']:raise ValueError('snapshot checksum mismatch')
        obj=cls(r['faces'],r['cycles'],r['state']);obj.receipts=r['receipts'];return obj


def transport_audit():
    p=json.loads((ROOT/'analysis/w33_genus_six_execution.json').read_text())['surface']
    vm=DurableSurface(p['oriented_faces'],p['symplectic_cycles'],[i%3 for i in range(12)])
    original=list(vm.state);vm.allocate();vm.state[-2:]=[1,2]
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/'snapshot.json';vm.save(path);recovered=DurableSurface.recover(path)
        assert recovered.state==vm.state and recovered.cycles==vm.cycles
        try:recovered.free()
        except ValueError:pass
        else:raise AssertionError('live state deletion')
        recovered.state[-2:]=[0,0];recovered.free();assert recovered.state==original
        # Incomplete next write does not replace committed snapshot.
        path.with_suffix('.pending').write_text('{');assert DurableSurface.recover(path).state==vm.state
        e=json.loads(path.read_text());e['payload']['state'][0]+=1;path.write_text(json.dumps(e))
        try:DurableSurface.recover(path)
        except ValueError:pass
        else:raise AssertionError('corrupt state accepted')
    return {'genus_trace':[6,7,6],'transported_logical_generators':12,'new_generators':2,
            'symplectic_pairing_preserved':True,'snapshot_recovery':True,'partial_write_ignored':True,
            'corrupt_snapshot_rejected':True,'live_free_rejected':True,
            'scope':'Single-writer atomic snapshot; unkeyed checksum detects corruption, not malicious rewriting'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    r={'status':'PASS','hodge':hodge_audit(),'transport':transport_audit()}
    if args.write:Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v if k!='hodge' else {x:y for x,y in v.items() if x not in ('harmonic_lattice_cycles','harmonic_gram')} for k,v in r.items()},indent=2))
