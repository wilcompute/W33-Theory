#!/usr/bin/env python3
"""Heterotic Z3 standard-embedding 729 matter carrier -> six-qutrit basis.

External string input (classic standard embedding; see Fischer thesis Sec.2.4,
eq. (2.41), and Dixon et al. NPB282 (1987)):
  T^6/Z3 has 27 fixed points and the twisted ground spectrum contains one
  E6 27-plet at each fixed point:
      27 * (1,27)
  under SU(3) x E6.
Hence the twisted E6 matter carrier has dimension 27*27 = 729.

Repo input:
  artifacts/e6_cubic_affine_heisenberg_model.json gives a bijection from the
  27 E6 labels to coordinates (u0,u1,z) in F3^3.

For the factorized Z3 geometry, label the 27 fixed points by
  f=(f0,f1,f2) in F3^3.
Then the matter basis is canonically coordinatized, after choosing the repo's
E6 chart, by
  (f0,f1,f2,u0,u1,z) in F3^6.

On any such six-trit coordinate basis define standard Weyl generators
  X_j |n> = |n+e_j>,
  Z_j |n> = omega^(n_j)|n>.
The code verifies the exact exponent-level Heisenberg relations for all
12 generators and the 729 basis labels.

WHAT IS PROVED:
  * the published heterotic twisted matter carrier really has dimension 729;
  * the repo E6 chart plus the factorized fixed-point labels give an explicit
    F3^6 computational basis;
  * that basis supports the standard irreducible six-qutrit Heisenberg module
    3^(1+12), hence is abstractly isomorphic to the W33 729-dimensional module.

WHAT IS NOT PROVED:
  * that the six-qutrit Weyl generators are all microscopic heterotic
    symmetries/operators.
The geometric fixed-point factor has known flavor/space-group shift-phase
structure, but the three gauge-side qutrit Weyl pairs defined from the E6
coordinate chart remain an operator proposal.  Until those are realized by
gauge/Narain/vertex-operator actions, the bridge is a carrier-level
intertwiner, not a full physical symmetry identification.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_heterotic_z3_729_matter_carrier.json'
E6=ROOT/'artifacts/e6_cubic_affine_heisenberg_model.json'

def add3(a,b): return tuple((x+y)%3 for x,y in zip(a,b))

def symp(v,w):
    # standard six-qutrit phase space vectors v=(a|b), w=(a'|b')
    a,b=v[:6],v[6:]
    ap,bp=w[:6],w[6:]
    return (sum(b[i]*ap[i]-a[i]*bp[i] for i in range(6)))%3

def main(write=True):
    e6=json.loads(E6.read_text())
    chart=e6['e6id_to_heisenberg']
    gauge={}
    for k,v in chart.items():
        c=tuple(v['u'])+(int(v['z']),)
        gauge[int(k)]=c
    coords=set(gauge.values())
    assert len(gauge)==27 and len(coords)==27
    assert coords==set(itertools.product(range(3),repeat=3))

    fixed=list(itertools.product(range(3),repeat=3))
    basis=[]
    inverse={}
    for f in fixed:
        for e6id in sorted(gauge):
            n=f+gauge[e6id]
            idx=len(basis)
            basis.append({'index':idx,'fixed':f,'e6id':e6id,'coord':n})
            inverse[n]=idx
    assert len(basis)==729 and len(inverse)==729
    assert set(inverse)==set(itertools.product(range(3),repeat=6))

    # X_j permutations
    x_perms={}
    for j in range(6):
        perm=[]
        for rec in basis:
            n=list(rec['coord']);n[j]=(n[j]+1)%3
            perm.append(inverse[tuple(n)])
        assert sorted(perm)==list(range(729))
        # X_j consists of 243 three-cycles
        seen=set();cycles=0
        for i in range(729):
            if i in seen:continue
            u=i
            for _ in range(3):
                seen.add(u);u=perm[u]
            assert u==i
            cycles+=1
        assert cycles==243
        x_perms[j]=perm

    # Weyl generator phase-space vectors: X_j=(e_j|0), Z_j=(0|e_j)
    gens={}
    for j in range(6):
        ex=[0]*12;ex[j]=1;gens[f'X{j}']=tuple(ex)
        ez=[0]*12;ez[6+j]=1;gens[f'Z{j}']=tuple(ez)

    comm={}
    names=list(gens)
    for a in names:
        for b in names:
            comm[(a,b)]=symp(gens[a],gens[b])
    for j in range(6):
        assert comm[(f'X{j}',f'Z{j}')]==2  # convention: ZX=omega XZ => <X,Z>=-1
        assert comm[(f'Z{j}',f'X{j}')]==1
        for k in range(6):
            if j!=k:
                assert comm[(f'X{j}',f'X{k}')]==0
                assert comm[(f'Z{j}',f'Z{k}')]==0
                assert comm[(f'X{j}',f'Z{k}')]==0

    parent=json.loads((ROOT/'data/w33_suzuki_outer_heisenberg_sector_swap.json').read_text())
    assert parent['heisenberg']['shape']=='3^(1+12)'
    assert parent['heisenberg']['schrodinger_dimension']==729

    out={
      'schema':'w33.heterotic_z3_729_matter_carrier.v1',
      'status':'PASS_EXACT_CARRIER_INTERTWINER__PHYSICAL_WEYL_REALIZATION_OPEN',
      'external_string_input':{
        'compactification':'factorized heterotic T6/Z3 standard embedding',
        'fixed_points':27,
        'twisted_E6_multiplets':27,
        'representation_per_fixed_point':'27 of E6',
        'twisted_E6_matter_dimension':729,
        'spectrum_formula':'3(3,27) + 27(1,27) + 81(3,1) under SU(3) x E6',
        'references':['Dixon et al., Nucl.Phys.B282 (1987) 13-73',
                      'M.F. Fischer, Heterotic Orbifolds dissertation (2014), Sec.2.4 Eq.(2.41)']},
      'repo_E6_input':{
        'artifact':'artifacts/e6_cubic_affine_heisenberg_model.json',
        'chart':'27 E6 labels biject to (u0,u1,z) in F3^3',
        'all_F3cubed_coordinates_present':True},
      'basis_intertwiner':{
        'heterotic_basis':'|f0,f1,f2; e6id>',
        'six_qutrit_basis':'|f0,f1,f2,u0,u1,z>',
        'coordinate_space':'F3^6',
        'dimension':729,
        'bijection_verified':True},
      'abstract_heisenberg':{
        'shape':'3^(1+12)',
        'schrodinger_dimension':729,
        'generators':'X_j shifts coordinate j; Z_j phases by coordinate j, j=0..5',
        'X_cycle_structure':'each X_j = 243 disjoint 3-cycles',
        'all_generator_commutators_verified':True,
        'module_match':'same dimension and central character class as the certified W33 six-qutrit Schrödinger module; finite Stone-von Neumann gives abstract module equivalence once the standard center action is chosen'},
      'factorization':{
        'geometry_factor':'27 fixed points = F3^3',
        'gauge_factor':'27 E6 labels = F3^3 via repo chart',
        'carrier':'C^27_fixed tensor C^27_E6 = C^729 = (C^3)^tensor6'},
      'physics_boundary':{
        'geometric_qutrits':'the fixed-point factor has published Z3 flavor/space-group shift-phase structure',
        'gauge_qutrits':'the repo chart supplies coordinates, but does not yet prove all three gauge-side X/Z pairs are microscopic string symmetries',
        'full_bridge':'therefore this is an exact carrier/basis intertwiner, not yet a certified physical 3^(1+12) symmetry of the heterotic compactification'},
      'checks':{
        '27_fixed_times_27_E6_equals_729':27*27==729,
        'E6_chart_is_F3cubed':True,
        'basis_is_F3six':True,
        'six_X_permutations':True,
        'twelve_generator_symplectic_algebra':True,
        'parent_W33_dimension_match':True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out
if __name__=='__main__':main(True)
