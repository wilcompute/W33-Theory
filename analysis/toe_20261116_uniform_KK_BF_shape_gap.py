"""Sharp shape-uniform BF instability theorem at equal M-theory flux.

At N0=N1=N2=N, square/shape torus spectrum has
lambda(m,n)=3*pi*|m+n*tau|^2/Im(tau).
For any unit-covolume lattice shortest squared length Q1<=2/sqrt(3).
Thus shortest lambda1<=2*pi*sqrt(3). If lambda1<1,
multiply its shortest primitive vector by ceil(1/sqrt(lambda1))
to get a harmonic lambda in [1,4); otherwise use the shortest vector.
Consequently every flat shape has a mode lambda in [1,2*pi*sqrt(3)].
The BF deficit delta(lambda)=sqrt(4+16*lambda)-lambda-2 has
its sole maximum at 15/4 and positive minimum on that interval at
lambda=2*pi*sqrt(3). Hexagonal tau=e^(i*pi/3) attains that minimum,
since its only unstable shell has Eisenstein norm 1; norm 2 is
impossible modulo 3 and norm>=3 exceeds lambda=12. Sharp theorem.
"""
import math,json,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_uniform_KK_BF_shape_gap.json"
sp=importlib.util.spec_from_file_location("winding",ROOT/"analysis"/"toe_20261116_circle_bundle_ring_winding_lattice.py")
winding=importlib.util.module_from_spec(sp);sp.loader.exec_module(winding)

def gap(lam):
    if lam<=0 or lam>=12:return 0.0
    return math.sqrt(4+16*lam)-lam-2

def exact_shape_theorem():
    lhex=2*math.sqrt(3)*math.pi
    deltahex=gap(lhex)
    d1=gap(1)
    assert 1<lhex<12 and 0<deltahex<d1
    return {
      "BF_depth_away_from_bound_in_m2L2":deltahex,
      "sharp_minimum_over_torus_shapes":"sqrt(4+32*pi*sqrt(3)) - 2*pi*sqrt(3) - 2",
      "hexagonal_shortest_lambda":lhex,
      "gap_at_lambda_1":d1,
      "shortest_lambda_universal_upper_bound":lhex,
      "witness_selection":"If lambda1>=1, use primitive shortest vector; if lambda1<1, use ceil(1/sqrt(lambda1)) times shortest vector.",
      "guaranteed_witness_lambda_interval":[1,lhex],
      "hex_optimality":"At hexagonal shape norm a^2+a*b+b^2 is never 2 mod 3; next shell >=3 and lambda >=3*lambdahex >12, so only shortest shell contributes.",
      "limitation":"Classical two-derivative physical sphere-odd KK subsystem at equal flux; not a theorem for unequal flux, higher-derivative corrections or varying Planck-scale torus cycles."
    }

def reduced_witness(tau:complex):
    x,y=tau.real,tau.imag
    if y<=0 or abs(x)>.5+1e-9 or abs(tau)<1-1e-9:raise ValueError("reduced fundamental-domain tau required")
    # In the standard reduced domain Qmin=1/y, attained by (m,n)=(1,0).
    lam1=3*math.pi/y
    harmonic=1 if lam1>=1 else math.ceil(1/math.sqrt(lam1))
    lam=harmonic*harmonic*lam1
    h=exact_shape_theorem()
    assert lam>=1-1e-9 and lam<=h["hexagonal_shortest_lambda"]+1e-8
    d=gap(lam)
    assert d>=h["BF_depth_away_from_bound_in_m2L2"]-1e-9
    return {"tau":[x,y],"first_lambda":lam1,
            "witness_Fourier_label":[harmonic,0],
            "witness_lambda":lam,"witness_BF_gap":d}

def verify():
    hexshape=.5+math.sqrt(3)/2*1j
    examples=[1j,hexshape,.3+1.2j,2j,10j,100j,10000j,1000000j]
    rows=[]
    best=exact_shape_theorem()
    for tau in examples:
        witness=reduced_witness(tau)
        census=winding.winding_census(1,1,tau)
        maximal=max((gap(v["lambda"]) for v in census["modes"]),default=0)
        assert maximal>=witness["witness_BF_gap"]-1e-9
        assert maximal>=best["BF_depth_away_from_bound_in_m2L2"]-1e-9
        witness["max_actual_BF_gap"]=maximal
        witness["BF_violating_signed_Fourier_labels"]=len(census["modes"])
        rows.append(witness)
    assert abs(rows[1]["max_actual_BF_gap"]-best["BF_depth_away_from_bound_in_m2L2"])<1e-10
    assert rows[1]["BF_violating_signed_Fourier_labels"]==6
    # By Eisenstein norm modulo 3: a²+ab+b²=(a-b)² mod3
    assert all(((a*a+a*b+b*b)%3)!=2 for a in range(-5,6) for b in range(-5,6))
    return {"status":"PASS_SHARP_UNIFORM_BF_GAP_FOR_ALL_EQUAL_FLUX_TORUS_SHAPES",
            "theorem":best,
            "samples":rows,
            "scope":"Exact shape-uniform lower bound within the specific classical equal-flux 11D KK subsystem. No full quantum vacuum-stability conclusion."}

if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(r["status"],r["theorem"]["BF_depth_away_from_bound_in_m2L2"])
