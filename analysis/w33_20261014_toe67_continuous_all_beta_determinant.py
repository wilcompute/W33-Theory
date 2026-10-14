"""TOE67 exact all-temperature continuous three-deck W33 fermion flux theorem.

Uniform hopping, finite 80-site free bipartite model with 3 flat deck phases.
Exact Gaussian-integer charpolys -> complete Fourier coefficients -> proof.
Not a dynamical gauge or physical Theory of Everything theorem.
"""
from __future__ import annotations
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import sys
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33

PHASE=(sp.Integer(1),sp.I,sp.Integer(-1),-sp.I)
MODES=tuple(product((-1,0,1),repeat=3))
GRID=tuple(product(range(4),repeat=3))

def native_three_chords():
    *_,flags,_=build_w33()
    edges=[(int(p),40+int(line)) for p,line in flags]
    assert len(edges)==160 and all(a<40<=b for a,b in edges)
    parents=list(range(80))
    def root(j):
        while parents[j]!=j:
            parents[j]=parents[parents[j]]
            j=parents[j]
        return j
    tree=set()
    for i,(a,b) in enumerate(edges):
        ra,rb=root(a),root(b)
        if ra!=rb:
            parents[ra]=rb
            tree.add(i)
    assert len(tree)==79
    chords=[i for i in range(160) if i not in tree]
    selected=tuple(chords[j] for j in (5,30,65))
    assert selected==(59,93,139)
    return edges,selected

def quarter_sample_coefficients(edges,selected,ks):
    B=sp.zeros(40,40)
    for i,(a,b) in enumerate(edges):
        B[a,b-40]=PHASE[ks[selected.index(i)]] if i in selected else 1
    x=sp.Symbol("x")
    char=sp.Poly((B*B.conjugate().T).charpoly(x).as_expr(),x)
    fixed=sp.Poly(x**12*(x-6)**18,x)
    quotient,remainder=divmod(char,fixed)
    assert remainder.is_zero and quotient.degree()==10
    e=[int((-1)**k*v) for k,v in enumerate(quotient.all_coeffs())]
    assert e[:4]==[1,52,1116,12960]
    return e

def recover_exact_fourier(samples):
    # Cauchy-Binet: minor determinant is affine in each unique phase entry.
    # Modulus square has only Laurent frequencies {-1,0,1} per coordinate.
    # A 4-point DFT in each angle therefore has NO aliasing.
    coefs={}
    for mode in MODES:
        values=[]
        for k in range(11):
            real=imag=0
            for ks,arr in samples.items():
                phase=(-sum(n*j for n,j in zip(mode,ks)))%4
                v=arr[k]
                if phase==0: real+=v
                elif phase==1: imag+=v
                elif phase==2: real-=v
                else: imag-=v
            assert imag==0 and real%64==0,(mode,k,real,imag)
            values.append(real//64)
        coefs[mode]=tuple(values)
    assert all(coefs[m]==coefs[tuple(-n for n in m)] for m in MODES)
    assert all(coefs[m][k]==0 for k in range(4) for m in MODES if m!=(0,0,0))
    return coefs

def positivity_certificate(coefs):
    # e_k(pi)-e_k(pi+delta) =
    # sum_{one representative ±n} 2*c_kn*(-1)^sum(n)*(1-cos(n.delta)).
    # For |support(n)|=m:
    # 1-cos(n.delta) <= m*sum_{j in support(n)}(1-cos delta_j).
    output=[]
    for k in range(4,11):
        signed={}
        for n in MODES:
            if n==(0,0,0) or n<tuple(-a for a in n): continue
            a=2*coefs[n][k]*(1 if sum(n)%2==0 else -1)
            if a: signed[n]=a
        singles=[signed[(1,0,0)],signed[(0,1,0)],signed[(0,0,1)]]
        cost=[0,0,0]
        for n,a in signed.items():
            if a>=0: continue
            m=sum(abs(x) for x in n)
            for j,x in enumerate(n):
                if x:cost[j]+=-a*m
        margin=[a-b for a,b in zip(singles,cost)]
        assert min(margin)>0,(k,singles,cost)
        output.append({"degree":k,"positive_single_axis":singles,
            "negative_cross_mode_cost":cost,"strict_coordinate_margin":margin,
            "negative_cross_modes":{str(n):a for n,a in signed.items() if a<0}})
    return output

def certificate():
    edges,selected=native_three_chords()
    samples={ks:quarter_sample_coefficients(edges,selected,ks) for ks in GRID}
    modes=recover_exact_fourier(samples)
    rows=positivity_certificate(modes)
    assert [min(x["strict_coordinate_margin"]) for x in rows]==[
        138,3344,29664,121056,221568,89088,13728]
    pi=samples[(2,2,2)]
    zero=samples[(0,0,0)]
    assert all(sum(modes[n][k]*(1 if sum(n)%2==0 else -1)
                   for n in MODES)==pi[k] for k in range(11))
    assert pi[10]>0 and zero[7]>0 and zero[8:]==[0,0,0]
    assert math.comb(24,12)==2704156
    assert math.comb(30,15)==155117520
    serial="\n".join(str(ks)+":"+",".join(map(str,samples[ks])) for ks in GRID)
    return {
        "status":"PASS_TOE67_EXACT_CONTINUOUS_ALL_BETA_FLUX_THEOREM",
        "W33_vertices":80,"W33_Levi_edges":160,
        "phase_chord_indices":list(selected),"exact_quarter_phase_samples":64,
        "full_characteristic_polynomial_factor":"x^12 (x-6)^18 Q_10(x;theta)",
        "flat_zero_singular_values_at_least":12,
        "flat_sqrt6_singular_values_at_least":18,
        "active_polynomial_degree":10,
        "fourier_laurent_support":"(-1,0,+1)^3; exact from minor multilinearity",
        "coefficients_e0_through_e10_at_pi":pi,"margin_table":rows,
        "fourier_coefficients":{str(n):list(v) for n,v in modes.items() if any(v)},
        "quarter_sample_sha256":hashlib.sha256(serial.encode()).hexdigest(),
        "flatband_entropy_obstruction":{
            "minimum_zero_one_particle_states_for_any_flat_phase":24,
            "exact_zero_one_particle_states_at_three_pi":24,
            "exact_zero_one_particle_states_at_trivial_phase":30,
            "canonical_N40_many_body_zero_shell_degeneracy_lower":math.comb(24,12),
            "canonical_N40_many_body_zero_shell_degeneracy_at_zero_phase":math.comb(30,15),
            "grand_canonical_zero_mode_entropy_lower_at_mu0":"24*k_B*ln(2)",
            "implication":"Massless static uniform three-deck hopping has no unique gapped half-filled many-body vacuum despite unique flux free-energy minimizer."
        },
        "theorem":"det(I+t B_pi B_pi*) > det(I+t B_theta B_theta*) for every t>0 and theta != pi modulo 2pi, by exact coefficientwise nonnegative differences and strict degree-four margin. Via cosh's Weierstrass product, pi uniquely minimizes free energy at every beta>0 for this noninteracting half-filled uniform three-deck model, including arbitrary common real sublattice-staggered mass.",
        "scope":"Finite static free spinless W33, uniform links, three selected flat U(1) coordinates; not interacting matter, arbitrary link disorder, dynamical gauge fields, Lorentz gravity, CP violation or physical TOE."
    }

if __name__=="__main__":
    data=certificate()
    (ROOT/"data/w33_20261014_toe67_continuous_all_beta_determinant.json").write_text(
        json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(data["status"],[min(x["strict_coordinate_margin"]) for x in data["margin_table"]])
