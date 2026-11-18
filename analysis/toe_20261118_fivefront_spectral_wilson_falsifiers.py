"""Five orthogonal Klein/W33 falsifiers. Arithmetic models, NOT a physical TOE."""
from __future__ import annotations
import json
from itertools import combinations
from math import fsum
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = (1, 9, 4, 3, 5)

def monomials(n, d):
    if n == 1:
        yield (d,)
        return
    for a in range(d + 1):
        for tail in monomials(n - 1, d - a):
            yield (a,) + tail

def c11_ambient(d):
    counts = [0] * 11
    for e in monomials(5, d):
        counts[sum(a*b for a,b in zip(e, WEIGHTS)) % 11] += 1
    return counts

def c5_ambient_on_c11_fixed(d):
    remaining = {e for e in monomials(5, d)
                 if sum(a*b for a,b in zip(e, WEIGHTS)) % 11 == 0}
    counts = [0] * 5
    while remaining:
        start = next(iter(remaining))
        orbit = {start}
        nxt = start[1:] + start[:1]
        while nxt != start:
            orbit.add(nxt)
            nxt = nxt[1:] + nxt[:1]
        assert orbit <= remaining and len(orbit) in (1, 5)
        remaining -= orbit
        if len(orbit) == 1:
            counts[0] += 1
        else:
            counts = [c + 1 for c in counts]
    return counts

def subtract_defining_cubic(ambient, previous):
    v = [a-b for a,b in zip(ambient, previous)]
    assert min(v) >= 0
    return v

def holomorphic_character_towers(max_degree=10):
    full = []
    c11 = []
    for deg in range(max_degree + 1):
        amb5 = c5_ambient_on_c11_fixed(deg)
        prev5 = c5_ambient_on_c11_fixed(deg-3) if deg >= 3 else [0]*5
        amb11 = c11_ambient(deg)
        prev11 = c11_ambient(deg-3) if deg >= 3 else [0]*11
        full.append(subtract_defining_cubic(amb5, prev5))
        c11.append(subtract_defining_cubic(amb11, prev11))
    assert full[0] == [1,0,0,0,0]
    assert full[1] == full[2] == [0]*5
    assert full[3] == [0,1,1,1,1]
    assert full[4] == [1,1,1,1,1]
    assert c11[3][0] == 4 and sum(c11[3]) == 34
    assert c11[1][0] == 0 and sum(c11[1]) == 5
    assert [sum(row) for row in full[:11]] == [1,0,0,4,5,11,15,25,34,45,61]
    def first_and_eig(table, nchars):
        out = []
        for char in range(nchars):
            first = next((d for d, row in enumerate(table) if row[char] and d > 0), None)
            q = 2*first if first is not None else None
            out.append(dict(character=char, first_degree=first,
                            first_multiplicity=table[first][char] if first is not None else 0,
                            Reeb_charge=q, scalar_laplacian=q*(q+6) if q is not None else None))
        return out
    return dict(full_F55_C5_character_coefficients=full,
                C11_character_coefficients=c11,
                F55_first_modes=first_and_eig(full,5),
                C11_first_modes=first_and_eig(c11,11),
                caveat="Holomorphic flat-line sectors only; not the complete twisted or untwisted KK spectrum.")

def su5_wilson_ledger():
    weights = (2,2,2,-3,-3)
    assert sum(weights) == 0
    assert all(w % 11 != 0 for w in weights)
    roots = [(weights[i]-weights[j]) % 11 for i in range(5)
             for j in range(5) if i != j]
    invariant_roots = roots.count(0)
    assert invariant_roots == 8
    matter = ([((weights[i]+weights[j])%11) for i,j in combinations(range(5),2)]
              + [(-w)%11 for w in weights] * 2
              + [w%11 for w in weights] + [0,0])
    assert len(matter) == 27 and matter.count(0) == 2
    valid_c5 = [(a,b) for a in range(5) for b in range(5)
                if (3*a+2*b)%5 == 0]
    assert valid_c5 == [(a,a) for a in range(5)]
    return dict(C11_wilson_weights=list(weights), exact_order=11,
                unbroken_adjoint_roots=invariant_roots, Cartan=4,
                unbroken_SU5_dimension=invariant_roots+4,
                broken_SU5_dimension=24-(invariant_roots+4),
                E6_27_SU5_branches="10 + 5bar + 1 + 5 + 5bar + 1",
                matter_27_phase_multiplicities={str(k):matter.count(k) for k in range(11)},
                phase_zero_matter_components=matter.count(0),
                C5_compatible_3plus2_holonomies=valid_c5,
                flat_Dirac_Friedrich_eigenvalue_squared_bound=">=49/4",
                caveat="The 2/27 count concerns invariant constant SU5 fibers, not full 4D chiral matter; flux-coupled/localized operators are untested.")

