"""Balanced point-source E8 Higgs data, exact relative complexes and cubic gate.

This is an explicit sourced Abelian gauge-sector construction and a strict
relative-cup diagnostic, not a complete compact G2/M-theory vacuum.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import Counter
import json
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
Q=np.array([[2,-1,-1,0],[-1,2,-1,0],[0,-1,2,-1],[-1,0,0,1]],dtype=np.int64)
W=[np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1]),np.array([-1,-1,-1])]


def rank_mod(A,p=101):
    A=np.array(A,dtype=np.int64,copy=True)%p
    row=0
    for col in range(A.shape[1]):
        inds=np.flatnonzero(A[row:,col])
        if not len(inds):continue
        j=row+int(inds[0]);A[[row,j]]=A[[j,row]]
        A[row]=A[row]*pow(int(A[row,col]),-1,p)%p
        idx=np.flatnonzero(A[:,col]);idx=idx[idx!=row]
        A[idx]=(A[idx]-A[idx,col,None]*A[row])%p
        row+=1
        if row==len(A):break
    return row


def sphere_and_holes():
    # Barycentric subdivision of boundary of the oriented 4-simplex.
    faces=[a for k in range(1,5) for a in combinations(range(5),k)]
    ids={a:i for i,a in enumerate(faces)}
    chain={}
    for missing in range(5):
        original=tuple(i for i in range(5) if i!=missing)
        for perm in permutations(original):
            tet=tuple(ids[tuple(sorted(perm[:k]))] for k in range(1,5))
            parity=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
            chain[tet]=(-1)**missing*parity
    def pick(start,chosen,used):
        if len(chosen)==4:return chosen
        for i in range(start,len(tets)):
            if not(set(tets[i])&used):
                out=pick(i+1,chosen+[tets[i]],used|set(tets[i]))
                if out:return out
        return None
    tets=sorted(chain);holes=pick(0,[],set())
    assert holes and len(set(v for t in holes for v in t))==16
    def boundary(c):
        ans=Counter()
        for tet,n in c.items():
            for j in range(4):ans[tet[:j]+tet[j+1:]]+=n*(-1)**j
        return {f:n for f,n in ans.items() if n}
    assert boundary(chain)=={}
    exterior={t:n for t,n in chain.items() if t not in holes}
    bd=boundary(exterior)
    assert len(bd)==16 and set(abs(n) for n in bd.values())=={1}
    return chain,holes,bd


def relative_betti(chain,holes,residues,prime=101):
    # Fill a source ball when this charged profile has zero residue there.
    # An artificial absolute hole would introduce spurious degree-two modes.
    tets=[t for t in chain if not any(t==holes[j] and residues[j]!=0 for j in range(4))]
    simplices=[sorted({f for t in tets for f in combinations(t,k+1)}) for k in range(4)]
    relative=[set() for _ in range(4)]
    for j,r in enumerate(residues):
        if r<0:
            for k in range(3):relative[k].update(combinations(holes[j],k+1))
    cells=[[f for f in fs if f not in relative[k]] for k,fs in enumerate(simplices)]
    Ds=[]
    for k in range(3):
        index={f:i for i,f in enumerate(cells[k])}
        D=np.zeros((len(cells[k+1]),len(cells[k])),dtype=np.int64)
        for row,f in enumerate(cells[k+1]):
            for j in range(k+2):
                face=f[:j]+f[j+1:]
                if face in index:D[row,index[face]]=(-1)**j
        Ds.append(D)
    assert np.all(Ds[1]@Ds[0]==0) and np.all(Ds[2]@Ds[1]==0)
    ranks=[rank_mod(D,prime) for D in Ds]
    bs=[len(cells[k])-(ranks[k-1] if k else 0)-(ranks[k] if k<3 else 0) for k in range(4)]
    m=sum(r<0 for r in residues);p=sum(r>0 for r in residues)
    assert bs==[0,m-1,p-1,0],(residues,bs)
    return bs


def sector_census():
    assert np.all(Q.sum(0)==0) and np.all(Q.sum(1)==0) and s.Matrix(Q).rank()==3
    e=np.eye(4,dtype=np.int64)
    sectors=[]
    for label,rep,weight in [('16_'+str(i+1),16,e[i]) for i in range(4)]+[
        ('10_'+str(i+1)+str(j+1),10,e[i]+e[j]) for i,j in combinations(range(4),2)]+[
        ('S_'+str(i+1)+str(j+1),1,e[i]-e[j]) for i,j in combinations(range(4),2)]:
        r=Q@weight;m=int(sum(r<0));p=int(sum(r>0))
        assert m and p
        charge=sum((int(weight[i])*W[i] for i in range(4)),np.zeros(3,dtype=np.int64))
        sectors.append({'label':label,'rep_dimension':rep,'SU4_charge':charge.tolist(),
                        'residues':r.tolist(),'b1':m-1,'b2':p-1})
    # Choose one orientation for real 10 pairs to avoid double counting;
    # enumerate all six SU4 weights for 10 with H1 only.
    fields=[]
    for a in sectors:
        if a['rep_dimension']==10:
            for _ in range(a['b1']):fields.append((10,a['SU4_charge'],a['label']))
        else:
            for _ in range(a['b1']):fields.append((a['rep_dimension'],a['SU4_charge'],a['label']))
            for _ in range(a['b2']):fields.append((a['rep_dimension'],[-x for x in a['SU4_charge']],'conj_'+a['label']))
    # 16 conjugates are absent for this Q; singlets conjugated as above.
    dims=Counter(d for d,q,label in fields)
    assert dims=={16:3,10:5,1:8}
    grav=sum((d*np.array(q) for d,q,label in fields),np.zeros(3,dtype=np.int64))
    mixed=sum(({16:2,10:1,1:0}[d]*np.array(q) for d,q,label in fields),np.zeros(3,dtype=np.int64))
    cubic=np.zeros((3,3,3),dtype=np.int64)
    for d,q,label in fields:cubic+=d*np.einsum('i,j,k->ijk',q,q,q)
    return sectors,fields,{'chiral_Spin10_16':3,'conjugate_16':0,'chiral_Spin10_10':5,
      'charged_singlet_fields':8,'complex_gauge_components':sum(d for d,q,l in fields),
      'gravitational_U1_trace':grav.tolist(),'Spin10_squared_U1_trace_T10_1':mixed.tolist(),
      'U1_cubic_tensor':cubic.tolist(),'unbroken_gauge_Lie_algebra':'so10+u1^3 (dimension48)',
      'SM_singlet_D_chi_obstruction':'All N in chiral16 have chi=-5; tens have no SM singlet; SU4 root singlets have chi=0. At zero FI, no nonzero N-only SM-preserving D-flat GUT breaking.'}


def root_and_anomaly_control(census):
    from toe_20261118_E8_H27_wire_index_parity import e8_roots_twice
    U=s.Matrix([[1,1,-1],[1,-1,1],[1,-1,-1]])
    B=U.inv()  # sends the first three even D3 halfspin weights to e1,e2,e3
    assert B*s.Matrix([-1,-1,1])==s.Matrix([-1,-1,-1])
    total=0;grav=s.zeros(3,1);mixed=s.zeros(3,1);cube=s.zeros(27,1)
    for root in e8_roots_twice():
        q=B*s.Matrix(root[5:])
        assert all(v.q==1 for v in q)
        if q==s.zeros(3,1):continue
        residues=s.Matrix(Q[:,:3])*q
        mult=sum(int(bool(v<0)) for v in residues)-1
        assert mult>=0
        total+=mult;grav+=mult*q
        mixed+=mult*s.Rational(root[0],2)**2*q/2
        for n,(i,j,k) in enumerate(product(range(3),repeat=3)):cube[n]+=mult*q[i]*q[j]*q[k]
    assert total==census['complex_gauge_components']==106
    assert list(grav)==census['gravitational_U1_trace']
    assert list(mixed)==census['Spin10_squared_U1_trace_T10_1']
    assert list(cube)==list(s.Matrix(np.array(census['U1_cubic_tensor']).reshape(27,1)))
    a,b,c=s.symbols('a b c');v=[a,b,c]
    poly=s.expand(sum(cube[n]*v[i]*v[j]*v[k] for n,(i,j,k) in enumerate(product(range(3),repeat=3))))
    restriction=s.factor(poly.subs(a,-(b+c)/2))
    assert s.expand(restriction-s.Rational(3,2)*(b-5*c)*(b+c)*(5*b-c))==0
    lines=[[-3,5,1],[0,-1,1],[-3,1,5]]
    for line in lines:
        assert sum(x*y for x,y in zip(line,[2,1,1]))==0
        assert poly.subs(dict(zip(v,line)))==0
    return {'E8_root_space_H1_complex_components':total,
            'root_trace_matches_sector_anomaly_sums':True,
            'cubic_U1_polynomial':str(poly),
            'cubic_restricted_to_mixed_anomaly_kernel':str(restriction),
            'anomaly_free_individual_U1_directions':lines,
            'no_two_dimensional_anomaly_free_subspace_without_inflow':True,
            'scope':'Massless charged-sector perturbative anomalies only, no boundary inflow or quantum global anomaly computed'}


def graph_classification():
    arcs=list(permutations(range(4),2));classes=Counter();n=0;distinct=0
    for edges in combinations(arcs,7):
        A=np.zeros((4,4),dtype=np.int64)
        for i,j in edges:A[i,j]=1
        if not np.array_equal(A.sum(0),A.sum(1)):continue
        L=np.diag(A.sum(1))-A
        if rank_mod(L)!=3:continue
        n+=1
        key=min(tuple(A[np.ix_(perm,perm)].ravel()) for perm in permutations(range(4)))
        classes[key]+=1
        if sorted((A.sum(0)-1).tolist())==[0,1,1,1]:distinct+=1
    assert n and distinct and sum(classes.values())==n
    return {'simple_7_arc_balanced_rank3_labeled_graphs':n,'isomorphism_classes':len(classes),
            'class_orbit_sizes':sorted(classes.values()),'distinct_three_family_weight_models':distinct,
            'minimum_source_points_for_rank3':4,
            'minimal_source_mirrorfree_three_implies':'one positive residue in each row/column, seven negative residues and five zero residues; Q is a balanced weighted directed Laplacian',
            'dense_source_parity':'if all four profiles have nonzero residues at every source, total16 index is even; odd3 requires a zero-residue stratum'}


def cup_gate(chain,holes,sectors):
    M={t:n for t,n in chain.items() if t not in holes}
    eta=[{v:int(v in h) for v in range(30)} for h in holes]
    def cup_integral(fs):
        return sum(n*(fs[0][t[1]]-fs[0][t[0]])*(fs[1][t[2]]-fs[1][t[1]])*(fs[2][t[3]]-fs[2][t[2]]) for t,n in M.items())
    # All degree-one relative classes on this rational homology sphere
    # are boundary-connecting classes. These vertex potentials represent them.
    values=[cup_integral([eta[i],eta[j],eta[k]]) for i,j,k in product(range(4),repeat=3)]
    assert values==[0]*64
    return {'oriented_3_simplices_full_sphere':len(chain),'exterior_3_simplices':len(M),
            'disjoint_source_ball_vertices':[list(h) for h in holes],
            'exact_Alexander_Whitney_triple_integrals_checked':64,'nonzero_integrals':0,
            'analytic_reason':'Each H1(M,A) with H1(M)=0 has representatives that are linear combinations of radial d(collar cutoff) forms; collars disjoint, all such pair wedges vanish',
            'conditional_cubic_result':'If the full bulk cubic descends to this relative de Rham cup product with no defect/boundary correction, it is zero even when gauge charges allow a full-rank texture',
            'not_claimed':'No blanket no-go for singular M-theory Yukawas, defect interactions, nontrivial flat systems, nonfactorized covers or all M2 corrections'}


def run():
    sectors,fields,census=sector_census();chain,holes,bd=sphere_and_holes()
    controls=[]
    for sector in sectors:
        for prime in (101,103):
            bs=relative_betti(chain,holes,sector['residues'],prime)
            assert bs[1:3]==[sector['b1'],sector['b2']]
        controls.append({'label':sector['label'],'Betti':bs})
    a,b,c=s.symbols('a b c');Y=s.Matrix([[0,a,b],[a,0,c],[b,c,0]])
    assert Y.det()==2*a*b*c
    result={'status':'PASS','scope':'sourced Abelian E8 gauge-sector data and conditional bulk-cup gate, not a complete physical vacuum',
      'source_matrix':Q.tolist(),'row_trace_zero':True,'column_total_charge_zero':True,
      'source_rank':3,'harmonic_background':'f_i(x)=sum_j Q_ji G_S3(dist(x,p_j)); four distinct supplied poles; sum_i f_i=0 and each f_i harmonic away from poles because sum_j Q_ji=0',
      'Green_function':'G(chi)=(pi-chi)cot(chi)/(4*pi^2), Delta G=1/(2*pi^2) away from pole',
      'sectors':sectors,'census_and_obstructions':census,'root_and_anomaly_control':root_and_anomaly_control(census),'graph_classification':graph_classification(),
      'exact_relative_complex_controls':controls,'cup_gate':cup_gate(chain,holes,sectors),
      'gauge_allowed_texture':{'families':['16_1','16_2','16_3'],'Higgs_weights':['10_34','10_24','10_14'],
       'matrix':[['0','a','b'],['a','0','c'],['b','c','0']],'formal_determinant':str(Y.det()),
       'warning':'Gauge selection rules permit this texture; coefficients are not computed or proven nonzero; strict relative-cup model instead gives zero'},
      'limitations':['four pole positions and quantized residue matrix supplied, not predicted',
       'zero-residue holes filled separately in each charged-sector complex',
       'extra U1 anomalies, physical source completion, Einstein equations and moduli not solved',
       'strict bulk cup product may omit necessary singular-domain, defect or boundary terms; comparison to full theory remains open',
       'no physical Standard Model vacuum or measured parameter prediction']}
    p=ROOT/'data/toe_20261119_balanced_source_E8_cup_gate.json';p.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print('PASS balanced4-source rank3; chiral16=3, mirrors0, tens5, singlets8; strict relative-cup cubic zero')
    print(json.dumps(result['graph_classification']))
    return result

if __name__=='__main__':run()
