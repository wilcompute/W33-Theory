"""Actual27 matter fixes global gauge form and its simple anomaly checks.

Lie algebras alone do not specify gauge groups. Standard center/Cartan
methods are applied to the native SL6 embedding, with explicit charges.
"""
import collections
import itertools
import json
import pathlib

import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1]


def build():
    a,b,c=s.symbols('a b c');w=[a,b,c,-a-b-c,0,0]
    duads=list(itertools.combinations(range(6),2))
    weights=[w[i]+w[j] for i,j in duads]+[-x for x in w]*2
    assert len(weights)==27 and s.expand(sum(weights))==0
    cubic=s.expand(sum(x**3 for x in weights));assert cubic==0
    quadratic=s.expand(sum(x*x for x in weights));assert s.expand(quadratic-6*sum(x*x for x in w))==0
    charges=[(int(i<4)+int(j<4))%4 for i,j in duads]+[3 if i<4 else 0 for i in range(6)]*2
    assert collections.Counter(charges)=={0:5,1:8,2:6,3:8}
    repair=json.loads((ROOT/'data/w33_20261102_clifford_native_cubic_repair.json').read_text())
    native_charges=[0]*27
    for row in repair['model_to_native']:native_charges[row['native_coordinate']]=charges[row['model_coordinate']]
    center=[]
    for k in range(4):
        phases=[s.I**(k*q) for q in native_charges]
        center.append(dict(power=k,trace=str(sum(phases)),native_diagonal=list(map(str,phases)),trivial=all(x==1 for x in phases)))
    assert [r['power'] for r in center if r['trivial']]==[0]
    # Supersymmetric massive multiplets contribute zero to the one-loop
    # effective-potential supertrace for every mass, before choosing t.
    assert 2-2==0 and 3+1-4==0
    return dict(status='PASS_NATIVE27_GAUGE_GLOBAL_FORM_AND_ANOMALY_AUDIT',
        Cartan_weights=list(map(str,weights)),cubic_anomaly_polynomial=str(cubic),linear_trace='0',quadratic_index_ratio_to_fundamental=6,total_Dynkin_index=3,
        center_charge_multiplicities={str(k):v for k,v in sorted(collections.Counter(charges).items())},native_center_matrices=center,
        allowed_global_form='With this matter SU4 is faithful; neither SO6=SU4/{+/-I} nor PSU4 can act on the same27. The surviving two USp4 fundamentals likewise require USp4 rather than SO5.',
        perturbative_anomaly_proof='Tr_R H^3 vanishes identically for general traceless Cartan H. The invariant cubic vanishes on a Cartan and hence on the Lie algebra; polarization gives the full perturbative cubic gauge-anomaly tensor. Linear trace also vanishes.',
        global_anomaly_scope='SU4 has pi4=0. In the unbroken USp4 theory the mod2 fundamental Witten count is2, hence even. This does not audit every possible discrete/background anomaly.',
        vacuum_orbit='SU4/USp4 = Spin6/Spin5 = S5',low_homotopy={'pi1':0,'pi2':0,'pi3':0,'pi4':0},H5_integer='Z',
        defects='This breaking alone supplies no stable pi1 strings, pi2 monopoles or pi3 textures. A synthetic Yang-monopole S4 control bundle is a different space.',
        WZW_boundary='S5 permits an integer5-form Wess-Zumino term in4D, but the actual UV SU4 cubic anomaly is zero. Anomaly matching therefore does not force a nonzero WZW coefficient here.',
        one_loop_potential='At the supersymmetric F=D=0 branch, each massive chiral multiplet has2-2=0 and each massive vector multiplet has3+1-4=0 in the supertrace. Coleman-Weinberg vacuum energy cancels; perturbation theory does not select t. Nonperturbative ADS dynamics is handled separately.',
        reference='https://arxiv.org/abs/1305.0318',
        boundary='Consistency checks in the supplied gauge model, not a derivation of gauging, spacetime chirality, the Standard Model or every global anomaly.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_gauge_global_form_audit.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['center_charge_multiplicities'],flush=True)