def gq_continuum_obstruction(qs=(2,3,4,5,7,9,11)):
    rows = []
    for q in qs:
        v=(q+1)*(q*q+1)
        k=q*(q+1)
        r=q-1
        s=-(q+1)
        mr=(-k-s*(v-1))//(r-s)
        ms=v-1-mr
        assert mr*(r-s) == -k-s*(v-1)
        assert k+mr*r+ms*s == 0
        assert k*k+mr*r*r+ms*s*s == v*k
        lo = (k-r)/k
        hi = (k-s)/k
        assert lo > 0 and hi >= lo
        rows.append(dict(q=q, v=v, degree=k, diameter=2,
                         adjacency_eigenvalues=[k,r,s],
                         multiplicities=[1,mr,ms],
                         normalized_laplacian_nonzero=[lo,hi],
                         spectral_ratio=hi/lo))
    assert rows[1]["v"] == 40 and rows[1]["degree"] == 12
    assert rows[1]["multiplicities"] == [1,24,15]
    return dict(rows=rows,
                theorem="All W(3,q) collinearity graphs have diameter 2 and only two distinct positive normalized Laplacian eigenvalues; they cannot spectrally converge, under any common scalar rescaling, to the full Laplace spectrum of a fixed positive-dimensional compact smooth manifold.",
                caveat="Does not exclude geometric limits of derived incidence complexes, sparse subgraphs, weighted/nonlocal operators, or renormalized multiscale systems.")

def binomial_tail(n,p):
    # P(X>=k) for k=0,...,n+1; stable for the n<=500 benchmarks here.
    pmf=[0.0]*(n+1)
    pmf[n]=p**n
    for k in range(n-1,-1,-1):
        pmf[k]=pmf[k+1]*(k+1)/(n-k)*(1-p)/p
    tail=[0.0]*(n+2)
    for k in range(n,-1,-1):
        tail[k]=tail[k+1]+pmf[k]
    assert abs(tail[0]-1) < 1e-10
    return tail

def min_binomial_test(p0,p1,alpha=.01,beta=.01,max_n=1000):
    assert 0 < p0 < p1 < 1
    for n in range(1,max_n+1):
        null=binomial_tail(n,p0)
        alternative=binomial_tail(n,p1)
        for k in range(1,n+1):
            if null[k] <= alpha and 1-alternative[k] <= beta:
                return dict(accepted_events=n, decision_threshold_plus_clicks=k,
                            type_I=null[k], type_II=1-alternative[k],
                            p0_worst=p0,p1_worst=p1)
    raise ValueError("No threshold found")

def photonic_budget():
    ideal=min_binomial_test(.5,.65)
    assert (ideal["accepted_events"],ideal["decision_threshold_plus_clicks"])==(235,136)
    eta_ratio=1.1
    worst_null=eta_ratio/(1+eta_ratio)
    worst_alt=(.65/eta_ratio)/(.65/eta_ratio+.35)
    robust=min_binomial_test(worst_null,worst_alt)
    assert (robust["accepted_events"],robust["decision_threshold_plus_clicks"])==(490,283)
    return dict(null="Conditional P(+)=0.5",alternative="Conditional P(+)=0.65",
                one_sided_exact_Neyman_Pearson=ideal,
                max_relative_arm_efficiency_ratio=eta_ratio,
                efficiency_envelope_robust=robust,
                caveat="Accepted-event IID binomial trials with independently certified arm-efficiency ratio; no claim of observed W33 hardware or loophole-free inference.")

