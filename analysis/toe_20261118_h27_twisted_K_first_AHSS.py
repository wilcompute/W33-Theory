"""First forced AHSS differential for all nine H27 torsion B-field twists.

Y=(S^5 x T^2)/H27 has H^3(Y;Z)=F3^2, proved in
analysis/toe_20261119_h27_integral_torsion_gerbes.py.
The twisted complex K-theory d3 on the unit is +/-H; the integral
Steenrod component vanishes on 1. Thus a nonzero twist forces any
rank-like E_infinity degree-zero class to be divisible by 3. This is
only a necessary condition: higher AHSS differentials/extensions
could force larger rank (period-index issue).
"""
from pathlib import Path
from itertools import product
import json

ROOT=Path(__file__).resolve().parents[1]

def period(v):
    for n in (1,2,3):
        if all((n*x)%3==0 for x in v):
            return n
    raise AssertionError(v)

def ray(v):
    a,b=v
    assert (a,b)!=(0,0)
    if a:
        inv=pow(a,-1,3)
        return (1,(b*inv)%3)
    return (0,1)

def main():
    twists=[(a,b) for a,b in product(range(3),repeat=2)]
    representatives={str(t):{"d3_of_unit":t,
                             "first_d3_kernel_subgroup_of_Z":f"{period(t)}Z",
                             "necessary_rank_multiple":period(t),
                             "projective_ray":ray(t) if t!=(0,0) else None}
                     for t in twists}
    rays={ray(t) for t in twists if t!=(0,0)}
    assert len(twists)==9 and len(rays)==4
    assert sum(period(t)==3 for t in twists)==8
    assert all(sum(ray(t)==r for t in twists if t!=(0,0))==2 for r in rays)
    out={"space":"Y7=(S5 x T2)/H27","H3_integral":"(Z3)^2",
         "nine_twists":representatives,
         "nontrivial_twists":8,"projective_rays":[list(x) for x in sorted(rays)],
         "twisted_AHSS_first_differential":"d3(1)= +/-H in H^3(Y;Z); d3(n)= +/-nH",
         "nonzero_twist_necessary_rank_condition":"rank divisible by 3",
         "untwisted_rank_condition":"no rank divisibility forced by d3(1)",
         "caveat":"Does NOT compute full twisted K^*(Y), prove existence of rank-3 twisted bundles, determine the actual topological index, or claim a brane compactification."}
    path=ROOT/"data"/"toe_20261118_h27_twisted_K_first_AHSS.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print("PASS nine twists / eight nontrivial / four rays; d3 unit kills primitive rank for nonzero twists")
    print(path)
    return out

if __name__=="__main__":
    main()
