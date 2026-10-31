"""Named D5 lattice control and a general balanced-regulator index obstruction.

The finite stabilizer supplies a faithful signed SO(5) representation. The
lattice, scale, replication and Dirac regulator below are explicitly supplied.
"""
from pathlib import Path
import sys,json,itertools
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]


def d5_symbol(k,a):
    roots=np.array([tuple(s if l==i else t if l==j else 0 for l in range(5))
                    for i,j in itertools.combinations(range(5),2)
                    for s,t in itertools.product((-1,1),repeat=2)])
    # 2 sin^2 is stable at small a, unlike subtracting cos from 1.
    return float(np.sum(2*np.sin(a*(roots@np.array(k))/2)**2)/(8*a*a))


def invariant_metric(generators):
    variables=sp.symbols('q0:15');Q=sp.zeros(5);n=0
    for i in range(5):
        for j in range(i,5):Q[i,j]=Q[j,i]=variables[n];n+=1
    rows=[]
    for g in generators:
        G=sp.Matrix(g);rows.extend(list(G.T*Q*G-Q))
    A,_=sp.linear_eq_to_matrix(rows,variables)
    basis=A.nullspace()
    assert A.rank()==14 and len(basis)==1
    return dict(symmetric_form_space_dimension=1,linear_constraint_rank=14,
                nondegenerate_signature='(5,0) or (0,5), never (1,4)',
                proof='The even-sign kernel makes Q diagonal; A5 permutes all five axes transitively, so Q=cI.')


def overlap_control(M,f):
    n=len(M);U,s,Vh=np.linalg.svd(M);V=Vh.conj().T
    fs=f(s*s)
    H=np.block([[(U*fs)@U.conj().T,M],[M.conj().T,-(V*fs)@V.conj().T]])
    lam,E=np.linalg.eigh(H);gap=float(min(abs(lam)))
    assert gap>1e-8
    expected=np.sort(np.r_[-np.sqrt(fs*fs+s*s),np.sqrt(fs*fs+s*s)])
    defect=float(np.max(abs(lam-expected)));assert defect<1e-10
    sign=(E*np.sign(lam))@E.conj().T;gamma=np.diag(np.r_[np.ones(n),-np.ones(n)])
    D=np.eye(2*n)+gamma@sign
    gw=float(np.max(abs(gamma@D+D@gamma-D@gamma@D)));assert gw<1e-10
    index=int(round(-np.sign(lam).sum()/2));assert index==0
    return dict(kernel_gap=gap,index=index,GW_defect=gw,spectral_pairing_defect=defect)


def internal_e6_support(generators):
    # Twice the D5 weights: scalar, ten vector weights, sixteen even half-spin
    # weights. U(1) charges separate the standard E6 cubic sectors.
    weights=[(0,)*5];charges=[4]
    for i in range(5):
        for s in (-1,1):weights.append(tuple(2*s if j==i else 0 for j in range(5)));charges.append(-2)
    for v in itertools.product((-1,1),repeat=5):
        if sum(x<0 for x in v)%2==0:weights.append(v);charges.append(1)
    assert len(weights)==27
    triples={tuple(t) for t in itertools.combinations(range(27),3)
             if sum(charges[i] for i in t)==0 and all(sum(weights[i][j] for i in t)==0 for j in range(5))}
    assert len(triples)==45 and sum(0 in t for t in triples)==5
    lookup={(c,v):i for i,(c,v) in enumerate(zip(charges,weights))};perms=[]
    for g in generators:
        G=np.array(g)
        p=[lookup[(c,tuple(int(x) for x in G@v))] for c,v in zip(charges,map(np.array,weights))]
        assert {tuple(sorted(p[i] for i in t)) for t in triples}==triples
        perms.append(p)
    orbits=[];unused=set(range(27))
    while unused:
        orbit={min(unused)};queue=list(orbit)
        for i in queue:
            for p in perms:
                if p[i] not in orbit:orbit.add(p[i]);queue.append(p[i])
        orbits.append(sorted(orbit));unused-=orbit
    assert sorted(map(len,orbits))==[1,10,16]
    return dict(doubled_weights=weights,charges=charges,cubic_support=sorted(triples),generator_permutations=perms,
                sector_orbit_sizes=sorted(map(len,orbits)),cubic_support_sector_sizes=[5,40],
                prior='Pass11185 owns the 1+10+16 and 5+40 frame/cubic dictionary. This explicitly transports the new q=5 stabilizer to the standard unsigned weight model.',
                boundary='Cubic monomial support is preserved. A lift preserving the actual signed repository cubic, physical Yukawa coefficients and a vacuum coupling is not supplied.')