def t11_winding_modular_bound():
    """Conditional on the published/repo mixed winding-radion mass branch."""
    from math import pi, sqrt
    # On SL2(Z) fundamental domain, Im(tau)>=sqrt(3)/2 and
    # shortest |u+v*tau| is 1, so shortest^2/Im(tau)<=2/sqrt(3).
    crit_universal=2*sqrt(3)/pi
    crit_square=4/pi
    assert 1 < crit_universal < crit_square
    def spectrum(shortest_covolume_normalized, ratio_N0_over_N):
        lam=3*pi*ratio_N0_over_N*shortest_covolume_normalized
        mass=lam-2-sqrt(4+16*lam)
        return dict(lambda_winding=lam, m2_L2=mass,
                    BF_deficit=max(0.0,-4-mass), BF_violated=(-4-mass)>1e-12)
    at_square=spectrum(1.0,1.0)
    at_hex=spectrum(2/sqrt(3),1.0)
    assert at_square["BF_violated"] and at_hex["BF_violated"]
    for lam in (0.01,1,6,11.999):
        assert (lam-2-sqrt(4+16*lam)) < -4
    for lam in (12,12.01,13,100):
        assert (lam-2-sqrt(4+16*lam)) >= -4-1e-12
    return dict(square_modulus_ratio1=at_square,
                hexagonal_modulus_ratio1=at_hex,
                critical_ratio_all_axiodilatons=crit_universal,
                critical_ratio_square=crit_square,
                theorem="If 0<N0/N<2sqrt(3)/pi, at least one winding lattice mode lies in the 0<lambda<12 AdS5 BF-violating interval for every axiodilaton tau, within the stated quadratic mixed-mode model.",
                derivation="m_minus^2+4=lambda+2-sqrt(4+16lambda), negative iff 0<lambda<12. Planar lattice Hermite bound shortest^2/Im(tau)<=2/sqrt(3) yields lambda_min<=2sqrt(3)*pi*N0/N.",
                caveat="Only the mixed mode of the 11D two-derivative truncation and its IIB winding dictionary; not full string stability, source-induced shifts or a full physical mode analysis.")

def torsion_and_local_flux():
    sectors=[dict(index=x,crt_mod3=x%3,crt_mod5=x%5) for x in range(15)]
    assert len({(s["crt_mod3"],s["crt_mod5"]) for s in sectors}) == 15
    assert [x for x in range(15) if x%3==0 and x%5==0] == [0]
    return dict(flat_degree4_Cfield_holonomy_classes="Z15",sector_CRT=sectors,
                flat_curvature_G4="0 in real de Rham cohomology",
                bulk_linearization="A flat torsion choice alone does not change the local two-derivative metric/G4 curvature equations. It can affect global/wrapped-brane observables and quantum refinements.",
                caveat="No calculation of complete 11D KK masses, T11 IIB winding modes, Page charges, nonperturbative sectors, or BF stability. No claim that all sectors are dynamically equivalent.")

def main():
    result=dict(holo=holomorphic_character_towers(),
                E6_Wilson=su5_wilson_ledger(),
                continuum=gq_continuum_obstruction(),
                photon=photonic_budget(),
                T11_winding=t11_winding_modular_bound(),
                torsion=torsion_and_local_flux())
    out=ROOT/"data/toe_20261118_fivefront_spectral_wilson_falsifiers.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS five independent controls",out)
    print("F55 modes:",result["holo"]["F55_first_modes"])
    print("C11 constant matter singlets:",result["E6_Wilson"]["phase_zero_matter_components"])
    print("T11 universal threshold N0/N:",result["T11_winding"]["critical_ratio_all_axiodilatons"])
    print("Photon accepted events:",result["photon"]["one_sided_exact_Neyman_Pearson"]["accepted_events"],
          result["photon"]["efficiency_envelope_robust"]["accepted_events"])
    return result

if __name__=="__main__":
    main()
