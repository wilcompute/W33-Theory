"""TOE83/84 logical quotient versus11980 modular/integral holonomies."""
import itertools
import json
from pathlib import Path
import numpy as np
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from w33_pass11980_heisenberg_fixed_holonomies import build_module,field_basis,DIRECTIONS
from w33_20261015_toe82_native_H27_h1_character import mul

ROOT=Path(__file__).resolve().parents[1]


def inverse3(a):
    n=len(a);m=np.concatenate((a.copy()%3,np.eye(n,dtype=np.int64)),axis=1)
    for k in range(n):
        row=k+int(np.flatnonzero(m[k:,k])[0]);m[[row,k]]=m[[k,row]]
        m[k]=m[k]*pow(int(m[k,k]),-1,3)%3
        for j in range(n):
            if j!=k:m[j]=(m[j]-m[j,k]*m[k])%3
    assert np.array_equal(m[:,:n],np.eye(n,dtype=int))
    return m[:,n:]


def payload():
    acts,_,coordinates=build_module()
    prior=json.loads((ROOT/'data/w33_20261015_toe83_h27_square_css_surgery.json').read_text())
    H=list(itertools.product(range(3),repeat=3));ix={h:i for i,h in enumerate(H)}
    faces=sorted({tuple(sorted(ix[mul(g,t)] for t in ((0,0,0),d,mul(d,d)))) for d in DIRECTIONS for g in H})
    edges=sorted({e for f in faces for e in itertools.combinations(f,2)});ei={e:i for i,e in enumerate(edges)}
    squares=set()
    for rep in prior['orbit_metadata']['selected_orbit_representatives']:
        for g in H:
            pm=[ix[mul(g,h)] for h in H]
            squares.add(tuple(sorted(tuple(sorted((pm[a],pm[b]))) for a,b in rep)))
    assert len(squares)==54
    F=np.zeros((135,54),dtype=np.int64)
    for j,square in enumerate(sorted(squares)):
        adj={v:[] for edge in square for v in edge}
        for a,b in square:adj[a].append(b);adj[b].append(a)
        a=min(adj);b=min(adj[a]);walk=[a,b]
        while len(walk)<4:walk.append(next(v for v in adj[walk[-1]] if v!=walk[-2]))
        walk.append(a)
        for a,b in zip(walk,walk[1:]):F[ei[tuple(sorted((a,b)))],j]+=1 if a<b else -1
    relations=coordinates@F
    boundary=field_basis(relations,3);assert boundary.shape[1]==38
    full=boundary
    for v in np.eye(64,dtype=np.int64).T:
        candidate=np.column_stack((full,v))
        if field_basis(candidate,3).shape[1]>full.shape[1]:full=candidate
    assert full.shape==(64,64)
    Q=inverse3(full)[38:];L=full[:,38:]
    small={g:Q@a@L%3 for g,a in acts.items()}
    assert all(not (Q@a@boundary%3).any() for a in acts.values())
    for g in H:
        for h in H:assert np.array_equal(small[g]@small[h]%3,small[mul(g,h)])
    differences=[small[g]-np.eye(26,dtype=np.int64) for g in ((1,0,0),(0,1,0))]
    radical=np.eye(26,dtype=np.int64);layers=[26]
    while radical.shape[1]:
        radical=field_basis(np.concatenate([d@radical for d in differences],axis=1),3)
        layers.append(radical.shape[1]);assert len(layers)<30
    center=small[(0,0,1)]-np.eye(26,dtype=np.int64);power=np.eye(26,dtype=np.int64);ranks=[]
    for _ in range(3):power=power@center%3;ranks.append(field_basis(power,3).shape[1])
    inv_dim=26-field_basis(np.concatenate(differences),3).shape[1]
    top_dim=26-field_basis(np.concatenate(differences,axis=1),3).shape[1]
    big=np.concatenate([acts[g]-np.eye(64,dtype=int) for g in ((1,0,0),(0,1,0))]+[relations],axis=1)
    smith=smith_normal_form(s.Matrix(big.tolist()),domain=ZZ)
    factors=[abs(int(smith[i,i])) for i in range(64) if abs(int(smith[i,i]))>1]
    assert all(smith[i,i] for i in range(64))
    old=json.loads((ROOT/'data/w33_pass11980_heisenberg_fixed_holonomies.json').read_text())['explicit_holonomies_and_matter_probe']
    generators=np.array(old['character_generators_mod9']);survive=[]
    for coeff in itertools.product(range(3),range(9),range(9)):
        phase=np.array(coeff)@generators%9
        if not (phase@relations%9).any():survive.append(list(coeff))
    assert len(survive)==int(s.prod(factors))
    spectrum=old['all_243_sector_spectra'];energies={tuple(r['coefficients']):sum(r['single_particle_spectrum'][:18]) for r in spectrum}
    original_min=min(energies.values());original_winners={c for c,e in energies.items() if abs(e-original_min)<1e-9}
    allowed_min=min(energies[tuple(c)] for c in survive)
    allowed_original_winners=[c for c in survive if tuple(c) in original_winners]
    return dict(status='PASS',prior_owners=['TOE83 selected54square faces and26logicalqudits','TOE84 faithfullogicalH27 action','11980 original64module and243fixedholonomies'],
        quotient_dimension=26,F3_invariant_dimension=inv_dim,F3_coinvariant_dimension=top_dim,
        F3_radical_dimensions=layers,F3_radical_layers=[a-b for a,b in zip(layers,layers[1:])],
        center_nilpotent_power_ranks=ranks,integral_H1_coinvariant_factors=factors,
        surviving_original_243_holonomy_count=len(survive),surviving_coefficients=survive,
        selected_stable_N18_order9_survives=[0,0,2] in survive,
        all_original_N18_minimizer_count=len(original_winners),surviving_original_N18_minimizers=allowed_original_winners,
        best_surviving_N18_static_energy=allowed_min,
        generator_logical_matrices={str(g):small[g].tolist() for g in ((1,0,0),(0,1,0))},
        scope='Exact modular quotient and discrete flat-holonomy tradeoff for the selected code surgery, not physical families, clock dynamics or universal quantum computation.')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11986_logical_modular_descent.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['F3_radical_dimensions'],d['integral_H1_coinvariant_factors'],d['surviving_original_243_holonomy_count'])