def main():
    d=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text())
    generators=d['signed_five_dimensional_generators']
    metric=invariant_metric(generators)
    k=np.array([.31,-.42,.27,.13,-.36]);target=float(k@k)
    rows=[]
    for a in (.5,.25,.125,.0625):
        value=d5_symbol(k,a);error=abs(value-target)
        assert error<=(5/6)*a*a*target*target+1e-12
        assert all(abs(d5_symbol(np.array(G)@k,a)-value)<1e-12 for G in generators)
        rows.append(dict(a=a,symbol=value,continuum_norm_squared=target,error=error,scaled_error=error/(a*a)))
    assert all(rows[i+1]['error']<rows[i]['error'] for i in range(len(rows)-1))
    sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
    from even_line_sets_gf import build
    _,_,N=build(3);rng=np.random.default_rng(20261031)
    M=N*np.exp(1j*rng.uniform(-np.pi,np.pi,N.shape))
    controls=[overlap_control(M,lambda x:.1*x-1.2),
              overlap_control(M,lambda x:.013*x*x-.2*x-.7),
              overlap_control(M,lambda x:np.sin(x)+.4)]
    # A deficient M still has paired null singular spaces, so equal block
    # sizes alone do not generate an index through zero singular values.
    Msmall=np.diag([0,0,.5,1.2,2.1]).astype(complex)
    controls.append(overlap_control(Msmall,lambda x:.1*x-1.2))
    out=dict(status='PASS_CONSTRUCTIVE_CONTROL_AND_SPECIFIC_OBSTRUCTIONS',
        internal_E6_support_control=internal_e6_support(generators),
        signed_metric=metric,lattice='Supplied scaled D5={z in Z^5: sum z_i even}; not identified with the 20 selected W(3,5) lines.',
        faithful_Lorentz_dimension_bound='At least 6 spacetime dimensions if this entire perfect finite stabilizer acts faithfully by Lorentz transformations. A finite time-orientation-preserving Lorentz group fixes a timelike vector by averaging its orbit. Perfectness forbids a nontrivial time-orientation character, so the spatial representation must be faithful and has dimension at least 5. The bound is attained by 1 plus the signed SO5 representation. This does not constrain a group acting internally or through a quotient on spacetime.',
        symbol='sigma_a(k)=(1/(8 a^2)) sum_{r in D5 roots}(1-cos(a r.k)) -> |k|^2',
        exact_error_bound='|sigma_a(k)-|k|^2| <= (5/6) a^2 |k|^4',continuum_rows=rows,
        balanced_overlap_controls=controls,
        generalized_index_theorem='For any square M and any real function f on its squared singular values, H=[f(MM*),M;M*,-f(M*M)] has eigenvalues +/-sqrt(f(s^2)^2+s^2). If H is invertible its overlap index is zero. This extends the specific linear regulator in TOE41; it does not exclude other topologies or regulator structures.',
        no_intrinsic_Wq_limit='W(3,q) point Laplacians have only 0, q^2+1, (q+1)^2. Scalar rescaling preserves the three-atom spectrum and cannot produce a Weyl-law tower. The repo already owns this obstruction.',
        boundary='No derived 3+1 spacetime, Lorentzian vacuum, nonzero native chiral index, anomaly-free chiral gauge measure, or gravity. D5 spatial locality is added. A nonzero index would require changing the balanced paired kernel, not merely replacing its scalar function f.',
        prior=['analysis/w33_20261010_toe41_w33_overlap_index_nogo.py','analysis/2026-10-29_W33_external_continuum_control.md','analysis/w33_pass11789_11792_transition_field_continuum.py'],
        literature=['https://arxiv.org/abs/hep-lat/9802011','https://doi.org/10.1103/PhysRevD.25.2649'])
    (ROOT/'data/w33_20261031_continuum_chirality.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
