"""Finite topological string-charge orbits vs genuine spinor deck modes.

Formal IIB F1/D1 species charges (m,n) in Z² can be tensored with
H1(Y;Z)=Z_g for a circle bundle Y(p,q) over S²xS².  The resulting
Z_g² module has SL(2,Z)-orbits labelled by gcd(m,n,g).
This is a topology-only candidate module, not a physical string spectrum
or a conserved charge group once endpoints, flux and branes are included.
"""
from collections import deque
from math import gcd
import json, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_spin_winding_SL2_orbits.json"
sp=importlib.util.spec_from_file_location("spin",ROOT/"analysis"/"toe_20261116_R4_threshold_spinor_modes.py")
spin=importlib.util.module_from_spec(sp);sp.loader.exec_module(spin)

def totient_two(n:int)->int:
    if n<1:raise ValueError("n positive")
    z=n*n
    t=n
    prime=2
    while prime*prime<=t:
        if t%prime==0:
            z=z//(prime*prime)*(prime*prime-1)
            while t%prime==0:t//=prime
        prime+=1
    if t>1:z=z//(t*t)*(t*t-1)
    return z

def orbit_table(g:int):
    if g<1:raise ValueError("g positive")
    unseen={(a,b) for a in range(g) for b in range(g)}
    table=[]
    while unseen:
        origin=min(unseen)
        seen={origin}
        todo=deque([origin])
        while todo:
            a,b=todo.popleft()
            # S and T generate SL(2,Z); both have finite images modulo g.
            for v in ((-b%g,a%g),((a+b)%g,b)):
                if v not in seen:
                    seen.add(v);todo.append(v)
        unseen.difference_update(seen)
        label=gcd(g,*origin)
        assert all(gcd(g,*v)==label for v in seen)
        expected=totient_two(g//label)
        assert len(seen)==expected
        table.append({"gcd_divisor":label,"orbit_cardinality":len(seen),
                      "Jordan_totient_J2":expected,"representative":origin})
    table.sort(key=lambda z:z["gcd_divisor"])
    assert sum(v["orbit_cardinality"] for v in table)==g*g
    return {"g":g,"module":"Z_g x Z_g","number_of_orbits":len(table),
            "orbits":table}

def compare_spin_and_species(N):
    d=spin.spinor_deck_table(N)
    return {"N":N,"spinor_cover_modes_survive":d["surviving_cover_Killing_spinor_mode"],
            "spin_lifts":d["lifts"],
            "formal_F1_D1_winding_orbits":orbit_table(N),
            "physical_nonidentification":"Deck residue k labels fermion Fourier transformation; the (m,n) module is string species tensored with a finite order fiber loop. Matching counts does not identify these spectra."}

def quantized_flux_topology_jump(N:int):
    """Compare equal and nearly equal mixed charges at fixed large N."""
    if N<2:raise ValueError("N>=2")
    ge=gcd(N,N)
    gn=gcd(N+1,N)
    assert ge==N and gn==1
    return {
        "N":N,"equal_mixed_periods":[N,N],
        "near_equal_mixed_periods":[N+1,N],
        "relative_flux_ratio_difference":1/N,
        "equal_pi1":f"Z_{ge}","near_equal_pi1":"trivial",
        "equal_complex_K0_torsion_order":ge*ge,
        "near_equal_complex_K0_torsion_order":1,
        "equal_spin_structure_count":2 if N%2==0 else 1,
        "near_equal_spin_structure_count":1,
        "near_equal_Y_diffeomorphic":"S2 x S3",
        "critical_scope":"Global torsion homotopy and K-theory jump despite smooth local 11D geometric parameter convergence. Contractible string windings can remain dynamical, non-topologically protected excitations."
    }

def verify():
    cases=[compare_spin_and_species(g) for g in (1,2,3,4,5,6,8,9,12)]
    six=orbit_table(6)["orbits"]
    assert [(x["gcd_divisor"],x["orbit_cardinality"]) for x in six]==[(1,24),(2,8),(3,3),(6,1)]
    assert [r["N"] for r in cases if r["spinor_cover_modes_survive"]]==[1,2]
    for r in cases:
        assert sum(x["orbit_cardinality"] for x in r["formal_F1_D1_winding_orbits"]["orbits"])==r["N"]**2
    return {"status":"PASS_SL2Z_TORSION_ORBIT_AND_SPINOR_DECK_SEPARATION",
            "arithmetic_theorem":"SL2(Z) orbits on (Z_g)^2 indexed by d=gcd(g,m,n) with size J2(g/d)",
            "six_flux_orbit_sizes":[x["orbit_cardinality"] for x in six],
            "no_physical_duality_spectrum_calculated":True,
            "caveat":"Finite topological charges are not an integer oscillator spectrum or proof of RR Page charge conservation.",
            "equal_vs_coprime_flux_topology_jump":[quantized_flux_topology_jump(n) for n in (2,3,10,100,1000)],
            "cases":cases}
if __name__=="__main__":
    o=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(o["status"],o["six_flux_orbit_sizes"])
